# Nhật kí quyết định

Phiên bản: 0.1 · Cập nhật: 13/10/2026.

Chỉ ghi quyết định có ảnh hưởng lâu dài; không chép hội thoại hay log lệnh. Bảng điều hành ghi việc hiện hành. [Điểm vào](README.md).


## QD_035 — Bảo vệ đúng bộ bản xem chủ trì chọn làm đối chiếu phát triển

- Ngày: 13/10/2026. Trạng thái: **đã chốt phạm vi bảo toàn**. Người chốt: chủ trì, chỉ định `file:///e%3A/zo_math/_audit/zo_home_refinement_2026-10-12/delivered/home-reading.html` cùng các trang nó liên kết tới, hỏi bộ đó đã thành nguồn không được xóa chưa, rồi giao “Làm đi” sau phương án bổ sung danh mục/checkpoint.
- Vấn đề và bằng chứng: đúng bộ này vẫn còn nhưng chưa được ghi riêng trong danh mục bảo toàn; DH_030 chọn Home `zo_home_copy_approved` và ba trang `zo_course_navigation/html-current`, không chứa đúng bộ `zo_home_refinement/delivered`. Không suy “tệp còn tồn tại” thành “đã được bảo toàn đúng bản”.
- Nội dung: bộ Home được chỉ định, D0/G01/G02 nó liên kết trực tiếp, toàn runtime và các đích/tài nguyên local cần thiết là **nguồn đối chiếu chính thức để phát triển tiếp, không được dọn/xóa hoặc tự thay bằng bản khác**. Giữ toàn cây delivered và từng phụ thuộc trong manifest DH_032; sao lưu độc lập ngoài repo, manifest/ZIP/hướng dẫn khôi phục và SHA-256 từng tệp. Chưa có chỉ thị riêng thì không di chuyển/ghi đè bộ gốc, kể cả khi nằm trong `_audit/` hoặc bị Git ignore.
- Chủ sở hữu: `bao_toan_bon_trang.md` sở hữu danh mục/điều kiện không được dọn; manifest DH_032 ghi tập tệp/hash của đúng bản; 03 sở hữu trạng thái DH_032; 08 và README dẫn vai trò. Nguồn dựng vẫn là QMD/template/data/script canonical, không biến HTML audit thành nguồn build hoặc bộ quy tắc thứ hai.
- Phần bị thay: lựa chọn bản xem mặc định trong chỉ mục DH_030 không còn được dùng để thay cho bộ chủ trì chỉ định trong lượt này. Không sửa hoặc ghi đè checkpoint DH_030/PRE_CLEANUP_QD033, lịch sử QD_001–034, receipt hoặc báo cáo cũ; không hủy bảo vệ các bộ khác đã được sao lưu.
- Phần không bị thay: QD_033/thiết kế/câu chữ đã duyệt, trạng thái nghiệm thu/PDF/phát hành và các nguồn sản xuất. Bản Home được chọn khác câu chữ canonical hiện hành; bảo toàn không tự hoàn nguyên biên tập và không chứng nhận có thể dựng lại chính xác bản đó. Nếu cần đồng bộ nguồn với bản đối chiếu, phải kiểm sai khác và giao sửa riêng; hiệu chỉnh hợp lệ ở nguồn không bị cấm.
- Tệp chịu ảnh hưởng: danh mục bảo toàn, 03/04/08 và README điều hành; checkpoint `E:/zo_math_ca_nhan/checkpoints/DH032_20261013_BO_BAN_XEM_CHU_TRI_CHON` cùng ZIP. Không sửa học liệu QMD/HTML/CSS/JavaScript/hình/PDF, schema/registry/checker hoặc `.git`.
- Chống hồi quy: trước dọn phải đọc danh mục và manifest DH_032, loại tệp được bảo vệ khỏi danh sách; kiểm payload và từng thành viên ZIP, tài nguyên local, hai cổng điều hành, hai checkpoint cũ và phạm vi HEAD/index/tệp ngoài thay đổi. Không lấy PASS bảo toàn làm nghiệm thu nội dung hay cho phép xóa. Không render, dọn thêm, stage/commit/push/xuất bản trong lượt này.

## QD_034 — Ngừng dùng driver lịch sử sau bảo toàn ngoài repo

- Ngày: 13/10/2026; người chốt: chủ trì. Trạng thái: **chủ trì cho phép thực hiện phương án đã trình với điều kiện an toàn và giữ được thành quả**; lời xác nhận “Mình không hiểu vấn đề. Nhưng nếu an toàn và giữ được thành quả thì cứ làm tiếp.” Không suy từ xác nhận này thành nghiệm thu kỹ thuật hoặc quyền mở rộng danh sách.
- Vấn đề/bằng chứng: đợt 2 đã lưu toàn bộ mười mục lịch sử nhưng giữ bảy cây vì 21 driver audit một lần còn đọc chúng. Khảo sát tiếp nối chỉ ra đây là đường chạy lịch sử, không phải mặc định sản xuất hiện hành; phương án tại `E:/zo_math_ca_nhan/legacy_backup_archive/ZO_MATH_AUDIT_HISTORY_20261012/evidence/phuong_an_go_phu_thuoc_lich_su_20261013.txt` xác định đúng phạm vi và điều kiện dừng.
- Nội dung: sao lưu nguyên byte 21 driver và ba tài liệu trước sửa vào kho bổ sung độc lập, manifest/SHA-256 khớp mới nghỉ dùng driver; chỉ gỡ bảy cây khi nguồn/bản lưu khớp từng tệp/cấu trúc, không còn caller hiện hành hoặc tiến trình/lock/reparse chưa rõ và cổng điều hành đạt. Mục không đạt phải giữ, không sửa checker/hợp đồng để hợp thức hóa việc gỡ.
- Phạm vi/tệp chịu ảnh hưởng: 03 sở hữu trạng thái DH_031; mục mới này ghi quyết định; 08 dẫn thẩm quyền; `luu_tru_lich_su.json` chỉ ánh xạ 7 cây/21 script tới hai kho và manifest ngoài repo. Chỉ mục không là nguồn build, chuẩn học tập hoặc bảng công việc thứ hai. Danh sách chi tiết và phân loại kiểm lịch sử tại chỉ mục/`evidence/dependency-resolution.json` của kho bổ sung.
- Phần bị thay: yêu cầu giữ bảy cây trong quyết định thao tác đợt 2 vì driver lịch sử còn tồn tại được thay bằng điều kiện nghỉ dùng/bảo toàn đã xác minh. Không viết lại báo cáo hay quyết định giữ của đợt 2. Các driver đã nghỉ dùng không được lấy lại làm điểm vào sản xuất hoặc tự tái kích hoạt; nếu cần phục dựng mốc cũ phải khôi phục có chọn lọc trong phạm vi được giao.
- Phần không bị thay: QD_033 và các quy tắc học tập/thiết kế còn hiệu lực; toàn bộ lịch sử QD_001–033, kết quả QA/receipt/checkpoint/manifest cũ; checker canonical nhận đầu vào mới, nguồn và bản xem bốn trang. Giữ `html-current`, `delivery` và figure `build` còn được dùng, không xóa theo tên thư mục cha. Không chuyển driver audit thành công cụ production, không dùng QA cũ chứng nhận sản phẩm mới.
- Chống hồi quy/bằng chứng: bản trước sửa 03/04/08 và 21 script tại `E:/zo_math_ca_nhan/legacy_backup_archive/ZO_MATH_AUDIT_RETIREMENT_20261013`; bảy cây tại kho lịch sử 20261012. Giữ cấu trúc repo, hướng dẫn khôi phục và hash manifest; kiểm hai cổng qua launcher, hai checkpoint, tài nguyên bản xem và HEAD/index/phạm vi ngoài danh sách trước/sau. Kết quả cuối tại `evidence/result.json` của kho bổ sung, không sửa kết quả cũ.
- Ranh giới: không sửa học liệu QMD/HTML/CSS/tài sản/PDF/bản xem, 01/07/schema/registry hay checker canonical; không render, stage/commit/push/xuất bản hoặc dọn mục khác. PASS bảo toàn không chứng nhận QMD/HTML G01/G02 đã áp dụng QD_033; việc đối chiếu ấy vẫn cần một lượt riêng.

## QD_033 — Khép kiến trúc học tập, điểm vào và hỗ trợ theo ngữ cảnh

- Ngày: 12/10/2026; trạng thái: **chủ trì giao cập nhật bộ điều hành theo các nguyên tắc đã nêu**, bản sửa tài liệu chờ chủ trì duyệt; chưa giao sửa sản phẩm.
- Vấn đề/bằng chứng: khảo sát điều hành phát hiện cách diễn đạt có thể biến tiến trình chuẩn thành điều kiện bắt buộc phải hoàn thành tuần tự, sáu việc theo thứ tự ở mọi Điểm dừng và liên kết quay lại đề vô điều kiện; yêu cầu hiện tại của chủ trì xác lập các nguyên tắc dưới đây cho toàn chương trình.
- Nội dung: Bài học → Luyện tập → Kiểm tra → Ôn lại là tiến trình chuẩn được khuyến nghị, nhưng không phải điều kiện bắt buộc phải hoàn thành tuần tự. Bốn khu vực có chức năng khác nhau; học sinh được chọn điểm vào theo nhu cầu, mức chuẩn bị và bằng chứng hiện có. Ôn nền, Lời giải, Sửa lỗi, Nhật kí là hỗ trợ độc lập theo ngữ cảnh. Trong một lượt Kiểm tra phải tự lực; muốn nhận trợ giúp thì kết thúc lượt và giữ riêng bài làm ban đầu. Lưu bằng chứng ở Điểm dừng khác ghi Nhật kí, không bắt ghi ở mọi Điểm dừng. Chỉ yêu cầu liên kết quay lại đề khi cặp đề–lời giải thực sự tách vị trí. Không tái áp dụng quy tắc đã bị thay.
- Chủ sở hữu: 01/2.2–2.4 giữ nghĩa học tập; 07/2, 3, 5.3–5.4 giữ yêu cầu trang; 02/1.2 giữ cơ chế thay thế/kiểm. 03 ghi trạng thái và bước tiếp; 08/README trỏ đúng thẩm quyền. Hợp đồng QMD, registry và guard chỉ đồng bộ phần hiện thực chịu ảnh hưởng.
- Phần bị thay: cách hiểu “quan hệ tổ chức bắt buộc” trong QD_021 là bắt hoàn thành bốn khu vực tuần tự; quy định sáu việc theo thứ tự và ghi kết quả bị hiểu thành nghi thức Nhật kí ở mọi Điểm dừng; yêu cầu quay lại đề vô điều kiện còn ở 07/5.3 và hợp đồng QMD; mô tả Nhật kí có thể thuộc Ôn lại trong hợp đồng QMD. QD_021 được thay bằng QD_033 ở chủ đề `learning_route`; giữ nguyên ma trận DH01–DH14 và phần không mâu thuẫn. QD_024/025/028–032 cùng schema/ID/14 trường không bị thay toàn bộ.
- Đính chính con trỏ lịch sử, không sửa mục cũ: dòng QD_031 dẫn “01/2.9” về Nhật kí phải tra 01/2.8, phần Hệ nhãn và 07/3; 01/2.9 là căn cứ khoa học. Mục QD_031 giữ nguyên để truy nguyên.
- Chống hồi quy: cập nhật quyết định `learning_route` trong registry, kiểm cả tiến trình chuẩn được khuyến nghị lẫn tính không cưỡng chế tuần tự; báo cáo theo QD_021 không chứng nhận QD_033. G01/G02 chưa được đối chiếu lại ở cấp QMD/HTML với quy tắc mới nên chưa xác định có nội dung nào cần sửa; không đổi metadata thành đã áp dụng. Các QA khác chỉ dùng lại sau xác minh đúng đầu vào/phép kiểm theo QD_022.
- Ranh giới lượt DH_029: chỉ tài liệu/hợp đồng/guard điều hành tối thiểu. Không sửa Nhà/D0/G01/G02, QMD học liệu, HTML/CSS/tài sản/PDF/bản xem audit; không dọn repo, G03, stage/commit/push hoặc xuất bản. Dừng để chủ trì duyệt trước bước bảo toàn bốn trang.
- Xác nhận tiếp nối ngày 12/10/2026: chủ trì trả lời “Mình duyệt” sau báo cáo DH_029, rồi giao thực hiện bước bảo toàn bốn trang. **Bản khép bộ điều hành QD_033 đã được duyệt**; trạng thái chờ duyệt ở dòng ghi nhận ban đầu phía trên là lịch sử. Việc duyệt này không chứng nhận nguồn G01/G02 đã áp dụng QD_033, không nghiệm thu HTML/PDF mới và không cấp quyền dọn repo hoặc thao tác Git/phát hành. Bảo toàn kỹ thuật ghi tại 03/DH_030, không tạo một quyết định kiến trúc mới.
- Làm rõ của chủ trì ngày 12/10/2026: “không bắt buộc tuần tự” không phủ định tiến trình chuẩn. Bài học → Luyện tập → Kiểm tra → Ôn lại vẫn là tiến trình chuẩn được khuyến nghị. Cụm “chờ rà nguồn” được hiểu chính xác là QMD/HTML chưa được đối chiếu lại với QD_033 và chưa xác định có nội dung nào cần sửa; không phải một lỗi sản phẩm đã được phát hiện.

## QD_032 — Điều hướng toàn khóa học bằng ba icon

- Ngày: 12/10/2026; trạng thái: **chủ trì duyệt mẫu V4 và giao triển khai bốn trang**, HTML cải tạo chờ xem lại.
- Phạm vi: Nhà, D0, R1-G01, R1-G02. Nhà → Danh sách toàn khóa học → Đầu trang; giữ logo và nhóm chọn nền/sắc xám. Danh sách đích mặc định đóng, liên kết thật, chỉ rõ trang hiện tại; bỏ “Đi tới”, tên khóa học trên thanh và hàng đích thường trực.
- Chủ sở hữu quy tắc: 07; hiện thực: module `zo_web_2027_navigation.py` và CSS/JS riêng của kit, được bốn adapter gọi sau khi dựng nội dung. Gateway nằm ngoài lượt này. Không sao chép bản mẫu audit thành phụ thuộc sản xuất.
- Thay thế cách điều hướng toolbar cũ trong đúng bốn trang; không thay kiến trúc học tập, nội dung, ID, logo, footer hoặc phân cấp tiêu đề chưa duyệt. Không PDF học liệu, promotion docs, Git hoặc phát hành.
- Kiểm chống tái diễn: guard kiểm ba điều khiển đúng thứ tự, bốn đích, trang hiện tại, trạng thái đóng, bảo toàn main/rail/footer/logo; browser kiểm responsive, bàn phím, chuyển trang và trở về đầu không mất ngữ cảnh. Hồ sơ DH_027: `_audit/zo_course_navigation_2026-10-12/`.

## QD_026 — Nhà khóa học dùng bộ khung canonical chung


- Ngày: 11/10/2026; trạng thái: **chủ trì giao triển khai**, chưa nghiệm thu HTML mới.
- Bằng chứng: yêu cầu dựng lại Nhà sau G02 theo ngôn ngữ thiết kế G01/G02, bao gồm đồng bộ mã nguồn.
- Phạm vi: QMD/data/partial Nhà, map riêng và adapter/checker; dùng shell/font/token/giấy/footer chung, không copy kiến trúc hoặc số vùng/nhiệm vụ R1. Danh mục một nguồn; `preview` chỉ là khả năng xem ứng viên, không đổi nghiệm thu/profile gói.
- Thay thế: giới hạn kỹ thuật Nhà chỉ preview và lớp pilot cũ trong đúng trang Nhà; không thay QD_021–025, thiết kế 9/10, lịch sử nghiệm thu, D0/G01/G02 riêng hoặc Design 0.4 khóa.
- Điều hành/bằng chứng: DH_017 ở 03 và README vận hành Nhà. Chỉ thị này không cho phép PDF, promotion docs, Git hay phát hành.

## QD_031 — Khép lỗi hành động cục bộ, bảng Sửa lỗi, thứ tự Toàn văn và provenance hình G02

- Ngày: 11/10/2026; chủ trì duyệt kế hoạch và giao thực hiện trong phiên hiện tại; chưa nghiệm thu HTML mới.
- Phạm vi: nguồn G01/G02, include Nền/Nhật kí, binding, kit/controller, bộ dựng/guard và tài liệu điều hành liên quan. Không đổi toán/ID, schema Nhật kí, thiết kế đã duyệt hoặc học lộ trình chính.
- Quy tắc hiện hành tại 01/2.9 và 07/3: Nhật kí độc lập, các phần ngang cấp không sáp nhập; Sửa lỗi/đáp án đúng owner/thứ tự; số và dẫn chiếu đồng bộ; bỏ hành động dẫn trùng khi đề–đáp án cùng vùng. Bảng chọn cùng mẫu theo vai trò, viết hoa đầu câu/ô.
- Hình G02: dựng đủ hai hình chính, hai hình Nền và bìa từ TeX/profile 0.4; khóa nguồn/style/font/palette/khung và hash đầu ra, không tin cache chỉ có provenance bìa. Giữ dữ kiện toán, bìa trong suốt và khung tách riêng; không thay profile mặc định v0.2 hoặc tài sản Design khóa.
- Thay thế: phần mô tả Nhật kí còn nằm trong Ôn lại và yêu cầu link hai chiều vô điều kiện của các đơn vị đề–đáp án cục bộ. Không thay QD_021/024/025/028/029/030 hoặc quy chuẩn dấu ngoặc LaTeX; lịch sử/receipt không sửa.
- Hồ sơ hiện hành: DH_026 ở 03, `_audit/zo_pair_backlog_2026-10-11/`. Không quyền PDF học liệu, promotion docs, Git hay phát hành.

## Quy tắc ghi

Mỗi quyết định gồm ID, ngày, vấn đề, nội dung, trạng thái, người chốt/bằng chứng, tệp/gói chịu ảnh hưởng và điều gì bị thay thế. Chỉ dùng “đã chốt” khi có chỉ thị hoặc xác nhận thực; đề xuất của AI không tự thành quyết định được duyệt.

Khi đảo một quyết định, giữ mục cũ, ghi “được thay bằng QD_xxx” và thêm mục mới. Không sửa lịch sử để trông như chưa từng có thay đổi. Đánh số tiếp tục từ ID lớn nhất; không cần một mục mới cho mỗi lỗi chính tả.

QD_001–015 bên dưới giữ trạng thái tại lúc ghi. QD_016–018 bổ sung chuỗi mới: phần **hình thức** ngang/thu gọn QD_007–009 đã được kit rail/drawer thay; các bất biến phân nhóm/không giật/ngữ cảnh vẫn giữ. QD_015 là receipt lịch sử FB033, không nghiệm thu FB036. Công việc sau cùng chỉ ở bảng 03.

## QD_001 — Biên tập một bộ Markdown điều hành trong repo

- Ngày: 06/10/2026.
- Trạng thái: **đã được người chủ trì yêu cầu**.
- Bằng chứng: yêu cầu “biên tập bộ Markdown”, kèm cách dùng, quản lý và cập nhật cho Codex/Copilot trong VS Code.
- Nội dung: một điểm vào, chuẩn chung, quy trình, bảng điều hành, nhật kí, hướng dẫn và hồ sơ từng gói; giữ Kế hoạch 0.6.
- Phạm vi: tạo bộ bàn giao. Chưa đồng nghĩa đã nhập vào repo hay đã duyệt mọi sửa đổi G01.
- Ảnh hưởng: toàn bộ gốc điều hành `tot_nghiep_thpt/2027/_quy_trinh/`.

## QD_002 — Các bổ sung kiến trúc và nội dung ngày 06/10

- Ngày: 06/10/2026.
- Trạng thái: **đề xuất đã biên tập; chờ đối chiếu và chốt phạm vi triển khai**.
- Nội dung: hoàn thiện đường học, Nền, bằng chứng mới, ngữ cảnh quay về; sửa các nhiệm vụ G01 được liệt kê trong hồ sơ.
- Căn cứ: nghiên cứu nguồn đính kèm và bản PDF ngày 06/10; phần đối chiếu tại tệp 06.
- Ảnh hưởng: tệp 01, 02 và hồ sơ G01; G02 áp dụng quy tắc chung sau khi được kiểm chứng.
- Điều không được suy ra: chưa nghiệm thu HTML, chưa xác nhận trạng thái repo hoặc hiệu quả trên người học.
- Trạng thái kế tiếp: phần được triển khai đã được chốt cụ thể bởi `QD_003` và `QD_004`; không dùng lại trạng thái “chờ chốt phạm vi” của mục này.

## QD_003 — Chốt phạm vi triển khai HTML R1-G01 và cách đếm

- Ngày: 06/10/2026.
- Trạng thái: **đã chốt để triển khai; HTML đang chờ người chủ trì duyệt**.
- Vấn đề và bằng chứng: báo cáo `_audit/r1_g01_doi_chieu_2026-10-06.md` phát hiện mâu thuẫn giữa hồ sơ, repo và fork giao diện cục bộ; người chủ trì sau đó chỉ thị triển khai Cụm 0 và A–C đến bước trình duyệt HTML.
- Nội dung quyết định: giữ Nhật kí 14 trường, hợp đồng tám PDF, ba chặng, ba tầng sửa lỗi, ba bài Ôn lại và tuyến S-K đúng họ lỗi; đưa phần hợp lệ của fork về component canonical dùng chung; triển khai các thay đổi O01/O02/L08/S-O và gián đoạn đã nêu; tạo bảy nguồn N canonical dùng chung; giữ ngữ cảnh quay về bằng URL theo từng tab.
- Cách đếm: giữ 42 nhiệm vụ quản lý. `G01-L08-XN01` là câu xác nhận con của L08; bảy tài nguyên N không thuộc manifest nhiệm vụ G01; nhánh Phối hợp sau G02 của O02 dùng lại dữ kiện và nhiệm vụ O02. Không mặc định tổng mới là 43.
- Vị trí kho N: `content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nen/`; mỗi tài nguyên có một nguồn, các gói include lại nguồn ấy.
- Người chốt hoặc chỉ thị làm căn cứ: người chủ trì ZO Math, chỉ thị triển khai R1-G01 ngày 06/10/2026.
- Tệp và gói chịu ảnh hưởng: R1-G01; component HTML/CSS dùng chung; hồi quy R1-G02; tệp 00, 01, 03, 04 và hồ sơ G01.
- Thay thế: chốt phần còn ở trạng thái đề xuất trong `QD_002`; thay nhận định sáu trường, chín PDF và khả năng tổng nhiệm vụ phải tăng.
- Giới hạn: chưa phải nghiệm thu HTML; chưa cho phép dựng lại tám PDF, cập nhật số trang, commit, push hoặc phát hành.

## QD_004 — Chốt quy tắc trình bày người học sau phản hồi HTML R1-G01

- Ngày: 06/10/2026.
- Trạng thái: **đã được người chủ trì yêu cầu triển khai; HTML sửa lại vẫn chờ duyệt**.
- Vấn đề và bằng chứng: chín ảnh phản hồi HTML cho thấy hướng dẫn đầu gói mở sẵn, bảng mất quy cách, mã quản lí lọt vào văn bản, một ảnh bảng biến thiên không tải, tiêu đề bị lặp, tên trường Nhật kí bị tự đổi và nhóm lời giải nằm ngoài hộp.
- Nội dung quyết định: văn bản người học dùng tên chính thức thay mã quản lí; bảng có liên kết vẫn theo hợp đồng bảng canonical; `guidance` mặc định đóng; tên 14 trường Nhật kí chép đúng đặc tả chung; mọi lời giải tách khỏi đề nằm trong `solution`; ảnh bảng biến thiên phải tải được và alt không mang mã kỹ thuật; không lặp nguyên văn tiêu đề ngay bên dưới.
- Nguồn chống tái diễn: `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/quy_chuan_goi_qmd.md` và checker của gói R1-G01.
- Bằng chứng thực hiện: checker G01 trên HTML vừa dựng `passed: true`; browser QA đạt 54/54, gồm ảnh bảng biến thiên, hai bảng liên kết, 14 tên trường Nhật kí, mã quản lí trong văn bản người học và quan hệ đề–hộp lời giải.
- Người chốt hoặc chỉ thị làm căn cứ: người chủ trì ZO Math, phản hồi HTML ngày 06/10/2026.
- Tệp và gói chịu ảnh hưởng: R1-G01; component bảng và tích hợp bảng biến thiên dùng chung; hồi quy R1-G02; tệp 01, 03, 04 và hồ sơ G01.
- Giới hạn: không thay mục tiêu toán học, không dựng tám PDF học liệu, không commit, push hoặc phát hành.

## QD_005 — Hợp nhất điều hành khóa 2027 về một gốc

- Ngày: 07/10/2026.
- Trạng thái: **đã được người chủ trì duyệt triển khai**.
- Vấn đề và bằng chứng: tài liệu có cùng nguồn gốc 2027 bị đặt ở `on_thi_toan_thpt/_quy_trinh/` và trong lớp lồng `2027/_quy_trinh/dieu_hanh/dieu_hanh_2027/`, tạo hai cấp điều hành và hai điểm vào cạnh tranh. Bộ 12 tệp Markdown “Ôn thi Toán THPT 2027 — Tháo gỡ hệ thống sản xuất và xuất bản” xác nhận Kế hoạch 0.6 là nguồn điều hành của dòng tài liệu này.
- Nội dung quyết định: gốc duy nhất là `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/`; `README.md` là điểm vào; `03_dieu_hanh_chuong_trinh.md` là bảng việc hiện hành; hồ sơ gói điều hành đặt tại `goi/`. Không duy trì lớp `dieu_hanh/dieu_hanh_2027` hoặc `_quy_trinh` song song ở cấp `on_thi_toan_thpt`.
- Ranh giới không trùng lặp: `_quy_trinh` trong `hoc_lieu/<ma_goi>/` tiếp tục giữ cấu hình, manifest, provenance và lịch sử riêng của gói; không phải bảng điều hành khóa.
- Tệp được thay thế: `00_bat_dau_o_day.md` được nhập vào README; `mau_ho_so_san_xuat.yml` trạng thái `design_only` được thay bằng `mau/ho_so_goi.md`; đặc tả 0.2 và ma trận 0.1 cũ tiếp tục được truy nguyên qua Git và bộ nguồn Downloads, không phục hồi thành chuẩn song song.
- Phụ thuộc phải cập nhật: `AGENTS.md` cục bộ, `scripts/zo_learning_architecture.py`, checker R1-G01/R1-G02, manifest D0, đặc tả vận hành D0 và các liên kết nội bộ.
- Giới hạn: không sửa học liệu, không dựng HTML/PDF, không commit, push hoặc phát hành; không xóa hay di chuyển bộ nguồn trong Downloads.
- Người chốt hoặc chỉ thị làm căn cứ: người chủ trì ZO Math, chỉ thị ngày 07/10/2026.

## QD_006 — Hợp nhất phần còn hiệu lực từ bộ nguồn tháo gỡ

- Ngày: 07/10/2026.
- Trạng thái: **đã được người chủ trì yêu cầu thực hiện**.
- Vấn đề và bằng chứng: 12 tệp Markdown trong thư mục “Ôn thi Toán THPT 2027 — Tháo gỡ hệ thống sản xuất và xuất bản” chứa lẫn kiến trúc, ma trận, nội dung gói, prompt theo commit và đặc tả giao diện; một số phần tiên tiến chưa có đích canonical rõ, trong khi một số quyết định đã bị chỉ thị ngày 06–07/10 thay thế.
- Nội dung quyết định: đối chiếu từng tệp theo nội dung và thẩm quyền; đưa cấu trúc trang còn hiệu lực vào `07_quy_chuan_cau_truc_trang_nguoi_hoc.md`; bổ sung quy trình nhập nguồn vào tệp 02; giữ nội dung toán ở hồ sơ/nguồn gói thay vì chép lại; ghi sổ 12 nguồn cùng SHA-256 ở tệp 06.
- Phần kế thừa: bốn lớp cần tách; mạch chính và lớp hỗ trợ; thứ tự QMD/DOM trước JavaScript; bảng theo vai trò; một nhiệm vụ–một lời giải; liên kết sâu và ngữ cảnh quay về; nghiệm thu responsive/keyboard/no-JS; cổng khóa PDF; phân biệt kiểm tự động, chấp nhận và phát hành.
- Phần bị thay thế: giao diện Nhật kí sáu trường được thay bằng schema 14 trường theo `QD_003`; yêu cầu mở sẵn “Cách thực hiện” ở Câu hỏi khởi động được thay bằng quy tắc `guidance` mặc định đóng theo `QD_004`; các prompt Pha 2/Pha 3 và “việc tiếp theo” trong Nhật kí không còn cấp quyền commit, dựng PDF hoặc buộc repo quay về commit nền cũ.
- Phần chỉ lưu lịch sử: số lượng và trạng thái `planned` tại từng pha, điều kiện worktree sạch tuyệt đối, commit dự kiến, lệnh commit và thứ tự công việc đã hoàn tất.
- Trạng thái sản phẩm: người chủ trì đã đọc HTML R1-G01 nhưng chưa nghiệm thu vì còn một điểm cần làm rõ; việc hợp nhất tài liệu không tự thay đổi HTML, PDF hoặc trạng thái này.
- Giới hạn: không sửa học liệu, component, script, checker hoặc cấu hình; không dựng HTML/PDF; không xóa, di chuyển hay sửa 12 tệp Downloads; không commit, push hoặc phát hành.
- Người chốt hoặc chỉ thị làm căn cứ: người chủ trì ZO Math, yêu cầu ngày 07/10/2026.
- Tệp và gói chịu ảnh hưởng: bộ điều hành 2027; trạng thái R1-G01 chỉ được làm rõ, không được nâng nghiệm thu.

## QD_007 — Chốt ba nhóm điều hướng trên trang người học

- Ngày: 07/10/2026.
- Trạng thái: **đã được người chủ trì yêu cầu triển khai; HTML sửa lại vẫn chờ duyệt**.
- Vấn đề và bằng chứng: ảnh phản hồi cho thấy bảng điều khiển đang dàn Mạch học chính, Hỗ trợ khi cần và Tiện ích thành một hàng thẻ phẳng; vai trò bị lẫn và Sửa lỗi đứng trước Ôn lại. Người chủ trì xác nhận Ôn lại thuộc mạch chính và phải đứng ngay sau Kiểm tra; ba vai trò phải được chia thành ba nhóm dù không dùng thiết kế thanh dọc của ảnh tham chiếu.
- Nội dung quyết định: nhóm Mạch học chính gồm Bắt đầu/Cách học, Bài học, Luyện tập, Kiểm tra, Ôn lại; nhóm Hỗ trợ khi cần gồm Ôn nền, Sửa lỗi, Nhật kí, Lời giải; nhóm Tiện ích gồm Tải PDF, Nguồn, Toàn văn. Desktop dùng ba vùng có nhãn trong bảng điều khiển ngang; mobile xếp ba nhóm thành các hàng/khối ngang và cho mục tự xuống dòng, không che Ôn lại và không biến thành thanh dọc.
- Bằng chứng thực hiện: component canonical dùng chung đã cập nhật; G01 và G02 dựng lại; browser QA trên HTML vừa dựng đạt ở 1440/430/390, click/Back/reload/truy cập trực tiếp; G02 chỉ hiện các mục thực có. Ảnh và JSON nằm tại `_audit/r1_g01_nav_groups_2026-10-07/`.
- Người chốt hoặc chỉ thị làm căn cứ: người chủ trì ZO Math, phản hồi HTML ngày 07/10/2026.
- Tệp và gói chịu ảnh hưởng: quy chuẩn trang, component HTML/CSS dùng chung, checker R1-G01/R1-G02, hồ sơ và bảng điều hành R1-G01.
- Giới hạn: đây là sửa cấu trúc điều hướng, không phải nghiệm thu HTML; không mở pha PDF, commit, push hoặc phát hành.

## QD_008 — Giữ điều hướng khi cuộn và tách view Ôn lại/Nhật kí

- Ngày: 07/10/2026.
- Trạng thái: **đã được người chủ trì yêu cầu triển khai; HTML sửa lại vẫn chờ duyệt**.
- Vấn đề và bằng chứng: người chủ trì kiểm HTML R1-G01 và xác nhận hai lỗi: thanh điều hướng biến mất khi cuộn; hai thẻ Ôn lại và Nhật kí cùng hiển thị vùng Ôn lại nên trộn hai vai trò. Hai lỗi có nguồn từ component dùng chung nên có nguy cơ lặp ở gói khác.
- Nội dung quyết định: giữ bảng ba nhóm đầy đủ ở đầu trang; sau khi nó rời viewport, dùng chính bảng ấy ở trạng thái thu gọn sticky một dòng, cuộn ngang cục bộ nếu cần. Mỗi lối vào sâu là một view riêng: view cha ẩn đích hỗ trợ con, view sâu chỉ hiện nhánh đích, `Toàn văn` mới khôi phục toàn bộ cây canonical.
- Hàng rào chống tái diễn: checker G01/G02 khóa sentinel, trạng thái sticky và hàm cô lập view sâu; browser QA phải cuộn view dài trên desktop/mobile, kiểm không tràn ngang cấp trang, rồi kiểm riêng Ôn lại/Nhật kí qua click, Back, tải lại và hồi quy G02.
- Bằng chứng thực hiện: HTML G01/G02 đã dựng lại; 35/35 phép kiểm trình duyệt đạt; checker G01, checker component G02 và `zo_qmd.py check` đạt. JSON và ảnh nằm tại `_audit/r1_g01_two_ui_fixes_2026-10-07/`.
- Người chốt hoặc chỉ thị làm căn cứ: người chủ trì ZO Math, yêu cầu ngày 07/10/2026.
- Tệp và gói chịu ảnh hưởng: component HTML/CSS dùng chung, checker R1-G01/R1-G02, quy chuẩn trang, quy chuẩn QMD, hồ sơ và bảng điều hành R1-G01.
- Giới hạn: không phải nghiệm thu HTML; không dựng lại tám PDF học liệu, không cập nhật metadata số trang, commit, push hoặc phát hành.

## QD_009 — Ngăn giật màn hình khi thanh điều hướng thu gọn

- Ngày: 07/10/2026.
- Trạng thái: **đã được người chủ trì yêu cầu xử lí; HTML sửa lại vẫn chờ duyệt**.
- Vấn đề và bằng chứng: người chủ trì phát hiện navbar giật khi cuộn ở một số thẻ. Đo theo từng bước cuộn cho thấy lần chuyển trạng thái làm thay đổi dấu chân bố cục; trên mobile, phần tử bao ngoài còn tràn ngang 759 px trong viewport 390 px, làm chiều rộng layout đổi và vị trí cuộn bị kéo về đầu trang.
- Nội dung quyết định: component canonical phải giữ dấu chân của thanh đầy đủ bằng spacer; trang gói học liệu loại vùng động khỏi scroll anchoring; lớp bao ngoài chặn tràn ngang còn dải thẻ giữ cuộn ngang cục bộ. Không dùng vòng `scrollTo` để cưỡng ép vị trí cuộn.
- Hàng rào chống tái diễn: checker G01/G02 khóa spacer, phép đo dấu chân, `overflow-anchor: none` ở cấp trang gói và `overflow-x: clip` ở lớp bao ngoài. Browser QA phải đo mọi view ở desktop 1440 px và mobile 390 px, yêu cầu mỗi view đủ dài chỉ chuyển một lần, không có bước lùi, sai số vị trí cuộn tối đa 1 px và chiều rộng cấp trang không đổi.
- Bằng chứng thực hiện: G01 đạt trên 12/12 view ở 1440 và 390 px; G02 đạt trên 10/10 view ở hai kích thước, sai số vị trí cuộn lớn nhất 0 px. Dữ liệu nằm tại `_audit/r1_g01_nav_jitter_2026-10-07/`.
- Người chốt hoặc chỉ thị làm căn cứ: người chủ trì ZO Math, phản hồi HTML ngày 07/10/2026.
- Tệp và gói chịu ảnh hưởng: component HTML/CSS dùng chung, checker R1-G01/R1-G02, quy chuẩn trang, quy chuẩn QMD, hồ sơ và bảng điều hành R1-G01.
- Giới hạn: không phải nghiệm thu HTML; không dựng lại tám PDF học liệu, không cập nhật metadata số trang, commit, push hoặc phát hành.

## QD_010 — Mở pha tích hợp thử nghiệm ZO Math 0.4 và giữ phản hồi cho 0.5

- Ngày: 07/10/2026.
- Trạng thái: **đã được người chủ trì duyệt và yêu cầu thiết lập mốc**.
- Vấn đề và bằng chứng: mẫu thiết kế 0.4 đã hoàn thành ở cấp bộ bàn giao nhưng chưa phải 1.0 và chưa được tích hợp vào repo. Người chủ trì muốn quan sát sản phẩm thật, tinh chỉnh dần và dùng các phản hồi đã kiểm chứng làm đầu vào nâng 0.4 lên 0.5 sau khi các trang hiện có được chấp nhận và xuất bản.
- Nội dung quyết định: mở một pha tích hợp có kiểm soát; dùng trang Nhà khóa 2027 và R1-G01 làm pilot, sau đó mới mở rộng sang R1-G02 và D0. Giữ nguyên nội dung toán, ID và luồng học nếu không có nhiệm vụ riêng. Tạm hoãn đồng bộ PDF cho đến khi lớp web 0.4 ổn định và có quyết định mở pha PDF.
- Cơ chế phản hồi: nguồn canonical là `_design/ngon_ngu_thiet_ke_zo_math_0_4/09_nhat_ki/phan_hoi_tich_hop_web_2027_0_4.md`. Mỗi phản hồi giữ lời gốc, bối cảnh/SHA HTML, phân loại, kết quả xác minh, nguồn sửa, hàng rào chống tái diễn, bằng chứng kiểm, trạng thái duyệt và kết luận đề cử 0.5. Phản hồi chưa được người chủ trì duyệt không tự trở thành quy chuẩn hoặc đầu vào chính thức cho 0.5.
- Mốc đối chiếu: `_audit/zo_design_0_4_web_2027_baseline_2026-10-07.md`.
- Hàng rào an toàn: loại `_design/**` khỏi render Quarto; không đưa bộ bàn giao vào resources/publication; bảo toàn diff có sẵn; không chép nguyên mẫu CSS/JS vào lớp toàn cục.
- Người chốt hoặc chỉ thị làm căn cứ: người chủ trì ZO Math, duyệt đề xuất và yêu cầu thiết lập mốc thử nghiệm ngày 07/10/2026.
- Tệp và gói chịu ảnh hưởng: điều hành thiết kế 0.4, điều hành khóa 2027, trang Nhà 2027, R1-G01; R1-G02 và D0 là phạm vi mở rộng sau pilot.
- Giới hạn: thiết lập mốc chưa phải áp dụng thị giác 0.4, chưa nghiệm thu HTML/PDF, chưa commit, push hoặc phát hành.

## QD_011 — Sửa lỗi đóng gói và nâng bộ bàn giao lên 0.4.2

- Ngày: 07/10/2026.
- Trạng thái: **đã được người chủ trì duyệt thực hiện**.
- Vấn đề và bằng chứng: `DESIGN04-INTEGRITY-001` cho thấy `00_BAT_DAU_O_DAY.md` trong thư mục và ZIP 0.4.1 khớp nhau nhưng mục tương ứng trong manifest 0.4.1 dùng kích thước/hash khác; checker vì vậy báo một lỗi toàn vẹn.
- Nội dung quyết định: lấy tệp thực và ZIP 0.4.1 đã đối chiếu làm căn cứ cho lỗi đóng gói; tăng riêng phiên bản bộ bàn giao lên 0.4.2, giữ mẫu thiết kế ở 0.4; cập nhật tài liệu phiên bản, báo cáo và manifest, không thay quy tắc hoặc tài sản thiết kế để đạt kiểm. Giữ ZIP 0.4.1 làm bản trước và tạo ZIP 0.4.2 riêng.
- Bằng chứng kiểm: `zo_design.py check` đạt 1812/1812; sáu ca kiểm `test_zo_design.py` đạt trên Windows; trạng thái công việc nhận package 0.4.2 và specimen 0.4. ZIP `_design/ngon_ngu_thiet_ke_zo_math_0_4_2.zip` có SHA-256 `00006c84264de3c8f4dadf5678058999603af1a9c315a8c803a06753ab589b73`; 612/612 thành viên khớp cây nguồn.
- Người chốt hoặc chỉ thị làm căn cứ: người chủ trì ZO Math, xác nhận “OK. Hãy thực hiện bước tiếp theo.” ngày 07/10/2026.
- Tệp và gói chịu ảnh hưởng: bộ bàn giao thiết kế, manifest, báo cáo kiểm, nhật kí thiết kế và điều hành khóa 2027.
- Giới hạn: đây là bản vá hồ sơ bàn giao, chưa tích hợp thị giác 0.4 vào trang pilot, chưa render học liệu, commit, push hoặc phát hành website.

## QD_012 — Dùng gốc thiết kế đã đổi tên và trình duyệt pilot 0.4

- Ngày: 07/10/2026.
- Trạng thái: **đã được người chủ trì yêu cầu thực hiện; kết quả HTML chờ duyệt**.
- Vấn đề và bằng chứng: người chủ trì xác nhận thư mục làm việc đã đổi từ `_design/zo_math_0_4` thành `_design/ngon_ngu_thiet_ke_zo_math_0_4` và duyệt triển khai đề xuất pilot. Hai bề mặt cần thử là trang Nhà khóa 2027 và R1-G01; baseline chức năng không được thay đổi chỉ để áp thị giác.
- Nội dung quyết định: lấy `_design/ngon_ngu_thiet_ke_zo_math_0_4/` làm gốc canonical hiện hành; tích hợp token/component 0.4 qua một lớp CSS và một bộ điều khiển dùng chung, giới hạn bằng body class trên hai bề mặt pilot. Giữ nguyên nội dung toán, ID và luồng học; điều khiển sáu nền/thang xám là tăng cường lũy tiến và không được làm mất bề mặt đọc khi JavaScript tắt.
- Đường dẫn cũ trong gói phát hành: bộ bàn giao 0.4.2 đã khóa còn ghi `_design/zo_math_0_4` như vị trí cài đặt đề xuất. Không sửa ngược manifest/ZIP 0.4.2 trong lượt tích hợp; nếu muốn phát hành lại tài liệu cài đặt phải mở bản vá bộ bàn giao riêng và tái kiểm toàn vẹn.
- Bằng chứng kiểm: trang Nhà và G01 đã dựng lại; browser QA 59/59 ở 1440/430/390, bàn phím, no-JS, sáu nền, thang xám và phân tách view; trace G01 ở 1440/430/390 và HTML G02 cũ ở 1440/390 không có bước cuộn ngược, sai số cuộn hoặc dao động vị trí sau khi thu gọn. Kết quả tại `_audit/zo_design_0_4_pilot_2026-10-07/` và `_audit/zo_design_0_4_pilot_preflight_2026-10-07.md`.
- Hàng rào chống tái diễn: `07_quy_chuan_cau_truc_trang_nguoi_hoc.md` yêu cầu bề mặt đọc no-JS và một nguồn canonical cho bộ điều khiển; sổ phản hồi 0.4 phải nhận lời người chủ trì trước khi sửa hoặc đề cử cho 0.5.
- Người chốt hoặc chỉ thị làm căn cứ: người chủ trì ZO Math, yêu cầu triển khai ngay và xác nhận tên thư mục ngày 07/10/2026.
- Tệp và gói chịu ảnh hưởng: trang Nhà 2027, R1-G01, hai tài sản tích hợp 0.4 dùng chung, hồ sơ/điều hành khóa 2027 và nhật kí thiết kế. R1-G02 chỉ được kiểm hồi quy trên HTML cũ; D0 chưa mở.
- Giới hạn: PASS kỹ thuật không phải nghiệm thu; chưa dựng PDF, cập nhật metadata số trang, commit, push hoặc phát hành.

## QD_013 — Ưu tiên mẫu khung bìa và hình/bảng trước khi mở việc G02

- Ngày: 08/10/2026.
- Trạng thái: kế hoạch được chủ trì duyệt; mẫu HTML đã dựng, chờ duyệt thị giác.
- Căn cứ: sau đồng bộ nguồn G01 (DH_004), chủ trì yêu cầu ảnh toán trên bìa
  trong suốt, ba dạng khung × hai cỡ, sáu nền sáng/tối Đỏ/Vàng/Xám ZO,
  đồ thị/bảng 0.4 và định nghĩa vùng chèn hình; sau đó giao bắt đầu kế hoạch.
- Quyết định: mở DH_005 làm việc hiện hành. Dựng mẫu riêng ở audit trước,
  không đổi G01 production cho tới khi chủ trì xem mẫu. Profile/tool mới
  phải opt-in, giữ tương thích v0.2 và dữ liệu toán/ID/luồng canonical.
- Nguồn và bằng chứng: WEB04-FB-030; profile dưới
  `_design/web_2027_mau_dung_chung/figure-profile-candidate/`; mẫu/QA tại
  `_audit/zo_math_figure_profile_2026-10-08/`.
- Không thay thế nghiệm thu thiết kế G01 9/10, Nhà/footer/FB027; không đóng
  khoảng cách kiến trúc G02 bằng kết quả mẫu hình. G02 tiếp tục để sau bước
  hình được giao. Không tiếp tục Video/M8.R hoặc thay phần đang làm ở repo khác.
- Giới hạn: chờ chủ trì duyệt HTML; chưa nối QMD/áp dụng mới production,
  dựng PDF học liệu, commit/push/phát hành hoặc khóa Design 0.5.

## QD_014 — Duyệt mẫu FB030; tích hợp payload hình vào HTML G01

- Ngày: 08/10/2026. Căn cứ: chủ trì “Mình duyệt bảng thiết kế này”, sau đó
  giao “OK. Hãy bắt đầu thực hiện bước này”.
- Mẫu HTML riêng được duyệt là bộ hình/bảng/khung, không thay khung giao diện
  G01 9/10. Tiếp tục DH_005 bằng source adapter và HTML G01 toàn trang.
- Giữ QMD toán/ID/luồng, 154 vùng đọc, controller, footer và CSS shell.
  SVG web nằm riêng; bảng native lấy JSON canonical, caption QMD giữ nguyên.
- Bằng chứng/lỗi/guard: WEB04-FB-031 và
  `_audit/zo_g01_figure_integration_2026-10-08/README.md`.
- Kiểm kỹ thuật không thay duyệt HTML tích hợp mới. Không dựng PDF học liệu,
  chuyển G02, tiếp tục M8.R, commit/push/phát hành hoặc khóa Design 0.5.

## QD_015 — Chốt HTML G01 FB032 và bảo vệ đường dựng nguồn

- Ngày: 08/10/2026. Trạng thái: đã chốt HTML; không là duyệt PDF/phát hành/0.5.
- Căn cứ chủ trì: “Mình đã xem kết quả, tốt.”; giao thực hiện bốn điểm đóng mốc, hợp đồng, guard chính thức, dựng đối chiếu.
- Mốc: receipt `hoc_lieu/r1_g01/giao_dien/web_2027_accepted.json`, SHA HTML `8b3a9a1ad532e72951edb415d9ab32a37990a80e13c2d754a2f57028fedc764a`.
- Không thay QMD, toán, ID, luồng, runtime đã duyệt; không lấy HTML audit làm nguồn dựng. Checker không tự cấp duyệt hoặc cập nhật baseline khi FAIL.
- Nguồn công cụ: `scripts/zo_web_2027_g01_checkpoint.py`; hợp đồng và hướng dẫn tại `_design/web_2027_mau_dung_chung/`.
- Bằng chứng: `_audit/zo_g01_html_checkpoint_2026-10-08/README.md`. DH_006 thay trạng thái chờ xem của DH_005; giữ lịch sử cũ.
- G02 hoàn thiện kiến trúc/nội dung là đề xuất nhiệm vụ tiếp; chưa có thay đổi G02, PDF, Git hoặc phát hành trong lượt này.

## QD_016 — Nhận nguồn và trạng thái liên gói FB034–036

- Ngày ghi: 10/10/2026; các lượt triển khai FB034–036 được ghi ngày 08/10/2026 trong sổ phản hồi.
- Căn cứ: chủ trì giao hoàn thiện G02, tiếp tục tinh chỉnh nguồn do còn lệch vai trò; rồi yêu cầu sửa cả G01/G02 theo 17 lỗi và tạo checkpoint FB036, sau đó đã yêu cầu tiếp tục.
- Quyết định: giữ QMD canonical, một nguồn Nhật kí 14 trường; cùng vai trò/cấp/vùng và mẫu bảng, không copy toán/số vùng. Header bảng thường/Nhật kí trái; UI Ôn lại/Sửa lỗi/Chọn bài sửa lỗi; câu xác nhận Nền thuộc đúng thẻ; Lời giải đúng nhóm và action khác chức năng có nhãn khác. Mọi disclosure G01/G02 đóng mặc định, deep-link mở ancestor cần thiết; điều kiện bắt buộc vẫn nhìn thấy.
- G02 có bìa riêng từ L02, Nền/CP/ba lượt Ôn lại đã được bổ sung. M1–M5 là lõi, M6 chuyển giao có điều kiện. Không dùng thiếu hụt FB029 làm hiện trạng hôm nay hoặc gọi thêm nội dung là nghiệm thu toàn gói.
- Trạng thái: nguồn đã triển khai theo hồ sơ FB036; G01 HTML cục bộ/G02 HTML audit **chờ chủ trì xem**. Receipt FB033 giữ nguyên lịch sử; chưa PDF/Git/phát hành/khóa 0.5.
- Bằng chứng: kit `doi_sanh_FB036.md`, audit `zo_web_pair_refinement_2026-10-08/`, checkpoint `E:/zo_math_ca_nhan/checkpoints/FB036_20261008_233145/`. Số PASS chỉ chứng minh phần kiểm đã ghi.
- Ảnh hưởng: hồ sơ hai gói, 02/03/07, chuẩn QMD, kit và nhật kí thiết kế. Thay trạng thái current FB033–035, mở rộng mặc định đóng QD_004 trong đúng G01/G02; không xóa nghiệm thu lịch sử.

## QD_017 — Làm rõ Bài học và Luyện tập, mở rà nội dung G01

- Ngày ghi: 10/10/2026. Căn cứ: phản hồi trực tiếp sau khi tiếp tục FB036: “Không đúng, Luyện tập và Bài học không xen kẽ nhau.” Không suy ngày phát ngôn từ ảnh/tên tệp.
- Đã xác nhận: hai khu vực không xen kẽ; chặng là tổ chức Luyện tập, liên kết xem lại là hỗ trợ theo nhu cầu. Tự đánh giá diễn ra ở các điểm dừng, không chờ xong toàn mạch. Thay mô tả “học và luyện chặng 1…2…3” trong 01 và hướng dẫn dự thảo tại hồ sơ G01; giữ mục tiêu, ngân hàng, ID, tuyến hỗ trợ và schema.
- Yêu cầu nội dung còn mở N01–07: bỏ câu Bắt đầu dư ở Cách học; sửa danh sách gây hiểu là ba bước tuần tự; làm rõ vị trí Ba chặng; rà Cách thực hiện Luyện tập; xem vai trò 45 phút/20 điểm; hướng dẫn gọn/bản đồ đúng; kiểm kê toàn gói. Vị trí mới của Ba chặng/thông số và sơ đồ chưa được chốt. Không coi lời đề xuất của agent là phê duyệt.
- Trạng thái: sửa chuẩn tài liệu được giao bởi QD_018; **chưa sửa QMD hoặc dựng HTML mới** cho các góp ý này. Chi tiết vị trí/giới hạn nằm ở hồ sơ G01.
- Giữ FB036 yêu cầu nêu chặng ở đầu làm lịch sử của lần sửa; câu hỏi mới về chuyển vào Luyện tập cần phương án, không tự xóa yêu cầu ấy. Bản đồ xen kẽ bị bác không được tái sử dụng.
- Ảnh hưởng: 01, 02, 07, hồ sơ hai gói, mẫu hồ sơ và lượt rà nội dung kế tiếp được ghi ở 03.

## QD_018 — Hợp nhất tài liệu điều hành theo quyết định hiện hành

- Ngày: 10/10/2026. Căn cứ: chủ trì “OK. Hãy thực hiện Bước tiếp theo trong baocao của bạn.”, dẫn bước hợp nhất trong báo cáo khôi phục quyết định ngày 10/10.
- Phạm vi đã giao: hợp nhất tài liệu/hướng dẫn theo D01–35, ghi N01–08 đúng trạng thái; mỗi quy tắc một chủ sở hữu, một việc hiện hành ở 03. Giữ lịch sử thay thế, provenance, receipt FB033/checkpoint FB036 và diff ngoài phạm vi.
- Đích: 01 sở hữu kiến trúc; 07 sở hữu vùng đọc/điều hướng; chuẩn QMD/kit chi tiết hiện thực; hồ sơ tham số/bằng chứng riêng; 04 quyết định; 05 cách tiếp quản; 06 nguồn/chuyển tiếp. Không tạo roadmap thiết kế cạnh tranh.
- Yêu cầu bàn giao N08 đã áp dụng: sau mỗi câu trả lời phải đặt tên bước tiếp theo rõ ràng để chủ trì sử dụng; ghi trong 05.
- Giới hạn: không sửa QMD/toán/CSS/JS/schema/checker/manifest/build config/tài sản/đầu ra; không dựng HTML/PDF, stage/commit/push/phát hành hoặc khóa Design 0.5. M8.R/Video giữ nguyên.
- Trạng thái thực hiện và kiểm: 03/DH_008, báo cáo `_audit/zo_2027_hop_nhat_dieu_hanh_2026-10-10.md`. Hoàn thành hợp nhất tài liệu không thay nghiệm thu nội dung/HTML hai gói.

## QD_019 — Đồng bộ toàn bộ các lớp điều hành trước khi biên tập tiếp

- Ngày: 10/10/2026. Căn cứ chỉ thị trực tiếp: “OK. Hãy thực hiện hợp nhất và đồng bộ toàn bộ bộ điều hành Ôn thi Toán THPT 2027 theo đề xuất của bạn.”
- Đã chốt phạm vi: kiểm kê và phân quyền tất cả lớp điều hành khóa, hồ sơ/mẫu, hướng dẫn vận hành, metadata trạng thái, kit/binding Design và chuyển tiếp; mỗi quy tắc một chủ sở hữu; chỉ 03 sở hữu công việc hiện hành. Danh mục 08 là sổ phân vai, không roadmap mới.
- Lượt hợp nhất QD_018 chưa bao phủ hết các phát biểu/trạng thái cũ ở tài liệu vệ tinh. QD_019 bổ sung phạm vi đồng bộ, không hủy kiến trúc 01, thiết kế đã duyệt, nghiệm thu lịch sử hoặc toán gói.
- Rà nội dung/đường học G01 đã có báo cáo 21 RD ngày 10/10. Ghi là phát hiện chưa sửa; không biến đề xuất bố trí Ba chặng, 45 phút/20 điểm, sơ đồ hoặc tiêu chí hoàn tất thành quyết định sư phạm mới.
- Trạng thái máy đọc phải tách nghiệm thu lịch sử và ứng viên FB036 đang chờ xem. Sửa hồ sơ trạng thái, không sửa cấu hình dựng/schema/manifest/receipt để hợp thức hóa PASS.
- Giới hạn: không biên tập QMD/toán/UI, không render HTML/PDF, Git/phát hành, không sửa package khóa/Kế hoạch 0.6/checkpoint và không tiếp tục M8.R/Video. Giữ thay đổi ngoài phạm vi.
- Thực hiện: 03/DH_009; bằng chứng `_audit/zo_2027_dong_bo_toan_bo_dieu_hanh_2026-10-10.md`. Hoàn thành đồng bộ văn bản không là nghiệm thu học liệu. Việc nội dung tiếp theo phải được giao theo phạm vi đã chốt.

## QD_020 — Duyệt biên tập thống nhất R1-G01 theo RD01–RD21

- Ngày: 10/10/2026. Bằng chứng trực tiếp: “Mình duyệt phương án biên tập R1-G01. Hãy thực hiện.”
- Trạng thái: **đã chốt phương án và giao triển khai; HTML sau biên tập chưa được nghiệm thu**.
- Nội dung: áp dụng phương án `_audit/r1_g01_phuong_an_bien_tap_thong_nhat_2026-10-10.md`; Cách học sở hữu điểm vào/bản đồ toàn gói, ba chặng sở hữu bởi Luyện tập, thông số và điều kiện độc lập bởi Kiểm tra. CP-LT3 dẫn làm Kiểm tra; CP-KT và bảng đọc kết quả có tuyến hai chiều. Nền/Sửa lỗi chỉ dùng xác nhận phù hợp chưa lộ, nêu rõ giới hạn ngân hàng; quay về nơi gọi. Nhật kí giữ 14 trường, ví dụ L02/sc02 khớp dữ kiện. Ôn lại tính từ hoàn tất lượt chính, không bắt chờ hết ba lượt mới học gói tiếp phù hợp.
- Giữ Bài học/Luyện tập không xen kẽ, ý nghĩa năm mục tiêu, ID và toán nhiệm vụ. Thay trạng thái chưa chốt vị trí/câu chữ của N01–06/RD tại QD_017; không thay chuẩn chung 01/07 hoặc nghiệm thu lịch sử.
- Nguồn chịu tác động: G01 QMD/manifest/layout, include Nhật kí/N-LT dùng chung, guard gói và hồ sơ trạng thái. G02 chỉ kiểm hồi quy các include, không biên tập nội dung riêng.
- Kiểm bảng: đầu Luyện tập thêm bảng T19 theo hợp đồng bảng hiện có; bộ lọc HTML khai báo đúng 19 bảng, giữ kiểm ID/cột/thứ tự. Các kiểm PDF cũ vẫn khóa, phải đồng bộ bằng lượt PDF riêng; không sửa provenance hoặc đoán số trang để làm PDF có vẻ CURRENT.
- Điều không được suy ra: `transfer` ở nhánh đạt CP-LT3 là tên kind sẵn có của schema để trỏ tới K01–K05, không thêm một chặng Chuyển giao hoặc bài P. Readiness PASS không phải nghiệm thu đường học.
- Giới hạn: không đổi art direction, CSS/controller, hình/BBT, schema, nguồn riêng G02/Nhà/D0, PDF, receipt FB033/checkpoint FB036, Git hoặc phát hành. Thành phẩm HTML mới cần chủ trì xem.
- Thực hiện và bằng chứng: 03/DH_011, hồ sơ G01 và `_audit/r1_g01_bien_tap_2026-10-10/qa/`.

## QD_021 — Khép đường học và thay thế tức thời quy tắc cũ

- Ngày: 10/10/2026. Căn cứ: chủ trì chỉ rõ mạch Bài học, Luyện tập, Kiểm tra, Ôn lại có thứ tự nhưng được đi tới/đi lui; ôn nguồn, sửa lỗi và Nhật kí diễn ra ở nhiều thời điểm; Kiểm tra tự lực hoàn toàn. Chủ trì giao thực hiện bước tiếp và yêu cầu cái mới thay cái cũ ngay.
- Có hiệu lực: 01/2.2.1–2.2.2 sở hữu quan hệ và 14 ca tình huống; 07 sở hữu cách thể hiện; 02/1.2 sở hữu việc thay thế/đồng bộ/thu hồi bằng chứng. Giữ Nhật kí 14 trường, toán, ID, số chặng và thiết kế 9/10.
- Thay phần nào: bác bỏ chuỗi bảy nút trong bản DH_011 và nhãn “Bài học, gồm Khởi động”. Đọc kết quả, sửa/xác nhận, ghi/hẹn ôn là thao tác cục bộ hoặc nhánh, không phải chặng toàn gói. QD_020 còn hiệu lực ở phần không bị thay; không hoàn nguyên toàn lượt biên tập.
- Ôn nguồn gồm xem lại Bài học trong gói và Ôn nền ngoài gói, không tự đổi menu hoặc trang Nguồn. Sửa lỗi gọi được sau nhiệm vụ Bài học, chặng Luyện tập, Kiểm tra đã kết thúc và Ôn lại; không tự tạo bài sửa chưa kiểm định.
- Nguyên nhân đã kiểm: predicate RD01/RD06 trong guard cũ chỉ kiểm cụm chữ và không có danh sách số thứ tự trực tiếp; không kiểm liên kết của chuỗi mũi tên. Vì vậy sơ đồ sai vẫn PASS. 465/465 lưu nguyên như bằng chứng cũ, không chứng nhận mô hình này.
- Trạng thái: ứng viên G01 DH_011 không còn chờ duyệt đường học; RD01/RD06 mở lại. G02 phải rà theo hợp đồng mới, chưa xác nhận toàn gói. Đồng bộ tài liệu không phải sửa nguồn học liệu hoặc nghiệm thu HTML.
- Hàng rào: registry phụ thuộc và guard kiểm quan hệ; kết quả không gắn đúng bản điều hành bị từ chối. Cập nhật phải thay phần hoạt động cũ và trạng thái liên quan cùng lượt, trước khi sản xuất tiếp. Lịch sử/receipt không sửa.
- Giới hạn lượt: chỉ tài liệu, trạng thái và guard hồi quy; không sửa QMD/manifest/layout/CSS/JS, dựng HTML/PDF, stage/commit/push/phát hành, mở M8.R hoặc nâng Design 0.5. Việc tiếp theo chỉ ở 03.

## QD_022 — Chống tái áp dụng quy tắc cũ, không khóa hiệu chỉnh

- Ngày: 10/10/2026. Căn cứ trực tiếp: chủ trì làm rõ cần chống tái áp dụng quy tắc cũ khi quy tắc mới đã cập nhật, không chống sửa chữa, hiệu chỉnh chỗ chưa hợp lí.
- Thay riêng cơ chế QD_021 làm hết hiệu lực mọi bằng chứng khi bất kỳ hash tài liệu/guard đổi. Giữ nguyên đường học QD_021, 14 tình huống, lỗi RD01/RD06 còn mở, thiết kế và Nhật kí.
- 02/1.2 sở hữu chính sách: mỗi chủ đề chỉ dùng quy tắc có hiệu lực sau cùng; ghi phần bị thay và cập nhật các mệnh lệnh chịu ảnh hưởng ngay. Registry chọn quyết định theo chủ đề, không khóa toàn bộ byte hay lấy quyết định mới của vấn đề khác để hủy quy tắc còn hiệu lực.
- Chỉnh sửa hợp lệ trong phạm vi đã giao được tiếp tục, không tạo cổng xin phép thường lệ. BLOCKED là trạng thái chưa đủ điều kiện xin duyệt, không cấm sửa nguồn lỗi.
- Chỉ kiểm lại phần chịu ảnh hưởng của thay đổi quy tắc, đầu vào hoặc phép kiểm. Kết quả không liên quan có thể giữ sau đối chiếu phạm vi; provenance/hash còn dùng để xác minh đầu vào, không là lệnh hủy toàn bộ QA.
- Guard phải chặn sơ đồ bảy nút/quy tắc đường học cũ và chấp nhận bản sửa đúng; sửa hash tài liệu không liên quan không tự làm lỗi. Không tuyên bố máy tự phát hiện mọi thay đổi ý nghĩa hay lỗi sư phạm.
- Phạm vi lượt: cơ chế điều hành/guard và con trỏ liên quan; không sửa học liệu, layout, runtime, HTML/PDF, receipt, Git/phát hành hoặc Design 0.5. Bằng chứng mới ở `_audit/zo_2027_quy_tac_thay_the_QD022_2026-10-10/`; bước tiếp chỉ ở 03.

## QD_023 — Hệ nhãn học liệu và bảng di trú G01

- Ngày: 10/10/2026. Căn cứ: chủ trì duyệt “Phương án học liệu hệ nhãn”, rồi giao “đồng bộ hệ nhãn đã duyệt vào bộ điều hành và lập bảng áp dụng đầy đủ cho R1-G01”.
- Có hiệu lực cho R1 khóa 2027: hai hệ nhãn kiến trúc/loại nội dung, chức năng nhiệm vụ riêng; một owner cấu trúc; tên điều hướng ổn định, tiêu đề theo nội dung; nhãn hiển thị không lặp tiêu đề; số liên tục trong toàn nhóm chức năng, không đặt lại qua chặng/lượt. Ôn nền là khu hỗ trợ độc lập. Tên Nhiệm vụ không xóa vai trò, mục tiêu, điều kiện tự lực hoặc độ lộ.
- Chủ sở hữu: 01 cho nghĩa/quan hệ, danh mục kiến trúc cho từ vựng có khóa, 07 cho hiển thị/mục lục/số, chuẩn QMD/schema cho hợp đồng máy. 08 phân vai; 03 giữ trạng thái và việc tiếp theo. Bảng di trú G01 ở `_quy_trinh/ap_dung_he_nhan.json`; bảng đầy đủ sinh từ nguồn QMD/include/manifest, không là nguồn build.
- Thay quy tắc nhãn chỉ trang trí, nhãn trùng tiêu đề bắt buộc, đánh lại số theo chặng và coi Ôn nền thuộc Bài học. Giữ QD_021, cơ chế hiệu chỉnh QD_022, mã H/L/K/O/S/N, Nhật kí 14 trường và lịch sử. Không dùng phần quy tắc bị thay làm chuẩn mới.
- Duyệt phần hệ nhãn/dữ liệu/cổng di trú của phương án không tự duyệt mọi tên, số S, anchor con, câu chữ chuyển gói hoặc bố trí cụ thể ở mục 3–5. Các điểm này được ghi riêng trong bảng G01 để chốt trước sửa nguồn.
- Lượt này cập nhật điều hành, danh mục/schema/loader/guard và bảng/hồ sơ; kiểm hợp đồng/fixture/bảo toàn. Không sửa học liệu QMD hoặc manifest, không render HTML/PDF, controller/CSS, receipt, stage/commit/push/phát hành hoặc khóa Design 0.5. G02 chưa lập bảng/applied; không gọi hai sản phẩm đã nhất quán vì hợp đồng đã đồng bộ.
- Thực hiện: 03/DH_013. Bảng/QA: `_audit/zo_2027_he_nhan_QD023_2026-10-10/`. Tiếp theo chốt áp dụng riêng G01 trước giao lượt sửa nguồn.

## QD_024 — Quyền bắt đầu và một lượt Kiểm tra, toàn chương trình

- Ngày: 10/10/2026. Trạng thái: đã chốt quy tắc. Chủ trì sửa bản chốt G01, giao “Mình đã sửa xong, hãy dùng bản này”, rồi xác nhận phạm vi: “Nó được áp dụng không những cho R1, mà là toàn bộ các gói của chương trình học.”
- Hai nội dung được xác nhận: đã chuẩn bị kĩ lưỡng **hoặc đủ tự tin** thì có thể thực hiện Kiểm tra; **không chia một lượt Kiểm tra thành nhiều đợt**. Chủ sở hữu duy nhất: 01/2.3–2.3.1. 07/4.4 điều hành việc hiển thị; 02 điều hành cách kiểm; registry/guard chọn chủ đề `assessment_policy`.
- Áp dụng cho toàn bộ các gói của chương trình Ôn thi Toán THPT 2027 có hoạt động Kiểm tra, không chỉ các gói R1. Không đổi tính tự nguyện hoặc hoạt động Khảo sát D0; không ép mọi loại gói phải có Kiểm tra hay dùng toàn bộ nguyên mẫu R1.
- Thay riêng điều kiện cũ ở 01/2.3: phải có bài làm độc lập phù hợp các mục tiêu mới được thử Kiểm tra trực tiếp. Quyền chia việc học thành nhiều buổi không cho phép chia một lượt Kiểm tra. Không thay toàn bộ QD_021: mạch chính, hỗ trợ ngang, tự lực trong Kiểm tra và DH01–DH14 vẫn giữ. QD_022/QD_023 không bị thay bởi quyết định này.
- Quyền vào Kiểm tra khác chứng nhận đạt mục tiêu/chuyển gói. Giữ bằng chứng độc lập, kết quả ban đầu/sau hỗ trợ, giới hạn bài đã lộ và tham số kiểm tra riêng từng gói. Không tự tạo chức năng khóa trang, lưu lượt hoặc chấm tự động.
- Bản biên tập G01 do chủ trì sửa được nhận làm đầu vào triển khai: `_audit/r1_g01_ban_chot_bien_tap_2026-10-10.md`, SHA-256 `51fe4f877b2c5e5c19d1ccf1736ff8599244ed43c8cbf257971a0c90482a5c0e`. Giữ nguyên tệp người dùng; trạng thái “chờ duyệt” trong bản lúc lập được tiếp quản bởi chỉ thị sau cùng này. Duyệt bản biên tập không là duyệt HTML chưa dựng.
- Đồng bộ quy tắc, vệ tinh, mẫu và trạng thái máy đọc; guard có ca kiểm phạm vi ngoài R1 và từ chối điều kiện cũ/chia lượt/tự tin thay bằng chứng. Học liệu QMD và HTML/PDF chưa áp dụng trong lượt đồng bộ này. G01 còn cần triển khai bản chốt; G02 còn lời dẫn điều kiện cũ ở Khởi động (`index.qmd`, câu “Chỉ thử Kiểm tra trực tiếp khi…”), giữ lỗi `KT-G02-01` mở. Không sửa bằng chứng/receipt cũ để báo đạt.
- Việc hiện hành và bước tiếp theo chỉ ở 03; không stage/commit/push/phát hành, không mở PDF hoặc đổi thiết kế đã duyệt.

## QD_025 — Áp dụng bản biên tập G01, bổ sung Gợi mở

- Ngày: 10/10/2026. Căn cứ: chủ trì giao “Áp dụng bản chốt đã sửa vào nguồn R1-G01 và dựng HTML”. Bản được nhận đã có hash ghi ở QD_024; không sửa tệp do chủ trì biên tập.
- Bổ sung `function.guided_thinking` vào từ vựng QD_023: nhiệm vụ thử suy nghĩ trước lời giải thích trong Bài học, dãy 01–07 riêng; không nhập vào Tự kiểm tra, không sao chép bảy đáp án và không coi lời giải thích là bằng chứng độc lập.
- Chốt sáu điểm LBL-G01-01–06 theo bản được nhận: tên/số toàn nhóm, định danh con, Cách học, Ôn nền độc lập, Sửa lỗi sau Ôn lại thuộc Sửa lỗi và phạm vi kiểm kê minh họa. Giữ QD_021–024, mã nhiệm vụ/ID cũ, toán học và khung thiết kế đã duyệt.
- Chuẩn từ vựng dùng chung được mở rộng; áp dụng sản phẩm trong lượt này chỉ G01 và định danh trung tính của nguồn Nền dùng chung. Không tuyên bố G02 đã di trú. Dựng HTML cô lập, không đổi receipt nghiệm thu cũ, không promotion/PDF/Git/phát hành.
- Sau sửa phải kiểm nguồn, binding, toán/ID, đề–đáp án, đường quay về, 14 trường Nhật kí và trình duyệt. Trạng thái áp dụng nguồn khác trạng thái chủ trì duyệt HTML; công việc và bước tiếp chỉ ở 03.

### Triển khai kế thừa G02 — DH_016, 11/10/2026

- Chủ trì giao áp dụng thay đổi đã làm G01 sang G02 sau khi hoàn thành G01. Đây là mở phạm vi triển khai QD_021/024/025 cho G02, không là quyết định thay kiến trúc, ép cùng toán hoặc nghiệm thu HTML.
- Đã áp dụng nguồn/layout/binding riêng G02, Ôn nền cấp gốc và số liên tục theo chức năng; 59 nhiệm vụ/59 đáp án. Giữ mã manifest, toán/ID cũ, Nhật kí 14 trường và nhánh chuyển giao riêng. Tuyên bố “G02 chưa di trú/chưa source_applied” ở lượt đồng bộ trước là lịch sử, không dùng lại làm trạng thái hiện hành.
- Kiểm mới và HTML ở audit DH_016; đã khép GOV-G02/KT-G02-01 trong phạm vi nguồn/đích/câu chữ DH01–DH14 và runtime đại diện, không gọi là kiểm toán toán độc lập toàn gói. Cập nhật registry/profile/điểm vào; giữ báo cáo/receipt lịch sử. Chưa PDF/production/Git/phát hành hoặc khóa 0.5; G01/G02 đều giữ trạng thái chủ trì duyệt riêng.

## QD_027 — D0 dùng kit web chung, giữ khảo sát riêng

- Ngày 11/10/2026; chỉ thị chủ trì: “Sau khi hoàn thành trang nhà, hãy hoàn thành tiếp trang Khảo sát đầu vào (D0).” Triển khai kế thừa thiết kế đã duyệt, không chọn lại hướng thiết kế.
- Nguồn QMD opt-in, adapter từ raw Quarto mới, map D0 riêng. Giữ năm khu vực/24 câu/Bài 00/25 đối chiếu/nội dung/ID/luồng tự nguyện và HTML-only. Không mang Kiểm tra R1/nhật kí/chặng/PDF vào D0, không đưa ghi chú sản xuất vào lời dẫn.
- Dùng chung shell/font/giấy/nền/rail/drawer/footer; disclosure đóng, header bảng trái, vùng cuộn hình. Trình HTML cô lập, không promotion root docs/Git/phát hành. Nghiệm thu lịch sử giữ riêng; giao diện mới pending owner review.
- Cập nhật nguồn/layout/CSS/JS/adapter/checker, D0 README/hợp đồng/ma trận/config/profile/manifest, kit và registry. Cổng nguồn ghi nhận chính xác hai nhãn danh mục đã đổi ở commit a46a8051; giữ SHA receipt và kiểm toàn chuỗi. Checker mạch trỏ Kế hoạch hiện hành, không khôi phục đường dẫn cũ.
- Trạng thái/bằng chứng/việc tiếp theo chỉ ở 03; không thay QD_021/024/025 hoặc Kế hoạch 0.6/Design 0.4 khóa.

## QD_028 — Đối sánh theo vai trò và phân biệt Phối hợp với Chuyển giao

- Ngày: 11/10/2026. Trạng thái: đã chốt nguyên tắc và quyền triển khai có mục tiêu; HTML mới chưa chủ trì duyệt.
- Căn cứ: yêu cầu triển khai đính kèm báo cáo `Doi-sanh-R1-G01-R1-G02.html`; chủ trì trả lời “Duyệt phân biệt hai chức năng như đề nghị”.
- Phối hợp kết nối kiến thức giữa gói; Chuyển giao áp dụng phương pháp sang họ hàm mới. Thay việc danh mục gọi toàn bộ function.transfer là Phối hợp; giữ khóa transfer cho Chuyển giao, thêm integration cho Phối hợp. Không đổi ID nhiệm vụ hoặc tạo nhánh bắt buộc.
- Củng cố các nguyên tắc đã duyệt tại 01/2.5.1, 02/1.3, 07 và chuẩn QMD. Không thay QD_021/024/025/022 ở những chủ đề còn hiệu lực.
- Sửa lỗi còn tồn tại từ M01–M48 sau kiểm nguồn; được thay một đơn vị toán tối thiểu khi cần, phải kiểm đúng mục tiêu và độ lộ. Hai gói là đối tượng đối sánh ngang nhau, không coi G01 hoàn hảo.
- Phạm vi: QMD/include/binding/bộ dựng/hồ sơ và điều hành liên quan G01–G02. Chỉ dựng HTML cô lập; không PDF học liệu, Git, root docs hay xuất bản. Báo cáo hiện hành theo DH_021 tại 03.

## QD_029 — Ký pháp toán và số mục Bài học

- Ngày: 11/10/2026. Căn cứ: chủ trì chỉ rõ G02 thiếu số mục so với G01; xác nhận công thức LaTeX, phân số `\frac`, đạo hàm `^\prime`, và yêu cầu chống tái diễn căn/công thức lệch hàng.
- Đây là củng cố nguyên tắc ký pháp và tính nhất quán, không thay kiến trúc học tập, bài toán, ID, tên chức năng hoặc thiết kế đã duyệt. 07 sở hữu số mục hiển thị; chuẩn QMD sở hữu ký pháp và ánh xạ HTML; 03 sở hữu trạng thái triển khai.
- Triển khai hiện tại chỉ G01/G02, include Nền liên quan, shell dùng chung và hai adapter. Không tuyên bố đã kiểm/sửa toàn repository. Lỗi phải sửa ở nguồn và cơ chế dựng; không sửa tay HTML hoặc nới strict binding để qua kiểm.
- Kết quả QA lịch sử không chứng nhận các lỗi mới này đã hết. Receipt lịch sử giữ nguyên. HTML mới chỉ để xem, chờ chủ trì duyệt; không PDF, promotion root docs, Git hay phát hành.

## QD_030 — Ngôn ngữ bảng 0.4 theo chức năng, dùng chung toàn khóa

- Ngày: 11/10/2026. Trạng thái: chỉ thị đã chốt, hiện thực/HTML chờ chủ trì xem.
- Căn cứ: chủ trì yêu cầu rà Design 0.4 và tinh chỉnh mọi bảng trên Nhà, D0, G01, G02. 57 bảng hiện tại; Nhà không có bảng. Bảng giá trị G02 bị ép header trái và số phải; bảng có link còn mất lớp chuẩn; D0 bảng dấu vẫn ở đường SVG.
- Quy tắc sở hữu duy nhất tại 07/6.1.1; chuẩn QMD giữ hợp đồng tích hợp. Tám loại 0.4 theo chức năng; bảo toàn toán/ID/liên kết/luồng, không ép cùng hình thức mọi loại. Thay quy tắc chung “header trái” bằng các ngoại lệ tường minh giá trị/ma trận/dấu/BBT; Nhật kí vẫn trái. Bảng dấu D0 dùng native/MathML từ đúng JSON, không sửa dữ liệu.
- Kit giữ binding vai trò và CSS, các adapter đều gọi bộ nối; bảng mới chưa phân loại/binding thiếu/trùng/dữ liệu JSON lệch chặn build. Kiểm theo role thay phép kiểm blanket-left; không nới kiểm nội dung để đạt.
- Phạm vi: toàn khóa ở cấp quy tắc, bốn trang hiện tại ở cấp hiện thực. Không đổi quy chuẩn global, Design 06/07, shell đã duyệt, QD_021/024/025/028/029, nội dung toán, PDF, receipt lịch sử, Git hoặc phát hành. Báo cáo lịch sử giữ nguyên; phần QA bị đổi phải kiểm lại theo QD_022.
- Nguồn hiện thực: `scripts/zo_course_tables.py`, `profiles/course-tables.json`, `course-tables.css` và bốn adapter canonical. Hồ sơ/bằng chứng tại DH_023/03, không xem PASS là nghiệm thu.

## Mẫu ghi quyết định mới

Sao chép mẫu này khi có quyết định thật; không đánh dấu mẫu là một quyết định.

- ID và tên:
- Ngày:
- Trạng thái: đề xuất / đã chốt / được thay thế.
- Vấn đề và bằng chứng:
- Nội dung quyết định:
- Người chốt hoặc chỉ thị làm căn cứ:
- Tệp và gói chịu ảnh hưởng:
- Thay thế quyết định nào:
- Việc cần cập nhật và người thực hiện:
