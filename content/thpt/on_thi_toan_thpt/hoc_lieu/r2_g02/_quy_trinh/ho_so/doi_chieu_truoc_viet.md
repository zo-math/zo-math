# Đối chiếu trước biên soạn R2-G02

Ngày: 29/10/2026. Căn cứ: chủ trì trả lời “Mình duyệt kế hoạch này.” sau bản rà soát phạm vi và đề cương trong cùng cuộc trao đổi. Phạm vi được chốt: Độ phân tán và so sánh dữ liệu; B36 phần độ phân tán, B38; gọi lại B37; tài nguyên Ôn nền dùng chung về số gần đúng, sai số và quy tròn. Chưa chuyển QMD, dựng HTML/PDF, commit hoặc phát hành.

Nguồn đang sửa dự kiến: `hoc_lieu/r2_g02/_quy_trinh/ban_thao/noi_dung.md`. Tài nguyên nền có một nguồn riêng ở `hoc_lieu/_dung_chung/nen/_quy_trinh/ban_thao/so_gan_dung_sai_so.md`; gói dẫn tới đó, không sao văn bản. Hình của bản thảo nằm trong `ban_thao/hinh/`. Vùng chuẩn bị trong workspace chỉ phục vụ chuyển tệp có kiểm soát; không là nguồn dựng hoặc một kho nội dung song song.

Mẫu bản thảo 1.6 và bảng kiểm 1.9. Quy tắc hiện hành: 01/2.1.1; 02/1.4–1.6; 07/6.1.4, 6.1.6–6.1.8, 6.2.1–6.3; quy chuẩn gói; dấu ngoặc LaTeX; hướng dẫn khối nội dung. Cổng điều hành: 192/192 đạt trước viết. Cổng schema/readiness mặc định cho hai gói R1 đối chứng báo ba tài sản TEX thiếu ở R1-G01 (do_thi_11, do_thi_12, do_thi_13); đây là lỗi đối chứng ngoài phạm vi, không sửa hoặc coi như đã đạt. Chưa tạo manifest R2-G02 ở pha bản thảo theo quy chuẩn gói, mục Khởi tạo.

## Đối chiếu theo chức năng

| Thành phần | Nguồn đối chứng đã đọc | Áp dụng R2-G02 |
|---|---|---|
| Bắt đầu và mục tiêu | R2-G01/index.qmd, Bắt đầu; R1-G01/index.qmd, Bắt đầu | Một bảng mục tiêu; tách kết quả độc lập, kết quả sau hỗ trợ, duy trì sau khoảng trễ. |
| Bài học và dẫn nhập | R2-G01/index.qmd, Bài học; quy tắc 07 đã thay phần mẫu cũ | Hai đoạn thường; năm mục toán đã duyệt; hoạt động thuộc đúng mục cha. |
| Khởi động và nền | R1-G02/index.qmd, Bài học/Ôn nền | Kiểm tần số, trung bình, tứ phân vị, căn; tuyến nền thực sự có câu tự làm. |
| Gợi mở, lời giảng, ví dụ | R2-G01/index.qmd, các mục 1–5 | Câu hỏi trước công thức; dữ liệu nhỏ giả định; phản ví dụ; dữ liệu thật dùng ở luyện tập, không làm khuôn toàn bài. |
| Luyện tập/Điểm dừng | R1-G02/index.qmd, Điểm dừng 01–03 | Ba nhóm theo nội dung: mẫu gốc, bảng nhóm, diễn giải; quyết định theo mục tiêu. |
| Kiểm tra | R1-G02/index.qmd, Kiểm tra/Điểm dừng 05 | Tự lực một lượt; bốn nhiệm vụ mới, thang 10 điểm và tiêu chí theo ý. |
| Ôn lại | 01/2.7; R2-G01/index.qmd, Ôn lại | Ba lượt 2–3 ngày, 7 ngày, 3–4 tuần; không nhắc công thức trước đề. |
| Sửa lỗi | 01/2.5; 07/6.1.7; R1-G02, Sửa lỗi | Bảng nút thắt, tám câu xác nhận riêng; dùng theo nhu cầu, ghi chưa xác nhận khi đã lộ. |
| Nhật kí | _dung_chung/nhat_ki_hoc_tap.qmd; R2-G01, Nhật kí | Giữ 14 trường; ví dụ giả lập thống kê không lộ lời giải nhiệm vụ dự trữ. |
| Nguồn và hình | R2-G01/hinh/y_tuong_v01/build_figures.py; 07/6.3 | Ba hình thống kê native, phông STIX Two và palette ZO Math 0.4; chú thích phân biệt dấu, dữ kiện và đại diện nhóm. |

## Bản đồ mục tiêu dự kiến

| Mục tiêu | Bài học | Luyện tập | Kiểm tra | Ôn lại | Hỗ trợ |
|---|---|---|---|---|---|
| Nhận ra trung tâm chưa đủ | 1, 5 | 08, 12 | 16 | 19 | 22, 28 |
| Khoảng biến thiên, tứ phân vị, bất thường | 2 | 07, 08 | 13 | 17 | 26, 29; nền 20 |
| Phương sai, độ lệch chuẩn, tần số | 3 | 07, 08 | 13, 15 | 17 | 23, 24; nền 21 |
| Ghép nhóm và giới hạn | 4 | 09, 10 | 14, 15 | 18 | 25 |
| Đơn vị, biến đổi và kết luận | 5 | 11, 12 | 15, 16 | 19 | 27, 28 |

## Ma trận hình trước viết

| Hình | Vị trí | Vai trò | Dữ liệu/giới hạn |
|---|---|---|---|
| Cùng trung tâm, khác độ trải | Mục 1 | Hai biểu đồ chấm cùng thang, thấy điều trung bình che đi | Hai mẫu giả định; chấm là quan sát, vạch là trung bình chung. |
| Một giá trị xa phần còn lại | Mục 2.3 | Đối chiếu khoảng tứ phân vị và ngưỡng phát hiện bất thường | Phân biệt ngưỡng kiểm tra với giá trị quan sát; không ngụ ý tự loại. |
| Cùng bảng nhóm, khác phân tán | Mục 4.3 | Bằng chứng bảng nhóm không xác định phương sai gốc | Hai mẫu có cùng trung bình/cùng tần số nhóm nhưng phương sai khác; trung điểm là đại diện. |

Nguồn toán: CT2018 trang 85–86, 110; Toán 10 KNTT tập một Bài 12 trang 73–77, Bài 14 trang 84–88; Toán 12 KNTT tập một Bài 9–10 trang 75–83. Đã đọc trang PDF trực tiếp. Giữ đúng phiên bản sách bản mẫu; không sao phép tính ví dụ mà chưa tự kiểm.
