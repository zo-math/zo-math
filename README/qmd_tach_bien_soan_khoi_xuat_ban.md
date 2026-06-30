# TÁCH BIÊN SOẠN KHỎI XUẤT BẢN

## Vấn đề

Khi soạn các tệp `.qmd` trong dự án ZO Math, mục tiêu thực tế là vừa viết vừa nhìn ngay kết quả để chỉnh sửa nhanh. Nếu cố dùng `quarto preview` làm công cụ biên soạn chính, công việc dễ bị chậm và rối.

## Giải pháp

Tách công việc thành hai phần.

### 1. Biên soạn

Dùng **Markdown Preview** trực tiếp trên tệp `.qmd`.

Mục đích:

- xem ngay tiêu đề, đoạn văn, danh sách, công thức, cấu trúc bài
- kéo tới đâu xem tới đó
- chỉnh sửa nhanh trong lúc viết

### 2. Xuất bản / kiểm tra bản thật

Khi cần xem đúng giao diện website Quarto, mới dùng:

```bash
cd /e/zo-math
quarto preview
```

Hoặc khi cần render chính thức:

```bash
quarto render
```

## Nguyên tắc làm việc

- **Markdown Preview** = công cụ biên soạn
- **Quarto Preview** = công cụ kiểm tra bản xuất bản
- **Quarto Render** = công cụ tạo đầu ra chính thức

## Kết luận

Không nên ép `quarto preview` làm công cụ chính để chỉnh từng câu từng đoạn.

Cách làm đúng cho ZO Math là:

- viết và hiệu chỉnh bằng **Markdown Preview**
- lâu lâu kiểm tra bằng **Quarto Preview**
- khi chốt thì dùng **Quarto Render**
