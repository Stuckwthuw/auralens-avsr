"""Capture module — owns camera and microphone devices."""

try:
    from auralens.capture.recorder import Recorder

    __all__ = ["Recorder"]
except ImportError:
    __all__ = []
