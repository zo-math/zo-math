# Cấu trúc cấu hình dự án cho hệ thống QMD

> **Trạng thái:** Schema vận hành v1.0.
>
> Tài liệu này mô tả cấu trúc được `scripts/zo_qmd_config.py` chấp nhận tại checker 2.6.0.

## 1. Vị trí chuẩn

Mỗi dự án đặt cấu hình tại:

```text
<project.root>/_quy_trinh/cau_hinh_san_xuat_qmd.yml
```

Checker tìm cấu hình gần nhất bằng cách đi từ bài lên các thư mục cha.

Loader xác nhận vị trí vật lí của tệp khớp chính xác với `project.root`. Cấu hình đặt sai vị trí bị từ chối.

## 2. Nguyên tắc schema

- dùng YAML dữ liệu thuần;
- không chứa mã thực thi;
- không chứa tên hàm Python;
- khóa trùng bị từ chối;
- khóa không biết bị từ chối, trừ nội dung bên trong `extensions`;
- đường dẫn phải là tương đối và không chứa `..`;
- mã mô-đun phải thuộc registry cố định;
- `qmd-core` là mô-đun bắt buộc;
- phiên bản schema là bắt buộc;
- cổng xác nhận xuất bản không thể bị tắt.

## 3. Khung tổng quát

```yaml
schema_version: 1

project:
  id: ma_du_an
  name: "Tên dự án"
  root: content/duong_dan_den_du_an

discovery:
  article_types:
    - id: ma_loai_bai
      include:
        - core/*.qmd
        - core/**/*.qmd
      exclude:
        - core/*_luu_kho.qmd
        - core/**/*_luu_kho.qmd

profiles:
  directory: _quy_trinh/ho_so
  naming: by_article_stem
  required: true

modules:
  required:
    - qmd-core
    - zo-html-pdf
    - content-blocks
    - ma_validator_du_an
  optional:
    - figure-layout

metadata:
  core_required:
    - title
    - title-meta
    - subtitle
    - pagetitle
    - summary
    - description
    - image
    - abstract
    - keywords
    - author
    - date
    - date-format
    - page-layout
    - toc
    - toc-title
    - toc-location
    - toc-depth
    - body-classes
    - zo-pdf-download
    - zo-pdf-branding
  project_required: []
  body_classes_required:
    - zo-page-article
    - zo-meta-hidden
  placeholders:
    - CHƯA XÁC ĐỊNH
    - CHUA_XAC_DINH

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

references:
  controlling_documents:
    - AGENTS.md
  templates:
    - _quy_trinh/ho_so_san_xuat_mac_dinh.yml
  theory_sources: []

regression:
  articles:
    - core/bai_hoi_quy.qmd
  expected_checker_version: "2.6.0"
  preserve_cli: true

extensions: {}
```

Khi dự án có danh mục hoặc lưới thẻ, có thể thêm nhóm `catalog` được mô tả ở mục 4.9.

## 4. Các nhóm trường

### 4.1. `schema_version`

Phiên bản hiện hỗ trợ:

```yaml
schema_version: 1
```

Giá trị khác bị từ chối.

### 4.2. `project`

```yaml
project:
  id: ma_du_an
  name: "Tên dự án"
  root: content/duong_dan_den_du_an
```

Ràng buộc:

- đủ ba khóa `id`, `name`, `root`;
- `id` và `name` là chuỗi không rỗng;
- `root` là đường dẫn tương đối không chứa `..`;
- tệp cấu hình phải nằm đúng tại `<root>/_quy_trinh/cau_hinh_san_xuat_qmd.yml`.

### 4.3. `discovery.article_types`

```yaml
discovery:
  article_types:
    - id: real_world_problem
      include:
        - core/*.qmd
        - core/**/*.qmd
      exclude:
        - core/*_luu_kho.qmd
        - core/**/*_luu_kho.qmd
```

Ràng buộc:

- danh sách không rỗng;
- mỗi loại bài có `id`, `include`, `exclude`;
- `id` không trùng trong cùng dự án;
- các mẫu là chuỗi không rỗng;
- khi một đường dẫn khớp nhiều loại bài, loader báo lỗi tại lúc xác định bài;
- một tệp nằm trong dự án nhưng không khớp loại bài nào chỉ nhận kiểm tra chung của phạm vi, không chạy adapter dự án.

Mẫu glob được so với đường dẫn tương đối bên trong `project.root`.

### 4.4. `profiles`

```yaml
profiles:
  directory: _quy_trinh/ho_so
  naming: by_article_stem
  required: true
```

Phiên bản 1 chỉ hỗ trợ:

```text
naming: by_article_stem
```

Với bài:

```text
core/ten_bai.qmd
```

đường dẫn hồ sơ là:

```text
<project.root>/<profiles.directory>/ten_bai.yml
```

`required` phải là boolean. Việc kiểm tra nội dung và sự tồn tại của hồ sơ thuộc adapter dự án.

### 4.5. `modules`

```yaml
modules:
  required:
    - qmd-core
    - zo-html-pdf
    - content-blocks
    - real-world-problem
  optional:
    - figure-layout
```

Registry phiên bản 1.0:

```text
qmd-core
zo-html-pdf
content-blocks
figure-layout
card-grid
functions-article
real-world-problem
```

Ràng buộc:

- `required` không rỗng;
- `required` phải chứa `qmd-core`;
- một mã không được vừa `required` vừa `optional`;
- mã chưa đăng kí bị từ chối;
- danh sách không được có phần tử trùng.

Ý nghĩa vận hành:

- `required` tạo danh sách mô-đun hoạt động;
- `optional` khai báo khả năng dự án có thể dùng nhưng không tự động kích hoạt adapter trong phiên bản 1.0;
- source/render adapter chỉ chạy khi mô-đun tương ứng là `required`, có `article_type` phù hợp và đã được cài trong checker.

### 4.6. `metadata`

```yaml
metadata:
  core_required:
    - title
    - title-meta
  project_required:
    - listing-order
  body_classes_required:
    - zo-page-article
    - zo-meta-hidden
  placeholders:
    - CHƯA XÁC ĐỊNH
```

Bốn danh sách đều bắt buộc tồn tại, nhưng có thể rỗng khi hợp đồng dự án cho phép.

- `core_required`: metadata nền mà dự án yêu cầu lõi kiểm tra;
- `project_required`: metadata bổ sung chỉ thuộc dự án;
- `body_classes_required`: lớp `body` bắt buộc trong QMD và HTML;
- `placeholders`: chuỗi giữ chỗ phải bị chặn.

Loader chỉ kiểm tra kiểu dữ liệu và giá trị trùng. Validator lõi và validator dự án chịu trách nhiệm kiểm tra front matter thực tế.

### 4.7. `publication`

Cấu trúc bị khóa ở phiên bản 1:

```yaml
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
```

Thứ tự và giá trị phải khớp chính xác.

Giá trị sau luôn bị từ chối:

```yaml
user_confirmation_required: false
```

Cấu hình chỉ khai báo hợp đồng trạng thái. Checker không tự chuyển trạng thái.

### 4.8. `references`

```yaml
references:
  controlling_documents:
    - AGENTS.md
    - _quy_trinh/quy_chuan_noi_dung.md
  templates:
    - _quy_trinh/ho_so_san_xuat_mac_dinh.yml
  theory_sources: []
```

Ba danh sách đều bắt buộc tồn tại.

Loader phiên bản 1 kiểm tra chúng là danh sách chuỗi không trùng. Việc xác nhận tệp có tồn tại và có thẩm quyền thuộc quy trình dự án và nhiệm vụ cụ thể.

### 4.9. `catalog`

`catalog` là nhóm top-level tùy chọn. Ví dụ của dự án 100+ Hàm số:

```yaml
catalog:
  module: card-grid
  data: _data/cards.yml
  key:
    article_metadata: listing-order
    item_field: number
  status_field: status
  href_field: href
```

Ràng buộc:

- `module` phải đã đăng kí;
- `module` phải xuất hiện trong `modules.required` hoặc `modules.optional`;
- `data` là đường dẫn tương đối không chứa `..`;
- `key` phải có `article_metadata` và `item_field`;
- `status_field` và `href_field` là chuỗi không rỗng.

Logic khớp bài với danh mục thuộc validator dự án.

### 4.10. `regression`

```yaml
regression:
  articles:
    - core/bai_hoi_quy.qmd
  expected_checker_version: "2.6.0"
  preserve_cli: true
```

Ràng buộc:

- `articles` là danh sách đường dẫn tương đối bên trong dự án;
- đường dẫn không được chứa `..`;
- `expected_checker_version` là chuỗi không rỗng hoặc `null`;
- `preserve_cli` là boolean.

Loader xác nhận an toàn đường dẫn, không tự chạy hồi quy và không dùng trường này để sửa checker. Quy trình hồi quy phải gọi checker trên các bài đã khai báo.

### 4.11. `extensions`

```yaml
extensions: {}
```

`extensions` phải là mapping. Loader lõi không kiểm tra các khóa bên trong; adapter dự án chịu trách nhiệm diễn giải và từ chối cấu trúc không hợp lệ.

Ví dụ của dự án bài toán thực tế:

```yaml
extensions:
  real_world_problem:
    required_sections:
      - Bối cảnh và dữ kiện
      - Mô hình hóa
      - Giải quyết
      - Kiểm tra và diễn giải
    forbidden_metadata:
      - listing-order
    collection: "100+ Bài toán thực tế"
    canonical_base: "https://zo-math.github.io/zo-math/"
    display_url: "zo-math.github.io/zo-math"
    profile_version: 1
```

Không đưa tên hàm Python hoặc đường import vào `extensions`.

## 5. Hai cấu hình đang hoạt động

### 5.1. 100+ Hàm số

```text
project.id: functions_100
article_type: function_article
required adapter module: functions-article
project metadata: listing-order
catalog: card-grid + _data/cards.yml
regression article: core/ham_ln_x.qmd
```

### 5.2. 100+ Bài toán thực tế

```text
project.id: real_world_100
article_type: real_world_problem
required adapter module: real-world-problem
project metadata: không có
forbidden metadata: listing-order
regression article: core/chi_phi_di_taxi.qmd
```

Dự án thứ hai dùng cùng metadata lõi nhưng không mang trường riêng của hàm số.

## 6. Khóa đã loại bỏ

Schema phiên bản 1 không có:

```yaml
compatibility:
legacy_validator:
```

Các khóa này bị xem là khóa top-level không hỗ trợ.

Bản tóm tắt của loader và kế hoạch validator vẫn có thể hiển thị:

```json
"compatibility_mode": "native"
```

Đây là trường đầu ra để giữ định dạng báo cáo ổn định, không phải khóa cấu hình.

## 7. Lệnh kiểm tra cấu hình

### 7.1. Kiểm tra một tệp cấu hình

```bash
python scripts/zo_python.py scripts/zo_qmd_config.py check \
  <duong_dan_den_cau_hinh>
```

### 7.2. Khám phá cấu hình và loại bài

```bash
python scripts/zo_python.py scripts/zo_qmd_config.py inspect \
  <duong_dan_den_bai_qmd>
```

### 7.3. Self-test loader

```bash
python scripts/zo_python.py scripts/zo_qmd_config.py self-test
```

## 8. Các lỗi cấu hình phải dừng

Dừng khi:

- YAML có khóa trùng hoặc sai cú pháp;
- `schema_version` không được hỗ trợ;
- cấu hình nằm sai vị trí so với `project.root`;
- đường dẫn chứa `..` hoặc thoát repository;
- loại bài trùng `id`;
- một bài khớp nhiều loại bài;
- hồ sơ dùng quy tắc đặt tên chưa hỗ trợ;
- mô-đun chưa đăng kí;
- `qmd-core` không nằm trong `required`;
- mô-đun vừa `required` vừa `optional`;
- trạng thái không đúng thứ tự đã khóa;
- `user_confirmation_required` không phải `true`;
- `catalog.module` không được khai báo trong dự án;
- xuất hiện khóa top-level không thuộc schema.

## 9. Kết luận

Cấu hình dự án là lớp dữ liệu cục bộ, có thể kiểm tra và không thực thi mã.

Nó chuyển các điểm gắn cứng ra khỏi checker nhưng không biến YAML thành một ngôn ngữ lập trình mới. Logic validator vẫn nằm trong Python và chỉ được kích hoạt qua registry an toàn.
