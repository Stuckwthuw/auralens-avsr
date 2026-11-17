"""Run separate speech and face pilots from one local recording."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--models-cache", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--sample-id", required=True)
    parser.add_argument("--single-person-confirmed", action="store_true")
    args = parser.parse_args()
    if not args.sample_id.strip():
        parser.error("--sample-id must not be empty")
    if args.output.resolve().is_relative_to(Path(__file__).resolve().parents[1]):
        parser.error("store pilot output outside Git")
    timing = subprocess.check_output(
        [sys.executable, "-m", "auralens.pilot_timing", str(args.video),
         "--sample-id", args.sample_id], text=True,
    )
    metadata = json.loads(timing)
    missing = metadata["missing_sources"]
    if "video" not in missing and not args.single_person_confirmed:
        parser.error("confirm one person for inputs with video")
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "timing.json").write_text(timing, encoding="utf-8")

    asr = ({"sample_id": args.sample_id, "mode": "asr_free", "text": "",
            "status": "invalid", "reason": "missing_audio", "infer_ms": None}
           if "audio" in missing else run_audio(args))
    (args.output / "asr.json").write_text(json.dumps(asr, ensure_ascii=False), encoding="utf-8")
    if "video" in missing:
        vision = {"sample_id": args.sample_id, "frame_count": 0, "valid_frames": 0,
                  "processing_ms": None, "status": "invalid", "reason": "missing_video"}
    else:
        vision = run_vision(args)
        vision["status"] = "ok" if vision["valid_frames"] else "invalid"
        vision["reason"] = None if vision["valid_frames"] else "no_face"
    (args.output / "vision-status.json").write_text(
        json.dumps({key: vision[key] for key in
                    ("sample_id", "frame_count", "valid_frames", "processing_ms", "status", "reason")}),
        encoding="utf-8",
    )

    if vision["sample_id"] != args.sample_id or asr["sample_id"] != args.sample_id:
        raise ValueError("pilot output sample IDs do not match")
    summary = {
        "sample_id": args.sample_id, "mock": False,
        "asr_status": asr["status"], "asr_infer_ms": asr["infer_ms"],
        "vision_frames": vision["frame_count"], "vision_valid_frames": vision["valid_frames"],
        "vision_processing_ms": vision["processing_ms"], "content_offset_ms": None,
        "asr_reason": asr["reason"], "vision_status": vision["status"],
        "vision_reason": vision["reason"], "missing_sources": missing,
    }
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary))


def run_audio(args):
    import numpy as np
    from faster_whisper import WhisperModel

    raw = subprocess.check_output(
        ["ffmpeg", "-v", "error", "-i", str(args.video), "-map", "0:a:0",
         "-ac", "1", "-ar", "16000", "-f", "f32le", "-"]
    )
    samples = np.frombuffer(raw, dtype="<f4").copy()
    if not samples.size or not np.isfinite(samples).all():
        raise ValueError("decoded audio must be nonempty and finite")
    model = WhisperModel("tiny", device="cpu", compute_type="int8",
                         download_root=str(args.models_cache), local_files_only=True)
    started = time.perf_counter()
    segments, _ = model.transcribe(samples, language="vi", beam_size=5)
    transcript = "".join(segment.text for segment in segments).strip()
    asr = {
        "sample_id": args.sample_id, "mode": "asr_free", "text": transcript,
        "status": "ok" if transcript else "uncertain",
        "reason": None if transcript else "empty_transcript",
        "model_version": "faster-whisper/tiny",
        "infer_ms": (time.perf_counter() - started) * 1000,
        "audio_samples": int(samples.size), "audio_peak": float(np.abs(samples).max()),
    }
    return asr


def run_vision(args):
    subprocess.run(
        [sys.executable, "-m", "auralens.vision.pilot_landmarks", "--video", str(args.video),
         "--model", str(args.model), "--output", str(args.output / "vision"),
         "--sample-id", args.sample_id, "--single-person-confirmed"],
        check=True,
    )
    return json.loads((args.output / "vision/pilot_landmarks.json").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
