# TV3 — Hoàng Hiếu — Thị giác máy tính và khẩu hình

Người phụ trách: Hoàng Hiếu — Thị giác máy tính và khẩu hình

Thời gian: 4 tuần, khoảng 12 giờ/tuần: 2 giờ học, 7 giờ làm, 2 giờ kiểm tra/báo cáo và 1 giờ họp.

## 1. Vai trò và phạm vi của bạn

Bạn xây nhánh camera → chuyển động miệng → bộ phân loại 10 câu → vector điểm cho TV4. Đây là thí nghiệm nhận dạng câu trong danh sách hữu hạn, không phải model đọc được mọi câu tiếng Việt. Phát hiện được miệng hoặc đo miệng mở/đóng chưa đủ để gọi là đọc khẩu hình.

Bản mẫu chính chạy trên laptop. Camera gắn kính là bước mở rộng; việc chuyển từ webcam cố định sang camera rung theo đầu phải được kiểm tra riêng.

Phối hợp: TV1 giao train/dev và nhãn; TV2 cung cấp thông tin âm thanh nhưng nhánh V không được dùng âm thanh để dự đoán; TV4 quản lý đồng bộ và kết hợp; TV5 quản lý luồng camera của ứng dụng. Chỉ một nơi mở camera khi chạy tích hợp, tránh tranh chấp thiết bị.

## 2. Các quy ước dùng chung

- 10 câu c00–c09 do TV1 chốt trước khi thu. Bộ chính: 10 người × 10 câu × 4 lần = 400 đoạn; 6/2/2 người ở train/dev/test. Nếu thiếu người, phương án 8 người chia 4/2/2.
- Cùng câu xuất hiện ở các tập, người nói khác nhau. Không kết luận model hiểu câu mới từ phép thử này.
- Mỗi thành viên hỗ trợ tuyển/quay 2 người. TV1 kiểm soát tập test; chỉ dùng train/dev để chọn features, model và ngưỡng chất lượng hình.
- Ảnh của mọi frame từ cùng clip và mọi augmentation giữ cùng split. Không coi các frame liên tiếp là các mẫu test độc lập.
- Nhánh V nhận video/landmarks và timestamp; không đọc âm thanh, transcript hay tên file có nhãn.
- Ngày 4 cắt được miệng; ngày 14 bộ V gọi được từ TV4; ngày 21 khóa model; tuần 4 hỗ trợ test.

## 3. Cách làm vừa sức trong 4 tuần

Đường chính:

1. Đọc frame bằng OpenCV; dùng MediaPipe Face Landmarker tìm các mốc trên khuôn mặt.
2. Xác định vùng miệng để xem chất lượng; lưu chuỗi landmarks miệng và timestamp.
3. Chuẩn hóa tịnh tiến, kích thước và góc xoay mặt bằng các mốc ổn định; biểu diễn vị trí tương đối của các điểm miệng. Ghi rõ quy tắc tọa độ.
4. Lấy đặc trưng hình dạng/chuyển động: độ mở, độ rộng chuẩn hóa, vị trí tương đối và chênh lệch giữa các frame có tính đến khoảng thời gian.
5. Chia chuỗi thành 8 vùng thời gian tương đối, lấy trung bình/độ lệch chuẩn; ghép thành vector cố định.
6. Dùng StandardScaler + Logistic Regression để phân loại 10 câu. Fit scaler/model chỉ trên train.

Đây là baseline nhẹ để kiểm chứng quy trình, có thể cho kết quả thấp. Đặc trưng landmarks bỏ lỡ thông tin răng/lưỡi/ảnh chi tiết; không hứa hẹn đạt chất lượng model đọc môi hiện đại. Nếu không vượt mức đoán ngẫu nhiên khoảng 10% trên dev cân bằng, cần kiểm tra pipeline và báo rõ, không giấu kết quả.

Mở rộng chỉ sau khi baseline chạy và còn thời gian: khảo sát model pretrained. [AV-HuBERT](https://github.com/facebookresearch/av_hubert) là mã nghiên cứu đã được lưu trữ ở trạng thái archive; cài đặt và checkpoint có thể không phù hợp tiếng Việt/máy hiện có. [ViCocktail](https://huggingface.co/datasets/nguyenvulebinh/ViCocktail) là nguồn dữ liệu tham khảo, không có nghĩa đã có sẵn một model cắm vào chạy. Không dành cả bốn tuần để sửa môi trường cho một repository.

## 4. Tuần 1 — Đọc camera và trích vùng miệng

### Các bước thực hiện

- [ ] Ngày 1: cùng TV5 thử webcam; xác định độ phân giải/fps thực đo, ánh sáng và khoảng cách để miệng đủ rõ. Có thể bắt đầu bằng 720p, mục tiêu khoảng 25–30 fps nếu máy đáp ứng; đây là cấu hình đề xuất, không phải yêu cầu cố định.
- [ ] Ngày 2–3: chạy Face Landmarker; vẽ điểm miệng trên video pilot và crop vùng miệng có lề.
- [ ] Ngày 4: cung cấp cho TV4 một sample gồm chuỗi landmarks/crop, timestamp và cờ valid.
- [ ] Ghi hành vi khi không có mặt, nhiều mặt, quay nghiêng hoặc miệng bị che. Trước mắt chỉ xử lý một người, không tự chọn ngẫu nhiên giữa nhiều người.
- [ ] Viết hướng dẫn quay 1 trang cho TV1: mặt hướng camera, ánh sáng đủ, tránh rung, không đọc hết câu trước khi bắt đầu thu.
- [ ] Kiểm tra 20 clip pilot; hỗ trợ tuyển 2 người và thu theo lịch chung.

### Học thêm — khoảng 2 giờ

- 35 phút: [OpenCV: Getting Started with Videos](https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html), học VideoCapture, frame, đọc file và giải phóng camera; quay một video ngắn rồi đọc lại.
- 50 phút: [MediaPipe Face Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker?tab=Python), đọc mục Python, running modes và landmarks; chạy ví dụ tương ứng phiên bản cài thật. Dùng Tasks API theo tài liệu, tránh chép ví dụ API cũ không tương thích.
- 35 phút: [nghiên cứu về viseme](https://arxiv.org/abs/2307.10157), đọc abstract/introduction để hiểu vì sao hình miệng không tương ứng từng chữ cái; viết giải thích 5–7 dòng.

### Nộp báo cáo và nghiệm thu

- Nộp script landmarks/crop, video có lớp đánh dấu, mẫu dữ liệu cho TV4, hướng dẫn quay.
- Báo cáo: fps thực, phần trăm frame hợp lệ theo định nghĩa rõ, 5 ví dụ tốt/xấu và thời gian xử lý.
- **Đạt:** crop không trượt khỏi miệng trên pilot mặt thẳng; khi mất mặt trả invalid; không lấy lại frame cũ rồi coi là frame mới.

## 5. Tuần 2 — Học bộ phân loại khẩu hình 10 câu

### Các bước thực hiện

- [ ] Nhận dữ liệu train/dev từ TV1 trước hoặc trong ngày 10; chỉ dùng train để fit các bước học tham số.
- [ ] Xây đặc trưng chuỗi như phần 3; lưu tên đặc trưng, shape, thứ tự điểm và cách xử lý frame bị thiếu.
- [ ] Chuẩn hóa vị trí/kích thước để model ít học nhầm mặt lớn/nhỏ hoặc vị trí người ngồi; không đưa background vào feature.
- [ ] Chia 8 vùng thời gian và train Logistic Regression; cố định seed, chỉ thử 2–3 cấu hình nhỏ.
- [ ] Trả vector 10 điểm theo class_order c00–c09; dùng `classes_` để kiểm tra thứ tự.
- [ ] Kiểm tra clip ngắn, trống, không đủ frame; gửi kết quả invalid và lý do thay vì tạo điểm giả.
- [ ] Trước ngày 14 bàn giao hàm infer cho TV4 và dự đoán dev cho TV1.

### Học thêm — khoảng 2 giờ

- 40 phút: [LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html), thực hành fit/predict_proba/classes_; giải thích 10 chiều đầu ra.
- 40 phút: [scikit-learn: lỗi thường gặp](https://scikit-learn.org/stable/common_pitfalls.html), học scaler/Pipeline và rò rỉ do chia frame thay vì chia người.
- 40 phút: đọc lại [Face Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker?tab=Python), đặc biệt tọa độ, chế độ video và timestamp; vẽ trực quan feature để phát hiện lỗi chuẩn hóa.

### Nộp báo cáo và nghiệm thu

- Nộp script trích features/train/infer, model, class_order, cấu hình và kết quả dev theo sample_id.
- Báo cáo: accuracy/macro-F1 từ TV1, tỷ lệ invalid, thời gian/clip và 5 cặp câu dễ nhầm. Ghi cả trường hợp model gần mức ngẫu nhiên.
- **Đạt:** TV4 chạy được với clip mới; V hoàn toàn không sử dụng audio/transcript; feature hữu hạn, shape nhất quán.

## 6. Tuần 3 — Kiểm tra chất lượng hình và đóng góp của chuyển động

### Các bước thực hiện

- [ ] Tạo bộ ca dev có đủ sáng, quay nghiêng, che miệng và mất mặt. Dùng người thuộc train/dev; không đưa người test vào demo phát triển.
- [ ] Xác định quy tắc valid: tỷ lệ frame nhìn được mặt, số frame tối thiểu và khoảng trống tối đa. Ngưỡng chọn trên dev, không cam kết phát hiện được mọi trường hợp che miệng.
- [ ] Đo sự ổn định khi đầu di chuyển; kiểm tra feature đang mô tả miệng hay chủ yếu vị trí đầu.
- [ ] Thử một phép đối chứng: xáo trộn thứ tự frame trên dev rồi chạy V. Nếu chất lượng gần như không đổi, ghi rằng model có thể chưa tận dụng tốt động học; không tự kết luận chỉ từ một phép thử.
- [ ] Cùng TV4 xác nhận đoạn hình và âm thanh có cùng khoảng thời gian; không tự tăng tốc video hoặc bỏ frame mà làm mất timestamp gốc.
- [ ] Khóa feature/model/config ngày 21; viết phần phương pháp hình ảnh 1–2 trang.

### Học thêm — khoảng 2 giờ

- 45 phút: [AV-HuBERT paper](https://arxiv.org/abs/2201.02184), đọc abstract và sơ đồ để hiểu model chuỗi khác baseline landmarks của nhóm ra sao.
- 45 phút: [ViCocktail paper](https://arxiv.org/abs/2506.04635), học vai trò cắt vùng miệng và đồng bộ; ghi 3 việc có thể học theo mà không huấn luyện lại hệ lớn.
- 30 phút: [scikit-learn metrics](https://scikit-learn.org/stable/api/sklearn.metrics.html), đọc confusion matrix; chọn 2 cặp câu nhầm để xem video chậm và phân tích.

### Nộp báo cáo và nghiệm thu

- Nộp log ca chất lượng hình, kết quả đối chứng, model đã khóa và phần báo cáo.
- Báo cáo: tỷ lệ invalid từng điều kiện, lỗi do landmark/camera/model, mức ảnh hưởng của xáo trộn frame.
- **Đạt:** khi V không đáng tin, TV4 nhận được cờ/lý do để dùng A; không trả “không thấy miệng” thành một câu giao tiếp chắc chắn.

## 7. Tuần 4 — Hỗ trợ đánh giá và trình bày giới hạn

### Các bước thực hiện

- [ ] Hỗ trợ TV1 chạy V trên test bằng pipeline đã khóa; ghi riêng các clip không có đầu vào hợp lệ.
- [ ] Phân tích ít nhất 5 lỗi mà chỉ nghe đúng nhưng nhìn sai, hoặc ngược lại, nếu dữ liệu thực tế có; không dựng ví dụ.
- [ ] Kiểm tra nhánh camera trong app TV5; nếu có camera gắn kính, chạy thêm thử nghiệm riêng và ghi điều kiện khác với webcam.
- [ ] Viết hướng dẫn inference, bàn giao model/feature config; tham gia 2 lượt diễn tập.
- [ ] Chuẩn bị trả lời: “Đây có phải đọc khẩu hình tổng quát?”, “Vì sao cùng khẩu hình có thể ứng với âm khác?”, “Dữ liệu ít ảnh hưởng gì?”.

### Học thêm — khoảng 2 giờ

- 60 phút: đọc lại [nghiên cứu viseme](https://arxiv.org/abs/2307.10157) và ghi chú tuần 1; liên hệ với lỗi thực tế.
- 60 phút: rà code/feature plot của chính nhóm, luyện giải thích từ frame đến vector 10 chiều trong 3 phút; người TV2 nghe và hỏi lại.

### Nộp báo cáo và nghiệm thu

- Nộp mã/model, video giải thích, kết quả và hạn chế, phần báo cáo đã kiểm chứng.
- **Đạt:** người khác chạy lại được; bản trình bày nói đúng phạm vi 10 câu; không đồng nhất landmark detection với đọc môi.

## 8. Khi gặp khó khăn

- Không chạy được MediaPipe: kiểm tra phiên bản Python và API theo tài liệu, thử môi trường riêng; phối hợp TV4, giới hạn xử lý lỗi cài đặt một buổi rồi báo trưởng nhóm.
- V thấp hơn dự kiến: xem video/nhãn/features, kiểm tra scaler và thứ tự lớp trước; không tăng số lớp hay đổi sang Transformer lớn giữa tuần 3.
- Không có cải thiện AV: vẫn bàn giao V, đánh giá trung thực; có thể kết luận baseline hình ảnh chưa đủ thông tin.
- Thiếu thời gian: giữ xử lý video từng đoạn, hoãn inference liên tục, model deep learning và nhiều người nói.

## 9. Mẫu báo cáo tuần

Mục tiêu → checklist có bằng chứng → tài liệu đã học và bài thực hành → cấu hình camera/features/model → số đo và số mẫu → lỗi/giới hạn → bàn giao TV1/TV4/TV5 → việc tuần sau. Kèm demo 1–3 phút; mọi biểu đồ phải có tên chỉ số và đơn vị.
