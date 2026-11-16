# TV3 — Hoàng Hiếu — Tuần 01: Đọc camera và trích vùng miệng

- Người phụ trách: Hoàng Hiếu — Thị giác máy tính và khẩu hình.
- Trạng thái: IN PROGRESS.
- Thời gian bắt đầu/kết thúc tuần: chưa xác định ngày bắt đầu dự án.
- Cập nhật lần cuối: 2026-11-14, chạy pilot Face Landmarker trên ba clip ban đầu, ba ca khó và một cặp che/không che gần camera.
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

Task: trích điểm môi từ video pilot (ngày 2–3). Trạng thái: VERIFIED trên ba clip cục bộ với điều kiện chỉ một người, chưa bàn giao tích hợp. Script `auralens/vision/pilot_landmarks.py` đọc timestamp gốc, trả cờ/lý do theo frame và tạo ảnh crop có điểm môi. Chưa tạo video phủ điểm hoặc mẫu theo hợp đồng TV4, nên checklist ngày 2–3 vẫn để mở. Xem [bàn giao pilot](../../handoffs/tv3-face-landmarker-pilot.md).

Định dạng pilot tạm ghi `source_width_px`, `source_height_px` từ frame thật và từ chối clip đổi kích thước giữa chừng; không ép 640 × 480 hay một FPS cố định. Đã chạy lại clip thứ ba: JSON ghi 1920 × 1080, 68/68 frame có điểm môi, timestamp cuối 2512 ms như lần trước. TV4 chưa xác nhận đây là hợp đồng tích hợp.

## 3. Kiến thức đã học và áp dụng

Chưa báo cáo. Ghi tài liệu đã đọc, nội dung hiểu được, bài thực hành và nơi áp dụng; tham khảo mục học của tuần trong kế hoạch gốc.

## 4. Kiểm tra và số liệu

- Webcam trên máy tính của Hoàng Hiếu: 640 × 480; FPS thực đo: 27,1 (số liệu người phụ trách cung cấp trong phiên trao đổi ngày 2026-11-14).
- Quan sát dưới đèn phòng do Hoàng Hiếu báo cáo: 20–50 cm — miệng rõ, không bị che; 70 cm — thấy miệng nhưng khẩu hình chưa rõ; 100 cm — thấy miệng nhưng không thấy được khẩu hình khi nói. Đây là nhận xét trực quan, chưa phải tỷ lệ frame hợp lệ hoặc kết quả model.
- Pilot đầu: 1920 × 1080, 13,008 giây, 376 frame; MediaPipe Face Landmarker 1.2.3 + OpenCV 5.0.0 trên Python 3.14.6. Cấu hình ban đầu `num_faces=2` cho 160/376 frame có điểm môi (42,6%) và 216 frame `no_face`. Sau khi chuyển sang `num_faces=1`, chạy lại cùng clip được 177/376 frame (47,1%) và 199 frame `no_face`. Giữ cả hai kết quả để thấy ảnh hưởng cấu hình; không coi lần chạy sau là phép test độc lập.
- Pilot mới: 1920 × 1080, 7,471 giây, 212 frame. `num_faces=2` chỉ cho 27/212 frame có điểm môi (12,7%); `num_faces=1` cho 212/212 frame (100%) trên đúng clip đó. Chế độ một người cần người chạy xác nhận trước, không tự kiểm tra nhiều người. `valid` ở đây chỉ có nghĩa model trả điểm môi trong điều kiện đã xác nhận một người, chưa chứng minh khẩu hình đủ rõ để phân loại câu.
- Pilot thứ ba: 1920 × 1080, 2,558 giây, 68 frame; `num_faces=1` cho 68/68 frame có điểm môi (100%), timestamp từ 0 đến 2.512 ms. 10 timestamp đầu khớp `ffprobe` sau làm tròn. Các frame đã xem có một người, mặt gần như giữ vị trí; ở khoảng giây 1,84 thấy miệng mở rõ. Crop có điểm môi tại khoảng giây 1 rộng 123 px, cao 80 px. Chưa xác nhận nội dung câu nói hay nhãn.
- Timestamp đọc từ video theo mili giây: hai clip bắt đầu 0 ms, kết thúc lần lượt 12.960 ms và 7.408 ms; 10 timestamp đầu của mỗi clip khớp `ffprobe` sau làm tròn. Ảnh crop ở khoảng 1 và 5 giây được xem trực quan, điểm môi bám vùng miệng. Vùng crop của clip mới rộng khoảng 84–95 px ở hai mốc này; chất lượng cho phân loại câu chưa được kiểm tra. Ảnh và landmarks chỉ lưu cục bộ ngoài Git.
- Script đã chạy trên ba clip thật; kiểm tra từ chối `--output` trong repo và yêu cầu xác nhận một người; `compileall` đạt. Chưa lưu log của phép đo webcam 640 × 480 trước đó; chưa đo tỷ lệ frame hợp lệ trên 20 clip pilot hoặc đánh giá khả năng phân loại câu.
- Ba ca khó bổ sung ngày 2026-11-14, cùng MediaPipe Face Landmarker `num_faces=1`: quay nghiêng/cúi mặt 0/162 frame có landmarks; khung hình phần lớn trống, người đôi lúc ở sát mép 0/175; che miệng bằng tay khi đứng xa 0/196. Tất cả frame còn lại trả `no_face`; số này là kết quả phát hiện landmarks, không phải kết luận về khả năng đọc khẩu hình. Xem [bàn giao pilot](../../handoffs/tv3-face-landmarker-pilot.md) để biết clip, timestamp và giới hạn. Video/ảnh/JSON chỉ lưu ngoài Git. Ca che miệng chưa kiểm tra được occlusion khi mặt được phát hiện.
- Cặp đối chứng gần camera ngày 2026-11-14: không che miệng 154/154 frame có landmarks; che miệng bằng tay 124/147 frame có landmarks, 23 frame `no_face`. Crop của clip che tại khoảng 1 và 5 giây cho thấy điểm môi nằm trên bàn tay, nên `valid=true` hiện chỉ có nghĩa model trả landmarks, không bảo đảm khẩu hình nhìn thấy hay dùng được. Hai clip quay dưới cùng ánh sáng và vị trí gần tương tự theo ảnh mẫu; chưa đo khoảng cách thực tế, chưa có nhãn câu nói được xác minh và chưa có phép đánh giá phân loại. JSON/ảnh chỉ lưu ngoài Git. Chi tiết ở [bàn giao pilot](../../handoffs/tv3-face-landmarker-pilot.md).

## 5. Vướng mắc và hỗ trợ cần thiết

Chưa báo cáo; không suy ra là không có vướng mắc. Ghi lỗi, cách tái hiện, điều đã thử, người có thể hỗ trợ và phần độc lập vẫn tiếp tục được.

## 6. Bàn giao, review và tích hợp

Đã ghi [bàn giao pilot](../../handoffs/tv3-face-landmarker-pilot.md) để TV4 xem cách đọc timestamp và trạng thái invalid. JSON pilot chưa phải hợp đồng chung; clip thứ ba ngắn và có điểm môi ở mọi frame với cấu hình một người, nhưng chưa được xác nhận nhãn/định dạng để TV4 chạy tích hợp. Chưa có review độc lập hoặc xác nhận tích hợp.

## 7. Việc tiếp theo và thời gian thực tế

Xác nhận bài thử webcam với TV5 và lưu log đo 640 × 480 để tái lập. Xác nhận nội dung và nhãn của clip thứ ba, kiểm tra đủ chi tiết miệng cho bài 10 câu; thử thêm ca không thấy mặt/nhiều mặt trong phạm vi pilot. Phối hợp TV4 về schema trước khi bàn giao mẫu tích hợp. Thời gian đã dùng: chưa báo cáo.

Đã thử cặp che/không che ở vị trí gần tương tự. Bước tiếp theo là xác định tiêu chí chất lượng riêng cho miệng bị che và kiểm tra trên tập dev; chưa được coi landmarks trên bàn tay là đầu vào V hợp lệ. Ca nhiều người vẫn chưa kiểm tra. PR pilot tiếp tục chờ review/tích hợp theo quy trình nhóm.
