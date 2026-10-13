# D0 — giao diện web dùng chung 2027

QD_030/DH_023: bảng dữ liệu/tần số, ma trận hai chiều, tra mạch và bảng dấu dùng ngôn ngữ 0.4 theo chức năng ở 07/6.1.1; binding chung `profiles/course-tables.json`. Bảng dấu native HTML thay ảnh SVG trong đầu ra opt-in từ JSON cũ, không thêm dữ kiện/toán. Bản xem mới `_audit/zo_course_tables_2026-10-11/html-current/d0-reading.html`; trạng thái chỉ ở 03; chưa duyệt hoặc phát hành.

DH_018 / QD_027, 11/10/2026. Chỉ dẫn sản xuất, không phải nội dung người học.

`../index.qmd` là nguồn nội dung. Marker `zo-web-2027-d0` chọn adapter
`scripts/zo_web_2027_d0.py` qua hook Quarto. `web_2027_layout.json` giữ bản đồ
nhịp riêng; CSS/JS cùng tên là bổ sung scoped D0. Shell/giấy/font/sáu nền/Sắc
xám/rail/drawer/footer dùng kit chung. Không chép bìa/controller R1.

CSS/script cũ còn dùng ở raw Quarto và đối chiếu lịch sử; adapter thay shell,
không đưa script di chuyển nội dung cũ vào HTML mới. Không chạy generator 6B.
Giữ năm khu vực, 24 câu, Bài 00, 25 đối chiếu, mã/ID/thứ tự, văn bản/TeX,
ngân hàng/câu thử lại riêng và tính tự nguyện. Mục lục/đối chiếu đóng mặc định;
nội dung chính mở cố định. Nhãn/heading trong giấy, hình/bảng cuộn cục bộ.
Không thêm PDF nội dung, Toàn văn, Nhật kí R1 hoặc cổng điểm vào học.

## Dựng và kiểm

Chạy từ gốc repo qua launcher:

```powershell
python scripts/zo_python.py scripts/zo_qmd.py check content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.qmd
python scripts/zo_python.py content/thpt/on_thi_toan_thpt/hoc_lieu/d0/cong_cu/kiem_chung.py
python scripts/zo_python.py scripts/zo_web_2027_d0_check.py rebuild --output _audit/<luot-moi>/source-current
```

`rebuild` dùng `zo_qmd.py render` trong cây nguồn cô lập/index riêng, không đổi
root docs/Git index. Dùng thư mục mới, không ghi đè bằng chứng. Khi được giao
dựng docs chính, dùng `zo_qmd.py render` cùng QMD/adapter, không dùng HTML audit.
`preview --html <HTML-vua-dung> --output <thu-muc-xem> --home <Home> --g01
<G01> --g02 <G02>` chỉ đổi URL đọc local. `check --html <ban-xem> --build
<source-current/build.json> --output <thu-muc-qa> --browser` kiểm toàn chuỗi,
nguồn tươi, tài sản, nhịp/đích và browser. Chọn HTML hiện hành theo bảng 03.

Nghiệm thu cũ chỉ là receipt lịch sử; HTML mới chờ chủ trì xem. Trạng thái ở
`../../../tot_nghiep_thpt/2027/_quy_trinh/03_dieu_hanh_chuong_trinh.md`.
Không PDF nội dung, Git, prepare/publish hoặc khóa Design 0.5 trong lượt này.
