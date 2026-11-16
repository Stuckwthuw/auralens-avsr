# TV3 — Hoàng Hiếu — Hướng dẫn quay pilot khẩu hình

Người phụ trách: Hoàng Hiếu — Hướng dẫn quay pilot tuần 1. Bản ngày 2026-11-16, chờ TV1/TV5 review và thử áp dụng. Dùng cho pilot laptop theo [kế hoạch TV1](../plans/01_thanh_vien_1_truong_nhom_du_lieu_danh_gia.md); chưa thay thế quy trình thu chính thức.

## Trước khi quay

- TV1 xác nhận người tham gia đồng ý, mã người, nơi lưu được phép và danh sách câu. Pilot dự kiến 20 đoạn từ 2 người thuộc train; không dùng người test. Danh sách c00–c09 trong kế hoạch hiện là đề xuất, cần TV1 chốt trước khi thu có nhãn.
- Cố định camera ngang mặt, đủ sáng từ phía trước, thấy trọn mặt và môi. Bắt đầu thử ở 20–50 cm rồi xem lại độ rõ; đây là quan sát trên máy Hiếu, chưa phải khoảng cách chuẩn cho mọi thiết bị.
- Ghi thiết bị, độ phân giải thực, FPS/cách đo, ánh sáng và khoảng cách đo được. Không điền 27,1 FPS cho lần thu mới: số này thuộc phép đo webcam cũ. Video pilot 1920 × 1080 và phép đo webcam 640 × 480 là hai nguồn khác nhau.
- Chỉ mở một ứng dụng thu camera/micro. Thu bản gốc có âm thanh cùng video; TV3 chỉ dùng hình và timestamp để suy luận.

## Mỗi đoạn

1. Gán `sample_id` không chứa đáp án; TV1 giữ nhãn và mã người trong manifest riêng. Xáo trộn thứ tự câu giữa các lượt.
2. Bấm Bắt đầu, chờ khoảng một giây rồi đọc trọn một câu với tốc độ tự nhiên. Giữ mặt hướng camera, không che môi; nói xong chờ khoảng một giây rồi Dừng. Khoảng đệm này là đề xuất thao tác cần thử, không phải ngưỡng thuật toán.
3. Xem lại toàn đoạn: có mất đầu/cuối câu, mờ/rung, môi khuất hay người thứ hai không? Ghi lỗi và giữ bản gốc; nếu thu lại, dùng ID mới và ghi quan hệ với bản cũ.
4. Lưu bản thu, ảnh crop, landmarks và thông tin đồng ý ngoài Git, tại nơi nhóm cho phép. Không đổi tốc độ, cắt hoặc resize âm thầm làm lệch A/V và timestamp.

## Checklist kiểm tra từng clip

- [ ] ID duy nhất; mã người/nhãn/split do TV1 xác nhận; câu thực tế đã được kiểm tra.
- [ ] Đọc được toàn clip; ghi độ phân giải, thời lượng và điều kiện thu thực tế.
- [ ] Xem toàn đoạn, ghi rõ mặt/môi có nhìn thấy và số người; không chỉ xem ảnh ở một mốc.
- [ ] Với clip đã xác nhận chỉ một người, chạy theo [hướng dẫn pilot](../handoffs/tv3-face-landmarker-pilot.md); giữ JSON/crop ngoài Git.
- [ ] Ghi commit, model/config, tổng frame, frame có landmarks, lý do invalid, timestamp và `processing_ms`; đây là thời gian xử lý file, không phải FPS webcam live.
- [ ] Ghi kết luận xem hình riêng với cờ `valid` của script. Model có thể vẽ điểm môi lên bàn tay; `valid=true` chưa chứng minh khẩu hình dùng được.

TV3 tổng hợp số clip đã xem, đạt/chưa đạt tiêu chí thu và lý do từng clip để TV1 quyết định. Không loại âm thầm clip khó. Các lần chạy lại một file chỉ tính một clip; 8 clip khảo sát hiện có chưa mặc nhiên đáp ứng bộ 20 đoạn có nhãn từ 2 người. Ca nghiêng, trống khung hình, che miệng và nhiều người ghi riêng để khảo sát lỗi; chưa có bộ lọc che khuất được xác minh. Không bật `--single-person-confirmed` cho clip nhiều người; script hiện chưa hỗ trợ tự phát hiện ca này.
