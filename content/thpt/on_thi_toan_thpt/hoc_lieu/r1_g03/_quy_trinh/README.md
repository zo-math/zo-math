# R1-G03 — quản lí bản thảo và nguồn học liệu

**GRAPH-G03-02 — sửa đủ năm ảnh còn lệch cỡ, 18/10/2026.** Cả 11 ảnh đã dùng cùng thành phần hiển thị; sáu ảnh cũ giữ cỡ. [Hồ sơ và bản xem](ho_so/dong_bo_nam_hinh_20261018.md). Nguồn QMD/TEX/SVG/PDF không đổi; chưa chủ trì duyệt HTML sửa hoặc xuất bản lại.


**Nhãn cấp chứa — ứng viên sau phát hành, 17/10/2026.** Đã đồng bộ theo chỉ thị chủ trì; [HTML mới và hồ sơ](ho_so/dong_bo_nhan_20261017.md). Nguồn QMD/hình/PDF giữ nguyên. Chưa xuất bản lại hoặc dựng PDF; các xác nhận phát hành/CURRENT bên dưới thuộc bộ đã phát hành trước lượt nhãn này. Chủ trì giao commit mốc nguồn, không phải nghiệm thu HTML hoặc phát hành.


**Phát hành được giao — 17/10/2026.** Chủ trì yêu cầu xuất bản ba gói.
Đã dựng từ nguồn hiện hành đủ tám PDF mỗi gói, mỗi bản đạt 17/17 kiểm kỹ thuật
và provenance CURRENT. Hồ sơ: [PDF đợt này](ho_so/pdf_release_20261017.json).
Các mốc chờ PDF bên dưới là lịch sử; trạng thái phát hành thực tế lấy ở bảng 03.

[Mở nguồn QMD](../index.qmd) · [Bản thảo tham chiếu](ban_thao/noi_dung.md) · [Hồ sơ phạm vi và nguồn](../../../tot_nghiep_thpt/2027/_quy_trinh/goi/R1_G03.md) · [Trạng thái và việc tiếp theo](../../../tot_nghiep_thpt/2027/_quy_trinh/03_dieu_hanh_chuong_trinh.md).

Khi tiếp tục biên tập/rà bản thảo, tự nạp hai mẫu theo [02/1.4](../../../tot_nghiep_thpt/2027/_quy_trinh/02_quy_trinh_va_nghiem_thu.md#ap-dung-mau-ban-thao). [Kết quả áp dụng mẫu 1.0](ho_so/bang_kiem_ban_thao_20261016.md) giữ bằng chứng theo phiên bản; trạng thái và phần được hoãn vẫn do 03 sở hữu.

## Vị trí và vai trò

G03 nằm trong `hoc_lieu/r1_g03/`, cùng cấp G01/G02. `_quy_trinh/README.md` là điểm vào quản lí gói; `ho_so/` giữ biên nhận có phạm vi cụ thể, theo cách tổ chức hai gói trước. Vùng `ban_thao/` được thêm theo yêu cầu chủ trì để tách bản thảo khỏi nguồn sản xuất.

| Vị trí tính từ thư mục gói | Vai trò |
|---|---|
| `_quy_trinh/ban_thao/noi_dung.md` | Bản 0.8 được giữ nguyên làm căn cứ chuyển đổi; không sửa song song với QMD |
| `_quy_trinh/ban_thao/noi_dung.pdf` nếu có | Bản xuất để đọc tại một thời điểm; phải đối chiếu phiên bản với Markdown, không là nguồn sửa hoặc PDF chính thức. Tình trạng hiện hành xem bảng 03 |
| `_quy_trinh/ban_thao/hinh/` | Tài nguyên độc lập của bản thảo: TeX, SVG/PDF, manifest; không là tài nguyên chính thức |
| `_quy_trinh/ho_so/` | Biên nhận và kết quả kiểm theo từng lượt; không thay nguồn nội dung hoặc bảng trạng thái 03 |
| `index.qmd` | Nguồn đang biên tập của ứng viên học liệu; HTML chờ chủ trì duyệt |

Hồ sơ [phạm vi](../../../tot_nghiep_thpt/2027/_quy_trinh/goi/R1_G03.md), [đề cương](../../../tot_nghiep_thpt/2027/_quy_trinh/goi/R1_G03_de_cuong_bien_soan.md) và [ma trận](../../../tot_nghiep_thpt/2027/_quy_trinh/goi/R1_G03_ma_tran_nhiem_vu.md) ở lớp điều hành khóa, chỉ dẫn tới nội dung trong gói. Không sao chép các tài liệu đó sang đây. Biên nhận di chuyển: [to_chuc_ban_thao_20261016.json](ho_so/to_chuc_ban_thao_20261016.json).

## Từ bản thảo đã duyệt sang QMD

Chỉ chuyển đổi sau khi chủ trì duyệt bản thảo. Khi đó đối chiếu nội dung với bản đã duyệt, tạo `index.qmd` và cấu hình gói theo [quy chuẩn QMD](../../../tot_nghiep_thpt/2027/_quy_trinh/quy_chuan_goi_qmd.md). Bản thảo đã duyệt và tài nguyên của nó được giữ riêng làm căn cứ; QMD trở thành nguồn biên soạn chính thức duy nhất sau khi chuyển đổi được kiểm và nghiệm thu. Không duy trì hai bản cùng sửa.

Tài nguyên chính thức phải được tạo từ đầu vào toán đã duyệt qua công cụ ZO Math, nhất quán với G01/G02: dữ liệu ở `du_lieu/`, nguồn hình ở `hinh/`, tài sản trình bày và binding ở `giao_dien/` theo hợp đồng đang áp dụng. Các thư mục sản xuất này chỉ tạo khi thực sự triển khai, không tạo rỗng ở giai đoạn bản thảo.

Điểm vào đồ họa hiện có là `scripts/zo_graphics.py`, gọi qua `python scripts/zo_python.py`; các nhánh `graph`, `variation`, `geometry` theo loại hình. Hình đồ thị hiện hành của G01/G02 dùng profile 0.4 và cặp SVG/PDF từ cùng nguồn. Khi chuyển đổi G03 phải kiểm lại công cụ/profile đang được áp dụng, dựng mới tài nguyên chính thức, kiểm nguồn và xem hình; không sao SVG/PDF bản thảo thành tài sản sản xuất hoặc sửa đầu ra bằng tay. Build chính thức không được đọc từ `_quy_trinh/ban_thao/`.

Vòng đời QMD dùng `scripts/zo_qmd.py`, PDF dùng `scripts/zo_pdf.py`, đều qua launcher của repository. G03 đã có cấu hình QMD cục bộ, hồ sơ index.yml, manifest kiến trúc và binding; xem hướng dẫn dựng ứng viên dưới đây. Việc tích hợp không tự cho phép PDF hoặc phát hành. Không tự sao script, quota, ID hoặc trạng thái nghiệm thu của G01/G02 sang G03.

## Quy tắc tiếp tục làm việc

Nội dung, số và biểu thức toán trong bản thảo dùng LaTeX; phân số dùng `\frac`; giới hạn ghi rõ hướng; định nghĩa và định lí phải được đối chiếu tài liệu chính thức trong Nguồn và ghi vị trí. Giữ các sửa trực tiếp của chủ trì. Chính văn dùng tên nội dung thay cho mã quản lí theo [07, mục Hệ nhãn và mục lục](../../../tot_nghiep_thpt/2027/_quy_trinh/07_quy_chuan_cau_truc_trang_nguoi_hoc.md); mã chỉ giữ ở ID, đường dẫn và hồ sơ nội bộ.

Trước khi tạo thêm thư mục lưu trữ, trình bày đường dẫn, mục đích, nội dung và lí do không dùng nơi hiện có; chờ chủ trì chốt. Không tự thêm bản sao hoặc kho lưu trữ song song. Trạng thái và việc tiếp theo chỉ ghi ở bảng 03 được dẫn đầu README.

## Dựng và kiểm ứng viên HTML

Chủ trì đã giao chuyển sang nguồn và dựng tài nguyên bằng lời “OK. Tiến hành.” ngày 16/10/2026. Nguồn biên tập hiện tại là `index.qmd`; giữ nguyên Markdown 0.8 và tài nguyên nháp làm căn cứ. HTML là ứng viên chờ duyệt, không là bản đã nghiệm thu/phát hành. Hồ sơ chuyển đổi: [chuyen_qmd_20261016.json](ho_so/chuyen_qmd_20261016.json).

- Đầu vào hình: `du_lieu/hinh_do_thi.json` và `hinh/*.tex`; đầu ra mới qua ZO Math graph 0.4 tại `giao_dien/assets/figures_0_4/`. `giao_dien/hinh_manifest.json` khóa ba dấu nguồn/SVG/PDF; khi đổi hình phải dựng, kiểm và xem lại rồi lập dấu mới, không sửa SVG/PDF bằng tay.
- `giao_dien/he_nhan.json` sở hữu ánh xạ nhiệm vụ/ví dụ của gói; nguồn QMD khai vai trò, số và ID. Manifest kiến trúc ở `_quy_trinh/kien_truc_hoc_tap.yml`. Ba đơn vị nền đã có trong nội dung được đăng ký vào danh mục chung; không ép dùng tên hoặc số bài của G01/G02.
- Bộ ghép `scripts/zo_web_2027_g03.py` nối vào post-render chung, dùng nguyên kit CSS/JS hiện hành; không đọc bản thảo, HTML lịch sử hoặc `_audit` để sinh nội dung. Bản xem nằm trong bản sao nguồn cô lập; nguồn và website hiện hành giữ riêng.
- Kiểm nguồn bằng `python scripts/zo_python.py -B scripts/zo_qmd.py check content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g03/index.qmd`. Khi dựng bản nháp trong bản sao cô lập, đặt `QUARTO_PROFILE=on-thi-preview` cho đúng tiến trình rồi dùng `zo_qmd.py render` với `--html-only`; giữ `draft: true`. Không đổi cờ thành đã phát hành chỉ để xem được trang.
- Kiểm đầu ra bằng `scripts/zo_web_2027_g03_check.py <HTML> --output-root <gốc đầu ra>`, qua launcher. Bộ kiểm đối chiếu toán với bản thảo cố định, đích nguồn/ảnh, cặp đề–lời giải, vai trò, bảng và điểm giao hệ trục theo khung nhìn; không thay phản biện toán hoặc xem trực quan.

Việc tiếp theo và các giới hạn nghiệm thu chỉ do bảng 03 sở hữu. Không dựng PDF học liệu trước khi HTML được duyệt và nhiệm vụ PDF được giao.

## Áp dụng nhãn QD_025

G03 dùng `giao_dien/he_nhan.json` với `display_contract: qd025-display-v1` và bộ gán/kiểm `scripts/zo_course_labels.py`; mẫu hiển thị đọc từ danh mục chung, quy tắc tại 07/6.2, bước bắt buộc tại 02/2.4. Binding bao phủ nhiệm vụ/đáp án, chặng/lượt/nơi phát hiện, câu xác nhận nền, điểm dừng, kiến thức và ví dụ. Nhãn lặp loại đã rõ trong tiêu đề được lược bỏ đúng quy tắc; không suy một loại nội dung từ tên để tạo nhãn.

Biên nhận chuyển đổi ban đầu giữ nguyên như lịch sử; phần nhãn thiếu và ứng viên HTML mới được tiếp quản bằng [ho_so/ap_dung_nhan_20261016.json](ho_so/ap_dung_nhan_20261016.json). Sau này mọi lần dựng lại đều qua cổng nguồn và cổng nhãn HTML, không chỉ dựa vào sự ghi nhớ của agent. Chỉ bảng 03 ghi trạng thái/việc tiếp.

## Bìa riêng của gói

Nguồn `hinh/bia_tiem_can.tex`, đầu ra `giao_dien/assets/figures_0_4/bia_tiem_can.svg`
và PDF vector cùng tên. Dựng qua `zo_graphics.py graph` với `--style 0.4
--surface transparent-light --force --check`; không nền toàn ảnh hoặc nền
nhãn. Công thức ở đầu nhánh, chừa khoảng cách với đường cong. Adapter G03
đưa SVG vào `assets/g03-cover.svg` riêng, không đổi bìa dùng chung.
