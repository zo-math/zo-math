# Áp dụng hệ nhãn R1-G01

Ngày: 10/10/2026 · Quy tắc: QD_025, kế thừa QD_023 · Trạng thái: đã áp dụng nguồn, chờ chủ trì duyệt HTML.

Tài liệu triển khai nội bộ, không phải nội dung công bố cho học sinh. Quy tắc chung có hiệu lực cho toàn bộ gói của chương trình Ôn thi Toán THPT 2027; bảng này chỉ ghi việc áp dụng riêng R1-G01. Trạng thái và việc tiếp theo thuộc bảng điều hành 03/DH_015.

## Nguồn và thẩm quyền

- `index.qmd` và các include canonical sở hữu câu chữ, toán, nhiệm vụ và lời giải.
- [Bảng áp dụng JSON](ap_dung_he_nhan.json) giữ annotations kiểm kê; không là bản thảo toán thứ hai.
- `giao_dien/he_nhan.json` nối ID nguồn với chức năng, số, tiêu đề, nhãn và đáp án hiển thị. Không tự định nghĩa quy tắc mới hoặc chép nội dung toán.
- `01_kien_truc_hoc_tap.md` và `07_quy_chuan_cau_truc_trang_nguoi_hoc.md` sở hữu hợp đồng hệ nhãn; QD_025 bổ sung Gợi mở và phạm vi toàn chương trình từ bản chủ trì đã sửa.
- Bản được áp dụng: `_audit/r1_g01_ban_chot_bien_tap_2026-10-10.md`, SHA-256 `51fe4f877b2c5e5c19d1ccf1736ff8599244ed43c8cbf257971a0c90482a5c0e`. Chỉ phần câu chữ công bố đi vào học liệu; các chỉ dẫn biên tập không đi vào trang học.

## Áp dụng đã thực hiện

| Nhóm chức năng | Nhiệm vụ | Lời giải |
|---|---:|---:|
| Khởi động | 4 | 4 |
| Gợi mở | 7 | 0 |
| Tự kiểm tra | 7 | 7 |
| Xác nhận nền | 8 | 8 |
| Xác nhận nhiệm vụ Luyện tập 08 | 1 | 1 |
| Kiểm tra | 5 | 5 |
| Ôn lại | 3 | 3 |
| Sửa lỗi | 26 | 26 |
| Luyện tập | 8 | 8 |
| Tổng | 69 | 62 |

Đánh số liên tục trong từng nhóm chức năng, không đặt lại qua chặng. Sửa lỗi: 01–09 sau Kiểm tra, 10–17 sau Luyện tập, 18–26 sau Ôn lại. Gợi mở 01–07 không mang lời giải hoặc bằng chứng đạt. Đích/ID cũ vẫn truy cập được; ID con mới chỉ bổ sung khi cần nhận diện từng nhiệm vụ.

- Cách học dùng ba nhịp: Học theo mạch chính; Hỗ trợ khi cần; Khi nào chuyển gói. Bốn hoạt động chính là Bài học → Luyện tập → Kiểm tra → Ôn lại, không xen kẽ Bài học/Luyện tập.
- Ôn nền là phần độc lập ngang cấp các phần hỗ trợ; bảy nguồn dùng chung vẫn include một lần. Sửa lỗi sau Ôn lại thuộc Sửa lỗi, không thuộc Ôn lại.
- Trang Lời giải dùng tên nhóm tương ứng; từng đáp án mang nhãn ngữ cảnh và tên/số khớp đề bài.
- Không lặp nhãn với tiêu đề đã đủ nghĩa; nhãn, tiêu đề và nội dung nằm trong cùng vùng đọc.
- QD_024 được áp dụng ở Cách học và đầu Kiểm tra: có thể vào khi đã chuẩn bị kĩ hoặc đủ tự tin, một lượt không chia đợt, tự lực; tự tin không phải bằng chứng đạt/chuyển gói.
- Bảng T01 giữ ID và chuyển thành bảng bốn hàng hỗ trợ; không còn dùng như bảng ẩn tương thích. Giữ 19 bảng, 13 bảng biến thiên, 13 đồ thị, 14 trường Nhật kí, toán và tài sản đã khóa.
- Sáu điểm LBL-G01-01–06 đã được triển khai từ bản chủ trì sửa; trạng thái triển khai không thay thế nghiệm thu HTML.

## Dựng và kiểm

Dựng bình thường đọc QMD tươi và binding canonical, không lấy HTML/audit làm nguồn. `scripts/zo_r1_g01_rebind.py` là công cụ bảo trì tường minh cho lượt di trú này; không phải phụ thuộc chạy build.

```text
python scripts/zo_python.py scripts/zo_learning_architecture.py labels --self-test --output _audit/r1_g01_ap_dung_ban_chot_2026-10-10/labels-current
python scripts/zo_python.py scripts/zo_r1_g01_labels_check.py --audit _audit/r1_g01_ap_dung_ban_chot_2026-10-10 --browser --report qa-bound-current.json
```

Bằng chứng hiện hành được lưu dưới `_audit/r1_g01_ap_dung_ban_chot_2026-10-10/`: bảo toàn ID/toán/tài sản, phép chiếu đầy đủ câu chữ nhiệm vụ và dòng điểm, 14 tình huống đường học, kiểm giao diện/điều hướng, tương thích các include dùng chung trên G02. Số kiểm và hash đầu vào lấy từ báo cáo thực chạy, không chép số lịch sử để chứng nhận bản mới.

Phân biệt đã sửa nguồn, đã kiểm, chủ trì duyệt và phát hành. Chưa đồng bộ PDF, chưa promotion `docs/`, chưa cập nhật receipt FB033, chưa biên tập nội dung riêng G02, chưa stage/commit/phát hành.
