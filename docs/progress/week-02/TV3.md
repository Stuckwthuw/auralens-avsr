# TV3 — Tuần 02: Học bộ phân loại khẩu hình 10 câu

- Người phụ trách: chưa điền tên.
- Trạng thái: CHƯA BÁO CÁO.
- Thời gian bắt đầu/kết thúc tuần: chưa xác định ngày bắt đầu dự án.
- Cập nhật lần cuối: chưa có báo cáo thực hiện.
- Kế hoạch gốc: [phân công TV3](../../plans/03_thanh_vien_3_thi_giac_khau_hinh.md).

> Đây là mẫu theo kế hoạch, chưa xác nhận bất kỳ nhiệm vụ chuyên môn nào đã hoàn thành. Chỉ đánh dấu khi có bằng chứng; tách công việc đang làm với kết quả đã được kiểm tra và tích hợp.

## 1. Nhiệm vụ được giao trong tuần

- [ ] Nhận dữ liệu train/dev từ TV1 trước hoặc trong ngày 10; chỉ dùng train để fit các bước học tham số.
- [ ] Xây đặc trưng chuỗi như phần 3; lưu tên đặc trưng, shape, thứ tự điểm và cách xử lý frame bị thiếu.
- [ ] Chuẩn hóa vị trí/kích thước để model ít học nhầm mặt lớn/nhỏ hoặc vị trí người ngồi; không đưa background vào feature.
- [ ] Chia 8 vùng thời gian và train Logistic Regression; cố định seed, chỉ thử 2–3 cấu hình nhỏ.
- [ ] Trả vector 10 điểm theo class_order c00–c09; dùng `classes_` để kiểm tra thứ tự.
- [ ] Kiểm tra clip ngắn, trống, không đủ frame; gửi kết quả invalid và lý do thay vì tạo điểm giả.
- [ ] Trước ngày 14 bàn giao hàm infer cho TV4 và dự đoán dev cho TV1.

## 2. Công việc thực tế và trạng thái

Chưa có báo cáo. Khi làm, ghi từng task: ID/tên, trạng thái, đầu ra, commit/PR và người nhận. Task hoàn tất trong tuần nào phải dẫn đúng bằng chứng của tuần đó; không sao chép trạng thái sang các tuần sau.

## 3. Kiến thức đã học và áp dụng

Chưa báo cáo. Ghi tài liệu đã đọc, nội dung hiểu được, bài thực hành và nơi áp dụng; tham khảo mục học của tuần trong kế hoạch gốc.

## 4. Kiểm tra và số liệu

Chưa đo/chưa chạy kiểm tra. Khi có, ghi lệnh thực tế, môi trường, dữ liệu/số mẫu, model/config, kết quả và phần chưa kiểm tra. Phân biệt dữ liệu thật, mock và video ghi trước; không đưa bản thu cá nhân hoặc bí mật vào Git.

## 5. Vướng mắc và hỗ trợ cần thiết

Chưa báo cáo; không suy ra là không có vướng mắc. Ghi lỗi, cách tái hiện, điều đã thử, người có thể hỗ trợ và phần độc lập vẫn tiếp tục được.

## 6. Bàn giao, review và tích hợp

Chưa bàn giao. Ghi người nhận, cách chạy, hợp đồng liên quan, liên kết PR và kết quả xác nhận. Phân biệt READY FOR REVIEW với REVIEWED và INTEGRATED; không tự xác nhận thay reviewer.

## 7. Việc tiếp theo và thời gian thực tế

Chưa báo cáo. Ghi phần còn thiếu, mục tiêu phiên sau, thời gian đã dùng và điều chỉnh được thống nhất nếu có. Báo cáo cuối tuần có thể vẫn còn task dở; phải ghi rõ thay vì đánh dấu toàn bộ đã hoàn thành.
