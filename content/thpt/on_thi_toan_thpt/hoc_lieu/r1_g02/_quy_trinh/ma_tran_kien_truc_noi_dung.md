# R1-G02 — ma trận kiến trúc nội dung đích

## 1. Phạm vi và trạng thái

Tài liệu này khóa kiến trúc đích cho lượt chuyển R1-G02 từ bản thảo HTML sang gói QMD canonical. Đây là tài liệu điều khiển nội bộ, không phải nội dung dành cho người học và không được render hoặc xuất bản.

Nguồn nội dung được bảo toàn:

```text
E:\zo_math_ca_nhan\zo_math_on_thi_toan_thpt\R1-G02\ZO_Math_R1-G02_ban_thao_noi_dung_v0.1_04.html
SHA-256: 7ee929aa7d2473d1b96f6136e9a93e8d94974b58bb3e01003a3aa896bd011f78
```

R1-G01 v1.2 là baseline canonical về tổ chức học liệu, giao diện, điều hướng, bảng, hình, liên kết lời giải và phân tách HTML/PDF. Ma trận này không thay đổi nội dung toán học, đáp số, mục tiêu M01–M04 hoặc dữ kiện nhiệm vụ của R1-G02.

Trạng thái ma trận: **đã khóa theo chỉ thị của chủ dự án ngày 2026-09-28**.

## 2. Bất biến chuyển đổi

- `index.qmd` là nguồn văn bản canonical duy nhất.
- Giữ nguyên nội dung toán học, dữ kiện, đáp số và mã nhiệm vụ hiện có.
- Không để lời giải nằm trong phần Luyện tập, Kiểm tra hoặc Sửa lỗi.
- Mỗi nhiệm vụ có lời giải phải có liên kết hai chiều bằng ID ổn định.
- Hồ sơ hiệu đính, truy nguyên và lịch sử bản thảo chuyển vào `_quy_trinh`;
  phần người học chỉ giữ nguồn đối chiếu cần thiết.
- Công thức dùng TeX QMD; không giữ span `.math` làm nguồn canonical.
- BBT và đồ thị không dùng HTML thô, data URI hoặc hình raster làm nguồn.
- HTML dùng SVG; PDF sau này dùng PDF vector; hai đầu ra sinh từ cùng nguồn TEX.
- Gói giữ `draft: true`, `production: in_production`, `publication: pending`
  cho đến khi có quyết định riêng.

## 3. Cây nội dung cấp cao đã khóa

| Thứ tự | ID canonical                | Tiêu đề hiển thị           | Chức năng                                                         |
| -----: | --------------------------- | -------------------------- | ----------------------------------------------------------------- |
|      1 | `cách-học-với-tài-liệu-này` | Cách học với tài liệu này  | Hướng dẫn sử dụng, mục tiêu, kiến thức cần trước và lộ trình học  |
|      2 | `bai-hoc`                   | Bài học                    | Hình thành khái niệm, phương pháp, sự tồn tại và cầu nối vận dụng |
|      3 | `phieu-luyen`               | Luyện tập                  | Mười nhiệm vụ L01–L10, không chứa lời giải                        |
|      4 | `tu-kiem-tra`               | Kiểm tra                   | Năm nhiệm vụ KT01–KT05, không chứa gợi ý hoặc lời giải            |
|      5 | `sua-loi`                   | Sửa lỗi                    | Bản đồ lỗi và sáu nhiệm vụ S00–S05, không chứa lời giải           |
|      6 | `on-lai`                    | Ôn lại                     | Lịch quay lại, nhiệm vụ mới và nhật kí học tập                    |
|      7 | `loi-giai`                  | Lời giải và hướng dẫn chấm | Toàn bộ đối chiếu, gợi ý cần giữ và lời giải theo nhóm            |
|      8 | `đọc-kết-quả-tự-kiểm-tra`   | Đọc kết quả tự kiểm tra    | Đối chiếu M01–M04 và định tuyến sửa lỗi                           |
|      9 | `nguon`                     | Nguồn đối chiếu            | Danh mục nguồn công khai, ngắn gọn và có vai trò rõ               |
|     10 | `tai-tai-lieu`              | Tải PDF                    | Vị trí giao diện đã khóa; chỉ kích hoạt tệp tải ở pha PDF         |

Thanh thẻ HTML dùng đúng chín nhãn của baseline R1-G01: Cách học, Bài học,
Luyện tập, Kiểm tra, Sửa lỗi, Ôn lại, Lời giải, Tải PDF và Toàn văn. Hai mục
`loi-giai` và `đọc-kết-quả-tự-kiểm-tra` cùng thuộc thẻ Lời giải; `nguon` thuộc
thẻ Cách học.

## 4. Ma trận phần Cách học và Bài học

| Vị trí đích | Nội dung nguồn hiện tại                               | Cách tổ chức đích                                                             | ID                                |
| ----------- | ----------------------------------------------------- | ----------------------------------------------------------------------------- | --------------------------------- |
| Cách học    | Lời dẫn và “Bắt đầu ở đây”                            | Lời giới thiệu gói, phạm vi, cách tự học; bỏ ngôn ngữ “bản để góp ý”          | `cách-học-với-tài-liệu-này`       |
| Cách học    | Bốn mục tiêu M01–M04                                  | Chuyển thành bảng ba cột theo baseline: mục tiêu, bằng chứng, nơi tự kiểm tra | `r1-g02-table-t01`                |
| Cách học    | Kiến thức cần trước                                   | Giữ thành đoạn riêng, không đặt trong lưới trang trí                          | `kien-thuc-can-truoc`             |
| Cách học    | Gợi ý chia lượt học                                   | Chuyển thành bảng Học–Luyện–Kiểm tra–Sửa lỗi–Ôn lại                           | `r1-g02-table-t02`                |
| Cách học    | Chỉ dẫn mở gợi ý/lời giải                             | Khối `.r1-details .r1-guidance` “Cách thực hiện”                              | `cach-thuc-hien-su-dung-tai-lieu` |
| Bài học 0   | Ba câu trước khi học                                  | Đưa vào đầu Bài học; đề ở đây, đối chiếu chuyển sang Lời giải                 | `bắt-đầu-từ-đâu`                  |
| Bài học 1   | Hàm số được cho bằng quy tắc và tập xác định          | Giữ nội dung; chia nhịp thử nghĩ–khái niệm–đối chiếu D/K–tự kiểm tra          | `doi-tuong`                       |
| Bài học 2   | Hai điều kiện cùng phải đúng                          | Giữ định nghĩa, cực trị/GTLN–GTNN và hàm hằng; tách lời giải khỏi mạch        | `dinh-nghia`                      |
| Bài học 3   | Trên đoạn đóng                                        | Giữ định lí, danh sách điểm và ví dụ hàm bậc hai; dùng BBT02 canonical        | `tren-doan`                       |
| Bài học 4   | Tập không phải đoạn đóng                              | Giữ bảng đổi tập, nhiều thành phần và sự đạt được                             | `tap-khac`                        |
| Bài học 5   | Cầu nối đến bài toán thực tiễn                        | Giữ quy trình lập đại lượng và ràng buộc; không mở rộng sang tối ưu tổng hợp  | `loi-van`                         |
| Khép lại    | Nội dung tổng kết rải ở cuối Học và “Học tiếp từ đây” | Gom thành kết luận bài học và tuyến học tiếp                                  | `khép-lại-bài-học`                |

Phần Bài học có đúng bảy mục cấp ba: mục 0, năm mục nội dung và “Khép lại bài
học”. Mỗi mục nội dung dùng nhịp canonical khi có đủ vật liệu: `Cách thực hiện`
→ `Thử nghĩ trước` → kiến thức/ví dụ → `Câu hỏi tự kiểm tra`.

## 5. Ma trận nhiệm vụ

### 5.1. Luyện tập

| ID đề | Tiêu đề đã khóa                                          | ID lời giải đích |
| ----- | -------------------------------------------------------- | ---------------- |
| `l01` | Bài luyện tập 01. Cực đại có phải lớn nhất?              | `loi-giai-l01`   |
| `l02` | Bài luyện tập 02. Một điểm không có đạo hàm              | `loi-giai-l02`   |
| `l03` | Bài luyện tập 03. Tập không bị chặn, hàm vẫn bị chặn     | `loi-giai-l03`   |
| `l04` | Bài luyện tập 04. Hai thành phần đều cần được xét        | `loi-giai-l04`   |
| `l05` | Bài luyện tập 05. Từ doanh thu đến lợi nhuận             | `loi-giai-l05`   |
| `l06` | Bài luyện tập 06. Đọc giá trị và sự đạt được trên đồ thị | `loi-giai-l06`   |
| `l07` | Bài luyện tập 07. Kiểm tra chuyển giao: hàm lượng giác   | `loi-giai-l07`   |
| `l08` | Bài luyện tập 08. Chuyển giao: hàm mũ và lôgarit         | `loi-giai-l08`   |
| `l09` | Bài luyện tập 09. Nghiệm đạo hàm nào được giữ lại?       | `loi-giai-l09`   |
| `l10` | Bài luyện tập 10. Chọn cách so sánh trực tiếp            | `loi-giai-l10`   |

Gợi ý của L01, L02, L03 và L05 được giữ cạnh đề dưới dạng `.r1-guidance`;
mọi lời giải chuyển khỏi phần Luyện tập.

### 5.2. Kiểm tra

| ID đề  | Tiêu đề đã khóa                                    | Mục tiêu | ID lời giải đích |
| ------ | -------------------------------------------------- | -------- | ---------------- |
| `kt01` | Bài kiểm tra 01. Đọc đồ thị trên tập được chỉ định | M01, M03 | `loi-giai-kt01`  |
| `kt02` | Bài kiểm tra 02. Có thể đạt tại nhiều điểm         | M02, M04 | `loi-giai-kt02`  |
| `kt03` | Bài kiểm tra 03. Đọc toàn bảng                     | M03      | `loi-giai-kt03`  |
| `kt04` | Bài kiểm tra 04. Biến nhận giá trị nguyên          | M04      | `loi-giai-kt04`  |
| `kt05` | Bài kiểm tra 05. Phản biện lời giải dùng đạo hàm   | M02      | `loi-giai-kt05`  |

Phần Kiểm tra không chứa `<details>`, đáp án, gợi ý hoặc định tuyến “nếu sai”.
Định tuyến chuyển sang phần Đọc kết quả tự kiểm tra.

### 5.3. Sửa lỗi

| ID đề | Tiêu đề đã khóa                                     | ID lời giải đích |
| ----- | --------------------------------------------------- | ---------------- |
| `s00` | Bài tập khắc phục lỗi 00. Cực đại và toàn đoạn      | `loi-giai-s00`   |
| `s01` | Bài tập khắc phục lỗi 01. Có cận nhưng không đạt    | `loi-giai-s01`   |
| `s02` | Bài tập khắc phục lỗi 02. Điểm gãy và tọa độ        | `loi-giai-s02`   |
| `s03` | Bài tập khắc phục lỗi 03. Đọc hai thành phần        | `loi-giai-s03`   |
| `s04` | Bài tập khắc phục lỗi 04. Tổng chi phí và số nguyên | `loi-giai-s04`   |
| `s05` | Bài tập khắc phục lỗi 05. Đoạn đóng chưa đủ         | `loi-giai-s05`   |

Bảng “Dấu hiệu trong bài làm – Thao tác sửa – Thử lại” đứng trước sáu nhiệm vụ
và trở thành hợp đồng định tuyến lỗi. Không đổi mã S00–S05 trong lượt chuyển.

## 6. Kiến trúc phần Lời giải

| Nhóm | Nội dung                                            | ID nhóm              |
| ---- | --------------------------------------------------- | -------------------- |
| B.1  | Đối chiếu ba câu trước khi học                      | `loi-giai-khoi-dong` |
| B.2  | Lời giải ví dụ và câu hỏi tự kiểm tra trong Bài học | `loi-giai-bai-hoc`   |
| B.3  | Lời giải L01–L10                                    | `loi-giai-luyen-tap` |
| B.4  | Lời giải/hướng dẫn chấm KT01–KT05                   | `loi-giai-kiem-tra`  |
| B.5  | Lời giải S00–S05 và câu mới sau L07                 | `loi-giai-sua-loi`   |
| B.6  | Đáp án các lượt Ôn lại                              | `loi-giai-on-lai`    |

Mỗi đề có một khối `.answer-link` trỏ tới đúng ID lời giải. Mỗi lời giải có liên
kết trở về đề. Không tạo bản sao nội dung lời giải ở vị trí cũ.

## 7. Ma trận bảng

### 7.1. Bốn bảng đi qua pipeline BBT

| ID tài sản | Vị trí dùng               | Dữ liệu được bảo toàn                                              | Vai trò                                  |
| ---------- | ------------------------- | ------------------------------------------------------------------ | ---------------------------------------- |
| `BBT01`    | Khởi động 01              | hàng `x`: −3, 0, 2, 4; hàng `r(x)`: 5 ↘ −2 ↗ 1 ↘ 0                 | BBT đầy đủ trên đoạn                     |
| `BBT04`    | KT03                      | hai thành phần `[-3;−1]`, `(0;2]`; giá trị 5 ↘ 2 và giới hạn 0 ↗ 4 | BBT có khoảng loại và giới hạn không đạt |

Hai BBT dùng một JSON canonical tại `du_lieu/bang_bien_thien.json`; công cụ chung
sinh `hinh/bbt01` và `hinh/bbt04` ở ba định dạng TEX/PDF/SVG. Caption trong QMD
được khóa theo ngữ cảnh, không buộc trùng trường `title` của JSON.

Bước 7 đã hoàn tất sau khi hiệu chỉnh phân loại: hai bản ghi JSON vượt kiểm tra
schema và quan hệ dấu–chiều; mỗi mã có đúng một bộ TEX/PDF/SVG sinh từ công cụ
chung. QMD chỉ giữ mã BBT và caption ngữ cảnh; HTML dùng SVG kèm bảng ngữ nghĩa
ẩn từ cùng JSON. Hai bảng giá trị của `p` và `f` không thuộc pipeline BBT.

### 7.2. Bảng thường

Tám bảng thường đã được kiểm kê và khóa hợp đồng trình bày. Bảng `t08` được
bổ sung ở Bước 9A khi phần “Cách học” được đưa về nhịp canonical của R1-G01;
bảng này chỉ tổ chức lại hướng dẫn sử dụng đã có, không thêm nội dung toán học:

| ID | Nội dung | Chế độ | Độ rộng cột | Tiêu đề hàng |
|:---|:---------|:-------|:------------|:--------------|
| `r1-g02-table-t01` | Phân biệt tập xác định và tập đang xét | `fit` | `26, 74` | Có |
| `r1-g02-table-t02` | Phân biệt cực trị và giá trị lớn nhất, nhỏ nhất | `scroll`, tối thiểu `42em` | `45, 55` | Không |
| `r1-g02-table-t03` | Giá trị lớn nhất, nhỏ nhất của $F$ trên các tập đang xét | `fit` | `40, 30, 30` | Có |
| `r1-g02-table-t04` | Dấu hiệu lỗi, thao tác sửa và bài thử lại | `scroll`, tối thiểu `54em` | `34, 48, 18` | Có |
| `r1-g02-table-t05` | Lịch ôn lại và nhiệm vụ tương ứng | `scroll`, tối thiểu `44em` | `24, 76` | Có |
| `r1-g02-table-t06` | Bảng giá trị của $p$ tại các điểm cần so sánh | `fit` | `25, 25, 25, 25` | Có |
| `r1-g02-table-t07` | Bảng giá trị của $f$ tại các điểm cần so sánh | `fit` | `20, 20, 20, 20, 20` | Có |
| `r1-g02-table-t08` | Cách học và kết quả cần giữ lại | `fit` | `18, 52, 30` | Có |

Hợp đồng thực thi nằm trong metadata `r1-tables` của `index.qmd`; filter cục bộ
gán độ rộng, vai trò tiêu đề, nhãn trợ năng và hành vi cuộn theo đúng cơ chế của
R1-G01. Hai BBT01 và BBT04 không thuộc inventory này và dùng pipeline BBT
canonical của Bước 7.

## 8. Ma trận đồ thị

| ID tài sản  | Vị trí dùng | Đặc tả bắt buộc                                                                                                  |
| ----------- | ----------- | ---------------------------------------------------------------------------------------------------------------- |
| `do_thi_01` | L06         | phần đồ thị của `f(x)=x²` trên `K=[−1;2)`; điểm kín (−1;1), (0;0); điểm hở (2;4); trục và nhãn đúng              |
| `do_thi_02` | KT01        | phần đồ thị của hàm nghịch biến trên `K=(1;3]`; điểm hở (1;3), điểm kín (3;−1); không tiết lộ công thức trong đề |

Mỗi đồ thị có đúng một nguồn `hinh/do_thi_0N.tex`; SVG và PDF được sinh từ TEX
cùng tên. QMD dùng SVG ở HTML và PDF vector ở đầu ra PDF qua filter. Alt text,
caption và mô tả trợ năng bảo toàn thông tin điểm kín, điểm hở và tập đang xét.
Không giữ data URI base64 trong QMD.

Bước 8 đã hoàn tất: `do_thi_01.tex` và `do_thi_02.tex` là hai nguồn TeX
canonical; công cụ đồ thị chung đã sinh và kiểm tra các cặp `do_thi_01.pdf` /
`do_thi_01.svg` và `do_thi_02.pdf` / `do_thi_02.svg`. QMD tham chiếu SVG cho
HTML; filter cục bộ chỉ đổi sang PDF vector khi có đầu ra LaTeX. Lượt này chỉ
render HTML preview để duyệt, chưa dựng PDF học liệu và chưa xuất bản.

## 9. Nội dung phải chuyển khỏi trang người học

Các mục sau của footer bản thảo chuyển vào hồ sơ nội bộ trong `_quy_trinh`:

- ghi chú hiệu đính 1–4;
- bảng đối chiếu M01–M04 với từng lần sửa;
- truy nguyên N01–N12;
- độ bao phủ, giới hạn kiểm định và lịch sử hiệu đính;
- trạng thái “bản thảo để chủ dự án xem xét”.

Phần `Nguồn đối chiếu` dành cho người học chỉ giữ danh mục nguồn đã thực sự dùng
và mô tả ngắn vai trò; không chứa hội thoại, đường dẫn sandbox hoặc quyết định
điều hành.

## 10. Inventory đích của pha HTML

| Thành phần                       | Số lượng khóa |
| -------------------------------- | ------------: |
| Phần cấp hai trong root học liệu |            10 |
| Mục cấp ba trong Bài học         |             7 |
| Bài luyện tập                    |            10 |
| Bài kiểm tra                     |             5 |
| Bài khắc phục lỗi                |             6 |
| BBT canonical                    |             2 |
| Đồ thị canonical                 |             2 |
| Lời giải luyện tập               |            10 |
| Lời giải kiểm tra                |             5 |
| Lời giải sửa lỗi                 |             6 |

Số bảng thường, công thức và khối hỗ trợ được khóa sau bước tái cấu trúc nguồn,
vì lượt chuyển cơ học hiện tại không phải inventory đáng tin cậy cho các thành
phần ấy. Việc chưa khóa ba số này không cho phép thêm hoặc bỏ nội dung.

## 11. Điều kiện hoàn thành bước kiến trúc

Bước 1 hoàn thành khi:

- cây phần cấp cao, ID và thứ tự đã xác định;
- toàn bộ L01–L10, KT01–KT05, S00–S05 có vị trí và ID lời giải;
- bốn BBT và hai đồ thị có ID, dữ liệu/vai trò và đầu ra đích;
- hồ sơ nội bộ được phân cách khỏi nội dung người học;
- không còn quyết định kiến trúc cần suy đoán trước khi tái cấu trúc `index.qmd`.

Ma trận này đáp ứng các điều kiện trên. Mọi thay đổi kiến trúc về sau cần quyết
định riêng của chủ dự án; sửa kỹ thuật để hiện thực hóa ma trận không được làm
thay đổi nội dung toán học.
