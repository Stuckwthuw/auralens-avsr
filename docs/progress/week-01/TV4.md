# TV4 — Tuần 01: API, dữ liệu mẫu và đồng bộ

- Người phụ trách: chưa điền tên.
- Trạng thái: IN PROGRESS.
- Thời gian bắt đầu/kết thúc tuần: chưa xác định ngày bắt đầu dự án.
- Cập nhật lần cuối: 17/11/2026. Kết quả kỹ thuật và các mục chờ review được ghi bên dưới.
- Kế hoạch gốc: [phân công TV4](../../plans/04_thanh_vien_4_ket_hop_model_tich_hop.md).

> Các mục kế hoạch gồm cả phần xác nhận của nhóm. Bằng chứng chạy và trạng thái hiện tại được ghi trong từng mục.

## 1. Nhiệm vụ được giao trong tuần

- [ ] Ngày 1–2: tạo schema ở phần 2, skeleton các hàm và 3 ví dụ: đầu vào hợp lệ, mất video, mất audio. Gửi TV2/TV3/TV5 xác nhận trước khi code sâu.
- [ ] Lập cấu trúc module đơn giản: capture, audio, vision, fusion, app, evaluation; một file cấu hình chung. Không cần microservices/cloud.
- [ ] Nhận một clip pilot từ TV1; tách/đọc hai nguồn sao cho giữ cùng gốc thời gian; in log độ dài và khoảng thời gian thực.
- [ ] Cùng TV5 kiểm tra offset audio/video bằng sự kiện thấy-nghe được như vỗ tay trong clip kiểm tra riêng. Ghi sai số ước lượng; không đưa tiếng vỗ tay vào feature câu.
- [ ] Cùng TV2/TV3 chạy audio và landmarks thật trước ngày 7. Dữ liệu mock chỉ để thử giao diện, phải có nhãn mock rõ ràng.
- [ ] Hỗ trợ tuyển/quay 2 người theo TV1; giúp nhóm pin môi trường sau khi cài chạy thành công.

## 2. Công việc thực tế và trạng thái

Đã kiểm chứng hợp đồng mock và một lệnh chạy hai pilot trên bản thu thật. Các mốc chạy và số liệu được trình bày bên dưới.

## 3. Kiến thức đã học và áp dụng

Xem [ghi chú do Codex chuẩn bị](../../handoffs/tv4-week01-contracts.md#ghi-chú-đọc-tài-liệu) về AV-HuBERT, ViCocktail và Python queue. Thời lượng tự học chờ thành viên xác nhận.

## 4. Kiểm tra và số liệu

Bốn kiểm thử đơn vị đạt. Kiểm chứng đủ tiếng và hình, chỉ có tiếng, chỉ có hình bằng bản thu thật. Đo offset từ ba lần vỗ tay trên một bản thu riêng.

## 5. Vướng mắc và hỗ trợ cần thiết

Đang chờ TV2, TV3 và TV5 xác nhận API. TV1 cần xác nhận tình trạng hỗ trợ thu hai người và danh sách câu.

## 6. Bàn giao, review và tích hợp

Có [hướng dẫn chạy và danh sách mục cần review](../../handoffs/tv4-week01-contracts.md). Nội dung PR đã chuẩn bị ở máy local. GitHub chưa có thông tin đăng nhập để push nhánh.

## 7. Việc tiếp theo và thời gian thực tế

Bước tiếp theo là review với TV2, TV3, TV5 và xác nhận dữ liệu với TV1. Thời gian làm việc của thành viên chưa được cung cấp.

## Cập nhật thực hiện ngày 16/11/2026

Người phụ trách chưa xác định họ tên — API, dữ liệu mẫu và đồng bộ.

- IMPLEMENTED — bản nháp hợp đồng và config tại contracts/, validator và bốn fixture mock. Chờ TV2/TV3/TV5 xác nhận.
- VERIFIED — khung mock, bài queue gửi/nhận, bốn nhóm unit test và smoke entry point đạt trên Python 3.14.10.
- VERIFIED trong phạm vi tổng hợp — công cụ pilot_timing đọc hai luồng video/audio và tính chênh lệch hai mốc giả.
- BLOCKED — chưa có clip pilot thật được cung cấp để chạy hai nhánh và đo offset.
- PLANNED — phối hợp thu hai người, đọc tài liệu khoa học, video bàn giao và pin môi trường model sau khi chạy thật.

Chi tiết file, lệnh và bằng chứng ở [bàn giao TV4](../../handoffs/tv4-week01-contracts.md). Thời gian làm việc của thành viên chưa được cung cấp. Chưa có review độc lập hoặc tích hợp thật. Các checkbox phía trên giữ trạng thái theo toàn bộ tiêu chí nghiệm thu.

## Cập nhật ngày 17/11/2026

VERIFIED trong phạm vi pilot ngoài — đã tải một mẫu train ViCocktail, kiểm tra 300 timestamp hình, tách audio float32 mono 16 kHz và chạy ASR Tiny thật. Xem [bằng chứng và giới hạn](../../handoffs/tv4-external-pilot.md). Điều kiện thiếu clip cho phần audio đã được giải quyết bằng dữ liệu ngoài. Landmarks còn chờ clip đủ mặt, offset nội dung chưa đo, API chưa được nhóm xác nhận. Chưa hoàn thành toàn bộ tuần 1.

## Pilot Wikitongues ngày 17/11/2026

VERIFIED phần trích landmarks thật — 360/360 frame có điểm môi, mọi timestamp khớp ffprobe, thời gian 3272 ms. ASR Tiny chạy chẩn đoán có transcript trong 4041.304 ms nhưng chưa xác minh độ chính xác. Xem [bàn giao và lệnh tái lập](../../handoffs/tv4-wikitongues-pilot.md). Clip đủ mặt đã giải quyết vướng mắc đầu vào TV3 của pilot trước. Cần xử lý quy ước biên độ audio, chất lượng ASR, xác nhận API và đo đồng bộ nội dung.

Đã đối chiếu transcript Tiny với bản chép do TV4 cung cấp. CER trên một clip là 38,14% với bản chép đầy đủ và 35,42% khi bỏ cụm mở đầu chưa chắc chắn. [Cách tính và phạm vi](../../handoffs/tv4-wikitongues-pilot.md#đối-chiếu-bản-chép-asr).

## Kiểm tra hai nhánh trên bản thu mới

Chạy một lệnh với bản thu người dùng cung cấp, mã `local_recording_001`, dài 5,589 giây, 1920×1080. Lệnh đọc metadata, giải mã audio thành mono float32 16 kHz, chạy ASR và Face Landmarker tuần tự, kiểm tra hai đầu ra có cùng mã đoạn.

- Face Landmarker của TV3 tìm được điểm môi ở 335/335 khung hình, thời gian xử lý 3580 ms. Timestamp tăng từ 0 đến 5564 ms theo gốc thời gian của OpenCV. So với timestamp ffprobe đã trừ mốc khung đầu, sai khác tối đa 0,5 ms.
- Whisper Tiny CPU int8 dùng tiếng Việt, beam size 5 và ngưỡng bỏ qua mặc định. Lượt chạy trả văn bản trong 424 ms sau khi nạp mô hình. Đối chiếu bản chép do người dùng cung cấp, CER trên bản thu này là **30,77% (24/78 ký tự)**. Cách tính giữ dấu tiếng Việt, chuyển chữ thường, bỏ dấu câu, gộp và tính khoảng trắng giữa các từ. Dữ liệu đối chiếu lưu trong `asr-evaluation.json` ngoài repo.
- Metadata ghi luồng hình bắt đầu ở 2,5 ms và luồng tiếng ở 0 ms. Phép đo độ lệch nội dung cần clip vỗ tay bổ sung.
- Bằng chứng lưu tại `pilot-data/local-recording-001/` ngoài repo. Kết quả Wikitongues và CER của clip trước được lưu riêng.

Lệnh tái lập từ thư mục repo, dùng thư mục đầu ra mới ở mỗi lần chạy. Lượt chạy đã dùng môi trường pilot cục bộ, model Face Landmarker đã tải và cache Whisper Tiny.

```sh
MPLCONFIGDIR=/tmp/tv4-mpl /tmp/tv4-runtime/bin/python -m auralens.week01_real_pilot \
  --video /duong-dan/ban-thu.mp4 \
  --model ../pilot-data/face_landmarker.task --models-cache ../pilot-data/models \
  --output ../pilot-data/local-recording-rerun --sample-id local_recording_001 \
  --single-person-confirmed
```

Mốc tích hợp này xác minh một lệnh gọi hai pilot. Các mục nghiệm thu còn lại gồm chuẩn ASR của TV2, xác nhận API, xử lý thiếu nguồn trên luồng thật và kết nối UI. Phép đo độ lệch trên clip vỗ tay được ghi ở mục bên dưới.

### So sánh mô hình ASR trên bản thu mới

Cùng bản thu `local_recording_001`, cùng bản chép tham chiếu và cách tính CER. Ba lượt dùng Faster-Whisper trên CPU int8, tiếng Việt, beam size 5. Bản chép chỉ dùng để chấm sau suy luận. Thời gian xử lý tính sau khi nạp mô hình, mỗi cấu hình chạy một lượt.

| Mô hình | Số thao tác trên 78 ký tự | CER | Thời gian xử lý |
|---|---:|---:|---:|
| Tiny | 24 | 30,77% | 424 ms |
| Base | 23 | 29,49% | 542 ms |
| Small | 17 | 21,79% | 1503 ms |

Small giảm 7 thao tác so với Tiny, tương ứng 8,97 điểm phần trăm tính trước khi làm tròn. Small nhận đúng cụm “kiểm tra”, vẫn nhầm “thành viên thứ tư” và từ “độ”. Kết quả áp dụng cho một clip 5,589 giây. Nhật ký JSON và script so sánh nằm trong `pilot-data/local-recording-001/` ngoài repo. Cấu hình mặc định của luồng pilot hiện dùng Tiny.


### Kiểm tra đồng bộ bằng clip vỗ tay ngày 17/11/2026

Đã đo ba lần vỗ trong bản thu `clap_sync_001`, dài 6,112 giây. Video 1920×1080 ở khoảng 60 khung hình/giây, audio 48 kHz. Clip được dùng riêng cho phép kiểm tra đồng bộ.

| Lần vỗ | Khoảng hai tay chạm nhau (ms) | Tiếng vỗ bắt đầu (ms) | Tiếng trễ hơn hình ước tính (ms) |
|---|---:|---:|---:|
| 1 | 799,6–832,9 | 881 | +64,8 |
| 2 | 2265,5–2315,5 | 2371 | +80,5 |
| 3 | 3748,2–3798,2 | 3857 | +83,8 |

Trung bình ba lần, tiếng trễ hơn hình khoảng **76 ms**. Khoảng ước lượng cho trung bình là **54–100 ms**, xấp xỉ ±23 ms, dựa trên khoảng giữa các khung hình và độ phân giải 1 ms của bước dò tiếng vỗ.

Lấy timestamp từng khung từ ffprobe. Với mỗi lần vỗ, khoanh khoảng từ khung cuối còn thấy hai tay tách tới khung thấy hai tay chạm hoặc chồng rõ, rồi lấy trung điểm để ước lượng mốc hình. Khung hình nhòe làm khoảng này rộng hơn một khung. Mốc tiếng là đầu của hai cửa sổ 1 ms liên tiếp có đỉnh biên độ tuyệt đối từ 0,10 trở lên, dò trên audio mono đã giải mã và cộng mốc audio 11 ms từ timestamp gốc. Quy ước độ lệch bằng mốc tiếng trừ mốc hình. Khoảng trên phản ánh cách chọn mốc, chưa tính các sai số khác như thời gian truyền âm.

Script tái lập và dữ liệu đo nằm ngoài repo tại `pilot-data/clap-sync-001/`. Kết quả áp dụng cho bản thu này. Tên thiết bị, ứng dụng quay và cấu hình thu của nhóm chưa được xác nhận.


### Kiểm tra trước bàn giao

Đã cập nhật nhánh từ `main` tại `5138161` và chạy lại pilot trên cùng một bản thu. Hai bản sao thiếu nguồn được tách bằng FFmpeg, giữ dữ liệu gốc của luồng còn lại.

| Đầu vào | Kết quả âm thanh | Kết quả hình ảnh |
|---|---|---|
| Đủ tiếng và hình | ASR có văn bản | 335/335 khung có điểm môi |
| Chỉ có tiếng | ASR có văn bản | `invalid / missing_video` |
| Chỉ có hình | `invalid / missing_audio` | 335/335 khung có điểm môi |

Cả ba ca đã đối chiếu `sample_id` giữa hai đầu ra. Video minh chứng 1 phút 21 giây và log chạy thật lưu ngoài Git tại `pilot-data/week01-validation/`. Video là bản trình bày số liệu do Codex dựng, có chữ tiếng Việt và không có giọng đọc. Bản ghi mặt, tiếng và văn bản chép được giữ ngoài repo.

### Kiểm chứng Whisper Medium của TV2

Đã gọi `FasterWhisperASR.transcribe_file` từ mã TV2 đã merge trên `main`. Đầu vào là WAV mono float32 16 kHz tách từ cùng bản thu `local_recording_001`. Dùng cấu hình mặc định của TV2 gồm Medium, CPU int8, tiếng Việt và PyAV 18.0.0 theo bản bàn giao.

Kết quả có 9 thao tác trên 78 ký tự tham chiếu, **CER 11,54%**, thời gian suy luận 3774 ms và thời gian nạp mô hình từ cache 1316 ms. Bản chép và cách chuẩn hóa giữ như ba lượt trước. Medium được chạy qua hàm đọc WAV của TV2, trong khi Tiny, Base và Small nhận mảng audio qua FFmpeg. Đây là phép kiểm tra một clip giữa các cấu hình pilot. Nhật ký và script lưu tại `pilot-data/week01-validation/tv2-medium-evaluation.json` và `run_tv2.py`.

### Sau review PR #8

Đã kiểm tra lỗi độc lập của hai nhánh trên bản thu có đủ tiếng và hình. Khi cache Whisper vắng, ASR báo `error / audio_processing_failed`, còn Face Landmarker trả điểm môi ở 335/335 khung. Khi tệp Face Landmarker vắng, nhánh hình báo `error / video_processing_failed`, còn ASR vẫn trả văn bản. Cả hai ca xuất `summary.json`.

Bản chỉ có hình trả `invalid / missing_audio` và đủ bảy trường ASR. Bản nháp dùng `model_version=null` và `infer_ms=null` khi không có kết quả suy luận, chờ TV5 xác nhận. Bảy kiểm thử đơn vị đạt, gồm ba ca hồi quy cho hai nhánh lỗi và cấu trúc kết quả khi thiếu tiếng. [Bình luận review](https://github.com/Stuckwthuw/auralens-avsr/pull/8#issuecomment-6943481678)
