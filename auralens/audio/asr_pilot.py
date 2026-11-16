"""Local Vietnamese Faster-Whisper pilot. The model loads only when instantiated."""

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

from faster_whisper import WhisperModel


@dataclass(frozen=True)
class ASRConfig:
    """Runtime options used by the TV2 pilot baseline."""

    model_size: str = "medium"
    device: str = "cpu"
    compute_type: str = "int8"
    language: str = "vi"


class FasterWhisperASR:
    """Load one model instance and reuse it for multiple audio files."""

    def __init__(self, config: ASRConfig | None = None) -> None:
        self.config = config or ASRConfig()
        started = perf_counter()
        self._model = WhisperModel(
            self.config.model_size,
            device=self.config.device,
            compute_type=self.config.compute_type,
        )
        self.model_ready_ms = round((perf_counter() - started) * 1000)

    def transcribe_file(self, audio_path: str | Path) -> dict[str, str | int]:
        """Return Vietnamese transcript text and file inference time in ms."""
        path = Path(audio_path).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f"Audio file not found: {path}")

        started = perf_counter()
        segments, _info = self._model.transcribe(
            str(path),
            language=self.config.language,
            task="transcribe",
        )
        text = " ".join(segment.text.strip() for segment in segments).strip()
        infer_ms = round((perf_counter() - started) * 1000)
        return {"text": text, "infer_ms": infer_ms}


def main() -> None:
    recognizer = FasterWhisperASR()
    print(
        "Config: "
        f"model={recognizer.config.model_size}, "
        f"device={recognizer.config.device}, "
        f"compute_type={recognizer.config.compute_type}, "
        f"language={recognizer.config.language}, task=transcribe"
    )
    print(f"Model ready: {recognizer.model_ready_ms} ms")
    print("Enter one WAV path per prompt. Press Enter on an empty prompt to quit.")

    while True:
        audio_path = input("\nWAV: ").strip().strip('"')
        if not audio_path:
            break
        try:
            result = recognizer.transcribe_file(audio_path)
        except FileNotFoundError as error:
            print(error)
            continue
        print(f"Inference: {result['infer_ms']} ms")
        print(f"Transcript: {result['text']}")


if __name__ == "__main__":
    main()
