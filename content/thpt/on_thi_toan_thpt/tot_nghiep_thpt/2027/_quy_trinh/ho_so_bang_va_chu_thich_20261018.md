# Bảng toán và chú thích hình/bảng — 18/10/2026

Trạng thái: đã sửa/kiểm nguồn và thành phần trong bộ nhớ; chưa dựng HTML/PDF, chưa kiểm hiển thị thật của bản mới, chưa chủ trì duyệt, chưa commit/push/xuất bản. Không thay đổi các HTML đang xem.

## Kết quả rà soát

Đã đọc nguồn QMD, dữ liệu BBT, mapping vai trò, bộ sinh và CSS; đối chiếu HTML hiện có của G01–G04 trong `_audit/r1_consistency_20261018/html/` và D0 trong `docs/` như bằng chứng trước sửa. Không dùng các HTML này làm đầu vào dựng chính thức.

| Trang | BBT | Bảng dấu | Bảng giá trị | Đồ thị/hình được rà |
|---|---:|---:|---:|---|
| G01 | 12 | 3, gồm một bảng giải thích | 0 | 13 đồ thị, đều có tên |
| G02 | 2 | 0 | 2 | 4 đồ thị, đều có tên |
| G03 | 0 | 0 | 0 | 11 đồ thị: 6 có tên, 5 giữ không tên |
| G04 | 35 | 0 | 0 | 35 đồ thị, đều có tên |
| D0 | 0 | 1 | 0 | Một hình hình học đã có chú thích phù hợp |

Tổng cộng 55 bảng toán, trong đó 52 bảng native theo JSON và 3 bảng thường theo mapping. R1 có 63 đồ thị. Các bảng hướng dẫn/tiêu chí/nhật kí vẫn giữ vai trò riêng, không bị biến thành bảng toán.

## Điểm lệch và sửa nguồn

- Bảng giá trị dùng kiểu bảng lời văn (chữ nhỏ hơn, nền trắng/header xám, khoảng đệm khác), còn BBT/sign native dùng nhịp ô và nền 0.4. Đã gắn cùng lớp `zo-math-grid` theo ba loại values/sign/variation: cùng cỡ chữ, nền giấy, nét lưới và khoảng đệm. Bảng ngắn không bị trải rộng; hàng–cột/mốc/khoảng giữ nguyên. Bảng giải thích dấu giữ phần lời văn, header và cột nhấn theo chức năng; cột loại vẫn có biên đôi. Đây là thống nhất diện mạo bảng toán của khóa, không phải khóa Design 0.5 mới.
- Hai tên BBT G02 nằm trên vì nhánh payload chèn bảng native sau chú thích đang có. Đã sửa nguồn nhánh chèn và chuẩn hóa bằng thành phần chung.
- Hai tên BBT G01 nằm dưới bảng nhưng ở trong vùng cuộn. Thành phần chung đưa chú thích nhìn thấy xuống cuối figure, ngoài vùng cuộn; áp dụng nhất quán cả bảng và đồ thị. Không đổi nội dung tên đang có.
- Chuyên mục kế thừa `tbl-cap-location: bottom`; CSS bảng hiện hành và CSS fallback đều dùng `caption-side: bottom`. Kiểu chữ chú thích chung áp dụng trong vùng đọc; tên bảng trợ năng vẫn ẩn để không xuất hiện hai tên. Không đổi đoạn dẫn “Bảng biến thiên là:” thành tên đặt trên bảng.

## Các trường hợp giữ không tên

| Đối tượng | Quyết định và căn cứ |
|---|---|
| G01 `r1-table-t04` | Giữ không tên riêng: thuộc ngay mục phương pháp về dấu đạo hàm, đầu cột xác định đủ đối tượng; chỉ có một bảng trong mục. |
| G02 `r1-g02-table-t06` | Giữ không tên riêng: đoạn trước nêu hàm và miền; hai hàng gắn rõ đầu vào với giá trị, không có bảng khác để nhầm. |
| G02 `r1-g02-table-t07` | Giữ không tên riêng: một bảng duy nhất trong lời giải nhiệm vụ, câu trước và nhãn hàng xác định hàm. |
| G03 `l09_doc_hinh.svg` — nhiệm vụ đọc hình trong Luyện tập | Giữ không tên: một đồ thị dữ kiện, câu dẫn và giới hạn đi kèm đã chỉ rõ vai trò; có mô tả thay thế. |
| G03 `k02_doc_hinh.svg` — nhiệm vụ đọc hình trong Kiểm tra | Giữ không tên: một hình dữ kiện trong câu; không thêm dòng chú thích dễ lặp dữ kiện hoặc gợi đáp án. |
| G03 `s_l05_doc_hinh.svg` — xác nhận sau Luyện tập | Giữ không tên: một hình duy nhất trong đúng nhiệm vụ, dữ kiện đi kèm rõ. |
| G03 `s_k04_doc_hinh.svg` — xác nhận sau Kiểm tra | Giữ không tên vì cùng quan hệ một hình–một nhiệm vụ; mô tả thay thế được giữ. |
| G03 `s_o03_doc_hinh.svg` — xác nhận sau Ôn lại | Giữ không tên vì câu dẫn và dữ kiện đã xác định đồ thị, không có tham chiếu số hình từ nơi khác. |

Các quyết định của ba bảng được ghi ngay tại mapping hiện hành (`caption_policy`, `caption_reason`). Năm ảnh G03 có thuộc tính nguồn `data-zo-caption="omitted"` và lý do; không có dòng kỹ thuật mới xuất hiện trong chính văn. Không thêm hệ số thứ tự cho hình/bảng. Các tên còn lại cần cho phân biệt, dẫn chiếu hoặc giải thích nên giữ nguyên. Không có trường hợp cần bổ sung tên nhìn thấy mới trong nhóm đã rà.

## Chủ sở hữu nguồn và chống tái diễn

- QMD ảnh được ghi quyết định: `content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g03/index.qmd`.
- Mặc định Quarto: `content/thpt/on_thi_toan_thpt/_metadata.yml`.
- Kiểu và mapping: `_design/web_2027_mau_dung_chung/course-tables.css`, `profiles/course-tables.json`; fallback tại `assets/css/zo_on_thi_learning_package.css`.
- Thành phần và kiểm: `scripts/zo_course_tables.py`; sửa nguồn nhánh sai tại `scripts/zo_web_2027_g02_payloads.py`; nối cổng tại `scripts/zo_check_repo.py` và `scripts/zo_web_2027_consistency.py`.
- Quy tắc/cách gọi: 07/6.1.1 và quy trình 02; trạng thái tiếp tục tại 03. Hồ sơ này chỉ ghi bằng chứng và lựa chọn áp dụng.

Cổng nguồn kiểm mặc định tên dưới, kiểu ô toán và quyết định không tên. Cổng thành phần kiểm lớp lưới, tên xuống cuối figure và lý do khi không có tên. Thử âm bắt tên nằm trên, thiếu lớp, khác cỡ/khoảng đệm ô, mất biên đôi và đồ thị thiếu tên không có lý do. Bộ công cụ `E:/zo_math_graphics` cùng nguồn SVG/TEX và JSON dữ liệu không bị sửa; không cần dựng lại hình để sửa cách đặt chú thích hoặc kiểu bảng HTML.

## Kiểm đã chạy và phần còn chờ

- CLI QMD `check` với D0/G01–G04: PASS; có đủ năm cổng `course-table-figure-presentation`. Phép kiểm hình học D0 là đọc/kiểm nguồn và SVG đang có, không dựng lại hình.
- `python scripts/zo_python.py -B scripts/zo_course_tables.py --self-test`: 44/44.
- Kiểm thành phần với dữ liệu HTML đối chứng tường minh, chỉ thao tác DOM trong bộ nhớ và không ghi trang HTML: 437/437. Giữ nguyên toàn bộ ô bảng, ID, ảnh/alt, chuỗi công thức và nội dung tên; các QMD giữ nguyên chính văn, chỉ thêm quyết định ở thuộc tính năm ảnh G03.
- Hồi quy nhãn liên kết đề–lời giải của lượt trước: 46/46.
- Bằng chứng trước/sau, kết quả cổng nguồn, các ca kiểm và đối chiếu bảo toàn tại `E:/zo_math/_audit/table_figure_sources_20261018/`.

Đây chưa phải kiểm computed style hoặc xem HTML mới sau dựng. Khi được giao dựng, cần kiểm thật trên màn hình rộng/hẹp: cỡ/nhịp ô, căn chữ theo chức năng, biên đôi, tên dưới/outside scroll, năm trường hợp không tên và không tràn trang. Những bản xem trước vẫn giữ nguyên; không dùng chúng để nghiệm thu nguồn sửa lần này. Các thay đổi điều hướng và nhãn thao tác trước đó được bảo toàn, vẫn chưa có HTML dựng lại cho ba lượt sửa nguồn.
