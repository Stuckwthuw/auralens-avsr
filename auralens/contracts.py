"""Draft week-one contract validation, using only the standard library."""
import json
import math
from pathlib import Path

CONFIG = json.loads((Path(__file__).resolve().parents[1] / "contracts/config.json").read_text())


def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def validate_branch(result, sample_id, start_ms, end_ms):
    """Require an explicit recording interval in addition to the branch fields."""
    prefix = f"contracts sample_id={sample_id}: "
    required = {"sample_id", "class_order", "scores", "valid", "reason", "infer_ms", "model_version", "start_ms", "end_ms"}
    if not isinstance(result, dict) or not required <= result.keys():
        raise ValueError(prefix + "missing branch fields")
    if not isinstance(sample_id, str) or not sample_id.strip():
        raise ValueError(prefix + "empty sample_id")
    if not number(start_ms) or not number(end_ms) or not 0 <= start_ms < end_ms:
        raise ValueError(prefix + "invalid recording interval")
    if (result["sample_id"], result["start_ms"], result["end_ms"]) != (sample_id, start_ms, end_ms):
        raise ValueError(prefix + "sample or interval mismatch")
    if result["class_order"] != CONFIG["class_order"]:
        raise ValueError(prefix + "class_order mismatch")
    if type(result["valid"]) is not bool:
        raise ValueError(prefix + "valid must be boolean")
    if not number(result["infer_ms"]) or result["infer_ms"] < 0:
        raise ValueError(prefix + "invalid infer_ms")
    if not isinstance(result["model_version"], str) or not result["model_version"].strip():
        raise ValueError(prefix + "missing model_version")
    if not result["valid"]:
        if not isinstance(result["reason"], str) or not result["reason"].strip() or result["scores"] is not None:
            raise ValueError(prefix + "invalid branch needs reason and null scores")
        return
    scores = result["scores"]
    if result["reason"] is not None:
        raise ValueError(prefix + "valid branch reason must be null")
    if not isinstance(scores, list) or len(scores) != 10 or not all(number(x) and x >= 0 for x in scores):
        raise ValueError(prefix + "invalid scores")
    if abs(sum(scores) - 1) > CONFIG["score_sum_tolerance"]:
        raise ValueError(prefix + "scores must sum to one")
