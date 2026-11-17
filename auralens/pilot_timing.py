"""Read stream timing without extracting or storing biometric media."""
import argparse
import json
import math
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("media")
    parser.add_argument("--sample-id", required=True)
    parser.add_argument("--audio-event-ms", type=float)
    parser.add_argument("--video-event-ms", type=float)
    args = parser.parse_args()
    if not args.sample_id.strip():
        parser.error("sample ID must be nonempty")
    events = (args.audio_event_ms, args.video_event_ms)
    if any(x is not None for x in events) and not all(x is not None and math.isfinite(x) and x >= 0 for x in events):
        parser.error("provide both finite nonnegative event times from the same recording clock")
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=index,codec_type,start_time,duration,time_base,sample_rate,channels", "-of", "json", args.media], capture_output=True, text=True)
    if probe.returncode:
        parser.error(f"pilot sample_id={args.sample_id}: ffprobe failed; check media locally")
    streams = json.loads(probe.stdout)["streams"]
    result = {"sample_id": args.sample_id, "streams": streams,
              "missing_sources": sorted({"audio", "video"} - {s["codec_type"] for s in streams}),
              "offset_ms": None, "offset_method": "not_measured"}
    if args.audio_event_ms is not None:
        result.update(offset_ms=args.audio_event_ms-args.video_event_ms,
                      offset_method="manual_same_recording_event; positive means audio later")
    print(json.dumps(result, allow_nan=False))


if __name__ == "__main__":
    main()
