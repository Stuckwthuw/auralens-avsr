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
from auralens.capture.storage import iter_timed_frames, save_capture


def _frames(count: int = 2, size: int = 32):
    return [
        (index * 33, np.zeros((size, size, 3), dtype=np.uint8))
        for index in range(count)
    ]


def _captured(**overrides):
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
        "audio_timing": {
            "clock": "time.perf_counter",
            "estimated": True,
            "block_count": 2,
            "overflow_count": 0,
            "gaps_ms": [],
        },
    }
    captured.update(overrides)
    return captured


class TestSaveCapture(unittest.TestCase):
    """Ghi đúng file và manifest cho một lượt thu."""

    def test_writes_audio_video_and_manifest(self) -> None:
        """Ba file nằm trong <output_dir>/<sample_id>/, manifest đủ trường."""
        with tempfile.TemporaryDirectory() as tmp:
            saved = save_capture(_captured(), tmp)

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
            saved = save_capture(_captured(audio=audio, video_frames=[]), tmp)
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
            saved = save_capture(_captured(video_frames=[]), tmp)
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
                        save_capture(_captured(sample_id=bad), tmp)
            self.assertEqual(os.listdir(tmp), [])

    def test_manifest_keeps_audio_and_video_timing(self) -> None:
        """Manifest giữ mốc audio xấp xỉ và cảnh báo AVI không có timestamp."""
        timing = {
            "clock": "time.perf_counter",
            "estimated": True,
            "first_block_start_ms": -10,
            "last_block_end_ms": 150,
            "block_count": 2,
            "overflow_count": 1,
            "gaps_ms": [{"at_ms": 0, "gap_ms": 140}],
            "blocks": [[-10, 0, 160, False], [140, 150, 160, True]],
        }
        with tempfile.TemporaryDirectory() as tmp:
            saved = save_capture(_captured(audio_timing=timing), tmp)
            with open(saved["manifest_file"], encoding="utf-8") as handle:
                manifest = json.load(handle)

            self.assertEqual(manifest["audio_timing"]["overflow_count"], 1)
            self.assertEqual(manifest["audio_timing"]["gaps_ms"][0]["gap_ms"], 140)
            self.assertTrue(manifest["video_timing"]["note"].count("iter_timed_frames"))
            self.assertEqual(manifest["video_timing"]["per_frame_timestamps"], "frame_timestamps_ms")


class TestTimedFrameAdapter(unittest.TestCase):
    """Đọc frame theo timestamp manifest, không theo đồng hồ của container."""

    def test_iter_timed_frames_uses_manifest_timestamps(self) -> None:
        """Frame không đều và mốc đầu khác 0 vẫn giữ đúng timestamp lúc thu."""
        frames = [
            (120, np.zeros((32, 32, 3), dtype=np.uint8)),
            (140, np.ones((32, 32, 3), dtype=np.uint8)),
            (400, np.full((32, 32, 3), 7, dtype=np.uint8)),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            saved = save_capture(_captured(video_frames=frames), tmp)
            pairs = list(iter_timed_frames(saved["directory"]))

            self.assertEqual([ts for ts, _ in pairs], [120, 140, 400])
            self.assertTrue(all(frame.shape == (32, 32, 3) for _, frame in pairs))

            with open(saved["manifest_file"], encoding="utf-8") as handle:
                manifest = json.load(handle)
            # fps = (số frame - 1) / khoảng thời gian thật → AVI phát xấp xỉ đúng độ dài thu.
            span_ms = manifest["frame_timestamps_ms"][-1] - manifest["frame_timestamps_ms"][0]
            self.assertEqual(manifest["video_fps"], round(2000.0 / span_ms, 3))

    def test_iter_timed_frames_requires_a_saved_video(self) -> None:
        """Mẫu không có video thì không được bịa timestamp."""
        with tempfile.TemporaryDirectory() as tmp:
            saved = save_capture(_captured(video_frames=[]), tmp)
            with self.assertRaises(ValueError):
                list(iter_timed_frames(saved["directory"]))


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


class TestRecorderAudioTiming(unittest.TestCase):
    """Mốc thời gian audio là xấp xỉ theo block và phải ghi rõ chỗ chưa chắc."""

    def _open_recorder(self) -> Recorder:
        recorder = Recorder(max_duration_s=None, max_frames=None)
        recorder._is_open = True  # không cần thiết bị thật
        return recorder

    def test_delayed_block_and_overflow_are_recorded(self) -> None:
        """Block trễ tạo gián đoạn, block overflow đếm riêng, offset ghi lại."""
        recorder = self._open_recorder()
        recorder.start_recording("timing-gap")
        try:
            recorder._audio_callback(
                np.zeros((160, 1), dtype=np.float32), 160, None, None
            )
            time.sleep(0.15)  # block sau bị trễ so với block trước

            class _Overflow:
                input_overflow = True

            recorder._audio_callback(
                np.ones((160, 1), dtype=np.float32), 160, None, _Overflow()
            )
            captured = recorder.stop_recording()
        finally:
            recorder.close()

        timing = captured["audio_timing"]
        self.assertEqual(timing["clock"], "time.perf_counter")
        self.assertTrue(timing["estimated"])
        self.assertEqual(timing["block_count"], 2)
        self.assertEqual(timing["overflow_count"], 1)
        self.assertEqual(len(timing["gaps_ms"]), 1)
        self.assertGreaterEqual(timing["gaps_ms"][0]["gap_ms"], 100)
        # Block đầu có thể bắt đầu trước mốc start_recording → offset âm được ghi lại
        # thay vì giả định audio bắt đầu đúng 0 ms.
        self.assertLessEqual(timing["first_block_start_ms"], 0)
        self.assertGreaterEqual(timing["last_block_end_ms"], 150)
        self.assertEqual([block[3] for block in timing["blocks"]], [False, True])

    def test_contiguous_blocks_have_no_gap(self) -> None:
        """Hai block liền nhau không bị báo gián đoạn và không có overflow."""
        recorder = self._open_recorder()
        recorder.start_recording("timing-contiguous")
        try:
            for _ in range(2):
                recorder._audio_callback(
                    np.zeros((160, 1), dtype=np.float32), 160, None, None
                )
            captured = recorder.stop_recording()
        finally:
            recorder.close()

        timing = captured["audio_timing"]
        self.assertEqual(timing["block_count"], 2)
        self.assertEqual(timing["overflow_count"], 0)
        self.assertEqual(timing["gaps_ms"], [])


if __name__ == "__main__":
    unittest.main()
