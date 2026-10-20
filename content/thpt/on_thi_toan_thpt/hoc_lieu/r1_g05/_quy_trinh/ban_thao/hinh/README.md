# Minh họa thực tế R1-G05 — nguồn bản thảo

## Đã tạo gì?

| Hình | Vai trò | Dữ liệu toán hoặc giới hạn |
|---|---|---|
| `hop_cat_gap` | Gợi mở 04, từ tấm bìa tới hộp mở | Tấm vuông cạnh $30$; kích thước mẫu để dựng cảnh là $x=4$, không phải lời giải tối ưu. Nhãn giữ biến $x$; nét đứt là đường gấp, dấu chéo là phần bỏ. |
| `khu_dat_sat_tuong` | Nhiệm vụ 11, nhận diện ba cạnh cần rào | Hai cạnh $x$, một cạnh $y$; tường không tính vào hàng rào. Tỉ lệ cảnh chỉ minh họa. |
| `quay_ban_hang` | Bối cảnh của Ví dụ 04 | Số hộp vẽ không là dữ liệu nhu cầu. Thẻ giá làm rõ biến quyết định; không bịa số khách. |
| `be_khong_nap` | Nhiệm vụ 21, một đáy và bốn thành | Đáy vuông cạnh $x$, cao $h$, không có nắp; không vẽ mực nước hoặc suy thể tích từ ảnh. |
| `khu_dat_co_vach` | Nhiệm vụ 26, sửa quan hệ ràng buộc | Thêm một vách vuông góc tường, tạo ba đoạn $x$ cần rào. |
| `huong_bia` | Phác hướng để chủ trì duyệt riêng | Cảnh cắt–gấp không nhãn/kích thước; chưa là bìa production hoặc được nghiệm thu. |

Mỗi cảnh có SVG vector và PNG để xem ngay trong Markdown. Nguồn duy nhất của cấu hình là `minh_hoa.json`; mã dựng là `sinh_minh_hoa.py`. Không sửa trực tiếp SVG/PNG.

## Khả năng của công cụ hiện có và phần bổ sung

Đã đọc `E:/zo_math_graphics/README.md`, engine geometry và cửa graph. Geometry có khối hộp lồi, đa diện lồi và các khối tròn xoay; graph/variation dựng đồ thị và bảng biến thiên. Chúng vẫn là nguồn công cụ chính thức cho các vai trò ấy. Chưa có một component cảnh cắt bốn góc–gấp hộp mở, cảnh hàng rào tựa tường có vách, hoặc quầy bán hàng được đóng gói sẵn trong API đã khảo sát. Không kết luận các cảnh này bất khả thi bằng TikZ nói chung.

Bộ bổ sung ở đây dựng **cảnh minh họa tham số**, không phải bộ thay thế geometry/graph. Nó dùng phép chiếu affine cho hình khối, lớp mặt xa–đáy–mặt gần cho vật mở, và component bối cảnh (tường, rào, vách, quầy, mái, thẻ giá). Phông STIX Two Text/Math, màu và độ rộng nét được đọc trực tiếp từ nguồn dùng chung thông qua `scripts/zo_graphics.py`; không chép engine hay tự tạo palette.

Đầu ra SVG/PNG đi thẳng từ nguồn, không tạo HTML, QMD hoặc PDF, kể cả PDF hình trung gian. Không chạy engine graph/geometry build vì đường dựng ấy sinh PDF kèm theo và lượt này giới hạn ở bản thảo/hình.

## Có tái sử dụng được không?

Có, ở mức **họ cảnh đã hỗ trợ**:

- Cắt–gấp: đổi chiều dài, chiều rộng, cạnh cắt và nhãn tương ứng trong cấu hình; kiểm tự động điều kiện cắt và bảo toàn diện tích còn lại.
- Khu đất: đổi chiều dài, chiều sâu, không vách hoặc một vách. Hình Nhiệm vụ 11 và 26 được sinh bằng cùng hàm, là hai lần dùng thực tế trong gói.
- Hộp/bể mở: cùng hàm dựng khối mở, thay kích thước, nhãn, độ trong của thành; ảnh hộp và ảnh bể cùng dùng cơ chế này.
- Quầy: component cảnh dùng lại được trong cùng loại bối cảnh; đổi vật phẩm hoặc cấu trúc quầy cần sửa nguồn và xem lại, không có lời hứa tự dựng mọi cửa hàng.

Giới hạn: chưa là thư viện dùng chung đã nghiệm thu; phép chiếu không tự xử lí mọi giao cắt hoặc vật thể tùy ý; chỉ hỗ trợ nhãn chữ và biểu thức ngắn đã khai, không thay máy dàn trang LaTeX. Cảnh mới ngoài các họ này cần thiết kế, kiểm toán và kiểm ảnh riêng. Khi chuyển sang production, phải chọn rõ cách tích hợp hoặc tách thành công cụ chung, có fixture và phê duyệt; không chép SVG bản thảo sang tài nguyên chính thức để bỏ qua quy trình.

## Chạy và kiểm

Từ gốc repo, dùng launcher:

```text
python -B scripts/zo_python.py -B content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g05/_quy_trinh/ban_thao/hinh/sinh_minh_hoa.py
```

Lệnh chỉ ghi vào chính thư mục hình bản thảo. `manifest.json` giữ hash dữ liệu, mã sinh, style, hai phông và từng ảnh. Có ba ca âm: cắt làm suy biến đáy, số vách chưa hỗ trợ, chiều cao không dương. Có kiểm nhãn nằm trong canvas, không phóng glyph bất thường, SVG không nhúng raster. Hash là bằng chứng nguồn–đầu ra, không là giấy nghiệm thu.

Đã xem trực tiếp sáu PNG bản cuối: không cắt nhãn; nhãn tường được dời khỏi đường tường; các chữ toán dùng STIX Two Math. Lần đầu phát hiện glyph CFF qua đường kết xuất phông của Matplotlib bị méo/phóng lớn. Đã sửa **mã sinh**: dùng fontTools lấy outline từ đúng tệp STIX rồi tạo path vector cho cả SVG/PNG, không thay phông và không vá ảnh. Đã sinh lại và xem lại. Đây là sửa ở đường dựng riêng, không thay công cụ chung hoặc font gốc.

Kích thước bản vẽ: cắt–gấp hai khung ngang $22\times8$ cm; khu đất/quầy $16\times9$ cm; bể $12\times9$ cm. PNG $180$ dpi dùng đọc bản thảo; SVG giữ nét vector. Bản thảo chưa có trình bày web responsive: chưa khẳng định kiểm điện thoại/khung đọc hoặc PDF. Khi tích hợp, giữ cỡ đọc được, cuộn hình cục bộ khi cần, không ép thu nhỏ để đủ chiều ngang.

## Hiệu chỉnh đường kích thước theo phản hồi ngày 20/10/2026

Lần kiểm ảnh trước đã bỏ sót việc hai đầu đoạn đo không khớp cạnh. Hàm cũ nhận tọa độ đã dịch thủ công, không giữ liên hệ với đỉnh gốc, không có đường dóng; `FancyArrowPatch` còn mặc định co hai đầu đoạn đo. Các kiểm hash, glyph và canvas trước đó không phát hiện loại lỗi này.

Đã sửa hàm `dim` trong nguồn dựng: nhận đúng hai đỉnh của cạnh, dịch cùng một khoảng theo phương vuông góc, vẽ đường dóng từ đỉnh tới quá đường kích thước; đoạn đo không bị co, vạch đầu đặt đúng đầu đoạn. Các nhãn và dữ liệu toán không đổi. Cùng cơ chế dùng cho tấm bìa, hộp/bể và khu đất; không sửa tay SVG/PNG hoặc công cụ ngoài repo.

Đã kiểm đủ 15 đoạn đo: 6 ở hình cắt–gấp, 3 ở khu đất sát tường, 3 ở bể, 3 ở khu đất có vách. Năm ca hồi quy cố ý sửa đối tượng nét vẽ thật gồm: rút ngắn đoạn, dịch dọc cạnh, lệch vạch đầu, lệch đường dóng, ẩn đường dóng; cả năm bị cổng chặn. Cổng đọc tọa độ của nét được vẽ, kiểm toàn bộ véc-tơ cạnh, phương dịch, tâm vạch đầu và vị trí đường dóng; không chỉ kiểm dữ liệu tính trung gian.

Đã xem lại sáu PNG hiện hành, đối chiếu từng đỉnh/đoạn/nhãn của bốn hình có kích thước. Hai hình không có đoạn đo (quầy và hướng bìa) giữ nguyên byte. Đây là kiểm kỹ thuật ảnh rời, chưa là chủ trì nghiệm thu, kiểm trang web hoặc PDF. Chứng cứ lần kiểm ảnh cũ giữ nguyên như lịch sử; kết luận riêng về đường kích thước được thay bằng lần hiệu chỉnh này.

[Báo cáo sửa lỗi và bảo toàn](../../../../../../../../_audit/r1_g05_dimensions_20261020/report.md).

## Hiệu chỉnh mui và cột quầy ngày 20/10/2026

Theo phản hồi tiếp theo của chủ trì, đã sửa riêng cảnh `quay_ban_hang`. Tọa độ cũ dùng hai hướng phối cảnh khác nhau cho bàn và mui; điểm đầu cột đặt độc lập. Ngoài ra, thứ tự lớp mặc định của Matplotlib đặt nét cột trên mặt mui, làm cột xuyên mui dù đã gọi vẽ mui sau.

Nguồn mới dùng một phép chiếu cho bàn, mui và cột. Hai chân cột neo trên mặt bàn, hai đầu cột neo ở mặt dưới mui. Mui là khối mỏng có mặt trên, viền trước và viền bên chung các đỉnh; các mặt mui được vẽ ở lớp trên cột để che đúng phần đầu cột. Đế bắt cột nằm cùng mặt phẳng bàn. Giữ số hộp minh họa, thẻ giá, chú thích và nội dung học liệu.

Cổng đọc tọa độ nét cột và đa giác mui thật, kiểm nối chân/đầu cột, viền trước/bên, chiều dày, hướng phối cảnh và thứ tự lớp. Năm ca âm (chân treo, đầu cột hở, sai phối cảnh mui, hở viền bên, cột vẽ đè mui) đều bị chặn. Đã xem trực tiếp PNG hiện hành. Mười SVG/PNG của năm cảnh còn lại giữ nguyên byte, gồm bốn hình kích thước đã được chủ trì duyệt và hướng bìa. Việc kiểm này không thay chủ trì duyệt riêng hình quầy mới.

Cơ chế dùng lại được cho cảnh quầy hộp có mui phẳng và cột thẳng trong bộ dựng bản thảo; không tự hỗ trợ mái cong, mái nghiêng hoặc mọi vật thể. Nguồn vẫn ở gói, không thay bộ công cụ hình học dùng chung.

[Báo cáo sửa mui và cột quầy](../../../../../../../../_audit/r1_g05_kiosk_20261020/report.md).
