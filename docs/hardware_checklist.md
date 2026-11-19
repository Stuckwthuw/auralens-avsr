# Bảng kiểm kê và kiểm tra phần cứng (Hardware Inventory Checklist) — Auralens AVSR

> **Dự án:** Auralens AVSR  
> **Người phụ trách:** TV5 (Ứng dụng, hiển thị phụ đề và tích hợp phần cứng)  
> **Mục tiêu:** Rà soát và kiểm kê thiết bị phần cứng, kiểm tra kết nối hiển thị và thu nhận camera/micro, quản lý chi phí/ngân sách thực tế và đưa ra quyết định phần cứng vào Ngày 7 theo kế hoạch Tuần 1.  
> **Tài liệu tham khảo luồng sử dụng:** [XRAI Platforms](https://xrai.glass/platforms/)

---

## 1. Thiết bị hiện có (Available Equipment)

| Thiết bị | Loại | Thông số | Người cho mượn | Ngày nhận | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Laptop** | Chưa điền | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| **Webcam** | Chưa điền | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| **Microphone** | Chưa điền | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| **Kính AR / Bộ hiển thị** | Chưa điền | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| *(Thiết bị khác nếu có)* | Chưa điền | Chưa điền | Chưa điền | Chưa điền | Chưa điền |

---

## 2. Kiểm tra kết nối hiển thị (Display Connection Check)

Kiểm tra đường vào hình ảnh và khả năng kết nối từ laptop xuất sang thiết bị hiển thị/kính AR:

- [ ] **HDMI output available?** (Cổng xuất HDMI có sẵn và hoạt động bình thường không?)
- [ ] **DisplayPort via USB-C?** (Cổng USB-C có hỗ trợ giao thức DisplayPort Alt Mode không?)
- [ ] **SDK or protocol for display device?** (Có SDK, thư viện hoặc giao thức truyền hình ảnh/dữ liệu chính thức cho thiết bị hiển thị không?)
- [ ] **USB-C confirmed for video output (not just data)?** (USB-C đã được kiểm chứng thực tế có hỗ trợ xuất video, không chỉ sạc hoặc truyền dữ liệu thông thường?)
- [ ] **Resolution verified on actual device?** (Độ phân giải hiển thị thực tế đã được kiểm chứng trên thiết bị thật?)
- [ ] **Vietnamese font rendering tested?** (Font tiếng Việt có dấu đã được kiểm tra hiển thị đúng, rõ ràng, không lỗi mã Unicode trên thiết bị hiển thị?)
- [ ] **Power supply and accessories needed?** (Nguồn điện cấp riêng và các cáp/adapter/phụ kiện kết nối cần thiết đã được xác định và chuẩn bị đủ?)

---

## 3. Kiểm tra Camera/Micro (Camera/Mic Check)

Kiểm tra thông số kỹ thuật và khả năng thu dữ liệu thô phục vụ pipeline nhận dạng nghe - nhìn (AVSR):

- [ ] **Camera mở và đóng đúng cách?** (Camera opens and closes properly — giải phóng tài nguyên hoàn toàn, không bị giữ tài nguyên sau khi ứng dụng đóng)
- [ ] **Độ phân giải Camera (Camera resolution):** ___
- [ ] **FPS thực tế của Camera (Camera FPS actual):** ___
- [ ] **Tần số lấy mẫu Microphone (Microphone sample rate):** ___ Hz
- [ ] **Truy cập dữ liệu thô (Raw data accessible)?** (Có thể truy cập trực tiếp khung hình raw / luồng âm thanh PCM thô từ camera và micro không?)
- [ ] **Thu đồng thời âm thanh và video (Can capture audio + video simultaneously)?** (Có thể thu cả video và audio cùng lúc mà không bị nghẽn hay lệch pha nghiêm trọng?)

---

## 4. Ngân sách và chi phí (Budget)

> **Lưu ý:** Chỉ ghi giá có nguồn và ngày cụ thể. Không coi ước tính là giá mua đã xác nhận.

| Hạng mục | Giá dự kiến | Nguồn báo giá | Ngày | Ghi chú |
| :--- | :--- | :--- | :--- | :--- |
| Cáp chuyển đổi / Adapter | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| Phụ kiện nguồn / Hub | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| Kính / Module hiển thị | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| Hạng mục phát sinh | Chưa điền | Chưa điền | Chưa điền | Chưa điền |

---

## 5. Quyết định phần cứng ngày 7 (Day 7 Hardware Decision)

Mốc chốt phương án phần cứng vào cuối tuần 1 (Ngày 7) nhằm đảm bảo tiến độ ứng dụng:

- [ ] **Thiết bị đã có và kiểm tra được** → Sử dụng cho tích hợp thực tế
- [ ] **Thiết bị đang chờ** → Ghi thời hạn bàn giao dự kiến: ___
- [ ] **Chưa có thiết bị phù hợp** → Dùng laptop, ghi phần kính là thiết kế/mô phỏng
- **Quyết định chốt (Decision field):** ___
- **Tham khảo (Reference):** [XRAI Platforms](https://xrai.glass/platforms/) để hiểu luồng sử dụng (for understanding usage flow)

---

## 6. Ghi chú

- "Không mua kính khi chưa kiểm tra giao diện kết nối"
- "USB-C có hình dạng phù hợp chưa chứng minh hỗ trợ xuất video"
- "Một module màn hình nhỏ chưa tự trở thành màn hình gần mắt; cần hệ quang học"
