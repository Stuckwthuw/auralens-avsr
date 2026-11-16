"""Local TV3 pilot only; output is not the shared TV4 contract."""

import argparse
import hashlib
import json
import math
import time
from pathlib import Path

import cv2
import mediapipe as mp


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--sample-id", required=True)
    parser.add_argument("--single-person-confirmed", action="store_true",
                        help="confirm that the entire clip shows only one person")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[2]
    if args.output.resolve().is_relative_to(repo_root):
        parser.error("--output must be outside this repository: crops and landmarks contain face data")
    if not args.video.is_file():
        parser.error("--video does not exist")
    if not args.model.is_file():
        parser.error("--model does not exist")
    if not args.sample_id.strip():
        parser.error("--sample-id must not be blank")
    if not args.single_person_confirmed:
        parser.error("confirm the clip has only one person with --single-person-confirmed")
    args.output.mkdir(parents=True, exist_ok=True)

    capture = cv2.VideoCapture(str(args.video))
    if not capture.isOpened():
        raise RuntimeError("vision pilot: cannot open video")

    options = mp.tasks.vision.FaceLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=str(args.model)),
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_faces=1,
    )
    lip_indices = sorted({index for pair in mp.tasks.vision.FaceLandmarksConnections.FACE_LANDMARKS_LIPS for index in (pair.start, pair.end)})
    frames = []
    preview_targets = (1_000, 5_000, 9_000, 11_000)
    preview_done = set()
    previous_ms = -1
    source_width = None
    source_height = None
    start = time.perf_counter()

    try:
        with mp.tasks.vision.FaceLandmarker.create_from_options(options) as landmarker:
            while True:
                ok, frame = capture.read()
                if not ok:
                    break
                height, width = frame.shape[:2]
                if source_width is None:
                    source_width, source_height = width, height
                elif (width, height) != (source_width, source_height):
                    raise RuntimeError(f"vision pilot: frame resolution changed at frame {len(frames)}")
                raw_ms = capture.get(cv2.CAP_PROP_POS_MSEC)
                if not math.isfinite(raw_ms) or raw_ms < 0:
                    raise RuntimeError("vision pilot: missing or invalid frame timestamp")
                timestamp_ms = round(raw_ms)
                if timestamp_ms <= previous_ms:
                    raise RuntimeError(f"vision pilot: non-increasing timestamp at frame {len(frames)}")
                previous_ms = timestamp_ms

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
                result = landmarker.detect_for_video(image, timestamp_ms)
                if not result.face_landmarks:
                    frames.append({"timestamp_ms": timestamp_ms, "valid": False,
                                   "reason": "no_face",
                                   "lip_landmarks": None})
                    continue

                landmarks = result.face_landmarks[0]
                points = [[landmarks[i].x, landmarks[i].y, landmarks[i].z] for i in lip_indices]
                frames.append({"timestamp_ms": timestamp_ms, "valid": True,
                               "reason": None, "lip_landmarks": points})

                for target in preview_targets:
                    if target in preview_done or timestamp_ms < target:
                        continue
                    preview_done.add(target)
                    xs = [landmarks[i].x * width for i in lip_indices]
                    ys = [landmarks[i].y * height for i in lip_indices]
                    margin_x = max(12, round((max(xs) - min(xs)) * 0.3))
                    margin_y = max(12, round((max(ys) - min(ys)) * 0.5))
                    left = max(0, round(min(xs)) - margin_x)
                    right = min(width, round(max(xs)) + margin_x)
                    top = max(0, round(min(ys)) - margin_y)
                    bottom = min(height, round(max(ys)) + margin_y)
                    crop = frame[top:bottom, left:right].copy()
                    for i in lip_indices:
                        x = round(landmarks[i].x * width) - left
                        y = round(landmarks[i].y * height) - top
                        cv2.circle(crop, (x, y), 2, (0, 255, 0), -1)
                    if not cv2.imwrite(str(args.output / f"mouth_{target}ms.jpg"), crop):
                        raise RuntimeError("vision pilot: failed to write mouth preview")
    finally:
        capture.release()

    if not frames:
        raise RuntimeError("vision pilot: video contains no decoded frames")
    valid_count = sum(frame["valid"] for frame in frames)
    model_hash = hashlib.sha256(args.model.read_bytes()).hexdigest()
    result = {
        "sample_id": args.sample_id,
        "pilot_only": True,
        "single_person_confirmed": True,
        "model_sha256": model_hash,
        "mediapipe_version": mp.__version__,
        "opencv_version": cv2.__version__,
        "source_width_px": source_width,
        "source_height_px": source_height,
        "lip_indices": lip_indices,
        "frame_count": len(frames),
        "valid_frames": valid_count,
        "invalid_frames": len(frames) - valid_count,
        "valid_fraction": valid_count / len(frames),
        "first_timestamp_ms": frames[0]["timestamp_ms"],
        "last_timestamp_ms": frames[-1]["timestamp_ms"],
        "processing_ms": round((time.perf_counter() - start) * 1000),
        "frames": frames,
    }
    (args.output / "pilot_landmarks.json").write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key not in {"frames", "lip_indices"}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
