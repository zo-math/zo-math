# Kiểm tra thành phẩm R1-G01 v1.1

## Phạm vi

Kiểm tra nguồn sản xuất canonical, khả năng tái sinh Markdown/HTML/PDF, cấu trúc đầu ra và hiển thị trực quan của ứng viên v1.1. Kết quả kiểm tra không thay thế quyết định duyệt phát hành hoặc dữ liệu sử dụng của học sinh.

## Trạng thái trước kiểm tra

- Nghiên cứu đã kết tinh ở cấp gói.
- v1.0 đã được đọc và tiếp nhận góp ý.
- v1.1 đang thẩm định.
- Chưa duyệt phát hành, chưa công bố website và chưa sản xuất Studio chính thức.

## Kết quả

### 1. Đầu vào đã ghi nhận

| Tài sản | SHA-256 |
|---|---|
| Khung điều phối tiền nhiệm | `efb71112cf9847377faaeac436ac42d91dd3ef2fd0573e3ca8fd9676302879af` |
| Kết quả nghiên cứu tiền nhiệm về đơn điệu | `eadff3c4720aa757d9432465cd8615c5726c260fa1046bb0de74cbfbd03155fb` |
| Kết quả nghiên cứu tiền nhiệm về cực trị | `1abea1c4feee91223c40e4f09439b0d22343c731cac8c63ee42a0c922571154a` |
| Gói bàn giao v1.0 | `c67d9c15b98290d6405fc2e0545fd129bbd72579952ff7b9df9209586afe3c97` |
| Gói bàn giao v1.1 | `8d51e2edeefddacfda7330954129a4d5a7924f55828a2b8450a5377071261a73` |
| Đề cương sản xuất 0.1 | `0866cfe15d4e486d66963b4798672b72fa85adbf0d426999bcdb2e1d55bc6420` |
| Nội dung nền 0.1 | `351942d1030525aa0db22307f0c699b78797e6d351eec63537b6f03bf49ac25a` |
| Ma trận biên tập 0.1 | `7ea1d221cc52681c3573ff9efa4968ad5da6ada2f4bb9b4f71922c836c4272a5` |
| HTML v1.0 rời | `88f21482c84a97db548c43c947b59ea519e96cce704a3fd2c8c01783738b0ac4` |
| HTML v1.1 rời | `4444529f326188efd86d3677ec60ac076c52a6cf66be24c53bd56122ee8af67c` |
| PDF v1.1 rời | `4f8fa22d374dd60b59f806e383a4a8b546103559217c0acdbc33f098a316e480` |

HTML v1.0 rời trùng bản tương ứng trong gói v1.0. HTML v1.1 rời trùng bản tương ứng trong gói v1.1. PDF v1.1 rời không trùng PDF trong gói v1.1; vì vậy không chọn một trong hai làm current mà tái sinh PDF từ nguồn canonical.

### 2. Tái sinh

Các lệnh đã chạy từ gốc repository:

```text
python scripts/zo_python.py -m py_compile _projects/on_thi_toan_thpt_2027/goi/R1-G01/src/bang_bien_thien.py _projects/on_thi_toan_thpt_2027/goi/R1-G01/src/zo_bieu_dien.py _projects/on_thi_toan_thpt_2027/goi/R1-G01/src/dong_goi.py _projects/on_thi_toan_thpt_2027/goi/R1-G01/src/xuat_pdf.py
python scripts/zo_python.py _projects/on_thi_toan_thpt_2027/goi/R1-G01/src/zo_bieu_dien.py
python scripts/zo_python.py _projects/on_thi_toan_thpt_2027/goi/R1-G01/src/dong_goi.py
python scripts/zo_python.py _projects/on_thi_toan_thpt_2027/goi/R1-G01/src/xuat_pdf.py
```

Kết quả:

- bốn script Python biên dịch cú pháp thành công;
- dựng đủ 10 đồ thị ở cả SVG và PNG;
- sinh lại Markdown và HTML thành công;
- sinh lại PDF thành công, 35 trang A4;
- PDF không mã hóa, không biểu mẫu, không JavaScript;
- metadata PDF đúng tên học liệu, R1-G01 v1.1 và tác giả ZO Math.

SHA-256 đầu ra tái sinh:

| Đầu ra | SHA-256 |
|---|---|
| `R1-G01_NOI_DUNG_v1.1.md` | `e4548e4ec13f8e6c7fe90af2a7d3730bcf334d70c5ed93f720b8443e60498b80` |
| `R1-G01_HOC_LIEU_v1.1.html` | `40137f0ffb59abeb697e575c73e87b2a1633c527954b1dd9643b49bd55e6b397` |
| `R1-G01_HOC_LIEU_v1.1.pdf` | `7794a138df911e6e3dcda9102a9fdb715be1a85e96f19272b606cc21cec5575d` |

Đầu ra tái sinh khác hash bản bàn giao vì đường dẫn tài sản được chuẩn hóa theo `src/`, đồ thị được dựng lại và PDF được tạo lại từ nguồn canonical.

### 3. Kiểm tra HTML

- 16 khối `details` chứa phần có thể mở khi cần.
- 10 SVG được nhúng trực tiếp.
- 2 font được nhúng trực tiếp.
- Không có tài nguyên `src` hoặc `href` phụ thuộc HTTP bên ngoài.
- Không có liên kết neo nội bộ trỏ đến đích bị thiếu.
- Nguồn hiển thị không còn hệ định danh nghiên cứu tiền nhiệm.

Không kiểm tra tương tác trực tiếp bằng trình duyệt trong môi trường này vì kết nối trình duyệt cục bộ không khởi tạo được. Cấu trúc HTML, tài sản nhúng và liên kết đã được kiểm tra bằng mã.

### 4. Kiểm tra PDF và trực quan

- Render đủ 35/35 trang thành PNG bằng Poppler.
- Kiểm tra toàn bộ trang qua bốn bảng ảnh thu nhỏ và kiểm tra chi tiết các trang 1, 5, 10, 15, 20, 25, 27, 30, 34 và 35.
- Không thấy chữ bị cắt, chồng lớp, ô đen, lỗi glyph hoặc bảng tràn lề.
- Công thức, bảng biến thiên và đồ thị rõ; màu, tiêu đề, đầu trang, chân trang và số trang nhất quán.
- Phần chuyển từ bài học sang luyện tập, kiểm tra, sửa lỗi, lời giải và nguồn đối chiếu rõ ràng.
- Log dựng không có lỗi kết thúc; PDF được tạo đủ 35 trang.

### 5. Giới hạn trạng thái

Kết quả trên xác nhận khả năng tái sinh và chất lượng kỹ thuật của ứng viên v1.1. Nó không xác nhận hiệu quả học tập, không thay thế phản biện chuyên môn độc lập và không làm thay đổi trạng thái: **đang thẩm định, chưa duyệt phát hành, chưa công bố website, chưa sản xuất Studio chính thức**.
