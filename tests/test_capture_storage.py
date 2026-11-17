"""Kiểm thử lưu mẫu thu (audio/video/manifest) và giới hạn thời lượng.

Không cần phần cứng: dữ liệu là mảng numpy tổng hợp và Recorder chỉ được mở
ở mức trạng thái nội bộ.
"""

import json
import os
import struct
import tempfile
import time
import unittest

import numpy as np

from auralens.capture.recorder import Recorder
from auralens.capture.storage import save_capture


def _frames(count: int = 2, size: int = 32):
    return [
        (index * 33, np.zeros((size, size, 3), dtype=np.uint8))
        for index in range(count)
    ]


class TestSaveCapture(unittest.TestCase):
    """Ghi đúng file và manifest cho một lượt thu."""

    def _captured(self, **overrides):
        captured = {
            "sample_id": "tv5-test-001",
            "audio": np.zeros(16000, dtype=np.float32),
            "video_frames": _frames(),
            "sample_rate": 16000,
            "duration_ms": 1000,
            "device_info": {
                "camera_index": 0,
                "camera_width": 32,
                "camera_height": 32,
                "mic_device_name": "Mic giả lập",
            },
            "limit_reached": False,
            "limit_reason": None,
            "max_duration_s": 15.0,
        }
        captured.update(overrides)
        return captured

    def test_writes_audio_video_and_manifest(self) -> None:
        """Ba file nằm trong <output_dir>/<sample_id>/, manifest đủ trường."""
        with tempfile.TemporaryDirectory() as tmp:
            saved = save_capture(self._captured(), tmp)

            self.assertEqual(saved["sample_id"], "tv5-test-001")
            self.assertEqual(
                os.path.dirname(saved["audio_file"]), os.path.join(tmp, "tv5-test-001")
            )
            self.assertTrue(os.path.isfile(saved["audio_file"]))
            self.assertTrue(os.path.isfile(saved["video_file"]))
            self.assertTrue(os.path.isfile(saved["manifest_file"]))

            with open(saved["manifest_file"], encoding="utf-8") as handle:
                manifest = json.load(handle)

            self.assertEqual(manifest["sample_id"], "tv5-test-001")
            self.assertEqual(manifest["sample_rate"], 16000)
            self.assertEqual(manifest["duration_ms"], 1000)
            self.assertEqual(manifest["num_audio_samples"], 16000)
            self.assertEqual(manifest["audio_duration_ms"], 1000)
            self.assertEqual(manifest["num_frames"], 2)
            self.assertEqual(manifest["frame_timestamps_ms"], [0, 33])
            self.assertEqual(manifest["last_frame_timestamp_ms"], 33)
            self.assertEqual(manifest["device_info"]["mic_device_name"], "Mic giả lập")
            self.assertEqual(manifest["device_info"]["camera_width"], 32)
            self.assertIn("created_at", manifest)
            self.assertFalse(manifest["limit_reached"])
            self.assertEqual(manifest["files"]["video"], "video.avi")

            import cv2

            video = cv2.VideoCapture(saved["video_file"])
            try:
                self.assertTrue(video.isOpened())
                self.assertGreaterEqual(int(video.get(cv2.CAP_PROP_FRAME_COUNT)), 1)
                ok, frame = video.read()
                self.assertTrue(ok)
                self.assertEqual(frame.shape[:2], (32, 32))
            finally:
                video.release()

    def test_audio_is_float32_wav(self) -> None:
        """WAV giữ đúng mẫu float32 mono, không lượng tử hoá sang int16."""
        audio = np.linspace(-0.5, 0.5, 160, dtype=np.float32)
        with tempfile.TemporaryDirectory() as tmp:
            saved = save_capture(self._captured(audio=audio, video_frames=[]), tmp)
            with open(saved["audio_file"], "rb") as handle:
                blob = handle.read()

            self.assertEqual(blob[:4], b"RIFF")
            self.assertEqual(blob[8:12], b"WAVE")
            audio_format, channels = struct.unpack("<HH", blob[20:24])
            sample_rate = struct.unpack("<I", blob[24:28])[0]
            bits = struct.unpack("<H", blob[34:36])[0]

            self.assertEqual(audio_format, 3)  # IEEE float
            self.assertEqual(channels, 1)
            self.assertEqual(sample_rate, 16000)
            self.assertEqual(bits, 32)
            self.assertEqual(len(blob), 44 + audio.size * 4)
            np.testing.assert_array_equal(
                np.frombuffer(blob[44:], dtype="<f4"), audio
            )

    def test_without_frames_omits_video(self) -> None:
        """Lượt thu không có frame vẫn có manifest, không có video.avi."""
        with tempfile.TemporaryDirectory() as tmp:
            saved = save_capture(self._captured(video_frames=[]), tmp)
            self.assertIsNone(saved["video_file"])
            with open(saved["manifest_file"], encoding="utf-8") as handle:
                manifest = json.load(handle)
            self.assertEqual(manifest["num_frames"], 0)
            self.assertIsNone(manifest["files"]["video"])
            self.assertIsNone(manifest["video_format"])

    def test_rejects_unsafe_sample_id(self) -> None:
        """sample_id dùng làm tên thư mục nên phải chặn đường dẫn lạ."""
        with tempfile.TemporaryDirectory() as tmp:
            for bad in ["../evil", "a/b", "", "  ", "-x", None]:
                with self.subTest(sample_id=bad):
                    with self.assertRaises(ValueError):
                        save_capture(self._captured(sample_id=bad), tmp)
            self.assertEqual(os.listdir(tmp), [])


class TestRecorderLimits(unittest.TestCase):
    """Giới hạn thu áp dụng ở Recorder, không cần camera/micro thật."""

    def test_duration_limit_stops_buffering(self) -> None:
        """Quá max_duration_s thì ngừng nhận dữ liệu và báo limit_reached."""
        recorder = Recorder(max_duration_s=0.05)
        recorder._is_open = True  # mô phỏng phiên đã mở, không cần thiết bị
        recorder.start_recording("limit-check")
        try:
            time.sleep(0.08)
            recorder._audio_callback(
                np.zeros((160, 1), dtype=np.float32), 160, None, None
            )
            self.assertTrue(recorder.limit_reached)
            captured = recorder.stop_recording()
        finally:
            recorder.close()

        self.assertTrue(captured["limit_reached"])
        self.assertEqual(captured["limit_reason"], "duration")
        self.assertEqual(captured["sample_id"], "limit-check")

    def test_invalid_limit_is_rejected(self) -> None:
        """Giới hạn 0 hoặc âm là lỗi cấu hình, không được im lặng bỏ qua."""
        with self.assertRaises(ValueError):
            Recorder(max_duration_s=0)
        with self.assertRaises(ValueError):
            Recorder(max_frames=-1)


if __name__ == "__main__":
    unittest.main()
