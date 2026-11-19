"""Persist a finished capture to disk as pilot data for TV2/TV3.

Layout per sample::

    <output_dir>/<sample_id>/
        audio.wav        # mono float32, sample_rate of the capture
        video.avi        # MJPG, frames in capture order (omitted if no frames)
        manifest.json    # sample_id, device_info, timestamps, sample_rate, ...

Audio is written as 32-bit float PCM WAV (WAVE format code 3), so the file keeps
exactly the samples the pipeline consumes (mono float32, 16 kHz by contract).

Frame timestamps are the monotonic millisecond offsets measured by Recorder and
are stored as an explicit list; frame index is never used in their place, per
AGENTS.md section 6.
"""

from __future__ import annotations

import json
import logging
import re
import struct
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

import numpy as np

logger = logging.getLogger(__name__)

#: Byte length of the RIFF/WAVE header written by :func:`write_float32_wav`.
WAV_HEADER_SIZE = 44

#: sample_id becomes a directory name, so keep it to a safe, portable charset.
_SAFE_SAMPLE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


def _check_sample_id(sample_id: Any) -> str:
    """Validate sample_id before it is used as a path component."""
    if not isinstance(sample_id, str) or not _SAFE_SAMPLE_ID.match(sample_id):
        raise ValueError(
            "sample_id phải là chuỗi 1-64 ký tự [A-Za-z0-9._-] và bắt đầu bằng "
            f"chữ/số, nhận được: {sample_id!r}"
        )
    return sample_id


def write_float32_wav(
    path: Union[str, Path],
    audio: np.ndarray,
    sample_rate: int,
) -> Path:
    """Write a mono float32 WAV file (WAVE format code 3).

    The standard library ``wave`` module only supports integer PCM, so the
    RIFF header is built here to keep the samples lossless.

    Args:
        path: Destination file.
        audio: Samples; flattened to mono if needed.
        sample_rate: Sample rate in Hz.

    Returns:
        The path written.
    """
    if int(sample_rate) <= 0:
        raise ValueError(f"sample_rate phải > 0, nhận được: {sample_rate!r}")

    data = np.asarray(audio, dtype=np.float32).reshape(-1)
    if data.size and not np.all(np.isfinite(data)):
        logger.warning("Audio có giá trị không hữu hạn, đã thay bằng 0/±1 trước khi ghi")
        data = np.nan_to_num(data, nan=0.0, posinf=1.0, neginf=-1.0).astype(np.float32)

    payload = data.astype("<f4", copy=False).tobytes()
    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",
        36 + len(payload),
        b"WAVE",
        b"fmt ",
        16,  # fmt chunk size
        3,  # WAVE_FORMAT_IEEE_FLOAT
        1,  # mono
        int(sample_rate),
        int(sample_rate) * 4,  # byte rate
        4,  # block align
        32,  # bits per sample
        b"data",
        len(payload),
    )

    target = Path(path)
    with open(target, "wb") as handle:
        handle.write(header)
        handle.write(payload)
    return target


def write_video(
    path: Union[str, Path],
    frames: List[Tuple[int, np.ndarray]],
    fallback_fps: float = 30.0,
) -> float:
    """Write timestamped BGR frames to an MJPG AVI file.

    Args:
        path: Destination file.
        frames: ``(timestamp_ms, frame)`` pairs in capture order.
        fallback_fps: Frame rate used when timestamps cannot provide one.

    Returns:
        The frame rate (FPS) written: -1 frame per average capture interval, so
        the AVI plays for approximately the recorded duration.

    Raises:
        RuntimeError: If the MJPG writer cannot be opened.
        ValueError: If ``frames`` is empty.
    """
    if not frames:
        raise ValueError("write_video cần ít nhất một frame")

    import cv2

    first = frames[0][1]
    height, width = first.shape[:2]

    # AVI only knows a constant frame rate. Use the average over the real capture
    # span (not the median gap between neighbours): cameras deliver frames in
    # bursts, so a median gap can be a few ms and inflate the rate until playback
    # runs much faster than the recorded wall time. Per-frame timestamps stay in
    # the manifest and are the authoritative source (see iter_timed_frames).
    fps = float(fallback_fps)
    if len(frames) > 1:
        span_ms = int(frames[-1][0]) - int(frames[0][0])
        if span_ms > 0:
            fps = (len(frames) - 1) * 1000.0 / span_ms
    fps = max(1.0, min(120.0, fps))

    target = Path(path)
    writer = cv2.VideoWriter(
        str(target), cv2.VideoWriter_fourcc(*"MJPG"), fps, (width, height)
    )
    if not writer.isOpened():
        raise RuntimeError(f"Không mở được VideoWriter MJPG cho {target}")

    try:
        for _, frame in frames:
            if frame.dtype != np.uint8:
                frame = np.clip(frame, 0, 255).astype(np.uint8)
            if frame.shape[1] != width or frame.shape[0] != height:
                frame = cv2.resize(frame, (width, height))
            writer.write(frame)
    finally:
        writer.release()
    return fps


def save_capture(
    captured: Dict[str, Any],
    output_dir: Union[str, Path],
    created_at: Optional[str] = None,
) -> Dict[str, Any]:
    """Save one capture turn (audio, video and manifest) under its sample_id.

    Args:
        captured: Result of ``Recorder.stop_recording()``: ``sample_id``,
            ``audio``, ``video_frames``, ``sample_rate``, ``duration_ms``,
            ``device_info`` and the optional limit fields.
        output_dir: Root directory for saved samples.
        created_at: ISO timestamp override (defaults to local time, with offset).

    Returns:
        Dictionary with ``sample_id``, ``directory``, the three file paths and
        the manifest that was written.

    Raises:
        ValueError: If ``sample_id`` is missing or unsafe as a directory name.
    """
    sample_id = _check_sample_id(captured.get("sample_id"))
    sample_dir = Path(output_dir) / sample_id
    sample_dir.mkdir(parents=True, exist_ok=True)

    audio = np.asarray(captured.get("audio", []), dtype=np.float32).reshape(-1)
    sample_rate = int(captured.get("sample_rate") or 16000)
    duration_ms = int(captured.get("duration_ms") or 0)
    frames: List[Tuple[int, np.ndarray]] = list(captured.get("video_frames") or [])
    device_info = dict(captured.get("device_info") or {})

    audio_path = write_float32_wav(sample_dir / "audio.wav", audio, sample_rate)

    video_path: Optional[Path] = None
    fps: Optional[float] = None
    if frames:
        video_path = sample_dir / "video.avi"
        fps = write_video(video_path, frames)

    manifest: Dict[str, Any] = {
        "sample_id": sample_id,
        "created_at": created_at
        or datetime.now().astimezone().isoformat(timespec="seconds"),
        "source": "auralens.capture.recorder",
        "sample_rate": sample_rate,
        "duration_ms": duration_ms,
        "num_audio_samples": int(audio.size),
        # Content length, which is shorter than duration_ms when a capture limit
        # stopped buffering before the user pressed Stop.
        "audio_duration_ms": int(round(audio.size * 1000.0 / sample_rate)),
        "num_frames": len(frames),
        "frame_timestamps_ms": [int(ts) for ts, _ in frames],
        "last_frame_timestamp_ms": int(frames[-1][0]) if frames else None,
        "video_fps": round(fps, 3) if fps is not None else None,
        "limit_reached": bool(captured.get("limit_reached", False)),
        "limit_reason": captured.get("limit_reason"),
        "max_duration_s": captured.get("max_duration_s"),
        "device_info": device_info,
        "audio_timing": captured.get("audio_timing") or {},
        "video_timing": (
            {
                "container": "avi/MJPG",
                "constant_fps": round(fps, 3) if fps is not None else None,
                "per_frame_timestamps": "frame_timestamps_ms",
                "note": (
                    "AVI không giữ timestamp tuyệt đối; đọc frame bằng "
                    "iter_timed_frames() để dùng timestamp của manifest."
                ),
            }
            if video_path is not None
            else None
        ),
        "audio_format": "wav/float32/mono",
        "video_format": "avi/MJPG" if video_path is not None else None,
        "files": {
            "audio": audio_path.name,
            "video": video_path.name if video_path is not None else None,
            "manifest": "manifest.json",
        },
    }

    manifest_path = sample_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    logger.info(
        "Đã lưu mẫu %s: %d mẫu âm thanh, %d frame → %s",
        sample_id,
        audio.size,
        len(frames),
        sample_dir,
    )

    return {
        "sample_id": sample_id,
        "directory": str(sample_dir),
        "audio_file": str(audio_path),
        "video_file": str(video_path) if video_path is not None else None,
        "manifest_file": str(manifest_path),
        "manifest": manifest,
    }


def iter_timed_frames(
    sample_dir: Union[str, Path],
) -> Iterator[Tuple[int, np.ndarray]]:
    """Read ``video.avi`` and pair each frame with its manifest timestamp.

    The AVI container only knows a constant FPS, so ``CAP_PROP_POS_MSEC`` stops
    matching capture time as soon as frames are dropped or the first frame does
    not start at 0 ms. Consumers must take the timestamp from
    ``manifest.json`` (``frame_timestamps_ms``) instead of the container.

    Args:
        sample_dir: Directory containing ``manifest.json`` and the video file.

    Yields:
        ``(timestamp_ms, frame)`` in capture order.

    Raises:
        ValueError: If the sample has no video, no timestamps, or the video
            frame count does not match the manifest.
        RuntimeError: If the video file cannot be opened.
    """
    import cv2

    directory = Path(sample_dir)
    with open(directory / "manifest.json", encoding="utf-8") as handle:
        manifest = json.load(handle)

    video_name = (manifest.get("files") or {}).get("video")
    if not video_name:
        raise ValueError(f"{directory} không có video trong manifest")

    timestamps = [int(ts) for ts in manifest.get("frame_timestamps_ms") or []]
    if not timestamps:
        raise ValueError(f"{directory} không có frame_timestamps_ms trong manifest")

    capture = cv2.VideoCapture(str(directory / video_name))
    if not capture.isOpened():
        raise RuntimeError(f"Không mở được {directory / video_name}")

    try:
        index = 0
        while index < len(timestamps):
            ok, frame = capture.read()
            if not ok:
                break
            yield timestamps[index], frame
            index += 1
        if index != len(timestamps):
            raise ValueError(
                f"{video_name} có {index} frame nhưng manifest ghi {len(timestamps)}; "
                "không ghép timestamp theo thứ tự khi số frame lệch"
            )
    finally:
        capture.release()
