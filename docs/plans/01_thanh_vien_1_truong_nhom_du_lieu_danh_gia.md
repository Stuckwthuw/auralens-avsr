# Thành viên 1 — Trưởng nhóm, dữ liệu và đánh giá

Người phụ trách: ................................  
Đối tượng: nhóm 5 sinh viên năm 3 ngành Trí tuệ nhân tạo.  
Thời gian: 4 tuần kể từ ngày nhóm bắt đầu; ngày 1–7 là tuần 1.  
Khối lượng dự kiến: 12 giờ/người/tuần, tổng 48 giờ/người. Đây là giả định lập kế hoạch, không phải yêu cầu của cuộc thi.

## 1. Đích chung và phạm vi cần thống nhất trước khi làm

Sau 4 tuần, nhóm cần có chương trình trên laptop, mã nguồn chạy lại được, dữ liệu có nhãn, kết quả thí nghiệm và bản trình diễn. Kính hiển thị thật là mục tiêu mở rộng, phụ thuộc thiết bị có sẵn; mô phỏng trên màn hình phải ghi rõ là mô phỏng.

Hai chế độ khác nhau:

- **Phụ đề tự do:** micro → model ASR tiếng Việt có sẵn → chữ. Chế độ này chỉ dùng âm thanh, chưa được gọi là đọc khẩu hình.
- **Thí nghiệm nghe–nhìn giới hạn:** nhận dạng 1 trong 10 câu đã định trước từ âm thanh, chuyển động miệng hoặc cả hai. Đây là mô hình phân loại câu hữu hạn, không phải model chép lời tiếng Việt bất kỳ. Nhận dạng theo đoạn, ban đầu dùng nút bắt đầu/kết thúc thu.

Lý do thu hẹp: nhóm đang vừa học vừa làm; huấn luyện một hệ thống đọc khẩu hình tiếng Việt tổng quát từ đầu không phải cam kết khả thi trong 4 tuần. Dùng 10 câu giúp kiểm chứng cơ chế kết hợp và có sản phẩm nghiên cứu trung thực. Không cam kết phần kết hợp chắc chắn tốt hơn chỉ nghe; kết quả không cải thiện cũng cần được báo cáo.

Câu hỏi nghiên cứu: “Trong tập 10 câu giao tiếp và với người nói chưa xuất hiện khi huấn luyện, kết hợp khẩu hình có cải thiện nhận dạng so với chỉ nghe ở một số mức nhiễu không?”

## 2. Chia việc toàn nhóm

- **TV1 — bạn trong file này:** điều phối, thiết kế dữ liệu, giữ tập test, tính chỉ số và biên tập báo cáo chung. Chọn người cẩn thận với số liệu; không bắt buộc người code giỏi nhất.
- **TV2:** ASR tự do, thu/xử lý âm thanh, bộ phân loại 10 câu bằng âm thanh.
- **TV3:** camera, vùng miệng, đặc trưng chuyển động, bộ phân loại 10 câu bằng hình ảnh.
- **TV4:** hợp đồng dữ liệu, đồng bộ, kết hợp hai bộ phân loại và nối toàn bộ pipeline. Phù hợp người mạnh Python/ML nhất.
- **TV5:** ứng dụng, phụ đề, xử lý tương tác và khảo sát phần cứng kính. Phù hợp người thích xây sản phẩm.

Mỗi người tự viết phần chuyên môn trong báo cáo. TV1 biên tập, không phải viết thay bốn người còn lại. Mỗi người hỗ trợ tuyển và quay 2 người nói; TV1 quản lý quy trình, không tự thu hết dữ liệu.

Nhịp làm việc: đầu tuần họp 15 phút, giữa tuần 15 phút, cuối tuần demo 30 phút. Phần còn lại khoảng 2 giờ học, 7 giờ thực hiện, 2 giờ kiểm tra và báo cáo. Kẹt quá 90 phút phải gửi lỗi, cách tái hiện và điều đã thử vào nhóm.

## 3. Mốc phụ thuộc trong 28 ngày

1. **Ngày 2:** chốt 10 câu, schema dữ liệu và thiết bị; TV5 có giao diện giả lập, TV4 có mẫu đầu vào/đầu ra.
2. **Ngày 4:** TV2 chạy ASR trên file; TV3 cắt được vùng miệng; TV4 ghép được một đoạn nghe–nhìn.
3. **Ngày 7:** hoàn thành pilot và chia người nói vào các tập; đóng băng phương pháp thu. Nếu phần cứng kính chưa rõ khả năng kết nối thì chọn màn hình laptop làm đầu ra bắt buộc.
4. **Ngày 10:** dữ liệu chính sẵn sàng; TV1 giữ nhãn test, chỉ chia train/dev cho người làm model.
5. **Ngày 14:** có hai bộ phân loại đơn và kết hợp trọng số cố định; ứng dụng chạy qua một lượt thu → dự đoán → hiển thị.
6. **Ngày 21:** khóa model, trọng số, ngưỡng, preprocessing và danh sách thí nghiệm sau khi thử trên dev.
7. **Ngày 22–24:** TV1 chạy test cuối; TV2–TV5 hỗ trợ kỹ thuật, không sửa model theo kết quả test.
8. **Ngày 25–28:** hoàn thiện báo cáo, video và diễn tập. Nếu sửa lỗi triển khai ảnh hưởng kết quả, ghi phiên bản mới, chạy lại toàn bộ phép so sánh và công khai lý do.

## 4. Quy chuẩn dữ liệu dùng chung

### Bộ 10 câu đề xuất

Chốt trước khi thu chính thức, tránh đổi nhãn giữa chừng:

- `c00`: Xin chào bạn.
- `c01`: Bạn tên là gì?
- `c02`: Tôi cần giúp đỡ.
- `c03`: Bạn nói lại được không?
- `c04`: Xin nói chậm hơn.
- `c05`: Cảm ơn bạn rất nhiều.
- `c06`: Tôi chưa hiểu ý bạn.
- `c07`: Chúng ta gặp nhau ở đâu?
- `c08`: Bây giờ là mấy giờ?
- `c09`: Hẹn gặp lại bạn.

Đây là bộ câu khởi đầu, chưa đại diện hội thoại thực tế. Mỗi câu một nhãn; không coi “học 10 câu” là “học tiếng Việt”.

### Quy mô và cách chia

- Mục tiêu: **10 người × 10 câu × 4 lần = 400 đoạn**, mỗi đoạn thường 2–6 giây.
- Chia theo người: **6 train / 2 dev / 2 test**, tương ứng **240 / 80 / 80 đoạn**. Cùng 10 câu xuất hiện ở các tập; mục tiêu là thử người mới, không phải câu mới.
- Thu thêm **10 câu ngoài danh sách/người** cho 4 người thuộc dev/test: **40 đoạn**, gồm 20 dev và 20 test, dùng kiểm tra việc từ chối câu lạ. Không dùng chúng như lớp thứ 11 để huấn luyện trong kế hoạch này.
- Nếu chỉ tuyển được 8 người: **4 train / 2 dev / 2 test**, tức 320 đoạn chính; giữ nguyên 40 đoạn ngoài danh sách. Ghi rõ giảm quy mô.
- Pilot riêng: khoảng 20 đoạn từ 2 người dự kiến thuộc train; không dùng người thuộc test để thử đi thử lại.
- 4 lượt đọc phải là các lần thu thật, không sao chép file. Xáo trộn thứ tự câu, giữ bối cảnh tương đối giống nhau giữa các nhãn, tránh để nền hoặc vị trí quay tiết lộ câu.
- Mỗi người đồng ý cho ghi hình/ghi âm và biết mục đích, người được truy cập, thời điểm xóa. Dùng mã người, giữ thông tin liên hệ riêng. Dữ liệu mặt/giọng vẫn là dữ liệu có thể nhận diện, không gọi là đã ẩn danh hoàn toàn.
- Lưu bản thu gốc có âm thanh đồng bộ; bước tiền xử lý do TV2/TV3 đảm nhiệm. Không dùng nhãn ASR tự động làm “đáp án đúng” mà không kiểm tra.

Manifest tối thiểu: `sample_id`, `speaker_id`, `session_id`, `phrase_id`, `transcript`, `split`, `audio_path`, `video_path`, `duration_ms`, `condition`, `consent_id`. Mọi biến thể nhiễu/crop của một bản thu gốc phải giữ cùng split. Không đưa transcript, phrase_id hoặc tên file chứa nhãn vào model khi suy luận.

### Quy tắc đánh giá

- So sánh chính: **A = bộ phân loại âm thanh 10 câu; V = bộ phân loại hình ảnh 10 câu; AV = kết hợp hai bộ đó**. Cùng clip, cùng nhãn và cùng preprocessing tương ứng.
- Đánh giá 3 điều kiện: bản gốc, nhiễu tổng hợp SNR +10 dB, SNR 0 dB. Chỉ thêm nhiễu vào âm thanh; hình ảnh giữ nguyên. Tài liệu giải thích công thức và kiểm tra SNR do TV2 cung cấp.
- Đây là thí nghiệm nhiễu tổng hợp. Không suy rộng thành đã thử quán cà phê thật nếu chưa thu tại đó.
- Báo cáo accuracy, macro-F1, ma trận nhầm lẫn; ngưỡng từ chối được đánh giá riêng qua tỷ lệ chấp nhận, accuracy trên phần chấp nhận và tỷ lệ câu lạ bị chấp nhận nhầm.
- Với 80 clip test thuộc 10 câu, báo accuracy toàn bộ mẫu; clip invalid/không trả lời tính là không đúng, không tự loại khỏi mẫu số. Macro-F1 lấy trung bình đúng 10 lớp mục tiêu, đầu ra invalid/từ chối tạo lỗi bỏ sót của lớp thật; ghi thêm số invalid. Có thể báo riêng tập clip cả A/V đều hợp lệ, nhưng phải công bố số lượng và giữ kết quả toàn tập.
- ASR tự do đánh giá riêng bằng CER; chuẩn hóa Unicode NFC, chữ thường, bỏ dấu câu nhất quán nhưng **giữ dấu tiếng Việt**, quy định bỏ khoảng trắng khi tính CER. Nếu dùng WER với tách theo khoảng trắng, ghi rõ đây là đơn vị phân tách bằng khoảng trắng, chưa phải tách từ tiếng Việt chuẩn.
- Chấm ASR trên 80 clip test câu định trước và 20 clip test câu ngoài danh sách, báo riêng từng nhóm; đáp án là lời thực tế được người kiểm tra, không ép câu lạ về 10 câu mẫu. Tập câu lạ dev và test có nội dung khác nhau, được viết trước khi chọn ngưỡng.
- Độ trễ: `thời điểm phụ đề cuối xuất hiện − thời điểm người nói kết thúc`, báo cáo trung vị/p95 và số mẫu. Nếu chỉ đo từ lúc bấm Dừng, phải đặt tên chỉ số đúng như vậy. Báo thêm thời gian thu đoạn; không dùng tốc độ xử lý file để tuyên bố streaming.
- Chỉ có 2 người test: kết quả mang tính thăm dò, báo cả từng người. Không kết luận đại diện toàn bộ người dùng hoặc có ý nghĩa thống kê chỉ từ con số tăng nhỏ.

## 5. Tuần 1 — Chốt đề cương và thử quy trình dữ liệu

### Việc cần làm

- [ ] Lập danh sách tên thật tương ứng TV1–TV5, giờ có thể làm, laptop/GPU, ngân sách và hạn thi; giới hạn mỗi người khoảng 12 giờ.
- [ ] Viết đề cương 1–2 trang: vấn đề, phạm vi hai chế độ, giả thuyết, cách đo, hạn chế.
- [ ] Tạo bảng việc có người phụ trách, hạn, trạng thái và link bằng chứng; thống nhất nhánh Git và cách review.
- [ ] Chốt 10 câu và manifest cùng TV2–TV4; lập mẫu đồng ý tham gia, hướng dẫn quay một trang.
- [ ] Phân công tuyển 2 người/thành viên, khóa danh sách split; thu và kiểm tra 20 đoạn pilot với TV5.
- [ ] Viết script kiểm tra manifest: thiếu file, thiếu nhãn, trùng sample_id và người nói giao nhau giữa split.

### Học để làm việc này — khoảng 2 giờ

- 30 phút: [GitHub Hello World](https://docs.github.com/en/get-started/using-github/hello-world), học branch, commit, pull request; thực hành review một thay đổi nhỏ.
- 45 phút: [scikit-learn: tránh rò rỉ dữ liệu](https://scikit-learn.org/stable/common_pitfalls.html), tập trung preprocessing và data leakage; viết 3 tình huống rò rỉ có thể xảy ra với nhóm.
- 45 phút: đọc abstract, sơ đồ và phần dữ liệu của [ViCocktail](https://arxiv.org/abs/2506.04635); ghi điểm kế thừa và điểm nhóm đang thu hẹp. Không cần hiểu hết công thức.

### Nộp cuối tuần và nghiệm thu

- Đề cương, danh sách phân vai, checklist thu, manifest pilot, ghi chú phân chia dữ liệu.
- Báo cáo: số đoạn đạt/loại và lý do; số người đã tuyển; tài nguyên thực tế; quyết định phạm vi.
- **Đạt:** TV2 và TV3 đọc được cùng một sample_id; 20 clip có nhãn đã kiểm tra; không trùng người giữa các split; nhóm đồng ý các mốc ngày 10/14/21.

## 6. Tuần 2 — Hoàn thành dữ liệu và bộ chấm điểm

### Việc cần làm

- [ ] Điều phối thu xong trước ngày 10; mỗi người kiểm tra dữ liệu mình thu, một người khác kiểm tra chéo bản chép lời.
- [ ] Hoàn thành 400 clip chính và 40 clip câu lạ, hoặc ghi rõ phương án 8 người. Không tính bản tạo nhiễu là người/đoạn thu độc lập mới.
- [ ] Khóa nhãn test; cung cấp dữ liệu train/dev và manifest đã kiểm tra cho TV2–TV4.
- [ ] Viết bộ tính accuracy, macro-F1, ma trận nhầm lẫn và CER; kiểm tra bằng 5 trường hợp tính tay gồm dự đoán đúng, sai, thêm/bớt ký tự, chuỗi rỗng.
- [ ] Chạy báo cáo dev đầu tiên từ đầu ra thật của A, V và AV; phân biệt kết quả thật với ví dụ minh họa.

### Học để làm việc này — khoảng 2 giờ

- 45 phút: [scikit-learn metrics](https://scikit-learn.org/stable/api/sklearn.metrics.html), học accuracy, macro-F1 và confusion matrix; giải thích bằng một ví dụ 3 lớp.
- 45 phút: [Hugging Face: đánh giá ASR](https://huggingface.co/learn/audio-course/en/chapter5/evaluation), học lỗi thay thế/thêm/xóa và CER/WER.
- 30 phút: [JiWER](https://github.com/jitsi/jiwer), đọc cách dùng và xử lý chuỗi rỗng; làm 5 ca kiểm tra ở trên.

### Nộp cuối tuần và nghiệm thu

- Dataset card mô tả nguồn, người nói theo mã, split, nhãn, giới hạn sử dụng; manifest đã khóa; script đánh giá; kết quả dev phiên bản đầu.
- Báo cáo: số lượng thực tế từng tập/lớp, tỷ lệ clip loại, lỗi nhãn sửa, kiểm tra rò rỉ, 5 ca tính tay.
- **Đạt:** đủ dữ liệu theo phương án đã chốt; mọi người dùng cùng split và nhãn; có kết quả dev tái lập, chưa dùng test để chọn model.

## 7. Tuần 3 — Chuẩn bị phép thử cuối và viết báo cáo sớm

### Việc cần làm

- [ ] Kiểm tra A/V/AV dùng cùng danh sách clip và cùng thứ tự lớp c00–c09.
- [ ] Chuẩn bị các phiên bản nhiễu cho dev/test bằng script TV2, giữ file nguồn và seed; test vẫn chưa được dùng để chọn tham số.
- [ ] Viết kế hoạch test trước khi mở kết quả: 3 phương pháp × 3 điều kiện, từ chối câu lạ, độ trễ, tình huống mất nguồn.
- [ ] Tổng hợp kết quả dev, kiểm tra có cải thiện hay giảm chất lượng; yêu cầu giải thích bằng ví dụ, không chỉ một điểm trung bình.
- [ ] Viết phần bối cảnh, dữ liệu, phương pháp đánh giá; nhận phần chuyên môn từ bốn thành viên.
- [ ] Ngày 21 ghi lại commit, file model, checksum dữ liệu, cấu hình và ngưỡng cuối.

### Học để làm việc này — khoảng 2 giờ

- 60 phút: đọc lại [hướng dẫn rò rỉ dữ liệu](https://scikit-learn.org/stable/common_pitfalls.html); tự kiểm tra scaler, augmentation, lựa chọn ngưỡng và thứ tự mở test.
- 60 phút: đọc phần thí nghiệm của [ViCocktail](https://www.isca-archive.org/interspeech_2025/nguyen25d_interspeech.pdf); học cách mô tả điều kiện thử và so sánh công bằng, không sao chép kết quả.

### Nộp cuối tuần và nghiệm thu

- Kế hoạch test đã khóa, báo cáo dev, bản thảo phần dữ liệu/phương pháp, biên bản ngày 21.
- Báo cáo: tham số đã chọn từ dev, lý do, điểm yếu còn tồn tại và thử nghiệm bị loại khỏi phạm vi.
- **Đạt:** một người khác chạy được bộ chấm; mỗi kết quả có sample_id/config; không còn quyết định phương pháp chờ test trả lời.

## 8. Tuần 4 — Chạy test, kết luận và chuẩn bị bảo vệ

### Việc cần làm

- [ ] Ngày 22–24 chạy bộ test đã khóa; báo cả từng người và tổng, cả trường hợp không cải thiện.
- [ ] Đối chiếu ít nhất 10 lỗi tiêu biểu với TV2–TV4; chỉ phân tích, không dùng chúng để tinh chỉnh rồi gọi là test độc lập.
- [ ] Tổng hợp báo cáo khoảng 8–12 trang theo thể lệ thật của cuộc thi, kèm nguồn, hạn chế, đóng góp từng người và đường dẫn mã/dữ liệu được phép chia sẻ.
- [ ] Chuẩn bị 8–10 slide: vấn đề, phạm vi, kiến trúc, dữ liệu, phương pháp, kết quả, demo, hạn chế/hướng phát triển.
- [ ] Phân 5 phần thuyết trình, diễn tập 2 lượt; chuẩn bị câu trả lời về tính mới, dữ liệu ít, câu hữu hạn và phần kính chưa hoàn thành nếu có.

### Học để làm việc này — khoảng 2 giờ

- 60 phút: đọc lại [đánh giá ASR](https://huggingface.co/learn/audio-course/en/chapter5/evaluation), tự giải thích CER/WER và vì sao không đồng nhất với accuracy phân loại câu.
- 60 phút: kiểm tra từng kết luận với log và số mẫu; thực hành trình bày một kết quả âm tính có giá trị nghiên cứu. Tài liệu thực hành là báo cáo dev/test của chính nhóm.

### Nộp cuối tuần và nghiệm thu

- Báo cáo cuối, bảng số liệu gốc, biểu đồ có nhãn/đơn vị, slide, biên bản hai lần diễn tập và danh mục đóng góp.
- **Đạt:** mọi số liệu truy được về log; báo cáo phân biệt ASR tự do và nhận dạng 10 câu; không tuyên bố đã có kính độc lập hay đọc được câu bất kỳ khi chưa làm được.

## 9. Mẫu báo cáo cá nhân mỗi tuần

Mỗi thành viên nộp 1–2 trang cùng video demo 1–3 phút; phần số liệu để file riêng nếu dài.

1. Mục tiêu tuần và khối lượng thực tế đã làm.
2. Các nhiệm vụ hoàn tất/chưa hoàn tất, dẫn tới commit/file/video.
3. Cấu hình chạy, dữ liệu và phiên bản model đã dùng.
4. Số đo thật, số mẫu, cách đo; không có số đo thì ghi chưa đo.
5. Ba điều đã học và áp dụng ở đâu.
6. Vấn đề, nguyên nhân đã xác minh, phương án thử tiếp.
7. Đầu ra đã bàn giao cho ai; người nhận xác nhận điều gì.
8. Kế hoạch tuần sau và hỗ trợ cần từ nhóm.

Hoàn thành nhiệm vụ nghĩa là có bằng chứng và người nhận chạy/đọc được, không chỉ đánh dấu đã học tài liệu.
