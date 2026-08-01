# Kiến trúc hệ thống sản xuất và kiểm định QMD cho ZO Math

> **Trạng thái:** Kiến trúc vận hành — phiên bản 1.0.
>
> Tài liệu này mô tả hệ thống đã được triển khai và kiểm nghiệm trên hai dự án. Hiệu lực của nó vẫn tuân theo thứ tự thẩm quyền của repository và yêu cầu hiện tại của người dùng.

## 1. Mục tiêu kiến trúc

Hệ thống cho phép nhiều dự án nội dung của ZO Math cùng sử dụng một lõi sản xuất và kiểm định QMD, trong khi mỗi dự án vẫn giữ:

- quy chuẩn nội dung chuyên biệt;
- cấu trúc thư mục riêng;
- metadata bổ sung;
- mô-đun tài nguyên riêng;
- tiêu chí kiểm định riêng;
- quyền quyết định xuất bản riêng.

Phiên bản 1.0 đã được kiểm nghiệm trên:

- **100+ Hàm số: Sự biến thiên và đồ thị**;
- **100+ Bài toán thực tế**.

## 2. Quyết định kiến trúc trung tâm

Hệ thống gồm bốn tầng:

```text
lõi ZO Math
    ↓
cấu hình dự án
    ↓
hồ sơ sản xuất và quy chuẩn chuyên biệt
    ↓
QMD, tài nguyên và đầu ra
```

Checker tạo **hợp đồng hiệu lực** cho mỗi bài bằng cách kết hợp:

```text
bất biến lõi
+ yêu cầu cấu hình dự án
+ mô-đun bắt buộc đã đăng kí
+ dữ liệu hồ sơ mà adapter dự án hiểu
= kế hoạch kiểm định của bài
```

## 3. Tầng 1 — Lõi dùng chung

Lõi chứa các quy tắc không phụ thuộc chủ đề:

- vòng đời kĩ thuật của bài;
- metadata nền;
- kiểm tra front matter;
- kiểm tra placeholder;
- kiểm tra tiêu đề và cấu trúc QMD;
- kiểm tra hình, tài nguyên và đường dẫn;
- kiểm tra mã thực thi bị cấm;
- kiểm tra HTML/PDF dùng chung;
- định dạng kết quả và báo cáo;
- cổng kiểm định có người quan sát;
- cổng xuất bản.

Thành phần triển khai chính:

```text
scripts/zo_qmd_core.py
scripts/zo_check_repo.py
```

Lõi không chứa:

- tên dự án;
- đường dẫn bài riêng của một dự án;
- `cards.yml`;
- `listing-order`;
- quy chuẩn khảo sát hàm số;
- quy chuẩn mô hình hóa bài toán thực tế;
- tên hàm Python do YAML cung cấp.

## 4. Tầng 2 — Cấu hình dự án

Mỗi dự án có một tệp cấu hình cục bộ:

```text
<goc_du_an>/_quy_trinh/cau_hinh_san_xuat_qmd.yml
```

Bộ đọc cấu hình:

```text
scripts/zo_qmd_config.py
```

Checker tìm cấu hình gần nhất bằng cách đi từ đường dẫn bài lên các thư mục cha. Cấu hình phải nằm đúng dưới `project.root`; cấu hình ở vị trí khác bị từ chối.

Cấu hình dự án khai báo:

- định danh và tên dự án;
- gốc dự án;
- loại bài và mẫu đường dẫn;
- thư mục hồ sơ;
- mô-đun bắt buộc và mô-đun tùy chọn;
- metadata lõi và metadata bổ sung;
- lớp trang bắt buộc;
- placeholder cần chặn;
- trạng thái sản xuất và xuất bản;
- dữ liệu danh mục khi áp dụng;
- tài liệu điều khiển;
- đường cơ sở hồi quy;
- phần mở rộng dự án.

Cấu hình chỉ dùng dữ liệu khai báo. Nó không được phép chỉ định đường dẫn Python tùy ý hoặc thực thi mã.

## 5. Tầng 3 — Hồ sơ sản xuất và quy chuẩn chuyên biệt

Cấu hình xác định vị trí hồ sơ theo quy tắc:

```text
profiles.naming: by_article_stem
```

Với bài `core/ten_bai.qmd`, hồ sơ được giải tại:

```text
<goc_du_an>/<profiles.directory>/ten_bai.yml
```

Phiên bản 1.0 khóa vòng đời và trách nhiệm của hồ sơ, nhưng chưa bắt buộc mọi dự án dùng một schema hồ sơ vật lí hoàn toàn giống nhau. Adapter dự án chịu trách nhiệm đọc và kiểm tra schema hồ sơ mà dự án đã chấp nhận.

Hồ sơ phải ghi được tối thiểu:

- nhận diện bài;
- phạm vi;
- tài liệu điều khiển;
- quyết định chuyên môn;
- tài nguyên;
- bằng chứng kiểm định;
- trạng thái sản xuất;
- trạng thái xuất bản;
- kết quả nghiệm thu;
- vấn đề còn lại.

Quy chuẩn chuyên biệt quy định phần mà lõi không thể suy ra, ví dụ:

- khảo sát hàm số;
- mô hình hóa bài toán thực tế;
- cấu trúc nhận thức;
- tiêu chuẩn lập luận;
- đơn vị và kiểm tra tính hợp lí trong bối cảnh.

## 6. Tầng 4 — QMD, tài nguyên và đầu ra

Đây là sản phẩm được kiểm định:

- tệp `.qmd`;
- hình và dữ liệu;
- HTML;
- PDF;
- metadata đầu ra;
- dữ liệu danh mục;
- báo cáo kiểm định.

QMD không phải nơi quyết định quy tắc. QMD phải thỏa hợp đồng hiệu lực được tạo từ các tầng điều khiển.

## 7. Thành phần checker

Luồng vận hành:

```text
điểm vào lệnh
    ↓
mở rộng phạm vi
    ↓
khám phá cấu hình gần nhất
    ↓
xác định loại bài
    ↓
tạo kế hoạch validator từ registry
    ↓
kiểm tra dùng chung của repository
    ↓
source adapter của dự án
    ↓
render khi được yêu cầu
    ↓
render adapter của dự án
    ↓
báo cáo và mã thoát
```

### 7.1. Điểm vào lệnh

```text
quick
scope
render
--staged
--report
```

Checker phiên bản đường cơ sở:

```text
2.6.0
```

### 7.2. Bộ khám phá dự án

Trách nhiệm:

- nhận đường dẫn tương đối hoặc tuyệt đối bên trong repository;
- tìm cấu hình gần nhất;
- xác nhận đường dẫn nằm trong `project.root`;
- xác định duy nhất một `article_type`;
- báo `INFO` khi tệp nằm trong dự án nhưng không thuộc loại bài đã đăng kí;
- từ chối cấu hình không hợp lệ.

Không còn fallback legacy cho bài hàm số thiếu cấu hình.

### 7.3. Registry mô-đun an toàn

Registry cố định tại:

```text
scripts/zo_qmd_registry.py
```

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

`modules.required` tạo danh sách mô-đun hoạt động của bài. `modules.optional` chỉ khai báo khả năng dự án có thể dùng; phiên bản 1.0 không tự động kích hoạt adapter từ danh sách tùy chọn.

Chỉ mô-đun có adapter đã đăng kí mới tạo dispatch nguồn hoặc sau render. Hiện tại:

```text
functions-article   → source + render adapter
real-world-problem → source + render adapter
```

### 7.4. Validator lõi

`qmd-core` phải nằm trong `modules.required` của mọi dự án.

Các hàm dùng chung được tách trong `scripts/zo_qmd_core.py`, nhưng checker vẫn điều phối thứ tự và ghi kết quả thống nhất.

### 7.5. Source adapter

Bảng dispatch nguồn nằm trong checker:

```text
SOURCE_VALIDATOR_ADAPTERS
```

Adapter nhận:

- đường dẫn bài;
- nội dung QMD;
- checker;
- ngữ cảnh gồm cấu hình, loại bài và kế hoạch validator.

### 7.6. Render adapter

Bảng dispatch sau render nằm trong checker:

```text
RENDER_VALIDATOR_ADAPTERS
```

Adapter chỉ chạy sau khi Quarto render thành công và HTML đầu ra tồn tại.

### 7.7. Báo cáo và nghiệm thu

Kết quả tự động phân biệt:

```text
PASS
WARN
FAIL
INFO
```

Mã thoát:

```text
0: không có FAIL
1: có FAIL
2: lỗi sử dụng lệnh
3: thiếu công cụ bắt buộc
```

Khi kế hoạch validator yêu cầu nghiệm thu của con người, checker luôn ghi:

```text
FINAL ACCEPTANCE: NOT_RUN
```

Checker không được tự tuyên bố nghiệm thu cuối.

## 8. Thứ tự thẩm quyền và khả năng ghi đè

Thứ tự thẩm quyền:

1. yêu cầu hiện tại của người dùng;
2. `AGENTS.md` và tài liệu được dẫn chiếu;
3. hợp đồng lõi có hiệu lực;
4. cấu hình dự án;
5. quy chuẩn chuyên biệt của dự án;
6. hồ sơ bài;
7. QMD và dữ liệu đầu ra.

Quy tắc:

- cấu hình dự án bổ sung yêu cầu vào lõi;
- cấu hình không được vô hiệu hóa bất biến an toàn;
- hồ sơ bài chỉ chọn trong phương án dự án cho phép;
- `không áp dụng` cần lí do và cơ chế được phép;
- metadata QMD không được dùng để tắt validator;
- khi xung đột không giải được bằng thứ tự thẩm quyền, phải dừng và yêu cầu quyết định của người dùng.

## 9. Hai trục trạng thái độc lập

Trạng thái sản xuất:

```text
draft
in_production
validated
accepted
```

Trạng thái xuất bản:

```text
pending
published
```

Bất biến:

- `validated` không đồng nghĩa `accepted`;
- `accepted` không đồng nghĩa `published`;
- bài chưa `accepted` không được `published`;
- chuyển sang `published` luôn cần xác nhận của người dùng;
- dữ liệu thẻ chỉ ánh xạ trạng thái xuất bản, không thay thế trạng thái sản xuất.

## 10. Kiến trúc tài liệu

```text
he_thong_san_xuat_qmd/
├── README.md
├── kien_truc_he_thong.md
├── hop_dong_loi_va_du_an.md
├── cau_truc_cau_hinh_du_an.md
├── vong_doi_bai_qmd.md
├── duong_co_so_hoi_quy_hai_du_an.md
├── huong_dan_them_du_an_va_validator.md
├── tieu_chi_nghiem_thu_he_thong.md
├── ke_hoach_chuyen_doi.md
├── duong_co_so_hoi_quy_ham_ln_x.md
├── kiem_ke_he_thong_hien_tai.md
├── ban_do_kien_truc_hien_trang.md
└── phan_loai_quy_tac_chung_rieng.md
```

Tài liệu vận hành và tài liệu lịch sử được phân loại trong `README.md`.

## 11. Hai dự án kiểm nghiệm

### 11.1. 100+ Hàm số

```text
project_id: functions_100
article_type: function_article
source adapter: functions-article
render adapter: functions-article
```

### 11.2. 100+ Bài toán thực tế

```text
project_id: real_world_100
article_type: real_world_problem
source adapter: real-world-problem
render adapter: real-world-problem
```

Hai dự án dùng chung loader, registry, checker, validator lõi, định dạng báo cáo và cổng xuất bản, nhưng không mang metadata chuyên biệt của nhau.

## 12. Bất biến không được phá vỡ

- không viết lại checker từ đầu khi có thể mở rộng qua cấu hình và adapter;
- không đổi giao diện lệnh nếu không có lí do bắt buộc;
- không buộc bài hồi quy sửa nội dung để thích nghi với checker;
- không tự xuất bản;
- không đưa nghiệp vụ của một dự án vào lõi;
- không cho cấu hình thực thi mã tùy ý;
- không tạo nhiều nguồn có thẩm quyền cạnh tranh;
- không làm mất kiểm định có người quan sát;
- không làm mất báo cáo JSON;
- không làm suy yếu một trong hai đường cơ sở hồi quy;
- không khôi phục nhánh legacy nếu chưa có nhiệm vụ di trú riêng và bằng chứng bắt buộc.

## 13. Kết luận

Kiến trúc phiên bản 1.0 là:

```text
lõi ổn định
+ cấu hình dự án cục bộ
+ hồ sơ và quy chuẩn chuyên biệt
+ registry an toàn
+ adapter nguồn và sau render
+ nghiệm thu của con người
```

Kiến trúc này đã chứng minh một lõi có thể phục vụ hai dự án khác nhau mà không làm dự án thứ hai mang các trường riêng của hàm số và không làm suy yếu bài hồi quy của dự án thứ nhất.
