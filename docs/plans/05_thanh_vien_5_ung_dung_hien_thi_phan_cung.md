# Thành viên 5 — Ứng dụng, hiển thị phụ đề và phần cứng

Người phụ trách: ................................  
Thời gian: 4 tuần, khoảng 12 giờ/tuần: 2 giờ học, 7 giờ làm, 2 giờ kiểm tra/báo cáo và 1 giờ họp.

## 1. Sản phẩm bạn chịu trách nhiệm

Bạn làm ứng dụng mà người dùng nhìn thấy và thao tác: Bắt đầu/Dừng thu, chọn chế độ, xem phụ đề, biết khi hệ thống không nhận dạng được. Bạn cũng khảo sát đường đưa chữ lên kính, nhưng đầu ra bắt buộc trong 4 tuần là ứng dụng chạy trên laptop.

Hai chế độ phải có tên rõ:

- **Phụ đề tiếng Việt từ âm thanh:** ASR tự do, nhận text từ TV2 qua TV4.
- **Thí nghiệm 10 câu nghe–nhìn:** chọn A/V/AV, nhận câu thuộc danh sách hoặc trạng thái chưa nhận dạng. Không gọi đây là khả năng hiểu mọi câu tiếng Việt.

Mặc định thu từng đoạn bằng nút Bắt đầu/Dừng, xử lý xong mới nhận đoạn tiếp. Đây là bản mẫu theo lượt nói; nhận dạng liên tục là việc mở rộng.

Phối hợp: TV4 sở hữu pipeline và API; TV2 hướng dẫn âm thanh; TV3 hướng dẫn hình; TV1 quản lý dữ liệu, người thử và đánh giá. Bạn không phải tự huấn luyện thêm model.

## 2. Thiết kế và giới hạn phần cứng

### Đường bắt buộc

Camera + micro → laptop xử lý → cửa sổ phụ đề. Dùng thiết bị sẵn có trước; không mua kính khi chưa kiểm tra giao diện kết nối và khả năng nhận hình từ laptop.

### Đường mở rộng

Nếu mượn được kính AR/bộ hiển thị gần mắt hoặc module có tài liệu rõ: xuất cửa sổ phụ đề sang thiết bị theo kết nối được nhà sản xuất hỗ trợ. Một module màn hình nhỏ chưa tự trở thành màn hình gần mắt; cần hệ quang học để lấy nét và nhìn được cảnh thật.

Trong tuần 1, lập danh sách thiết bị và kiểm tra:

- Thiết bị đã có, người cho mượn và thời điểm nhận.
- Đường vào hình ảnh: HDMI, DisplayPort qua USB-C, SDK hay giao thức khác; USB-C có hình dạng phù hợp chưa chứng minh hỗ trợ xuất video.
- Độ phân giải thực, font tiếng Việt, nguồn điện và phụ kiện cần.
- Camera/micro là bộ phận riêng hay thiết bị có cho truy cập dữ liệu thô.
- Tổng chi phí theo báo giá có ngày và nguồn; không coi ước tính là giá mua đã xác nhận.

**Chốt ngày 7:** nếu chưa có thiết bị và cách xuất hình được kiểm chứng, tiếp tục ứng dụng laptop; ghi phần kính là thiết kế/mô phỏng. Nếu có thiết bị trước ngày 14, thử xuất hình; chỉ giữ việc tích hợp nếu không làm trễ phần mềm chính. Không đặt mục tiêu tự chế waveguide hay PCB trong 4 tuần.

Nguồn tham khảo sản phẩm để hiểu luồng sử dụng, không phải yêu cầu mua: [XRAI Platforms](https://xrai.glass/platforms/). Việc nền tảng đó hỗ trợ kính không chứng minh mọi kính đều chạy được ứng dụng của nhóm.

## 3. Quy ước phối hợp

- Dùng Python + Tkinter làm UI đơn giản. Tách luồng thu/xử lý khỏi event loop; dùng queue và cập nhật widget trên luồng UI.
- Chỉ một bộ thu mở camera/micro; chia dữ liệu cho các nhánh qua TV4, không để mỗi module mở thiết bị riêng.
- Frame/audio phải có timestamp chung; phối hợp TV4 kiểm tra offset và TV3 kiểm tra fps thực.
- Dataset chung: 400 đoạn, 10 người, 10 câu, 4 lần; split 6/2/2 người. Bạn tuyển/hỗ trợ thu 2 người, không tự dùng người test để chỉnh UI/model trước đánh giá cuối.
- TV4 bàn giao schema ngày 2; bạn có thể dùng dữ liệu giả gắn nhãn để xây UI sớm, nhưng trước ngày 14 phải nối kết quả thật.
- Giữ tối đa một lượt xử lý đang chạy ở bản đầu; nút Dừng/tạm dừng không để kết quả cũ bất ngờ hiện thành câu mới.

## 4. Tuần 1 — Giao diện mẫu, thu dữ liệu và quyết định phần cứng

### Các bước thực hiện

- [ ] Ngày 1: kiểm kê máy, camera, micro và thiết bị hiển thị với TV1; ghi tài nguyên và giới hạn ngân sách thật.
- [ ] Ngày 2: dựng UI có chọn chế độ, Bắt đầu/Dừng, vùng phụ đề 1–2 dòng và trạng thái đang thu/đang xử lý/chưa rõ/lỗi. Dữ liệu giả phải có nhãn “Mô phỏng”.
- [ ] Cho chỉnh cỡ chữ, xuống dòng và tương phản; ưu tiên cụm chữ ổn định, chưa làm chữ chạy liên tục.
- [ ] Cùng TV2/TV3 làm bộ thu pilot; lưu audio/video đúng sample_id, thông tin thiết bị và thời điểm.
- [ ] Cùng TV4 ghi clip kiểm tra đồng bộ riêng; cùng TV1 kiểm tra 20 clip pilot.
- [ ] Ngày 7 đưa quyết định phần cứng: thiết bị đã thử được, còn chờ, hoặc dùng laptop. Hỗ trợ tuyển 2 người nói.

### Học thêm — khoảng 2 giờ

- 45 phút: [Tkinter](https://docs.python.org/3/library/tkinter.html), học window, label, button, event loop và phần threading; làm nút đổi dòng phụ đề.
- 30 phút: [OpenCV video](https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html), học mở/đóng webcam và đọc frame; kiểm tra camera không bị giữ sau khi tắt app.
- 25 phút: [sounddevice Usage](https://python-sounddevice.readthedocs.io/en/latest/usage.html), học record và sample rate để phối hợp TV2.
- 20 phút: [W3C: involving users](https://www.w3.org/WAI/planning/involving-users/), học cách hỏi người dùng về tác vụ cụ thể, không tự giả định mọi người khiếm thính có cùng nhu cầu.

### Nộp báo cáo và nghiệm thu

- Nộp video UI giả lập, công cụ thu pilot, checklist thiết bị và quyết định hiển thị.
- Báo cáo: chức năng thật/giả lập, thiết bị đã kiểm chứng, chi phí dự kiến có nguồn nếu có, lỗi thu gặp phải.
- **Đạt:** text Việt có dấu hiển thị đúng; Bắt đầu/Dừng hoạt động; app giải phóng thiết bị; mọi người biết phần kính có nằm trong demo tuần 4 hay không.

## 5. Tuần 2 — Nối kết quả thật và làm lượt sử dụng hoàn chỉnh

### Các bước thực hiện

- [ ] Nhận API của TV4, thay nội dung giả bằng kết quả thực; giữ mock ở chế độ phát triển riêng có nhãn.
- [ ] Tách luồng xử lý khỏi Tkinter: nhận job qua queue, đưa kết quả về main thread bằng cơ chế event/after phù hợp.
- [ ] Cho chạy ASR tự do và thí nghiệm 10 câu như hai chế độ riêng; hiển thị nguồn A/V/AV đúng kết quả trả về.
- [ ] Xử lý trạng thái uncertain/invalid/error bằng thông báo ngắn: “Chưa nhận dạng rõ”, “Không thấy mặt”, “Không có micro”; chi tiết kỹ thuật ghi log, không chiếm vùng phụ đề.
- [ ] Không hiển thị điểm model dưới dạng xác suất đúng. Không tự sửa câu nhận dạng để “nghe tự nhiên” khi hệ thống đang được đo.
- [ ] Nếu có kính tương thích trước ngày 14, thử xuất chữ cố định trước, sau đó mới text động; nếu chưa có, hoàn thiện fullscreen trên laptop và đánh dấu mô phỏng kính.

### Học thêm — khoảng 2 giờ

- 40 phút: [Python queue](https://docs.python.org/3/library/queue.html), học producer/consumer, hàng đợi giới hạn và xử lý khi đầy; viết ví dụ một job chậm.
- 40 phút: [Tkinter](https://docs.python.org/3/library/tkinter.html), đọc threading model, thực hành không cập nhật widget từ worker.
- 40 phút: đọc API TV4 và tài liệu chính hãng của thiết bị thật nếu có. Nếu chưa có kính, dùng thời gian làm thử nghiệm font, xuống dòng và trạng thái lỗi.

### Nộp báo cáo và nghiệm thu

- Nộp app bản đầu, video một lượt thu → dự đoán → phụ đề, log kết quả và trạng thái phần cứng.
- Báo cáo: mode nào đã chạy thật, thời gian chờ, lỗi UI đứng hình, đầu ra nào đang là mô phỏng.
- **Đạt:** cả hai chế độ phần mềm được nối theo khả năng pipeline; người dùng thao tác được trong khi xử lý; phụ đề không lấy từ đáp án đã nạp sẵn. Nếu A/V chưa được bàn giao, báo rõ mục này chưa đạt.

## 6. Tuần 3 — Thử người dùng, xử lý lỗi và đo độ trễ

### Các bước thực hiện

- [ ] Chuẩn bị 5 tác vụ: bắt đầu nhận dạng, dừng/tạm dừng, đọc một câu, tăng cỡ chữ, nhận biết khi hệ thống chưa rõ.
- [ ] Thử với 3–5 người tình nguyện; nếu tiếp cận được người khiếm thính và họ đồng ý, ưu tiên lấy phản hồi trực tiếp. Nếu chỉ thử với bạn học, ghi rõ đây là thử khả dụng ban đầu, chưa xác nhận đáp ứng người khiếm thính.
- [ ] Ghi mỗi người làm được tác vụ nào, mất bao lâu và vướng ở đâu; không suy rộng từ mẫu nhỏ.
- [ ] Thử rút camera, mất micro, nhấn nút nhiều lần, đổi chế độ khi đang chạy và đóng app giữa job; không để câu cũ hiện như câu mới.
- [ ] Đo thời điểm nhận job, bắt đầu/kết thúc suy luận, cập nhật widget và phụ đề thực sự hiển thị nếu đo được. Nếu chỉ đo thời điểm gọi cập nhật UI, ghi đây là xấp xỉ, không nhận là đo photon-to-photon.
- [ ] Với TV1/TV4, thống nhất độ trễ cuối câu → phụ đề; nếu dùng bấm Dừng làm mốc thì ghi riêng độ trễ sau nút Dừng. Mục tiêu kỹ thuật đề xuất là cố gắng dưới 2 giây sau khi kết thúc đoạn trên máy demo, nhưng phải báo số đo thực, không coi đây là lời hứa chất lượng.

### Học thêm — khoảng 2 giờ

- 45 phút: [W3C: involving users](https://www.w3.org/WAI/planning/involving-users/), học quan sát tác vụ và ghi phản hồi; viết kịch bản thử không gợi ý đáp án.
- 30 phút: [Python perf_counter](https://docs.python.org/3/library/time.html#time.perf_counter), học đo thời lượng bằng đồng hồ monotonic; so sánh với timestamp dữ liệu.
- 45 phút: đọc lại [queue](https://docs.python.org/3/library/queue.html) và [Tkinter](https://docs.python.org/3/library/tkinter.html), thực hành bỏ/hủy job cũ mà không khóa UI.

### Nộp báo cáo và nghiệm thu

- Nộp phiếu tác vụ, phản hồi người thử theo mã, danh sách lỗi/sửa, log độ trễ và app khóa ngày 21.
- Báo cáo: số người và đặc điểm liên quan có đồng ý chia sẻ; tỷ lệ hoàn thành từng tác vụ; trung vị/p95 độ trễ kèm số lượt; các phép đo chỉ là xấp xỉ.
- **Đạt:** 5 tác vụ có kết quả; lỗi thiết bị hiển thị rõ; không mất khả năng Dừng; không tuyên bố đã kiểm chứng người khiếm thính nếu chưa thử với họ.

## 7. Tuần 4 — Đóng gói demo và diễn tập

### Các bước thực hiện

- [ ] Cùng TV4 chạy liên tục 10 phút, ghi số lượt thành công/thất bại và lỗi. Mục tiêu là ổn định có bằng chứng, không chỉ quay một lượt may mắn.
- [ ] Cùng TV1 đo test cuối; giữ riêng số liệu khoa học và video giới thiệu sản phẩm.
- [ ] Chuẩn bị demo 3–5 phút: nêu hai chế độ, một trường hợp nghe rõ, một trường hợp nhiễu, một trường hợp từ chối hoặc lỗi nguồn.
- [ ] Quay video dự phòng 2–3 phút, ghi rõ “Video ghi trước”. Nếu dùng file nghe–nhìn thay camera live, hiển thị rõ nguồn file.
- [ ] Viết hướng dẫn khởi động, chọn thiết bị, chạy mode, xử lý mất camera/micro và tắt app; thử lại trên máy demo sau khởi động mới.
- [ ] Nếu dùng kính thật, báo đúng bộ phận nào ở kính và bộ phận nào ở laptop; ghi thời lượng pin/trọng lượng chỉ khi đã đo, không suy từ thông số quảng cáo.
- [ ] Bàn giao video, ảnh giao diện, hướng dẫn và phần trải nghiệm/phần cứng trong báo cáo; tham gia 2 lượt diễn tập.

### Học thêm — khoảng 2 giờ

- 60 phút: dùng checklist và hướng dẫn của chính bạn để nhờ người khác chạy app; sửa chỗ họ không hiểu, không hướng dẫn miệng thay cho tài liệu.
- 60 phút: rà tài liệu thiết bị thật và [Tkinter](https://docs.python.org/3/library/tkinter.html) để xử lý các lỗi khởi động/đóng cửa sổ còn lại; không thêm framework mới ở tuần cuối.

### Nộp báo cáo và nghiệm thu

- Nộp app cuối, hướng dẫn sử dụng/cài đặt, log chạy 10 phút, video dự phòng, danh sách thiết bị thật và hạng mục mô phỏng.
- **Đạt:** một người ngoài nhóm triển khai có thể khởi động bằng hướng dẫn; demo không nhầm dữ liệu giả/ghi trước/live; công bố đúng giới hạn phần kính.

## 8. Ưu tiên khi thiếu thời gian

Giữ bằng mọi giá: hai chế độ đặt tên đúng, thu từng đoạn, text Việt rõ, Bắt đầu/Dừng, thông báo chưa rõ, logging và hướng dẫn chạy.

Hoãn: app điện thoại, cloud, lưu lịch sử dài, dịch đa ngôn ngữ, nhiều người nói, nhận dạng liên tục và tự chế quang học. Không dành thời gian làm giao diện đẹp trước khi luồng thật hoạt động.

Không có kính không làm mất toàn bộ dự án: trình bày thành nguyên mẫu phần mềm và thiết kế tích hợp kính. Nếu thể lệ yêu cầu phần cứng kính hoạt động, TV1 phải biết từ ngày 1 để điều chỉnh ngân sách hoặc phạm vi ngay.

## 9. Mẫu báo cáo tuần

Mục tiêu → chức năng thật/mô phỏng → commit/video → kiến thức đã học → thiết bị/cấu hình → kết quả tác vụ và độ trễ → lỗi → bàn giao TV1/TV4 → việc tuần sau. Video 1–3 phút; không đưa hình ảnh người tham gia lên báo cáo công khai khi chưa được đồng ý.
