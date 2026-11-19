# TV3 — Hoàng Hiếu — Đo landmarks trong pilot hai người

TV3-PILOT-TWO-FACES, tuần 1. Nhánh `feat/tv3-hoang-hieu-two-person-pilot`, base `09e6b88`. Công cụ độc lập `auralens/vision/pilot_two_faces.py` nhận một video, trả JSON riêng của pilot. Mỗi frame có timestamp ms và 0–2 bộ gồm 40 điểm môi (x, y, z theo MediaPipe). Các bộ điểm được sắp từ trái sang phải theo tâm môi trong từng frame. Thứ tự này không xác định danh tính, người đang nói hay mức độ nhìn rõ môi. Không đổi hợp đồng TV4.

## Kết quả trên bốn video

Mã dưới đây là phần giờ của tên clip. Cả bốn có kích thước 2336 × 1080 và có stream âm thanh. Chỉ dùng hình cho phép đo.

- 103701 — 120/120 frame trả hai bộ điểm, timestamp 0–4149 ms.
- 103726 — 110/110 frame trả một bộ điểm, timestamp 0–3813 ms. Trong ảnh mẫu chỉ thấy người áo trắng. Không gán bộ điểm thứ hai khi người kia ở ngoài hình.
- 103739 — 113/113 frame trả hai bộ điểm, timestamp 0–3901 ms. Ở frame 12, 48 và 84, cả hai che miệng và điểm môi được vẽ lên bàn tay. Cuối clip có hạ tay.
- 103911 — 99/99 frame trả hai bộ điểm, timestamp 0–3440 ms.

Đối chiếu đủ 442 timestamp với `ffprobe` (best_effort_timestamp_time), sai lệch tối đa 0,5 ms sau khi làm tròn. Tọa độ hữu hạn. Kiểm tra trực quan ảnh lấy cách 12 frame và ảnh phủ điểm tại frame 12, 48, 84 của mỗi clip. Hai clip 103701 và 103911 đều thấy hai miệng trong các ảnh mẫu. Chưa xác định clip nhiễu bằng đánh giá âm thanh, chưa đánh dấu khoảng nói riêng theo người.

## Chạy lại

Môi trường đã chạy: Python 3.14, OpenCV 5.0.0, MediaPipe 1.2.3, Face Landmarker VIDEO với num_faces=2 và các ngưỡng mặc định. Model SHA-256 `64184e229b263107bc2b804c6625db1341ff2bb731874b0bcc2fe6544e0bc9ff`. Dùng môi trường pilot TV3 và đường dẫn video/model cục bộ. Thư mục đích cần tồn tại, ngoài Git, tên JSON mới cho mỗi lần chạy.

```powershell
python -m auralens.vision.pilot_two_faces --video 'chemin/clip.mp4' --model 'chemin/face_landmarker.task' --sample-id pilot_01 --output "$env:TEMP/pilot_01.json"
```

## Bàn giao

Bộ test repo chạy đạt 7/7 với `$env:PYTHONUTF8='1'` và `python -m unittest discover -s tests -q`. Với encoding Windows mặc định, một test ASR đọc sai dấu ở chuỗi tiếng Việt.

Hoàng Hiếu đã chọn chỉ đo landmarks tuần 1 trong khi chờ TV1 chốt split. Clip, ảnh kiểm tra, tọa độ và câu nói cá nhân ở ngoài Git. Nhãn lời nói do người quay cung cấp theo màu áo. Trong ảnh giải mã, áo trắng ở trái, áo xanh ở phải. Chưa fit model, gán c00–c09 hoặc tính chỉ số phân loại. Mỗi người chỉ có một câu nên bốn clip chưa cho phép tách ảnh hưởng của người nói khỏi khác biệt ở từ cuối.

TV1 chốt người thuộc train/dev/test và cách thu chéo cả hai câu cho mỗi người nếu tiếp tục thí nghiệm phân biệt từ cuối. TV4 có thể dùng số đo để review cách xử lý nhiều mặt, mất người và che miệng. Chưa xác minh tích hợp.
