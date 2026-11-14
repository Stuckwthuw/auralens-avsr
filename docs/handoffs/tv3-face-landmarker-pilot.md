# TV3 — Hoàng Hiếu — Pilot Face Landmarker

Task / người phụ trách / nhánh / commit: thử trích vùng miệng tuần 1 / Hoàng Hiếu / `feat/tv3-hoang-hieu-mouth-pilot` / `a6ce501` (script; báo cáo và bàn giao trong cùng nhánh).

Đầu ra và file/module thay đổi: `auralens/vision/pilot_landmarks.py`, `auralens/vision/requirements-pilot.txt`, `docs/progress/week-01/TV3.md`. Script đọc video từng frame, giữ timestamp mili giây của nguồn, trả `no_face` hoặc `multiple_faces` khi không có đúng một mặt, và ghi ảnh crop có điểm môi. Ảnh/JSON chứa dữ liệu khuôn mặt chỉ ghi ra thư mục ngoài Git.

Hợp đồng dùng hoặc thay đổi: chưa có hợp đồng TV4. JSON có `pilot_only: true`, `sample_id`, danh sách chỉ số điểm môi và các frame `{timestamp_ms, valid, reason, lip_landmarks}` để khảo sát; không được dùng như đầu ra tích hợp hoặc benchmark. Script dùng `num_faces=1` để theo dõi một người và yêu cầu `--single-person-confirmed`; nó không tự phát hiện clip nhiều người. `valid` chỉ là điều kiện model trả điểm môi sau xác nhận thủ công, chưa kiểm tra chất lượng khẩu hình.

Cách chạy và kiểm tra đã thực hiện:

1. Windows, Python 3.14.6; tạo venv riêng và cài `pip install -r auralens/vision/requirements-pilot.txt`.
2. Tải model chính thức từ `https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task` vào thư mục ngoài repo. SHA-256 đã dùng: `64184e229b263107bc2b804c6625db1341ff2bb731874b0bcc2fe6544e0bc9ff`.
3. Chạy từ root của nhánh, thay các đường dẫn bằng file cục bộ của người chạy:

   ```powershell
   .\.venv\Scripts\python.exe auralens\vision\pilot_landmarks.py --video '<video-pilot.mp4>' --model '<face_landmarker.task>' --output "$env:TEMP\auralens-tv3-pilot" --sample-id pilot_tv3_001 --single-person-confirmed
   ```

4. Đã chạy trên hai clip cá nhân cục bộ, kiểm tra `python -m compileall -q auralens/vision/pilot_landmarks.py` và xác nhận script từ chối output nằm trong checkout hoặc khi chưa xác nhận một người. `ffprobe` được dùng để đối chiếu 10 timestamp đầu của mỗi clip. Không đưa clip, ảnh crop hoặc JSON landmarks vào Git.

Kết quả thật / mock / chưa kiểm tra: clip đầu dài 13,008 giây, 1920 × 1080, 376 frame. Cấu hình thử ban đầu `num_faces=2`: 160/376 frame có điểm môi (42,6%), 216 frame `no_face`. Chạy lại với `num_faces=1`: 177/376 frame (47,1%), 199 frame `no_face`. Clip mới dài 7,471 giây, 1920 × 1080, 212 frame: `num_faces=2` cho 27/212 frame (12,7%); `num_faces=1` cho 212/212 frame (100%). Đây là so sánh cấu hình trên cùng clip, không phải test độc lập. Hai crop ở khoảng 1 và 5 giây của clip mới được xem trực quan, điểm bám đúng miệng nhưng crop chỉ rộng khoảng 84–95 px; chưa biết đủ chi tiết để phân loại câu hay không. Số đo webcam trực tiếp 640 × 480, 27,1 FPS là phép thử khác; không suy hiệu năng live từ thời gian xử lý file. Chưa kiểm tra 20 clip, không có kết quả phân loại 10 câu.

Người nhận và việc có thể làm tiếp: TV4 xem schema timestamp/invalid và chốt hợp đồng chung; TV3 xác nhận clip mới có đúng một câu, kiểm tra chất lượng crop trên cả đoạn và bổ sung phép kiểm nhiều người trước tích hợp; TV5 phối hợp thử webcam tích hợp. Script này chưa ở trạng thái READY FOR REVIEW cho tích hợp.

Vướng mắc, cách tái hiện, điều đã thử: clip đầu thay đổi khoảng cách/hướng mặt nên tỷ lệ frame phát hiện thấp. Clip mới ổn định hơn nhưng với `num_faces=2` model bỏ lỡ nhiều frame dù ảnh vẫn thấy mặt; `num_faces=1` giải quyết trường hợp một người trên clip này. [Tài liệu MediaPipe](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker?hl=en) ghi chế độ làm mượt chỉ áp dụng khi `num_faces=1`. Chưa hiệu chỉnh ngưỡng trên dev; chưa kiểm tra ca nhiều người.
