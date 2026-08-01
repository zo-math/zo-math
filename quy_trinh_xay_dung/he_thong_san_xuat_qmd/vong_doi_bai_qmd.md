# Vòng đời bài QMD trong ZO Math

> **Trạng thái:** Bản thiết kế v1.0 — Giai đoạn 1.

## 1. Hai trục trạng thái

Mỗi bài có hai trạng thái độc lập:

```yaml
production:
  status: draft

publication:
  status: pending
```

Không gộp hai trục thành một trường.

## 2. Trạng thái sản xuất

### `draft`

Bài hoặc hồ sơ mới được khởi tạo.

Điều kiện:

- nhận diện cơ bản đã có;
- chưa đủ bằng chứng kiểm định;
- không được nghiệm thu.

### `in_production`

Bài đang được xây dựng hoặc sửa.

Điều kiện:

- phạm vi đã khóa;
- tài liệu điều khiển đã xác định;
- hồ sơ đang được điền;
- có thể chưa render.

### `validated`

Bài đã vượt qua các kiểm định bắt buộc có thể mã hóa.

Điều kiện:

- checker không có `FAIL`;
- các cảnh báo đã được đọc;
- bằng chứng kiểm định đã ghi;
- chưa đồng nghĩa với nghiệm thu nội dung.

### `accepted`

Bài đã được con người nghiệm thu.

Điều kiện:

- toán học và nội dung đạt;
- mạch giải thích đạt;
- HTML/PDF thật đã quan sát khi áp dụng;
- các giới hạn còn lại đã được chấp nhận;
- hồ sơ nghiệm thu hoàn tất.

## 3. Trạng thái xuất bản

### `pending`

Bài chưa công khai hoặc chưa được kích hoạt trong giao diện dự án.

Đây là trạng thái mặc định, kể cả khi bài đã `accepted`.

### `published`

Bài đã được người dùng xác nhận công khai.

Điều kiện bắt buộc:

- `production.status: accepted`;
- kiểm định kĩ thuật gần nhất đạt;
- tài nguyên công khai tồn tại;
- dữ liệu danh mục được cập nhật;
- người dùng xác nhận rõ;
- quy trình xuất bản chính thức được dùng.

## 4. Chuyển trạng thái hợp lệ

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

`published` không tự động phát sinh từ `accepted`.

## 5. Chuyển lùi

Khi bài `accepted` bị sửa nội dung hoặc kĩ thuật có ảnh hưởng, trạng thái sản xuất phải lùi về:

```text
in_production
```

hoặc:

```text
validated
```

tùy mức thay đổi và quy tắc dự án.

Bài đang `published` có thể vẫn công khai trong thời gian sửa nhỏ, nhưng hồ sơ phải ghi rõ. Thay đổi lớn cần một quy trình riêng, không tự suy diễn trong giai đoạn thiết kế này.

## 6. Ánh xạ với lưới thẻ

Đối với 100+ Hàm số:

```text
cards.yml status: pending  ↔ publication.status: pending
cards.yml status: published ↔ publication.status: published
```

`cards.yml` không lưu trạng thái sản xuất.

`href: ''` là hợp lệ khi `pending`.

## 7. Cổng kiểm định

### Cổng V — Validation

Để vào `validated`:

- cấu hình và hồ sơ hợp lệ;
- validator lõi đạt;
- validator mô-đun đạt;
- validator dự án đạt;
- không có `FAIL`;
- bằng chứng được ghi.

### Cổng A — Acceptance

Để vào `accepted`:

- đã `validated`;
- kiểm định có người quan sát hoàn tất;
- nội dung chuyên môn đạt;
- người dùng hoặc người được ủy quyền nghiệm thu.

### Cổng P — Publication

Để vào `published`:

- đã `accepted`;
- người dùng xác nhận;
- dữ liệu công khai được cập nhật;
- quy trình xuất bản chạy thành công.

## 8. Checker và trạng thái

Checker được phép:

- xác nhận trạng thái khai báo hợp lệ;
- xác nhận điều kiện kĩ thuật cho trạng thái;
- báo lỗi khi `published` thiếu tài nguyên;
- báo lỗi khi `published` nhưng chưa `accepted`;
- báo cảnh báo khi hồ sơ và dữ liệu danh mục lệch nhau.

Checker không được:

- tự đổi trạng thái;
- tự xuất bản;
- tự ghi nghiệm thu cuối.

## 9. Bằng chứng trạng thái

Hồ sơ phải ghi:

```yaml
production:
  status: validated
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

Tên trường chính thức sẽ được khóa khi thiết kế mẫu hồ sơ lõi.

## 10. Kết luận

Tách trạng thái sản xuất khỏi trạng thái xuất bản giải quyết ba vấn đề:

- một bài có thể đạt nhưng chưa công khai;
- lưới thẻ không phải nơi lưu toàn bộ vòng đời;
- checker không thể vô tình biến nghiệm thu thành xuất bản.
