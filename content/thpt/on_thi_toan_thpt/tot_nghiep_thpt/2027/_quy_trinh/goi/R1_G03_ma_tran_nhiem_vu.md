# R1-G03 — Ma trận mục tiêu, nhiệm vụ và kiểm chứng

Phiên bản 0.2 · 16/10/2026. Chỉ mục của [bản thảo nội dung 0.2](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md), chưa phải ngân hàng đã nghiệm thu.

[Hồ sơ phạm vi](R1_G03.md) · [Đề cương](R1_G03_de_cuong_bien_soan.md). Đề, dữ kiện và lời giải được sửa tại bản nội dung. Ma trận giữ độ phủ và các tuyến kiểm, không giữ bản đáp án song song. Bản đặc tả 0.1 trước chuyển đổi được lưu tại `_audit/r1_g03_manuscript_20261016/before/` tính từ gốc repo.

## 1. Ma trận mục tiêu–bằng chứng

| Mục tiêu | Học/ví dụ | Luyện và điểm dừng | Kiểm tra | Ôn lại lấy mẫu | Lỗi chính |
|---|---|---|---|---|---|
| M1: miền, giới hạn và giá trị | bh-01/H01 | L03, L04; CP01 | K01 | O01(a), O03(a) | E01 |
| M2: ngang, hai đầu vô cực | bh-02/H02–H03 | L01, L02, L05; CP01 | K02 | O01(b), O03(b) | E03 |
| M3: đứng, ít nhất một phía | bh-03/H04 | L01–L04; CP01 | K01, K03 | O01(a), O02(a) | E01–E02 |
| M4: xiên, kiểm hiệu về 0 | bh-04/H05 | L06–L07; CP02 | K03 | O02(a), O03(c) | E04 |
| M5: đổi biểu diễn, phản ví dụ | bh-02…bh-05 | L08–L09; CP02 | K02, K04 | O02(b), O03(b) | E03, E05 |
| M6: miền và ý nghĩa mô hình | bh-05/H06 | L10; CP02 | K05 | O03(d) | E06 |

Mỗi ý K là bằng chứng đúng mục tiêu mà nó kiểm, không suy từ một điểm tổng. K01 sai miền không được che bởi K03 tính nhanh; K02 đúng theo dữ kiện chưa tự chứng nhận khả năng tính giới hạn căn. Trước công nhận lượt chính, bổ sung bằng chứng còn mới cho mục tiêu chưa đạt; không sửa điểm K ban đầu bằng điểm sau hỗ trợ.

## 2. Quy tắc phân vai và độ lộ

H01–H06 là ví dụ trong bản nội dung, không là bài đo độc lập. L là tự luyện nhưng chỉ tính bằng chứng trước mở trợ giúp. K chỉ tự lực trong toàn lượt. O dùng sau khoảng trễ thực. S cần lời giải mẫu/phân tích lỗi riêng; câu xác nhận S không được giải sẵn trong chính đoạn dẫn. P là nhánh tự chọn. Câu nền xác nhận thao tác nền, không tự xác nhận mục tiêu toàn gói.

Bản thảo hiện triển khai: 10 L, 5 K, 3 O nhiều ý, 9 S, 2 P; 6 ví dụ H có lời giải mẫu trong Bài học. Đây là 29 nhiệm vụ L/K/O/S/P, không phải số đơn vị cuối cùng của QMD, không gồm các câu Khởi động/Tự kiểm tra Bài học hoặc câu nền. Số lượng phải đổi nếu rà nội dung thấy thiếu bằng chứng; không dùng con số này làm chỉ tiêu nghiệm thu.

Khi viết nguồn, mỗi nhiệm vụ có: ID, owner, chức năng, mục tiêu/ý, dữ kiện chuẩn, đề, lời giải, tiêu chí, lịch sử dùng làm mẫu, nơi gọi và nơi về. So cả công thức sau rút gọn, hình và kết luận cốt lõi giữa H/L/K/O/S/N; đổi số hoặc mã không tự chứng minh một câu còn mới với người học. Các câu trong bản thảo chưa được gắn vào lịch sử gặp bài của học sinh.

## 3. Chỉ mục đề và lời giải

| Mã | Nhiệm vụ | Lời giải |
|---|---|---|
| L01 | [Từ giới hạn đến đường thẳng](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#L01) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-L01) |
| L02 | [Giữ miền trước khi tính](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#L02) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-L02) |
| L03 | [Một điểm hở](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#L03) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-L03) |
| L04 | [Chỉ có một phía để tiến gần](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#L04) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-L04) |
| L05 | [Không bỏ sót đầu trái](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#L05) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-L05) |
| L06 | [Thương và phần dư](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#L06) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-L06) |
| L07 | [Đừng bỏ mất hệ số tự do](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#L07) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-L07) |
| L08 | [Cắt mà vẫn tiến sát](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#L08) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-L08) |
| L09 | [Một hình, ba hành vi](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#L09) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-L09) |
| L10 | [Nhiệt độ trong mô hình](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#L10) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-L10) |
| K01 | [Hai hàm ở cùng một mốc](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#K01) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-K01) |
| K02 | [Đọc hai đầu và một mốc hữu hạn](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#K02) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-K02) |
| K03 | [Đường xiên cần đủ hai hệ số](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#K03) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-K03) |
| K04 | [Một phản ví dụ cần hai điều](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#K04) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-K04) |
| K05 | [Giới hạn của mô hình](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#K05) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-K05) |
| O01 | [Nhớ lại miền và giới hạn](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#O01) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-O01) |
| O02 | [Phần dư và giao điểm](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#O02) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-O02) |
| O03 | [Chọn điều cần kiểm](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#O03) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-O03) |
| P01 | [Phối hợp — tiệm cận và giá trị không đạt](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#P01) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-P01) |
| P02 | [Chuyển giao — hai đường xiên khác nhau](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#P02) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-P02) |
| S-L01 | [Giữ điểm bị loại](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#S-L01) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-S-L01) |
| S-L02 | [Dấu ở hai phía](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#S-L02) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-S-L02) |
| S-L03 | [Hai đầu và một giao điểm](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#S-L03) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-S-L03) |
| S-L04 | [Giữ hằng số và giữ miền mô hình](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#S-L04) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-S-L04) |
| S-K01 | [Phân biệt hữu hạn và vô cực](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#S-K01) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-S-K01) |
| S-K02 | [Không nhầm giới hạn với giao điểm](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#S-K02) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-S-K02) |
| S-K03 | [Xác nhận đường xiên và ý nghĩa mô hình](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#S-K03) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-S-K03) |
| S-O01 | [Ôn lại miền, phía và hai đầu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#S-O01) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-S-O01) |
| S-O02 | [Ôn lại phần dư và cách diễn giải](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#S-O02) | [Đối chiếu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-S-O02) |

Hai điểm dừng [CP01](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#CP01), [CP02](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#CP02) và [sau Kiểm tra](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#CPK) giữ tiêu chí, nhánh hỗ trợ và nơi quay về. Các mô hình đã có đơn vị và miền trong đề; L09/K02 có hình riêng kèm giới hạn chính xác.

## 4. Ví dụ, câu tự kiểm và nền

| Nhóm | Đề/vị trí và phản hồi |
|---|---|
| GM01 | [Gợi mở](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#GM01), phản hồi tại chỗ |
| H01 | [Ví dụ 01](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#H01), lời giải mẫu tại chỗ |
| H02 | [Ví dụ 02](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#H02), lời giải mẫu tại chỗ |
| H03 | [Ví dụ 03](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#H03), lời giải mẫu tại chỗ |
| H04 | [Ví dụ 04](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#H04), lời giải mẫu tại chỗ |
| H05 | [Ví dụ 05](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#H05), lời giải mẫu tại chỗ |
| H06 | [Ví dụ 06](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#H06), lời giải mẫu tại chỗ |
| T01 | [Tự kiểm tra 01](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#T01) · [Lời giải](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-T01) |
| T02 | [Tự kiểm tra 02](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#T02) · [Lời giải](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-T02) |
| T03 | [Tự kiểm tra 03](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#T03) · [Lời giải](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-T03) |
| T04 | [Tự kiểm tra 04](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#T04) · [Lời giải](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-T04) |
| T05 | [Tự kiểm tra 05](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#T05) · [Lời giải](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#lg-T05) |
| N02-Q | [Một phía](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#N02-Q), đáp án và tiêu chí tại chỗ |
| N03-Q1 | [Phân thức ở vô cực](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#N03-Q1), đáp án và tiêu chí tại chỗ |
| N03-Q2 | [Căn ở hai đầu](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#N03-Q2), đáp án và tiêu chí tại chỗ |
| NDS-Q | [Thương và dư](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#NDS-Q), đáp án và tiêu chí tại chỗ |

Tổng kiểm kê: 39 nhiệm vụ/câu tự kiểm và 6 ví dụ. Ba phần nền có 4 câu vì phần căn có tiêu chí riêng; không dùng kết quả câu phân thức để xác nhận nền căn.

## 5. Họ lỗi, hỗ trợ và câu xác nhận còn mới

| Mã lỗi | Dấu hiệu cần đối chiếu | Nền/đoạn học cần gọi |
|---|---|---|
| E01 | Gọi mọi nghiệm mẫu là đứng; bỏ điều kiện sau rút gọn; gán giới hạn làm giá trị | N-TXĐ-01, bh-01/03 |
| E02 | Mất dấu vô cực, nhầm phía; đòi cả hai phía cùng vô cực | N-DẤU-01, N-GH-02, bh-03 |
| E03 | Chỉ xét +∞; đếm đôi cùng một đường; nhầm phương trình x=L/y=L | N-GH-03, bh-02 |
| E04 | Chia sai, thiếu b; chỉ dùng f(x)/x, hoặc dùng hiệu không về 0 | N-ĐS-01, bh-04 |
| E05 | Dùng hình phác làm số đo chính xác; cho rằng cắt là không thể tiệm cận | bh-02/05; đối chiếu giới hạn và giao điểm |
| E06 | Ngoại suy sang mốc ngoài miền; gọi giới hạn là giá trị tối ưu đạt được | bh-05; N-TXĐ-01/N-GH-01 nếu đúng nhu cầu |

Xem [bảng chọn câu sửa](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#chon-sua-loi) và [xử lí khi hết câu mới](../../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md#het-bai-moi). Lời giải câu sửa tách khỏi đoạn dẫn. Mỗi ý chỉ xác nhận mục tiêu tương ứng; giữ kết quả trước và sau trợ giúp riêng.

Các câu sửa lỗ hổng, dấu giới hạn, phần dư và mô hình gần cấu trúc với bài học/luyện tập; chúng phục vụ xác nhận mục tiêu hẹp, không chứng minh chuyển giao rộng. Đã rà cả công thức và ý nghĩa, không chỉ so mã. Độ lộ thực tế cần lịch sử gặp bài của từng học sinh. Nếu hình K02 đã lộ và khả năng đọc hình chưa đạt, câu chỉ tính công thức không thay đủ bằng chứng đó; ghi rõ phần còn thiếu.

## 6. Ánh xạ 14 tình huống đường học — đối chiếu bản thảo, chưa kiểm giao diện

| Ca theo 01 | Tình huống riêng G03, đích và điều kiện |
|---|---|
| DH01 | Vướng khái niệm trong bh-02: xem lại định nghĩa/giới hạn ở bh-02, trở về câu tự kiểm của mục ấy |
| DH02 | Không đọc được giới hạn trái/phải ở bh-03: N-GH-02 và xác nhận nền, quay đúng câu; thẻ đã có trong bản thảo |
| DH03 | Tự kiểm Bài học sai E01: giữ bài, đối chiếu lời giải, gọi S-L01 nếu còn mới; quay về câu/điểm dừng Bài học |
| DH04 | L06 thiếu cách tách xiên: bh-04, trở về L06; phần sau trợ giúp ghi đúng mức hỗ trợ |
| DH05 | L02 không biết dấu mẫu: N-DẤU-01/N-GH-02, trở lại bước giới hạn của L02 |
| DH06 | CP01/CP02: đối chiếu từng mục tiêu; nếu đạt tiếp tục tự chọn, nếu sai gọi đúng ý S; không bắt đi qua hỗ trợ |
| DH07 | Đang làm K03: không mở lời giải/N/khối học; muốn trợ giúp thì kết thúc toàn lượt K trước |
| DH08 | K hoàn tất: lưu kết quả gốc; sai mục tiêu nào dùng nhánh S-K tương ứng, giữ riêng bằng chứng sau sửa |
| DH09 | O02(a) quên phép chia: N-ĐS-01 hoặc bh-04 tùy nguyên nhân; quay lại O02(a), không tính phần đã hỗ trợ thành kết quả ban đầu |
| DH10 | O03(d) sai nghĩa mô hình: đối chiếu và S-O02(c) còn mới, quay lại mục tiêu/điểm dừng O03 |
| DH11 | Kết thúc buổi hoặc quyết định hẹn ôn: Nhật kí chung 14 trường, chỉ điền dữ kiện có; ghi locator tiếp tục |
| DH12 | Vào thẳng Kiểm tra khi đủ tự tin: cho phép; không coi L chưa làm là lỗi hoặc phần bỏ qua đã đạt; DH07 vẫn áp dụng |
| DH13 | Vào thẳng S-L04/N-GH-03: chọn câu đang cần hỗ trợ hoặc một điểm vào phù hợp; không đưa mọi người về CP02 cố định |
| DH14 | S-K01(a) đã xem đáp án: tìm câu còn mới đúng E01, nếu hết thì ghi chưa đủ bằng chứng; không đổi mã rồi tái sử dụng |

Các đích bản thảo, cặp đề–đáp án và liên kết quay về đã được kiểm. Chưa có QMD/DOM để kiểm hành vi khi dựng. Không chép bảng quản trị này vào lời dẫn người học.

## 7. Giới hạn kiểm còn giữ

Đã có nội dung, câu tự kiểm, ba phần nền, các lời giải và bảy hình. Các kiểm toán học có mục tiêu, liên kết và nguồn hình được lưu trong báo cáo lượt biên soạn; không thay phản biện toán độc lập, đọc thử với học sinh, chốt tải học hoặc đo duy trì sau khoảng trễ. Khi chuyển sang QMD, còn phải kiểm binding, nhãn và DH01–DH14 trong giao diện thực. Không dùng số dòng nhiệm vụ làm tiêu chí nghiệm thu. Việc tiếp theo do bảng 03 điều hành.
