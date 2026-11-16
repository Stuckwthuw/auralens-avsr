# TV2 — ASR pilot handoff

## Scope

This is a local-file Vietnamese ASR pilot, not the integrated TV4 pipeline and not the 10-class audio classifier. WAV files, Buzz TXT files, and the conversational recording stay outside Git. Use an approved group data store if another member needs to inspect audio.

## Repository files

- `auralens/audio/asr_pilot.py`: Faster-Whisper wrapper. Construct `FasterWhisperASR` once and call `transcribe_file(path)` for each file; the model is reused within that object.
- `auralens/audio/plot_pilot.py`: creates waveform, spectrogram, and MFCC plots for a WAV selected at runtime.
- `auralens/audio/requirements-pilot.txt`: pinned environment snapshot captured from Dương's local pilot environment.

## Environment and configuration

- OS: Windows (exact release not recorded); Python: 3.14.4.
- ASR: Faster-Whisper 1.2.1 / Whisper Medium / CPU / `int8` / Vietnamese (`vi`) / `transcribe`.
- Plotting: librosa 1.0.1 and Matplotlib 3.11.2; plot input is resampled by librosa to mono 16 kHz.
- The full package snapshot is in `auralens/audio/requirements-pilot.txt`.

## Run from the repository root (Windows CMD)

Create and activate an environment, then install the pinned packages:

```cmd
py -3.14 -m venv .venv
.venv\Scripts\activate
python -m pip install -r auralens\audio\requirements-pilot.txt
```

Run ASR; enter one WAV path at each prompt. The first model load may need internet access to download Whisper Medium. The audio path can point to a file outside the repository.

```cmd
python -m auralens.audio.asr_pilot
```

Run the three-plot script; enter a WAV path when prompted. The PNG is saved beside that WAV.

```cmd
python -m auralens.audio.plot_pilot
```

## Sanitized pilot log

Captured 2026-11-16. Absolute paths and speaker-identifying names are omitted. The table includes only the 10 short scripted Buzz pilot outputs; the natural conversation transcript is not shared.

### Buzz: 10 scripted pilot clips

The transcript column is the actual Buzz export text. No ground-truth transcript is claimed for clips whose intended sentence has not been confirmed.

| Sample | Buzz output |
|---|---|
| `sample_01` | Mảy tính chuyển lời nói thành văn bản |
| `sample_02` | Hôm nay tôi kiểm tra micro |
| `sample_03` | Tôi muốn thử nhận dạng bằng tiếng Việt |
| `sample_04` | Tôi sẽ đọc chậm và rõ ràng. |
| `sample_05` | Ngày mai tôi sẽ học tiếp |
| `sample_06` | Buổi sáng nay thời tiết khá mát |
| `sample_07` | Tôi đang học cách xử lý âm thanh! |
| `sample_08` | Xin hãy chép lại đúng những gì tôi nói |
| `sample_09` | Tôi sẽ lưu bản ghi này vào từ một thử nghiệm. |
| `sample_10` | chiếc micro đặt trên mà gần máy tính |

| Run | Input | Configuration | Model ready | Inference | Notes |
|---|---|---|---:|---:|---|
| `fw-medium-01` | `sample_09`, 7.680 s, mono 48 kHz | Faster-Whisper Medium, CPU `int8`, `vi`, transcribe | 5,138 ms (once per process) | 6,963 ms | File-path inference; no separate 16 kHz WAV was supplied. |
| `fw-medium-02` | `sample_04`, 4.544 s, mono 16 kHz | Same process/config as above | Reused loaded model | 7,559 ms | Confirms reuse in one local process; not streaming latency. |
| `buzz-pilot-10` | 10 unique short WAVs | Buzz / Whisper.cpp Medium / Vietnamese / Transcribe, as reported by Dương | Not recorded by Buzz export | Not recorded | 10 TXT exports exist locally. Ground truth is incomplete; CER was not computed. |
| `conversation-01` | 38.933 s, mono 16 kHz, two speakers | Buzz / Whisper.cpp Medium / Vietnamese / Transcribe | Not recorded | Not recorded | Dương reported several proper-name/phrase transcription errors. Text and names are withheld. |

The timings above are measurements from Dương's laptop (Intel Core i5-10300H, 15.8 GB available RAM, NVIDIA GTX 1650 4 GB, Intel UHD Graphics). The ASR run used CPU; timings are not a benchmark across machines. No accuracy percentage is claimed.

## AI-use disclosure

ChatGPT helped explain audio/ASR concepts, draft the pilot scripts and run instructions, and summarize results. Audio recordings were made by Dương; Buzz and Faster-Whisper produced the reported transcripts. The shared log includes outputs from the 10 scripted pilot clips but omits absolute paths, the natural conversation transcript, and speaker-identifying names. No audio files are included in this repository.

## Verification status and next handoff

The original local scripts were run by Dương. The repository copy and clean-environment install have not yet been independently rerun or reviewed by TV4. Treat this as an implemented pilot handoff pending another member's verification, not as an integrated API.
