# Sổ yêu cầu, quyết định và mẫu thử

Đọc cột trạng thái trước khi áp dụng. “Yêu cầu đã xác nhận” không đồng nghĩa chủ dự án đã duyệt từng pixel của tệp hiện thực. Nguồn YC nằm trong [phản hồi](../06_nguon/yeu_cau_chu_du_an/phan_hoi_thiet_ke.md); nguồn S nằm trong [mục lục nguồn](../06_nguon/00_muc_luc.md). Dữ liệu tương ứng: [quy_tac.json](../03_du_lieu/quy_tac.json).

## ZO001 — Màu

**Yêu cầu đã xác nhận**. Giữ Đỏ ZO #EF5350, Vàng ZO #FFCA28, Xám ZO #3E3A35 và 23 mã thang màu 0.4.

Phạm vi: Mọi sản phẩm dùng hệ màu này.

Căn cứ: YC04, YC07. Giới hạn: Tên và mã; không tự coi mọi vai trò màu đã được duyệt.

## ZO002 — Màu

**Yêu cầu đã xác nhận**. Tên token red-1..7, yellow-1..7, gray-1..9; bảo toàn ánh xạ tên cũ.

Phạm vi: Cấu hình dùng chung.

Căn cứ: YC08. Giới hạn: Thứ tự nhạt đến đậm là cách hiện thực 0.4; số không biểu thị khoảng cách cảm nhận đều.

## ZO003 — Logo

**Yêu cầu đã xác nhận**. Z đỏ và O vàng không viền O; mỗi chữ trong một ô Xám ZO độc lập.

Phạm vi: Hướng logo đang phát triển.

Căn cứ: YC09. Giới hạn: Tỉ lệ ô, hình chữ và khoảng hở của các SVG là mẫu thử.

## ZO004 — Logo

**Mẫu thử / chưa chốt chi tiết**. Dùng họ SVG logo 0.4 để thử; bản màu, một màu, đứng/ngang và kích thước nhỏ.

Phạm vi: Mẫu và sản phẩm thử.

Căn cứ: YC09. Giới hạn: Chưa chốt logo master cuối; cần duyệt ở kích thước sử dụng.

## ZO005 — Tương tác

**Yêu cầu đã xác nhận**. Link không gạch chân; màu/hover; thẻ hiện hành có khung màu.

Phạm vi: Web và giao diện tương tác.

Căn cứ: YC10. Giới hạn: Trạng thái bàn phím cần rõ; không bỏ outline chỉ vì không dùng gạch chân.

## ZO006 — Bố cục

**Yêu cầu đã xác nhận**. Sáu tùy chọn nền từ ba thang; khối nội dung trắng; giữ Sắc xám.

Phạm vi: Web.

Căn cứ: YC12, YC13. Giới hạn: Không suy thành sáu phiên bản xuất video/PDF bắt buộc.

## ZO007 — Bố cục

**Mẫu thử / chưa chốt chi tiết**. Thử red-1/2, yellow-1/2, gray-2/3; mặc định gray-3.

Phạm vi: Web 0.4.

Căn cứ: YC12. Giới hạn: Cơ chế sáu nền đã được yêu cầu; sáu token cụ thể và mặc định do trợ lí chọn trong mẫu.

## ZO008 — Bố cục

**Yêu cầu đã xác nhận**. Hạn chế đường ngang chia nội dung; dùng khoảng trắng và cấp tiêu đề.

Phạm vi: Bố cục trang.

Căn cứ: YC14. Giới hạn: Không áp dụng lệnh bỏ đường kẻ cho lưới bảng dữ liệu.

## ZO009 — Bảng

**Yêu cầu đã xác nhận**. Đủ đường ngang-dọc; tránh đường đầu/cuối quá đậm; toán dàn LaTeX.

Phạm vi: Bảng học liệu.

Căn cứ: YC05. Giới hạn: Độ dày 1px và màu gray-3 của mẫu cần kiểm ở từng phương tiện.

## ZO010 — Bảng

**Yêu cầu đã xác nhận**. Hàng hàm số phẳng, chỉ một hàng; giữ nguyên những hàng dữ kiện có trong nguồn.

Phạm vi: Bảng biến thiên.

Căn cứ: YC11. Giới hạn: Không tự thêm hàng đạo hàm; không tự sửa ví dụ sai có chủ ý.

## ZO011 — Bảng

**Mẫu thử / chưa chốt chi tiết**. Hàng/cột nhấn yellow-1; ô giao yellow-2; tổng gray-2; lỗi có giải thích red-1.

Phạm vi: Bảng 0.4.

Căn cứ: YC05. Giới hạn: Đây là đề xuất phân vai, không phải ý nghĩa toán tự có của màu.

## ZO012 — Nhãn

**Yêu cầu đã xác nhận**. Tag phụ, nhỏ và mờ, small caps, không hộp, ngay phía trên trái nội dung.

Phạm vi: Khối nội dung.

Căn cứ: YC06. Giới hạn: Cỡ .79em và gray-6 của mẫu chưa là tham số chốt toàn hệ.

## ZO013 — Toán

**Yêu cầu đã xác nhận**. Hàm từng khoảng có “khi”; dấu phẩy cuối các dòng trước và dấu chấm cuối dòng cuối.

Phạm vi: Diễn đạt công thức từng khoảng.

Căn cứ: YC03. Giới hạn: Giữ điều kiện toán; không dùng dấu câu thay cấu trúc xuống dòng LaTeX.

## ZO014 — Ủng hộ

**Yêu cầu đã xác nhận**. Thiết kế lời mời Ủng hộ ZO Math nổi bật, xuất hiện thêm ở vị trí phù hợp.

Phạm vi: Web/PDF và bối cảnh thích hợp.

Căn cứ: YC15. Giới hạn: Không mặc định chèn lời mời nhiều lần vào mọi video ngắn.

## ZO015 — PDF

**Yêu cầu đã xác nhận**. Đánh giá và thiết kế trang đầu/trang cuối PDF theo hệ chung.

Phạm vi: PDF.

Căn cứ: YC16. Giới hạn: 0.4 chỉ làm lại bìa/kết; ruột còn giữ bản nguồn v1.3.

## ZO016 — Giải thích

**Yêu cầu đã xác nhận**. Mỗi thiết kế có chú thích lí do, dùng trong tài liệu/mẫu kiểm.

Phạm vi: Tài liệu thiết kế.

Căn cứ: YC02. Giới hạn: Không đưa chú thích kỹ thuật thiết kế vào bài học của học sinh.

## ZO017 — Triển khai

**Yêu cầu đã xác nhận**. Áp dụng thử trước cho khóa Ôn thi Toán THPT 2027.

Phạm vi: Web khóa 2027.

Căn cứ: YC17. Giới hạn: Danh sách trang cần kiểm kê tại repo; chưa được tự đổi toàn zomath.vn.

## ZO018 — Bàn giao

**Yêu cầu đã xác nhận**. Tài nguyên và chương trình điều hành phải dùng độc lập với phiên chat.

Phạm vi: Bộ bàn giao này.

Căn cứ: YC20, YC21. Giới hạn: Quy trình cụ thể được biên soạn mới để phục vụ yêu cầu; không tự trở thành governance 1.0.

## ZO019 — Chữ

**Mẫu thử / chưa chốt chi tiết**. Thử Be Vietnam Pro cho giao diện/lời dẫn; STIX Two Text/Math cho học liệu/toán.

Phạm vi: Mẫu đa phương tiện.

Căn cứ: S02, S26. Giới hạn: Kiểm dấu tiếng Việt, nhúng font, fallback và cỡ xem thực.

## ZO020 — Dấu nhấn

**Mẫu thử / chưa chốt chi tiết**. Giữ dạng hai vạch: 15u, khe 1.75u, 8u; cập nhật vàng theo ZO001.

Phạm vi: Nhận diện phụ.

Căn cứ: S01. Giới hạn: Tệp nguồn ghi là đề xuất; không phải kí hiệu toán và không thay logo.

## ZO021 — Hình toán

**Mẫu thử / chưa chốt chi tiết**. Đỏ cho đối tượng đang xét, xám cho ngữ cảnh; vàng nhạt cho vùng chú ý; loại nét/nhãn giữ nghĩa.

Phạm vi: Đồ thị/hình học/video.

Căn cứ: S21, M04. Giới hạn: Vai trò hình học và ý nghĩa Toán phải đúng trước khi tô màu.

## ZO022 — Hình toán

**Nền nghiên cứu có căn cứ**. Phân biệt tập xác định, khoảng lấy mẫu, cửa sổ quan sát; giữ điểm hở/kín, tiệm cận/tiếp tuyến và nhãn gắn đối tượng.

Phạm vi: Kiểm tính đúng của hình.

Căn cứ: S20, S21. Giới hạn: R6 là ràng buộc nghiên cứu; không tự tạo taxonomy cuối.

## ZO023 — Nền tảng

**Nền nghiên cứu có căn cứ**. ZO Math là không gian giáo dục toán học; học sinh trung tâm dài hạn, THPT ưu tiên hiện nay; suy lí và kiến tạo ý nghĩa là nền hiện tại.

Phạm vi: Định hướng nội bộ.

Căn cứ: S08, S09, S26. Giới hạn: Không biến thành lời hứa hiệu quả hoặc wording công khai cuối.

## ZO024 — Tính cách

**Nền nghiên cứu có căn cứ**. Gần gũi trong tôn trọng; sống động nhưng điềm tĩnh; giản dị mà sâu sắc; rõ ràng và trong sáng.

Phạm vi: Định hướng biểu đạt.

Căn cứ: S15, S16, S26. Giới hạn: Đã owner-calibrate ở cấp candidate; không phải toàn bộ voice specification đã chốt.

## ZO025 — Chuyển động

**Mẫu thử / chưa chốt chi tiết**. Giữ căn tính đối tượng; cho thời gian quan sát; có bản tĩnh/giảm chuyển động trên web.

Phạm vi: Chuyển động và tương tác.

Căn cứ: S21, M04. Giới hạn: 24 giây, các mốc dừng và 24fps của clip không phải thông số chung.

## ZO026 — Âm thanh

**Mẫu thử / chưa chốt chi tiết**. Hai cue focus/close là ứng viên; không tự phát âm trên web, không dùng âm như phán xét người học.

Phạm vi: Mẫu âm 0.4.

Căn cứ: M04. Giới hạn: Chưa duyệt giọng thương hiệu, sonic logo, nhạc và mức phối âm.

## ZO027 — Phụ đề

**Hướng dẫn kế thừa theo phạm vi**. Văn bản thuần, Unicode cho biểu thức đơn giản; biểu thức phức tạp đưa vào vùng công thức LaTeX đã render.

Phạm vi: Phụ đề và mô tả chỉ nhận văn bản thuần.

Căn cứ: S02. Giới hạn: Không áp dụng Unicode để thay công thức LaTeX trong nội dung QMD/bảng.

## ZO028 — Lập luận

**Nền nghiên cứu có căn cứ**. Ưu tiên diễn đạt suy luận bằng câu; không lạm dụng kí hiệu suy ra/tương đương.

Phạm vi: Diễn đạt Toán.

Căn cứ: S26. Giới hạn: Công thức thật vẫn phải được dàn đúng; không giả lập công thức bằng text thường.

## ZO029 — Bìa và thẻ

**Mẫu thử / chưa chốt chi tiết**. Một hệ chữ/màu/logo; bố trí lại theo tỉ lệ, không kéo giãn hoặc cắt mù.

Phạm vi: Ảnh bìa và phân phối.

Căn cứ: S02, M04. Giới hạn: Kiểm hình thu nhỏ và vùng bị giao diện nền tảng che ở thời điểm xuất.

## ZO030 — Vận hành

**Đề xuất vận hành của bộ bàn giao**. Mỗi lần áp dụng ghi nguồn phiên bản, phạm vi, bằng chứng kiểm và cách hoàn tác.

Phạm vi: Quy trình bàn giao.

Căn cứ: S06, YC21. Giới hạn: Không thêm thủ tục xin phép cho chỉnh sửa nhỏ đã được giao; không tự phê duyệt thiết kế hoặc xuất bản.
