# TV4 — Hợp đồng tuần 1, bản nháp 0.1

Trạng thái IMPLEMENTED, chờ TV2/TV3/TV5 xác nhận. Người phụ trách TV4 chưa xác định tên.

Nguồn thứ tự lớp và cấu hình là config.json. TV1 cần cung cấp ánh xạ c00–c09 sang câu thật trước khi hiển thị câu dự đoán.

Mỗi nhánh trả sample_id, class_order, scores, valid, reason, infer_ms, model_version. Bản nháp bổ sung start_ms/end_ms để kiểm tra cùng khoảng ghi hình, đơn vị mili giây từ đầu bản thu. Khoảng hợp lệ có 0 <= start_ms < end_ms. Hai nhánh phải có cùng khoảng và sample_id. Cần producer/consumer xác nhận phần bổ sung trước tích hợp.

Scores gồm 10 số hữu hạn, không âm, tổng lệch 1 tối đa 1e-6. valid phải là boolean. Nhánh valid có reason=null. Bản nháp chuẩn hóa nhánh invalid thành scores=null và reason có nội dung. infer_ms là thời lượng xử lý không âm, đo bằng đồng hồ monotonic. Điểm chưa hiệu chỉnh.

Đầu ra UI gồm sample_id, mode, text, status, reason, model_version, infer_ms. Mode hợp lệ theo kế hoạch là asr_free/audio_10/visual_10/av_10. Status là ok/uncertain/invalid/error. Entry point tuần 1 là mock, luôn trả mock=true, text rỗng, uncertain hoặc invalid. UI phát triển phải hiển thị nhãn MOCK từ trường này.

Trong pilot thật, `asr.json` giữ đủ bảy trường đầu ra kể cả khi thiếu tiếng hoặc xử lý lỗi. Bản nháp để `model_version=null` và `infer_ms=null` khi nhánh không có kết quả suy luận. Kiểu nullable này chờ TV5 xác nhận. Một nguồn vắng trả `invalid` và lý do `missing_audio` hoặc `missing_video`. Nếu nguồn có mặt nhưng xử lý thất bại, nhánh đó trả `error` với lý do `audio_processing_failed` hoặc `video_processing_failed`. Pilot vẫn thử nhánh còn lại và ghi trạng thái cả hai vào `summary.json`.

Fixture gồm đủ nguồn, thiếu video, thiếu audio và thiếu cả hai. Validator thực thi ở auralens/contracts.py. Ca sai dữ liệu nằm trong tests/test_week01.py.

Audio mục tiêu là mono float32 16 kHz hữu hạn. Pilot landmarks của TV3 có timestamp_ms theo nguồn và valid chỉ phản ánh model tìm được mặt. Adapter thật cần kiểm tra chất lượng khẩu hình và đồng bộ nguồn trước khi tạo kết quả visual_10. Phiên này chưa hiện thực chuẩn hóa audio hoặc chuyển landmarks thành điểm phân loại.

Layout thống nhất dùng auralens/audio, vision, capture, fusion, app, evaluation theo trách nhiệm TV2/TV3/TV5/TV4/TV1. Các module được thêm khi có triển khai thực tế. auralens/pipeline.py điều phối thử hợp đồng và queue một phần tử. Đây là bài thực hành gửi/nhận đồng bộ, worker/UI thật còn cần TV5 phối hợp.
