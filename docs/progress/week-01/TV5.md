# TV5 — Tuần 01: Giao diện mẫu, thu dữ liệu và quyết định phần cứng

- Người phụ trách: TV5 — Ứng dụng, hiển thị, phụ đề và phần cứng. (Tên thật: chưa xác định — chưa điền theo mẫu "Họ tên — Nhiệm vụ đang làm".)
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

- Ô "bộ thu pilot": phần **code** đã xong và đã chạy thật (mục 2, Task B) nhưng chưa có bàn giao dữ liệu cho TV2/TV3 và chưa ghi file — nên chưa tick.
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

## 3. Kiến thức đã học và áp dụng

- Vòng đời thiết bị: `open()` ở đầu lượt, `close()` trong `finally`, và đóng lần hai ở `_on_close()` cho trường hợp worker còn kẹt. Đây là cách duy nhất để tiêu chí "app giải phóng thiết bị" có bằng chứng thay vì lời khai.
- Chỉ một chủ sở hữu thiết bị (`Recorder`); UI không tự gọi `cv2.VideoCapture` hay `sd.InputStream` (AGENTS.md mục 6).
- Tkinter không thread-safe: worker chỉ `queue.put`; mọi cập nhật widget nằm trên UI thread trong `_poll_queue`.
- Nhãn trạng thái phần cứng phải sinh từ dữ liệu thật; chữ cứng "sẵn sàng" là một tuyên bố chưa kiểm chứng.

## 4. Kiểm tra và số liệu

Môi trường: Windows, Python 3.14.7, Tkinter 9.0, OpenCV 5.0.0, sounddevice 0.5.6, numpy 2.5.5.

**Kiểm thử tự động** — `python -m unittest discover tests`:

```text
Ran 10 tests in 3.311s
OK
```

10/10 đạt, gồm 3 ca mới cho tích hợp thiết bị:

- `test_live_turn_opens_records_stops_and_releases`: mở → thu → Dừng → đóng; nhãn thiết bị lấy từ `device_info`; phụ đề là "Đã thu…" với `status=uncertain`.
- `test_close_window_mid_recording_releases_devices`: đóng cửa sổ giữa lượt thu vẫn gọi `close()`.
- `test_device_error_is_reported_without_fake_result`: mở thiết bị lỗi → `status=error`, không hiện câu bịa.

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

**Chưa kiểm tra:**

- Bấm tay trên cửa sổ hiện (Bắt đầu → Dừng) — cần một lượt thủ công, xem "Nghiệm thu" bên dưới.
- Chưa có pipeline nhận dạng (TV4 chưa bàn giao) nên không có phụ đề thật.
- Chưa ghi audio/video ra đĩa; frame được giữ trong RAM nên lượt thu càng dài càng tốn bộ nhớ (~27 MB/giây ở 640×480×3, 30 fps).
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
- **Rủi ro bộ nhớ:** giữ toàn bộ frame trong RAM; cần giới hạn thời lượng hoặc bật/tắt ghi frame trước khi thu dài.

## 6. Bàn giao, review và tích hợp

- Bản bàn giao: [tv5-ui-prototype.md](../../handoffs/tv5-ui-prototype.md) (đã bổ sung mục 6 về bộ thu thật).
- Nhánh: `feat/tv5-ui-capture-week01` — đã push và mở PR [#9](https://github.com/Stuckwthuw/auralens-avsr/pull/9); chưa merge, đang chờ người review/tích hợp của nhóm (AGENTS.md mục 13).
- Trạng thái: **READY FOR REVIEW** cho Task A/B/C. Chưa có REVIEWED/INTEGRATED.
- Người nhận: TV4 (nối pipeline vào `_process_live` hoặc thay chỗ đặt kết quả), TV2 (kiểm tra 16 kHz mono float32 và hợp đồng `sample_id`), TV1 (dùng app để thử khả dụng).

## 7. Việc tiếp theo và thời gian thực tế

- Điền `hardware_checklist.md` bằng số liệu thật rồi chốt Ngày 7: laptop hay kính.
- Một lượt nghiệm thu thủ công trên cửa sổ hiện (lệnh ở mục 4) và ghi kết quả vào báo cáo.
- Thống nhất với TV4 điểm đặt kết quả nhận dạng (`queue` message `subtitle`) để thay dòng "chưa có pipeline".
- Cùng TV2/TV3 chốt: lưu file thô ở đâu, ai resample, giới hạn thời lượng một lượt thu.
