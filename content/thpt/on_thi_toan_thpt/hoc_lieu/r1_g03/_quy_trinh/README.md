# R1-G03 — quản lí bản thảo và nguồn học liệu

[Mở bản thảo đang sửa](ban_thao/noi_dung.md) · [Hồ sơ phạm vi và nguồn](../../../tot_nghiep_thpt/2027/_quy_trinh/goi/R1_G03.md) · [Trạng thái và việc tiếp theo](../../../tot_nghiep_thpt/2027/_quy_trinh/03_dieu_hanh_chuong_trinh.md).

## Vị trí và vai trò

G03 nằm trong `hoc_lieu/r1_g03/`, cùng cấp G01/G02. `_quy_trinh/README.md` là điểm vào quản lí gói; `ho_so/` giữ biên nhận có phạm vi cụ thể, theo cách tổ chức hai gói trước. Vùng `ban_thao/` được thêm theo yêu cầu chủ trì để tách bản thảo khỏi nguồn sản xuất.

| Vị trí tính từ thư mục gói | Vai trò |
|---|---|
| `_quy_trinh/ban_thao/noi_dung.md` | Bản thảo nội dung duy nhất đang sửa; tiếp tục biên tập tại đây |
| `_quy_trinh/ban_thao/hinh/` | Tài nguyên độc lập của bản thảo: TeX, SVG/PDF, manifest; không là tài nguyên chính thức |
| `_quy_trinh/ho_so/` | Biên nhận và kết quả kiểm theo từng lượt; không thay nguồn nội dung hoặc bảng trạng thái 03 |
| `index.qmd` | Vị trí nguồn chính thức sau khi bản thảo được duyệt và chuyển đổi; hiện chưa tạo |

Hồ sơ [phạm vi](../../../tot_nghiep_thpt/2027/_quy_trinh/goi/R1_G03.md), [đề cương](../../../tot_nghiep_thpt/2027/_quy_trinh/goi/R1_G03_de_cuong_bien_soan.md) và [ma trận](../../../tot_nghiep_thpt/2027/_quy_trinh/goi/R1_G03_ma_tran_nhiem_vu.md) ở lớp điều hành khóa, chỉ dẫn tới nội dung trong gói. Không sao chép các tài liệu đó sang đây. Biên nhận di chuyển: [to_chuc_ban_thao_20261016.json](ho_so/to_chuc_ban_thao_20261016.json).

## Từ bản thảo đã duyệt sang QMD

Chỉ chuyển đổi sau khi chủ trì duyệt bản thảo. Khi đó đối chiếu nội dung với bản đã duyệt, tạo `index.qmd` và cấu hình gói theo [quy chuẩn QMD](../../../tot_nghiep_thpt/2027/_quy_trinh/quy_chuan_goi_qmd.md). Bản thảo đã duyệt và tài nguyên của nó được giữ riêng làm căn cứ; QMD trở thành nguồn biên soạn chính thức duy nhất sau khi chuyển đổi được kiểm và nghiệm thu. Không duy trì hai bản cùng sửa.

Tài nguyên chính thức phải được tạo từ đầu vào toán đã duyệt qua công cụ ZO Math, nhất quán với G01/G02: dữ liệu ở `du_lieu/`, nguồn hình ở `hinh/`, tài sản trình bày và binding ở `giao_dien/` theo hợp đồng đang áp dụng. Các thư mục sản xuất này chỉ tạo khi thực sự triển khai, không tạo rỗng ở giai đoạn bản thảo.

Điểm vào đồ họa hiện có là `scripts/zo_graphics.py`, gọi qua `python scripts/zo_python.py`; các nhánh `graph`, `variation`, `geometry` theo loại hình. Hình đồ thị hiện hành của G01/G02 dùng profile 0.4 và cặp SVG/PDF từ cùng nguồn. Khi chuyển đổi G03 phải kiểm lại công cụ/profile đang được áp dụng, dựng mới tài nguyên chính thức, kiểm nguồn và xem hình; không sao SVG/PDF bản thảo thành tài sản sản xuất hoặc sửa đầu ra bằng tay. Build chính thức không được đọc từ `_quy_trinh/ban_thao/`.

Vòng đời QMD dùng `scripts/zo_qmd.py`, PDF dùng `scripts/zo_pdf.py`, đều qua launcher của repository. G03 chưa có cấu hình sản xuất; README này không khẳng định các pipeline đã tích hợp hoặc cho phép render/phát hành. Không tự sao script, quota, ID hoặc trạng thái nghiệm thu của G01/G02 sang G03.

## Quy tắc tiếp tục làm việc

Nội dung, số và biểu thức toán trong bản thảo dùng LaTeX; phân số dùng `\frac`; giới hạn ghi rõ hướng; định nghĩa và định lí phải được đối chiếu tài liệu chính thức trong Nguồn và ghi vị trí. Giữ các sửa trực tiếp của chủ trì.

Trước khi tạo thêm thư mục lưu trữ, trình bày đường dẫn, mục đích, nội dung và lí do không dùng nơi hiện có; chờ chủ trì chốt. Không tự thêm bản sao hoặc kho lưu trữ song song. Trạng thái và việc tiếp theo chỉ ghi ở bảng 03 được dẫn đầu README.
