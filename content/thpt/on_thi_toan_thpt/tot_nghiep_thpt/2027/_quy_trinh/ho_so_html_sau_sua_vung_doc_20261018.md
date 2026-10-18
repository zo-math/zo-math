# Dựng lại sáu HTML sau hiệu chỉnh bìa và vùng đọc — 18/10/2026

[Bộ xem mới](http://127.0.0.1:8877/_audit/html_six_20261018/index.html).

- HTML: `E:\zo_math\_audit\html_six_20261018\html`; bản nguồn cách ly: `E:\zo_math\.quarto\html_six_20261018`.
- Tệp mở lại sau reboot: `E:\zo_math\_audit\html_six_20261018\Mo_ban_xem_HTML.cmd`. Công cụ mở lại canonical kiểm HTTP đúng nội dung và tái dùng máy chủ 8877; không dựng lại.
- Dựng từ sáu QMD hiện hành và toàn bộ sửa nguồn đang có, qua launcher chính thức. Gói dùng `zo_qmd.py render --html-only`, Nhà dùng `zo_quarto.py render --to html`. G04 giữ `draft: true`, xem bằng profile `on-thi-preview`; lần đầu thiếu profile tạo trang rỗng và bị cổng chặn, đã dựng lại riêng G04 đúng profile. Không thay trạng thái bản thảo hoặc bỏ cổng kiểm.
- Đổi breadcrumb thành “Khóa 2027”, bỏ CTA bìa thừa; nhiệm vụ/lời giải Khởi động G01/G02 có vùng riêng. G03/G04, D0 và Nhà giữ phân vùng phù hợp từng chức năng. Trong bộ xem mới, từng trang điều hướng đến đủ sáu trang mới.
- Bốn HTML thông tin được liên kết ở chân trang và tài nguyên kèm theo được sao chép nguyên trạng từ thành phẩm hiện có; không dựng lại các trang ngoài phạm vi. Không dùng HTML cũ làm nguồn sinh sáu trang.

## Kiểm đã thực hiện

- Kiểm sáu trang: 427/427; cổng riêng Nhà: 111/111; D0: 135/135.
- Trình duyệt 1440 px và 390 px: 208/208, gồm tải ảnh, tràn trang, vùng trắng, khoảng cách, bảng, menu sáu trang, mục lục mobile và 15 vòng đi–về Khởi động. Đã xem ảnh chụp vùng đọc G01/G02 và bìa D0.
- Hai báo lệch trục ban đầu thuộc tiêu đề vùng Ủng hộ hai cột có logo của G02. Đã kiểm lại đúng hai view và giới hạn phép đo trục vào giấy nội dung bài; không sửa sản phẩm để ép component Ủng hộ thành giấy bài học. Giữ báo cáo ban đầu và báo cáo kiểm lại 16/16 trong audit.
- Toàn bộ chữ người học (không tính nhãn ngữ cảnh), MathML/TeX và tập ID nguồn so với bộ xem trước được giữ. Các liên kết cục bộ và đích fragment đều tồn tại.
- PDF học liệu, website đã xuất bản, bộ xem cũ và Git index được bảo vệ theo fingerprint; không đổi. Không commit/push/xuất bản.

Bằng chứng tại `_audit/html_six_20261018`: `source-manifest.json`, `render-results.json`, các log, `qa-static.json`, `qa-browser-final.json`, `qa-home-final/qa.json`, `qa-d0-final/qa.json`, `support-dependencies.json`, `final.json` và `screenshots/`. Nguồn hiển thị giữ snapshot dựng; chỉ hồ sơ/trạng thái điều hành được cập nhật sau kiểm.

Trạng thái: sáu HTML đã dựng và kiểm kỹ thuật, chờ chủ trì xem/duyệt. Chưa tạo lại PDF học liệu, chưa xuất bản. Bìa D0 vẫn theo hướng đã duyệt và đang chờ duyệt ảnh thành phẩm; không tự nâng cờ duyệt.
