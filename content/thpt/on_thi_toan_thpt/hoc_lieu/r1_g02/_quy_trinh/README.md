# R1-G02 — gói học liệu canonical đã nghiệm thu

`index.qmd` là nguồn biên soạn canonical của gói sau khi nội dung từ bản thảo
HTML được chuyển đổi và đối chiếu. Nội dung, HTML và hệ PDF đã được nghiệm thu;
trạng thái xuất bản vẫn là `pending` cho đến khi quy trình website hoàn tất.

Nguồn đầu vào chỉ đọc:

```text
E:\zo_math_ca_nhan\zo_math_on_thi_toan_thpt\R1-G02\ZO_Math_R1-G02_ban_thao_noi_dung_v0.1_04.html
```

SHA-256 của nguồn: `7ee929aa7d2473d1b96f6136e9a93e8d94974b58bb3e01003a3aa896bd011f78`.

Không sửa ngược bản HTML nguồn. Mọi thay đổi tiếp theo của học liệu được thực
hiện trong `index.qmd` và tài sản canonical của gói. HTML/PDF là đầu ra sinh.

R1-G01 là baseline trình bày và vận hành đã nghiệm thu; không sao chép nội dung,
ID hoặc các hằng số kiểm định riêng của R1-G01 sang gói này.

Kiến trúc nội dung đích đã được chủ dự án duyệt và khóa tại
[`ma_tran_kien_truc_noi_dung.md`](ma_tran_kien_truc_noi_dung.md). Tệp này là
căn cứ cho lượt tái cấu trúc `index.qmd`; không suy kiến trúc từ bản render tạm.

Bước 2 đã hoàn tất: ghi chú hiệu đính, truy nguyên và lịch sử rà soát được bảo
toàn tại [`ho_so/lich_su_ban_thao_v0_1.md`](ho_so/lich_su_ban_thao_v0_1.md),
không còn nằm trong nội dung dành cho người học. `index.qmd` chỉ giữ phần nguồn
đối chiếu công khai, ngắn gọn.

Hệ thành phần học liệu dùng hợp đồng canonical của chuyên mục. CSS và phép
chuẩn hóa AST dùng chung lần lượt nằm tại
`assets/css/_zo_learning_components.scss` và
`assets/lua/zo_learning_components.lua`; adapter của gói chỉ ánh xạ các lớp
chuyển tiếp trong nguồn R1-G02. Bốn khối gợi ý là `hint`, không được tính là
`guidance`. Kiểm kê nguồn riêng của gói chạy bằng:

```text
python scripts/zo_python.py content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02/cong_cu/kiem_chung_thanh_phan.py
```

Baseline PDF canonical của R1-G02 được chủ dự án nghiệm thu thị giác ngày
2026-09-30 và chốt ở Pha 6C với ma trận số trang: `full` 26, `student` 17,
`bai_hoc` 10, `luyen_tap` 6, `kiem_tra` 4, `sua_loi` 5, `on_lai` 3 và
`loi_giai` 10. Checker phải so sánh toàn bộ ma trận này và metadata hai thẻ tải
phải ghi đúng 17/26 trang; không nới thành điều kiện chỉ lớn hơn 0. Thay đổi nguồn
thuộc fingerprint PDF phải dựng lại đủ biến thể bị `STALE` và đưa manifest
provenance về `CURRENT`; không sửa receipt hoặc manifest bằng tay.
