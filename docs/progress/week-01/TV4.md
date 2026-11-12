# TV4 — Tuần 01: API, dữ liệu mẫu và đồng bộ

- Người phụ trách: chưa điền tên.
- Trạng thái: CHƯA BÁO CÁO.
- Thời gian bắt đầu/kết thúc tuần: chưa xác định ngày bắt đầu dự án.
- Cập nhật lần cuối: chưa có báo cáo thực hiện.
- Kế hoạch gốc: [phân công TV4](../../plans/04_thanh_vien_4_ket_hop_model_tich_hop.md).

> Đây là mẫu theo kế hoạch, chưa xác nhận bất kỳ nhiệm vụ chuyên môn nào đã hoàn thành. Chỉ đánh dấu khi có bằng chứng; tách công việc đang làm với kết quả đã được kiểm tra và tích hợp.

## 1. Nhiệm vụ được giao trong tuần

- [ ] Ngày 1–2: tạo schema ở phần 2, skeleton các hàm và 3 ví dụ: đầu vào hợp lệ, mất video, mất audio. Gửi TV2/TV3/TV5 xác nhận trước khi code sâu.
- [ ] Lập cấu trúc module đơn giản: capture, audio, vision, fusion, app, evaluation; một file cấu hình chung. Không cần microservices/cloud.
- [ ] Nhận một clip pilot từ TV1; tách/đọc hai nguồn sao cho giữ cùng gốc thời gian; in log độ dài và khoảng thời gian thực.
- [ ] Cùng TV5 kiểm tra offset audio/video bằng sự kiện thấy-nghe được như vỗ tay trong clip kiểm tra riêng. Ghi sai số ước lượng; không đưa tiếng vỗ tay vào feature câu.
- [ ] Cùng TV2/TV3 chạy audio và landmarks thật trước ngày 7. Dữ liệu mock chỉ để thử giao diện, phải có nhãn mock rõ ràng.
- [ ] Hỗ trợ tuyển/quay 2 người theo TV1; giúp nhóm pin môi trường sau khi cài chạy thành công.

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
