"""Hardware recorder module for audio-visual speech capture.

This module owns camera and microphone hardware devices for the Auralens
project. Per AGENTS.md rules:
- Only ONE capture module owns camera and microphone devices.
- Audio and video frames have shared timestamps (milliseconds from start of recording).
- Monotonic clock (time.perf_counter) is used for all recording timestamps.
- Audio after capture is normalized to 1D mono float32, 16 kHz with finite values.
- Device indices and settings are configuration-driven.
"""

from __future__ import annotations

import logging
import math
import threading
import time
from typing import Any, Dict, List, Optional, Tuple, Type, Union

import cv2
import numpy as np
import sounddevice as sd

logger = logging.getLogger(__name__)


class Recorder:
    """Audio-visual recorder owning camera and microphone devices.

    Records 16 kHz mono float32 audio and timestamped BGR video frames
    with shared monotonic millisecond timestamps from recording start.
    """

    def __init__(
        self,
        camera_index: int = 0,
        audio_device: Optional[Union[int, str]] = None,
        sample_rate: int = 16000,
        max_duration_s: Optional[float] = 15.0,
        max_frames: Optional[int] = 450,
    ) -> None:
        """Initialize recorder configuration without opening hardware devices.

        Args:
            camera_index: Camera device index for OpenCV VideoCapture (default 0).
            audio_device: Sounddevice input device index or name (default None for system default).
            sample_rate: Audio sampling rate in Hz (default 16000).
            max_duration_s: Wall-clock cap for one turn in seconds, so a forgotten
                Stop does not exhaust RAM (None disables the cap). Frames are
                ~0.9 MB each at 640×480, so 15 s at 30 fps is ~420 MB worst case.
            max_frames: Secondary cap on buffered frames (None disables it).

        Raises:
            ValueError: If a cap is zero or negative.
        """
        if max_duration_s is not None and max_duration_s <= 0:
            raise ValueError(f"max_duration_s phải > 0, nhận được: {max_duration_s!r}")
        if max_frames is not None and max_frames <= 0:
            raise ValueError(f"max_frames phải > 0, nhận được: {max_frames!r}")

        self.camera_index = camera_index
        self.audio_device = audio_device
        self.sample_rate = sample_rate
        self.max_duration_s = max_duration_s
        self.max_frames = max_frames

        self._camera: Optional[cv2.VideoCapture] = None
        self._audio_stream: Optional[sd.InputStream] = None

        self._is_open: bool = False
        self._is_recording: bool = False

        self._recording_start_time: float = 0.0
        self._sample_id: Optional[str] = None
        self._limit_reached: bool = False
        self._limit_reason: Optional[str] = None
        self._frame_count: int = 0

        self._audio_chunks: List[np.ndarray] = []
        self._video_frames: List[Tuple[int, np.ndarray]] = []

        self._video_thread: Optional[threading.Thread] = None
        self._audio_lock = threading.Lock()
        self._video_lock = threading.Lock()
        self._state_lock = threading.RLock()

        # Initialize device info with default/configured settings
        self._device_info: Dict[str, Any] = {
            "camera_index": self.camera_index,
            "camera_resolution": (0, 0),
            "camera_width": 0,
            "camera_height": 0,
            "mic_device_name": str(self.audio_device if self.audio_device is not None else "default"),
            "mic_device": self.audio_device if self.audio_device is not None else "default",
        }

    @property
    def is_open(self) -> bool:
        """Whether camera and microphone devices are currently open."""
        return self._is_open

    @property
    def is_recording(self) -> bool:
        """Whether a recording session is currently active."""
        return self._is_recording

    @property
    def limit_reached(self) -> bool:
        """Whether capture stopped buffering because a limit was reached."""
        return self._limit_reached

    @property
    def device_info(self) -> Dict[str, Any]:
        """Snapshot of the real device information gathered in open().

        Returned as a copy so callers cannot mutate the recorder's state.
        """
        with self._state_lock:
            return dict(self._device_info)

    def open(self) -> None:
        """Open camera and start audio stream.

        Raises:
            RuntimeError: If camera or microphone fails to open.
        """
        with self._state_lock:
            if self._is_open:
                return

            # 1. Open camera device via OpenCV VideoCapture
            try:
                self._camera = cv2.VideoCapture(self.camera_index)
                if self._camera is None or not self._camera.isOpened():
                    raise RuntimeError(
                        f"Không mở được camera (device index: {self.camera_index})"
                    )
            except Exception as exc:
                self.close()
                if isinstance(exc, RuntimeError) and "Không mở được camera" in str(exc):
                    raise
                raise RuntimeError(f"Không mở được camera: {exc}") from exc

            # Query camera resolution
            try:
                cam_w = int(self._camera.get(cv2.CAP_PROP_FRAME_WIDTH))
                cam_h = int(self._camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
            except Exception:
                cam_w, cam_h = 0, 0

            # 2. Query mic device info and start audio input stream
            try:
                try:
                    if self.audio_device is not None:
                        dev_info = sd.query_devices(self.audio_device, "input")
                    else:
                        dev_info = sd.query_devices(kind="input")
                    mic_name = (
                        dev_info.get("name", "Unknown")
                        if isinstance(dev_info, dict)
                        else str(dev_info)
                    )
                except Exception:
                    mic_name = str(self.audio_device if self.audio_device is not None else "default")

                self._audio_stream = sd.InputStream(
                    samplerate=self.sample_rate,
                    channels=1,
                    dtype="float32",
                    device=self.audio_device,
                    callback=self._audio_callback,
                )
                self._audio_stream.start()
            except Exception as exc:
                self.close()
                raise RuntimeError(f"Không mở được micro: {exc}") from exc

            self._device_info = {
                "camera_index": self.camera_index,
                "camera_resolution": (cam_w, cam_h),
                "camera_width": cam_w,
                "camera_height": cam_h,
                "mic_device_name": mic_name,
                "mic_device": self.audio_device if self.audio_device is not None else "default",
            }
            self._is_open = True

    def _audio_callback(
        self,
        indata: np.ndarray,
        frames: int,
        time_info: Any,
        status: sd.CallbackFlags,
    ) -> None:
        """Callback invoked by sounddevice on the audio thread for incoming audio blocks."""
        if not self._is_recording or self._limit_reached:
            return

        # Duration guard: stop buffering instead of growing RAM without bound.
        if (
            self.max_duration_s is not None
            and time.perf_counter() - self._recording_start_time >= self.max_duration_s
        ):
            self._trip_limit("duration")
            return

        # Flatten input to 1D mono float32 chunk and copy to detach from driver buffer
        chunk = indata.flatten().astype(np.float32, copy=True)
        with self._audio_lock:
            if self._is_recording:
                self._audio_chunks.append(chunk)

    def _trip_limit(self, reason: str) -> None:
        """Stop buffering new data once a capture limit is reached.

        The session stays open so ``stop_recording()`` still returns what was
        captured; the limit is reported in the result and in the UI.
        """
        if self._limit_reached:
            return
        self._limit_reached = True
        self._limit_reason = reason
        logger.warning(
            "Capture reached the %s limit for sample %s", reason, self._sample_id
        )

    def _video_capture_loop(self) -> None:
        """Loop executed in video thread to capture frames while recording."""
        while self._is_recording and self._is_open and not self._limit_reached:
            if self._camera is None:
                break

            if (
                self.max_duration_s is not None
                and time.perf_counter() - self._recording_start_time
                >= self.max_duration_s
            ):
                self._trip_limit("duration")
                break

            ret, frame = self._camera.read()
            if not ret or frame is None:
                # Frame dropped or hardware delay; sleep briefly to prevent busy-wait
                time.sleep(0.005)
                continue

            now = time.perf_counter()
            if not self._is_recording:
                break

            timestamp_ms = max(0, int(round((now - self._recording_start_time) * 1000.0)))

            # If initial resolution was not reported by driver, update from first frame
            if self._device_info.get("camera_resolution") == (0, 0):
                h, w = frame.shape[:2]
                self._device_info["camera_resolution"] = (w, h)
                self._device_info["camera_width"] = w
                self._device_info["camera_height"] = h

            frame_cap_hit = False
            with self._video_lock:
                self._video_frames.append((timestamp_ms, frame))
                self._frame_count += 1
                if self.max_frames is not None and self._frame_count >= self.max_frames:
                    frame_cap_hit = True
            if frame_cap_hit:
                self._trip_limit("frames")

    def start_recording(self, sample_id: str) -> None:
        """Start buffering audio and video frames into lists.

        Args:
            sample_id: Non-empty identifier for the recording sample.

        Raises:
            ValueError: If sample_id is not a valid non-empty string.
            RuntimeError: If recorder is not open or a recording is already active.
        """
        with self._state_lock:
            if not self._is_open:
                raise RuntimeError("Recorder is not open. Call open() before start_recording().")

            if self._is_recording:
                raise RuntimeError(
                    f"Recording is already in progress for sample '{self._sample_id}'. "
                    "Call stop_recording() before starting a new recording."
                )

            if not isinstance(sample_id, str) or not sample_id.strip():
                raise ValueError("sample_id must be a valid non-empty string.")

            # Flush any stale frame in camera driver buffer
            if self._camera is not None:
                try:
                    self._camera.grab()
                except Exception:
                    pass

            with self._audio_lock:
                self._audio_chunks.clear()

            with self._video_lock:
                self._video_frames.clear()

            self._sample_id = sample_id.strip()
            self._recording_start_time = time.perf_counter()
            self._is_recording = True
            self._limit_reached = False
            self._limit_reason = None
            self._frame_count = 0

            # Start video capture loop in a separate thread
            self._video_thread = threading.Thread(
                target=self._video_capture_loop,
                name="Recorder-VideoCapture",
                daemon=True,
            )
            self._video_thread.start()

    def stop_recording(self) -> Dict[str, Any]:
        """Stop recording and return captured audio and video frames.

        Returns:
            Dictionary containing:
                - sample_id: str
                - audio: numpy array float32 mono 16kHz
                - video_frames: list of (timestamp_ms: int, frame: numpy array BGR)
                - sample_rate: int (16000)
                - duration_ms: int
                - device_info: dict with camera resolution, mic device name

        Raises:
            RuntimeError: If recorder is not currently recording.
        """
        with self._state_lock:
            if not self._is_recording:
                raise RuntimeError("Cannot stop recording: no recording in progress.")

            stop_time = time.perf_counter()
            self._is_recording = False

            # Wait for video capture thread to exit
            if self._video_thread is not None and self._video_thread.is_alive():
                self._video_thread.join(timeout=2.0)
            self._video_thread = None

            duration_ms = max(0, int(round((stop_time - self._recording_start_time) * 1000.0)))

            # Collect audio chunks
            with self._audio_lock:
                chunks = list(self._audio_chunks)
                self._audio_chunks.clear()

            if chunks:
                audio = np.concatenate(chunks, axis=0).astype(np.float32)
            else:
                audio = np.empty((0,), dtype=np.float32)

            if audio.ndim > 1:
                audio = audio.flatten()

            # Ensure all audio values are finite per AGENTS.md rules
            if not np.all(np.isfinite(audio)):
                audio = np.nan_to_num(audio, nan=0.0, posinf=1.0, neginf=-1.0).astype(np.float32)

            # Collect video frames
            with self._video_lock:
                video_frames = list(self._video_frames)
                self._video_frames.clear()

            sample_id = self._sample_id or ""
            self._sample_id = None

            return {
                "sample_id": sample_id,
                "audio": audio,
                "video_frames": video_frames,
                "sample_rate": self.sample_rate,
                "duration_ms": duration_ms,
                "device_info": dict(self._device_info),
                "limit_reached": self._limit_reached,
                "limit_reason": self._limit_reason,
                "max_duration_s": self.max_duration_s,
                "max_frames": self.max_frames,
            }

    def close(self) -> None:
        """Release camera and audio stream resources.

        Guarantees device release using try/finally blocks even if errors occur.
        """
        with self._state_lock:
            # Stop any active recording first
            if self._is_recording:
                self._is_recording = False
                if self._video_thread is not None and self._video_thread.is_alive():
                    try:
                        self._video_thread.join(timeout=2.0)
                    except Exception:
                        pass
                self._video_thread = None

            # Guarantee releasing both audio stream and camera
            try:
                if self._audio_stream is not None:
                    try:
                        if hasattr(self._audio_stream, "active") and self._audio_stream.active:
                            self._audio_stream.stop()
                    except Exception as exc:
                        logger.warning("Error stopping audio stream during close: %s", exc)
                    try:
                        self._audio_stream.close()
                    except Exception as exc:
                        logger.warning("Error closing audio stream during close: %s", exc)
            finally:
                try:
                    if self._camera is not None:
                        try:
                            self._camera.release()
                        except Exception as exc:
                            logger.warning("Error releasing camera during close: %s", exc)
                finally:
                    self._camera = None
                    self._audio_stream = None
                    self._is_open = False
                    self._is_recording = False

    def __enter__(self) -> "Recorder":
        """Context manager entry; opens capture devices."""
        self.open()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        """Context manager exit; releases capture devices."""
        self.close()
