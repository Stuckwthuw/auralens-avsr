# TV3 — Hoàng Hiếu — Pilot Face Landmarker

Task / người phụ trách / nhánh / commit: thử trích vùng miệng tuần 1 / Hoàng Hiếu / `feat/tv3-hoang-hieu-mouth-pilot` / `a6ce501` (script; báo cáo và bàn giao trong cùng nhánh).

Đầu ra và file/module thay đổi: `auralens/vision/pilot_landmarks.py`, `auralens/vision/requirements-pilot.txt`, `docs/progress/week-01/TV3.md`. Script đọc video từng frame, giữ timestamp mili giây của nguồn, trả `no_face` hoặc `multiple_faces` khi không có đúng một mặt, và ghi ảnh crop có điểm môi. Ảnh/JSON chứa dữ liệu khuôn mặt chỉ ghi ra thư mục ngoài Git.

Hợp đồng dùng hoặc thay đổi: chưa có hợp đồng TV4. JSON có `pilot_only: true`, `sample_id`, danh sách chỉ số điểm môi và các frame `{timestamp_ms, valid, reason, lip_landmarks}` để khảo sát; không được dùng như đầu ra tích hợp hoặc benchmark. `valid` chỉ là điều kiện phát hiện đúng một mặt, chưa kiểm tra chất lượng khẩu hình.

Cách chạy và kiểm tra đã thực hiện:

1. Windows, Python 3.14.6; tạo venv riêng và cài `pip install -r auralens/vision/requirements-pilot.txt`.
2. Tải model chính thức từ `https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task` vào thư mục ngoài repo. SHA-256 đã dùng: `64184e229b263107bc2b804c6625db1341ff2bb731874b0bcc2fe6544e0bc9ff`.
3. Chạy từ root của nhánh, thay các đường dẫn bằng file cục bộ của người chạy:

   ```powershell
   .\.venv\Scripts\python.exe auralens\vision\pilot_landmarks.py --video '<video-pilot.mp4>' --model '<face_landmarker.task>' --output "$env:TEMP\auralens-tv3-pilot" --sample-id pilot_tv3_001
   ```

4. Đã chạy trên một clip cá nhân cục bộ, kiểm tra `python -m compileall -q auralens/vision/pilot_landmarks.py` và xác nhận script từ chối output nằm trong checkout. `ffprobe` được dùng để đối chiếu 10 timestamp đầu. Không đưa clip, ảnh crop hoặc JSON landmarks vào Git.

Kết quả thật / mock / chưa kiểm tra: clip pilot dài 13,008 giây, 1920 × 1080, 376 frame; 160 frame có đúng một mặt và điểm môi (42,6%); 216 frame trả `no_face`; không có `multiple_faces`. Hai crop ở khoảng 1 và 5 giây được xem trực quan, điểm môi bám đúng miệng. Từ khoảng giây 6, người trong clip lùi xa/đổi hướng và model không còn trả mặt. Số đo webcam trực tiếp 640 × 480, 27,1 FPS là phép thử khác; không suy hiệu năng live từ thời gian xử lý file. Chưa kiểm tra 20 clip, không có kết quả phân loại 10 câu.

Người nhận và việc có thể làm tiếp: TV4 xem schema timestamp/invalid và chốt hợp đồng chung; TV3 quay clip một câu ở khoảng cách ổn định rồi kiểm tra chất lượng crop trên cả đoạn; TV5 phối hợp thử webcam tích hợp. Script này chưa ở trạng thái READY FOR REVIEW cho tích hợp.

Vướng mắc, cách tái hiện, điều đã thử: clip hiện tại thay đổi khoảng cách/hướng mặt nên tỷ lệ frame phát hiện thấp, không phù hợp làm mẫu một câu ổn định. Chạy lại script với clip này để xem `no_face` tăng sau khoảng giây 6. Đã kiểm tra ảnh nguồn tại các mốc đầu, giữa và cuối; chưa hiệu chỉnh ngưỡng Face Landmarker trên dev.
