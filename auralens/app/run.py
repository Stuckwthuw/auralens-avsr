"""Entry point for the Auralens subtitle application.

Usage:
    python -m auralens.app.run [--mock]

Flags:
    --mock    Run with simulated data (labeled as 'Mô phỏng')
"""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Auralens — Vietnamese audio-visual subtitle prototype"
    )
    parser.add_argument(
        "--mock", action="store_true", default=True,
        help="Run with simulated recognition results (default: True in week 1)"
    )
    parser.add_argument(
        "--camera", type=int, default=0,
        help="Camera device index (default: 0)"
    )
    parser.add_argument(
        "--output-dir", default="recordings",
        help="Directory for saved pilot samples (default: recordings)"
    )
    parser.add_argument(
        "--max-seconds", type=float, default=15.0,
        help="Maximum length of one capture turn in seconds (default: 15)"
    )
    parser.add_argument(
        "--no-mock", action="store_true",
        help="Disable mock mode (requires pipeline connection)"
    )
    args = parser.parse_args()

    mock_mode = not args.no_mock

    from auralens.app.main_window import AuralensApp
    app = AuralensApp(
        mock_mode=mock_mode,
        camera_index=args.camera,
        output_dir=args.output_dir,
        max_duration_s=args.max_seconds,
    )
    app.run()


if __name__ == "__main__":
    main()
