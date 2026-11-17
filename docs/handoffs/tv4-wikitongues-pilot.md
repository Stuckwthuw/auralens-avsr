# TV4 — Pilot Wikitongues ngày 17/11/2026

Người phụ trách chưa xác định họ tên — Kiểm tra audio và landmarks trên cùng clip.

Nguồn WIKITONGUES: Đức speaking Vietnamese, https://www.youtube.com/watch?v=z_cAYz0Q5DI . Nguồn ghi CC BY-NC 4.0; ghi công Wikitongues và Đức. Đoạn yêu cầu 20–35 giây, tải theo keyframe rồi chuyển H.264/AAC dài 15 giây, vì vậy mốc gốc xấp xỉ. File local external_wikitongues_001 có 1280×720, 24 fps. Các ảnh lấy mẫu cách 250 ms cho thấy một người, đủ mặt và miệng không che. Audio tải từ track được YouTube đánh dấu original, dù metadata ngôn ngữ ghi en-US; ASR tự phát hiện vi.

## Kết quả thật

- Hai luồng có start_time 0, duration 15 giây. 360 timestamp hình tăng nghiêm ngặt từ 0 đến 14958 ms.
- Giải mã audio bằng FFmpeg về mono 16 kHz float32 cho 240000 mẫu hữu hạn. Peak 1.32753 vượt 1 sau giải mã/resample. Đã giữ và ghi nhận giá trị thực; cần thống nhất chuẩn hóa biên độ với TV2 trước tích hợp.
- MediaPipe 1.2.3 / OpenCV 5.0.0 chạy nguyên script TV3, model chính thức Face Landmarker. 360/360 frame có landmarks, processing_ms 3272. Tất cả timestamp JSON khớp ffprobe. Ảnh môi ở giây 5 đã được xem, điểm nằm trên vùng môi. Đây là tỷ lệ tìm được landmarks, chưa đo chất lượng phân loại.
- Faster-Whisper 1.2.1 / Tiny CPU int8 trả rỗng ở cấu hình phát hiện tự động. Chạy chẩn đoán language=vi, beam_size=5, no_speech_threshold=None trả transcript trong 4041.304 ms. no_speech_prob 0.67163, cao hơn ngưỡng bỏ qua thông thường. Văn bản có nhiều cụm thiếu tự nhiên, chưa có bản chép chuẩn để tính CER. Thay ngưỡng chỉ là thử chẩn đoán, chưa chọn cấu hình production hoặc thay thế Medium của TV2.
- ASR và vision dùng cùng sample_id và cùng file 15 giây, chạy độc lập tuần tự. Chưa có UI, bộ phân loại 10 câu hoặc phép đo độ lệch nội dung. Metadata cùng mốc 0 chưa chứng minh lip-sync.
- Lần chạy MediaPipe trong sandbox treo ở import; lần retry ngoài sandbox với timeout 60 giây đã hoàn thành. Tiến trình treo cũ đã dừng.

## Tái lập

Chạy từ repo, môi trường đã cài ở /tmp/tv4-runtime. requirements-wikitongues.txt bên ngoài repo lưu pip freeze thực tế. Model lấy từ https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task . Mã model và clip có checksum trong wikitongues-summary.json.

```sh
python -m auralens.pilot_timing ../pilot-data/wikitongues-duc-pilot.mp4 --sample-id external_wikitongues_001
/tmp/tv4-runtime/bin/python ../pilot-data/run_wikitongues.py
MPLCONFIGDIR=/tmp/tv4-mpl /tmp/tv4-runtime/bin/python -m auralens.vision.pilot_landmarks --video ../pilot-data/wikitongues-duc-pilot.mp4 --model ../pilot-data/face_landmarker.task --output ../pilot-data/wikitongues-vision-retry --sample-id external_wikitongues_001 --single-person-confirmed
```

Dữ liệu và transcript ở pilot-data cạnh checkout, ngoài Git. wikitongues-asr.json, wikitongues-timing.json, wikitongues-summary.json và wikitongues-vision-retry/pilot_landmarks.json là bằng chứng local. Chưa push GitHub. Tuần 1 còn cần API được TV2/TV3/TV5 xác nhận, clip đồng bộ thiết bị có sự kiện kiểm tra, quay dữ liệu theo TV1 và video bàn giao. AI thực hiện chạy phần mềm, chưa xác nhận thay công việc của thành viên.

## Đối chiếu bản chép ASR

TV4 cung cấp bản chép tham chiếu cho clip 15 giây. So với đầu ra đã lưu của lượt Faster-Whisper Tiny chạy chẩn đoán, CER là **38,14% (82/215)** với bản chép nguyên văn. Khi bỏ cụm mở đầu 23 ký tự kể cả khoảng trắng kế tiếp vì chưa rõ cụm đó có thuộc lời thoại, CER là **35,42% (68/192)**. Hai phép tính dùng cùng đầu ra ASR.

CER bằng số thao tác thêm, xóa hoặc thay ký tự tối thiểu, chia cho số ký tự tham chiếu. Chuẩn hóa Unicode NFC, chuyển chữ thường, giữ dấu tiếng Việt, bỏ dấu câu, gộp khoảng trắng và tính khoảng trắng giữa các từ. Bản chép đầy đủ và số liệu lưu trong `pilot-data/wikitongues-asr-evaluation.json` ngoài repo. Kết quả chỉ áp dụng cho một clip và cấu hình Tiny chẩn đoán đã ghi ở trên.
