# TV5 — Tuần 02: Nối kết quả thật và làm lượt sử dụng hoàn chỉnh

- Người phụ trách: chưa điền tên.
- Trạng thái: CHƯA BÁO CÁO.
- Thời gian bắt đầu/kết thúc tuần: chưa xác định ngày bắt đầu dự án.
- Cập nhật lần cuối: chưa có báo cáo thực hiện.
- Kế hoạch gốc: [phân công TV5](../../plans/05_thanh_vien_5_ung_dung_hien_thi_phan_cung.md).

> Đây là mẫu theo kế hoạch, chưa xác nhận bất kỳ nhiệm vụ chuyên môn nào đã hoàn thành. Chỉ đánh dấu khi có bằng chứng; tách công việc đang làm với kết quả đã được kiểm tra và tích hợp.

## 1. Nhiệm vụ được giao trong tuần

- [ ] Nhận API của TV4, thay nội dung giả bằng kết quả thực; giữ mock ở chế độ phát triển riêng có nhãn.
- [ ] Tách luồng xử lý khỏi Tkinter: nhận job qua queue, đưa kết quả về main thread bằng cơ chế event/after phù hợp.
- [ ] Cho chạy ASR tự do và thí nghiệm 10 câu như hai chế độ riêng; hiển thị nguồn A/V/AV đúng kết quả trả về.
- [ ] Xử lý trạng thái uncertain/invalid/error bằng thông báo ngắn: “Chưa nhận dạng rõ”, “Không thấy mặt”, “Không có micro”; chi tiết kỹ thuật ghi log, không chiếm vùng phụ đề.
- [ ] Không hiển thị điểm model dưới dạng xác suất đúng. Không tự sửa câu nhận dạng để “nghe tự nhiên” khi hệ thống đang được đo.
- [ ] Nếu có kính tương thích trước ngày 14, thử xuất chữ cố định trước, sau đó mới text động; nếu chưa có, hoàn thiện fullscreen trên laptop và đánh dấu mô phỏng kính.

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
