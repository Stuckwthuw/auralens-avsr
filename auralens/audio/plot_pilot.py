"""Plot waveform, spectrogram, and MFCC for one WAV selected at runtime."""

from pathlib import Path

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


SAMPLE_RATE = 16_000
N_FFT = 512
HOP_LENGTH = 160
N_MFCC = 13


def plot_file(
    audio_path: str | Path, output_dir: str | Path | None = None
) -> tuple[Path, tuple[int, int]]:
    """Plot one WAV; default output is the current directory, not the WAV folder.

    Pass ``output_dir`` to choose another writable destination. This avoids
    failing merely because the source audio directory is read-only.
    """
    path = Path(audio_path).expanduser()
    if not path.is_file():
        raise FileNotFoundError(f"Audio file not found: {path}")

    # librosa resamples to 16 kHz and converts to mono for this visualization.
    audio, sample_rate = librosa.load(path, sr=SAMPLE_RATE, mono=True)
    stft = librosa.stft(audio, n_fft=N_FFT, hop_length=HOP_LENGTH)
    spectrogram = librosa.amplitude_to_db(np.abs(stft), ref=np.max)
    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=sample_rate,
        n_mfcc=N_MFCC,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
    )

    _figure, axes = plt.subplots(3, 1, figsize=(12, 10))

    time = np.arange(len(audio)) / sample_rate
    axes[0].plot(time, audio, linewidth=0.5)
    axes[0].set(title="Waveform", xlabel="Time (s)", ylabel="Amplitude")

    librosa.display.specshow(
        spectrogram,
        sr=sample_rate,
        hop_length=HOP_LENGTH,
        x_axis="time",
        y_axis="linear",
        ax=axes[1],
    )
    axes[1].set(title="Spectrogram", xlabel="Time (s)", ylabel="Frequency (Hz)")

    librosa.display.specshow(
        mfcc,
        sr=sample_rate,
        hop_length=HOP_LENGTH,
        x_axis="time",
        ax=axes[2],
    )
    axes[2].set(
        title=f"MFCC — shape {mfcc.shape} (coefficients, frames)",
        xlabel="Time (s)",
        ylabel="MFCC coefficient index",
    )

    plt.tight_layout()
    destination = Path(output_dir).expanduser() if output_dir else Path.cwd()
    destination.mkdir(parents=True, exist_ok=True)
    output_path = destination / f"{path.stem}_waveform_spectrogram_mfcc.png"
    plt.savefig(output_path, dpi=150)
    print(f"Saved plot: {output_path}")
    print(f"Analysis sample rate: {sample_rate} Hz")
    print(f"MFCC shape: {mfcc.shape}")
    plt.show()
    return output_path, mfcc.shape


def main() -> None:
    audio_path = input("Enter WAV path: ").strip().strip('"')
    if audio_path:
        output_dir = input("Output folder (Enter for current folder): ").strip().strip('"')
        plot_file(audio_path, output_dir or None)


if __name__ == "__main__":
    main()
