# Bản đồ kiến trúc hiện trạng của hệ thống QMD

> **Trạng thái:** Bản đồ quan sát của Giai đoạn 0.
>
> Tài liệu này mô tả hệ thống đang tồn tại. Các ranh giới đích chưa được xem là quyết định kiến trúc chính thức.

## 1. Toàn cảnh hiện tại

Hệ thống đang vận hành theo các tầng sau:

```text
chỉ dẫn cấp repository
        ↓
chỉ dẫn cấp dự án
        ↓
quy trình sản xuất bài hàm số
        ↓
quy chuẩn nội dung + quy chuẩn kĩ thuật
        ↓
hồ sơ sản xuất + mẫu QMD
        ↓
QMD + tài nguyên
        ↓
checker
        ↓
HTML + PDF
        ↓
kiểm định có người quan sát
        ↓
nghiệm thu
        ↓
pending
        ↓
published khi người dùng xác nhận
```

## 2. Tầng điều phối

### Cấp repository

```text
AGENTS.md
├── quy_tac_lam_viec_voi_agent.md
└── quy_trinh_thuc_hien_nhiem_vu_ky_thuat.md
```

Vai trò:

- xác định nguyên tắc làm việc;
- khóa phạm vi;
- điều phối công cụ;
- xác định cách kiểm tra;
- quy định quyền quyết định của người dùng;
- ngăn thao tác tự động có tính phá hủy hoặc xuất bản.

### Cấp dự án 100+ Hàm số

```text
content/.../100_ham_so_su_bien_thien_va_do_thi/AGENTS.md
```

Vai trò:

- kích hoạt ba tài liệu điều khiển bài hàm số;
- xác định mẫu và hồ sơ bắt buộc;
- kích hoạt tài liệu khối, đồ thị và phong cách theo điều kiện;
- phân biệt trang công khai với nguồn điều khiển;
- giới hạn quyền sửa tài liệu điều khiển.

## 3. Tầng nghiệp vụ dự án

```text
_quy_trinh/
├── quy_trinh_tao_bai_ham_so.md
├── quy_chuan_khao_sat_ham_so.md
├── quy_chuan_ki_thuat_bai_ham_so_qmd.md
├── mau_ki_thuat_qmd.qmd
├── ho_so_san_xuat_mac_dinh.yml
├── ho_so/
└── nguon_li_thuyet/
```

Quan hệ chính:

```text
quy_trinh_tao_bai_ham_so.md
├── gọi quy_chuan_khao_sat_ham_so.md
├── gọi quy_chuan_ki_thuat_bai_ham_so_qmd.md
├── khởi tạo từ ho_so_san_xuat_mac_dinh.yml
├── tạo QMD từ mau_ki_thuat_qmd.qmd
└── đối chiếu dữ liệu dự án và tài nguyên
```

## 4. Tầng bài viết

Một bài hiện gồm nhiều loại tài sản:

```text
bài.qmd
bài.pdf
hồ_sơ_bài.yml
hình nguồn .tex
hình trung gian .pdf
hình web .svg
metadata trong _quarto.yml
dữ liệu thẻ trong cards.yml
```

Không phải bài nào cũng cần toàn bộ loại tài sản trên, nhưng hồ sơ sản xuất phải xác định rõ cái nào áp dụng.

## 5. Luồng sản xuất bài hiện tại

```text
yêu cầu của người dùng
        ↓
khóa đơn vị khảo sát
        ↓
tìm thẻ và đường dẫn
        ↓
khởi tạo hồ sơ
        ↓
vòng rà toán học
        ↓
mệnh đề–chứng cứ
        ↓
hiện tượng trung tâm
        ↓
đề cương vận hành
        ↓
đặc tả bảng và hình
        ↓
tạo QMD và tài nguyên
        ↓
kiểm định nội dung
        ↓
checker scope hoặc render
        ↓
quan sát HTML và PDF
        ↓
nghiệm thu
        ↓
bàn giao ở trạng thái pending
```

Các bước từ vòng rà toán học đến đề cương vận hành là nghiệp vụ chuyên biệt của dự án hàm số.

Các bước từ khóa phạm vi đến bàn giao có phần đáng kể có thể khái quát hóa.

## 6. Kiến trúc checker hiện tại

### 6.1. Luồng chung

```text
main()
  ├── parser()
  ├── find_repo_root()
  ├── expand_paths()
  ├── run_scope()
  │     └── validate_file()
  └── render_pages()
        ├── run_scope()
        ├── Quarto render
        └── kiểm tra HTML sau render
```

### 6.2. Nhận diện bài hàm số

```text
is_function_article(relative)
```

Điều kiện hiện hành:

- phần mở rộng `.qmd`;
- nằm dưới `core/` hoặc `depth/` của dự án 100+ Hàm số.

### 6.3. Kiểm tra trước render

Trong `validate_file()`:

```text
kiểm tra tệp chung
        ↓
validate_markdown()
        ↓
nếu là bài hàm số
        ↓
validate_function_article()
```

`validate_function_article()` tiếp tục gọi:

```text
validate_function_metadata()
validate_function_body()
```

### 6.4. Kiểm tra sau render

Trong `render_pages()`:

```text
render QMD
        ↓
xác nhận HTML tồn tại
        ↓
nếu là bài hàm số
        ↓
validate_rendered_function_page()
```

Bộ kiểm tra sau render hiện xác nhận:

- lớp `body`;
- số lượng `H1`;
- liên kết PDF;
- tài nguyên PDF;
- quan hệ với trạng thái thẻ;
- yêu cầu quan sát trực tiếp.

### 6.5. Lưới thẻ

Lưới thẻ có luồng riêng:

```text
card_scope()
        ↓
check_card_grid()
```

Nó kiểm tra:

- cấu trúc dữ liệu;
- định danh;
- trạng thái;
- tài nguyên;
- liên kết;
- partial được sinh;
- SVG.

Lưới thẻ là một mô-đun dự án hoặc mô-đun giao diện, không đồng nhất với toàn bộ hệ thống kiểm định QMD.

## 7. Ranh giới sơ bộ giữa lõi và dự án

### 7.1. Ứng viên cho lõi dùng chung

- nhận diện nhiệm vụ;
- khóa phạm vi;
- hồ sơ nhận diện;
- đường dẫn;
- tài liệu điều khiển;
- phạm vi được sửa;
- hợp đồng YAML;
- metadata dùng chung;
- cấu trúc QMD;
- tài nguyên;
- khối nội dung;
- HTML;
- PDF;
- render;
- kiểm định tự động;
- kiểm định có người quan sát;
- bằng chứng kiểm định;
- nghiệm thu;
- bàn giao;
- cổng xuất bản;
- báo cáo JSON;
- giao diện lệnh checker.

### 7.2. Thành phần riêng của 100+ Hàm số

- đơn vị khảo sát là hàm số hoặc họ hàm;
- bản đồ miền;
- vòng rà toán học;
- hồ sơ mệnh đề–chứng cứ;
- hiện tượng trung tâm của hàm số;
- quy chuẩn khảo sát hàm số;
- `core/` và `depth/`;
- `_data/cards.yml`;
- `listing-order`;
- số thẻ;
- collection của dự án;
- nguồn lí thuyết khảo sát hàm số;
- đồ thị hàm số;
- bảng dấu;
- bảng biến thiên.

### 7.3. Thành phần chưa đủ bằng chứng để khóa

- cấu trúc chính xác của hồ sơ lõi;
- cách biểu diễn phần mở rộng trong YAML;
- tên và vị trí tệp cấu hình dự án;
- cách đăng kí validator;
- mức độ tổng quát của metadata PDF;
- quan hệ giữa trạng thái bài và trạng thái thẻ;
- việc lưới thẻ thuộc lõi hay mô-đun tùy chọn;
- cấu trúc thư mục của dự án thứ hai.

Những điểm này phải được quyết định trong Giai đoạn 1, không suy ra chỉ từ hệ thống hàm số.

## 8. Các điểm gắn cứng cần xử lí sau này

### Trong tài liệu

- tên dự án;
- tên loại bài;
- `core/`;
- `depth/`;
- `_data/cards.yml`;
- `listing-order`;
- bài tham chiếu;
- nguồn lí thuyết;
- quy chuẩn khảo sát hàm số.

### Trong mẫu QMD

- tiêu đề “Hàm số”;
- collection;
- hình thẻ;
- `listing-order`;
- hướng dẫn đối chiếu thẻ;
- đường dẫn dự án.

### Trong hồ sơ

- bản đồ miền;
- tham số hàm;
- mệnh đề–chứng cứ toán học;
- hồ sơ biểu diễn hàm số;
- thẻ dự án;
- tài liệu điều khiển được viết cứng.

### Trong checker

- `CARD_PROJECT`;
- `FUNCTION_ARTICLE_DIRS`;
- metadata bắt buộc;
- placeholder;
- lớp cũ;
- màu khối;
- canonical base;
- thư mục hồ sơ;
- lớp hình mở rộng;
- nhận diện bài;
- liên kết thẻ;
- validator trước và sau render.

## 9. Rủi ro kiến trúc

### 9.1. Tổng quát hóa quá sớm

Một quy tắc hợp lí cho bài khảo sát hàm số chưa chắc hợp lí cho bài toán thực tế.

Biện pháp:

- chỉ đưa vào lõi những phần có bằng chứng dùng chung;
- kiểm nghiệm bằng dự án thứ hai trước khi khóa.

### 9.2. Viết lại checker

Viết lại toàn bộ có thể làm mất các kiểm tra đã được kiểm nghiệm.

Biện pháp:

- giữ nguyên luồng chung;
- thêm cơ chế cấu hình;
- chuyển từng nhóm validator;
- chạy hồi quy sau mỗi bước.

### 9.3. Sao chép tài liệu

Sao chép quy chuẩn vào lõi tạo ra nhiều nguồn có thẩm quyền cạnh tranh.

Biện pháp:

- trích phần chung;
- dẫn chiếu phần chuyên biệt;
- xác định rõ thứ tự thẩm quyền.

### 9.4. Hồ sơ quá lớn

Hồ sơ mặc định hiện tại chứa nhiều trường chuyên sâu của hàm số.

Biện pháp:

- tách hồ sơ lõi tối thiểu;
- nạp phần mở rộng theo dự án;
- không bắt dự án khác điền trường không áp dụng.

### 9.5. Làm thay đổi bài đã nghiệm thu

Tái cấu trúc có thể làm thay đổi metadata, HTML hoặc PDF của `ham_ln_x`.

Biện pháp:

- dùng bài này làm đường cơ sở hồi quy;
- không sửa nội dung bài trong quá trình tách lõi;
- so sánh kết quả kiểm định trước và sau.

## 10. Điểm mở rộng có triển vọng

Kiến trúc hiện tại cho phép thay:

```python
if is_function_article(relative):
    validate_function_article(...)
```

bằng cơ chế định hướng:

```text
xác định cấu hình dự án
        ↓
xác định loại bài
        ↓
chạy validator lõi
        ↓
chạy validator dự án
```

Tương tự, nhánh sau render có thể chuyển từ:

```text
validate_rendered_function_page()
```

sang:

```text
validate_rendered_page_core()
+ validator sau render của dự án
```

Các lệnh `quick`, `scope`, `render`, cách gọi Quarto và định dạng báo cáo không cần thay đổi chỉ để đạt mục tiêu này.

## 11. Kết luận

Hệ thống hiện tại đã có một lõi tiềm ẩn nhưng lõi ấy chưa được biểu diễn thành tầng riêng. Phần dùng chung và phần chuyên biệt đang đan xen trong:

- quy trình;
- quy chuẩn kĩ thuật;
- mẫu QMD;
- hồ sơ;
- checker.

Nhiệm vụ tiếp theo không phải tạo thêm chức năng, mà là lập bảng phân loại từng nhóm quy tắc theo ba trạng thái:

```text
dùng chung chắc chắn
riêng cho 100+ Hàm số
chưa đủ căn cứ
```

Bảng phân loại đó sẽ là đầu vào trực tiếp cho thiết kế kiến trúc ở Giai đoạn 1.
