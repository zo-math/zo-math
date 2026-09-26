# Quy chuẩn tổ chức học liệu Ôn thi Toán THPT

Tài liệu nội bộ, chỉ áp dụng cho chuyên mục này. Pha 1 xác lập khung và ranh giới xuất bản, chưa triển khai bộ kiểm định gói hoặc chuyển học liệu.

## Một bộ nguồn hiện hành

- Mỗi gói dùng lại nằm tại `hoc_lieu/<ma_goi>/`, độc lập với năm thi.
- `index.qmd` là nguồn biên soạn văn bản duy nhất của gói sau khi chuyển đổi được nghiệm thu. Dữ liệu có cấu trúc và tài sản hình được dẫn chiếu, không chép thành một nguồn bài học thứ hai.
- HTML/PDF là đầu ra sinh, không sửa tay. Mốc lịch sử không được tiếp tục dùng như nguồn phát triển song song.
- Trang khóa `tot_nghiep_thpt/<nam>/index.qmd` dẫn tới học liệu dùng lại; không sao chép bài vào từng khóa.
- Điều hành khóa và hồ sơ nội bộ nằm trong `_quy_trinh`, không đưa nguyên tài liệu điều hành lên trang người học.

## Hợp đồng cho pha tích hợp gói sau này

Mỗi gói sẽ có cấu hình kỹ thuật cục bộ với định danh duy nhất và hồ sơ `_quy_trinh/ho_so/index.yml`, cùng dùng hợp đồng và bộ kiểm định chung của chuyên mục. Cách này tránh va chạm hồ sơ giữa các nguồn cùng tên `index.qmd`.

Mẫu `mau_ho_so_san_xuat.yml` hiện chỉ ghi các quyết định cần có; chưa là schema được CLI hỗ trợ. Không tự đăng ký adapter, sửa receipt PDF hoặc tạo hồ sơ R1-G01 trong Pha 1.

Khi chuyển đổi được giao ở pha sau, phải bảo toàn nội dung, nhiệm vụ, thuật ngữ, ID, bảng và hình; kiểm chứng HTML tương tác và toàn bộ PDF. Phân biệt kiểm định tự động, nghiệm thu của con người và quyết định xuất bản. Không tự đổi trạng thái nghiệm thu/xuất bản.

## Hàng rào bắt buộc

Các trang và tài sản đã duyệt của chuyên mục chỉ được chọn qua allowlist trong `publish_public.yml`. `_quy_trinh` luôn bị chặn kể cả khi mở các trang học. Không đưa liên kết, dữ liệu chỉ mục hay resources chứa đường dẫn nội bộ vào cây public.

Preview dùng profile `on-thi-preview`, chỉ ở `127.0.0.1`; không phải pipeline xuất bản. `zo_publish.py` phải từ chối profile này và kiểm tra đường dẫn bị cấm sau chuẩn hóa trong manifest, HTML, `search.json` và sitemap.
