# TV4 — Pilot dữ liệu ngoài ngày 17/11/2026

Người phụ trách chưa xác định họ tên — Kiểm tra audio/video tuần 1.

Nguồn chính thức https://huggingface.co/datasets/nguyenvulebinh/ViCocktail

Đã lấy member 0000000000.video từ data/avvn-train-000000.tar, dùng mã external_vicocktail_001. SHA256 157f239e8f254537d4435eee369036fc657843fe32e09b973f978ff45b18fcec. Dữ liệu thật từ tập train bên ngoài. Trang chính thức chưa ghi giấy phép; quyền phân phối lại chưa xác minh. Media, transcript, model và ảnh kiểm tra được giữ ngoài Git ở thư mục pilot-data cạnh checkout.

## Kết quả kiểm tra thực tế

- Video H.264 96×96, 25 fps, 300 frame, duration 12000 ms. Timestamp từng frame tăng nghiêm ngặt từ 0 đến 11960 ms.
- Audio gốc AAC mono 16 kHz, duration 12032 ms. Tách bằng FFmpeg thành WAV PCM float32 mono 16 kHz, 192512 mẫu, toàn bộ hữu hạn, peak 0.9529979.
- Hai stream bắt đầu ở 0 theo metadata. Chênh lệch độ dài 32 ms chưa chứng minh lệch nội dung. Offset nội dung chưa đo.
- Kiểm tra ảnh lấy mẫu mỗi giây cho thấy video cắt sát miệng. Không đủ mặt cho điều kiện pilot Face Landmarker hiện có của TV3. Chưa chạy landmarks.
- ASR thật bằng Faster-Whisper 1.2.1, Whisper Tiny, CPU int8, language vi, beam_size 5. Kết quả có text, status ok, infer_ms 2775.096, model_load_ms 254.874 trong lượt model đã tải về. Đây là thời gian chạy cục bộ một mẫu, chưa đo CER hoặc độ chính xác. Cấu hình Tiny do AI chọn để thử luồng đọc, khác Medium của TV2.
- PyAV 19.0.2 không nhận metadata_errors từ Faster-Whisper 1.2.1. Đã dùng FFmpeg giải mã float32 và truyền numpy array qua API transcribe hỗ trợ mảng audio. Chưa sửa mã TV2.
- Đã thử video VAVD 0sO68p2mQjw đoạn 30–40 giây; yt-dlp không có định dạng tải phù hợp. Chưa có clip mặt đầy đủ thay thế.

## Tái lập và tệp bằng chứng

Trong thư mục pilot-data cạnh repo có source.json, inspection.json, timing.json, asr.json, run_asr.py và requirements-asr.txt. Script hiện dùng đường dẫn local của máy này. Môi trường thử nằm ở /tmp/tv4-runtime, có thể bị xóa khi dọn thư mục tạm.

```sh
python -m auralens.pilot_timing ../pilot-data/0000000000.video --sample-id external_vicocktail_001
/tmp/tv4-runtime/bin/python ../pilot-data/run_asr.py
```

Đã kiểm tra smoke trên clip thật. Chưa tích hợp UI hoặc bộ phân loại 10 câu. Cần nguồn đủ mặt, quyền sử dụng xác định, đo đồng bộ nội dung và xác nhận TV2/TV3/TV5 trước nghiệm thu toàn bộ tuần 1. Chưa push GitHub. Hỗ trợ AI thực hiện tải mẫu, kiểm tra metadata, lập trình và chạy ASR; thành viên chưa xác nhận việc học hoặc tuyển/quay người.
