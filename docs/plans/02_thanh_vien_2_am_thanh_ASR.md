# Thành viên 2 — Âm thanh và nhận dạng lời nói

Người phụ trách: ................................  
Thời gian: 4 tuần từ ngày bắt đầu; 12 giờ/tuần, gồm khoảng 2 giờ học, 7 giờ làm, 2 giờ kiểm tra/báo cáo và 1 giờ họp.

## 1. Bạn chịu trách nhiệm gì?

Bạn làm hai nhánh riêng:

1. **ASR tự do:** dùng model có sẵn để chép lời tiếng Việt từ micro/file âm thanh.
2. **Phân loại 10 câu:** trích đặc trưng âm thanh và học bộ phân loại nhẹ để kết hợp với TV3 qua TV4.

Không lấy kết quả ASR tự do làm bằng chứng phần khẩu hình đã hoạt động. Trong thí nghiệm chính, bộ A là bộ phân loại âm thanh 10 câu; bộ AV kết hợp chính bộ A đó với bộ V của TV3. So sánh AV với một model ASR khác không tự chứng minh lợi ích của hình ảnh.

Đầu vào: âm thanh mono và mốc thời gian do bộ thu TV5/TV4 cung cấp. Đầu ra: văn bản ASR hoặc vector điểm 10 lớp theo thứ tự c00–c09; kèm thời gian xử lý, trạng thái hợp lệ và model_version. Không gửi phần trăm “đúng” nếu chưa hiệu chỉnh và kiểm chứng.

## 2. Quy ước chung bạn phải theo

- TV1 giữ danh sách 10 câu, manifest và test. Mục tiêu dữ liệu: 10 người × 10 câu × 4 lần = 400 đoạn; 6/2/2 người ở train/dev/test. Nếu chỉ có 8 người: 4/2/2. Không chia ngẫu nhiên từng file khiến cùng người lọt vào nhiều tập.
- Có thêm 20 câu ngoài danh sách ở dev và 20 ở test, dùng thử từ chối; không huấn luyện lên các câu này.
- Âm thanh đầu vào thống nhất mono 16 kHz sau chuyển đổi đúng cách; giữ bản gốc. Không chỉ thay giá trị sample_rate mà không resample.
- Hai bên dùng cùng đoạn thời gian. Nếu audio được cắt đầu/cuối thì TV4 phải cắt video tương ứng; không tự bỏ khoảng lặng làm lệch khẩu hình.
- Bản mẫu đầu nhận dạng từng đoạn bằng nút Bắt đầu/Dừng. Tách câu tự động/VAD là mở rộng khi đã chạy ổn.
- Ngày 4: ASR file chạy; ngày 14: A và ASR được gọi qua hàm; ngày 21: khóa cấu hình; tuần 4: hỗ trợ test, không chỉnh theo test.
- Mỗi người tuyển/hỗ trợ quay 2 người nói. Chỉ nhận train/dev để phát triển model.

## 3. Công nghệ đề xuất và phần cần hiểu

- Python, NumPy; thu âm qua `sounddevice` do TV5 tích hợp.
- `faster-whisper` cho ASR: thử một model nhỏ có hỗ trợ đa ngôn ngữ; không chọn checkpoint chỉ tiếng Anh. Chọn kích thước và kiểu tính toán sau khi đo trên laptop thật. GPU không bắt buộc cho nhánh phân loại nhẹ.
- `librosa` để tính MFCC: đặc trưng tóm tắt phổ âm thanh theo thời gian.
- `StandardScaler` + `LogisticRegression` trong một pipeline scikit-learn cho 10 lớp. Đây là baseline đơn giản, không phải kiến trúc tối ưu đã được chứng minh.
- Chia chuỗi MFCC thành 8 vùng thời gian tương đối, lấy trung bình/độ lệch chuẩn từng vùng rồi ghép thành vector. Trường hợp quá ngắn phải xử lý có quy tắc, không tạo NaN.

## 4. Tuần 1 — Hiểu âm thanh và dựng hai đầu vào

### Các bước thực hiện

- [ ] Ngày 1: kiểm tra Python/môi trường, CPU/GPU/RAM và thiết bị thu với TV5; ghi phiên bản đã chạy được, không nâng thư viện tùy ý giữa dự án.
- [ ] Ngày 2: thu một câu, lưu WAV và nghe lại; kiểm tra kênh, tần số lấy mẫu, độ dài, méo do clipping.
- [ ] Ngày 3–4: chạy ASR trên ít nhất 10 đoạn tiếng Việt pilot; chọn chế độ chép lời, không dịch sang tiếng Anh.
- [ ] Viết hàm ASR nhận dữ liệu/đường dẫn trung tính và trả text + thời gian xử lý. Tách tải model khỏi mỗi lần suy luận.
- [ ] Tạo notebook/scrip nhỏ vẽ waveform, spectrogram và MFCC của 2 câu; ghi shape và đơn vị trục.
- [ ] Thống nhất API âm thanh với TV4; hỗ trợ quay pilot và tuyển 2 người.

### Học thêm — khoảng 2 giờ, vừa đọc vừa làm

- 35 phút: [Hugging Face: model ASR](https://huggingface.co/learn/audio-course/en/chapter5/asr_models), hiểu inference, CTC/encoder-decoder ở mức khái niệm; vẽ đường đi audio → text.
- 35 phút: [faster-whisper README](https://github.com/SYSTRAN/faster-whisper), đọc Installation và Usage; chạy ví dụ trên một file Việt. Hiệu năng trong README không phải hiệu năng máy nhóm.
- 25 phút: [sounddevice Usage](https://python-sounddevice.readthedocs.io/en/latest/usage.html), học recording, sample rate và array; kiểm tra file thu có thời lượng đúng.
- 25 phút: [librosa MFCC](https://librosa.org/doc/0.11.0/generated/librosa.feature.mfcc.html), hiểu tham số `sr`, `n_mfcc`, shape đầu ra; không cần tự suy diễn toàn bộ biến đổi toán học tuần này.

### Nộp báo cáo và nghiệm thu

- Nộp script ASR, file cấu hình môi trường, 10 kết quả pilot, hình waveform/MFCC, mô tả API.
- Báo cáo: model nào, máy nào, thời gian tải và suy luận riêng; 3 lỗi chép lời; vấn đề chất lượng thu.
- **Đạt:** TV4 gọi được hàm ASR; text Việt giữ dấu; thời lượng âm thanh đúng; không tải model lặp lại mỗi câu.

## 5. Tuần 2 — Huấn luyện baseline âm thanh 10 câu

### Các bước thực hiện

- [ ] Nhận train/dev của TV1 trước hoặc trong ngày 10; kiểm tra thiếu file và mapping c00–c09.
- [ ] Viết hàm tiền xử lý chung cho train và inference: mono/resample, quy tắc mức âm lượng, MFCC, pooling 8 vùng. Fit scaler chỉ trên train.
- [ ] Huấn luyện Logistic Regression; cố định seed. Chỉ thử tối đa 2–3 cấu hình nhỏ để tránh hết thời gian vào tuning.
- [ ] Chạy dev, lưu sample_id, nhãn dự đoán, vector điểm và thời gian; gửi TV1 để chấm độc lập.
- [ ] Viết adapter trả 10 điểm theo đúng class_order. Nếu thư viện sắp xếp lớp khác, ánh xạ lại bằng `classes_`.
- [ ] Gói ASR tự do và bộ A thành hai hàm riêng; đưa ví dụ cho TV4 trước ngày 14.

### Học thêm — khoảng 2 giờ

- 45 phút: [LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html), học `fit`, `predict`, `predict_proba`, `classes_`; chạy bài 3 lớp nhỏ trước.
- 35 phút: [scikit-learn: lỗi thường gặp](https://scikit-learn.org/stable/common_pitfalls.html), tập trung scaler chỉ fit train và dùng Pipeline.
- 40 phút: [Hugging Face: đánh giá ASR](https://huggingface.co/learn/audio-course/en/chapter5/evaluation), phân biệt CER của ASR với accuracy của bài 10 câu; tự tính một ví dụ.

### Nộp báo cáo và nghiệm thu

- Nộp bộ A đã lưu, script train/infer, metadata features/class_order, kết quả dev và hướng dẫn chạy.
- Báo cáo: số mẫu từng lớp; cấu hình đã thử; accuracy/macro-F1 do TV1 tính; 5 nhầm lẫn tiêu biểu; thời gian ASR và A.
- **Đạt:** từ một clip chưa dùng train tạo ra đủ 10 điểm hữu hạn; TV4 chạy được; không đọc transcript hoặc tên nhãn khi dự đoán.

## 6. Tuần 3 — Tạo nhiễu có kiểm soát và ổn định vận hành

### Các bước thực hiện

- [ ] Viết script thêm nhiễu tại SNR +10 dB và 0 dB. Với công suất tín hiệu `Ps`, nhiễu `Pn`, hệ số nhiễu là `sqrt(Ps / (Pn * 10^(SNR_dB/10)))`; xác định công suất trên vùng lời nói đã thống nhất, tránh clip im lặng.
- [ ] Kiểm tra SNR đầu ra, xử lý clipping bằng cách co đồng thời tín hiệu/nhiễu nếu cần; ghi hệ số và seed. Không chuẩn hóa hai thành phần độc lập sau khi trộn.
- [ ] Dùng cùng file nhiễu cho so sánh A và AV; nguồn/đoạn nhiễu train, dev, test tách biệt. Nếu thêm augmentation để train, chỉ dùng bản xuất phát từ train.
- [ ] Chạy A và ASR trên dev sạch/nhiễu; gửi đầu ra thô cho TV1, vector A cho TV4.
- [ ] Đo trường hợp im lặng, rút micro, clipping; cùng TV5 tạo thông báo lỗi thay vì giữ câu cũ như kết quả mới.
- [ ] Tối ưu một yếu tố có bằng chứng gây chậm: model ASR nhỏ hơn hoặc giảm xử lý thừa. Khóa ngày 21.

### Học thêm — khoảng 2 giờ

- 40 phút: đọc lại [librosa MFCC](https://librosa.org/doc/0.11.0/generated/librosa.feature.mfcc.html), kiểm tra cửa sổ/hop và khác biệt giữa phổ log với waveform; giải thích ảnh hưởng nhiễu.
- 40 phút: [faster-whisper](https://github.com/SYSTRAN/faster-whisper), xem các lựa chọn suy luận phù hợp máy; đo một thay đổi thay vì chạy hết tùy chọn.
- 40 phút: [sounddevice](https://python-sounddevice.readthedocs.io/en/latest/usage.html), học streaming/callback ở mức đủ để phối hợp TV5. Nếu chưa ổn, giữ thu từng đoạn.

### Nộp báo cáo và nghiệm thu

- Nộp script nhiễu, danh sách nguồn nhiễu và quyền dùng, log kiểm tra SNR, model/config khóa, phần viết “Nhánh âm thanh” khoảng 1–2 trang.
- Báo cáo: kết quả theo từng điều kiện dev; độ trễ; lỗi mất micro; thay đổi nào cải thiện hoặc làm xấu kết quả.
- **Đạt:** TV1 tạo lại đúng biến thể nhiễu từ seed; A và AV dùng cùng waveform; có đường xử lý lỗi, không còn NaN.

## 7. Tuần 4 — Bàn giao, hỗ trợ test và bảo vệ

### Các bước thực hiện

- [ ] Hỗ trợ TV1 chạy test bằng model/config ngày 21; chỉ sửa lỗi thực thi có ghi nhận, không tuning theo test.
- [ ] Chọn 3 câu ASR đúng và 3 lỗi đáng học từ log để giải thích; không chỉ chọn video thuận lợi làm bằng chứng chất lượng.
- [ ] Kiểm tra model đã tải sẵn trên máy demo; xác nhận có cần Internet lúc chạy hay không bằng thử thực tế.
- [ ] Hoàn thiện hướng dẫn cài/chạy, tài nguyên cần và phần âm thanh trong báo cáo; tham gia 2 lượt diễn tập.

### Học thêm — khoảng 2 giờ

- 60 phút: đọc lại [Hugging Face ASR metrics](https://huggingface.co/learn/audio-course/en/chapter5/evaluation) và kết quả nhóm; giải thích 3 lỗi thay/thêm/xóa.
- 60 phút: luyện trình bày sơ đồ đặc trưng MFCC → classifier → 10 điểm; tài liệu chính là code và log của bạn. Phân biệt pipeline này với ASR tự do.

### Nộp báo cáo và nghiệm thu

- Nộp mã, model, phiên bản môi trường, hướng dẫn chạy, log hiệu năng cuối và phần báo cáo chuyên môn.
- **Đạt:** TV4 hoặc TV5 chạy lại được trên máy demo; bạn giải thích được vì sao câu ngoài danh sách không được ép thành một trong 10 câu với sự chắc chắn giả tạo.

## 8. Nếu chậm tiến độ

- ASR cài lỗi: tối đa một buổi tìm cấu hình tương thích; nhờ TV4 hỗ trợ, thử model nhỏ/CPU theo tài liệu. Không để ASR chặn nhánh phân loại nhẹ.
- Accuracy thấp: kiểm tra nhãn, âm lượng, class_order và rò rỉ trước khi đổi model. Không dùng test để sửa.
- Không đủ thời gian làm VAD: giữ nút Bắt đầu/Dừng, ghi rõ độ trễ theo đoạn.
- Chưa có cải thiện trong nhiễu: báo trung thực, phân tích; không thêm bước sửa văn bản bằng LLM để che lỗi đo lường.

## 9. Mẫu báo cáo tuần

Mục tiêu → việc đã làm và commit → kiến thức đã học → cấu hình/dữ liệu → số đo và số mẫu → lỗi còn lại → đầu ra bàn giao cho TV1/TV4/TV5 → kế hoạch tuần sau. Kèm video 1–3 phút và lệnh chạy thực tế. Checklist chỉ được đánh dấu hoàn thành khi đầu ra chạy được.
