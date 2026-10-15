# Phạm vi mẫu web dùng chung 2027

Chỉ dẫn gốc repository tiếp tục có hiệu lực. Trước khi làm trong thư mục này, đọc `README.md`, `hop_dong_vung_doc.md`, `kiem_thu.md`.

Bản tích hợp bốn trang đã xuất bản ngày 15/10/2026. Trạng thái hiện hành
và hồ sơ khép việc lấy ở mục A của bảng điều hành 03, không lấy từ trạng
thái chờ xem của các mốc FB/DH cũ. Nguồn bộ khung vẫn chưa là Design 0.5
đã khóa. Thay đổi mới giữ quy trình kiểm và quyền phát hành theo phạm vi.

- Đây là nguồn bộ khung dùng lại, chưa là Ngôn ngữ thiết kế 0.5 đã khóa. G01, G02, Nhà và D0 đã tích hợp opt-in vào đường dựng HTML canonical; G02 theo DH_019, Nhà theo DH_017, D0 theo DH_018 với map riêng. Mỗi HTML mới chờ duyệt riêng; không suy quyền promotion/PDF/phát hành.
- Giữ G01 đã duyệt 9/10 làm đối chứng; không mở lại vòng chọn hướng hoặc ghi đè HTML đã duyệt để thử ý tưởng mới.
- Tách khung/khối chung khỏi bản đồ nhịp đọc riêng; không sao chép vùng G01 hoặc ép luồng R1 vào Nhà/D0.
- Bảng theo QD_030/07/6.1.1 của khóa, dẫn mẫu Design 0.4: đọc `profiles/course-tables.json`, dùng `scripts/zo_course_tables.py` và CSS scoped. Kiểm đủ cả bảng có liên kết/lời giải thu gọn; unknown/missing/duplicate hoặc sai JSON native phải chặn dựng. Không dùng lại blanket header-left đã bị thay hoặc coi tất cả bảng là một kiểu.
- Preview lịch sử qua `scripts/zo_web_2027_preview.py`/`scripts/zo_web_2027_check.py`. Nhà hiện hành dựng/kiểm qua `scripts/zo_web_2027_home_check.py`, lấy raw Quarto mới và adapter `zo_web_2027_home.py`; không dùng HTML docs/audit cũ làm nguồn. Luôn gọi bằng `scripts/zo_python.py`.
- Trạng thái/nhiệm vụ khóa chỉ tại `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/03_dieu_hanh_chuong_trinh.md`, đọc README/01/07 và hồ sơ liên quan trước áp dụng kit. Kit sở hữu hiện thực, không sở hữu đường học/toán hoặc roadmap khóa.
- Receipt G01 tại `hoc_lieu/r1_g01/giao_dien/web_2027_accepted.json` chứng nhận mốc FB033 lịch sử; `scripts/zo_web_2027_g01_checkpoint.py check|rebuild` chỉ đối chiếu mốc ấy. Bản sửa FB036 kiểm theo pair_check/pair_semantics và còn chờ xem, không dùng gate cũ hoặc sửa receipt để đạt PASS. Bài học/Luyện tập không xen kẽ, Nhật kí một nguồn dùng chung; chi tiết tại bộ điều hành.
- Ghi lỗi/guard và phân biệt kiểm, duyệt, tích hợp, phát hành. Nhiệm vụ prototype không tự cấp quyền sửa/render production, PDF, commit/push/phát hành hoặc nâng toàn bộ 0.5.
