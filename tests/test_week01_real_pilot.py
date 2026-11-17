import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from auralens import week01_real_pilot


class RealPilotTests(unittest.TestCase):
    def run_pilot(self, *, missing=(), audio_error=None, video_error=None):
        audio_result = {
            "sample_id": "pilot_001", "mode": "asr_free", "text": "xin chào",
            "status": "ok", "reason": None, "model_version": "faster-whisper/tiny",
            "infer_ms": 12,
        }
        vision_result = {
            "sample_id": "pilot_001", "frame_count": 20, "valid_frames": 20,
            "processing_ms": 40, "status": "ok", "reason": None,
        }
        with TemporaryDirectory() as temp:
            output = Path(temp) / "result"
            argv = [
                "week01_real_pilot", "--video", "clip.mp4", "--model", "face.task",
                "--models-cache", "models", "--output", str(output),
                "--sample-id", "pilot_001", "--single-person-confirmed",
            ]
            with (
                patch("sys.argv", argv),
                patch("builtins.print"),
                patch.object(week01_real_pilot.subprocess, "check_output",
                             return_value=json.dumps({"missing_sources": list(missing)})),
                patch.object(week01_real_pilot, "run_audio", return_value=audio_result,
                             side_effect=audio_error) as audio,
                patch.object(week01_real_pilot, "run_vision", return_value=vision_result,
                             side_effect=video_error) as vision,
            ):
                week01_real_pilot.main()
                self.assertEqual(audio.call_count, int("audio" not in missing))
                self.assertEqual(vision.call_count, int("video" not in missing))
            return [
                json.loads((output / name).read_text())
                for name in ("summary.json", "asr.json", "vision-status.json")
            ]

    def test_audio_failure_keeps_vision_result(self):
        summary, asr, vision = self.run_pilot(audio_error=FileNotFoundError("missing model"))
        self.assertEqual(summary["asr_status"], "error")
        self.assertEqual(summary["asr_reason"], "audio_processing_failed")
        self.assertEqual(asr["status"], "error")
        self.assertIsNone(asr["model_version"])
        self.assertEqual(vision["status"], "ok")
        self.assertEqual(summary["vision_valid_frames"], 20)

    def test_video_failure_keeps_asr_result(self):
        summary, asr, vision = self.run_pilot(video_error=subprocess.CalledProcessError(1, "vision"))
        self.assertEqual(summary["vision_status"], "error")
        self.assertEqual(summary["vision_reason"], "video_processing_failed")
        self.assertEqual(vision["status"], "error")
        self.assertEqual(summary["asr_status"], "ok")
        self.assertEqual(asr["text"], "xin chào")

    def test_missing_audio_output_includes_every_ui_field(self):
        summary, asr, vision = self.run_pilot(missing=("audio",))
        self.assertEqual(set(asr), {
            "sample_id", "mode", "text", "status", "reason", "model_version", "infer_ms",
        })
        self.assertEqual(asr["sample_id"], summary["sample_id"])
        self.assertEqual(asr["status"], "invalid")
        self.assertEqual(asr["reason"], "missing_audio")
        self.assertIsNone(asr["model_version"])
        self.assertIsNone(asr["infer_ms"])
        self.assertEqual(summary["vision_status"], "ok")
        self.assertEqual(vision["status"], "ok")


if __name__ == "__main__":
    unittest.main()
