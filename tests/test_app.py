"""Unit tests for AuralensApp UI prototype."""

import json
import os
import shutil
import struct
import tempfile
import time
import tkinter as tk
import unittest

import numpy as np

from auralens.app.main_window import (
    AuralensApp,
    MOCK_ASR_SENTENCES,
    MODE_ASR_FREE,
    MODE_EXPERIMENT_10,
    PREDEFINED_10_SENTENCES,
    SOURCE_AUDIO,
    SOURCE_AV,
    SOURCE_VISUAL,
    STATUS_ERROR,
    STATUS_PROCESSING,
    STATUS_READY,
    STATUS_RECORDING,
    STATUS_UNCERTAIN,
    UNCERTAIN_EXPERIMENT_TEXT,
)


class TestAuralensApp(unittest.TestCase):
    """Test suite for AuralensApp."""

    def setUp(self) -> None:
        self.root = tk.Tk()
        self.app = AuralensApp(root=self.root, mock_mode=True)
        self.root.update()

    def tearDown(self) -> None:
        self.app._on_close()

    def test_window_properties(self) -> None:
        """Verify window title, minimum size, and mock badge."""
        self.assertEqual(self.root.title(), "Auralens — Phụ đề thông minh")
        min_w, min_h = self.root.minsize()
        self.assertGreaterEqual(min_w, 800)
        self.assertGreaterEqual(min_h, 400)
        self.assertIn("⚠ Mô phỏng", self.app.mock_badge.cget("text"))

    def test_mode_selection_and_source_visibility(self) -> None:
        """Verify mode switching and conditional visibility of the source selector."""
        # Initial mode should be ASR free mode, with source group hidden
        self.assertEqual(self.app.mode_var.get(), MODE_ASR_FREE)
        self.assertEqual(self.app.source_group.winfo_ismapped(), 0)

        # Switch to 10-sentence experiment mode
        self.app.mode_var.set(MODE_EXPERIMENT_10)
        self.app._on_mode_change()
        self.root.update()
        self.assertEqual(self.app.source_group.winfo_ismapped(), 1)
        self.assertIn(MODE_EXPERIMENT_10, self.app.status_mode_label.cget("text"))

        # Switch source to Visual only
        self.app.source_var.set(SOURCE_VISUAL)
        self.app._on_source_change()
        self.assertIn("[V]", self.app.status_mode_label.cget("text"))

        # Switch back to ASR free mode
        self.app.mode_var.set(MODE_ASR_FREE)
        self.app._on_mode_change()
        self.root.update()
        self.assertEqual(self.app.source_group.winfo_ismapped(), 0)
        self.assertIn(MODE_ASR_FREE, self.app.status_mode_label.cget("text"))

    def test_font_size_controls(self) -> None:
        """Verify font size adjustment and bounds [16, 48]."""
        initial_size = self.app.font_size
        self.assertGreaterEqual(initial_size, 24)

        # Test increment
        self.app._adjust_font_size(4)
        self.assertEqual(self.app.font_size, initial_size + 4)
        self.assertEqual(self.app.font_value_label.cget("text"), f"{initial_size + 4} pt")

        # Test lower clamp bound (16)
        self.app._adjust_font_size(-100)
        self.assertEqual(self.app.font_size, 16)

        # Test upper clamp bound (48)
        self.app._adjust_font_size(100)
        self.assertEqual(self.app.font_size, 48)

    def test_contrast_toggle(self) -> None:
        """Verify contrast toggle updates dark_mode state and colors."""
        initial_mode = self.app.dark_mode
        self.app._toggle_contrast()
        self.assertNotEqual(self.app.dark_mode, initial_mode)
        self.root.update()

        # Toggle back
        self.app._toggle_contrast()
        self.assertEqual(self.app.dark_mode, initial_mode)
        self.root.update()

    def test_subtitle_wraplength_follows_resize(self) -> None:
        """Xuống dòng theo bề rộng vùng phụ đề, không hẹp dưới 200 px."""
        wraplength = lambda: int(str(self.app.subtitle_label.cget("wraplength")))

        # Giá trị đầu phụ thuộc bề rộng cửa sổ lúc dựng, chỉ cần lớn hơn chặn dưới.
        self.assertGreater(wraplength(), 200)
        self.assertTrue(
            self.app.subtitle_box.bind("<Configure>"),
            "vùng phụ đề chưa gắn handler <Configure>",
        )

        class _Resize:
            width = 500

        self.app._on_subtitle_box_resize(_Resize())
        self.assertEqual(wraplength(), 452)  # 500 - 48 padding

        _Resize.width = 100
        self.app._on_subtitle_box_resize(_Resize())
        self.assertEqual(wraplength(), 200)  # chặn dưới, chữ không bị cắt

        # Sự kiện <Configure> thật phải đi qua cùng handler.
        self.app.subtitle_box.event_generate("<Configure>", width=700, height=300)
        self.root.update()
        self.assertEqual(wraplength(), 652)

    def test_status_indicator_and_subtitle_update(self) -> None:
        """Verify _update_subtitle updates subtitle text and status pill."""
        statuses = [STATUS_READY, STATUS_RECORDING, STATUS_PROCESSING, STATUS_UNCERTAIN, STATUS_ERROR]
        test_text = "Thử nghiệm phụ đề tiếng Việt có dấu."

        for status in statuses:
            self.app._update_subtitle(test_text, status)
            self.root.update()
            self.assertEqual(self.app.subtitle_label.cget("text"), test_text)
            self.assertEqual(self.app.status_indicator.cget("text"), status)

    def test_mock_data_contents(self) -> None:
        """Verify predefined sentences conform to TV1 contract and ASR sentences exist."""
        self.assertEqual(len(PREDEFINED_10_SENTENCES), 10)
        self.assertIn("Xin chào bạn.", PREDEFINED_10_SENTENCES)
        self.assertIn("Hẹn gặp lại bạn.", PREDEFINED_10_SENTENCES)
        self.assertEqual(UNCERTAIN_EXPERIMENT_TEXT, "Chưa nhận dạng được")
        self.assertGreaterEqual(len(MOCK_ASR_SENTENCES), 5)

    def test_mock_recognition_lifecycle(self) -> None:
        """Verify complete start -> recording -> processing -> result lifecycle."""
        self.app._on_start_stop()
        self.root.update()
        self.assertTrue(self.app.is_running)
        self.assertEqual(self.app.start_stop_btn.cget("text"), "Dừng")

        # Advance to processing early
        self.app._on_start_stop()
        self.root.update()

        # Wait for completion
        start_t = time.time()
        while self.app.is_running and time.time() - start_t < 4.0:
            self.root.update()
            time.sleep(0.05)

        self.assertFalse(self.app.is_running)
        self.assertEqual(self.app.start_stop_btn.cget("text"), "Bắt đầu")
        self.assertIn(self.app.status_indicator.cget("text"), [STATUS_READY, STATUS_UNCERTAIN])


class FakeRecorder:
    """Recorder giả: kiểm tra vòng đời thiết bị mà không cần phần cứng."""

    def __init__(
        self,
        camera_index: int = 0,
        audio_device=None,
        sample_rate: int = 16000,
        max_duration_s: float = 15.0,
    ) -> None:
        self.calls: list[str] = []
        self.sample_id = ""
        self.sample_rate = sample_rate
        self.max_duration_s = max_duration_s
        self.fail_open = False
        self.frame_count = 2
        self.limit_reached = False
        self.limit_reason = None
        self._is_recording = False
        self.device_info = {
            "camera_index": camera_index,
            "camera_width": 640,
            "camera_height": 480,
            "mic_device_name": "Mic giả lập",
        }

    @property
    def is_recording(self) -> bool:
        return self._is_recording

    def open(self) -> None:
        self.calls.append("open")
        if self.fail_open:
            raise RuntimeError("Không mở được camera (device index: 0)")

    def start_recording(self, sample_id: str) -> None:
        self.calls.append("start")
        self.sample_id = sample_id
        self._is_recording = True

    def stop_recording(self) -> dict:
        self.calls.append("stop")
        self._is_recording = False
        frames = [
            (index * 33, np.zeros((48, 64, 3), dtype=np.uint8))
            for index in range(self.frame_count)
        ]
        return {
            "sample_id": self.sample_id,
            "audio": np.zeros(16000, dtype=np.float32),
            "video_frames": frames,
            "sample_rate": 16000,
            "duration_ms": 1000,
            "device_info": dict(self.device_info),
            "limit_reached": self.limit_reached,
            "limit_reason": self.limit_reason,
            "max_duration_s": self.max_duration_s,
        }

    def close(self) -> None:
        self.calls.append("close")
        self._is_recording = False


class TestLiveCaptureIntegration(unittest.TestCase):
    """Một lượt thu thật ở mức code: mở, thu, dừng, nhả thiết bị."""

    def _make_app(self, fake: FakeRecorder):
        root = tk.Tk()
        root.withdraw()  # không hiện cửa sổ khi chạy test
        out_dir = tempfile.mkdtemp(prefix="auralens-test-")
        self.addCleanup(shutil.rmtree, out_dir, True)
        app = AuralensApp(
            root=root,
            mock_mode=False,
            recorder_factory=lambda **_: fake,
            output_dir=out_dir,
        )
        return root, app

    @staticmethod
    def _pump(root: tk.Tk, until, timeout: float = 3.0) -> bool:
        deadline = time.time() + timeout
        while time.time() < deadline:
            root.update()
            if until():
                return True
            time.sleep(0.02)
        return False

    def test_live_turn_opens_records_stops_and_releases(self) -> None:
        """Bắt đầu mở thiết bị; Dừng đóng thiết bị và báo số liệu thu thật."""
        fake = FakeRecorder()
        root, app = self._make_app(fake)
        try:
            app._on_start_stop()
            self.assertTrue(
                self._pump(root, lambda: "start" in fake.calls),
                "worker chưa mở thiết bị và bắt đầu thu",
            )
            self.assertIn("open", fake.calls)
            # Nhãn thiết bị đến qua queue nên cần thêm một nhịp poll của UI.
            self.assertTrue(
                self._pump(
                    root,
                    lambda: "640×480" in app.status_device_label.cget("text"),
                ),
                "nhãn thiết bị chưa được cập nhật từ device_info",
            )

            app._on_start_stop()  # Dừng
            self.assertTrue(
                self._pump(
                    root,
                    lambda: "close" in fake.calls
                    and "Đã thu" in app.subtitle_label.cget("text")
                    and app.status_device_label.cget("text").startswith(
                        "Thiết bị: đã nhả"
                    ),
                ),
                "kết quả thu hoặc trạng thái nhả thiết bị chưa hiển thị",
            )
            self.assertIn("stop", fake.calls)
            self.assertEqual(app.status_indicator.cget("text"), STATUS_UNCERTAIN)
            self.assertEqual(
                app.status_device_label.cget("text"),
                "Thiết bị: đã nhả camera & micro",
            )
        finally:
            app._on_close()

    def test_close_window_mid_recording_releases_devices(self) -> None:
        """Đóng cửa sổ khi đang thu vẫn phải nhả thiết bị."""
        fake = FakeRecorder()
        root, app = self._make_app(fake)
        app._on_start_stop()
        self.assertTrue(self._pump(root, lambda: "start" in fake.calls))

        app._on_close()

        self.assertIn("close", fake.calls)
        self.assertIsNone(app._recorder)

    def test_device_error_is_reported_without_fake_result(self) -> None:
        """Không mở được thiết bị: báo lỗi, không hiển thị câu bịa."""
        fake = FakeRecorder()
        fake.fail_open = True
        root, app = self._make_app(fake)
        try:
            app._on_start_stop()
            self.assertTrue(
                self._pump(
                    root,
                    lambda: "Lỗi thiết bị" in app.subtitle_label.cget("text"),
                )
            )
            self.assertEqual(app.status_indicator.cget("text"), STATUS_ERROR)
            self.assertNotIn("Đã thu", app.subtitle_label.cget("text"))
            self.assertIn("close", fake.calls)
        finally:
            app._on_close()

    def test_live_turn_writes_audio_video_and_manifest(self) -> None:
        """Lượt thu thật ghi audio.wav, video.avi và manifest.json theo sample_id."""
        fake = FakeRecorder()
        root, app = self._make_app(fake)
        try:
            app._on_start_stop()
            self.assertTrue(self._pump(root, lambda: "start" in fake.calls))

            app._on_start_stop()  # Dừng
            self.assertTrue(
                self._pump(
                    root,
                    lambda: "đã lưu mẫu" in app.subtitle_label.cget("text"),
                ),
                "phụ đề chưa báo đã lưu mẫu",
            )

            sample_dir = os.path.join(app.output_dir, fake.sample_id)
            self.assertTrue(os.path.isdir(sample_dir), sample_dir)
            for name in ("audio.wav", "video.avi", "manifest.json"):
                self.assertTrue(os.path.isfile(os.path.join(sample_dir, name)), name)

            with open(
                os.path.join(sample_dir, "manifest.json"), encoding="utf-8"
            ) as handle:
                manifest = json.load(handle)

            self.assertEqual(manifest["sample_id"], fake.sample_id)
            self.assertEqual(manifest["sample_rate"], 16000)
            self.assertEqual(manifest["num_audio_samples"], 16000)
            self.assertEqual(manifest["num_frames"], fake.frame_count)
            self.assertEqual(len(manifest["frame_timestamps_ms"]), fake.frame_count)
            self.assertEqual(manifest["device_info"]["camera_width"], 640)
            self.assertEqual(manifest["device_info"]["mic_device_name"], "Mic giả lập")
            self.assertIn("created_at", manifest)
            self.assertFalse(manifest["limit_reached"])

            with open(os.path.join(sample_dir, "audio.wav"), "rb") as handle:
                header = handle.read(44)
            self.assertEqual(header[:4], b"RIFF")
            self.assertEqual(struct.unpack("<H", header[20:22])[0], 3)  # float32
            self.assertEqual(struct.unpack("<I", header[24:28])[0], 16000)

            import cv2

            video = cv2.VideoCapture(os.path.join(sample_dir, "video.avi"))
            try:
                self.assertTrue(video.isOpened())
                ok, frame = video.read()
                self.assertTrue(ok)
                self.assertEqual(frame.shape[:2], (48, 64))
            finally:
                video.release()
        finally:
            app._on_close()

    def test_limit_reached_is_reported_and_saved(self) -> None:
        """Chạm giới hạn thời lượng: UI báo giới hạn và manifest ghi lại."""
        fake = FakeRecorder(max_duration_s=0.2)
        root, app = self._make_app(fake)
        try:
            app._on_start_stop()
            self.assertTrue(self._pump(root, lambda: "start" in fake.calls))

            # Recorder tự dừng khi chạm giới hạn; app phải nhận ra và kết thúc lượt.
            fake.limit_reached = True
            fake.limit_reason = "duration"
            self.assertTrue(
                self._pump(
                    root,
                    lambda: "giới hạn" in app.subtitle_label.cget("text")
                    and "đã lưu mẫu" in app.subtitle_label.cget("text"),
                ),
                "phụ đề chưa báo giới hạn thời lượng",
            )

            with open(
                os.path.join(app.output_dir, fake.sample_id, "manifest.json"),
                encoding="utf-8",
            ) as handle:
                manifest = json.load(handle)
            self.assertTrue(manifest["limit_reached"])
            self.assertEqual(manifest["limit_reason"], "duration")
        finally:
            app._on_close()


if __name__ == "__main__":
    unittest.main()
