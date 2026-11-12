# TV2 — Tuần 03: Tạo nhiễu có kiểm soát và ổn định vận hành

- Người phụ trách: chưa điền tên.
- Trạng thái: CHƯA BÁO CÁO.
- Thời gian bắt đầu/kết thúc tuần: chưa xác định ngày bắt đầu dự án.
- Cập nhật lần cuối: chưa có báo cáo thực hiện.
- Kế hoạch gốc: [phân công TV2](../../plans/02_thanh_vien_2_am_thanh_ASR.md).

> Đây là mẫu theo kế hoạch, chưa xác nhận bất kỳ nhiệm vụ chuyên môn nào đã hoàn thành. Chỉ đánh dấu khi có bằng chứng; tách công việc đang làm với kết quả đã được kiểm tra và tích hợp.

## 1. Nhiệm vụ được giao trong tuần

- [ ] Viết script thêm nhiễu tại SNR +10 dB và 0 dB. Với công suất tín hiệu `Ps`, nhiễu `Pn`, hệ số nhiễu là `sqrt(Ps / (Pn * 10^(SNR_dB/10)))`; xác định công suất trên vùng lời nói đã thống nhất, tránh clip im lặng.
- [ ] Kiểm tra SNR đầu ra, xử lý clipping bằng cách co đồng thời tín hiệu/nhiễu nếu cần; ghi hệ số và seed. Không chuẩn hóa hai thành phần độc lập sau khi trộn.
- [ ] Dùng cùng file nhiễu cho so sánh A và AV; nguồn/đoạn nhiễu train, dev, test tách biệt. Nếu thêm augmentation để train, chỉ dùng bản xuất phát từ train.
- [ ] Chạy A và ASR trên dev sạch/nhiễu; gửi đầu ra thô cho TV1, vector A cho TV4.
- [ ] Đo trường hợp im lặng, rút micro, clipping; cùng TV5 tạo thông báo lỗi thay vì giữ câu cũ như kết quả mới.
- [ ] Tối ưu một yếu tố có bằng chứng gây chậm: model ASR nhỏ hơn hoặc giảm xử lý thừa. Khóa ngày 21.

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
