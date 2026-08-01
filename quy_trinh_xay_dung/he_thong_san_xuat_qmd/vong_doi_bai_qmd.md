# Vòng đời bài QMD trong ZO Math

> **Trạng thái:** Hợp đồng vòng đời vận hành — phiên bản 1.0.

## 1. Hai trục trạng thái

Mỗi bài có hai trạng thái độc lập:

```text
production
publication
```

Không gộp hai trục thành một trường.

Trạng thái sản xuất mô tả mức hoàn thành của bài. Trạng thái xuất bản mô tả việc bài đã được công khai hay chưa.

## 2. Trạng thái sản xuất

### `draft`

Bài hoặc hồ sơ mới được khởi tạo.

Điều kiện điển hình:

- nhận diện cơ bản đã có;
- phạm vi có thể chưa khóa đầy đủ;
- chưa đủ bằng chứng kiểm định;
- chưa được nghiệm thu.

### `in_production`

Bài đang được xây dựng hoặc sửa.

Điều kiện:

- phạm vi đã khóa;
- tài liệu điều khiển đã xác định;
- hồ sơ đang được điền;
- QMD hoặc tài nguyên đang thay đổi;
- có thể chưa render.

### `validated`

Bài đã vượt qua các kiểm định bắt buộc có thể mã hóa.

Điều kiện:

- cấu hình hợp lệ;
- hồ sơ đáp ứng validator dự án;
- checker không có `FAIL`;
- cảnh báo đã được đọc;
- bằng chứng kiểm định đã được ghi khi quy trình yêu cầu.

`validated` không đồng nghĩa với nghiệm thu nội dung.

### `accepted`

Bài đã được con người nghiệm thu.

Điều kiện:

- đã đạt `validated`;
- toán học và nội dung đạt;
- mạch giải thích đạt;
- HTML/PDF thật đã được quan sát khi áp dụng;
- các giới hạn còn lại đã được chấp nhận;
- hồ sơ nghiệm thu hoàn tất.

## 3. Trạng thái xuất bản

### `pending`

Bài chưa công khai hoặc chưa được kích hoạt trong giao diện dự án.

Đây là trạng thái mặc định, kể cả khi bài đã `accepted`.

### `published`

Bài đã được người dùng xác nhận công khai.

Điều kiện bắt buộc:

- `production` đã đạt `accepted`;
- kiểm định kĩ thuật gần nhất đạt;
- tài nguyên công khai tồn tại;
- dữ liệu danh mục được cập nhật khi dự án dùng danh mục;
- người dùng xác nhận rõ;
- quy trình xuất bản chính thức được dùng.

## 4. Chuyển trạng thái hợp lệ

Trạng thái sản xuất:

```text
draft
  ↓
in_production
  ↓
validated
  ↓
accepted
```

Trạng thái xuất bản:

```text
pending
  ↓
published
```

Không có chuyển tự động từ `accepted` sang `published`.

## 5. Chuyển lùi

Khi bài `accepted` bị sửa, trạng thái sản xuất phải được đánh giá lại.

Thông thường:

- sửa nội dung, toán học, cấu trúc hoặc tài nguyên có ảnh hưởng: lùi về `in_production`;
- sửa kĩ thuật nhỏ nhưng làm mất bằng chứng kiểm định gần nhất: lùi về `validated` hoặc `in_production` theo quy chuẩn dự án;
- chỉ sửa tài liệu ngoài bài và không tác động đầu ra: không cần đổi trạng thái bài.

Bài đang `published` không tự động bị gỡ khi có sửa nhỏ, nhưng hồ sơ phải ghi trạng thái sản xuất hiện tại. Thay đổi lớn cần nhiệm vụ xuất bản lại riêng.

## 6. Biểu diễn trong hồ sơ

Phiên bản 1.0 khóa tên và ý nghĩa của các trạng thái, nhưng chưa bắt buộc mọi dự án dùng một schema hồ sơ vật lí giống hệt nhau.

Mỗi adapter dự án phải đọc được tối thiểu:

- trạng thái sản xuất;
- trạng thái xuất bản;
- bằng chứng kiểm định liên quan;
- kết quả nghiệm thu khi có.

Một biểu diễn khuyến nghị:

```yaml
production:
  status: in_production
  validated_at: null
  checker_version: null
  report: null

acceptance:
  status: not_run
  accepted_at: null
  accepted_by: null

publication:
  status: pending
  confirmed_at: null
  confirmed_by: null
```

Dự án có thể dùng schema đã được adapter của mình chấp nhận, miễn không làm thay đổi ý nghĩa hai trục trạng thái.

## 7. Ánh xạ với dữ liệu dự án

### 7.1. 100+ Hàm số

```text
cards.yml status: pending   ↔ publication: pending
cards.yml status: published ↔ publication: published
```

`cards.yml` không lưu trạng thái sản xuất.

`href: ''` hợp lệ khi thẻ `pending`.

Bài `ham_ln_x.qmd` trong đường cơ sở giữ:

```text
card 114: pending
href: rỗng
```

### 7.2. 100+ Bài toán thực tế

Bài hồi quy `chi_phi_di_taxi.qmd` không dùng `cards.yml` trong phiên bản 1.0.

Hồ sơ của bài giữ:

```text
production: in_production
publication: pending
```

Việc có HTML và PDF không tự động đổi bài sang `published`.

## 8. Ba cổng vận hành

### Cổng V — Validation

Để vào `validated`:

- cấu hình hợp lệ;
- validator lõi đạt;
- source adapter dự án đạt;
- render adapter đạt khi đầu ra thuộc phạm vi nhiệm vụ;
- không có `FAIL`;
- cảnh báo đã được xem xét;
- bằng chứng được ghi khi quy trình yêu cầu.

### Cổng A — Acceptance

Để vào `accepted`:

- đã `validated`;
- kiểm định có người quan sát hoàn tất;
- nội dung chuyên môn đạt;
- đầu ra thật đạt;
- người dùng hoặc người được ủy quyền nghiệm thu.

### Cổng P — Publication

Để vào `published`:

- đã `accepted`;
- người dùng xác nhận;
- dữ liệu công khai được cập nhật;
- quy trình xuất bản chạy thành công;
- không có thay đổi ngoài phạm vi.

## 9. Checker và trạng thái

Checker được phép:

- xác nhận giá trị trạng thái hợp lệ;
- xác nhận điều kiện kĩ thuật cho trạng thái;
- báo lỗi khi `published` thiếu tài nguyên bắt buộc;
- báo lỗi khi dữ liệu công khai mâu thuẫn với hồ sơ;
- báo cảnh báo khi cần kiểm định có người quan sát.

Checker không được:

- tự đổi trạng thái;
- tự ghi thời điểm nghiệm thu;
- tự xác nhận người nghiệm thu;
- tự stage hoặc commit;
- tự xuất bản;
- coi `PASS_WITH_WARNINGS` là nghiệm thu cuối.

## 10. Bằng chứng trạng thái

Bằng chứng nên ghi:

- phiên bản checker;
- lệnh đã chạy;
- phạm vi kiểm tra;
- kết quả và mã thoát;
- báo cáo JSON khi có;
- trạng thái HTML/PDF;
- vấn đề còn lại;
- người và thời điểm nghiệm thu;
- xác nhận xuất bản riêng.

Đường cơ sở hai dự án được ghi tại:

```text
quy_trinh_xay_dung/he_thong_san_xuat_qmd/duong_co_so_hoi_quy_hai_du_an.md
```

## 11. Điều kiện phải dừng

Dừng chuyển trạng thái khi:

- có `FAIL` chưa giải quyết;
- trạng thái hồ sơ và dữ liệu danh mục mâu thuẫn;
- kiểm định có người quan sát chưa hoàn tất nhưng bài được đề nghị `accepted`;
- chưa có xác nhận của người dùng nhưng bài được đề nghị `published`;
- QMD hoặc tài nguyên đã thay đổi sau lần kiểm định dùng làm bằng chứng;
- không xác định được tài liệu có thẩm quyền.

## 12. Kết luận

Tách trạng thái sản xuất khỏi trạng thái xuất bản bảo đảm:

- một bài có thể đạt nhưng chưa công khai;
- dữ liệu thẻ không phải nơi lưu toàn bộ vòng đời;
- checker không thể biến kiểm định kĩ thuật thành nghiệm thu;
- nghiệm thu không thể tự động biến thành xuất bản;
- quyền xuất bản luôn thuộc người dùng.
