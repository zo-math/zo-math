# D0 — Hồ sơ hoàn tất biên soạn v1.0

- Dự án: ZO Math — Ôn thi Toán THPT, ấn bản 2027.
- Căn cứ điều hành: Kế hoạch 0.5, đặc biệt 11.1 và D.18; không sửa kế hoạch.
- Ngày biên soạn và kiểm tính toán: 09/09/2026.
- Ngày hoàn tất kiểm tra thành phẩm và đóng gói: 10/09/2026.
- Trạng thái: **đã đóng gói để người chủ trì xem/duyệt thành phẩm**.
- Phạm vi đã thực hiện: ma trận, 24 nhiệm vụ khảo sát, 24 câu dự phòng, lời giải, tiêu chí và chỉ dẫn phân tích, hồ sơ phản hồi, PDF và nguồn chỉnh sửa.
- Người/công cụ thực hiện: ChatGPT hỗ trợ ZO Math biên soạn và tự kiểm; Python, SymPy, Fraction kiểm tính toán; Matplotlib dựng hình từ tọa độ; Pandoc/XeLaTeX dàn trang; PyMuPDF kết xuất ảnh để trợ lý xem.
- Chưa có xác nhận người chủ trì đã tự giải/duyệt; không ghi Human Review PASS.
- Chưa có dữ liệu học sinh; hồ sơ chưa được điền bằng kết quả giả lập.
- Website/URL: chưa xuất bản. “Xuất bản tài liệu” trong lần giao này là xuất bộ tệp hoàn chỉnh; chưa triển khai vào repo ZO Math.

## 1. Danh sách thành phẩm

| Tệp | Công dụng | Quy mô |
|---|---|---|
| `2027_D0_hoc_sinh_v1.0.pdf` | Khai báo phạm vi và ngân hàng 24 nhiệm vụ | 10 trang; mỗi mạch một trang |
| `2027_D0_loi_giai_v1.0.pdf` | Lời giải, tiêu chí, lỗi, nơi ôn; đáp án và lời giải câu thử lại | 17 trang |
| `2027_D0_huong_dan_phan_tich_v1.0.pdf` | Chọn câu, đọc kết quả, hai ưu tiên, hồ sơ điền thực tế | 7 trang |
| `2027_D0_thu_lai_v1.0.pdf` | 24 câu dự phòng, chỉ giao câu cần dùng | 9 trang |
| Bốn tệp `.md` cùng tên | Bản nội dung để đọc, sửa và tái xuất | Cùng phiên bản nội dung 1.0 |
| `D0_ngan_hang_v1.0.json` | Dữ liệu có cấu trúc: đề, lời giải, nguồn, tiêu chí, lịch sử, họ câu | 24 bản ghi chính, mỗi bản kèm một SL |
| `D0_ma_tran_va_ho_so_cau_v1.0.md` | Ma trận tám mạch và hồ sơ đầy đủ từng mã | Có CT, bài/trang in và PDF SGK |
| `kiem_chung/` | Mã kiểm toán và kết quả ghi lại | 48 nhiệm vụ có phép kiểm tương ứng |
| `src/` | Mã biên soạn, dàn trang, hình và kiểu chữ | Dùng tái tạo bộ tài liệu |
| `MANIFEST_SHA256.txt` | Dấu kiểm toàn vẹn tệp trong gói | Không tính chính tệp manifest |

## 2. Kiểm đặc tả 11.1 / D.18

| Yêu cầu | Bằng chứng thực hiện |
|---|---|
| Tám mạch, 3 nhiệm vụ/mạch | 24 mã D0-R1-01 đến D0-R8-03; kiểm đếm tự động |
| Nhận diện, thực hiện, giải thích/phối hợp | Vị trí 01/02/03 trong mỗi mạch; lý do tư duy ghi trong ma trận |
| Chọn theo phần đã học, N lồng vào | Mỗi câu có điều kiện học trước; bảng khai báo; N trong hồ sơ câu |
| Chưa học khác làm sai | Mã CH riêng; phạm vi hỗn hợp trong một mạch được giữ; CH không tính sai |
| Tự soạn, tự giải, không nạp lời giải thứ sinh | Đề mới từ phạm vi CT/SGK; lời giải ZO Math; không dùng bảng đáp án ngoài |
| Điều kiện, hình, dữ liệu, lời giải | Kiểm miền, biên, số nguyên, bảng số liệu, phương án/ý; hình dựng từ tọa độ |
| Họ câu, lịch sử đã gặp | Mỗi mã có họ riêng; SL cùng họ; chưa biết lịch sử cá nhân nên hỏi trước khi giao |
| Bản học sinh/lời giải/hồ sơ | Bốn PDF và Markdown kèm theo |
| Tối đa hai ưu tiên và nơi ôn | Hướng dẫn mục 5–7; từng câu có đoạn SGK, hàng lộ trình và câu SL |
| Thiếu bằng chứng phải có cách thử thêm | 24 SL dự phòng; hướng dẫn không coi đổi số là bằng chứng chuyển giao toàn mạch |
| Không dự báo điểm thi/không giả dữ liệu | Ghi rõ trong hướng dẫn và phiếu; không có bảng xếp loại theo điểm D0 |
| Chưa chuyển sang R1-G01 | Chỉ định vị gói tiếp theo trong hướng dẫn, chưa sản xuất gói ấy |

## 3. Phạm vi kiểm toán và kết quả

Tất cả 24 đề chính và 24 đề thử lại đã được giải từ dữ kiện đã soạn. Lời giải viết rõ điều kiện áp dụng, cách xác định đầy đủ nghiệm/các trường hợp và đáp số. Bằng chứng kiểm bổ sung ghi ở ma trận và `kiem_chung/ket_qua_tinh_toan.md`.

- Hàm số: giao điều kiện của căn và mẫu; thế biên; đạo hàm và tiếp điểm; bảng dấu khả thi và việc đổi/không đổi dấu.
- Thống kê: tổng tần số, trung điểm, trung vị, tính chính xác có trọng số; hai công thức phương sai; giữ tính ước lượng và giới hạn kết luận.
- Hình học: bội vectơ ở cả tọa độ, không chia 0; hình chiếu lên mặt phẳng; hai cách tính góc cho cùng kết quả.
- Xác suất: vét cạn bốn kết quả đồng xu, sáu mặt xúc xắc; tất cả 21/28 cặp bi; mẫu số điều kiện từ bảng.
- Dãy số/lôgarit: hiệu, tỉ số tổng quát; nghiệm đại số và đối số dương; mốc trước/sau ngưỡng nguyên.
- Lượng giác: đổi đơn vị, dấu, thế từng nghiệm; kiểm đầy đủ k theo khoảng; chu kì và thời điểm đầu.
- Nguyên hàm/tích phân: đạo hàm kiểm ngược, điều kiện đầu, tích phân có dấu/trị tuyệt đối; diện tích hai tam giác vận tốc.
- Tối ưu: kiểm mô hình ba cạnh, cước theo d−1; vét cạn đủ các cặp nguyên. Bài gốc có 17 cặp khả thi, bài thử lại có 13; nghiệm tối ưu duy nhất khớp bảng rút gọn.

**Kết quả:** 48/48 nhiệm vụ qua những phép kiểm tính toán được khai báo. Đây không phải chứng nhận tự động mọi khía cạnh sư phạm; kiểm số không thay lập luận tổng quát. Không dùng việc hai AI cùng trả lời làm chứng minh.

## 4. Kiểm tra thành phẩm

- Bốn PDF mở được, tổng 43 trang; đối chiếu mã chính/SL với dữ liệu gốc và Markdown.
- Đã kết xuất và xem toàn bộ 43 trang qua ảnh tổng quan; xem riêng ở kích thước lớn các trang hình hộp, công thức lượng giác dài và hai phiếu ghi kết quả.
- Không thấy cắt chữ, đè công thức, mất ký tự hoặc bảng tràn lề trong các ảnh đã xem; nhật ký XeLaTeX không còn báo tràn dòng hoặc thiếu ký tự.
- Bản học sinh giữ ba nhiệm vụ của mỗi mạch trên cùng một trang. Bản lời giải chủ động tách nhiệm vụ phối hợp để không đứt lời giải giữa trang.
- Hình hộp đã đổi góc chiếu để đường chéo không đi sát các nhãn đỉnh không liên quan; nhãn cạnh và dữ kiện khớp đề.
- Phiếu ghi kết quả có dòng chấm để dùng khi in; hồ sơ Markdown vẫn chỉnh sửa được.
- Bản học sinh và bản thử lại không chứa các trường lời giải/đáp án của ngân hàng. Lời giải thử lại được giữ trong bản người hướng dẫn.

## 5. Các chỉnh sửa trong quá trình hoàn thiện

1. Sửa cách lưu chuỗi công thức trong mã nguồn để dấu gạch chéo không bị hiểu thành ký tự điều khiển; tạo lại JSON/Markdown từ bản đã sửa.
2. Tăng cỡ chữ, sửa ngắt trang lời giải, điều chỉnh độ rộng bảng hướng dẫn và thêm dòng chấm vào các phiếu.
3. Tách danh sách nghiệm lượng giác dài thành các cụm có thể xuống dòng; không thay nghiệm.
4. Làm rõ câu lấy số kì nguyên: lấy số nguyên nhỏ nhất không dưới ngưỡng, không bỏ phần thập phân.
5. Chỉnh hình chiếu minh họa để tránh đường chéo gần trùng các đỉnh khác. Không thay hình không gian hoặc đáp số.

Các sửa này diễn ra trước khi giao bản v1.0 đầu tiên, không thay quyết định của Kế hoạch 0.5. Không còn lỗi toán hoặc lỗi trình bày đã biết chặn việc giao bộ tệp này.

## 6. Điểm tiếp tục

**Một việc tiếp theo:** người chủ trì xem và tự giải bản học sinh D0 v1.0, đối chiếu bản lời giải và cách diễn giải kết quả, đúng vai trò tại mục 11.1. Sau khi chọn học sinh dùng thử, khai báo phần đã học rồi chỉ giao các mã phù hợp; không cần làm cả ngân hàng.

Khi có bài làm, ghi dữ liệu thật vào hồ sơ; chọn tối đa hai ưu tiên và câu thử lại. Nếu chưa đủ bằng chứng, soạn thêm cụm theo mục tiêu thực sự vướng. Không tự xác nhận giảm luyện/chuyển chặng từ ba nhiệm vụ hoặc một câu đổi số.

R1-G01 là công việc sản xuất kế tiếp theo kế hoạch, nhưng chưa thuộc phần triển khai D0 vừa hoàn tất. Khi cần công bố website, phải làm trong repo theo quy trình hiện hành; chưa có URL để báo đã xuất bản.

## 7. Tái tạo và cập nhật

Yêu cầu công cụ: Python 3 với SymPy, Matplotlib, PyMuPDF; Pandoc; XeLaTeX; DejaVu Serif/Sans, Latin Modern Math. Không cần mạng để xem các PDF đã xuất. Các sách nguồn không được sao chép vào gói này.

Chạy từ thư mục gói:

```bash
python src/bien_soan.py
python kiem_chung/kiem_tra_toan.py
python src/dong_goi.py
python src/xuat_pdf.py
```

Đề, lời giải và hồ sơ câu nằm trong `src/bien_soan.py`, từ đó tạo JSON rồi các bản Markdown. Hướng dẫn phân tích là Markdown riêng. Khi đổi dữ kiện, cập nhật kiểm toán, tạo lại toàn bộ bản liên quan, xem lại PDF và tăng phiên bản theo quy tắc 10.5 của kế hoạch. Không sửa một đáp án trong PDF rời mà bỏ quên bản gốc.
