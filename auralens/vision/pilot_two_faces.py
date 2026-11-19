"""Measure up to two sets of mouth landmarks per frame for the TV3 offline pilot."""

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path

import cv2
import mediapipe as mp


def measure(video: Path, model: Path, sample_id: str) -> dict:
    options = mp.tasks.vision.FaceLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=str(model)),
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_faces=2,
    )
    connections = mp.tasks.vision.FaceLandmarksConnections.FACE_LANDMARKS_LIPS
    indices = sorted({i for edge in connections for i in (edge.start, edge.end)})
    frames = []
    counts = Counter()
    capture = cv2.VideoCapture(str(video))
    try:
        with mp.tasks.vision.FaceLandmarker.create_from_options(options) as detector:
            while True:
                ok, frame = capture.read()
                if not ok:
                    break
                ms = round(capture.get(cv2.CAP_PROP_POS_MSEC))
                if ms < 0 or (frames and ms <= frames[-1]["timestamp_ms"]):
                    raise ValueError(f"vision {sample_id}: invalid timestamp at frame {len(frames)}")
                image = mp.Image(image_format=mp.ImageFormat.SRGB,
                                 data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                result = detector.detect_for_video(image, ms)
                faces = [[[face[i].x, face[i].y, face[i].z] for i in indices]
                         for face in result.face_landmarks]
                if not all(math.isfinite(v) for face in faces for point in face for v in point):
                    raise ValueError(f"vision {sample_id}: non-finite landmarks at {ms} ms")
                # Order is local to each frame. No identity or speaker is inferred.
                faces.sort(key=lambda points: sum(p[0] for p in points))
                frames.append({"timestamp_ms": ms, "mouths": faces})
                counts[len(faces)] += 1
    finally:
        capture.release()
    if not frames:
        raise ValueError(f"vision {sample_id}: no decoded frames")
    return {"pilot_only": True, "sample_id": sample_id, "num_faces": 2,
            "model_sha256": hashlib.sha256(model.read_bytes()).hexdigest(),
            "mediapipe": mp.__version__, "opencv": cv2.__version__, "lip_indices": indices,
            "frames_by_detection_count": {n: counts[n] for n in range(3)}, "frames": frames}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--sample-id", required=True)
    parser.add_argument("--output", type=Path, required=True, help="New private JSON outside Git")
    args = parser.parse_args()
    out = args.output.resolve()
    if any((p / ".git").exists() for p in out.parents):
        parser.error("landmarks must be stored outside Git")
    if not args.video.is_file() or not args.model.is_file() or not args.sample_id.strip():
        parser.error("provide existing video/model files and a nonempty sample ID")
    if out.exists():
        parser.error("choose a new output path")
    report = measure(args.video, args.model, args.sample_id)
    with out.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, allow_nan=False, separators=(",", ":"))
    print(args.sample_id, report["frames_by_detection_count"])


if __name__ == "__main__":
    main()
