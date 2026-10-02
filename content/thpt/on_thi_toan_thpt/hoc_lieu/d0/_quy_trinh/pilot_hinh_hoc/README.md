# Pilot hình học D0-R3-03

## Kiểm kê

D0 hiện có một tài sản hình học được tham chiếu trong nội dung công khai:
`hinh/hinh_hop.pdf`, tại nhiệm vụ `D0-R3-03`. Bản PNG cùng tên phục vụ preview
và kiểm chứng. Câu thử lại dùng cùng họ bài nhưng không chèn thêm hình.

## Phạm vi pilot

- giữ nguyên câu hỏi, dữ kiện, ID, caption và đường dẫn trong `index.qmd`;
- giữ (AC_1) đỏ liền, (AC) đỏ đứt và ba nhãn kích thước như tài sản lịch sử;
- dùng compiler production `scripts/zo_geometry.py`, checker
  `scripts/zo_geometry_check.py` và style `assets/tex/zo-geometry-styles.tex`;
- đầu ra pilot thay thế đúng hai tài sản `hinh/hinh_hop.pdf` và
  `hinh/hinh_hop.png`, sau khi qua kiểm tra nguồn, SVG/PDF và nghiệm thu trực quan.

Không dựng hàng loạt và không thay đổi nội dung toán trong Đợt 5.

## Kết quả kỹ thuật

- YAML qua validator và checker nhãn nghiêm ngặt, không có lỗi/cảnh báo;
- PDF pilot là vector một trang, nhúng STIX Two Text và STIX Two Math;
- HTML dùng `hinh/hinh_hop.svg` qua bộ lọc `cong_cu/d0.lua`; PDF giữ tài sản PDF vector. Checker HTML bắt buộc SVG khớp checksum tài sản canonical và từ chối nhúng trình đọc PDF;
- checker toàn chuỗi D0 và checker HTML đều đạt;
- nghiệm thu trực quan trong trang thật vẫn chờ người dùng;
- bốn biến thể PDF canonical của D0 vẫn thuộc bước sản xuất riêng, chưa được tạo
  hoặc tuyên bố hoàn tất bởi pilot này.

Lệnh dựng canonical từ gốc repository:

```text
python scripts/zo_python.py scripts/zo_geometry.py build content/thpt/on_thi_toan_thpt/hoc_lieu/d0/_quy_trinh/pilot_hinh_hoc/d0_r3_03_hinh_hop.yml content/thpt/on_thi_toan_thpt/hoc_lieu/d0/hinh/hinh_hop
```
