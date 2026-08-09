# Hướng dẫn thêm dự án và validator vào hệ thống QMD

> **Trạng thái:** Hướng dẫn vận hành — phiên bản 1.0.
>
> Hướng dẫn này áp dụng cho việc thêm một dự án QMD mới mà không sao chép checker hiện hành. Mỗi bước phải tuân theo `AGENTS.md`, phạm vi nhiệm vụ và quy tắc Git của repository.

## 1. Nguyên tắc

Một dự án mới chỉ nên thêm:

- cấu hình cục bộ;
- quy chuẩn chuyên biệt;
- hồ sơ sản xuất;
- một bài hồi quy đại diện;
- validator dự án khi thực sự cần.

Không sao chép toàn bộ:

- `scripts/zo_check_repo.py`;
- `scripts/zo_qmd_core.py`;
- hệ thống HTML/PDF;
- vòng đời bài;
- cổng xuất bản.

Không đưa quy tắc chuyên biệt vào lõi chỉ vì một dự án mới cần nó.

## 2. Điều kiện trước khi bắt đầu

Phải xác định:

- tên và `project.id`;
- đường dẫn gốc dự án;
- loại bài đầu tiên;
- bài hồi quy đại diện;
- tài liệu điều khiển;
- metadata nào thực sự dùng chung;
- metadata nào chỉ thuộc dự án;
- cấu trúc hồ sơ tối thiểu;
- kiểm tra nào lõi đã có;
- kiểm tra nào cần adapter mới;
- trạng thái xuất bản ban đầu, mặc định là `pending`.

Kiểm kê trước khi tạo tệp:

```bash
find <thu_muc_cha> -maxdepth 3 -type d -print | sort
rg -n '<ten_du_an|tu_khoa_lien_quan>' content quy_trinh_xay_dung
```

Không giả định dự án chưa tồn tại chỉ dựa vào tên thư mục mong muốn.

## 3. Cấu trúc tối thiểu của dự án

```text
<project.root>/
├── AGENTS.md
├── _quy_trinh/
│   ├── cau_hinh_san_xuat_qmd.yml
│   ├── quy_chuan_noi_dung.md
│   ├── ho_so_san_xuat_mac_dinh.yml
│   └── ho_so/
│       └── bai_hoi_quy.yml
├── core/
│   └── bai_hoi_quy.qmd
└── assets/
    └── ...
```

Chỉ tạo thư mục thực sự cần cho loại bài đầu tiên.

## 4. Tạo `AGENTS.md` cục bộ

`AGENTS.md` phải xác định:

- phạm vi của dự án;
- tài liệu phải đọc;
- nguồn có thẩm quyền;
- tệp được phép sửa;
- quy tắc nội dung và kĩ thuật;
- lệnh kiểm tra;
- điều kiện nghiệm thu;
- quyền xuất bản thuộc người dùng.

Không sao chép nguyên `AGENTS.md` của dự án khác rồi chỉ đổi tên. Chỉ mang sang quy tắc thực sự dùng chung.

## 5. Tạo cấu hình dự án

Vị trí bắt buộc:

```text
<project.root>/_quy_trinh/cau_hinh_san_xuat_qmd.yml
```

Khởi đầu từ schema trong `cau_truc_cau_hinh_du_an.md`.

Các quyết định cần khóa:

- `project.id` duy nhất;
- `project.root` đúng vị trí;
- `article_type.id` ổn định;
- glob `include` và `exclude` không chồng lấn;
- `profiles.directory`;
- `modules.required`;
- metadata bổ sung;
- placeholder;
- tài liệu điều khiển;
- bài hồi quy;
- dữ liệu `extensions` của dự án.

Không thêm:

```yaml
compatibility:
legacy_validator:
```

Phiên bản 1.0 chỉ dùng native.

## 6. Chọn mô-đun

Mọi dự án phải có:

```yaml
modules:
  required:
    - qmd-core
```

Thường thêm:

```yaml
    - zo-html-pdf
    - content-blocks
```

Chỉ thêm mô-đun dự án khi có adapter tương ứng.

Danh sách registry hiện tại:

```text
qmd-core
zo-html-pdf
content-blocks
figure-layout
card-grid
functions-article
real-world-problem
```

Một mã mới không thể chỉ được ghi trong YAML. Nó phải được đăng kí trong Python.

## 7. Tạo loại bài và bài hồi quy

Loại bài nên mô tả đơn vị nội dung, không mô tả một bài cụ thể.

Ví dụ:

```text
function_article
real_world_problem
```

Bài hồi quy phải:

- đủ nhỏ để kiểm tra nhanh;
- đủ đại diện để kích hoạt quy tắc dự án;
- có hồ sơ riêng;
- có tài nguyên cần thiết;
- giữ `publication: pending`;
- không được dùng như lí do để tổng quát hóa mọi quy tắc của dự án.

Khai báo trong cấu hình:

```yaml
regression:
  articles:
    - core/bai_hoi_quy.qmd
  expected_checker_version: "2.7.0"
  preserve_cli: true
```

## 8. Tạo quy chuẩn và hồ sơ

Quy chuẩn nội dung phải nêu:

- cấu trúc bài;
- tiêu chuẩn lập luận;
- dữ kiện và giả định;
- biểu diễn chuyên môn;
- tiêu chí kiểm tra tính đúng;
- tiêu chí kiểm tra tính hợp lí;
- kiểm định có người quan sát;
- điều kiện dừng.

Hồ sơ mặc định phải cho phép ghi:

- nhận diện;
- phạm vi;
- tài liệu điều khiển;
- trạng thái sản xuất;
- trạng thái xuất bản;
- quyết định chuyên biệt;
- tài nguyên;
- kết quả checker;
- nghiệm thu;
- vấn đề còn lại.

Phiên bản 1.0 cho phép adapter dự án dùng schema hồ sơ riêng, nhưng ý nghĩa trạng thái phải tuân theo `vong_doi_bai_qmd.md`.

## 9. Khi nào cần validator mới

Không tạo validator mới khi quy tắc đã được lõi kiểm tra.

Cần validator dự án khi phải kiểm tra một trong các điểm:

- metadata chỉ thuộc dự án;
- cấu trúc mục bắt buộc;
- dữ liệu danh mục riêng;
- schema hồ sơ riêng;
- quy tắc canonical URL riêng;
- cấm metadata của dự án khác;
- kiểm tra nội dung có thể mã hóa;
- điều kiện đầu ra riêng sau render.

Không mã hóa đánh giá cần phán đoán chuyên môn sâu thành `PASS` giả tạo. Các điểm đó phải là cảnh báo hoặc cổng kiểm định có người quan sát.

## 10. Tạo module validator

Đặt script tại:

```text
scripts/zo_<ten_ngan_du_an>.py
```

Cấu trúc tối thiểu nên có:

```text
validate_<loai_bai>_article(...)
validate_rendered_<loai_bai>_page(...)
self-test
CLI self-test
```

Adapter không được:

- tự tìm một cấu hình khác;
- tự sửa QMD;
- tự đổi trạng thái;
- tự stage, commit hoặc xuất bản;
- gọi mã từ đường dẫn do YAML cung cấp.

Adapter nên nhận `ArticleValidationContext` do checker đã tạo.

## 11. Đăng kí mô-đun trong registry

Sửa:

```text
scripts/zo_qmd_registry.py
```

Thêm một `ModuleSpec` cố định:

```python
ModuleSpec(
    "ma-module",
    article_types=("ma_loai_bai",),
    source_adapter="ma-module",
    render_adapter="ma-module",
    requires_human_acceptance=True,
)
```

Quy tắc:

- `id` duy nhất;
- `article_types` đúng loại bài;
- tên adapter ổn định;
- `requires_human_acceptance=True` khi nội dung cần người nghiệm thu;
- bổ sung self-test registry.

Không cho cấu hình chỉ định tên hàm Python.

## 12. Cài adapter trong checker

Sửa:

```text
scripts/zo_check_repo.py
```

### 12.1. Import validator

```python
from zo_ten_du_an import (
    validate_ten_bai,
    validate_rendered_ten_bai,
)
```

### 12.2. Đăng kí source adapter

```python
SOURCE_VALIDATOR_ADAPTERS = {
    ...
    "ma-module": validate_ten_bai,
}
```

### 12.3. Đăng kí render adapter

```python
RENDER_VALIDATOR_ADAPTERS = {
    ...
    "ma-module": validate_rendered_ten_bai,
}
```

### 12.4. Nâng checker version

Nâng `CHECKER_VERSION` khi thay đổi hành vi có thể quan sát của checker và cập nhật `regression.expected_checker_version` ở các dự án đường cơ sở.

Không nâng phiên bản chỉ vì sửa tài liệu.

## 13. Self-test bắt buộc

Sau khi thêm validator:

```bash
python scripts/zo_python.py -m py_compile \
  scripts/zo_check_repo.py \
  scripts/zo_qmd_config.py \
  scripts/zo_qmd_core.py \
  scripts/zo_qmd_registry.py \
  scripts/zo_<ten_ngan_du_an>.py

python scripts/zo_python.py scripts/zo_qmd_config.py self-test
python scripts/zo_python.py scripts/zo_qmd_registry.py self-test
python scripts/zo_python.py scripts/zo_qmd_core.py self-test
python scripts/zo_python.py scripts/zo_<ten_ngan_du_an>.py self-test
```

## 14. Kiểm tra cấu hình mới

```bash
python scripts/zo_python.py scripts/zo_qmd_config.py check \
  <project.root>/_quy_trinh/cau_hinh_san_xuat_qmd.yml
```

Kiểm tra một bài:

```bash
python scripts/zo_python.py scripts/zo_qmd_config.py inspect \
  <project.root>/core/bai_hoi_quy.qmd
```

Phải thấy đúng:

- `project_id`;
- `article_type`;
- profile path;
- required modules;
- `compatibility_mode: native` trong đầu ra tóm tắt.

## 15. Hồi quy ba phía

Khi thêm dự án thứ ba, phải chạy đồng thời:

1. `ham_ln_x.qmd`;
2. `chi_phi_di_taxi.qmd`;
3. bài hồi quy của dự án mới.

Kiểm tra nguồn:

```bash
python scripts/zo_python.py scripts/zo_check_repo.py scope \
  <ham_ln_x.qmd> \
  <chi_phi_di_taxi.qmd> \
  <bai_hoi_quy_moi.qmd>
```

Kiểm tra render:

```bash
python scripts/zo_python.py scripts/zo_check_repo.py render \
  <ham_ln_x.qmd> \
  <chi_phi_di_taxi.qmd> \
  <bai_hoi_quy_moi.qmd>
```

Không thay bài cũ để làm dự án mới vượt qua.

## 16. Kiểm tra ranh giới dự án

Phải chứng minh:

- bài mới nhận đúng adapter;
- hai bài cũ vẫn nhận adapter cũ;
- metadata mới không trở thành bắt buộc cho hai dự án cũ;
- validator mới không chạy trên bài cũ;
- validator cũ không chạy trên bài mới;
- không có mô-đun chưa đăng kí;
- không có đường dẫn ngoài repository;
- trạng thái ba bài vẫn `pending` trừ nhiệm vụ xuất bản riêng.

## 17. Kiểm định có người quan sát

Trước khi nghiệm thu dự án mới, mở:

- HTML desktop;
- HTML mobile;
- PDF thật;
- hình và bảng;
- liên kết tải PDF;
- metadata trình duyệt và PDF;
- nội dung chuyên môn.

Checker chỉ xác nhận phần cấu trúc có thể mã hóa.

## 18. Stage và commit

Chỉ stage tệp thuộc phạm vi:

```bash
git add -- \
  <config> \
  <AGENTS.md> \
  <quy_chuan> \
  <ho_so> \
  <QMD_va_tai_nguyen> \
  <validator> \
  scripts/zo_qmd_registry.py \
  scripts/zo_check_repo.py
```

Không dùng:

```bash
git add .
```

Sau đó:

```bash
python scripts/zo_python.py scripts/zo_check_repo.py scope --staged \
  <cac_tep_da_stage>

git diff --cached --check
git --no-pager diff --cached --name-status
git --no-pager diff --cached --stat
```

Commit cấu hình/validator và commit tài liệu lớn nên tách riêng khi phạm vi đủ rõ.

## 19. Điều kiện phải dừng

Dừng khi:

- không xác định được gốc dự án;
- glob khớp bài của dự án khác;
- cấu hình yêu cầu mã chưa đăng kí;
- validator mới phải sửa lõi bằng quy tắc chuyên biệt;
- bài cũ phát sinh `FAIL`;
- QMD cũ phải sửa chỉ để checker vượt qua;
- dự án mới phải mang metadata của dự án cũ;
- PDF hoặc HTML cũ thay đổi ngoài dự kiến;
- trạng thái `pending` bị đổi;
- YAML được dùng để chỉ định hàm Python;
- diff lan sang tệp ngoài phạm vi.

## 20. Checklist nghiệm thu dự án mới

- [ ] Có `AGENTS.md` cục bộ.
- [ ] Có cấu hình schema 1 hợp lệ.
- [ ] Có loại bài không chồng lấn.
- [ ] Có `qmd-core` trong `modules.required`.
- [ ] Có quy chuẩn chuyên biệt tối thiểu.
- [ ] Có hồ sơ mặc định và hồ sơ bài hồi quy.
- [ ] Có bài hồi quy đại diện.
- [ ] Có validator dự án khi cần.
- [ ] Module đã đăng kí trong registry.
- [ ] Source adapter đã cài trong checker.
- [ ] Render adapter đã cài khi cần.
- [ ] Self-test đạt.
- [ ] Hồi quy các dự án cũ đạt.
- [ ] Bài mới không mang metadata không áp dụng.
- [ ] HTML/PDF đã được quan sát.
- [ ] Trạng thái vẫn `pending`.
- [ ] Chỉ tệp trong phạm vi được stage.
- [ ] Người dùng quyết định nghiệm thu và xuất bản.

## 21. Kết luận

Thêm dự án mới không phải là sao chép cỗ máy QMD.

Quy trình đúng là:

```text
cấu hình dự án
+ quy chuẩn và hồ sơ riêng
+ một bài hồi quy
+ adapter tối thiểu
+ đăng kí an toàn
+ hồi quy các dự án hiện có
```

Chỉ những quy tắc đã được chứng minh ở nhiều dự án mới được xem xét thăng cấp vào lõi.
