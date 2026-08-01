# Kiến trúc hệ thống sản xuất và kiểm định QMD cho ZO Math

> **Trạng thái:** Bản thiết kế v1.0 — Giai đoạn 1.
>
> Tài liệu này đề xuất kiến trúc đích. Nó chỉ trở thành tài liệu có thẩm quyền sau khi người dùng duyệt và hệ thống chỉ dẫn của repository dẫn chiếu phù hợp.

## 1. Mục tiêu kiến trúc

Hệ thống phải cho phép nhiều dự án nội dung của ZO Math cùng sử dụng một lõi sản xuất và kiểm định QMD, trong khi mỗi dự án vẫn giữ:

- quy chuẩn nội dung chuyên biệt;
- cấu trúc thư mục riêng;
- metadata bổ sung;
- mô-đun tài nguyên riêng;
- tiêu chí kiểm định riêng;
- quyền quyết định xuất bản riêng.

Kiến trúc phải bảo toàn hành vi đã nghiệm thu của dự án **100+ Hàm số: Sự biến thiên và đồ thị**, đồng thời đủ mở để tiếp nhận **100+ Bài toán thực tế** mà không sao chép toàn bộ quy trình và checker.

## 2. Quyết định kiến trúc trung tâm

Hệ thống gồm bốn tầng chính:

```text
lõi ZO Math
    ↓
cấu hình dự án
    ↓
hồ sơ sản xuất của bài
    ↓
QMD, tài nguyên và đầu ra
```

Checker tạo **hợp đồng hiệu lực** cho mỗi bài bằng cách kết hợp ba nguồn đầu, rồi dùng hợp đồng ấy để kiểm tra nguồn và đầu ra.

## 3. Tầng 1 — Lõi dùng chung

Lõi chứa các quy tắc không phụ thuộc chủ đề:

- vòng đời kĩ thuật của bài;
- hợp đồng QMD cơ bản;
- metadata dùng chung;
- quản lí tài nguyên;
- HTML và PDF;
- kiểm định tự động;
- kiểm định có người quan sát;
- nghiệm thu;
- bàn giao;
- cổng xuất bản;
- định dạng báo cáo;
- giao diện lệnh checker.

Vị trí thiết kế và tài liệu lõi:

```text
quy_trinh_xay_dung/he_thong_san_xuat_qmd/
```

Lõi không chứa:

- tên dự án;
- đường dẫn `core/` hoặc `depth/`;
- `cards.yml`;
- `listing-order`;
- quy chuẩn khảo sát hàm số;
- quy chuẩn mô hình hóa bài toán thực tế;
- tên hàm validator có thể được gọi tùy ý từ YAML.

## 4. Tầng 2 — Cấu hình dự án

Mỗi dự án có một tệp cấu hình cục bộ:

```text
<goc_du_an>/_quy_trinh/cau_hinh_san_xuat_qmd.yml
```

Checker tìm cấu hình bằng cách đi từ đường dẫn bài lên các thư mục cha; tại mỗi gốc dự án tiềm năng, checker kiểm tra tệp:

```text
_quy_trinh/cau_hinh_san_xuat_qmd.yml
```

Cấu hình dự án khai báo:

- định danh và tên dự án;
- gốc dự án;
- mẫu đường dẫn bài;
- loại bài;
- thư mục hồ sơ;
- metadata bắt buộc bổ sung;
- mô-đun kiểm định được kích hoạt;
- dữ liệu danh mục hoặc lưới thẻ khi áp dụng;
- quy tắc trạng thái xuất bản;
- đường dẫn tài liệu chuyên biệt;
- đường cơ sở hồi quy của dự án.

Cấu hình chỉ dùng dữ liệu khai báo. Nó không được phép chỉ định đường dẫn Python tùy ý hoặc thực thi mã.

## 5. Tầng 3 — Hồ sơ sản xuất của bài

Mỗi bài có một hồ sơ cục bộ, do cấu hình dự án xác định vị trí.

Hồ sơ gồm hai vùng:

```yaml
loi:
  ...

mo_rong:
  <ma_du_an>:
    ...
```

Vùng `loi` ghi:

- nhận diện;
- nhiệm vụ;
- đường dẫn;
- phạm vi thay đổi;
- tài liệu điều khiển;
- đầu ra;
- tài nguyên;
- kiểm định;
- nghiệm thu;
- bàn giao;
- trạng thái sản xuất;
- trạng thái xuất bản.

Vùng `mo_rong` ghi nghiệp vụ chuyên biệt, ví dụ:

```yaml
mo_rong:
  ham_so:
    ban_do_mien: ...
    menh_de_chung_cu: ...
    truc_nhan_thuc: ...
```

Dự án khác không phải khai báo các trường của hàm số.

## 6. Tầng 4 — QMD, tài nguyên và đầu ra

Đây là sản phẩm được kiểm định:

- tệp `.qmd`;
- hình và dữ liệu;
- HTML;
- PDF;
- metadata đầu ra;
- dữ liệu danh mục;
- bằng chứng kiểm định.

QMD không phải nơi quyết định quy tắc. QMD phải thỏa hợp đồng hiệu lực được tạo từ lõi, cấu hình dự án và hồ sơ bài.

## 7. Thành phần checker

Checker được tổ chức theo các lớp chức năng:

```text
điểm vào lệnh
    ↓
mở rộng phạm vi
    ↓
khám phá dự án
    ↓
nạp cấu hình
    ↓
xác định loại bài
    ↓
tạo hợp đồng hiệu lực
    ↓
validator lõi
    ↓
validator mô-đun
    ↓
validator dự án
    ↓
render khi được yêu cầu
    ↓
validator sau render
    ↓
báo cáo
```

### 7.1. Điểm vào lệnh

Giữ nguyên:

```text
quick
scope
render
--staged
--report
```

### 7.2. Bộ khám phá dự án

Trách nhiệm:

- nhận đường dẫn tương đối;
- tìm cấu hình gần nhất có hiệu lực;
- xác nhận đường dẫn nằm trong gốc dự án;
- trả về `project_id`, `article_type` và danh sách mô-đun.

### 7.3. Registry mô-đun an toàn

Checker có registry cố định trong Python:

```text
qmd-core
zo-html-pdf
content-blocks
figure-layout
card-grid
functions-article
real-world-problem
```

Cấu hình chỉ được khai báo các mã mô-đun đã đăng kí. Mã không tồn tại là lỗi cấu hình.

Không cho YAML ghi tên hàm Python hoặc import module tùy ý.

### 7.4. Validator lõi

Chạy cho mọi bài QMD đã được một dự án đăng kí:

- front matter;
- placeholder;
- metadata lõi;
- tài nguyên;
- cấu trúc Markdown/QMD;
- mã thực thi;
- HTML/PDF chung;
- bằng chứng và báo cáo.

### 7.5. Validator mô-đun

Chỉ chạy khi cấu hình kích hoạt, ví dụ:

- `content-blocks`;
- `figure-layout`;
- `card-grid`;
- `zo-html-pdf`.

### 7.6. Validator dự án

Kiểm tra nghiệp vụ riêng:

- `functions-article`;
- `real-world-problem`;
- các loại bài khác về sau.

## 8. Thứ tự thẩm quyền và khả năng ghi đè

Thứ tự thẩm quyền:

1. yêu cầu hiện tại của người dùng;
2. `AGENTS.md` và tài liệu được dẫn chiếu;
3. hợp đồng lõi đã được phê duyệt;
4. cấu hình dự án;
5. quy chuẩn chuyên biệt của dự án;
6. hồ sơ bài;
7. QMD và dữ liệu đầu ra.

Quy tắc ghi đè:

- cấu hình dự án được **bổ sung** yêu cầu vào lõi;
- cấu hình không được vô hiệu hóa bất biến an toàn của lõi;
- hồ sơ bài chỉ chọn trong những phương án cấu hình cho phép;
- `không áp dụng` phải có lí do và chỉ dùng cho trường được cho phép;
- metadata QMD không được dùng để tự bỏ qua validator.

## 9. Hai trục trạng thái độc lập

Không dùng một trường duy nhất cho cả sản xuất và xuất bản.

### 9.1. Trạng thái sản xuất

```text
draft
in_production
validated
accepted
```

### 9.2. Trạng thái xuất bản

```text
pending
published
```

Quan hệ:

- bài chưa `accepted` không được `published`;
- bài `accepted` vẫn có thể giữ `pending`;
- chuyển sang `published` luôn cần xác nhận của người dùng;
- trạng thái thẻ của dự án phải ánh xạ với trạng thái xuất bản, không thay thế trạng thái sản xuất.

## 10. Kiến trúc tài liệu

Sau khi Giai đoạn 1 được duyệt, thư mục dự kiến gồm:

```text
he_thong_san_xuat_qmd/
├── README.md
├── kiem_ke_he_thong_hien_tai.md
├── ban_do_kien_truc_hien_trang.md
├── phan_loai_quy_tac_chung_rieng.md
├── duong_co_so_hoi_quy_ham_ln_x.md
├── kien_truc_he_thong.md
├── hop_dong_loi_va_du_an.md
├── cau_truc_cau_hinh_du_an.md
├── vong_doi_bai_qmd.md
├── ke_hoach_chuyen_doi.md
└── tieu_chi_nghiem_thu_he_thong.md
```

## 11. Bất biến không được phá vỡ

- không viết lại checker từ đầu;
- không đổi giao diện lệnh nếu không có lí do bắt buộc;
- không buộc bài cũ sửa nội dung để thích nghi với kiến trúc mới;
- không tự xuất bản;
- không đưa nghiệp vụ hàm số vào lõi;
- không cho cấu hình thực thi mã tùy ý;
- không tạo nhiều nguồn có thẩm quyền cạnh tranh;
- không làm mất kiểm định có người quan sát;
- không làm mất khả năng báo cáo JSON;
- không làm suy yếu đường cơ sở `ham_ln_x`.

## 12. Kết luận

Kiến trúc đích là một hệ thống **lõi ổn định + cấu hình dự án + hồ sơ mở rộng + registry validator an toàn**.

Đây là kiến trúc tối thiểu đủ để:

- tách phần dùng chung khỏi 100+ Hàm số;
- bảo toàn checker hiện hành;
- thêm dự án thứ hai;
- tiếp tục mạnh lên theo mô-đun mà không phình thành một khối đơn khó kiểm soát.
