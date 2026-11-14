# TV3 — Hoàng Hiếu — Tuần 01: Đọc camera và trích vùng miệng

- Người phụ trách: Hoàng Hiếu — Thị giác máy tính và khẩu hình.
- Trạng thái: IN PROGRESS.
- Thời gian bắt đầu/kết thúc tuần: chưa xác định ngày bắt đầu dự án.
- Cập nhật lần cuối: 2026-11-14, chạy pilot Face Landmarker trên một clip cục bộ.
- Kế hoạch gốc: [phân công TV3](../../plans/03_thanh_vien_3_thi_giac_khau_hinh.md).

> Đã có số đo webcam, quan sát trực tiếp và kết quả pilot trên một clip. Các nhiệm vụ còn lại chưa được xác nhận hoàn thành. Chỉ đánh dấu khi có bằng chứng; tách công việc đang làm với kết quả đã được kiểm tra và tích hợp.

## 1. Nhiệm vụ được giao trong tuần

- [ ] Ngày 1: cùng TV5 thử webcam; xác định độ phân giải/fps thực đo, ánh sáng và khoảng cách để miệng đủ rõ. Có thể bắt đầu bằng 720p, mục tiêu khoảng 25–30 fps nếu máy đáp ứng; đây là cấu hình đề xuất, không phải yêu cầu cố định.
- [ ] Ngày 2–3: chạy Face Landmarker; vẽ điểm miệng trên video pilot và crop vùng miệng có lề.
- [ ] Ngày 4: cung cấp cho TV4 một sample gồm chuỗi landmarks/crop, timestamp và cờ valid.
- [ ] Ghi hành vi khi không có mặt, nhiều mặt, quay nghiêng hoặc miệng bị che. Trước mắt chỉ xử lý một người, không tự chọn ngẫu nhiên giữa nhiều người.
- [ ] Viết hướng dẫn quay 1 trang cho TV1: mặt hướng camera, ánh sáng đủ, tránh rung, không đọc hết câu trước khi bắt đầu thu.
- [ ] Kiểm tra 20 clip pilot; hỗ trợ tuyển 2 người và thu theo lịch chung.

## 2. Công việc thực tế và trạng thái

Task: thử webcam tích hợp trên máy tính (ngày 1). Trạng thái: IN PROGRESS. Hoàng Hiếu báo cáo độ phân giải thực 640 × 480, FPS thực đo 27,1 và quan sát vùng miệng dưới đèn phòng ở ba khoảng cách bên dưới. Chưa xác nhận thử cùng TV5 nên chưa đánh dấu hoàn thành checklist ngày 1.

Task: trích điểm môi từ video pilot (ngày 2–3). Trạng thái: VERIFIED cho một clip cục bộ, chưa bàn giao tích hợp. Script `auralens/vision/pilot_landmarks.py` đọc timestamp gốc, trả cờ/lý do theo frame và tạo ảnh crop có điểm môi. Chưa tạo video phủ điểm hoặc mẫu theo hợp đồng TV4, nên checklist ngày 2–3 vẫn để mở. Xem [bàn giao pilot](../../handoffs/tv3-face-landmarker-pilot.md).

## 3. Kiến thức đã học và áp dụng

Chưa báo cáo. Ghi tài liệu đã đọc, nội dung hiểu được, bài thực hành và nơi áp dụng; tham khảo mục học của tuần trong kế hoạch gốc.

## 4. Kiểm tra và số liệu

- Webcam trên máy tính của Hoàng Hiếu: 640 × 480; FPS thực đo: 27,1 (số liệu người phụ trách cung cấp trong phiên trao đổi ngày 2026-11-14).
- Quan sát dưới đèn phòng do Hoàng Hiếu báo cáo: 20–50 cm — miệng rõ, không bị che; 70 cm — thấy miệng nhưng khẩu hình chưa rõ; 100 cm — thấy miệng nhưng không thấy được khẩu hình khi nói. Đây là nhận xét trực quan, chưa phải tỷ lệ frame hợp lệ hoặc kết quả model.
- Pilot video riêng: 1920 × 1080, 13,008 giây, 376 frame; MediaPipe Face Landmarker 1.2.3 + OpenCV 5.0.0 trên Python 3.14.6. Đúng một mặt và trích được điểm môi ở 160/376 frame (42,6%); 216 frame trả `no_face`; không có frame `multiple_faces`. `valid` ở đây chỉ có nghĩa phát hiện đúng một mặt, chưa chứng minh khẩu hình đủ rõ để phân loại câu.
- Timestamp đọc từ video theo mili giây: frame đầu 0 ms, frame cuối 12.960 ms; 10 timestamp đầu khớp `ffprobe`. Hai ảnh crop ở khoảng 1 và 5 giây được xem trực quan, điểm môi bám vùng miệng. Từ khoảng giây 6, nhánh phát hiện không còn trả mặt khi người trong clip lùi xa và đổi hướng. Ảnh và landmarks chỉ lưu cục bộ ngoài Git.
- Script đã chạy trên clip thật; kiểm tra từ chối `--output` trong repo và `compileall` đạt. Chưa lưu log của phép đo webcam 640 × 480 trước đó; chưa đo tỷ lệ frame hợp lệ trên 20 clip pilot hoặc đánh giá khả năng phân loại câu.

## 5. Vướng mắc và hỗ trợ cần thiết

Chưa báo cáo; không suy ra là không có vướng mắc. Ghi lỗi, cách tái hiện, điều đã thử, người có thể hỗ trợ và phần độc lập vẫn tiếp tục được.

## 6. Bàn giao, review và tích hợp

Đã ghi [bàn giao pilot](../../handoffs/tv3-face-landmarker-pilot.md) để TV4 xem cách đọc timestamp và trạng thái invalid. JSON pilot chưa phải hợp đồng chung; chưa có mẫu một câu ổn định để TV4 chạy tích hợp. Chưa có review độc lập hoặc xác nhận tích hợp.

## 7. Việc tiếp theo và thời gian thực tế

Xác nhận bài thử webcam với TV5 và lưu log đo 640 × 480 để tái lập. Quay clip mới gồm đúng một câu, giữ mặt hướng camera ở 20–50 cm dưới đèn phòng; chạy lại script, kiểm tra crop và ca không thấy mặt. Phối hợp TV4 về schema trước khi bàn giao mẫu tích hợp. Thời gian đã dùng: chưa báo cáo.
