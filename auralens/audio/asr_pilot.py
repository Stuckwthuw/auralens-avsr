"""Local-file ``asr_free`` transcription pilot, not the 10-class audio task.

The model loads only when instantiated. This module transcribes free-form speech;
it does not classify the project's ten fixed phrases.
"""

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
    """Load one model instance and reuse it for ``asr_free`` audio files."""

    def __init__(self, config: ASRConfig | None = None) -> None:
        self.config = config or ASRConfig()
        started = perf_counter()
        self._model = WhisperModel(
            self.config.model_size,
            device=self.config.device,
            compute_type=self.config.compute_type,
        )
        self.model_ready_ms = round((perf_counter() - started) * 1000)

    def transcribe_file(
        self, audio_path: str | Path, *, sample_id: str
    ) -> dict[str, str | int]:
        """Transcribe one ``asr_free`` file and return contract metadata.

        ``sample_id`` is supplied by the caller so local filenames are not
        treated as sample identifiers or exposed in the result.
        """
        if not sample_id.strip():
            raise ValueError("sample_id must be a non-empty sample identifier")
        sample_id = sample_id.strip()
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
        return {
            "sample_id": sample_id,
            "mode": "asr_free",
            "text": text,
            "status": "ok",
            "reason": "",
            "model_version": f"faster-whisper/{self.config.model_size}",
            "infer_ms": infer_ms,
        }


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
    print("Task: asr_free transcription (not the 10-class audio classifier).")
    print("Enter a sample_id and one WAV path per prompt. Empty sample_id quits.")

    while True:
        sample_id = input("\nsample_id: ").strip()
        if not sample_id:
            break
        audio_path = input("WAV: ").strip().strip('"')
        if not audio_path:
            print("WAV path is required for this sample_id.")
            continue
        try:
            result = recognizer.transcribe_file(audio_path, sample_id=sample_id)
        except FileNotFoundError as error:
            print(error)
            continue
        except ValueError as error:
            print(error)
            continue
        print(f"Sample: {result['sample_id']} | mode={result['mode']}")
        print(f"Model: {result['model_version']} | status={result['status']}")
        print(f"Inference: {result['infer_ms']} ms")
        print(f"Transcript: {result['text']}")


if __name__ == "__main__":
    main()
