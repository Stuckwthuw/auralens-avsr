# TV4 — Chưa xác định họ tên — API, dữ liệu mẫu và đồng bộ

Nhánh feat/tv4-week01-contracts, base 2331e8b. Bản triển khai local ngày 16/11/2026.

## Đầu ra và cách chạy

Python 3.14.10 đã kiểm tra. Các module TV4 dùng thư viện chuẩn, không cần pip. ffprobe n9.0.2 dùng để đọc metadata. Môi trường model chung chưa pin vì chưa chạy model thật.

Chạy từ thư mục gốc repo

```sh
python -m unittest discover -s tests -v
python -m auralens.pipeline contracts/fixtures/valid.json
python -m auralens.pipeline contracts/fixtures/missing_video.json
python -m auralens.pipeline contracts/fixtures/missing_audio.json
python -m auralens.pilot_timing /duong/dan/clip.mp4 --sample-id pilot_001
```

Để ghi offset thủ công của cùng một sự kiện trong clip kiểm tra riêng, thêm --audio-event-ms và --video-event-ms. Offset bằng audio trừ video, dương nghĩa tiếng đến sau hình. Người đo cần ghi cách chọn mốc và sai số ước lượng riêng. Metadata start_time và duration có thể vắng tùy container; công cụ giữ nguyên trạng thái đó. Công cụ không chứng minh đồng bộ nội dung hoặc tự sửa độ lệch.

## Kiểm tra đã chạy

Bốn test unittest đạt, bao phủ bốn tình huống nguồn và từ chối NaN/Inf, tổng điểm sai, shape sai, lớp đảo, ID hoặc thời gian lệch, infer_ms âm, valid sai kiểu và thiếu model_version. Smoke entry point mock đạt.

Đã tạo video tổng hợp đen 32x32, 10 fps, dài 1 giây và audio im lặng mono 16 kHz ngoài Git bằng FFmpeg. ffprobe đọc được hai nguồn, không có nguồn thiếu. Hai mốc giả 200/180 ms cho offset 20 ms đúng phép trừ. Đây hoàn toàn là kiểm tra tổng hợp, chưa có số đo clip thật hoặc benchmark.

## Người nhận và phần cần xác nhận

- TV2 xác nhận hợp đồng và adapter asr_free, cung cấp clip/đầu ra thật cùng sample_id.
- TV3 xác nhận khoảng thời gian và ngữ nghĩa valid trước khi chuyển từ pilot landmarks sang kết quả phân loại.
- TV5 xác nhận đầu ra UI, hiển thị mock và thử capture cùng đồng hồ.
- TV1 cung cấp clip pilot được phép truy cập và danh sách câu c00–c09.

Chưa gửi thông điệp tới thành viên, chưa có xác nhận API, chưa có clip nhóm trong workspace, chưa chạy ASR/landmarks thật, chưa đo vỗ tay, chưa tuyển/quay hai người, chưa quay video bàn giao. Tài liệu học AV-HuBERT/ViCocktail vẫn cần thành viên đọc và ghi nhận. AI đã viết mã, tài liệu và chạy kiểm tra phần mềm, không xác nhận thay việc học hoặc thực nghiệm của thành viên.

Chưa push hoặc mở PR. Công cụ gh không có trong môi trường hiện tại. Người phụ trách dùng nhánh này để review và bổ sung tên thật trước bàn giao nhóm.

## Bàn giao chạy thử trên bản thu thật

Nhánh công việc đã cập nhật từ `main` tại `5138161`, có bản bàn giao TV2 đã merge tại `8da4dae`. Kiểm tra với Python 3.14, FFmpeg/ffprobe và các gói trực tiếp sau.

```sh
python -m venv /duong-dan/venv
/duong-dan/venv/bin/python -m pip install \
  -r auralens/vision/requirements-pilot.txt \
  faster-whisper==1.2.1 av==18.0.0 ctranslate2==4.9.0
```

Dùng tệp model Face Landmarker chính thức và cache Whisper Tiny cục bộ. Có thể tạo cache bằng lệnh sau khi có Internet.

```sh
/duong-dan/venv/bin/python -c 'from faster_whisper.utils import download_model; download_model("tiny", cache_dir="/duong-dan/models")'
```

Dùng thư mục đầu ra mới bên ngoài repo ở mỗi lượt. Xác nhận clip chỉ có một người trước khi truyền `--single-person-confirmed`. Đầu vào chỉ có tiếng có thể bỏ cờ này.

```sh
/duong-dan/venv/bin/python -m auralens.week01_real_pilot \
  --video /duong-dan/clip.mp4 --model /duong-dan/face_landmarker.task \
  --models-cache /duong-dan/models --output /duong-dan/ket-qua-moi \
  --sample-id pilot_001 --single-person-confirmed
python -m unittest discover -s tests -v
```

Đã chạy đủ nguồn và hai bản sao tách luồng bằng FFmpeg từ cùng một bản thu thật. Bản chỉ có tiếng tiếp tục chạy ASR và trả `missing_video`. Bản chỉ có hình tiếp tục trích đủ 335/335 khung và trả `missing_audio`. Cả ba ca giữ cùng mã đoạn trong trạng thái của hai nhánh. Tiến trình này chạy ASR tự do và Face Landmarker tuần tự. TV5 có thể đọc `summary.json` để kiểm tra trạng thái. Chế độ 10 câu sẽ dùng các vector điểm của TV2 và TV3 qua hợp đồng nháp.

## Ghi chú đọc tài liệu

- AV-HuBERT học biểu diễn từ âm thanh và hình ảnh bằng cách che một phần đầu vào rồi dự đoán các đơn vị ẩn. Pilot tuần 1 kiểm tra dữ liệu và hai nhánh độc lập. Tuần 2 dự kiến kết hợp điểm phân loại ở đầu ra theo kế hoạch. [Bài báo AV-HuBERT](https://arxiv.org/abs/2201.02184)
- ViCocktail xây quy trình tự động thu thập dữ liệu nghe–nhìn tiếng Việt. Clip mẫu tải được ở lượt thử của nhóm đã cắt quanh miệng. Face Landmarker cần đầu vào đủ mặt, nên clip đó chỉ được dùng thử ASR và timestamp. [Bài báo ViCocktail](https://arxiv.org/abs/2506.04635)
- `queue.Queue` cung cấp hàng đợi FIFO có khóa để chuyển dữ liệu giữa các luồng. Pilot mock đã dùng hàng đợi một phần tử làm ví dụ gửi và nhận; việc nối worker với vòng lặp giao diện thuộc tích hợp sau. [Tài liệu Python](https://docs.python.org/3/library/queue.html)

Ghi chú tóm tắt do Codex chuẩn bị. Phần học và thời lượng của thành viên chờ người thực hiện tự xác nhận.

## Nội dung chờ nhóm review

- TV2 và TV3 xác nhận thứ tự lớp, khoảng thời gian, điều kiện `valid` và lý do lỗi của mỗi nguồn.
- TV5 xác nhận các trường đầu ra, trạng thái thiếu nguồn và cùng môi trường thu dùng cho phép đo vỗ tay.
- TV1 xác nhận ánh xạ câu và tình trạng hỗ trợ thu hai người. Bằng chứng hiện có gồm một bản thu nói do người dùng gửi và một clip vỗ tay. Số người đã tuyển hoặc thu theo quy trình của nhóm chưa được xác nhận.

## Kiểm chứng chương trình TV2

Bản TV2 trên `main` đã chạy qua `FasterWhisperASR.transcribe_file` với WAV float32 mono 16 kHz. Medium, CPU int8, tiếng Việt, PyAV 18.0.0. API trả đúng `sample_id` và `mode=asr_free`. CER 11,54% (9/78) và thời gian suy luận 3774 ms trên một bản thu. [Số liệu tuần 1](../progress/week-01/TV4.md#kiểm-chứng-whisper-medium-của-tv2)
