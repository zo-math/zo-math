# R1-G05 — Sửa chú thích nguồn và căn giữa công thức, 21/10/2026

Theo phản hồi của chủ trì về HTML G05, đã sửa nguồn và dựng lại chỉ HTML G05 ở vị trí chuẩn trong `docs/`. HTML và bố cục bìa tiếp tục chờ chủ trì duyệt; chưa dựng PDF, commit, push hoặc xuất bản.

## Lỗi, nguyên nhân và sửa nguồn

Bảy tham chiếu nguồn trong QMD đã bị chuyển thành footnote đánh số ở lượt chuyển ban đầu. Các số đứng riêng không giải thích tài liệu/vị trí đang dẫn, trái 07/6.3 và mục Công thức và nguồn đối chiếu của quy chuẩn gói. Đã thay bằng bảy đoạn `.zo-source-note` ngay sau nội dung liên quan: câu hoàn chỉnh, tên tài liệu đầy đủ, ghi rõ Bài/mục/trang; giữ phần phân biệt dữ kiện ZO Math tự biên soạn. Bỏ adapter đưa footnote về cuối trang. Component dùng chung sở hữu cỡ 12 px, màu xám phụ; đoạn dài được xuống dòng theo khung để đọc được trên điện thoại, không ép một hàng vật lý.

CSS dùng chung đã gán `display:block` cho MathML riêng dòng, làm mất chế độ toán native và căn giữa. Đã sửa thành `display:block math`, giữ vùng cuộn ngang cục bộ. Gói sử dụng lại cùng nguồn CSS; không ghi CSS chữa riêng trong HTML. Một binding tài nguyên CSS hiện hành trong `r1_g01/giao_dien/web_2027_layout.json` được đồng bộ đúng đầu vào mới, không đổi bố cục, nội dung hoặc biên nhận nghiệm thu G01. Lần dựng đầu bị cổng binding chặn; báo cáo FAIL được giữ riêng. Chỉ sau khi sửa đúng binding nguồn mới dựng lại; không tắt cổng hoặc sửa thành phẩm.

## Kiểm chứng

- CLI QMD HTML-only đạt; kiểm gói 1900/1900, không có tệp/neo hỏng. HTML có 576 biểu thức, 9 bảng, 89 vùng đọc; giảm một vùng vì bỏ danh sách footnote cuối bài.
- 567 biểu thức toán trong QMD không đổi thứ tự hoặc nội dung. Bản thảo và các hình giữ nguyên.
- Trình duyệt ở 1440 và 390 px: đủ bảy nguồn, chữ 12 px nhỏ hơn chính văn 17/16 px, màu xám nhẹ hơn; không còn footnote đánh số. Đủ 23 công thức riêng dòng; sai lệch tâm của công thức vừa khung dưới 0,01 px. Trên điện thoại, 11 công thức dài cuộn riêng; trang không tràn ngang.
- Cổng kiểm âm tái hiện số nguồn trơ, tên nguồn viết tắt, CSS `display:block`, mất quy tắc hoặc mất cuộn; hồi quy toán 45/45. Cổng trình bày trên bốn HTML đã phát hành đạt 837/837, 592/592, 765/765, 710/710, đọc trong bộ nhớ, không dựng lại.
- Trong 850 tệp được đối chiếu từ lượt chuyển trước, 849 giữ nguyên; chỉ một binding CSS nguồn nói trên đổi đúng một checksum. Sáu HTML, 33 PDF và tài nguyên đã phát hành giữ nguyên. Chưa triển khai CSS mới sang các HTML cũ trong lượt này.

Bằng chứng: `_audit/g05_notes_math_20261021/` gồm baseline, báo cáo dựng đầu/chốt, checks.json, math_regression.json, shared_note_regression.json, css-binding-transition.json, số đo/ảnh trình duyệt và bản bàn giao mới. `_audit/` chỉ giữ bằng chứng. Nguồn chính thức tiếp tục là QMD, CSS và adapter; HTML chuẩn ở docs. Kiểm kỹ thuật không thay chủ trì nghiệm thu hoặc kiểm toán độc lập; không có dữ liệu quan sát học sinh.
