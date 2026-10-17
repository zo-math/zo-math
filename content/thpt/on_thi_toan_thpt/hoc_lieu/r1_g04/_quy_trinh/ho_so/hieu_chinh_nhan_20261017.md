# R1-G04 — Kiểm kê và sửa nhãn theo cấp chứa

Chỉ thị chủ trì ngày 17/10/2026: Bài học có nhãn MẠCH HỌC CHÍNH; Khởi động có MẠCH HỌC CHÍNH · BÀI HỌC. Đã kiểm kê toàn bộ nhãn G04 và đối chứng G01–G03; sản phẩm sửa trong lượt này là G04.

Nguyên nhân: nhãn đầu phần ở profile, nhãn chức năng trong binding và chuỗi riêng của adapter cùng ghi vào một dòng .role. Chúng không có cùng quy tắc cấp chứa và dùng lẫn hai dấu chấm. Đã bỏ chuỗi riêng G04, đưa giá trị cấp cha về danh mục kiến trúc và một hàm gán/kiểm dùng chung. Giá trị hiển thị cũ trong binding G04 đã được thay; chức năng, số và cặp ID giữ nguyên.

Quy tắc tái sử dụng tại quy chuẩn 07/6.2; danh mục label_contract.display_contract.context_labels là nguồn giá trị. Binding G04 chọn parent-context-v1. Loại/chức năng vẫn ở metadata và tiêu đề, không thay dòng ngữ cảnh. Kiểu chữ/cỡ/màu/trục dùng .role hiện có; dấu phân cách duy nhất là U+00B7 với khoảng trắng hai bên.

Trước sửa có 79 nhãn/21 cách ghi. Sau sửa có 121 nhãn: bổ sung ngữ cảnh cho các tiêu đề trước đây chưa có, không tạo mục hoặc dãy số mới. Bảng dưới ghi đầy đủ owner/tiêu đề/trước–sau, bao gồm cả lời giải.

G01–G03 chỉ được kiểm kê/hồi quy, chưa di trú hoặc thay bản đã phát hành. Nhãn cũ của chúng giữ tương thích nhưng không được dùng làm mẫu gán nhãn mới. Không sửa QMD, nội dung toán, hình, PDF hoặc danh mục công khai.

| Owner | Tiêu đề | Nhãn trước | Nhãn sau |
|---|---|---|---|
| bat-dau | Bắt đầu | Bắt đầu học | MẠCH HỌC CHÍNH |
| mục-tiêu | Mục tiêu | Chưa có nhãn | MẠCH HỌC CHÍNH · BẮT ĐẦU |
| tiên-quyết | Tiên quyết | Chưa có nhãn | MẠCH HỌC CHÍNH · BẮT ĐẦU |
| cách-học-và-chọn-nơi-bắt-đầu | Cách học và chọn nơi bắt đầu | Chưa có nhãn | MẠCH HỌC CHÍNH · BẮT ĐẦU |
| bản-đồ-học-và-hỗ-trợ | Bản đồ học và hỗ trợ | Chưa có nhãn | MẠCH HỌC CHÍNH · BẮT ĐẦU |
| khi-nào-hoàn-tất-lượt-chính | Khi nào hoàn tất lượt chính? | Chưa có nhãn | MẠCH HỌC CHÍNH · BẮT ĐẦU |
| bai-hoc | Bài học | Mạch học chính | MẠCH HỌC CHÍNH |
| khoi-dong | Khởi động | Bài học · Khởi động | MẠCH HỌC CHÍNH · BÀI HỌC |
| KD01 | Nhiệm vụ 01 — Miền trước và sau rút gọn | BÀI HỌC • KHỞI ĐỘNG | MẠCH HỌC CHÍNH · BÀI HỌC · KHỞI ĐỘNG |
| KD02 | Nhiệm vụ 02 — Đạo hàm và dấu | BÀI HỌC • KHỞI ĐỘNG | MẠCH HỌC CHÍNH · BÀI HỌC · KHỞI ĐỘNG |
| KD03 | Nhiệm vụ 03 — Giới hạn có hướng | BÀI HỌC • KHỞI ĐỘNG | MẠCH HỌC CHÍNH · BÀI HỌC · KHỞI ĐỘNG |
| KD04 | Nhiệm vụ 04 — Thương và phần dư | BÀI HỌC • KHỞI ĐỘNG | MẠCH HỌC CHÍNH · BÀI HỌC · KHỞI ĐỘNG |
| CP-KD | Sau khi làm xong | BÀI HỌC • KHỞI ĐỘNG | MẠCH HỌC CHÍNH · BÀI HỌC · KHỞI ĐỘNG |
| bh-01 | 1. Từ dữ kiện đến sơ đồ khảo sát | Chưa có nhãn | MẠCH HỌC CHÍNH · BÀI HỌC |
| GM01 | Gợi mở 01 | BÀI HỌC • GỢI MỞ | MẠCH HỌC CHÍNH · BÀI HỌC |
| kt-01 | 1.1. Phương pháp — Sơ đồ khảo sát | Chưa có nhãn | MẠCH HỌC CHÍNH · BÀI HỌC |
| VD01 | 1.2. Ví dụ 01 — Cùng dấu đạo hàm, khác vị trí | Chưa có nhãn | MẠCH HỌC CHÍNH · BÀI HỌC |
| T01 | 1.3. Tự kiểm tra 01 — Tìm mâu thuẫn trước khi nối nét | BÀI HỌC • TỰ KIỂM TRA | MẠCH HỌC CHÍNH · BÀI HỌC |
| bh-02 | 2. Khảo sát và vẽ đồ thị hàm số bậc ba | Chưa có nhãn | MẠCH HỌC CHÍNH · BÀI HỌC |
| GM02 | Gợi mở 02 | BÀI HỌC • GỢI MỞ | MẠCH HỌC CHÍNH · BÀI HỌC |
| kt-02 | 2.1. Những thông tin cần giữ | Giải thích | MẠCH HỌC CHÍNH · BÀI HỌC |
| VD02 | 2.2. Ví dụ 02 — Hai cực trị và một nghiệm kép của hàm | Chưa có nhãn | MẠCH HỌC CHÍNH · BÀI HỌC |
| VD03 | 2.3. Ví dụ 03 — Đạo hàm bằng không mà không có cực trị | Chưa có nhãn | MẠCH HỌC CHÍNH · BÀI HỌC |
| T02 | 2.4. Tự kiểm tra 02 — Một điểm dừng không đổi chiều | BÀI HỌC • TỰ KIỂM TRA | MẠCH HỌC CHÍNH · BÀI HỌC |
| bh-03 | 3. Khảo sát hàm phân thức bậc nhất trên bậc nhất | Chưa có nhãn | MẠCH HỌC CHÍNH · BÀI HỌC |
| GM03 | Gợi mở 03 | BÀI HỌC • GỢI MỞ | MẠCH HỌC CHÍNH · BÀI HỌC |
| kt-03 | 3.1. Từ công thức đến hai nhánh | Giải thích | MẠCH HỌC CHÍNH · BÀI HỌC |
| VD04 | 3.2. Ví dụ 04 — Ghép biến thiên với tiệm cận ngang | Chưa có nhãn | MẠCH HỌC CHÍNH · BÀI HỌC |
| T03 | 3.3. Tự kiểm tra 03 — Hai nhánh đồng biến | BÀI HỌC • TỰ KIỂM TRA | MẠCH HỌC CHÍNH · BÀI HỌC |
| bh-04 | 4. Khảo sát hàm phân thức bậc hai trên bậc nhất | Chưa có nhãn | MẠCH HỌC CHÍNH · BÀI HỌC |
| GM04 | Gợi mở 04 | BÀI HỌC • GỢI MỞ | MẠCH HỌC CHÍNH · BÀI HỌC |
| kt-04 | 4.1. Phần thương, phần dư và đối xứng | Giải thích | MẠCH HỌC CHÍNH · BÀI HỌC |
| VD05 | 4.2. Ví dụ 05 — Tiệm cận xiên và hai cực trị | Chưa có nhãn | MẠCH HỌC CHÍNH · BÀI HỌC |
| VD06 | 4.3. Ví dụ 06 — Cùng tiệm cận, không có cực trị | Chưa có nhãn | MẠCH HỌC CHÍNH · BÀI HỌC |
| T04 | 4.4. Tự kiểm tra 04 — Kiểm lại dấu của phần dư | BÀI HỌC • TỰ KIỂM TRA | MẠCH HỌC CHÍNH · BÀI HỌC |
| bh-05 | 5. Đọc và sử dụng kết quả khảo sát đúng miền | Chưa có nhãn | MẠCH HỌC CHÍNH · BÀI HỌC |
| GM05 | Gợi mở 05 | BÀI HỌC • GỢI MỞ | MẠCH HỌC CHÍNH · BÀI HỌC |
| kt-05 | 5.1. Ba câu hỏi trước khi diễn giải | Giải thích | MẠCH HỌC CHÍNH · BÀI HỌC |
| VD07 | 5.2. Ví dụ 07 — Chi phí trung bình có cận nhưng không có giá trị nhỏ nhất | Chưa có nhãn | MẠCH HỌC CHÍNH · BÀI HỌC |
| T05 | 5.3. Tự kiểm tra 05 — Giữ miền khi đọc chi phí | BÀI HỌC • TỰ KIỂM TRA | MẠCH HỌC CHÍNH · BÀI HỌC |
| khep-lai | Khép lại bài học | Chưa có nhãn | MẠCH HỌC CHÍNH · BÀI HỌC |
| phieu-luyen | Luyện tập | Tự luyện | MẠCH HỌC CHÍNH |
| chang-1 | Chặng 1 — Bậc ba và phân thức bậc nhất | Chưa có nhãn | MẠCH HỌC CHÍNH · LUYỆN TẬP |
| L01 | Nhiệm vụ 01 — Khảo sát một hàm bậc ba | LUYỆN TẬP • CHẶNG 1 | MẠCH HỌC CHÍNH · LUYỆN TẬP · CHẶNG 1 |
| L02 | Nhiệm vụ 02 — Không có cực trị theo hai cách | LUYỆN TẬP • CHẶNG 1 | MẠCH HỌC CHÍNH · LUYỆN TẬP · CHẶNG 1 |
| L03 | Nhiệm vụ 03 — Khảo sát phân thức với hai nhánh tăng | LUYỆN TẬP • CHẶNG 1 | MẠCH HỌC CHÍNH · LUYỆN TẬP · CHẶNG 1 |
| CP01 | Điểm dừng 01 — Đối chiếu chặng đầu | LUYỆN TẬP • CHẶNG 1 | MẠCH HỌC CHÍNH · LUYỆN TẬP · CHẶNG 1 |
| chang-2 | Chặng 2 — Tiệm cận xiên và miền mô hình | Chưa có nhãn | MẠCH HỌC CHÍNH · LUYỆN TẬP |
| L04 | Nhiệm vụ 04 — Khảo sát phân thức có tiệm cận xiên | LUYỆN TẬP • CHẶNG 2 | MẠCH HỌC CHÍNH · LUYỆN TẬP · CHẶNG 2 |
| L05 | Nhiệm vụ 05 — Dấu trừ làm thay đổi hai nhánh | LUYỆN TẬP • CHẶNG 2 | MẠCH HỌC CHÍNH · LUYỆN TẬP · CHẶNG 2 |
| L06 | Nhiệm vụ 06 — Đồ thị chỉ trên miền sản xuất | LUYỆN TẬP • CHẶNG 2 | MẠCH HỌC CHÍNH · LUYỆN TẬP · CHẶNG 2 |
| CP02 | Điểm dừng 02 — Đối chiếu khảo sát và diễn giải | LUYỆN TẬP • CHẶNG 2 | MẠCH HỌC CHÍNH · LUYỆN TẬP · CHẶNG 2 |
| tu-kiem-tra | Kiểm tra | Chưa có nhãn | MẠCH HỌC CHÍNH |
| K01 | Nhiệm vụ 01 — Khảo sát hàm bậc ba | KIỂM TRA | MẠCH HỌC CHÍNH · KIỂM TRA |
| K02 | Nhiệm vụ 02 — Khảo sát phân thức bậc nhất | KIỂM TRA | MẠCH HỌC CHÍNH · KIỂM TRA |
| K03 | Nhiệm vụ 03 — Khảo sát phân thức bậc hai | KIỂM TRA | MẠCH HỌC CHÍNH · KIỂM TRA |
| K04 | Nhiệm vụ 04 — Kết luận trong miền của mô hình | KIỂM TRA | MẠCH HỌC CHÍNH · KIỂM TRA |
| CPK | Kết thúc lượt và đối chiếu kết quả | KIỂM TRA • KẾT QUẢ | MẠCH HỌC CHÍNH · KIỂM TRA |
| on-lai | Ôn lại | Ôn sau khoảng trễ | MẠCH HỌC CHÍNH |
| on-luot-1 | Lượt 1 — Sau khoảng 2 2 – 3 3 ngày | Chưa có nhãn | MẠCH HỌC CHÍNH · ÔN LẠI |
| O01 | Nhiệm vụ 01 — Nhớ lại khảo sát bậc ba | ÔN LẠI • LƯỢT 1 | MẠCH HỌC CHÍNH · ÔN LẠI · LƯỢT 1 |
| CP-O01 | Điểm dừng lượt 1 | ÔN LẠI • LƯỢT 1 | MẠCH HỌC CHÍNH · ÔN LẠI · LƯỢT 1 |
| on-luot-2 | Lượt 2 — Sau khoảng 7 7 ngày | Chưa có nhãn | MẠCH HỌC CHÍNH · ÔN LẠI |
| O02 | Nhiệm vụ 02 — Nhớ lại phân thức và miền mô hình | ÔN LẠI • LƯỢT 2 | MẠCH HỌC CHÍNH · ÔN LẠI · LƯỢT 2 |
| CP-O02 | Điểm dừng lượt 2 | ÔN LẠI • LƯỢT 2 | MẠCH HỌC CHÍNH · ÔN LẠI · LƯỢT 2 |
| on-luot-3 | Lượt 3 — Sau khoảng 3 3 – 4 4 tuần | Chưa có nhãn | MẠCH HỌC CHÍNH · ÔN LẠI |
| O03 | Nhiệm vụ 03 — Nhớ lại tiệm cận xiên và cực trị | ÔN LẠI • LƯỢT 3 | MẠCH HỌC CHÍNH · ÔN LẠI · LƯỢT 3 |
| CP-O03 | Điểm dừng lượt 3 | ÔN LẠI • LƯỢT 3 | MẠCH HỌC CHÍNH · ÔN LẠI · LƯỢT 3 |
| on-nen | Ôn nền | Chưa có nhãn | HỖ TRỢ KHI CẦN |
| sua-loi | Sửa lỗi | Hỗ trợ khi cần | HỖ TRỢ KHI CẦN |
| chon-sua-loi | Chọn đúng ý và nơi quay về | Chưa có nhãn | HỖ TRỢ KHI CẦN · SỬA LỖI |
| het-bai-moi | Khi câu phù hợp đã lộ hoặc vẫn chưa đúng | Chưa có nhãn | HỖ TRỢ KHI CẦN · SỬA LỖI |
| S01 | Sau Luyện tập hoặc Tự kiểm tra | Chưa có nhãn | HỖ TRỢ KHI CẦN · SỬA LỖI |
| S01 | Nhiệm vụ 01 — Sau luyện tập — Bậc ba | SỬA LỖI • SAU LUYỆN TẬP | HỖ TRỢ KHI CẦN · SỬA LỖI · SAU LUYỆN TẬP |
| S02 | Nhiệm vụ 02 — Sau luyện tập — Phân thức và miền | SỬA LỖI • SAU LUYỆN TẬP | HỖ TRỢ KHI CẦN · SỬA LỖI · SAU LUYỆN TẬP |
| S03 | Sau Kiểm tra | Chưa có nhãn | HỖ TRỢ KHI CẦN · SỬA LỖI |
| S03 | Nhiệm vụ 03 — Sau kiểm tra — Bậc ba | SỬA LỖI • SAU KIỂM TRA | HỖ TRỢ KHI CẦN · SỬA LỖI · SAU KIỂM TRA |
| S04 | Nhiệm vụ 04 — Sau kiểm tra — Phân thức và miền | SỬA LỖI • SAU KIỂM TRA | HỖ TRỢ KHI CẦN · SỬA LỖI · SAU KIỂM TRA |
| S05 | Sau Ôn lại | Chưa có nhãn | HỖ TRỢ KHI CẦN · SỬA LỖI |
| S05 | Nhiệm vụ 05 — Sau ôn lại — Bậc ba | SỬA LỖI • SAU ÔN LẠI | HỖ TRỢ KHI CẦN · SỬA LỖI · SAU ÔN LẠI |
| S06 | Nhiệm vụ 06 — Sau ôn lại — Phân thức và miền | SỬA LỖI • SAU ÔN LẠI | HỖ TRỢ KHI CẦN · SỬA LỖI · SAU ÔN LẠI |
| nhat-ky | Nhật kí | Chưa có nhãn | HỖ TRỢ KHI CẦN |
| loi-giai | Lời giải | Chưa có nhãn | HỖ TRỢ KHI CẦN |
| lg-KD01 | Khởi động | Chưa có nhãn | HỖ TRỢ KHI CẦN · LỜI GIẢI |
| lg-KD01 | Nhiệm vụ 01 — Miền trước và sau rút gọn | BÀI HỌC • KHỞI ĐỘNG | HỖ TRỢ KHI CẦN · LỜI GIẢI · BÀI HỌC · KHỞI ĐỘNG |
| lg-KD02 | Nhiệm vụ 02 — Đạo hàm và dấu | BÀI HỌC • KHỞI ĐỘNG | HỖ TRỢ KHI CẦN · LỜI GIẢI · BÀI HỌC · KHỞI ĐỘNG |
| lg-KD03 | Nhiệm vụ 03 — Giới hạn có hướng | BÀI HỌC • KHỞI ĐỘNG | HỖ TRỢ KHI CẦN · LỜI GIẢI · BÀI HỌC · KHỞI ĐỘNG |
| lg-KD04 | Nhiệm vụ 04 — Thương và phần dư | BÀI HỌC • KHỞI ĐỘNG | HỖ TRỢ KHI CẦN · LỜI GIẢI · BÀI HỌC · KHỞI ĐỘNG |
| lg-T01 | Tự kiểm tra | Chưa có nhãn | HỖ TRỢ KHI CẦN · LỜI GIẢI |
| lg-T01 | Tự kiểm tra 01 — Tìm mâu thuẫn trước khi nối nét | BÀI HỌC • TỰ KIỂM TRA | HỖ TRỢ KHI CẦN · LỜI GIẢI · BÀI HỌC · TỰ KIỂM TRA |
| lg-T02 | Tự kiểm tra 02 — Một điểm dừng không đổi chiều | BÀI HỌC • TỰ KIỂM TRA | HỖ TRỢ KHI CẦN · LỜI GIẢI · BÀI HỌC · TỰ KIỂM TRA |
| lg-T03 | Tự kiểm tra 03 — Hai nhánh đồng biến | BÀI HỌC • TỰ KIỂM TRA | HỖ TRỢ KHI CẦN · LỜI GIẢI · BÀI HỌC · TỰ KIỂM TRA |
| lg-T04 | Tự kiểm tra 04 — Kiểm lại dấu của phần dư | BÀI HỌC • TỰ KIỂM TRA | HỖ TRỢ KHI CẦN · LỜI GIẢI · BÀI HỌC · TỰ KIỂM TRA |
| lg-T05 | Tự kiểm tra 05 — Giữ miền khi đọc chi phí | BÀI HỌC • TỰ KIỂM TRA | HỖ TRỢ KHI CẦN · LỜI GIẢI · BÀI HỌC · TỰ KIỂM TRA |
| lg-L01 | Luyện tập | Chưa có nhãn | HỖ TRỢ KHI CẦN · LỜI GIẢI |
| lg-L01 | Nhiệm vụ 01 — Khảo sát một hàm bậc ba | LUYỆN TẬP • CHẶNG 1 | HỖ TRỢ KHI CẦN · LỜI GIẢI · LUYỆN TẬP · CHẶNG 1 |
| lg-L02 | Nhiệm vụ 02 — Không có cực trị theo hai cách | LUYỆN TẬP • CHẶNG 1 | HỖ TRỢ KHI CẦN · LỜI GIẢI · LUYỆN TẬP · CHẶNG 1 |
| lg-L03 | Nhiệm vụ 03 — Khảo sát phân thức với hai nhánh tăng | LUYỆN TẬP • CHẶNG 1 | HỖ TRỢ KHI CẦN · LỜI GIẢI · LUYỆN TẬP · CHẶNG 1 |
| lg-L04 | Nhiệm vụ 04 — Khảo sát phân thức có tiệm cận xiên | LUYỆN TẬP • CHẶNG 2 | HỖ TRỢ KHI CẦN · LỜI GIẢI · LUYỆN TẬP · CHẶNG 2 |
| lg-L05 | Nhiệm vụ 05 — Dấu trừ làm thay đổi hai nhánh | LUYỆN TẬP • CHẶNG 2 | HỖ TRỢ KHI CẦN · LỜI GIẢI · LUYỆN TẬP · CHẶNG 2 |
| lg-L06 | Nhiệm vụ 06 — Đồ thị chỉ trên miền sản xuất | LUYỆN TẬP • CHẶNG 2 | HỖ TRỢ KHI CẦN · LỜI GIẢI · LUYỆN TẬP · CHẶNG 2 |
| lg-K01 | Kiểm tra | Chưa có nhãn | HỖ TRỢ KHI CẦN · LỜI GIẢI |
| lg-K01 | Nhiệm vụ 01 — Khảo sát hàm bậc ba | KIỂM TRA | HỖ TRỢ KHI CẦN · LỜI GIẢI · KIỂM TRA |
| lg-K02 | Nhiệm vụ 02 — Khảo sát phân thức bậc nhất | KIỂM TRA | HỖ TRỢ KHI CẦN · LỜI GIẢI · KIỂM TRA |
| lg-K03 | Nhiệm vụ 03 — Khảo sát phân thức bậc hai | KIỂM TRA | HỖ TRỢ KHI CẦN · LỜI GIẢI · KIỂM TRA |
| lg-K04 | Nhiệm vụ 04 — Kết luận trong miền của mô hình | KIỂM TRA | HỖ TRỢ KHI CẦN · LỜI GIẢI · KIỂM TRA |
| lg-O01 | Ôn lại | Chưa có nhãn | HỖ TRỢ KHI CẦN · LỜI GIẢI |
| lg-O01 | Nhiệm vụ 01 — Nhớ lại khảo sát bậc ba | ÔN LẠI • LƯỢT 1 | HỖ TRỢ KHI CẦN · LỜI GIẢI · ÔN LẠI · LƯỢT 1 |
| lg-O02 | Nhiệm vụ 02 — Nhớ lại phân thức và miền mô hình | ÔN LẠI • LƯỢT 2 | HỖ TRỢ KHI CẦN · LỜI GIẢI · ÔN LẠI · LƯỢT 2 |
| lg-O03 | Nhiệm vụ 03 — Nhớ lại tiệm cận xiên và cực trị | ÔN LẠI • LƯỢT 3 | HỖ TRỢ KHI CẦN · LỜI GIẢI · ÔN LẠI · LƯỢT 3 |
| lg-sua-loi | Sửa lỗi | Chưa có nhãn | HỖ TRỢ KHI CẦN · LỜI GIẢI |
| lg-S01 | Sau Luyện tập hoặc Tự kiểm tra | Chưa có nhãn | HỖ TRỢ KHI CẦN · LỜI GIẢI |
| lg-S01 | Nhiệm vụ 01 — Sau luyện tập — Bậc ba | SỬA LỖI • SAU LUYỆN TẬP | HỖ TRỢ KHI CẦN · LỜI GIẢI · SỬA LỖI · SAU LUYỆN TẬP |
| lg-S02 | Nhiệm vụ 02 — Sau luyện tập — Phân thức và miền | SỬA LỖI • SAU LUYỆN TẬP | HỖ TRỢ KHI CẦN · LỜI GIẢI · SỬA LỖI · SAU LUYỆN TẬP |
| lg-S03 | Sau Kiểm tra | Chưa có nhãn | HỖ TRỢ KHI CẦN · LỜI GIẢI |
| lg-S03 | Nhiệm vụ 03 — Sau kiểm tra — Bậc ba | SỬA LỖI • SAU KIỂM TRA | HỖ TRỢ KHI CẦN · LỜI GIẢI · SỬA LỖI · SAU KIỂM TRA |
| lg-S04 | Nhiệm vụ 04 — Sau kiểm tra — Phân thức và miền | SỬA LỖI • SAU KIỂM TRA | HỖ TRỢ KHI CẦN · LỜI GIẢI · SỬA LỖI · SAU KIỂM TRA |
| lg-S05 | Sau Ôn lại | Chưa có nhãn | HỖ TRỢ KHI CẦN · LỜI GIẢI |
| lg-S05 | Nhiệm vụ 05 — Sau ôn lại — Bậc ba | SỬA LỖI • SAU ÔN LẠI | HỖ TRỢ KHI CẦN · LỜI GIẢI · SỬA LỖI · SAU ÔN LẠI |
| lg-S06 | Nhiệm vụ 06 — Sau ôn lại — Phân thức và miền | SỬA LỖI • SAU ÔN LẠI | HỖ TRỢ KHI CẦN · LỜI GIẢI · SỬA LỖI · SAU ÔN LẠI |
| nguon | Nguồn | Nguồn học liệu | TIỆN ÍCH |

Kết quả kiểm, bản xem và trạng thái hiện hành ở JSON cùng tên và README gói; HTML mới chờ chủ trì xem. Không commit/push hoặc xuất bản.

[Mở HTML đã gán lại nhãn](../../../../../../../_audit/r1_g04_labels_20261017/r1-g04-reading.html). Kiểm HTML 989/989; trình duyệt 138/138 ở 1440/430/390 px; hồi quy G01–G03 và thử lỗi 12/12. Đã xem ảnh thực ở desktop/mobile. Cổng điều hành 177/177, self-test 235/235. 1404 tệp docs cùng Git index không đổi. QMD giữ nguyên hash; không dựng hình/PDF. Chờ chủ trì xem đầu ra, chưa phát hành.
