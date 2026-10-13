# Nguồn, giới hạn kiểm chứng và chuyển tiếp hồ sơ cũ

Phiên bản: 0.7 · Ngày biên tập: 10/10/2026 · Chuyển tiếp theo QD_021–025.

QD_024 lấy hai sửa đổi trong bản biên tập G01 do chủ trì sửa và xác nhận phạm vi toàn chương trình làm căn cứ. Quy tắc hiện hành ở 01/2.3–2.3.1; 04 ghi chỉ thị, hash bản nhận và phần cũ bị thay. Không dùng điều kiện QD_021 cũ đòi bài làm độc lập trước khi vào Kiểm tra, hoặc suy quyền chia việc học nhiều buổi thành quyền chia cùng một lượt Kiểm tra. Bản gốc người dùng và báo cáo lịch sử giữ nguyên; cập nhật điều hành chưa đồng nghĩa nguồn/đầu ra đã sửa.

QD_023 lấy phê duyệt trực tiếp của chủ trì và phương án hệ nhãn làm căn cứ; từ vựng/quy tắc hiện hành nằm trong danh mục/01/07, không trong hội thoại hoặc audit. Bảng áp dụng G01 được tái tạo từ QMD canonical, tám include chung và manifest; hash/dòng nguồn ghi trong JSON kiểm kê. `_audit/r1_g01_phuong_an_nhan_tieu_de_2026-10-10.md` giữ nội dung đề xuất riêng chưa chốt; tên/số ở đó không tự là chuẩn. Báo cáo `_audit/zo_2027_he_nhan_QD023_2026-10-10/` chỉ chứng minh phạm vi hợp đồng/bảng, không nghiên cứu hiệu quả học tập hoặc nghiệm thu toán/HTML. Phần bị thay được xác định ở QD_023; không hoàn nguyên các quyết định khác.

Tệp này ghi xuất xứ và vai trò tài liệu; không điều hành việc hiện hành. [Điểm vào](README.md).


## Danh mục hiện hành và điểm tiếp quản

[08 — Danh mục thẩm quyền](08_danh_muc_tham_quyen_dieu_hanh.md) phân vai toàn bộ lớp tài liệu, gồm các lớp ngoài thư mục khóa. Kế hoạch 0.6 và baseline D0 giữ nguyên byte; chỉ phần phạm vi/lộ trình của Kế hoạch chưa bị quyết định sau thay thế tiếp tục điều hành. Prompt, checklist gói, mô tả D0, trạng thái chờ và kiểu trình bày cũ không là lệnh hiện hành.

**QD_025/DH_015:** chủ trì giao áp dụng bản biên tập đã tự sửa vào G01 và dựng HTML; QMD/binding đã sửa, HTML cô lập chờ duyệt. Bản người dùng giữ nguyên SHA tại QD_024; không trở thành nguồn build. Từ vựng toàn chương trình lấy từ danh mục/01/07, bổ sung Gợi mở trên nền QD_023. Đường học QD_021, Kiểm tra QD_024 và thay thế QD_022 giữ nguyên. Các mô tả nguồn chưa sửa của DH_012–014 là lịch sử; G02 đã áp dụng/kiểm riêng tại DH_016, HTML mới chờ chủ trì duyệt; các kết quả G01 không thay nghiệm thu G02. Bằng chứng mới thuộc `_audit/r1_g01_ap_dung_ban_chot_2026-10-10/`; không dùng QA/receipt cũ nghiệm thu bản mới.

Rà G01 ban đầu có 21 RD. Phương án đã được duyệt ở QD_020 và biên tập tại DH_011; sau đó chủ trì bác bỏ sơ đồ, được tiếp quản bởi QD_021/DH_012. Các phương án và báo cáo kiểm cũ dưới audit là bằng chứng theo thời điểm, không tự ghi đè phản hồi sau cùng. Các phần 7.x bên dưới giữ nguồn nghiên cứu cũ, không phải kiểm mới của repo. Việc tiếp theo chỉ ở 03.

## Cách tiếp quản trong repo

Bộ Markdown tách và biên tập từ bản tổng hợp `ZO_Math_Kien_truc_hoc_tap_va_lo_trinh_2027_20261006.pdf` và các nguồn đã đọc. Bản PDF vẫn là ảnh chụp nghiên cứu theo thời điểm; không bị sửa ngầm để khớp trạng thái mới.

Khi nhập repo, tìm từng tài liệu cũ bằng tên và nội dung, không mặc định đường dẫn. Ghi nơi thực của Kế hoạch tại điểm vào, của nguồn G01/G02 tại hồ sơ gói. Với tài liệu còn thiếu, ghi thiếu; không tạo một tệp mang tên nguồn cũ rồi điền nội dung suy đoán.

Không tự di chuyển hoặc xóa cả bộ cũ. Nếu được giao hợp nhất, giữ bản gốc và ghi rõ ở đầu tệp cũ phần nào đã được thay thế, đường dẫn tới chuẩn đang dùng và ngày hiệu lực. Với tài liệu còn có nội dung hiệu lực, chỉ đánh dấu phần được thay; không ghi toàn tệp hết hiệu lực.

| Nội dung sau khi tách | Nơi làm việc hiện hành |
|---|---|
| Kiến trúc chung của bản tổng hợp | `01_kien_truc_hoc_tap.md` |
| Quy trình và tiêu chí chung | `02_quy_trinh_va_nghiem_thu.md` |
| Lộ trình và trạng thái hiện hành | `03_dieu_hanh_chuong_trinh.md` |
| Quyết định phát sinh từ nay | `04_nhat_ki_quyet_dinh.md` |
| Cách vận hành cùng Codex/Copilot | `05_huong_dan_su_dung.md` |
| Áp dụng, nội dung thay thế và phép kiểm G01 | `goi/R1_G01.md` |
| Ma trận và yêu cầu kiểm G02 | `goi/R1_G02.md` |

Phần dưới giữ kết quả truy nguyên ngày 06/10. Các phát biểu “đã có/chưa có” nói về bộ nguồn của lần nghiên cứu; không tự thành trạng thái repo hôm nay. Trạng thái thực mới ghi ở hồ sơ gói và bảng điều hành.

## Nối nguồn sau FB036

Theo QD_016–018, phần quy phạm được hợp nhất tại 01 (kiến trúc), 07 (trang người học), chuẩn QMD (component) và hồ sơ từng gói. Bài học/Luyện tập không xen kẽ; mô tả luân phiên trong đặc tả cũ đã bị thay ở đúng quan hệ này. Phân nhóm điều hướng, giữ ngữ cảnh, no-JS và không giật vẫn còn hiệu lực; hình thức bảng ngang/thanh thu gọn QD_007–009 là lịch sử, được rail/drawer của kit thay thế.

| Nguồn mới | Vai trò hiện hành và giới hạn |
|---|---|
| `_design/web_2027_mau_dung_chung/` | Nguồn shell, profile và hợp đồng kỹ thuật đã được dùng; không phải nguồn toán hoặc nơi điều hành khóa. Hợp đồng sư phạm thuộc bộ này. |
| Sổ `phan_hoi_tich_hop_web_2027_0_4.md`, FB001–036 | Yêu cầu, chuỗi thay thế và bằng chứng. FB021 đặt tiêu đề ngoài đã bị FB022 thay; FB024 chốt 9/10; FB027 được FB028 chốt; FB036 mở lại lỗi cụ thể. Không nâng toàn Design 0.5. |
| `giao_dien/web_2027_accepted.json` của G01 | Receipt nghiệm thu HTML FB033, giữ nguyên để đối chiếu; không chứng nhận bản sửa FB036. |
| `doi_sanh_FB036.md` trong kit và audit pair refinement | 17 lỗi, nguyên nhân, nguồn sửa, guard và kết quả của lượt FB036; chưa phải kiểm nội dung toàn gói hoặc nghiệm thu mới. |
| `E:/zo_math_ca_nhan/checkpoints/FB036_20261008_233145/` | Bản chụp bảo toàn. Kiểm ngày 10/10 trước hợp nhất: 1535/1535 mục FILES và 1511/1511 nguồn khớp. Sau hợp nhất, tài liệu được đổi có chủ đích; không cập nhật checkpoint để che khác biệt. |
| `_audit/zo_2027_quyet_dinh_hien_hanh_2026-10-10.md` | Bằng chứng khôi phục D01–35 và N01–08 tại thời điểm khảo sát; không là chuẩn chạy hoặc roadmap thứ hai. |

Góp ý nội dung sau khi tiếp tục checkpoint được ghi trong hồ sơ G01 và QD_017; chưa chốt câu chữ/sơ đồ mới. Trạng thái công việc chỉ ở 03. Bộ nguồn Downloads, Kế hoạch 0.6, receipt, checkpoint và báo cáo lịch sử không bị sửa để phù hợp hiện tại.

## Hồ sơ truy nguyên của lần biên tập

## 7.1. Quan hệ giữa bản này với hồ sơ trước

Bản này gộp phần điều hành, hạt nhân kiến trúc và đặc tả áp dụng đang bị phân tán. Các bản thảo toán học cũ vẫn là nguồn nội dung; không chép lại toàn bộ hàng chục bài vào tài liệu điều hành. Những chỗ cần đổi đã viết cụ thể ở Mục 4 của hồ sơ `goi/R1_G01.md`.

| Tài liệu cũ | Vai trò sau biên tập |
|---|---|
| Kế hoạch thực hiện 2027 phiên bản 0.6 | Giữ làm chuẩn điều hành phạm vi và lộ trình toàn chương trình |
| Nhật kí bước chân trong ZIP | Giữ làm lịch sử đến Bước 021 có trong tệp; không dùng các “việc kế tiếp” cũ làm lệnh hiện hành |
| Đặc tả cụm sửa 01 | Giữ quyết định tên, mã và ý nghĩa D0; phần thao tác là hồ sơ của một đợt sửa |
| Kiến trúc chung 0.1 | Lịch sử, đã được 0.2 thay thế |
| Kiến trúc chung 0.2 | Nguồn hạt nhân kế thừa; tệp `01_kien_truc_hoc_tap.md` cụ thể hóa và giải quyết các đường hở |
| Ma trận triển khai 0.1 | Giữ mã và ánh xạ hữu ích; cập nhật theo phạm vi và biến thể ở hồ sơ `goi/R1_G01.md` |
| Bản thảo bổ sung R1-G02 Pha 2 | Giữ nguồn 14 nhiệm vụ; không diễn giải “chưa tích hợp” ở đầu tệp như trạng thái hiện tại của repo |
| Prompt tích hợp R1-G02 Pha 2 | Lưu lịch sử giao việc; không chạy lại để tái tạo 14 ô |
| Bản thảo bổ sung R1-G01 Pha 3 | Giữ nguồn 21 nhiệm vụ, trừ các thay đổi được nêu rõ tại Mục 4 của hồ sơ `goi/R1_G01.md` |
| Prompt tích hợp R1-G01 Pha 3 | Lưu lịch sử; không dùng lệnh PDF/commit trong đó cho lượt HTML hiện tại |
| Bàn giao ngữ cảnh 05/10 | Dùng truy nguyên quyết định và trạng thái được báo cáo; thông tin repo phải xác minh khi triển khai |
| Đặc tả trang R1-G01 0.1 và 0.2 | Giữ các hợp đồng giao diện còn đúng; 0.1 là lịch sử, 0.2 được đối chiếu với phần học tập của bản này |
| Ghi chú một lõi hai cửa vào | Giữ là giả thuyết sản phẩm về sau, chưa tăng phạm vi hiện hành |

Không xóa lịch sử hoặc thay bản gốc bằng một nội dung rút gọn mất dữ kiện. Sau khi người chủ trì chốt bản hợp nhất, đánh dấu các phần quy phạm bị thay là đã được thay thế; hồ sơ cũ vẫn đọc được nhưng không tranh quyền điều hành với bản đang dùng.

## 7.2. Những điều được kế thừa và những điều mới cần ghi nhận

| Quyết định | Tính chất |
|---|---|
| Tự học là mặc định; Nền và Sửa lỗi gọi khi cần; nhật kí xuyên suốt | Kế thừa |
| Làm trước lời giải; bằng chứng trong lượt khác duy trì; không dùng tổng điểm che lỗi thiết yếu | Kế thừa |
| Ba chặng 4–2–2 của R1-G01; năm bài Kiểm tra; ba lượt Ôn lại | Kế thừa cấu trúc, làm rõ điều kiện sử dụng |
| Phân biệt năm khu vực điều hướng với chu trình học–luyện | Làm rõ mâu thuẫn diễn đạt giữa các đặc tả |
| Một bài sửa mới làm độc lập có thể là phép xác nhận, không tự đòi thêm bài thứ ba | Làm rõ quy tắc và tránh phát sinh nhiệm vụ không có đích |
| Bài mới phải xét nội dung, lịch sử gặp và mức hỗ trợ, không chỉ mã | Bổ sung cách kiểm ngữ nghĩa |
| Tách phần GTLN/GTNN của O02; thay O01, S-O-E02, S-O-E08; bổ sung xác nhận L08; thống nhất ba nhiệm vụ gián đoạn | Thay đổi nội dung có chủ ý, cần cập nhật phiên bản |
| Bảy thẻ Nền và câu xác nhận | Nội dung mới cho các tuyến còn hở |
| Schema Nhật kí 14 trường đã duyệt giữ kết quả, hỗ trợ và việc tiếp theo | Kế thừa đúng schema chung; không rút riêng G01 còn sáu trường |
| Điểm hết ngân hàng có cách xử lý rõ; không mặc định ba tầng bài cho mọi lỗi ở mọi gói tương lai | Hoàn thiện quy tắc vận hành và giới hạn sản xuất |
| Cổng nghiệm thu và tiêu chí dừng sửa | Hợp nhất thành quy trình dùng được |

Không tự nâng tên thành “Kiến trúc 1.0 đã nghiệm thu” trước khi có kết quả triển khai. Khi R1-G01 và R1-G02 đáp ứng các hợp đồng, ghi phiên bản chuẩn được chốt và ngày hiệu lực; các điều chỉnh tham số về sau không phải nâng lại kiến trúc.

## 7.3. Mức kiểm chứng của lần nghiên cứu này

**Đã kiểm trực tiếp:** 12 tệp Markdown trong ZIP tháo gỡ ở các phần liên quan đến quyết định và triển khai; đặc tả kiến trúc 0.2; ma trận hai gói; bản thảo bổ sung R1-G01; cấu trúc, nội dung và script trong HTML đính kèm; các phần Bài học/Luyện/Kiểm tra/Sửa/Ôn của nội dung R1-G01; phạm vi và nhánh chính của R1-G02; các mục Kế hoạch 0.6 về kiến trúc, đánh giá, độ phủ và lịch; ghi chú hai cửa vào. Những bản 0.1 được dùng để nhận diện lịch sử thay đổi, không làm chuẩn song song.

**Đối chiếu nguồn toán có mục tiêu:** Chương trình 2018, trang 105–106, cùng yêu cầu nền liên quan; SGK Toán 12 tập 1 trang in 6 và 9 cho cách phát biểu đơn điệu và bối cảnh định nghĩa cực trị. Các tệp SGK quét và PDF tham chiếu khác là nguồn đối chiếu khi cần, không được coi là đã kiểm từng trang trong lần này. Các đề thi đính kèm không được dùng để suy tần suất hoặc tuyên bố cấu trúc thi 2027.

**Giới hạn ảnh hưởng nghiệm thu:** bộ ZIP HTML thiếu các tài nguyên `site_libs` mà trang tham chiếu, không có nguồn QMD, manifest hoặc repo hiện hành. Môi trường kiểm tra chưa có trình duyệt thực thi phù hợp để hoàn tất kiểm tương tác/thị giác. Vì vậy các phát hiện về logic script là kiểm mã; chưa phải báo cáo PASS/FAIL thị giác toàn trang. Không khẳng định trạng thái website công khai, diff hay commit hiện tại từ bản bàn giao cũ.

Bộ bổ sung có 21 ô trong hồ sơ; phép cộng các nhóm L, K, S-L và bổ sung cho ra 42 nhiệm vụ ở mô hình cũ. Con số này không bao gồm tất cả câu khởi động, câu trong bài và ví dụ. Nó không chứng minh mọi mục tiêu đã có đủ bằng chứng và sẽ thay đổi khi tích hợp các bổ sung ở Mục 4 của hồ sơ `goi/R1_G01.md`.

Một điểm thiếu hồ sơ đáng chú ý: bàn giao nhắc `00_BAT_DAU_O_DAY.md`, `01_NGU_CANH_GOC.md`, `02_PROMPT_DIEU_HANH_WORK.md`, hướng dẫn học chung và Nhật kí tới Bước 026; các tệp hoặc đoạn tương ứng không có đầy đủ trong ZIP đã nhận. Bản này không gán cho chúng nội dung chưa đọc. Việc hợp nhất dựa vào các quyết định đã có bằng chứng trong tệp hiện có.

## 7.4. Sổ đối chiếu bộ nguồn tháo gỡ ngày 07/10/2026

Vị trí nguồn được người chủ trì chỉ định: `D:\Downloads\Ôn thi Toán THPT 2027 — Tháo gỡ hệ thống sản xuất và xuất bản`. Các tệp ở đó được giữ nguyên làm nguồn truy nguyên, không phải điểm vào vận hành. Trạng thái dưới đây áp dụng theo từng vai trò nội dung, không biến toàn tệp thành chỉ dẫn hiện hành.

| Tệp nguồn | SHA-256 | Kết luận và đích canonical |
|---|---|---|
| `03_NHAT_KI_BUOC_CHAN(2).md` | `0096a7c92d8372592ef8c85f69829096c40a832be54eaeb00bcdfda4188049c4` | Lịch sử tiến trình. Kế thừa nguyên tắc một việc tiếp theo, phân lớp lỗi và tách kiểm–nghiệm thu–phát hành; trạng thái/việc tiếp theo cũ không còn điều hành. Đích: tệp 02–05. |
| `04_DAC_TA_CUM_SUA_01_DONG_BO_DANH_MUC_VA_DUONG_BAT_DAU.md` | `56a7565edf79c8d279337364bda2929c93a8dca25e48e776efcd675d2a2765c0` | Hồ sơ một đợt đồng bộ. Kế thừa tên chính thức, bảo toàn ID/URL và yêu cầu kiểm đủ bề mặt; hiện trạng triển khai đã được repo thay thế. Đích: README, tệp 02 và hồ sơ gói. |
| `05_DAC_TA_KIEN_TRUC_HOC_TAP_CHUNG_V0.1.md` | `2136b0f9bfccc733d29e96f9cdd7d94410313559680937cb629e1909b8e78864` | Bản lịch sử, đã bị 0.2 thay thế. Không duy trì như chuẩn song song. |
| `05_DAC_TA_KIEN_TRUC_HOC_TAP_CHUNG_V0.2.md` | `27b87420027c51203e6ecc076118681f2112aab1fe4090d70f37ff521b032597` | Nguồn kiến trúc chính được kế thừa có điều chỉnh. Đích: `01_kien_truc_hoc_tap.md`, tệp 02 và tệp 07. |
| `06_MA_TRAN_TRIEN_KHAI_KIEN_TRUC_HOC_TAP_R1_G01_R1_G02_V0.1.md` | `171583043440ec23abc1e710b88023f575326f4624ca00ccdb4e0d5ad20321b8` | Ma trận thiết kế hai gói. Ánh xạ còn đúng nằm ở hồ sơ G01/G02, schema và manifest; số lượng/trạng thái pha cũ không tự là hiện trạng. |
| `07_BAN_THAO_NOI_DUNG_BO_SUNG_R1_G02_PHA_2_V0.1.md` | `3d879d937833be75c8f86a5495471732eb2ba4cc06b5ac831246ae494846db4e` | Nguồn nội dung 14 nhiệm vụ G02 đã tích hợp. Nguồn thực hiện hành là QMD/manifest G02; không chép bản thảo vào điều hành. |
| `08_PROMPT_CODEX_TICH_HOP_R1_G02_PHA_2.md` | `59c1a4293ed61c3d8737f9db0933cd3ef80c03aa7e7068675f0f11351be9cf98` | Lệnh triển khai theo commit, chỉ lưu lịch sử. Quy tắc công thức phân nhánh còn hiệu lực đã có ở `quy_chuan_goi_qmd.md`; quyền commit/render/PDF trong prompt không còn áp dụng. |
| `09_BAN_THAO_NOI_DUNG_BO_SUNG_R1_G01_PHA_3_V0.1.md` | `b33ac4b6c3764fbe7b1baec1e6698ecde9fe0ff2a5bfc79f18edaa68005c9e76` | Nguồn nội dung 21 nhiệm vụ G01, sau đó đã được sửa có chủ ý theo `QD_003`. Đích hiện hành: QMD/manifest và `goi/R1_G01.md`; không hoàn nguyên theo bản thảo. |
| `10_PROMPT_CODEX_TICH_HOP_R1_G01_PHA_3.md` | `8ac81cb74cfa47472e527931b628f12eaaadbfa82e6d667e4842d7c78a057b62` | Lệnh triển khai theo commit, chỉ lưu lịch sử. Điều kiện worktree sạch, 21 `planned`, dựng PDF và tạo commit thuộc pha cũ; không dùng cho ứng viên HTML hiện tại. |
| `ZO_Math_Ban_giao_ngu_canh_goc_2026-10-05.md` | `e808f680f65e5f752385752c8c5d29d54d59bf2d6342c8006e62fa23fece6321` | Bằng chứng ngữ cảnh hỗn hợp. Kế thừa nguyên tắc UX và phân biệt cổng; nhận định Nhật kí sáu trường cùng trạng thái repo cũ bị quyết định mới thay thế. Đích: tệp 02, 03, 04 và 07. |
| `ZO_Math_Dac_ta_cau_truc_trang_nguoi_hoc_R1_G01_v0.1.md` | `1571065a7f778d20f9233d2dd81911102c86338e464b335c7d5293b18c1daf0d` | Bản lịch sử, đã bị v0.2 thay thế; không là chuẩn song song. |
| `ZO_Math_Dac_ta_cau_truc_trang_nguoi_hoc_R1_G01_v0.2.md` | `e990a3b3b4956379744e05662201d510f351610c806e3e6a5726448ad5b40acb` | Kế thừa có điều chỉnh vào `07_quy_chuan_cau_truc_trang_nguoi_hoc.md`. Không kế thừa Nhật kí sáu trường hoặc chỉ dẫn khởi động mở sẵn; hai điểm ấy đã bị `QD_003`/`QD_004` thay thế. |

Các hash trên được tính lại trực tiếp ngày 07/10/2026 trước khi cập nhật bộ điều hành. Không tệp nào trong thư mục Downloads bị sửa, di chuyển hoặc xóa trong lượt này.

## 7.5. Tài liệu tham chiếu

**Nguồn dự án**

1. `ZO_Math_On_thi_Toan_THPT_Ke_hoach_thuc_hien_2027_0.6(1).md`: đặc biệt các mục 4.5–4.6, 5.1–5.7, 12.1–12.13, 13 và 15–16.
2. `05_DAC_TA_KIEN_TRUC_HOC_TAP_CHUNG_V0.2.md`: hạt nhân, hợp đồng Nền, vai trò nhiệm vụ, nhật kí, tiêu chí kết thúc.
3. `06_MA_TRAN_TRIEN_KHAI_KIEN_TRUC_HOC_TAP_R1_G01_R1_G02_V0.1.md`: mục tiêu, ba chặng, nhóm lỗi và nhiệm vụ.
4. `09_BAN_THAO_NOI_DUNG_BO_SUNG_R1_G01_PHA_3_V0.1.md`: O02 tại Mục 2.2; S-K-E02 tại 3.2; S-O-E02 tại 4.2; S-O-E08 tại 4.8.
5. `ZO_Math_R1-G01_HTML_duyet_20261006.zip`: `content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.html`, các PDF và tài nguyên kèm theo. Các đích kiểm chính: `cp-lt1`, `cp-lt2`, `cp-lt3`, `cp-kt`, `cp-on1`–`cp-on3`, `g01-o02`, `lt08`, `on-nen`, `nhat-ky` và script điều hướng cuối trang.
6. `R1-G01_noi_dung_day_du.md`, `R1-G02_noi_dung_day_du.md`, bản bổ sung R1-G02 Pha 2, hai đặc tả trang người học, bàn giao ngày 05/10 và Nhật kí trong ZIP.
7. Chương trình giáo dục phổ thông môn Toán 2018, trang 105–106; SGK Toán 12 tập 1, Kết nối tri thức với cuộc sống, trang in 6 và 9, tương ứng trang PDF 8 và 11 của bản nhận.

**Nghiên cứu bổ sung đã đối chiếu**

- Nghiên cứu 1: Pashler và cộng sự, 2007. *Organizing Instruction and Study to Improve Student Learning*. IES Practice Guide. [Trang chính thức](https://ies.ed.gov/ncee/wwc/PracticeGuide/1).
- Nghiên cứu 2: Wisniewski, Zierer và Hattie, 2020. *The Power of Feedback Revisited: A Meta-Analysis of Educational Feedback Research*. [Bài báo](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.03087/full).
- Nghiên cứu 3: Rohrer, Dedrick và Burgess, 2014. *The benefit of interleaved mathematics practice is not limited to superficially similar kinds of problems*. [Tóm tắt bài nghiên cứu](https://pubmed.ncbi.nlm.nih.gov/24578089/). DOI: 10.3758/s13423-014-0588-3.
