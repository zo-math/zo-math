# AGENTS.md — 100+ Bài toán thực tế

Tệp này áp dụng cho toàn bộ thư mục `100_bai_toan_thuc_te/`.

## 1. Thứ tự thẩm quyền

1. yêu cầu trực tiếp của người dùng;
2. `AGENTS.md` ở gốc repository;
3. tệp này;
4. `_quy_trinh/cau_hinh_san_xuat_qmd.yml`;
5. `_quy_trinh/quy_chuan_noi_dung_bai_toan_thuc_te.md`;
6. hồ sơ riêng của từng bài.

Khi hai nguồn cùng cấp mâu thuẫn và yêu cầu hiện tại chưa giải quyết, phải dừng và hỏi người dùng.

## 2. Phạm vi dự án

Dự án xây dựng các bài toán thực tế theo chu trình:

- xác định bối cảnh và dữ kiện;
- chọn đại lượng, đơn vị và giả định;
- xây dựng mô hình toán học;
- giải quyết trong mô hình;
- kiểm tra và diễn giải kết quả trở lại bối cảnh.

Không áp dụng các trường, thẻ hoặc quy tắc riêng của dự án 100+ Hàm số nếu cấu hình dự án này không khai báo.

## 3. Quy tắc vận hành

- Mỗi bài trong `core/` phải có hồ sơ cùng tên trong `_quy_trinh/ho_so/`.
- Dùng checker thống nhất: `python scripts/zo_python.py scripts/zo_check_repo.py ...`.
- Không thay đổi trạng thái xuất bản sang `published` và không đặt xác nhận xuất bản thành `true` nếu người dùng chưa xác nhận rõ.
- Không sửa tệp ngoài phạm vi nhiệm vụ.
- Không dùng `git add .`; chỉ stage các tệp đã được kiểm tra và được người dùng cho phép.
- Kiểm định tự động không thay thế việc người đọc kiểm tra dữ kiện, giả định, đơn vị, tính hợp lí của mô hình và ý nghĩa kết quả.
