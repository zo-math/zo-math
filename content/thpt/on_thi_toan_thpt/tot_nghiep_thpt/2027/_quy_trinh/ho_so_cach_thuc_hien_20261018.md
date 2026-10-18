# Rà soát Cách thực hiện — 18/10/2026

Chủ trì giao kiểm tính cần thiết, bỏ phần dư và biên tập hướng dẫn còn cần. Chỉ sửa nguồn, không dựng HTML/PDF.

## Phạm vi và kết quả

Đã tìm toàn bộ QMD hiện hành của chuyên mục, gồm các include dùng chung; không lấy bản thảo/receipt làm nguồn. Trang khóa và Khảo sát đầu vào không có mục mang tên này. Bốn gói có 38 mục: bỏ 24 đoạn lặp; biên tập 14 chỉ dẫn cần thiết thành đoạn nhìn thấy, trước đúng hoạt động. Không còn hộp Cách thực hiện trong bốn gói; hộp trợ giúp tùy chọn vẫn được phép khi có căn cứ theo 07/6.1.5.

| Nguồn | Trước | Bỏ đoạn lặp | Biên tập và cho nhìn thấy |
|---|---:|---:|---:|
| [Đơn điệu và cực trị](../../../hoc_lieu/r1_g01/index.qmd) | 14 | 7 | 7 |
| [Giá trị lớn nhất và giá trị nhỏ nhất](../../../hoc_lieu/r1_g02/index.qmd) | 11 | 6 | 5 |
| [Đường tiệm cận](../../../hoc_lieu/r1_g03/index.qmd) | 7 | 6 | 1 |
| [Khảo sát sự biến thiên và vẽ đồ thị](../../../hoc_lieu/r1_g04/index.qmd) | 6 | 5 | 1 |

## Nguyên nhân và sửa cơ chế

Lỗi viết thường nằm ngay trong QMD G03/G04, không phải do CSS. Mẫu bản thảo có sẵn ô Cách thực hiện ở từng mục; bảng kiểm và câu “sau Cách thực hiện” trong 01/07 khiến ô này dễ được điền như thành phần bắt buộc. Quy tắc mặc định đóng lại bị áp cho cả thao tác cần biết trước hoạt động. Cổng cũ chưa kiểm việc hướng dẫn có cần, có bị ẩn hay có viết hoa.

Đã sửa các phát biểu hoạt động trong 01/07, mẫu bản thảo 1.3 và bảng kiểm 1.6. 07/6.1.5 sở hữu quy tắc; 02 giữ bước đọc đối chiếu và kiểm. Cổng `zo_course_instructions.py` gọi ở kiểm nguồn QMD và kiểm HTML dùng chung; binding chỉ khai ID/vai trò, không sao lời hướng dẫn. Cổng tự động kiểm được khai báo, chữ đầu câu, chỉ dẫn bị ẩn và hộp cũ tái xuất; tính hữu ích cần đọc trong ngữ cảnh, không thể chứng nhận chỉ bằng máy.

G01 đồng bộ bản đồ nguồn và phép đảo giới hạn trên bản sao cây kiểm. Chỉ những nút chỉ dẫn đã kiểm kê được đảo để đối chiếu; lời người học không lấy từ văn bản lịch sử. Giữ nguyên fingerprint và hash nghiệm thu cũ; binding nguồn hiện hành ghi đúng SHA mới.

## Kiểm kê từng mục

Cột nơi kiểm ghi mốc trong nguồn hiện hành. Toàn văn trước/sau và dấu vết từng mục lưu trong [JSON đối chiếu](ho_so_cach_thuc_hien_20261018.json); không là nguồn dựng người học.

| Gói / vị trí | Xử lí | Căn cứ / nơi giữ yêu cầu |
|---|---|---|
| r1_g01 / Khởi động | Biên tập, nhìn thấy | Giữ tại `cach-thuc-hien-bat-dau`; thao tác cụ thể, đầu câu viết hoa. |
| r1_g01 / 1. Đơn điệu nói điều gì? | Bỏ đoạn lặp | Bỏ lộ trình đọc lặp. Gợi mở vẫn yêu cầu thử trả lời trước; phần giảng/ví dụ và Tự kiểm tra của chính mục giữ nội dung và thao tác. Mốc: thử-nghĩ-trước, từ-đi-lên-đến-định-nghĩa, g01-dinh-nghia-dong-bien. |
| r1_g01 / 2. Dấu đạo hàm cho phép kết luận gì? | Bỏ đoạn lặp | Bỏ lộ trình đọc lặp. Gợi mở vẫn yêu cầu thử trả lời trước; phần giảng/ví dụ và Tự kiểm tra của chính mục giữ nội dung và thao tác. Mốc: thử-nghĩ-trước-1, định-lí-và-phạm-vi-áp-dụng, một-số-hữu-hạn-điểm-đạo-hàm-bằng-0. |
| r1_g01 / 3. Một chuỗi biểu diễn được dựng thế nào? | Bỏ đoạn lặp | Bỏ lộ trình đọc lặp. Gợi mở vẫn yêu cầu thử trả lời trước; phần giảng/ví dụ và Tự kiểm tra của chính mục giữ nội dung và thao tác. Mốc: thử-nghĩ-trước-2, ví-dụ-v03-bắt-đầu-từ-công-thức, từ-đạo-hàm-đến-dấu-và-chiều-biến-thiên. |
| r1_g01 / 4. Điều gì xảy ra tại một điểm cần xét? | Bỏ đoạn lặp | Bỏ lộ trình đọc lặp. Gợi mở vẫn yêu cầu thử trả lời trước; phần giảng/ví dụ và Tự kiểm tra của chính mục giữ nội dung và thao tác. Mốc: thử-nghĩ-trước-3, điều-kiện-đủ-qua-dấu-đạo-hàm, r1-table-t05. |
| r1_g01 / 5. Cực trị được gọi tên thế nào? | Bỏ đoạn lặp | Bỏ lộ trình đọc lặp. Gợi mở vẫn yêu cầu thử trả lời trước; phần giảng/ví dụ và Tự kiểm tra của chính mục giữ nội dung và thao tác. Mốc: thử-nghĩ-trước-4, định-nghĩa-theo-so-sánh-trong-một-lân-cận, g01-dinh-nghia-cuc-dai. |
| r1_g01 / 6. Có thể đọc ngược đến đâu? | Bỏ đoạn lặp | Bỏ lộ trình đọc lặp. Gợi mở vẫn yêu cầu thử trả lời trước; phần giảng/ví dụ và Tự kiểm tra của chính mục giữ nội dung và thao tác. Mốc: thử-nghĩ-trước-5, bảng-có-hàng-đạo-hàm-và-bảng-chỉ-có-chiều-biến-thiên, đồ-thị-của-f-khác-đồ-thị-của-fprime. |
| r1_g01 / 7. Làm sao biết mình đã sửa được lỗi? | Bỏ đoạn lặp | Bỏ lộ trình đọc lặp. Gợi mở vẫn yêu cầu thử trả lời trước; phần giảng/ví dụ và Tự kiểm tra của chính mục giữ nội dung và thao tác. Mốc: thử-nghĩ-trước-6, phán-quyết-từ-đúng-giả-thiết, r1-table-t09. |
| r1_g01 / Luyện tập | Biên tập, nhìn thấy | Giữ tại `cach-thuc-hien-luyen-tap`; thao tác cụ thể, đầu câu viết hoa. |
| r1_g01 / Kiểm tra | Biên tập, nhìn thấy | Giữ tại `cach-thuc-hien-kiem-tra`; thao tác cụ thể, đầu câu viết hoa. |
| r1_g01 / Sau khi hoàn thành bài kiểm tra | Biên tập, nhìn thấy | Giữ tại `cach-thuc-hien-sau-kiem-tra`; thao tác cụ thể, đầu câu viết hoa. |
| r1_g01 / Ôn lại | Biên tập, nhìn thấy | Giữ tại `cach-thuc-hien-on-lai`; thao tác cụ thể, đầu câu viết hoa. |
| r1_g01 / Sửa lỗi | Biên tập, nhìn thấy | Giữ tại `cach-thuc-hien-sua-loi`; thao tác cụ thể, đầu câu viết hoa. |
| r1_g01 / Lời giải | Biên tập, nhìn thấy | Giữ tại `cach-thuc-hien-dung-loi-giai`; thao tác cụ thể, đầu câu viết hoa. |
| r1_g02 / Khởi động | Biên tập, nhìn thấy | Giữ tại `cach-thuc-hien-bat-dau`; thao tác cụ thể, đầu câu viết hoa. |
| r1_g02 / 1. Hàm số và tập đang xét | Bỏ đoạn lặp | Bỏ bản tóm tắt lặp trước Gợi mở; định nghĩa/quy trình/lập luận trong phần giảng bên dưới giữ đầy đủ thao tác và điều kiện. Mốc: g02-goi-mo-01, quy-tac-va-tap-xac-dinh, g02-dinh-nghia-ham-so. |
| r1_g02 / 2. So sánh và sự đạt được | Bỏ đoạn lặp | Bỏ bản tóm tắt lặp trước Gợi mở; định nghĩa/quy trình/lập luận trong phần giảng bên dưới giữ đầy đủ thao tác và điều kiện. Mốc: g02-goi-mo-02, dinh-nghia-tren-tap-dang-xet, g02-dinh-nghia-gia-tri-lon-nhat. |
| r1_g02 / 3. Tìm trên đoạn đóng | Bỏ đoạn lặp | Bỏ bản tóm tắt lặp trước Gợi mở; định nghĩa/quy trình/lập luận trong phần giảng bên dưới giữ đầy đủ thao tác và điều kiện. Mốc: g02-goi-mo-03, dieu-kien-bao-dam-ton-tai, g02-dinh-li-ton-tai. |
| r1_g02 / 4. Các tập khác đoạn đóng | Bỏ đoạn lặp | Bỏ bản tóm tắt lặp trước Gợi mở; định nghĩa/quy trình/lập luận trong phần giảng bên dưới giữ đầy đủ thao tác và điều kiện. Mốc: g02-goi-mo-04, doc-su-dat-duoc-khi-thay-tap, r1-g02-table-t03. |
| r1_g02 / 5. Mô hình và ràng buộc | Bỏ đoạn lặp | Bỏ bản tóm tắt lặp trước Gợi mở; định nghĩa/quy trình/lập luận trong phần giảng bên dưới giữ đầy đủ thao tác và điều kiện. Mốc: g02-goi-mo-05, dai-luong-ham-muc-tieu-rang-buoc, cau-hoi-bai-hoc-05. |
| r1_g02 / Luyện tập | Biên tập, nhìn thấy | Giữ tại `cach-thuc-hien-luyen-tap`; thao tác cụ thể, đầu câu viết hoa. |
| r1_g02 / Kiểm tra | Bỏ đoạn lặp | Ba đoạn nhìn thấy ngay trước đã nêu trọn lượt, tự lực, tập đang xét, căn cứ và điều kiện mở hướng dẫn chấm; bỏ hộp nhắc lại. Mốc: kt01, bài-kiểm-tra-01.-đọc-đồ-thị-trên-tập-được-chỉ-định, kt02. |
| r1_g02 / Ôn lại | Biên tập, nhìn thấy | Giữ tại `cach-thuc-hien-on-lai`; thao tác cụ thể, đầu câu viết hoa. |
| r1_g02 / Sửa lỗi | Biên tập, nhìn thấy | Giữ tại `cach-thuc-hien-sua-loi`; thao tác cụ thể, đầu câu viết hoa. |
| r1_g02 / Lời giải | Biên tập, nhìn thấy | Giữ tại `cach-thuc-hien-dung-loi-giai`; thao tác cụ thể, đầu câu viết hoa. |
| r1_g03 / Khởi động | Biên tập, nhìn thấy | Giữ tại `huong-dan-khoi-dong`; thao tác cụ thể, đầu câu viết hoa. |
| r1_g03 / 1. Giới hạn mô tả hành vi của hàm số | Bỏ đoạn lặp | Bỏ lộ trình đọc lặp. Gợi mở vẫn yêu cầu thử trả lời trước; phần giảng/ví dụ và Tự kiểm tra của chính mục giữ nội dung và thao tác. Mốc: GM01, giá-trị-giới-hạn-tại-điểm-và-giới-hạn-ở-vô-cực, H01. |
| r1_g03 / 2. Tiệm cận ngang: xét riêng hai đầu vô cực | Bỏ đoạn lặp | Bỏ lộ trình đọc lặp. Gợi mở vẫn yêu cầu thử trả lời trước; phần giảng/ví dụ và Tự kiểm tra của chính mục giữ nội dung và thao tác. Mốc: GM02, định-nghĩa-và-ý-nghĩa, fnref1. |
| r1_g03 / 3. Tiệm cận đứng: một phía vô cực đã đủ | Bỏ đoạn lặp | Bỏ lộ trình đọc lặp. Gợi mở vẫn yêu cầu thử trả lời trước; phần giảng/ví dụ và Tự kiểm tra của chính mục giữ nội dung và thao tác. Mốc: GM03, định-nghĩa-và-các-phía-được-phép-xét, fnref2. |
| r1_g03 / 4. Tiệm cận xiên: kiểm phần chênh lệch | Bỏ đoạn lặp | Bỏ lộ trình đọc lặp. Gợi mở vẫn yêu cầu thử trả lời trước; phần giảng/ví dụ và Tự kiểm tra của chính mục giữ nội dung và thao tác. Mốc: GM04, định-nghĩa-bằng-giới-hạn-của-hiệu, fnref3. |
| r1_g03 / 5. Đọc kết quả trong đúng miền và đúng bối cảnh | Bỏ đoạn lặp | Bỏ lộ trình đọc lặp. Gợi mở vẫn yêu cầu thử trả lời trước; phần giảng/ví dụ và Tự kiểm tra của chính mục giữ nội dung và thao tác. Mốc: GM05, chọn-giới-hạn-theo-câu-hỏi-và-theo-miền, g03-table-05. |
| r1_g03 / 6. Sửa một lập luận và tự kiểm lại | Bỏ đoạn lặp | Gợi mở và phản hồi đã phân biệt đọc lời chữa với tự làm; Ví dụ 08, Tự kiểm tra 06 và mục Ghi lại điều đã sửa giữ nguyên. Mốc: GM06, H08, T06. |
| r1_g04 / 1. Từ dữ kiện đến sơ đồ khảo sát | Bỏ đoạn lặp | Bỏ lộ trình đọc lặp. Gợi mở vẫn yêu cầu thử trả lời trước; phần giảng/ví dụ và Tự kiểm tra của chính mục giữ nội dung và thao tác. Mốc: GM01, kt-01, VD01. |
| r1_g04 / 2. Khảo sát và vẽ đồ thị hàm số bậc ba | Bỏ đoạn lặp | Bỏ lộ trình đọc lặp. Gợi mở vẫn yêu cầu thử trả lời trước; phần giảng/ví dụ và Tự kiểm tra của chính mục giữ nội dung và thao tác. Mốc: GM02, kt-02, VD02. |
| r1_g04 / 3. Khảo sát hàm phân thức bậc nhất trên bậc nhất | Bỏ đoạn lặp | Bỏ lộ trình đọc lặp. Gợi mở vẫn yêu cầu thử trả lời trước; phần giảng/ví dụ và Tự kiểm tra của chính mục giữ nội dung và thao tác. Mốc: GM03, kt-03, VD04. |
| r1_g04 / 4. Khảo sát hàm phân thức bậc hai trên bậc nhất | Bỏ đoạn lặp | Bỏ lộ trình đọc lặp. Gợi mở vẫn yêu cầu thử trả lời trước; phần giảng/ví dụ và Tự kiểm tra của chính mục giữ nội dung và thao tác. Mốc: GM04, kt-04, VD05. |
| r1_g04 / 5. Đọc và sử dụng kết quả khảo sát đúng miền | Bỏ đoạn lặp | Bỏ lộ trình đọc lặp. Gợi mở vẫn yêu cầu thử trả lời trước; phần giảng/ví dụ và Tự kiểm tra của chính mục giữ nội dung và thao tác. Mốc: GM05, kt-05, VD07. |
| r1_g04 / Luyện tập | Biên tập, nhìn thấy | Giữ tại `huong-dan-luyen-tap`; thao tác cụ thể, đầu câu viết hoa. |

## Kiểm và giới hạn

- Cổng nguồn bốn QMD đạt; hồi quy chỉ dẫn 102/102 và hồi quy mục tiêu 92/92.
- Đối chiếu G01 bằng DOM trong bộ nhớ 18/18: đảo đủ cả mục tiêu và chỉ dẫn về cây đối chứng, binding chỉ dẫn mới khớp; không ghi HTML. Pool của HTML đã trình bày có giới hạn ở một số khóa ngoài phạm vi, đã so với baseline và không phát sinh khóa lệch mới từ lượt này.
- Kiểm toàn vẹn nguồn ngoài 38 mục: nhiệm vụ, công thức, điều kiện và liên kết giữ nguyên. Giữ bookmark cũ dưới dạng span rỗng, không tạo mục trống trong mục lục.
- 2608 tệp được bảo vệ không đổi: website công khai, hai bộ xem, PDF hiện có và Git index.
- Chưa kiểm trực quan bố cục mới, chưa được chủ trì duyệt, chưa commit hoặc xuất bản.

## Bản xem đang có

[Bộ HTML sáu trang](http://127.0.0.1:8877/_audit/html_six_20261018/index.html) là bản trước các lượt sửa mục tiêu và Cách thực hiện. Chưa có bản xem HTML áp dụng lượt sửa này; mở QMD được liên kết phía trên để xem nguồn mới. Khi chủ trì cho dựng, dựng HTML từ nguồn hiện hành và kiểm bố cục rộng/hẹp; không tự tạo PDF hoặc xuất bản.

Bằng chứng kỹ thuật hiện hành tại `_audit/activity_instructions_20261018/`: inventory, baseline, bảo vệ tệp, hồi quy, QMD, DOM và toàn vẹn. Tệp patch dùng một lần không là nguồn vận hành.
