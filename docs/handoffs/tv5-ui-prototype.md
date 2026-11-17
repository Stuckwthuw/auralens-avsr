# Bàn giao TV5: Nguyên mẫu Giao diện người dùng Auralens (Tkinter UI Prototype)

- **Người phụ trách:** TV5 — Ứng dụng, hiển thị phụ đề và phần cứng.
- **Ngày thực hiện:** 2026-11-16.
- **Mã nguồn:** `auralens/app/__init__.py`, `auralens/app/main_window.py`.
- **Kiểm thử:** `tests/test_app.py`.

---

## 1. Đầu ra và File / Module thay đổi

- `auralens/app/__init__.py`: Package init exporting `AuralensApp`.
- `auralens/app/main_window.py`: Toàn bộ ứng dụng Tkinter `AuralensApp`:
  - 2 chế độ độc lập: `"Phụ đề tiếng Việt từ âm thanh"` (ASR tự do) và `"Thí nghiệm 10 câu nghe–nhìn"` (10 câu A/V/AV).
  - Nút chuyển trạng thái "Bắt đầu" / "Dừng" (`_on_start_stop()`).
  - Vùng hiển thị phụ đề lớn, 1–2 dòng, font Segoe UI/Arial 24pt+ (mặc định 28pt), hỗ trợ co giãn dòng tự động (dynamic wrap).
  - Đèn báo trạng thái trực quan: `"Sẵn sàng"` (xám), `"Đang thu..."` (đỏ), `"Đang xử lý..."` (cam), `"Chưa nhận dạng rõ"` (vàng), `"Lỗi"` (nền đỏ).
  - Điều khiển cỡ chữ: nút `+` / `−` và thanh trượt slider (giới hạn 16pt – 48pt).
  - Nút chuyển đổi tương phản cao: Chế độ tối (nền đen `#000000`, chữ trắng) / Chế độ sáng (nền trắng `#ffffff`, chữ đen).
  - Bộ chọn nguồn A / V / AV: Radio buttons chỉ hiển thị khi ở chế độ thí nghiệm 10 câu.
  - Nhãn dữ liệu giả: Huy hiệu `"⚠ Mô phỏng"` nổi bật màu vàng hổ phách ở thanh trạng thái (`mock_mode=True`).
  - Thanh trạng thái đáy hiển thị: Chế độ hiện hành, trạng thái phần cứng thiết bị, nhãn mô phỏng.
  - Quản lý luồng an toàn: Xử lý nền tách biệt, đồng bộ dữ liệu giao diện qua `queue.Queue` và `root.after(100, _poll_queue)`.
  - Giải phóng tài nguyên và dừng luồng an toàn khi đóng cửa sổ (`_on_close`).

## 2. Hợp đồng sử dụng và kết nối

- Tuân thủ hợp đồng TV1 (`PREDEFINED_10_SENTENCES` gồm `c00` đến `c09` và trạng thái `UNCERTAIN_EXPERIMENT_TEXT = "Chưa nhận dạng được"`).
- Tuân thủ hợp đồng TV4 (`sample_id`, `status` gồm `ok` -> `Sẵn sàng`, `uncertain` -> `Chưa nhận dạng rõ`, `error` -> `Lỗi`).
- Giao tiếp luồng xử lý qua hàng đợi `self.queue`:
  - Message `status`: `{"type": "status", "status": STATUS_*}`
  - Message `subtitle`: `{"type": "subtitle", "text": str, "status": STATUS_*, "meta": str, "finished": bool}`
  - Message `error`: `{"type": "error", "text": str, "status": STATUS_ERROR, "finished": bool}`

## 3. Cách chạy và kiểm tra đã thực hiện

1. **Khởi chạy ứng dụng trực tiếp:**
   ```powershell
   python auralens/app/main_window.py
   # hoặc:
   python -m auralens.app.main_window
   ```

2. **Chạy bộ kiểm thử tự động (unittest):**
   ```powershell
   python -m unittest discover tests
   ```
   Kết quả: 7/7 tests passed trong 3.19 giây:
   - `test_window_properties`: Kiểm tra kích thước tối thiểu >= 800x400, tiêu đề cửa sổ, nhãn mô phỏng.
   - `test_mode_selection_and_source_visibility`: Kiểm tra chuyển chế độ và ẩn/hiện bộ chọn A/V/AV.
   - `test_font_size_controls`: Kiểm tra nút +/-, slider và chặn biên [16, 48].
   - `test_contrast_toggle`: Kiểm tra đảo giao diện sáng/tối.
   - `test_status_indicator_and_subtitle_update`: Kiểm tra cả 5 trạng thái và cập nhật phụ đề.
   - `test_mock_data_contents`: Kiểm tra 10 câu định trước và tập câu mẫu ASR.
   - `test_mock_recognition_lifecycle`: Kiểm tra luồng chạy ngầm mô phỏng (bắt đầu -> thu -> xử lý -> trả kết quả).

## 4. Kết quả thật / mock / chưa kiểm tra

- **Đã kiểm tra:**
  - Kiểm tra hoàn tất trên Python 3.14 (Windows) với Tkinter 9.0.
  - Toàn bộ thao tác giao diện không bị giật/đơ nhờ chạy worker thread.
  - Bắt lỗi luồng Python 3.14 (không truy cập biến Tkinter từ thread con).
  - Tự động ngắt luồng nền khi đóng ứng dụng.
- **Đang mock:**
  - Dữ liệu nhận dạng đang chạy `_process_mock()` với nhãn `⚠ Mô phỏng` hiển thị rõ ràng.
- **Chưa kiểm tra:**
  - Tích hợp pipeline thật của TV4 (chờ TV4 bàn giao API tích hợp).
  - Xuất phụ đề sang phần cứng kính (hiện chạy hoàn chỉnh trên màn hình laptop).

## 5. Người nhận và việc có thể làm tiếp

- **TV4 (Tích hợp):** Có thể nối API suy luận của pipeline vào phương thức `_process_live()` hoặc qua hàng đợi `app.queue`.
- **TV1 (Đánh giá):** Có thể sử dụng bản mẫu này để kiểm thử tính khả dụng và khảo sát người dùng về kích thước chữ, độ tương phản.

## 6. Cập nhật 2026-11-16 — bộ thu thật đã nối vào ứng dụng

- **Chạy chế độ thu thật:**
  ```powershell
  python -m auralens.app.run --no-mock --camera 0
  ```
  Bấm **Bắt đầu** để mở camera + micro, bấm **Dừng** để kết thúc lượt. Nhãn đáy màn hình đọc từ `Recorder.device_info` (độ phân giải camera, tên micro thật), không còn chữ cứng "sẵn sàng".
- **Không còn kết quả giả:** chế độ live kết thúc lượt bằng `status=uncertain` và câu "Đã thu X giây — chưa có pipeline nhận dạng" kèm `sample_id`, số mẫu, số frame. Khi TV4 nối pipeline, chỉ cần thay chỗ đặt message `subtitle`; không đổi giao diện.
- **Giải phóng thiết bị:** `Recorder.close()` nằm trong `finally` của lượt thu và được gọi lại ở `_on_close()`. Đã kiểm tra: sau khi đóng app, `cv2.VideoCapture(0).read()` mở lại thành công.
- **Hợp đồng message mới:** `{"type": "device", "text": str}` — worker gửi, UI chỉ cập nhật nhãn ở `_poll_queue`.
- **Điểm tiêm để test:** `AuralensApp(..., recorder_factory=...)`; test dùng `FakeRecorder`, không cần phần cứng.
- **Chưa làm:** chưa ghi audio/video ra file, frame còn giữ trong RAM, chưa đo độ trễ cuối câu → phụ đề.
