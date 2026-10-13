# Fixture hồi quy hình học

YAML, SVG và hai PNG trong thư mục này được sao chép nguyên nội dung từ
baseline hình học v0.1 đã nghiệm thu. Đây là đầu vào kiểm thử được quản lý
cùng mã nguồn; không là đầu ra hiện hành của học liệu.

`scripts/zo_geometry_selftest.py` đọc fixture này và chỉ gọi compiler/checker
canonical trong `scripts/`. Helper ma trận tại `scripts/zo_geometry_stress.py`;
token được kiểm trực tiếp tại `assets/tex/zo-geometry-styles.tex`.
Không import compiler, helper hoặc style lịch sử từ `_audit/`.

Các SVG/PNG là đối chứng bất biến. Thay baseline cần nhiệm vụ riêng; không
tái sinh chúng để hợp thức hóa một lỗi kiểm thử.
