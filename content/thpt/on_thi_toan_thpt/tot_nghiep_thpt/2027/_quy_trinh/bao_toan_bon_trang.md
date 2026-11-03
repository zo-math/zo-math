# Bảo vệ nguồn và thành phẩm hiện hành của khóa 2027

Theo yêu cầu trực tiếp của chủ trì ngày 03/11/2026, bản R01 riêng, prototype, dự án cũ và các bản xem cũ đã nghỉ dùng. Quy định giữ chúng làm đối chiếu trước đây hết hiệu lực trong phạm vi khóa 2027. Không phục hồi hoặc đọc chúng làm đầu vào.

Nguồn duy nhất là QMD, include, dữ liệu, hình, bindings và công cụ hiện hành trong repository chính. Hướng dẫn vận hành: `scripts/zo_course_site_sources/README.md`. Trạng thái và việc tiếp theo: `03_dieu_hanh_chuong_trinh.md`.

Danh mục bảo vệ được sinh từ bản dựng hiện hành tại `ban_dang_duyet.json`, gồm nguồn, 17 trang HTML, phụ thuộc CSS/JS/phông/hình, PDF đang dùng và đường mở lại. `scripts/zo_course_site_protection.py` cập nhật danh mục sau dựng đạt. Không lấy hash hay trạng thái nghiệm thu của bộ cũ để chứng nhận bản mới.

Bộ công cụ đồ họa sản xuất dùng chung ở repository `zo_math_graphics` vẫn là phụ thuộc hiện hành, qua adapter canonical; không phải nguồn học liệu cũ.
