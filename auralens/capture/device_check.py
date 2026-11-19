"""Quick check that camera and microphone are accessible.

Usage:
    python -m auralens.capture.device_check

Prints device info and exits. Does NOT keep devices open.
"""
import sys

def check_camera(index: int = 0) -> dict:
    import cv2
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        return {"available": False, "error": "Không mở được camera"}
    try:
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        ok, frame = cap.read()
        return {
            "available": True,
            "width": w,
            "height": h,
            "fps_reported": round(fps, 1),
            "read_ok": ok,
            "frame_shape": list(frame.shape) if ok else None,
        }
    finally:
        cap.release()


def check_microphone() -> dict:
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        default_input = sd.query_devices(kind="input")
        return {
            "available": True,
            "default_device": default_input["name"],
            "sample_rate": int(default_input["default_samplerate"]),
            "channels": default_input["max_input_channels"],
            "total_devices": len(devices),
        }
    except Exception as e:
        return {"available": False, "error": str(e)}


def main():
    import json
    print("=" * 50)
    print("Auralens — Kiểm tra thiết bị")
    print("=" * 50)

    print("\n📷 Camera:")
    cam = check_camera()
    print(json.dumps(cam, indent=2, ensure_ascii=False))

    print("\n🎤 Microphone:")
    mic = check_microphone()
    print(json.dumps(mic, indent=2, ensure_ascii=False))

    print("\n" + "=" * 50)
    if cam.get("available") and mic.get("available"):
        print("✅ Cả camera và micro đều sẵn sàng.")
    else:
        issues = []
        if not cam.get("available"):
            issues.append(f"Camera: {cam.get('error', 'unknown')}")
        if not mic.get("available"):
            issues.append(f"Micro: {mic.get('error', 'unknown')}")
        print("⚠ Có vấn đề:\n  " + "\n  ".join(issues))
    print("=" * 50)


if __name__ == "__main__":
    main()
