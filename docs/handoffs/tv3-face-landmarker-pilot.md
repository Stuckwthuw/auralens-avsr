# TV3 — Hoàng Hiếu — Pilot Face Landmarker

Task / người phụ trách / nhánh / commit: thử trích vùng miệng tuần 1 / Hoàng Hiếu / `feat/tv3-hoang-hieu-mouth-pilot` / `a6ce501` (script; báo cáo và bàn giao trong cùng nhánh).

Đầu ra và file/module thay đổi: `auralens/vision/pilot_landmarks.py`, `auralens/vision/requirements-pilot.txt`, `docs/progress/week-01/TV3.md`. Script đọc video từng frame ở độ phân giải gốc, giữ timestamp mili giây của nguồn, trả `no_face` khi model không tìm thấy mặt và ghi ảnh crop có điểm môi. Script chưa tự phát hiện nhiều mặt. Ảnh/JSON chứa dữ liệu khuôn mặt chỉ ghi ra thư mục ngoài Git.

Hợp đồng dùng hoặc thay đổi: chưa có hợp đồng TV4. JSON có `pilot_only: true`, `sample_id`, `source_width_px`, `source_height_px`, danh sách chỉ số điểm môi và các frame `{timestamp_ms, valid, reason, lip_landmarks}` để khảo sát; không được dùng như đầu ra tích hợp hoặc benchmark. FPS không được cố định hoặc suy ra từ thứ tự frame; mỗi frame giữ timestamp nguồn. Nếu kích thước frame đổi trong cùng clip, script báo lỗi thay vì ngầm resize. Script dùng `num_faces=1` để theo dõi một người và yêu cầu `--single-person-confirmed`; nó không tự phát hiện clip nhiều người. `valid` chỉ là điều kiện model trả điểm môi sau xác nhận thủ công, chưa kiểm tra chất lượng khẩu hình.

Cách chạy và kiểm tra đã thực hiện:

1. Windows, Python 3.14.6; tạo venv riêng và cài `pip install -r auralens/vision/requirements-pilot.txt`.
2. Tải model chính thức từ `https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task` vào thư mục ngoài repo. SHA-256 đã dùng: `64184e229b263107bc2b804c6625db1341ff2bb731874b0bcc2fe6544e0bc9ff`.
3. Chạy từ root của nhánh, thay các đường dẫn bằng file cục bộ của người chạy:

   ```powershell
   .\.venv\Scripts\python.exe auralens\vision\pilot_landmarks.py --video '<video-pilot.mp4>' --model '<face_landmarker.task>' --output "$env:TEMP\auralens-tv3-pilot" --sample-id pilot_tv3_001 --single-person-confirmed
   ```

4. Đã chạy trên ba clip cá nhân cục bộ, kiểm tra `python -m compileall -q auralens/vision/pilot_landmarks.py` và xác nhận script từ chối output nằm trong checkout hoặc khi chưa xác nhận một người. `ffprobe` được dùng để đối chiếu 10 timestamp đầu của mỗi clip. Không đưa clip, ảnh crop hoặc JSON landmarks vào Git.

Kết quả thật / mock / chưa kiểm tra: clip đầu dài 13,008 giây, 1920 × 1080, 376 frame. Cấu hình thử ban đầu `num_faces=2`: 160/376 frame có điểm môi (42,6%), 216 frame `no_face`. Chạy lại với `num_faces=1`: 177/376 frame (47,1%), 199 frame `no_face`. Clip mới dài 7,471 giây, 1920 × 1080, 212 frame: `num_faces=2` cho 27/212 frame (12,7%); `num_faces=1` cho 212/212 frame (100%). Đây là so sánh cấu hình trên cùng clip, không phải test độc lập. Hai crop ở khoảng 1 và 5 giây của clip mới được xem trực quan, điểm bám đúng miệng nhưng crop chỉ rộng khoảng 84–95 px; chưa biết đủ chi tiết để phân loại câu hay không. Số đo webcam trực tiếp 640 × 480, 27,1 FPS là phép thử khác; không suy hiệu năng live từ thời gian xử lý file. Chưa kiểm tra 20 clip, không có kết quả phân loại 10 câu.

Clip thứ ba dài 2,558 giây, 1920 × 1080, 68 frame: `num_faces=1` trả điểm môi ở 68/68 frame (100%), timestamp từ 0 đến 2512 ms. 10 timestamp đầu khớp `ffprobe` sau làm tròn. Các mốc hình đã xem cho thấy một người và vị trí mặt tương đối ổn định; miệng mở rõ gần giây 1,84. Crop có điểm môi gần giây 1 kích thước 123 × 80 px. Chưa xác nhận nhãn câu nói hoặc kiểm tra chất lượng cho phân loại.

Người nhận và việc có thể làm tiếp: TV4 xem schema timestamp/invalid và chốt hợp đồng chung; TV3 xác nhận clip thứ ba có đúng một câu, kiểm tra chất lượng crop trên cả đoạn và bổ sung phép kiểm nhiều người trước tích hợp; TV5 phối hợp thử webcam tích hợp. Script này chưa ở trạng thái READY FOR REVIEW cho tích hợp.

Vướng mắc, cách tái hiện, điều đã thử: clip đầu thay đổi khoảng cách/hướng mặt nên tỷ lệ frame phát hiện thấp. Clip mới ổn định hơn nhưng với `num_faces=2` model bỏ lỡ nhiều frame dù ảnh vẫn thấy mặt; `num_faces=1` giải quyết trường hợp một người trên clip này. [Tài liệu MediaPipe](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker?hl=en) ghi chế độ làm mượt chỉ áp dụng khi `num_faces=1`. Chưa hiệu chỉnh ngưỡng trên dev; chưa kiểm tra ca nhiều người.

## Bổ sung kiểm tra ba ca khó ngày 2026-11-14

Chạy cùng script, model SHA-256 và môi trường nêu trên với `num_faces=1`; đầu ra JSON nằm trong `%TEMP%\auralens-tv3-negative-165042`, `...-165029` và `...-165125`, không đưa vào Git. Quan sát contact sheet lấy khoảng mỗi giây để mô tả điều kiện; đây là nhận xét trực quan, không phải nhãn tự động.

- `WIN_20261114_16_50_42_Pro.mp4`: mặt quay sang bên rồi cúi xuống, 1920 × 1080, 162 frame, timestamp 0–6432 ms. Kết quả 0/162 frame có landmarks, 162 frame `no_face`.
- `WIN_20261114_16_50_29_Pro.mp4`: phần lớn khung hình trống, đôi lúc người đi sát mép khung hình; không gọi đây là clip hoàn toàn không có người. 1920 × 1080, 175 frame, timestamp 0–6160 ms. Kết quả 0/175 frame có landmarks, 175 frame `no_face`.
- `WIN_20261114_16_51_25_Pro.mp4`: một người đứng xa camera, bàn tay che miệng xuyên suốt ảnh lấy mẫu. 1920 × 1080, 196 frame, timestamp 0–6768 ms. Kết quả 0/196 frame có landmarks, 196 frame `no_face`.

Ba clip đều bị từ chối ở bước phát hiện mặt. Vì vậy clip che miệng **chưa kiểm tra được** khả năng phân biệt miệng bị che sau khi đã phát hiện mặt; khoảng cách và kích thước mặt cũng có thể ảnh hưởng. `no_face` chỉ có nghĩa Face Landmarker không trả landmarks, không khẳng định khung hình hoàn toàn không có người. Bước tiếp theo của TV3: quay một clip che miệng ở khoảng cách 20–50 cm, cùng vị trí/ánh sáng với clip mặt rõ, rồi so sánh theo frame; chưa hiệu chỉnh thuật toán bằng ba ca khó này và chưa đánh dấu READY FOR REVIEW cho tích hợp.
