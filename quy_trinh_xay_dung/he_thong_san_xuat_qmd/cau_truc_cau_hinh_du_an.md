# Cấu trúc cấu hình dự án cho hệ thống QMD

> **Trạng thái:** Bản thiết kế schema v1.0 — Giai đoạn 1.
>
> Ví dụ trong tài liệu này chưa phải tệp cấu hình đang hoạt động.

## 1. Vị trí chuẩn

Mỗi dự án đặt cấu hình tại:

```text
<goc_du_an>/_quy_trinh/cau_hinh_san_xuat_qmd.yml
```

Checker tìm cấu hình gần nhất bằng cách đi từ bài lên các thư mục cha.

## 2. Nguyên tắc schema

- dùng YAML dữ liệu thuần;
- không chứa mã thực thi;
- không chứa tên hàm Python;
- đường dẫn là tương đối với gốc repository hoặc gốc dự án theo trường đã định;
- mã mô-đun phải thuộc registry cố định;
- khóa không biết là lỗi cấu hình, trừ vùng `extensions`;
- phiên bản schema là bắt buộc.

## 3. Khung tổng quát

```yaml
schema_version: 1

project:
  id: functions_100
  name: "100+ Hàm số: Sự biến thiên và đồ thị"
  root: content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi

discovery:
  article_types:
    - id: function_article
      include:
        - core/**/*.qmd
        - depth/**/*.qmd
      exclude: []

profiles:
  directory: _quy_trinh/ho_so
  naming: by_article_stem
  required: true

modules:
  required:
    - qmd-core
    - zo-html-pdf
    - content-blocks
    - functions-article
  optional:
    - figure-layout
    - card-grid

metadata:
  core_required: []
  project_required:
    - listing-order
  body_classes_required:
    - zo-page-article
    - zo-meta-hidden
  placeholders: []

publication:
  production_states:
    - draft
    - in_production
    - validated
    - accepted
  publication_states:
    - pending
    - published
  user_confirmation_required: true

catalog:
  module: card-grid
  data: _data/cards.yml
  key:
    article_metadata: listing-order
    item_field: number
  status_field: status
  href_field: href

references:
  controlling_documents: []
  templates: []
  theory_sources: []

regression:
  articles: []
  expected_checker_version: null
  preserve_cli: true

compatibility:
  mode: legacy
  legacy_validator: functions-article

extensions: {}
```

## 4. Giải thích các nhóm trường

### 4.1. `schema_version`

Phiên bản cấu trúc cấu hình. Checker phải từ chối phiên bản không hỗ trợ.

### 4.2. `project`

- `id`: mã ổn định, không dấu, không đổi tùy tiện;
- `name`: tên hiển thị;
- `root`: đường dẫn từ gốc repository.

`project.root` phải khớp vị trí thực tế của tệp cấu hình.

### 4.3. `discovery.article_types`

Mỗi loại bài khai báo:

- `id`;
- mẫu `include`;
- mẫu `exclude`;
- mô-đun bổ sung nếu cần;
- mẫu hồ sơ nếu nhiều loại bài dùng hồ sơ khác nhau.

Một đường dẫn chỉ được khớp đúng một loại bài. Khớp nhiều loại là lỗi.

### 4.4. `profiles`

- `directory`: thư mục hồ sơ;
- `naming`: quy tắc ánh xạ từ bài sang hồ sơ;
- `required`: bài có bắt buộc có hồ sơ hay không.

Giai đoạn đầu chỉ hỗ trợ `by_article_stem` để tránh phức tạp.

### 4.5. `modules`

- `required`: luôn chạy với bài thuộc dự án;
- `optional`: chỉ chạy khi hồ sơ hoặc loại bài kích hoạt.

Mã mô-đun phải có trong registry Python.

### 4.6. `metadata`

- `core_required`: chỉ dùng để bổ sung trường lõi đã định nghĩa, không xóa trường lõi;
- `project_required`: trường riêng của dự án;
- `body_classes_required`: lớp HTML bắt buộc;
- `placeholders`: placeholder riêng.

### 4.7. `publication`

Tách hai trục:

- trạng thái sản xuất;
- trạng thái xuất bản.

`user_confirmation_required` phải là `true` đối với mọi dự án công khai của ZO Math.

### 4.8. `catalog`

Nhóm tùy chọn dành cho dự án có dữ liệu danh mục hoặc lưới thẻ.

Nó khai báo:

- mã mô-đun;
- đường dẫn dữ liệu;
- cách nối bài với mục dữ liệu;
- trường trạng thái;
- trường liên kết.

Dự án không có danh mục bỏ toàn bộ nhóm này.

### 4.9. `references`

Liệt kê rõ các nguồn có thẩm quyền:

- tài liệu điều khiển;
- mẫu;
- nguồn lí thuyết.

Tệp không được dẫn chiếu không tự động có hiệu lực.

### 4.10. `regression`

- các bài hồi quy;
- phiên bản checker đường cơ sở;
- yêu cầu giữ giao diện lệnh.

### 4.11. `compatibility`

Dùng trong giai đoạn chuyển đổi:

```yaml
mode: legacy
```

Sau khi hoàn tất:

```yaml
mode: native
```

### 4.12. `extensions`

Vùng dự phòng có namespace theo dự án. Checker lõi không diễn giải nội dung này nếu mô-đun tương ứng không đăng kí schema.

## 5. Cấu hình dự kiến cho 100+ Hàm số

Bản đầu tiên nên khai báo:

- `project.id: functions_100`;
- hai thư mục bài `core/` và `depth/`;
- hồ sơ trong `_quy_trinh/ho_so`;
- mô-đun `functions-article`;
- mô-đun `card-grid`;
- `listing-order`;
- `_data/cards.yml`;
- bài hồi quy `core/ham_ln_x.qmd`;
- chế độ `legacy`.

Không chuyển toàn bộ hằng `FUNCTION_*` vào YAML trong một lần. Chỉ chuyển dữ liệu cấu hình, giữ logic validator trong Python.

## 6. Cấu hình dự kiến cho 100+ Bài toán thực tế

Chỉ tạo sau khi lõi tối thiểu ổn định.

Dự án thứ hai sẽ:

- có `project.id` riêng;
- có loại bài `real_world_problem`;
- không khai báo trường hàm số;
- kích hoạt mô-đun `real-world-problem`;
- dùng cùng validator lõi HTML/PDF;
- có hồ sơ mở rộng riêng;
- có một bài hồi quy đại diện.

## 7. Kiểm tra cấu hình

Checker phải xác nhận:

- YAML hợp lệ và không có khóa trùng;
- schema version được hỗ trợ;
- root tồn tại và khớp vị trí;
- glob hợp lệ;
- loại bài không chồng lấn;
- thư mục hồ sơ tồn tại khi bắt buộc;
- mã mô-đun đã đăng kí;
- đường dẫn không thoát repository;
- trạng thái hợp lệ;
- cổng xuất bản không bị tắt;
- bài hồi quy tồn tại.

## 8. Kết luận

Cấu hình dự án là lớp dữ liệu cục bộ, có thể kiểm tra và không thực thi mã.

Nó chuyển các điểm gắn cứng ra khỏi checker nhưng không biến YAML thành một ngôn ngữ lập trình mới.
