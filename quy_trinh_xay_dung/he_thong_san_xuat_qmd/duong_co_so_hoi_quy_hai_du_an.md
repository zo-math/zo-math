# Đường cơ sở hồi quy hai dự án của hệ thống QMD

> **Trạng thái:** Đường cơ sở vận hành — phiên bản 1.0.
>
> Tài liệu này phải được dùng khi thay đổi loader, registry, validator lõi, checker, dispatch adapter, schema cấu hình hoặc logic đầu ra có thể tác động nhiều dự án.

## 1. Mục tiêu

Đường cơ sở phải chứng minh đồng thời:

- một lõi phục vụ hai dự án;
- mỗi dự án nhận đúng adapter;
- dự án bài toán thực tế không mang metadata riêng của hàm số;
- bài hàm số không bị suy yếu;
- HTML/PDF vẫn hoạt động;
- trạng thái xuất bản không bị thay đổi;
- checker không tự nghiệm thu hoặc xuất bản.

## 2. Thành phần hệ thống cần bảo toàn

```text
scripts/zo_check_repo.py
scripts/zo_qmd_config.py
scripts/zo_qmd_core.py
scripts/zo_qmd_registry.py
scripts/zo_real_world_problem.py
```

Phiên bản đường cơ sở:

```text
checker: 2.6.0
schema: 1
validation mode: native
```

Các lệnh phải tiếp tục hoạt động:

```text
quick
scope
render
--staged
--report
```

## 3. Dự án 100+ Hàm số

### 3.1. Cấu hình

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/_quy_trinh/cau_hinh_san_xuat_qmd.yml
```

### 3.2. Bài hồi quy

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/core/ham_ln_x.qmd
```

### 3.3. Kế hoạch validator mong đợi

```text
project: functions_100
article_type: function_article
modules:
  - qmd-core
  - zo-html-pdf
  - content-blocks
  - functions-article
source adapter:
  - functions-article
render adapter:
  - functions-article
```

### 3.4. Bất biến nguồn

- front matter hợp lệ;
- không còn placeholder;
- đủ metadata lõi;
- có `listing-order: 114`;
- `body-classes` có `zo-page-article` và `zo-meta-hidden`;
- ảnh thẻ tồn tại và khớp thẻ 114;
- thẻ 114 giữ `status: pending`;
- `href` của thẻ giữ rỗng;
- PDF href là `ham_ln_x.pdf`;
- canonical URL khớp bài;
- hồ sơ hình phiên bản hiện hành hợp lệ;
- số hình mở rộng khai báo bằng 0;
- số hình mở rộng trong QMD bằng 0;
- không có lớp cũ hoặc cấu trúc LaTeX bị cấm;
- không sửa nội dung bài chỉ để checker vượt qua.

### 3.5. Bất biến đầu ra

- Quarto thoát 0;
- HTML tồn tại;
- `body` có hai lớp bắt buộc;
- HTML có đúng một H1;
- HTML có liên kết tới `ham_ln_x.pdf`;
- PDF vật lí tồn tại và được `pdfinfo` đọc;
- PDF Title là `Hàm số y = ln x`;
- số trang đường cơ sở là 15;
- trạng thái vẫn `pending`;
- checker ghi cảnh báo kiểm định trực quan thay vì tự nghiệm thu.

Số trang là tín hiệu hồi quy. Nó không phải bất biến tuyệt đối nếu có nhiệm vụ nội dung riêng đã được duyệt.

## 4. Dự án 100+ Bài toán thực tế

### 4.1. Cấu hình

```text
content/thpt/zo_math_100/100_bai_toan_thuc_te/_quy_trinh/cau_hinh_san_xuat_qmd.yml
```

### 4.2. Bài hồi quy

```text
content/thpt/zo_math_100/100_bai_toan_thuc_te/core/chi_phi_di_taxi.qmd
```

### 4.3. Kế hoạch validator mong đợi

```text
project: real_world_100
article_type: real_world_problem
modules:
  - qmd-core
  - zo-html-pdf
  - content-blocks
  - real-world-problem
source adapter:
  - real-world-problem
render adapter:
  - real-world-problem
```

### 4.4. Bất biến nguồn

- front matter hợp lệ;
- không còn placeholder;
- đủ metadata lõi;
- không có `listing-order`;
- `body-classes` có `zo-page-article` và `zo-meta-hidden`;
- ảnh đại diện tồn tại;
- PDF href là `chi_phi_di_taxi.pdf`;
- canonical URL khớp bài;
- hồ sơ phiên bản 1 hợp lệ;
- `production` là `in_production`;
- `publication` là `pending`;
- đủ các phần:
  - `Bối cảnh và dữ kiện`;
  - `Mô hình hóa`;
  - `Giải quyết`;
  - `Kiểm tra và diễn giải`;
- hình dùng đường dẫn tương đối và có văn bản thay thế;
- không có thao tác mã bị cấm.

### 4.5. Bất biến đầu ra

- Quarto thoát 0;
- HTML tồn tại;
- `body` có các lớp bắt buộc;
- HTML có đúng một H1;
- HTML có liên kết tới `chi_phi_di_taxi.pdf`;
- PDF tồn tại ở cạnh QMD và trong `docs` sau render;
- PDF Title là `Chi phí một chuyến taxi`;
- PDF khổ A4;
- số trang đường cơ sở là 4;
- trạng thái vẫn `pending`;
- checker ghi cảnh báo kiểm định trực quan thay vì tự nghiệm thu.

Bài này là ca kiểm nghiệm hệ thống. Đường cơ sở không tuyên bố bài đã được nghiệm thu nội dung để xuất bản.

## 5. Bất biến dùng chung

Cả hai bài phải:

- được khám phá qua cấu hình gần nhất;
- dùng `qmd-core`;
- chạy đúng source adapter;
- chạy đúng render adapter;
- không chạy adapter của dự án kia;
- kết thúc `scope` và `render` với mã 0;
- không có `FAIL`;
- giữ `FINAL ACCEPTANCE: NOT_RUN` khi còn yêu cầu người quan sát;
- không thay đổi QMD, hồ sơ, PDF hoặc dữ liệu xuất bản ngoài nhiệm vụ;
- không stage, commit hoặc xuất bản do checker thực hiện.

## 6. Self-test bắt buộc khi đổi lõi

```bash
python scripts/zo_python.py scripts/zo_qmd_config.py self-test
python scripts/zo_python.py scripts/zo_qmd_registry.py self-test
python scripts/zo_python.py scripts/zo_qmd_core.py self-test
python scripts/zo_python.py scripts/zo_real_world_problem.py self-test
```

Kết quả mong đợi:

```text
PASS: zo_qmd_config self-test
PASS: zo_qmd_registry self-test
PASS: zo_qmd_core self-test
PASS: zo_real_world_problem self-test
```

## 7. Lệnh hồi quy nguồn hai dự án

```bash
FUNCTION_ARTICLE='content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/core/ham_ln_x.qmd'
REAL_ARTICLE='content/thpt/zo_math_100/100_bai_toan_thuc_te/core/chi_phi_di_taxi.qmd'

python scripts/zo_python.py scripts/zo_check_repo.py scope \
  "$FUNCTION_ARTICLE" \
  "$REAL_ARTICLE"
```

Dấu hiệu chính:

```text
CHECKER VERSION: 2.6.0
project='functions_100'
article_type='function_article'
source=['functions-article']
project='real_world_100'
article_type='real_world_problem'
source=['real-world-problem']
AUTOMATED RESULT: PASS_WITH_WARNINGS | EXIT=0
```

## 8. Lệnh hồi quy render hai dự án

```bash
FUNCTION_ARTICLE='content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/core/ham_ln_x.qmd'
REAL_ARTICLE='content/thpt/zo_math_100/100_bai_toan_thuc_te/core/chi_phi_di_taxi.qmd'

python scripts/zo_python.py scripts/zo_check_repo.py render \
  "$FUNCTION_ARTICLE" \
  "$REAL_ARTICLE"
```

Dấu hiệu chính:

```text
PASS quarto-render
PASS render-html
PASS qmd-render-adapter
AUTOMATED RESULT: PASS_WITH_WARNINGS | EXIT=0
```

## 9. Báo cáo JSON

Khi thay đổi lõi hoặc chuẩn bị khóa phiên bản, ghi một báo cáo chung:

```bash
python scripts/zo_python.py scripts/zo_check_repo.py scope \
  "$FUNCTION_ARTICLE" \
  "$REAL_ARTICLE" \
  --report _audit/qmd_two_project_regression.json
```

Báo cáo phải nằm trong `_audit/` và không cần commit trừ khi nhiệm vụ yêu cầu lưu bằng chứng lâu dài.

## 10. Khi nào chỉ chạy `scope`

Chỉ cần `scope` khi thay đổi:

- tài liệu;
- schema mô tả nhưng không đổi mã;
- placeholder;
- metadata nguồn;
- logic kiểm tra trước render;
- cấu hình không ảnh hưởng đường tạo đầu ra.

Vẫn phải chạy self-test nếu sửa loader, registry hoặc validator lõi.

## 11. Khi nào bắt buộc chạy `render`

Bắt buộc chạy `render` khi thay đổi:

- logic dispatch sau render;
- cách xác định HTML đầu ra;
- kiểm tra lớp trang hoặc H1 trong HTML;
- liên kết hoặc tài nguyên PDF;
- Quarto, Lua filter hoặc TeX;
- metadata đầu ra;
- logic sao chép PDF vào `docs`;
- adapter sau render.

## 12. Kiểm tra index trước commit

Sau khi worktree đạt:

```bash
git add -- <chi_dung_cac_tep_trong_pham_vi>

python scripts/zo_python.py scripts/zo_check_repo.py scope --staged \
  <chi_dung_cac_tep_da_stage>

git diff --cached --check
git --no-pager diff --cached --name-status
git --no-pager diff --cached --stat
```

Không dùng `git add .`.

## 13. Điều kiện hồi quy đạt

- bốn self-test đạt khi áp dụng;
- checker phiên bản mong đợi;
- hai cấu hình hợp lệ;
- hai bài được nhận diện đúng;
- đúng source adapter và render adapter;
- không có `FAIL`;
- QMD hồi quy không bị sửa ngoài nhiệm vụ;
- PDF và metadata không đổi ngoài dự kiến;
- trạng thái xuất bản vẫn `pending`;
- không có tệp ngoài phạm vi bị stage;
- không xuất bản.

## 14. Điều kiện phải dừng

Dừng và điều tra khi:

- một bài không còn tìm thấy cấu hình;
- một bài không còn khớp loại bài;
- kế hoạch validator thiếu adapter dự án;
- adapter của dự án này chạy cho dự án kia;
- `qmd-core-validator` biến mất ở một bài;
- bài hàm số phải sửa để checker mới vượt qua;
- bài thực tế bị buộc thêm `listing-order`;
- thẻ 114 hoặc hồ sơ bài taxi đổi sang `published`;
- PDF biến mất hoặc metadata PDF sai;
- render xuất hiện lỗi hoặc khác biệt bất thường;
- diff lan sang nội dung ngoài phạm vi;
- xuất hiện lại đường legacy hoặc khóa `compatibility`.

## 15. Kết luận

Đường cơ sở hai dự án là cổng bảo vệ phiên bản 1.0.

Mọi thay đổi lõi chỉ được xem là an toàn khi chứng minh đồng thời:

```text
100+ Hàm số không suy yếu
và
100+ Bài toán thực tế không bị đồng hóa thành bài hàm số
```
