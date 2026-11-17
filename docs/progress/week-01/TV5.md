# TV5 — Tuần 01: Giao diện mẫu, thu dữ liệu và quyết định phần cứng

- Người phụ trách: TV5 — Trần Quang Huy — Ứng dụng, hiển thị, phụ đề và phần cứng.
- Trạng thái: IN PROGRESS. Giao diện và bộ thu đã có bằng chứng kiểm tra; nhiệm vụ kiểm kê phần cứng, thu pilot với TV2/TV3 và quyết định Ngày 7 chưa xong.
- Thời gian bắt đầu/kết thúc tuần: Tuần 01.
- Cập nhật lần cuối: 2026-11-17.
- Kế hoạch gốc: [phân công TV5](../../plans/05_thanh_vien_5_ung_dung_hien_thi_phan_cung.md).

> Báo cáo này tách rõ ba mức: đã kiểm tra tự động, đã chạy trên thiết bị thật, và chưa kiểm tra. Không có kết quả nhận dạng thật nào được tạo ra trong tuần này vì pipeline TV4 chưa bàn giao; ứng dụng báo "chưa có pipeline nhận dạng" thay vì hiển thị câu giả.

## 1. Nhiệm vụ được giao trong tuần

- [ ] Ngày 1: kiểm kê máy, camera, micro và thiết bị hiển thị với TV1; ghi tài nguyên và giới hạn ngân sách thật.
- [x] Ngày 2: dựng UI có chọn chế độ, Bắt đầu/Dừng, vùng phụ đề 1–2 dòng và trạng thái đang thu/đang xử lý/chưa rõ/lỗi. Dữ liệu giả phải có nhãn “Mô phỏng”.
- [x] Cho chỉnh cỡ chữ, xuống dòng và tương phản; ưu tiên cụm chữ ổn định, chưa làm chữ chạy liên tục.
- [ ] Cùng TV2/TV3 làm bộ thu pilot; lưu audio/video đúng sample_id, thông tin thiết bị và thời điểm.
- [ ] Cùng TV4 ghi clip kiểm tra đồng bộ riêng; cùng TV1 kiểm tra 20 clip pilot.
- [ ] Ngày 7 đưa quyết định phần cứng: thiết bị đã thử được, còn chờ, hoặc dùng laptop. Hỗ trợ tuyển 2 người nói.

Ghi chú cho hai ô còn trống:

- Ô "bộ thu pilot": **đã có đường lưu thật** — `save_capture()` ghi `audio.wav` (float32 mono), `video.avi` (MJPG) và `manifest.json` theo `sample_id`, đã kiểm thử và đã chạy trên thiết bị thật (Task D). Vẫn chưa tick vì chưa có buổi thu pilot chung với TV2/TV3, chưa chốt nơi lưu mẫu và chưa bàn giao mẫu thật.
- `docs/hardware_checklist.md` đã tạo nhưng toàn bộ ô còn "Chưa điền" → Ngày 1 và Ngày 7 chưa đạt.

## 2. Công việc thực tế và trạng thái

### Task A — Nguyên mẫu giao diện Tkinter (Ngày 2)

Trạng thái: **VERIFIED** (kiểm thử tự động).

- `auralens/app/main_window.py`: `AuralensApp` với 2 chế độ, chọn nguồn A/V/AV, nút Bắt đầu/Dừng, vùng phụ đề 1–2 dòng (16–48 pt), đèn trạng thái 5 màu, chuyển tương phản, nhãn "⚠ Mô phỏng".
- Luồng nền: worker thread + `queue.Queue` + `root.after(100, _poll_queue)`; snapshot `mode`/`source` trên main thread trước khi mở worker.
- `tests/test_app.py`: 7 ca kiểm thử UI.

### Task B — Nối bộ thu thật vào ứng dụng (mới trong phiên này)

Trạng thái: **VERIFIED ở mức tự động + chạy thiết bị thật**. Bấm tay trên cửa sổ hiện chưa kiểm tra (mục 4).

- `auralens/app/main_window.py`:
  - `_process_live()` thay placeholder bằng một lượt thu thật: mở `Recorder` → `start_recording(sample_id)` → chờ nút Dừng/đóng cửa sổ → `stop_recording()` → đóng bộ thu trong `finally`.
  - `_recorder_factory` là điểm tiêm cho test; mặc định `_tao_recorder()` import `Recorder` muộn, nên chế độ mock và test UI không cần OpenCV/sounddevice.
  - `_on_close()` đóng bộ thu thêm một lần nữa nếu worker còn kẹt trong driver → thiết bị không bị giữ sau khi tắt app.
  - `camera_index`, `audio_device`, `sample_rate` (mặc định 16 000 Hz) là tham số cấu hình.
- `auralens/capture/recorder.py`: thêm property `device_info` (bản sao dict nội bộ).
- `auralens/app/run.py`: `--camera` được truyền vào app (trước đây bị bỏ qua).
- Hợp đồng message mới giữa worker và UI: `{"type": "device", "text": str}`.

### Task C — Nhãn thiết bị và nhãn chế độ phải trung thực

Trạng thái: **VERIFIED**.

- Nhãn đáy màn hình mặc định là "Thiết bị: chưa mở — bấm Bắt đầu"; chỉ đổi thành `camera WxH · mic <tên thật>` khi `Recorder.device_info` trả về, và "Thiết bị: đã nhả camera & micro" sau khi đóng.
- Xóa câu bịa "Đã nhận dạng trực tiếp từ pipeline." khỏi chế độ live; kết quả một lượt thu là `status=uncertain` với số liệu thật: `Đã thu X giây — chưa có pipeline nhận dạng`.
- Badge chế độ không mock đổi từ "● Trực tiếp" thành "● Thu trực tiếp".

### Task D — Lưu mẫu thu cho bộ thu pilot (TV2/TV3)

Trạng thái: **VERIFIED ở mức tự động + chạy thiết bị thật**.

- `auralens/capture/storage.py` (mới): `save_capture(captured, output_dir)` ghi `<output_dir>/<sample_id>/audio.wav` (WAV **float32 mono**, format code 3 — giữ đúng mẫu pipeline dùng, không lượng tử hoá sang int16), `video.avi` (MJPG, fps suy từ timestamp frame) và `manifest.json`.
- Manifest gồm: `sample_id`, `created_at` (giờ máy kèm offset), `sample_rate`, `duration_ms` (độ dài phiên), `audio_duration_ms`, `num_audio_samples`, `num_frames`, `frame_timestamps_ms` (monotonic ms từ đầu bản thu), `last_frame_timestamp_ms`, `video_fps`, `device_info`, `limit_reached`, `limit_reason`, `max_duration_s`, `files`.
- `sample_id` được kiểm tra trước khi dùng làm tên thư mục (chỉ `[A-Za-z0-9._-]`, 1–64 ký tự) nên `../` hay `a/b` bị từ chối.
- Giới hạn RAM: `Recorder(max_duration_s=15.0, max_frames=450)`; chạm giới hạn thì **ngừng nhận dữ liệu**, `limit_reached`/`limit_reason` được trả về và ghi vào manifest + UI. Frame 640×480 ≈ 0,9 MB nên trần hiện tại ≈ 420 MB (trước đây không có trần).
- UI: kết thúc lượt hiện `Đã thu X giây — đã lưu mẫu <sample_id>` kèm đường dẫn ở dòng meta; lỗi ghi đĩa hiện `chưa lưu được file` chứ không che số liệu thu.
- CLI: `python -m auralens.app.run --no-mock --output-dir recordings --max-seconds 15`.

## 3. Kiến thức đã học và áp dụng

- Vòng đời thiết bị: `open()` ở đầu lượt, `close()` trong `finally`, và đóng lần hai ở `_on_close()` cho trường hợp worker còn kẹt. Đây là cách duy nhất để tiêu chí "app giải phóng thiết bị" có bằng chứng thay vì lời khai.
- Chỉ một chủ sở hữu thiết bị (`Recorder`); UI không tự gọi `cv2.VideoCapture` hay `sd.InputStream` (AGENTS.md mục 6).
- Tkinter không thread-safe: worker chỉ `queue.put`; mọi cập nhật widget nằm trên UI thread trong `_poll_queue`.
- Nhãn trạng thái phần cứng phải sinh từ dữ liệu thật; chữ cứng "sẵn sàng" là một tuyên bố chưa kiểm chứng.
- Module `wave` chỉ ghi PCM số nguyên, nên WAV float32 phải ghi header RIFF tay (format code 3). Nếu dùng `wave` sẽ âm thầm đổi mẫu float32 thành int16.
- Giới hạn thu phải nằm ở `Recorder` (nơi giữ buffer), không ở UI: UI chỉ đọc `limit_reached` để kết thúc lượt và hiển thị.
- `duration_ms` (độ dài phiên) khác `audio_duration_ms`/`last_frame_timestamp_ms` (độ dài nội dung) khi chạm giới hạn — manifest ghi cả hai để TV2/TV3 không suy diễn sai.

## 4. Kiểm tra và số liệu

Môi trường: Windows, Python 3.14.7, Tkinter 9.0, OpenCV 5.0.0, sounddevice 0.5.6, numpy 2.5.5.

**Kiểm thử tự động** — `python -m unittest discover tests`:

```text
Ran 18 tests in 3.528s
OK
```

18/18 đạt, gồm 3 ca tích hợp thiết bị và 8 ca cho phần lưu mẫu / giới hạn:

- `test_live_turn_opens_records_stops_and_releases`: mở → thu → Dừng → đóng; nhãn thiết bị lấy từ `device_info`; phụ đề là "Đã thu…" với `status=uncertain`.
- `test_close_window_mid_recording_releases_devices`: đóng cửa sổ giữa lượt thu vẫn gọi `close()`.
- `test_device_error_is_reported_without_fake_result`: mở thiết bị lỗi → `status=error`, không hiện câu bịa.
- `test_live_turn_writes_audio_video_and_manifest`: lượt thu (Recorder giả) tạo đủ `audio.wav`, `video.avi`, `manifest.json`; kiểm tra header float32 16 kHz, đọc lại được frame và các trường `device_info`/`frame_timestamps_ms`/`created_at`.
- `test_limit_reached_is_reported_and_saved`: chạm giới hạn → phụ đề báo "giới hạn", manifest ghi `limit_reached=true`.
- `test_writes_audio_video_and_manifest`, `test_audio_is_float32_wav`, `test_without_frames_omits_video`, `test_rejects_unsafe_sample_id` (storage), `test_duration_limit_stops_buffering`, `test_invalid_limit_is_rejected` (Recorder): dữ liệu numpy tổng hợp, không cần phần cứng.

**Chạy thật trên thiết bị của máy phát triển** (cửa sổ ẩn, cùng đường code với nút Bắt đầu/Dừng):

```text
LABEL_INITIAL: Thiết bị: chưa mở — bấm Bắt đầu
LABEL_OPEN:    Thiết bị: camera 640×480 · mic Microphone Array (Realtek(R) …
SUBTITLE:      Đã thu 1.2 giây — chưa có pipeline nhận dạng
META:          tv5-… · 19968 mẫu @ 16000 Hz · 36 frame · chưa nối TV4
STATUS:        Chưa nhận dạng rõ
LABEL_CLOSED:  Thiết bị: đã nhả camera & micro
RECORDER_REF:  None
CAMERA_REOPEN_AFTER_CLOSE read_ok: True frame: (480, 640, 3)
```

Camera mở lại và đọc được frame sau khi app đóng → thiết bị đã được nhả.

**Chạy thật với đường lưu file, giới hạn 2 s** (thư mục tạm, cùng `Recorder` + `save_capture` mà app dùng):

```text
DEVICE          640 x 480 | mic Microphone Array (Realtek(R) ...
LIMIT           True duration | dur_ms 2501 | samples 32032 | frames 61
FILES           audio.wav 128172 B · video.avi 1451704 B · manifest.json 1432 B
MANIFEST        sample_rate 16000, num_audio_samples 32032, num_frames 61,
                created_at 2026-11-17T14:34:19+07:00
TS_FIRST_LAST   [47, 66, 97] ... [1937, 1985, 2049]
```

`audio.wav` = 44 + 32.032×4 = 128.172 byte → đúng float32 mono, không lượng tử hoá. Bản ghi chứa giọng/mặt người thu nên nằm ở thư mục tạm và **đã xoá ngay** sau khi đọc số liệu; không có dữ liệu cá nhân nào vào Git.

**Chưa kiểm tra:**

- Bấm tay trên cửa sổ hiện (Bắt đầu → Dừng) — cần một lượt thủ công, xem "Nghiệm thu" bên dưới.
- Chưa có pipeline nhận dạng (TV4 chưa bàn giao) nên không có phụ đề thật.
- Trần bộ nhớ đã có (mặc định 15 s / 450 frame ≈ 420 MB) nhưng chưa thử một lượt dài đúng bằng trần trên thiết bị thật.
- Chưa có mẫu pilot thật nào được TV2/TV3 dùng thử; chưa chốt nơi lưu và người thu.
- Chưa đo độ trễ cuối câu → phụ đề.

### Nghiệm thu tuần 1 (theo mục 4 của kế hoạch)

| Tiêu chí | Kết quả | Bằng chứng |
| --- | --- | --- |
| Text Việt có dấu hiển thị đúng | Đạt | `test_status_indicator_and_subtitle_update`; phụ đề thật ở lần chạy E2E |
| Bắt đầu/Dừng hoạt động | Đạt (mock + live) | `test_mock_recognition_lifecycle`, `test_live_turn_opens_records_stops_and_releases` |
| App giải phóng thiết bị | Đạt ở mức code | E2E: camera mở lại `read_ok=True` sau `_on_close`; test đóng giữa lượt thu |
| Mọi người biết phần kính có trong demo tuần 4 hay không | **Chưa đạt** | `docs/hardware_checklist.md` còn trống, mục 5 chưa có quyết định Ngày 7 |

Lượt nghiệm thu thủ công còn thiếu (khoảng 2 phút):

```bat
..\.venv\Scripts\python.exe -m auralens.app.run --no-mock
```

Bấm **Bắt đầu** → nhãn đáy phải hiện độ phân giải camera và tên micro thật → nói 2–3 giây → bấm **Dừng** → phụ đề hiện "Đã thu … giây — chưa có pipeline nhận dạng" và trạng thái "Chưa nhận dạng rõ" → đóng app → mở lại app và bấm Bắt đầu lần nữa: nếu mở được ngay thì camera đã được nhả.

## 5. Vướng mắc và hỗ trợ cần thiết

- **Chặn bởi TV4:** chưa có API pipeline nên `_process_live` dừng ở mức thu và báo "chưa có pipeline". Không được thay bằng câu giả để demo.
- **Chặn bởi TV1/TV2/TV3:** chưa có buổi thu pilot chung, chưa thống nhất ai lưu file và định dạng lưu.
- **Phần cứng:** chưa có thiết bị hiển thị; Ngày 7 chưa chốt nên chưa thể nói kính có trong demo tuần 4 hay không.
- **Bộ nhớ:** đã có giới hạn thời lượng/số frame ở `Recorder` (mặc định 15 s / 450 frame), nhưng vẫn giữ frame trong RAM tới khi kết thúc lượt; nếu cần thu dài phải stream thẳng ra đĩa.
- **Chưa chốt với TV2/TV3:** nơi lưu mẫu thật (thư mục nào, ai giữ), ai thu, số mẫu và cách đặt `sample_id` ngoài `tv5-<epoch_ms>`.

## 6. Bàn giao, review và tích hợp

- Bản bàn giao: [tv5-ui-prototype.md](../../handoffs/tv5-ui-prototype.md) (đã bổ sung mục 6 về bộ thu thật).
- Nhánh: `feat/tv5-ui-capture-week01` — đã push và mở PR [#9](https://github.com/Stuckwthuw/auralens-avsr/pull/9); chưa merge, đang chờ người review/tích hợp của nhóm (AGENTS.md mục 13).
- Trạng thái: **READY FOR REVIEW** cho Task A/B/C/D. Chưa có REVIEWED/INTEGRATED.
- Người nhận: TV4 (nối pipeline vào `_process_live` hoặc thay chỗ đặt kết quả), TV2 (kiểm tra 16 kHz mono float32 và hợp đồng `sample_id`), TV1 (dùng app để thử khả dụng).

## 7. Việc tiếp theo và thời gian thực tế

- Bàn giao thử định dạng mẫu (mục 7 của bản bàn giao) cho TV2/TV3, chốt nơi lưu và người thu mẫu pilot.
- Điền `hardware_checklist.md` bằng số liệu thật rồi chốt Ngày 7: laptop hay kính.
- Một lượt nghiệm thu thủ công trên cửa sổ hiện (lệnh ở mục 4) và ghi kết quả vào báo cáo.
- Thống nhất với TV4 điểm đặt kết quả nhận dạng (`queue` message `subtitle`) để thay dòng "chưa có pipeline".
- Cùng TV2/TV3 chốt: lưu file thô ở đâu, ai resample, giới hạn thời lượng một lượt thu.
