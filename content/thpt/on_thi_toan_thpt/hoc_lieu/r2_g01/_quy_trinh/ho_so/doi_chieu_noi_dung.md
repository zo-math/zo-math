# R2-G01 — Đối chiếu bản thảo nội dung 0.1

**Lượt rà diễn đạt 0.2 ngày 22/10/2026:** [đối chiếu trước–sau và kiểm bảo toàn](ra_dien_dat_20261022.md). Báo cáo dưới đây và kết quả kiểm 0.1 được giữ làm hồ sơ lượt biên soạn trước; chúng không thay kết quả kiểm của bản 0.2. Phạm vi toán, dữ liệu và thiết kế học giữ nguyên; bản sửa câu chữ đang chờ chủ trì duyệt.

Ngày 22/10/2026. Phạm vi: nội dung và kiểm nguồn, chưa QMD/HTML/PDF. Bản nội dung: [noi_dung.md](../ban_thao/noi_dung.md). Hash bản kiểm nằm trong [kết quả kiểm](ket_qua_kiem_tra.json); tài nguyên nguồn và chia mẫu ở [hồ sơ dữ liệu](nguon_va_phan_chia.json).

## 1. Căn cứ và giới hạn ủy quyền

Chủ trì đã duyệt phương án, thiết kế chi tiết và yêu cầu viết bản thảo; dữ liệu Học–Luyện–Kiểm tra–Ôn lại phải giữ riêng. Chưa dựng HTML/PDF, chưa commit/push/phát hành. Thiết kế được triển khai bằng một bản Markdown duy nhất cùng năm tài nguyên dữ liệu trong vùng bản thảo. Không tạo index.qmd, cấu hình hoặc manifest sản xuất để giả đạt readiness.

B37 là trọng tâm; B36 chỉ lấy nền đọc dữ liệu, số đặc trưng mẫu gốc và làm tròn cần thiết. Chưa phủ hết B36. B38/độ phân tán, hồi quy, dự báo, suy luận nhân quả và toàn bộ chương sai số nằm ngoài gói.

Nguồn toán đã đọc trực quan từ PDF cá nhân chỉ đọc: Toán 10 tập một, Kết nối tri thức với cuộc sống, trang 78–81; Toán 11 tập một, trang 58–59, 62–67. Bản ghi hash và đường sách ở hồ sơ dữ liệu. Trang PDF cao hơn trang in một đơn vị. Không chép bài tập hoặc hình sách vào học liệu.

## 2. Đối chiếu chức năng trước viết

Nguồn quản trị đã đọc: AGENTS gốc và chuyên mục; quy tắc làm việc với agent; quy trình kỹ thuật; quy chuẩn ngoặc và khối; 01/02/07/08, README/03 hiện hành; quy chuẩn gói; mẫu bản thảo 1.4 và bảng kiểm 1.7.

Mẫu R1 được đọc như đối chứng chức năng, không suy rằng có hợp đồng kỹ thuật R2 đã triển khai. Gói R2-G01 dùng thiết kế cụ thể được chủ trì duyệt; các chính sách Kiểm tra, nhãn, thuật ngữ và bảng áp dụng toàn chương trình vẫn được giữ.

| Thành phần | Đối chứng thực sự đã đọc | Vị trí R2-G01 | Giữ/điều chỉnh |
|---|---|---|---|
| Bắt đầu, mục tiêu, điểm vào | G01 index.qmd, phần Bắt đầu/Cách học, khoảng dòng 257–320; G02 index.qmd, Bắt đầu/Cách học, khoảng dòng 200–275 | #bat-dau | Giữ điểm vào theo nhu cầu; thay tiên quyết và mục tiêu theo thống kê |
| Bài học → Khởi động | G01/G02 mục Bài học/Khởi động, cây tiêu đề và đường chọn nền; 01/07 | #khoi-dong, #nv01 | Một nhiệm vụ gồm ba thao tác đủ phạm vi, không sao số câu |
| Bài học → từng mục → Gợi mở, giải thích, ví dụ, nhiệm vụ | Mẫu 1.4 và 07; cây mục G01/G02 | #hoc-doc, #hoc-goc, #hoc-ghep, #hoc-uoc-luong, #hoc-chon | Năm mục theo thiết kế; năm Gợi mở, chín Ví dụ, nhiệm vụ 02–06 |
| Luyện tập → chặng → Điểm dừng | 01/2.4, 07/4.3 và mẫu | #luyen-tap, #dung01–03 | Ba chặng, tám nhiệm vụ; không xen Luyện vào Bài học |
| Kiểm tra → kết thúc → đọc kết quả | G01/G02 Cách học; 01/QD_024, 07/4.4 | #kiem-tra, #dung04 | Một lượt 45 phút; không bắt qua Học–Luyện; không tự thêm thang điểm |
| Ôn lại → lượt và giới hạn | G01/G02 điều kiện chuyển gói; 01/2.7 | #on-lai, #dung05–07 | Ba phần dữ liệu mới, đúng lịch 2–3 ngày/7 ngày/3–4 tuần |
| Ôn nền | 01/2.6, mẫu | #nen-tinh, #nen-khoang | Hai thẻ số học/khoảng cục bộ; chưa có nguồn Nền thống kê dùng chung được xác định; không sao thẻ đạo hàm |
| Sửa lỗi | 01/2.5, 07/6.1.7 | #sua-loi, #nv24–27 | Một ngân hàng dự phòng dùng có theo dõi cho mọi nơi gọi, không nhân ba ngân hàng theo lỗi |
| Nhật kí | Nguồn chung _dung_chung/nhat_ki_hoc_tap.qmd đã đọc | #nhat-ki | Dẫn nguồn chung đủ 14 trường, không viết lại schema |
| Lời giải và Nguồn | 07/5.3, 6.3 | #loi-giai, #nguon | 27 cặp đề–lời giải; chín ví dụ giải tại chỗ |

## 3. Ma trận mục tiêu và bằng chứng

| Mục tiêu | Học | Luyện | Kiểm tra | Ôn lại | Xác nhận sau hỗ trợ |
|---|---|---|---|---|---|
| M1 đọc dữ liệu | Mục 1, NV02 | NV07a | NV15a,16a,18 | NV19a | NV24a: cỡ mẫu; NV26a: thiếu |
| M2 mẫu gốc | Mục 2, NV03 | NV07b–c,08 | NV15b,17c,18a | NV19; NV21a | NV24b–c; NV25a: nhiều mốt; NV26d: không mốt |
| M3 ghép nhóm | Mục 3, NV04 | NV09,11a | NV15c,16a,d | NV20a: đọc bảng, không tự lập từ mẫu gốc | NV25a–b |
| M4 số đặc trưng nhóm | Mục 4, NV05 | NV10 | NV16a–c | NV20a–b | NV25c–d |
| M5 chọn số đại diện | Mục 5 | NV12,13,14c | NV17a–b | NV21b | NV26b–c: trọng số/phạm vi; không thay trọn M5 trong mọi bối cảnh |
| M6 giới hạn/đơn vị/ước lượng | Xuyên suốt, NV06 | NV10d,11c,12c,13c,14 | NV16d,17c,18b–c | NV20c,21c–d | NV25b,d; NV26a,c; NV27 |

Kiểm tra chính dùng mẫu gốc chẵn; trường hợp lẻ không được gán là đã kiểm trong lượt đó. M2 nhiều mốt có NV07c trước khi hoàn tất lượt chính và được kiểm lại trong Ôn lại; không suy từ câu một mốt. M3 tự lập bảng và đọc bảng được phân biệt. Đáp án đúng sau tra không được tính ngược thành độc lập.

## 4. Phần trích và chống lộ dữ liệu

- Học: Adélie 2007 dòng 1–50, Gentoo 2007 dòng 153–186; Bike 01/2012; NOAA 01/2023.
- Luyện: Adélie 2008 dòng 51–100; Bike 02/2012; NOAA 07/2023. NV07 giữ mẫu tính tay 12 dòng 51–62, thêm ý c với quan sát kế tiếp dòng 63 = 185 mm để tự làm trường hợp nhiều mốt ngay trong lượt chính. Đây là cụ thể hóa nhiệm vụ trong phần trích đã duyệt, không đổi nguồn/nhóm dữ liệu hoặc số nhiệm vụ.
- Kiểm tra: Adélie 2009 dòng 101–152; Bike 03/2012; NOAA 11/2023.
- Ôn lại: Chinstrap 2007 dòng 277–302; 2008 dòng 303–320; 2009 dòng 321–344. Lượt 1 dùng 12 dòng đầu; 14 dòng còn lại chưa dùng, không tự gọi thành một nhiệm vụ đã biên soạn.
- Sửa: Gentoo 2008 dòng 187–198 (NV24), 199–232 (NV25); Gentoo 2009 dòng 233–276 (NV26); NOAA 02/2023 (NV27 dùng ngày 09–11).
- NV26d chọn dòng nguồn 233, 234, 236, 238, giá trị 212,221,224,228; là phần chọn cho thao tác không mốt, không mẫu ngẫu nhiên.
- Không có giao khóa dòng/ngày giữa năm vai trò. Các mẫu nhỏ nằm trong mẫu lớn cùng vai trò được ghi rõ; không tuyên bố là hai bằng chứng mới độc lập.
- Mỗi phần Ôn lại có khóa nguồn riêng. Không đưa bảng chung ba năm/tháng hoặc kết quả tổng toàn bộ nguồn vào Bài học/Luyện tập.
- Tệp dữ liệu giữ giá trị và NA nguyên dạng. Loại NA chỉ ở phép tính chiều dài. Không loại vì trường không dùng bị thiếu. NOAA giữ đủ PRCP_ATTRIBUTES; đơn vị API đã là mm, không chia thêm cho 10.
- Toàn bộ các tệp JSON là tài nguyên nội bộ của bản thảo, không là tài nguyên tải công khai. Khi triển khai sản phẩm phải chiếu đúng vai trò và lượt, kiểm không đưa dữ liệu tương lai vào trang Học/Luyện hoặc payload dùng chung.

Các phần chưa dùng chỉ là dự phòng dữ liệu, chưa phải một đề kiểm tra thứ hai. Hết bài mới thì ghi đúng giới hạn; không tái sinh đề tùy tiện.

## 5. Khoảng nhóm và những phân biệt cần giữ

Penguins: đóng trái–mở phải, rộng 5 mm; bảng chính Adélie từ 170 đến 215 mm; đối chiếu 10 mm dùng cùng gốc 170. Chinstrap từ 175 đến 215; Gentoo từ 200 đến 235. Mẫu nhỏ có thể chỉ trình các khoảng cần bao phủ và nhóm rỗng bên trong.

Độ dài là biến liên tục được ghi số nguyên mm; khoảng được chọn trực tiếp trên trục đo. Không đổi sang biên nửa đơn vị trong cùng một bài. Quy tắc hiệu chỉnh nhóm đếm nguyên đóng hai đầu trong SGK được phân biệt bằng chú thích ở mục 3.

Bike: khoảng 1000 lượt/ngày; ví dụ tháng 01/2012 có hai nhóm cao nhất đồng hạng, không dùng để kiểm mốt ghép nhóm duy nhất. Bảng tháng luyện/kiểm không cần hiển thị nếu nhiệm vụ dùng tổng/trung vị; dữ liệu nguồn vẫn giữ đủ.

NOAA: lớp điểm {0}, (0;1), [1;5), [5;10), [10;20), [20;40); chỉ mô tả, không nội suy các số đặc trưng trên lớp điểm và nhóm rộng khác nhau. Đếm cờ T riêng trong các số 0. Cờ chất lượng trống đã được kiểm ở các tháng chọn, không phát biểu rằng dữ liệu tuyệt đối không có sai số.

Trung bình gốc Adélie 2008 = 191,04; nhóm 5 mm = 192; nhóm 10 mm = 191,8. Giữ phản ví dụ chống khẳng định “nhóm hẹp hơn luôn gần hơn”. Mốt gốc khác mốt nhóm không được gọi là lỗi tính toán.

## 6. Rà bản thảo trước trình

| Nhóm kiểm | Vị trí/bằng chứng | Kết quả và giới hạn |
|---|---|---|
| Mục tiêu, điểm vào, thời lượng | #bat-dau; ma trận mục 3 | Đã viết đủ sáu mục tiêu và 245 phút lượt chính + 60 phút ôn; hỗ trợ 20–40 phút theo nhu cầu, chưa thử người học |
| Lời giảng có căn cứ, quy ước toán | Mục 1–5, chú thích nguồn tại chỗ | Đã đọc các trang nguồn; diễn giải riêng trên dữ liệu thực, không sao bài tập SGK |
| Ví dụ và Gợi mở | Năm mục Bài học | Có câu hỏi/cầu nối, đủ lời giải; nhiệm vụ dùng lại dữ liệu trong bài chỉ là tự kiểm thao tác, không gán là xác nhận mới |
| Luyện và Điểm dừng | NV07–14; #dung01–03 | Đủ đề, lời giải, tiêu chí, đích hỗ trợ theo ý |
| QD_024 | #bat-dau, #kiem-tra, #dung04 | Có quyền vào thẳng; một lượt; giữ kết quả ban đầu; kết thúc trước hỗ trợ |
| Ôn lại | NV19–21; #dung05–07 | Có lịch, dữ liệu riêng, giới hạn theo mục tiêu; không dùng sớm |
| Ôn nền | NV22–23 | Ví dụ minh họa ghi rõ không dữ liệu thực địa; có câu khác, đáp án, tiêu chí và nơi quay về |
| Nút thắt và xác nhận | #sua-loi; NV24–27 | 11 dòng, bốn cột đúng vai trò; route theo ý; nhận rõ giới hạn và ngân hàng hữu hạn |
| Nhật kí | #nhat-ki | Liên kết nguồn chung 14 trường; không điền giả kết quả học sinh |
| Nhãn và cặp đề–lời giải | NV01–27; Ví dụ 01–09; Gợi mở 01–05; Điểm dừng 01–07 | Dãy liên tục theo loại toàn gói; không đặt lại số theo chức năng |
| Tài nguyên thị giác | Các bảng mẫu nhỏ, bảng nhóm, bảng quan trắc | Bảng số trực tiếp phục vụ nội dung đã duyệt; không có hình/bìa được giao ở pha này, không tạo hình rỗng hoặc PNG bảng |
| Liên kết, LaTeX, dữ liệu và tính toán | ket_qua_kiem_tra.json | Kiểm nguồn trong phạm vi báo cáo máy; không thay duyệt sư phạm |
| QMD/HTML/PDF, responsive, in và trình duyệt | Chưa có sản phẩm | Chưa thực hiện theo chỉ thị, không ghi đạt |
| Chủ trì duyệt nội dung | Bản 0.1 và hash | Chờ duyệt, không kế thừa việc đã duyệt thiết kế thành duyệt nội dung |

### Rà lời văn trong ngữ cảnh

| Cách diễn đạt cần tránh | Vấn đề | Cách đã dùng | Điều giữ lại |
|---|---|---|---|
| “3121 người thuê xe” | Đồng nhất lượt thuê với người | NV06/NV12/NV17 nêu lượt thuê và giới hạn người dùng | Đúng biến cnt |
| “0 nghĩa là không có giáng thủy” | Mất thông tin cờ T | Ví dụ 09 và NV18/NV27 giữ số được ghi cùng cờ | Không tự gán lượng nước cho trace |
| “Đạt sau ba lượt ôn” | Kết luận vượt phần đã kiểm | Mỗi Điểm dừng ôn ghi mục tiêu thực sự được hỏi | Giữ lịch và khoảng trễ thực |
| “Nhóm nhỏ hơn chắc chắn chính xác hơn” | Quy tắc quá mạnh | NV11 dùng đối chiếu thực và lời giải phản ví dụ | Giữ thông tin mất khi ghép nhóm |
| “Làm lại bài này là xác nhận mới” | Bỏ qua lịch sử xem/làm | Phần Sửa lỗi và Điểm dừng giữ giới hạn bài đã dùng | Không lấy dữ liệu lượt ôn sau |
| “Tứ phân vị = vị trí” | Nhầm đối tượng | NV03 dùng giá trị tại vị trí; NV08/15 ghi rõ vị trí | Quy ước chia hai nửa |
| “Trung bình đo chính xác đến 4 chữ số” | Nhầm kết quả số học với độ phân giải phép đo | Ví dụ 01 phân biệt kết quả phép chia và dữ liệu đo | Không thay số liệu gốc |
| “Mọi số gốc phục hồi từ bảng” | Nhầm mô hình nhóm với quan sát | Mục 3–4 và nhiều lời giải phân biệt rõ | Đơn vị và điều kiện công thức |

Đã đọc lại chính văn, đề, lời giải, bảng và chỉ dẫn sau khi viết. Không thêm “Cách thực hiện” lặp ở mỗi mục; giữ điều kiện tự lực tại nơi cần. Chưa dùng kiểm từ vựng tự động để thay đọc nghĩa.

## 7. Kiểm công cụ chung và giới hạn hiện có

- Cổng điều hành bằng Python hệ thống qua launcher: 192/192, không có lỗi tài liệu.
- Lần gọi bằng runtime Python đóng gói thiếu bs4/yaml; đã đổi sang Python hệ thống có thư viện, không cài gói hoặc sửa môi trường.
- Schema/readiness mặc định của zo_learning_architecture.py kiểm G01/G02, báo ba tham chiếu TEX thiếu của G01: do_thi_11.tex, do_thi_12.tex, do_thi_13.tex. Đây là phạm vi kế thừa ngoài R2-G01; không sửa hoặc đổi trạng thái để vượt kiểm.
- R2-G01 chưa có manifest/QMD ở pha bản thảo; các lệnh trên không chứng nhận readiness R2. Phép kiểm riêng cho bản thảo dùng dữ liệu nguồn, liên kết và cấu trúc thực tế.
- 3140 tệp có trước được ghi hash làm đường cơ sở; kết quả so cuối phải giữ nguyên ngoài ghi chú trạng thái R2 được thêm vào 03.
- Không chạy render, prepare, publish, stage, commit hoặc push.

## 8. Tự kiểm và đề nghị duyệt

Đề nghị chủ trì duyệt lời giảng, cách diễn giải ba bối cảnh, độ khó/thời lượng nhiệm vụ và tiêu chí đọc kết quả. Đây là bản thảo đủ nội dung để đọc; chưa là xác nhận hiệu quả với người học thật.

Nếu được duyệt, pha chuyển QMD cần triển khai manifest và chiếu dữ liệu đúng chức năng, sau đó mới có quyền dựng/kiểm sản phẩm theo yêu cầu riêng. Không để một lượt dựng toàn văn dùng chung làm lộ đề hoặc lời giải của các lượt chưa đến.

