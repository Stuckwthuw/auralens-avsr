"""Week-one mock entry point. Real model adapters remain producer-owned."""
import argparse
import json
from queue import Queue
from time import perf_counter
from .contracts import validate_branch


def run_mock(sample):
    started = perf_counter()
    if sample.get("mock") is not True:
        raise ValueError("pipeline: this entry point requires mock=true")
    for source in ("audio", "vision"):
        validate_branch(sample[source], sample["sample_id"], sample["start_ms"], sample["end_ms"])
    available = [s for s in ("audio", "vision") if sample[s]["valid"]]
    result = {"sample_id": sample["sample_id"], "mode": "av_10", "text": "",
              "status": "uncertain" if available else "invalid",
              "reason": "mock_only; available=" + ",".join(available),
              "model_version": "mock-week01", "infer_ms": (perf_counter()-started)*1000,
              "mock": True}
    queue = Queue(maxsize=1)
    queue.put_nowait(result)
    return queue.get_nowait()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture")
    args = parser.parse_args()
    with open(args.fixture) as stream:
        result = run_mock(json.load(stream))
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
