# Đường cơ sở hồi quy cho bài Hàm số y = ln x

> **Trạng thái:** Hồ sơ đường cơ sở của Giai đoạn 0.
>
> Tài liệu này ghi các điều kiện phải được bảo toàn khi tách lõi và cấu hình hóa hệ thống. Không dùng tài liệu này để xuất bản bài.

## 1. Đối tượng hồi quy

Bài QMD:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/core/ham_ln_x.qmd
```

Hồ sơ sản xuất:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/_quy_trinh/ho_so/ham_ln_x.yml
```

PDF tải xuống:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/core/ham_ln_x.pdf
```

Thư mục hình:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/_figures/do_thi_ham_ln_x/
```

Dữ liệu và cấu hình liên quan:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/_data/cards.yml
_quarto.yml
```

## 2. Trạng thái đã nghiệm thu

Đường cơ sở đã đạt:

```text
checker: 2.0.4
automated result: PASS_WITH_WARNINGS
exit code: 0
nghiệm thu cuối: ĐẠT
```

Các cảnh báo còn lại là yêu cầu quan sát của con người, không phải lỗi kĩ thuật ngăn nghiệm thu.

Bài đang dừng trước cổng xuất bản.

## 3. Trạng thái xuất bản phải được bảo toàn

Thẻ số 114 phải giữ:

```yaml
status: pending
href: ''
```

Không chuyển bài sang `published` trong quá trình:

- tách lõi;
- tạo cấu hình dự án;
- sửa checker;
- kiểm tra hồi quy;
- tạo dự án thứ hai.

Xuất bản chỉ được thực hiện khi người dùng xác nhận rõ.

## 4. Metadata cần bảo toàn

- `title` là tiêu đề hiển thị và có thể chứa TeX;
- `title-meta` là tiêu đề thuần văn bản dùng cho metadata;
- `pagetitle` là văn bản thuần;
- cấu hình PDF tải xuống trỏ đúng tệp;
- branding PDF giữ đúng tiêu đề ngắn;
- canonical URL khớp đường dẫn bài;
- lớp trang giữ đúng trạng thái bài viết;
- PDF Title thực tế khớp `title-meta`.

Không tái đưa TeX vào `title-meta` hoặc `pagetitle`.

## 5. Hình cần bảo toàn

Bài hiện dùng hai đồ thị của hàm lô-ga-rit tự nhiên.

Mỗi hình phải tiếp tục bảo toàn:

- nguồn TikZ/PGFPlots;
- PDF trung gian;
- SVG dùng cho HTML;
- tham chiếu đúng từ QMD;
- văn bản thay thế;
- chiều rộng nội dung mặc định;
- không dùng lớp hình mở rộng khi hồ sơ không khai báo.

Đường cơ sở:

```text
số hình mở rộng được khai báo: 0
số hình mở rộng xuất hiện trong QMD: 0
```

Không tự thêm lớp `column-screen-inset-shaded`.

## 6. HTML cần bảo toàn

Sau render, checker phải tiếp tục xác nhận:

- HTML tồn tại;
- `body` có các lớp bắt buộc;
- không có số lượng `H1` bất thường;
- liên kết tải PDF xuất hiện;
- tài nguyên PDF được xử lí đúng theo trạng thái `pending`;
- có cảnh báo yêu cầu kiểm tra trực quan trên desktop/mobile.

## 7. PDF cần bảo toàn

PDF vật lí phải tiếp tục:

- tồn tại tại đường dẫn đã khai báo;
- có header hợp lệ;
- được `pdfinfo` đọc khi công cụ có sẵn;
- có số trang hợp lệ;
- có PDF Title khớp `title-meta`;
- giữ branding ZO Math;
- không bị thay đổi chỉ vì tái cấu trúc checker.

Đường cơ sở đã quan sát:

```text
số trang: 15
```

Con số này chỉ dùng để phát hiện thay đổi bất thường. Thay đổi số trang không tự động là lỗi nếu có nhiệm vụ nội dung riêng đã được duyệt.

## 8. Checker cần bảo toàn

Các lệnh sau phải tiếp tục hoạt động:

```text
python scripts/zo_python.py scripts/zo_check_repo.py quick
python scripts/zo_python.py scripts/zo_check_repo.py scope <path>
python scripts/zo_python.py scripts/zo_check_repo.py render <path>
```

Sau khi cấu hình hóa:

- checker vẫn nhận diện đúng bài;
- validator lõi chạy;
- validator 100+ Hàm số chạy;
- kiểm tra thẻ tiếp tục hoạt động;
- kiểm tra hồ sơ hình tiếp tục hoạt động;
- định dạng báo cáo không bị phá vỡ;
- mã thoát vẫn phản ánh đúng kết quả.

## 9. Tệp không được sửa trong hồi quy thông thường

Trừ khi gói thay đổi đang kiểm nghiệm trực tiếp yêu cầu, không sửa:

```text
core/ham_ln_x.qmd
core/ham_ln_x.pdf
_quy_trinh/ho_so/ham_ln_x.yml
_figures/do_thi_ham_ln_x/
_data/cards.yml
```

Hồi quy phải kiểm tra hệ thống mới trên bài cũ, không điều chỉnh bài để làm checker mới vượt qua.

## 10. Khi nào chạy hồi quy

Chạy `scope` khi thay đổi:

- quy chuẩn lõi;
- cấu hình dự án;
- schema hoặc bộ đọc hồ sơ;
- validator trước render.

Chạy `render` khi thay đổi:

- validator sau render;
- metadata HTML;
- hệ PDF;
- Lua filter;
- TeX branding;
- cấu hình Quarto ảnh hưởng trực tiếp đến bài;
- logic xác định đầu ra.

Không lặp lại render khi thay đổi chỉ là tài liệu thiết kế.

## 11. Lệnh hồi quy chuẩn

Kiểm tra không render:

```bash
python scripts/zo_python.py scripts/zo_check_repo.py scope   content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/core/ham_ln_x.qmd
```

Kiểm tra có render:

```bash
python scripts/zo_python.py scripts/zo_check_repo.py render   content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/core/ham_ln_x.qmd
```

## 12. Điều kiện hồi quy đạt

- checker kết thúc với mã `0`;
- không xuất hiện `FAIL` mới;
- bài vẫn được nhận diện là bài của 100+ Hàm số;
- QMD không bị sửa ngoài ý muốn;
- metadata không đổi ngoài phạm vi;
- liên kết PDF vẫn hoạt động;
- PDF Title vẫn khớp;
- trạng thái thẻ vẫn là `pending`;
- không xuất bản;
- không có tệp ngoài phạm vi bị thay đổi.

## 13. Điều kiện phải dừng

Dừng tái cấu trúc và điều tra ngay khi:

- checker không còn nhận diện bài;
- validator dự án không chạy;
- metadata bắt buộc bị thay đổi;
- bài phải sửa chỉ để thích nghi với kiến trúc mới;
- trạng thái thẻ thay đổi;
- PDF biến mất hoặc metadata PDF sai;
- render khác bất thường mà không có lí do;
- diff chạm vào nội dung toán học của bài;
- xuất hiện thay đổi ngoài phạm vi.

## 14. Kết luận

`ham_ln_x.qmd` là ca hồi quy chính của hệ thống hiện hành.

Mục tiêu của việc tách lõi là chứng minh kiến trúc mới:

- bảo toàn hành vi đã nghiệm thu;
- loại bỏ điểm gắn cứng khỏi lõi;
- vẫn kích hoạt đúng mô-đun 100+ Hàm số;
- mở đường cho dự án thứ hai mà không làm suy yếu dự án thứ nhất.
