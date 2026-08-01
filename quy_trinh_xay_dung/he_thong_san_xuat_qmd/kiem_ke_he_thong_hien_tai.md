# Kiểm kê hệ thống sản xuất QMD hiện tại

> **Trạng thái:** Bản ghi đường cơ sở của Giai đoạn 0.
>
> Tài liệu này mô tả hiện trạng đã quan sát. Nó chưa phải quy chuẩn hoặc quyết định kiến trúc cuối cùng.

## 1. Phạm vi kiểm kê

Đợt kiểm kê tập trung vào:

- hệ thống sản xuất bài của dự án **100+ Hàm số: Sự biến thiên và đồ thị**;
- các tài liệu xây dựng dùng chung đang có;
- checker thống nhất của repository;
- hệ thống HTML và PDF liên quan trực tiếp;
- bài `ham_ln_x.qmd` làm đường cơ sở hồi quy.

Đợt kiểm kê chưa bao gồm:

- thiết kế nội dung của 100+ Bài toán thực tế;
- tái cấu trúc checker;
- sửa các quy trình hiện hành;
- xuất bản bài;
- quy chuẩn sinh bảng biến thiên;
- những thay đổi không liên quan đang tồn tại trong working tree.

## 2. Trạng thái repository khi bắt đầu

Tại thời điểm kiểm kê:

```text
nhánh: master
so với origin/master: ahead 14
working tree: không sạch
```

Working tree có các thay đổi và tệp chưa theo dõi không thuộc nhiệm vụ này.

Những thành phần ngoài phạm vi phải được giữ nguyên, gồm:

- `khung_khao_sat_ham_so.qmd`;
- tệp PDF bài tập trong `figures/`;
- quy chuẩn đồ thị đang có thay đổi chưa commit;
- `.continue/`;
- các tệp ZIP;
- favicon;
- `assets/tex/zo-graph-styles.tex`;
- các tệp thử nghiệm;
- tệp lưu kho và tài liệu tạm của các nhiệm vụ trước.

Không dùng `git add .` trong công việc này.

## 3. Chỉ dẫn có thẩm quyền

### 3.1. Cấp repository

Nguồn điều phối:

```text
AGENTS.md
```

Hai tài liệu bắt buộc được dẫn chiếu:

```text
quy_trinh_xay_dung/quy_tac_lam_viec_voi_agent.md
quy_trinh_xay_dung/quy_trinh_thuc_hien_nhiem_vu_ky_thuat.md
```

Các nguyên tắc trực tiếp liên quan:

- phải khảo sát trước khi sửa;
- không mở rộng phạm vi;
- phân biệt hiện trạng với quyết định thiết kế;
- không tự sửa đầu ra tự động;
- giữ diff nhỏ và có thể kiểm tra;
- không tự commit, push, xuất bản, xóa hoặc di chuyển;
- dùng checker thống nhất qua `scripts/zo_python.py`;
- tài liệu mới không tự động trở thành quy chuẩn có hiệu lực.

### 3.2. Cấp dự án 100+ Hàm số

Nguồn điều phối:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/AGENTS.md
```

Ba tài liệu điều khiển chính:

```text
_quy_trinh/quy_trinh_tao_bai_ham_so.md
_quy_trinh/quy_chuan_khao_sat_ham_so.md
_quy_trinh/quy_chuan_ki_thuat_bai_ham_so_qmd.md
```

Hai mẫu vận hành:

```text
_quy_trinh/mau_ki_thuat_qmd.qmd
_quy_trinh/ho_so_san_xuat_mac_dinh.yml
```

Nguồn lí thuyết nội bộ:

```text
_quy_trinh/nguon_li_thuyet/khung_khao_sat_ham_so_hoan_chinh_04.qmd
```

## 4. Quy mô các nguồn chính

### Quy trình sản xuất bài khảo sát hàm số

```text
432 dòng
3.868 từ
25.060 kí tự
```

Cấu trúc chính:

- mục đích và phạm vi;
- phạm vi tệp và đường dẫn;
- chế độ vận hành;
- đầu vào;
- thứ tự thẩm quyền;
- sản phẩm làm việc;
- chín giai đoạn thực hiện;
- kiểm định;
- cập nhật tài liệu điều khiển;
- nghiệm thu;
- mẫu lệnh giao việc.

### Quy chuẩn kĩ thuật bài hàm số QMD

```text
910 dòng
5.897 từ
38.214 kí tự
```

Cấu trúc chính:

- thẩm quyền;
- loại quy tắc và trạng thái;
- hợp đồng đầu ra;
- YAML và metadata;
- cấu trúc thân bài;
- mã thực thi;
- khối nội dung;
- bảng, hình và tài nguyên;
- bài tập;
- PDF;
- cấu trúc bị cấm;
- kiểm định tự động;
- kiểm định có người quan sát;
- nghiệm thu.

### Mẫu kĩ thuật QMD

```text
259 dòng
1.113 từ
7.937 kí tự
```

Mẫu chứa:

- YAML của dự án;
- metadata lưới thẻ;
- cấu hình PDF;
- ghi chú khởi tạo;
- vị trí tài nguyên;
- cú pháp khối;
- cấu trúc bài tập.

### Hồ sơ sản xuất mặc định

```text
721 dòng
1.432 từ
19.531 kí tự
```

Các nhóm dữ liệu chính:

- nhận diện;
- nhiệm vụ;
- đơn vị khảo sát;
- đường dẫn;
- phạm vi thay đổi;
- tài liệu điều khiển;
- bản đồ miền;
- vòng rà;
- mệnh đề–chứng cứ;
- trục nhận thức;
- bản đồ hiện tượng;
- đề cương vận hành;
- hồ sơ biểu diễn;
- tài nguyên hình;
- hệ thống bài tập;
- đầu ra kĩ thuật;
- hệ khối nội dung;
- kiểm định;
- nghiệm thu;
- vấn đề hệ thống;
- bàn giao.

### Quy chuẩn khảo sát hàm số

```text
1.349 dòng
11.070 từ
71.653 kí tự
```

Đây là quy chuẩn nội dung toán học và nhận thức chuyên biệt của dự án, không phải ứng viên để chuyển nguyên khối vào lõi QMD dùng chung.

## 5. Hạ tầng dùng chung đang tồn tại

Các tài liệu dùng chung hiện có trong `quy_trinh_xay_dung/`:

```text
huong_dan_su_dung_khoi_noi_dung.md
phong_cach_viet/
quy_chuan_do_thi_sinh_ma_nguon_tikz_pgfplots.md
quy_chuan_luoi_the.md
quy_tac_lam_viec_voi_agent.md
quy_tac_sidebar_va_muc_luc.md
quy_trinh_thuc_hien_nhiem_vu_ky_thuat.md
quy_trinh_xuat_ban_website.md
```

Lõi QMD mới phải dẫn chiếu các tài liệu phù hợp, không sao chép nội dung chi tiết của chúng.

Hạ tầng kĩ thuật liên quan:

```text
_quarto.yml
assets/lua/zo_pdf_branding.lua
assets/tex/zo-pdf.tex
scripts/zo_python.py
scripts/zo_quarto.py
scripts/zo_check_repo.py
```

## 6. Checker hiện hành

Checker thống nhất:

```text
scripts/zo_check_repo.py
```

Phiên bản đường cơ sở:

```text
2.0.4
```

Quy mô tại thời điểm kiểm kê:

```text
73.425 byte
```

Giao diện lệnh hiện hành:

```text
quick
scope
render
```

Các phần dùng chung đã có:

- tìm gốc repository;
- mở rộng phạm vi;
- kiểm tra Git;
- kiểm tra EOL và khoảng trắng;
- đọc UTF-8;
- kiểm tra YAML;
- kiểm tra Markdown và tài nguyên;
- kiểm tra SVG;
- kiểm tra Python;
- chuẩn bị môi trường Quarto;
- render;
- đọc log;
- báo cáo kết quả;
- ghi báo cáo JSON.

## 7. Phần gắn cứng với 100+ Hàm số trong checker

Các hằng chính:

```text
CARD_PROJECT
CARD_IMAGE_DIR
FUNCTION_ARTICLE_DIRS
FUNCTION_REQUIRED_METADATA
FUNCTION_PLACEHOLDERS
FUNCTION_LEGACY_CLASSES
FUNCTION_BLOCK_COLORS
FUNCTION_CANONICAL_BASE
FUNCTION_PROFILE_DIR
FUNCTION_EXPANDED_FIGURE_CLASS
```

Các hàm chuyên biệt chính:

```text
is_function_article()
function_card()
validate_function_metadata()
function_profile_path()
parse_expanded_figure_profile()
expanded_figure_records()
validate_function_figure_layout()
validate_function_body()
validate_function_article()
validate_rendered_function_page()
```

Ba điểm nối điều phối:

1. `is_function_article()` nhận diện bài trong `core/` hoặc `depth/`.
2. `validate_file()` kích hoạt `validate_function_article()`.
3. `render_pages()` kích hoạt `validate_rendered_function_page()`.

Kiểm tra lưới thẻ được kích hoạt riêng qua:

```text
card_scope()
check_card_grid()
```

## 8. Phân loại sơ bộ bốn nguồn cần tách

### `quy_chuan_ki_thuat_bai_ham_so_qmd.md`

Phần lớn nội dung có khả năng trở thành lõi dùng chung:

- YAML;
- metadata;
- tiêu đề;
- mã thực thi;
- khối nội dung;
- tài nguyên;
- HTML;
- PDF;
- kiểm định;
- bằng chứng;
- nghiệm thu.

Phần riêng của dự án:

- `listing-order`;
- quan hệ với `_data/cards.yml`;
- tên bộ sưu tập;
- trạng thái thẻ;
- dẫn chiếu sang quy chuẩn khảo sát hàm số.

### `quy_trinh_tao_bai_ham_so.md`

Đây là tài liệu pha trộn.

Phần có khả năng dùng chung:

- khóa phạm vi;
- khởi tạo hồ sơ;
- đặc tả tài nguyên;
- tạo QMD;
- kiểm định kĩ thuật;
- nghiệm thu;
- bàn giao.

Phần riêng:

- hàm số hoặc họ hàm;
- hồ sơ khảo sát toán học;
- bản đồ miền;
- mệnh đề–chứng cứ;
- trục nhận thức của bài khảo sát hàm số;
- `core/`, `depth/`;
- `_data/cards.yml`;
- nguồn lí thuyết khảo sát hàm số.

### `mau_ki_thuat_qmd.qmd`

Mẫu này là mẫu dự án được xây trên nền kĩ thuật chung.

Phần riêng nổi bật:

- tiêu đề “Hàm số”;
- đường dẫn hình thẻ;
- `listing-order`;
- collection của dự án;
- dẫn chiếu tài liệu hàm số;
- đối chiếu `_data/cards.yml`.

Không nên chuyển nguyên mẫu này thành mẫu lõi.

### `ho_so_san_xuat_mac_dinh.yml`

Hồ sơ chứa đồng thời:

- phần nhận diện và kiểm định dùng chung;
- phần nghiệp vụ khảo sát hàm số.

Hướng tách sơ bộ:

```text
hồ sơ lõi
+ phần mở rộng theo dự án
+ dữ liệu riêng của từng bài
```

## 9. Đường cơ sở hồi quy

Bài được chọn làm đường cơ sở:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/core/ham_ln_x.qmd
```

Các đầu ra liên quan đã có:

- QMD;
- HTML;
- PDF;
- hai đồ thị;
- hồ sơ sản xuất;
- cấu hình sidebar.

Kết quả kiểm định gần nhất:

```text
PASS_WITH_WARNINGS
EXIT=0
nghiệm thu: ĐẠT
```

Bài đang dừng trước cổng xuất bản.

Thẻ số 114 vẫn phải giữ:

```text
status: pending
href: ''
```

Không dùng việc tái cấu trúc hệ thống để tự động chuyển bài sang `published`.

## 10. Kết luận kiểm kê ban đầu

Hệ thống hiện tại không phải một tập hợp rời rạc. Nó đã có:

- một quy trình sản xuất thực tế;
- một hợp đồng đầu ra tương đối đầy đủ;
- một hồ sơ sản xuất chi tiết;
- một mẫu QMD;
- một checker thống nhất;
- một bài đã kiểm nghiệm từ đầu đến cuối.

Vấn đề chính không phải xây lại từ đầu, mà là:

1. phân tách phần dùng chung khỏi nghiệp vụ khảo sát hàm số;
2. thay các điểm gắn cứng bằng cấu hình dự án;
3. giữ nguyên hành vi đã kiểm nghiệm;
4. chứng minh lõi dùng được cho một dự án thứ hai.
