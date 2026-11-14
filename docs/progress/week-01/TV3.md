# TV3 — Hoàng Hiếu — Tuần 01: Đọc camera và trích vùng miệng

- Người phụ trách: Hoàng Hiếu — Thị giác máy tính và khẩu hình.
- Trạng thái: IN PROGRESS.
- Thời gian bắt đầu/kết thúc tuần: chưa xác định ngày bắt đầu dự án.
- Cập nhật lần cuối: 2026-11-14, số đo webcam do Hoàng Hiếu cung cấp.
- Kế hoạch gốc: [phân công TV3](../../plans/03_thanh_vien_3_thi_giac_khau_hinh.md).

> Mới có số đo webcam do người phụ trách báo cáo; các nhiệm vụ còn lại chưa được xác nhận hoàn thành. Chỉ đánh dấu khi có bằng chứng; tách công việc đang làm với kết quả đã được kiểm tra và tích hợp.

## 1. Nhiệm vụ được giao trong tuần

- [ ] Ngày 1: cùng TV5 thử webcam; xác định độ phân giải/fps thực đo, ánh sáng và khoảng cách để miệng đủ rõ. Có thể bắt đầu bằng 720p, mục tiêu khoảng 25–30 fps nếu máy đáp ứng; đây là cấu hình đề xuất, không phải yêu cầu cố định.
- [ ] Ngày 2–3: chạy Face Landmarker; vẽ điểm miệng trên video pilot và crop vùng miệng có lề.
- [ ] Ngày 4: cung cấp cho TV4 một sample gồm chuỗi landmarks/crop, timestamp và cờ valid.
- [ ] Ghi hành vi khi không có mặt, nhiều mặt, quay nghiêng hoặc miệng bị che. Trước mắt chỉ xử lý một người, không tự chọn ngẫu nhiên giữa nhiều người.
- [ ] Viết hướng dẫn quay 1 trang cho TV1: mặt hướng camera, ánh sáng đủ, tránh rung, không đọc hết câu trước khi bắt đầu thu.
- [ ] Kiểm tra 20 clip pilot; hỗ trợ tuyển 2 người và thu theo lịch chung.

## 2. Công việc thực tế và trạng thái

Task: thử webcam tích hợp trên máy tính (ngày 1). Trạng thái: IN PROGRESS. Hoàng Hiếu báo cáo độ phân giải thực 640 × 480 và FPS thực đo 27,1. Chưa ghi nhận điều kiện ánh sáng, khoảng cách và độ rõ vùng miệng nên chưa đánh dấu hoàn thành checklist ngày 1.

## 3. Kiến thức đã học và áp dụng

Chưa báo cáo. Ghi tài liệu đã đọc, nội dung hiểu được, bài thực hành và nơi áp dụng; tham khảo mục học của tuần trong kế hoạch gốc.

## 4. Kiểm tra và số liệu

- Webcam trên máy tính của Hoàng Hiếu: 640 × 480; FPS thực đo: 27,1 (số liệu người phụ trách cung cấp trong phiên trao đổi ngày 2026-11-14).
- Chưa lưu lệnh, log đo, thời lượng đo và cấu hình camera để người khác chạy lại; chưa đo tỷ lệ frame hợp lệ hoặc kiểm tra landmarks.

## 5. Vướng mắc và hỗ trợ cần thiết

Chưa báo cáo; không suy ra là không có vướng mắc. Ghi lỗi, cách tái hiện, điều đã thử, người có thể hỗ trợ và phần độc lập vẫn tiếp tục được.

## 6. Bàn giao, review và tích hợp

Chưa bàn giao. Ghi người nhận, cách chạy, hợp đồng liên quan, liên kết PR và kết quả xác nhận. Phân biệt READY FOR REVIEW với REVIEWED và INTEGRATED; không tự xác nhận thay reviewer.

## 7. Việc tiếp theo và thời gian thực tế

Ghi điều kiện ánh sáng, khoảng cách và đánh giá độ rõ vùng miệng ở 640 × 480; lưu lệnh/log đo để tái lập. Sau đó thử clip pilot và trích landmarks/crop theo kế hoạch. Thời gian đã dùng: chưa báo cáo.
