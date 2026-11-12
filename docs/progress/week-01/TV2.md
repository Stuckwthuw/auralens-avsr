# TV2 — Tuần 01: Hiểu âm thanh và dựng hai đầu vào

- Người phụ trách: chưa điền tên.
- Trạng thái: CHƯA BÁO CÁO.
- Thời gian bắt đầu/kết thúc tuần: chưa xác định ngày bắt đầu dự án.
- Cập nhật lần cuối: chưa có báo cáo thực hiện.
- Kế hoạch gốc: [phân công TV2](../../plans/02_thanh_vien_2_am_thanh_ASR.md).

> Đây là mẫu theo kế hoạch, chưa xác nhận bất kỳ nhiệm vụ chuyên môn nào đã hoàn thành. Chỉ đánh dấu khi có bằng chứng; tách công việc đang làm với kết quả đã được kiểm tra và tích hợp.

## 1. Nhiệm vụ được giao trong tuần

- [ ] Ngày 1: kiểm tra Python/môi trường, CPU/GPU/RAM và thiết bị thu với TV5; ghi phiên bản đã chạy được, không nâng thư viện tùy ý giữa dự án.
- [ ] Ngày 2: thu một câu, lưu WAV và nghe lại; kiểm tra kênh, tần số lấy mẫu, độ dài, méo do clipping.
- [ ] Ngày 3–4: chạy ASR trên ít nhất 10 đoạn tiếng Việt pilot; chọn chế độ chép lời, không dịch sang tiếng Anh.
- [ ] Viết hàm ASR nhận dữ liệu/đường dẫn trung tính và trả text + thời gian xử lý. Tách tải model khỏi mỗi lần suy luận.
- [ ] Tạo notebook/scrip nhỏ vẽ waveform, spectrogram và MFCC của 2 câu; ghi shape và đơn vị trục.
- [ ] Thống nhất API âm thanh với TV4; hỗ trợ quay pilot và tuyển 2 người.

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
