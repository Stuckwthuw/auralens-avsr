import json
from pathlib import Path
import unittest
from auralens.pipeline import run_mock

ROOT = Path(__file__).resolve().parents[1]

class ContractTests(unittest.TestCase):
    def fixture(self, name="valid"):
        return json.loads((ROOT / f"contracts/fixtures/{name}.json").read_text())

    def test_sources(self):
        for name in ("valid", "missing_audio", "missing_video", "both_missing"):
            with self.subTest(name=name):
                result = run_mock(self.fixture(name))
                self.assertTrue(result["mock"])
                self.assertEqual(result["sample_id"], "mock_001")
                self.assertEqual(result["status"], "invalid" if name == "both_missing" else "uncertain")
                self.assertEqual(result["text"], "")

    def test_bad_branch_rejected(self):
        changes = {"class_order": list(reversed(self.fixture()["audio"]["class_order"])),
                   "sample_id": "other", "start_ms": 1, "end_ms": 999,
                   "scores": [float("nan")]*10, "infer_ms": -1, "valid": 1,
                   "model_version": ""}
        for key, value in changes.items():
            with self.subTest(key=key):
                sample = self.fixture()
                sample["audio"][key] = value
                with self.assertRaises(ValueError):
                    run_mock(sample)

    def test_score_shapes_and_sums(self):
        for scores in ([1], [1]*10, [-1]+[2/9]*9, [float("inf")]*10):
            sample = self.fixture()
            sample["audio"]["scores"] = scores
            with self.assertRaises(ValueError):
                run_mock(sample)

    def test_real_rejected(self):
        sample = self.fixture()
        sample["mock"] = False
        with self.assertRaises(ValueError):
            run_mock(sample)
