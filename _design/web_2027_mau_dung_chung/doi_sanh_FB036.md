# FB036 — sửa và đối sánh lại R1-G01 / R1-G02

Ngày 08/10/2026. Phạm vi do chủ trì mở lại: nguồn và HTML hai gói; không PDF,
Git, phát hành hoặc khóa Design 0.5. Đây là hồ sơ xử lí phản hồi, không tự là
quy chuẩn toàn ZO Math. Receipt G01 FB033 giữ nguyên như mốc lịch sử.

## Ma trận lỗi — nguyên nhân, nguồn sửa và guard

| ID | Triệu chứng / nguyên nhân đã xác minh | Sửa trên nguồn nào | Hàng rào chống tái diễn |
|---|---|---|---|
| P36-01 | Bìa G02 mượn đồ thị G01; payload copy tài nguyên gói khác | `r1_g02/giao_dien/cover_g02.tex`, payload và receipt SVG | Nguồn thuộc G02, hash nguồn/ảnh khớp receipt, khác ảnh G01, surface transparent-light |
| P36-02 | Tiêu đề bảng thường và Nhật kí căn giữa theo metadata cũ | QMD hai gói; include Nhật kí; scoped CSS/policy | DOM và computed `text-align:left` ở cả sáu viewport; BBT toán native là ngoại lệ |
| P36-03 | G01 chưa nêu ba chặng ở Cách học; manifest đã có nhưng không hiển thị | G01 QMD `#lo-trinh-hoc`, layout binding | Ba chặng và đúng CP/link; thứ tự nguồn–HTML: tiêu đề → hướng dẫn → chặng |
| P36-04 | L06 có hai nhãn “Xem lời giải” nhưng đích khác nhau | G02 QMD | Nhãn riêng “Xem công thức để kiểm tra” / “Xem lời giải”; giữ hai target thật; fixture âm nhãn trùng |
| P36-05 | “Bài Ôn lại”, “Bài sửa lỗi”, “khắc phục lỗi” dùng xen kẽ | Hai QMD, shared journal, layout binding | Tên UI ngắn “Ôn lại”, “Sửa lỗi”, “Chọn bài sửa lỗi”; ID cũ giữ nguyên |
| P36-06 | Ôn lại G02 thiếu vai trò/mục tiêu/điểm dừng/lỗi cần quan sát so với G01 | G02 O01–03 QMD | Mỗi lượt có đủ metadata và CP thật; giữ nguyên ba đề/lời giải toán |
| P36-07 | “TỰ KIỂM TRA” được adapter chèn cả ngoài và trong cùng paper | Adapter G02 và policy chung | Một nhãn vai trò trong owner; fixture chèn nhãn trùng bị phát hiện |
| P36-08 | Hoạt động xác nhận Nền bị tách thành selftest độc lập; h5 làm owner khó hiểu | G02 QMD: hai `r1-foundation-confirmation` | Task, dữ kiện, hình và lời giải cùng thẻ Nền đóng; ID hoạt động vẫn truy cập được |
| P36-09 | Ôn nền/lời giải mở sẵn theo class và JS cũ | Controller R1, layout và policy scoped | Fresh visit/no-JS có 0 details[open]; deep-link chỉ mở ancestor đích |
| P36-10 | Bảng chọn Sửa lỗi G02 ba cột, G01 bốn cột, widths khác | Hai QMD, `r1-consistency.json`, adapter/CSS | Chung bốn cột 40/20/20/20; target S-L/S-K/S-O tồn tại, cuộn trong table viewport |
| P36-11 | Nhật kí có nguy cơ nhân bản riêng và lệch heading | Shared include `_dung_chung/nhat_ki_hoc_tap.qmd` | Cả hai dùng một nguồn, đủ 14 trường, header trái, tách view Ôn lại |
| P36-12 | Lời giải Khởi động không được nhận diện cùng một nhóm | Hai QMD và layout G01 | Cùng nhóm Lời giải Khởi động, answer IDs tồn tại; deep-link mở đúng lời giải |
| P36-13 | Nhóm lời giải G01 chứa đáp án không thuộc S-O; G02 trộn S-L/S-K và chuyển giao | Hai QMD, layout binding G01 | Cùng tám nhóm vai trò; G02 chuyển giao có nhóm riêng vì có nội dung riêng, không ép G01 có nhóm rỗng |
| P36-14 | Nguồn G02 nằm trong wrapper `.r1-footer`, kế thừa chữ footer nhỏ | G02 QMD bỏ wrapper sai; giữ footer website riêng | Font/size/line-height Nguồn hai gói bằng nhau ở sáu viewport |
| P36-15 | Nhãn trang chính Kiểm tra/Ôn lại/Sửa lỗi/Nguồn/Tải PDF khác tên dù cùng vai trò | Policy/adapter scoped | Ánh xạ cùng chín nhãn vai trò ở hai gói, không đổi nội dung toán |
| P36-16 | Bản đồ G01 có binding cũ khi QMD đổi cấu trúc | One-time migration, canonical layout | Fresh source fingerprint, toán/ID; candidate layout bằng canonical; hook strict không bị bỏ qua |
| P36-17 | PASS hình học cũ bị hiểu nhầm là nghiệm thu/nhất quán semantic | README, hồ sơ trạng thái, checker và báo cáo | Tách đã sửa / đã kiểm / chờ chủ trì / phát hành; hash bản kiểm và receipt lịch sử không ghi đè |

G02 Ôn lại giữ ba lượt sau 2–3 ngày, 7 ngày, 3–4 tuần: tập xác định và sự đạt
được; tập không bị chặn; đại lượng/bối cảnh. Bổ sung định hướng và nhánh sửa,
không thêm đề chỉ để đếm ngang G01. Các lượt này kiểm trọng điểm, không được
suy là mỗi lượt phủ toàn bộ mục tiêu gói.

## Lỗi cũ và giới hạn

Danh sách nguyên văn 28 phản hồi cũ vẫn ở
`_audit/zo_web_2027_g01_g02_doi_sanh_2026-10-08/old-defects.json`.
Không xóa lịch sử B2/B3 hoặc nhận xét chưa đạt để tạo cảm giác không còn lỗi.
Các guard hiện hành kiểm lại trục/inset, ownership nhãn/heading, paper trắng
ở sáu nền, tràn, cỡ hình, ID/math/link, drawer, deep-link và tách Ôn lại/Nhật kí.
FB030–035 và lỗi mới ở bảng trên bổ sung cho 28 bản ghi đó, không thay chúng.

Bằng chứng hiện hành: `_audit/zo_web_pair_refinement_2026-10-08/README.md`,
`pair-qa.json`, `protected-result.json`, ảnh desktop/mobile và `g01-promotion.json`.
Không lấy số PASS làm thẩm định độc lập chân trị toàn bộ đáp án hoặc nghiệm thu.
Chưa kiểm Safari/Firefox, cảm ứng thật, screen reader; PDF chưa đồng bộ.

## Dựng và kiểm

```powershell
python scripts/zo_python.py scripts/zo_web_2027_pair.py render --package r1_g01
python scripts/zo_python.py scripts/zo_g02_completion.py render --output _audit/zo_web_pair_refinement_2026-10-08/g02
python scripts/zo_python.py scripts/zo_g02_completion.py preview --output _audit/zo_web_pair_refinement_2026-10-08/g02
python scripts/zo_python.py scripts/zo_web_2027_pair_check.py
python scripts/zo_python.py scripts/zo_web_2027_pair.py protect
```

Không chạy lại migration hay snapshot để che thay đổi. Promotion G01 là bước
được giao riêng trong lượt này, cần QA PASS và hash nguồn/HTML khớp; không tự
promotion G02, cập nhật receipt nghiệm thu hoặc chuyển tới phát hành.
