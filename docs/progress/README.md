# Báo cáo tiến độ Auralens

Tiến độ chính thức được lưu trên `main` sau review. Không dùng branch dài hạn riêng cho báo cáo. Mỗi người có một file mỗi tuần để làm song song, hạn chế conflict.

## Bắt đầu từ đâu?

- Tuần 1: [TV1](week-01/TV1.md), [TV2](week-01/TV2.md), [TV3](week-01/TV3.md), [TV4](week-01/TV4.md), [TV5](week-01/TV5.md).
- Tuần 2: [TV1](week-02/TV1.md), [TV2](week-02/TV2.md), [TV3](week-02/TV3.md), [TV4](week-02/TV4.md), [TV5](week-02/TV5.md).
- Tuần 3: [TV1](week-03/TV1.md), [TV2](week-03/TV2.md), [TV3](week-03/TV3.md), [TV4](week-03/TV4.md), [TV5](week-03/TV5.md).
- Tuần 4: [TV1](week-04/TV1.md), [TV2](week-04/TV2.md), [TV3](week-04/TV3.md), [TV4](week-04/TV4.md), [TV5](week-04/TV5.md).

Tất cả 20 file được khởi tạo là **CHƯA BÁO CÁO**. Danh sách nhiệm vụ lấy từ kế hoạch gốc, không phải kết quả thực hiện. Nhóm điền ngày bắt đầu rồi tính tuần theo lịch dự án; không suy tuần từ thời điểm agent được mở.

## Luồng cập nhật

1. Cập nhật repo sạch, đọc AGENTS và kế hoạch đúng vai trò/tuần.
2. Tạo nhánh task, ví dụ `feat/tv1-dataset-validation`; làm việc và chạy kiểm tra.
3. Trước bàn giao, cập nhật đúng file tuần trong cùng nhánh: kết quả, bằng chứng, kiểm tra, vướng mắc, bước tiếp theo.
4. Tạo PR gồm công việc và báo cáo, nhờ người liên quan review. Chỉ sửa báo cáo thì dùng nhánh ngắn hạn `docs/tv1-week01-progress`.
5. Sau review/merge, mọi người cập nhật main để nhận trạng thái chung. Xác nhận tích hợp trong PR báo cáo tiếp theo nếu bằng chứng chỉ có sau merge; không đánh dấu trước.

Không sửa AGENTS mỗi lần task xong. Các agent chỉ cập nhật khi đang có phiên chạy và có quyền; file này không phải automation.

## Trạng thái task và bằng chứng

- **CHƯA BÁO CÁO:** chưa có dữ liệu thực hiện; không đồng nghĩa chưa làm hoặc đã hoàn tất.
- **PLANNED:** đã xác định phạm vi/người phụ trách, chưa bắt đầu thực hiện.
- **IN PROGRESS:** đang làm, ghi phần đã có và phần còn thiếu.
- **BLOCKED:** có điều kiện chặn cụ thể; ghi điều đã thử và phần vẫn có thể làm tiếp.
- **IMPLEMENTED:** đã tạo đầu ra, còn chưa đủ kiểm tra/nghiệm thu.
- **VERIFIED:** người thực hiện đã kiểm tra đạt tiêu chí đã nêu; ghi lệnh/kết quả và phạm vi kiểm tra.
- **READY FOR REVIEW:** đủ đầu ra, hướng dẫn và bằng chứng để người khác review; chưa tự coi đã được chấp nhận.
- **REVIEWED:** reviewer đã xác nhận bằng comment/PR có liên kết; tác giả không tự xác nhận thay.
- **INTEGRATED:** đã merge và xác minh trong luồng sử dụng liên quan, có commit và bằng chứng. PR merge riêng chưa đủ để khẳng định hệ thống chạy tích hợp.

Đây là các trạng thái mô tả, không bắt buộc mọi task đi qua tất cả; task bị chặn có thể quay lại làm tiếp. Báo cáo có thể đã nộp dù một số task chưa hoàn tất. Không gán một trạng thái “xong” cho cả tuần để che các task còn thiếu.

## Quy tắc nội dung

- Chỉ tick nhiệm vụ có bằng chứng đáp ứng tiêu chí; ghi nguồn thật/mock/ghi trước.
- Mọi kết quả ML ghi dữ liệu/split, số mẫu, model/config, môi trường và commit. Không tuning bằng test hoặc đưa dữ liệu người tham gia vào Git.
- Không có số liệu thì ghi chưa đo, không điền ví dụ như số liệu thật.
- Ghi nguồn học và cách áp dụng; “đã đọc” không tự chứng minh đã hoàn thành công việc.
- Mỗi người sửa báo cáo của mình; nhận xét từ reviewer dẫn bằng liên kết. Khi sửa sai số liệu, giữ ghi chú đính chính và nguồn, không che lịch sử.
- File cá nhân là nguồn tiến độ chính. Chỉ tạo tổng hợp khi cần báo cáo nhóm; ghi rõ thời điểm tổng hợp, tránh duy trì hai bộ trạng thái cạnh tranh.

## Mẫu ghi một task

```text
Task: [ID và tên công việc thật]
Trạng thái: [chọn theo bằng chứng hiện có]
Đầu ra: [file/module và mô tả]
Bằng chứng: [commit/PR/log được phép chia sẻ]
Kiểm tra: [lệnh, cấu hình, kết quả; hoặc chưa chạy]
Hạn chế/vướng mắc: [thực tế]
Bàn giao: [người nhận và việc họ có thể tiếp tục]
Tiếp theo: [bước cụ thể]
```

Mẫu trên chỉ hướng dẫn cách điền, không xác nhận task nào đã hoàn thành.
