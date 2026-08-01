# Hệ thống sản xuất và kiểm định QMD cho ZO Math

> **Trạng thái:** Phiên bản 1.0 — có hiệu lực từ commit khóa tài liệu M9B.
>
> Đây là tài liệu vận hành nội bộ. Nó chỉ có thẩm quyền trong phạm vi mà `AGENTS.md`, cấu hình dự án hoặc yêu cầu hiện tại của người dùng dẫn chiếu. Các hồ sơ kiểm kê và thiết kế ban đầu được giữ lại như bằng chứng lịch sử, không tự động ghi đè quy trình đang có hiệu lực ở nơi khác.

## 1. Mục đích

Hệ thống cung cấp một điểm vào thống nhất để sản xuất và kiểm định nhiều loại bài QMD của ZO Math:

```text
tiếp nhận nhiệm vụ
→ khóa phạm vi
→ xác định dự án và loại bài
→ nạp cấu hình dự án
→ nạp hồ sơ sản xuất
→ tạo hoặc sửa QMD và tài nguyên
→ kiểm định nguồn
→ render khi cần
→ kiểm định đầu ra
→ kiểm định có người quan sát
→ nghiệm thu
→ xuất bản khi người dùng xác nhận
```

Hệ thống không tự viết thay quy chuẩn chuyên môn, không tự nghiệm thu nội dung và không tự xuất bản.

## 2. Kiến trúc đang vận hành

Phiên bản 1.0 gồm bốn tầng:

1. **Lõi dùng chung**
   - vòng đời bài;
   - metadata nền;
   - kiểm tra QMD, tài nguyên, HTML và PDF;
   - định dạng báo cáo;
   - cổng nghiệm thu và xuất bản.

2. **Cấu hình dự án**
   - gốc dự án;
   - loại bài và mẫu đường dẫn;
   - thư mục hồ sơ;
   - mô-đun đã đăng kí;
   - metadata bổ sung;
   - tài liệu điều khiển;
   - đường cơ sở hồi quy.

3. **Hồ sơ sản xuất và quy chuẩn chuyên biệt**
   - quyết định của bài cụ thể;
   - trạng thái sản xuất và xuất bản;
   - phần mở rộng nghiệp vụ của dự án;
   - bằng chứng kiểm định và nghiệm thu.

4. **QMD, tài nguyên và đầu ra**
   - tệp nguồn;
   - hình và dữ liệu;
   - HTML;
   - PDF;
   - dữ liệu danh mục khi áp dụng.

Checker tạo hợp đồng hiệu lực từ lõi, cấu hình dự án và mô-đun được đăng kí, rồi chỉ kiểm tra phần có thể mã hóa.

## 3. Thành phần triển khai

### 3.1. Điểm vào kiểm định

```text
scripts/zo_check_repo.py
```

Phiên bản đường cơ sở của hệ thống 1.0:

```text
CHECKER VERSION: 2.6.0
```

Các lệnh được giữ ổn định:

```text
quick
scope
render
--staged
--report
```

### 3.2. Bộ đọc cấu hình

```text
scripts/zo_qmd_config.py
```

Trách nhiệm:

- tìm cấu hình gần nhất;
- nạp YAML an toàn và từ chối khóa trùng;
- kiểm tra schema phiên bản 1;
- xác định loại bài;
- xác định đường dẫn hồ sơ;
- từ chối mô-đun chưa đăng kí và đường dẫn không an toàn.

### 3.3. Validator lõi

```text
scripts/zo_qmd_core.py
```

Chứa các kiểm tra dùng chung như front matter, metadata, placeholder, tiêu đề, hình, tài nguyên, đường dẫn bị cấm và mã thực thi.

### 3.4. Registry mô-đun

```text
scripts/zo_qmd_registry.py
```

Registry cố định trong Python; YAML không được gọi hàm hoặc import mã tùy ý.

Các mã mô-đun của phiên bản 1.0:

```text
qmd-core
zo-html-pdf
content-blocks
figure-layout
card-grid
functions-article
real-world-problem
```

### 3.5. Validator dự án

- `functions-article`: được cài trong checker hiện hành;
- `real-world-problem`: được cài tại `scripts/zo_real_world_problem.py`.

Mỗi adapter chỉ chạy cho loại bài mà registry cho phép.

## 4. Hai dự án đường cơ sở

### 4.1. 100+ Hàm số: Sự biến thiên và đồ thị

Cấu hình:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/_quy_trinh/cau_hinh_san_xuat_qmd.yml
```

Bài hồi quy:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/core/ham_ln_x.qmd
```

Loại bài và adapter:

```text
function_article
functions-article
```

Bất biến quan trọng:

- thẻ 114 giữ `pending`;
- `href` của thẻ vẫn rỗng;
- PDF Title khớp `title-meta`;
- PDF đường cơ sở có 15 trang;
- số hình mở rộng của bài là 0;
- không sửa nội dung bài để làm checker vượt qua.

### 4.2. 100+ Bài toán thực tế

Cấu hình:

```text
content/thpt/zo_math_100/100_bai_toan_thuc_te/_quy_trinh/cau_hinh_san_xuat_qmd.yml
```

Bài hồi quy:

```text
content/thpt/zo_math_100/100_bai_toan_thuc_te/core/chi_phi_di_taxi.qmd
```

Loại bài và adapter:

```text
real_world_problem
real-world-problem
```

Bất biến quan trọng:

- không mang `listing-order` hoặc metadata riêng của dự án hàm số;
- đủ bốn phần mô hình hóa bắt buộc;
- hồ sơ giữ `production: in_production` và `publication: pending`;
- HTML có liên kết PDF;
- PDF đường cơ sở có 4 trang;
- không xuất bản trong quá trình kiểm nghiệm hệ thống.

Đường cơ sở hợp nhất được ghi tại `duong_co_so_hoi_quy_hai_du_an.md`.

## 5. Quy trình vận hành ngắn

### 5.1. Kiểm tra cấu hình

```bash
python scripts/zo_python.py scripts/zo_qmd_config.py check \
  <duong_dan_den_cau_hinh>
```

### 5.2. Xác định dự án và loại bài

```bash
python scripts/zo_python.py scripts/zo_qmd_config.py inspect \
  <duong_dan_den_bai_qmd>
```

### 5.3. Kiểm tra nguồn

```bash
python scripts/zo_python.py scripts/zo_check_repo.py scope \
  <duong_dan_den_bai_qmd>
```

### 5.4. Kiểm tra và render

```bash
python scripts/zo_python.py scripts/zo_check_repo.py render \
  <duong_dan_den_bai_qmd>
```

### 5.5. Kiểm tra index trước commit

```bash
python scripts/zo_python.py scripts/zo_check_repo.py scope --staged \
  <cac_duong_dan_da_stage>

git diff --cached --check
```

Báo cáo JSON chỉ được ghi bên trong `_audit/`:

```bash
python scripts/zo_python.py scripts/zo_check_repo.py scope \
  <duong_dan> \
  --report _audit/bao_cao.json
```

## 6. Trạng thái và quyền xuất bản

Hai trục độc lập:

```text
production: draft → in_production → validated → accepted
publication: pending → published
```

Các bất biến:

- `validated` chỉ có nghĩa là kiểm định có thể mã hóa không còn `FAIL`;
- `accepted` cần kiểm định có người quan sát;
- `accepted` không tự động thành `published`;
- `published` luôn cần xác nhận rõ của người dùng;
- checker không tự đổi trạng thái, không stage, không commit và không xuất bản.

## 7. Phân loại tài liệu trong thư mục

### 7.1. Tài liệu vận hành phiên bản 1.0

- `README.md`;
- `kien_truc_he_thong.md`;
- `hop_dong_loi_va_du_an.md`;
- `cau_truc_cau_hinh_du_an.md`;
- `vong_doi_bai_qmd.md`;
- `duong_co_so_hoi_quy_hai_du_an.md`;
- `huong_dan_them_du_an_va_validator.md`;
- `tieu_chi_nghiem_thu_he_thong.md`.

### 7.2. Hồ sơ chuyển đổi

- `ke_hoach_chuyen_doi.md`;
- `duong_co_so_hoi_quy_ham_ln_x.md`.

Hai tài liệu này ghi lại đường chuyển đổi và đường cơ sở ban đầu; không dùng chúng để khôi phục nhánh legacy đã loại bỏ.

### 7.3. Hồ sơ lịch sử Giai đoạn 0

- `kiem_ke_he_thong_hien_tai.md`;
- `ban_do_kien_truc_hien_trang.md`;
- `phan_loai_quy_tac_chung_rieng.md`.

Các tài liệu lịch sử mô tả bằng chứng và giả định tại thời điểm khảo sát. Khi khác với tài liệu vận hành phiên bản 1.0, tài liệu vận hành hiện hành được ưu tiên trong phạm vi cỗ máy QMD.

## 8. Bất biến của phiên bản 1.0

- cấu hình dự án là YAML khai báo, không thực thi mã;
- mọi dự án phải dùng cấu hình cục bộ tại vị trí chuẩn;
- `qmd-core` là mô-đun bắt buộc;
- checker giữ một điểm vào thống nhất;
- validator dự án chỉ chạy đúng loại bài;
- không còn đường chạy legacy hoặc fallback cho bài hàm số thiếu cấu hình;
- hai dự án hồi quy phải cùng đạt trước khi đổi lõi, loader, registry hoặc dispatch;
- kiểm định tự động không thay thế nghiệm thu của con người;
- xuất bản vẫn thuộc quyền quyết định của người dùng.

## 9. Đường chuyển đổi đã hoàn tất

Các commit nền của phiên bản 1.0:

```text
b8740b0  docs(qmd-system): define architecture and baseline
48ae4f3  feat(qmd-system): add project configuration foundation
9c92cd2  refactor(checker): discover configured qmd projects
d386588  refactor(qmd-system): move function rules into project config
2ae9661  refactor(qmd-system): extract shared qmd core validator
e6371d6  refactor(qmd-system): add validator registry and dispatch
b577787  refactor(qmd-system): switch functions project to native mode
31a1916  feat(real-world): add initial qmd project configuration
ab7581a  refactor(qmd-system): remove legacy compatibility path
```

Commit khóa tài liệu M9B hoàn tất phiên bản 1.0 mà không thay đổi QMD hồi quy hoặc trạng thái xuất bản.
