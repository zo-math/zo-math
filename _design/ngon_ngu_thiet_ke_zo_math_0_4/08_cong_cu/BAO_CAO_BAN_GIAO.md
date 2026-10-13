# Báo cáo kiểm bộ bàn giao 0.4.2

Ngày: 07/10/2026. Đây là kiểm bộ tài nguyên/điều hành; không phải kiểm thị giác tích hợp vào sản phẩm.

## Bản vá 0.4.2

0.4.2 sửa lỗi đóng gói `DESIGN04-INTEGRITY-001`: tệp `00_BAT_DAU_O_DAY.md` trong thư mục và ZIP 0.4.1 khớp nhau nhưng mục tương ứng trong manifest 0.4.1 dùng kích thước/hash của một bản khác. Bản vá giữ nguyên mẫu thiết kế 0.4, cập nhật số phiên bản tài liệu điều hành và tạo manifest mới từ các tệp phát hành hiện hành. ZIP 0.4.1 được giữ lại làm bản trước; không dùng việc sửa manifest để thay đổi quy tắc hay tài sản thiết kế.

## Phạm vi gói

- 30 đầu vào gốc: 29 Markdown và source_bundle.zip, giữ nguyên byte và có SHA-256.
- Bản giải nén source_bundle để AI đọc trực tiếp.
- Toàn bộ 361 tệp của gói mẫu 0.4 đã phát hành, giữ cấu trúc nội bộ; gồm mẫu xem/nghe, tài sản, nguồn dựng và bằng chứng kiểm cũ.
- 30 bản ghi quy tắc/yêu cầu phân biệt trạng thái; 21 trích đoạn chủ dự án; 18 miền nghiên cứu được giữ trong danh mục.
- 6 hướng dẫn tích hợp: web, video, đồ thị/hình học, ảnh bìa, bảng biến thiên, PDF.
- Điểm bắt đầu cho người dùng, lệnh khởi động cho Codex, chỉ dẫn AI, sổ công việc, hồ sơ tiếp nhận, mẫu báo cáo/quyết định và công cụ kiểm chỉ đọc.
- Mốc thử nghiệm web 2027 và sổ phản hồi 0.4 → 0.5 nằm trong vùng vận hành; chưa thay đổi mẫu thị giác 0.4.

## Cách kiểm

Đối chiếu hash các đầu vào với tệp được cung cấp; đối chiếu từng thành viên mẫu với ZIP 0.4; kiểm ID/căn cứ, trạng thái quy tắc, thang màu, đường dẫn tài sản và liên kết tài liệu điều hành. Chạy công cụ từ thư mục khác để xác minh không phụ thuộc cwd. Sáu ca kiểm công cụ bao gồm bản sạch, thiếu logo, trạng thái/căn cứ không hợp lệ, sửa nguồn gốc, nhật kí được cập nhật hợp lệ và đường dẫn ra ngoài bộ. Kết quả máy ở [kết quả kiểm](../_audit/ket_qua_kiem.json).

## Giới hạn có chủ đích

Nguồn lịch sử được giữ nguyên, nên một số liên kết của chúng vẫn trỏ tới nơi không nằm trong bộ. Dùng mục lục nguồn và lệnh find; danh mục thiếu của source_bundle vẫn có hiệu lực. Kiểm liên kết vận hành áp dụng cho tài liệu mới của bộ, không tuyên bố đã sửa mọi liên kết lịch sử.

Nguồn dựng 0.4 có phần phụ thuộc thư mục nghiên cứu cũ. Tài sản xuất sẵn dùng để xem độc lập; mã dựng dùng làm tham khảo khi tích hợp vào repo, không được quảng cáo là một lệnh dựng lại toàn bộ ở mọi máy. Công cụ zo_design.py riêng chạy bằng Python chuẩn, không cần thư viện ngoài.

Checker bộ bàn giao và sáu ca kiểm công cụ đã chạy trên Windows qua launcher của repo. Chưa chạy lại Quarto, pipeline video/ảnh hoặc kiểm trình duyệt cho lớp thị giác 0.4; chưa nâng các mẫu âm/logo thành quyết định cuối. Các kết quả 359 kiểm của mẫu nằm trong qa của mẫu, tách khỏi kết quả kiểm bộ bàn giao.

Bộ bàn giao không tự động thi hành thay đổi thiết kế. Người dùng hoặc AI đọc quy trình, áp dụng vào mã hiện tại trong phạm vi nhiệm vụ và ghi kết quả. Không cần cuộc trò chuyện gốc để tra các căn cứ đã kết tinh ở đây.
