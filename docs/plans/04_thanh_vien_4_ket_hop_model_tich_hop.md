# Thành viên 4 — Kết hợp nghe–nhìn và tích hợp hệ thống

Người phụ trách: ................................  
Thời gian: 4 tuần, khoảng 12 giờ/tuần: 2 giờ học, 7 giờ làm, 2 giờ kiểm tra/báo cáo và 1 giờ họp. Vai trò này phù hợp người mạnh Python/ML nhất.

## 1. Trách nhiệm của bạn

Bạn đảm bảo các module chạy cùng nhau và xây bộ kết hợp A/V. TV2 sở hữu âm thanh, TV3 sở hữu thị giác; bạn không viết lại model của họ. TV5 sở hữu ứng dụng; bạn bàn giao API suy luận, TV1 sở hữu dữ liệu/test và chấm điểm.

Phạm vi 4 tuần:

- ASR tiếng Việt tự do từ audio là một chế độ độc lập.
- Thí nghiệm A/V/AV phân loại một trong 10 câu định trước; có cơ chế từ chối, nhưng chưa bảo đảm phát hiện mọi câu lạ.
- Thu từng đoạn bằng Bắt đầu/Dừng trước. Chưa gọi là streaming nếu chưa làm và đo thực sự.
- Laptop chạy model; kính là đầu ra mở rộng nếu có phần cứng tương thích.

Nghiên cứu không mặc định AV tốt hơn A. Nhiệm vụ của bạn là làm phép kết hợp có cơ sở và cho phép kiểm chứng, kể cả khi kết quả không cải thiện.

## 2. Hợp đồng kỹ thuật cần chốt ngày 2

### Đơn vị dữ liệu

- Một `sample_id` là một đoạn lời nói, gồm audio/video có cùng gốc thời gian.
- Dữ liệu huấn luyện mục tiêu: 400 đoạn từ 10 người, chia 6/2/2 người; 40 đoạn câu ngoài danh sách cho dev/test. TV1 giữ test.
- Âm thanh sau chuẩn hóa: mono float32, 16 kHz, kiểm tra hữu hạn và mức biên độ.
- Video: chuỗi frame/landmarks kèm timestamp mili giây tính từ đầu bản thu; không lấy chỉ số frame làm thời gian khi có rớt frame.
- `start_ms`, `end_ms` chỉ thời gian trong bản thu. `infer_ms` là thời gian xử lý, không được nhầm với timestamp.
- Mốc thời gian hiệu năng dùng một đồng hồ monotonic trên cùng máy. Không trừ timestamp của hai đồng hồ khác nhau nếu chưa đồng bộ.

### Đầu ra nhánh A và V

Các trường thống nhất: `sample_id`, `class_order`, `scores`, `valid`, `reason`, `infer_ms`, `model_version`.

- `class_order` chính xác c00–c09, theo danh sách TV1.
- `scores` là 10 điểm không âm, tổng xấp xỉ 1; xác định rõ lấy từ hàm nào. Đây chưa mặc nhiên là xác suất đã hiệu chỉnh.
- Khi invalid: `scores` có thể để null; không thay bằng vector ngẫu nhiên rồi tiếp tục như thật.
- Trước kết hợp phải kiểm tra shape, NaN, class_order, sample_id và khoảng thời gian.

### Đầu ra cho ứng dụng

`sample_id`, `mode`, `text`, `status`, `reason`, `model_version`, `infer_ms`.

- `mode`: `asr_free`, `audio_10`, `visual_10`, `av_10`.
- `status`: `ok`, `uncertain`, `invalid`, `error`.
- Chỉ ánh xạ class_id sang câu mẫu sau khi dự đoán. Không đưa đáp án thật vào runtime.
- UI không được hiển thị điểm số thành “độ chính xác 95%” nếu chưa có căn cứ hiệu chỉnh.

## 3. Cách kết hợp được chọn

Baseline **late fusion**: hai nhánh nhận cùng đoạn, mỗi nhánh đưa 10 điểm rồi kết hợp theo cùng lớp.

`score_AV = alpha * score_A + (1 - alpha) * score_V`

Tuần 2 bắt đầu `alpha = 0.5`. Tuần 3 thử một lưới nhỏ `{0, 0.25, 0.5, 0.75, 1}` trên dev với đủ 3 điều kiện sạch/+10 dB/0 dB; chọn theo macro-F1 trung bình các điều kiện đã quy định, hòa thì ưu tiên phương án đơn giản. Hai đầu 0 và 1 là đối chứng chỉ nhìn/chỉ nghe, không được trình bày như AV đang dùng cả hai nguồn.

Nếu quy mô dữ liệu quá nhỏ để hiệu chỉnh điểm đáng tin cậy, ghi rõ dùng điểm chưa hiệu chỉnh và đánh giá thực nghiệm. Không so trực tiếp score từ hai thang đo khác nhau. Không lấy chuỗi ASR và một câu từ V rồi nhờ LLM chọn câu “nghe hợp lý”.

Quy tắc đầu vào lỗi: V invalid thì dùng A nếu A valid; A invalid thì chỉ dùng V với trạng thái nêu rõ nguồn; cả hai invalid thì báo chưa nhận dạng. Ngưỡng max-score hoặc khoảng cách top-1/top-2 để từ chối được chọn trên dev, thử số lựa chọn nhỏ và ghi lại. Ngưỡng thấp/cao không tự bảo đảm câu đúng/sai.

## 4. Tuần 1 — API, dữ liệu mẫu và đồng bộ

### Các bước thực hiện

- [ ] Ngày 1–2: tạo schema ở phần 2, skeleton các hàm và 3 ví dụ: đầu vào hợp lệ, mất video, mất audio. Gửi TV2/TV3/TV5 xác nhận trước khi code sâu.
- [ ] Lập cấu trúc module đơn giản: capture, audio, vision, fusion, app, evaluation; một file cấu hình chung. Không cần microservices/cloud.
- [ ] Nhận một clip pilot từ TV1; tách/đọc hai nguồn sao cho giữ cùng gốc thời gian; in log độ dài và khoảng thời gian thực.
- [ ] Cùng TV5 kiểm tra offset audio/video bằng sự kiện thấy-nghe được như vỗ tay trong clip kiểm tra riêng. Ghi sai số ước lượng; không đưa tiếng vỗ tay vào feature câu.
- [ ] Cùng TV2/TV3 chạy audio và landmarks thật trước ngày 7. Dữ liệu mock chỉ để thử giao diện, phải có nhãn mock rõ ràng.
- [ ] Hỗ trợ tuyển/quay 2 người theo TV1; giúp nhóm pin môi trường sau khi cài chạy thành công.

### Học thêm — khoảng 2 giờ

- 45 phút: [AV-HuBERT paper](https://arxiv.org/abs/2201.02184), đọc abstract và kiến trúc để hiểu audio/video representation; phân biệt nghiên cứu đó với late fusion đơn giản của nhóm.
- 35 phút: [ViCocktail paper](https://arxiv.org/abs/2506.04635), tìm phần AV synchronization và speaker; viết ghi chú vì sao ghép lệch người/lệch đoạn sẽ sai.
- 40 phút: [Python queue](https://docs.python.org/3/library/queue.html), học queue giữa luồng thu, xử lý và UI; tạo ví dụ gửi/nhận một kết quả giả có gắn nhãn.

### Nộp báo cáo và nghiệm thu

- Nộp schema, skeleton pipeline, config mẫu, log pilot đồng bộ, ghi chú cài đặt.
- Báo cáo: module nào đã dùng dữ liệu thật, module nào mock; offset đo được; vấn đề đang chặn từng người.
- **Đạt:** TV2/TV3/TV5 đồng ý API; cùng sample_id đi xuyên pipeline; mock không thể bị hiểu nhầm là kết quả nghiên cứu.

## 5. Tuần 2 — Ghép hai model và hoàn thành lượt chạy đầu

### Các bước thực hiện

- [ ] Tích hợp ASR của TV2 làm chế độ riêng; nhận model A/V trước ngày 14.
- [ ] Viết adapter và kiểm tra class_order, shape, score, sample_id. Bất đồng schema phải sửa tại adapter, không âm thầm tráo nhãn.
- [ ] Triển khai alpha 0.5, lưu điểm từng nhánh và điểm AV để TV1 kiểm toán.
- [ ] Làm fallback khi thiếu nguồn và trả status/reason cho TV5.
- [ ] Kiểm tra tối thiểu: hai vector giống nhau; hai vector mâu thuẫn; V invalid; A invalid; cả hai invalid; class_order đảo; score NaN; đoạn lệch sample_id.
- [ ] Chạy một lượt thật thu → A/V → fusion → UI; đo từng phần thời gian, bàn giao log cho TV1.

### Học thêm — khoảng 2 giờ

- 45 phút: [scikit-learn: probability calibration](https://scikit-learn.org/stable/modules/calibration.html), hiểu vì sao `predict_proba` không luôn bằng tần suất đúng thực tế.
- 35 phút: [scikit-learn metrics](https://scikit-learn.org/stable/api/sklearn.metrics.html), học macro-F1 và so sánh trên cùng mẫu.
- 40 phút: đọc code adapter của TV2/TV3; tự tính một ví dụ fusion 3 lớp bằng tay rồi kiểm tra kết quả máy.

### Nộp báo cáo và nghiệm thu

- Nộp module fusion, adapter, các ca kiểm tra, log dev và bản pipeline cho TV5.
- Báo cáo: một ví dụ A đúng/V sai, A sai/V đúng nếu có trong dữ liệu; độ trễ từng module; các fallback.
- **Đạt:** 8 ca kiểm tra có kết quả mong đợi; UI lấy đầu ra thật; không ghép hai đoạn khác thời gian/người.

## 6. Tuần 3 — Chọn trọng số, ngưỡng và khóa pipeline

### Các bước thực hiện

- [ ] Chạy lưới alpha nhỏ trên dev sạch/+10 dB/0 dB do TV2/TV1 chuẩn bị; ghi mọi cấu hình đã thử.
- [ ] Thử ngưỡng từ chối trên dev và 20 câu ngoài danh sách dev. Báo đồng thời coverage, accuracy phần chấp nhận và false acceptance câu lạ; không chỉ báo accuracy sau khi loại gần hết mẫu khó.
- [ ] So sánh A, V, AV ở trạng thái không từ chối trên cùng các clip; đánh giá cơ chế từ chối là phần riêng.
- [ ] Làm kiểm tra thiếu camera, lệch đoạn, hàng đợi đầy; phối hợp TV5 giới hạn một job đang chạy và hủy kết quả cũ.
- [ ] Nếu AV không cải thiện, kiểm tra thang điểm/đồng bộ/V trước; không tìm vô hạn tham số để thắng dev.
- [ ] Ngày 21 đóng băng commit, model, alpha, threshold, features và config; bàn giao TV1.

### Học thêm — khoảng 2 giờ

- 45 phút: đọc lại [calibration](https://scikit-learn.org/stable/modules/calibration.html), giải thích reliability và hạn chế dev ít người; không triển khai calibration phức tạp nếu chưa có đủ dữ liệu tách biệt.
- 45 phút: [scikit-learn: common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html), tập trung chọn tham số trên dev, không test.
- 30 phút: đọc log timing/queue của chính nhóm; chỉ ra đâu là thu, chờ và suy luận. Thực hành một ca kết quả đến muộn sau khi bấm Dừng.

### Nộp báo cáo và nghiệm thu

- Nộp bảng cấu hình dev, quyết định alpha/ngưỡng, pipeline khóa, các ca lỗi, phần phương pháp fusion 1–2 trang.
- Báo cáo: mức cải thiện hoặc suy giảm, số mẫu bị từ chối, ngưỡng chọn vì lý do gì, giới hạn điểm chưa hiệu chỉnh.
- **Đạt:** TV1 chạy lại bằng một cấu hình; không còn tuning dựa test; TV5 nhận status/reason rõ ràng.

## 7. Tuần 4 — Kiểm thử toàn hệ thống và hỗ trợ bảo vệ

### Các bước thực hiện

- [ ] Hỗ trợ TV1 chạy test cuối trên model khóa; thống nhất log, không sửa âm thầm giữa các điều kiện.
- [ ] Chạy app liên tục 10 phút với TV5; ghi số lượt, lỗi, job bỏ, thời gian chờ và tiêu thụ bộ nhớ nếu đo được.
- [ ] Kiểm tra bằng người mới trong tập test chỉ ở giai đoạn đánh giá; demo trước đó dùng train/dev.
- [ ] Hoàn thiện hướng dẫn cài từ môi trường sạch, thứ tự chạy và chế độ offline/online thực tế; người TV1 hoặc TV5 thử lại.
- [ ] Viết sơ đồ cuối, đóng góp và hạn chế; diễn tập giải thích fusion trong 3 phút.

### Học thêm — khoảng 2 giờ

- 60 phút: so sánh sơ đồ nhóm với [AV-HuBERT](https://arxiv.org/abs/2201.02184), chuẩn bị trả lời “nhóm tự xây phần nào, dùng lại phần nào?”.
- 60 phút: rà log và ca kiểm tra của chính nhóm; thực hành giải thích một trường hợp AV tệ hơn A mà không đổ lỗi chung chung cho AI.

### Nộp báo cáo và nghiệm thu

- Nộp release mã nguồn, config, model metadata, sơ đồ hệ thống, log tích hợp và hướng dẫn tái lập.
- **Đạt:** hệ thống có một lệnh/quy trình khởi chạy rõ; kết quả truy về model/config; không trộn kết quả chế độ 10 câu với ASR tự do.

## 8. Khi chậm tiến độ

- Chưa có A/V: dùng adapter mock để TV5 tiếp tục UI, ghi rõ mock; không đưa mock vào số liệu.
- Đồng bộ live khó: dùng file nghe–nhìn ghi sẵn đồng bộ để làm thí nghiệm; giữ ASR microphone live riêng. Ghi đúng loại demo.
- Không có lợi ích từ fusion: báo kết quả âm tính và phân tích, không nâng phạm vi sang model lớn ở tuần 4.
- Bỏ trước: cloud, app di động, streaming phức tạp, speaker diarization, attention fusion và fine-tuning AVSR tổng quát.

## 9. Mẫu báo cáo tuần

Mục tiêu → commit/schema → nguồn thật/mock → kiến thức đã học → cấu hình và phép thử → số đo/sample_id → lỗi và cách tái hiện → bàn giao cho TV1/TV5 → việc tuần sau. Kèm video 1–3 phút, tuyệt đối không dùng số mô phỏng làm kết quả thực nghiệm.
