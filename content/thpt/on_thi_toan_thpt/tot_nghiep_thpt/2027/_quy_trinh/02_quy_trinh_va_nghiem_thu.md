# Quy trình sản xuất, sửa chữa và nghiệm thu

Phiên bản: 0.10 · Ngày biên tập: 16/10/2026 · Đường học QD_033; thay thế QD_022; hệ nhãn QD_025; Kiểm tra QD_024.

Áp dụng cho Codex/Copilot khi làm trong repo. [Điểm vào](README.md).

**Kiểm kiến trúc QD_033:** lấy nghĩa ở 01 và cách thể hiện ở 07; xác nhận Bài học → Luyện tập → Kiểm tra → Ôn lại là tiến trình chuẩn được khuyến nghị nhưng không dùng thứ tự mục lục làm điều kiện bắt buộc phải hoàn thành tuần tự. Rà điểm vào theo nhu cầu/chuẩn bị/bằng chứng; bốn hỗ trợ độc lập theo ngữ cảnh; kết thúc lượt Kiểm tra trước trợ giúp và giữ riêng bài ban đầu; lưu bằng chứng không bắt ghi Nhật kí ở mọi Điểm dừng; chỉ link quay lại đề khi thực sự tách vị trí. Registry chọn QD_033 cho `learning_route`. Audit profile QD_021 là lịch sử; khi QMD/HTML chưa được đối chiếu lại với quyết định này thì mã máy đọc được vẫn là `pending_source_review`, kèm phạm vi `qmd_html_alignment_not_yet_cross_checked` và `known_mismatch: false`; không diễn giải mã đó thành một lỗi đã xác định hoặc đổi trạng thái thành đã áp dụng. Cổng tài liệu có thể PASS với chuyển tiếp này, nhưng cổng ứng viên đường học phải chặn cho đến khi có phép đối chiếu nguồn/đầu ra mới.

**Kiểm điều hướng QD_032:** dùng quy tắc tại 07 và nguồn dùng chung, không tái dùng toolbar cũ từ layout đóng băng. Nghiệm thu trên đủ Nhà/D0/G01/G02: đích thật, trang hiện tại, bàn phím/no-JS, mobile, bảo toàn URL/view khi về đầu, bảng màu và drawer độc lập. Chạy `scripts/zo_web_2027_navigation_check.py` qua `zo_python.py` với `--output` thư mục build cách ly; thêm `--browser` để kiểm trực quan/hành vi. Không thay bằng chứng cũ, không khóa việc hiệu chỉnh; kiểm lại các phần bị ảnh hưởng. Duyệt mẫu không cho phép đổi heading chưa duyệt hoặc phát hành.

Lượt QD_031: hai adapter G01/G02 bắt buộc kiểm nguồn và DOM bằng `scripts/zo_web_2027_backlog_check.py`: thứ tự Toàn văn, khu vực ngang hàng, sở hữu nhóm nhiệm vụ/lời giải, số Sửa lỗi và mọi nhãn liên kết, hành động cục bộ, bảng chọn bài. Dựng năm hình G02 mới và kiểm manifest nguồn/asset theo profile 0.4; không dùng cache cũ làm bằng chứng. Lấy trạng thái/bản xem ở 03/DH_026, không từ QA hoặc receipt lịch sử. Kiểm tự động phải kèm xem hình; không thay nghiệm thu chủ trì.


## 1. Chọn đúng loại công việc

| Loại | Bắt đầu từ | Kết quả trước khi sửa nguồn |
|---|---|---|
| Rà gói đã có | Nguồn và bản thực chạy, hồ sơ gói, kiến trúc | Báo cáo khoảng cách có vị trí đối chiếu |
| Sửa gói đã có | Phạm vi sửa đã được giao | Danh sách thay đổi có đích, bảo toàn phần đúng |
| Tạo gói mới | Kế hoạch, tiên quyết, nguồn toán chính thống | Phạm vi và ma trận học–đánh giá được chốt |
| Bảo trì sau phát hành | Phản hồi hoặc lỗi tái hiện được | Mức ảnh hưởng, phạm vi sửa và bản phát hành chịu tác động |
| Đồng bộ bộ điều hành | Quyết định đã xác nhận và danh mục 08, không chỉ thư mục `_quy_trinh` | Ma trận chủ sở hữu–tài liệu chịu ảnh hưởng–phần bị thay–trạng thái/bằng chứng; chưa sửa học liệu |

### 1.1. Cổng đồng bộ trước biên tập tiếp

Theo QD_019, một lượt đổi quyết định dùng chung phải khép đủ các đích: nguồn quy tắc, hồ sơ gói/mẫu, hướng dẫn vận hành, metadata trạng thái nếu bị ảnh hưởng, hợp đồng kit và con trỏ chuyển tiếp. Không chỉ cập nhật README hoặc thêm báo cáo rồi coi toàn bộ đã thông suốt. Danh mục và phạm vi ở [08](08_danh_muc_tham_quyen_dieu_hanh.md).

Phép kiểm tối thiểu:

- Một quy tắc một chủ sở hữu, tài liệu vệ tinh không đưa mệnh lệnh khác; các phần lịch sử có nhãn và đích tiếp quản rõ.
- Bài học/Luyện tập không xen kẽ; chặng thuộc Luyện tập; Nhật kí một nguồn 14 trường; vai trò/cấp sư phạm không suy từ heading/CSS hoặc số vùng.
- Mạch bắt buộc mở cố định; chỉ hộp có trạng thái đóng/mở mặc định đóng. Kiểm hướng dẫn có che điều kiện bắt buộc không, ghi lỗi nguồn riêng thay vì tự đổi quy tắc.
- Phân biệt đã sửa, đã kiểm, chủ trì duyệt đúng bản và phát hành. Metadata không kế thừa nghiệm thu cũ cho nguồn mới.
- Có danh sách tệp thay đổi và đối chiếu hash/diff ngoài phạm vi; liên kết mới tồn tại; không sửa receipt, baseline hoặc kết quả cũ.
- Phát hiện chưa sửa có ID/vị trí/đích xử lí; chưa quyết định sư phạm ghi rõ chưa chốt. Chỉ 03 ghi một bước tiếp theo.

Cổng này kiểm tài liệu điều hành, không thay kiểm nội dung, toán, UI hoặc PDF. Khi được giao biên tập tiếp, lập phạm vi sửa theo các ID còn mở; không tự chạy tất cả công việc trong prompt lịch sử.

### 1.2. Quyết định mới thay quy tắc cũ ngay, sản phẩm chưa sửa bị chặn

Trong cùng lượt cập nhật điều hành, trước khi biên tập hoặc xin duyệt tiếp:

1. Ghi quyết định đã xác nhận, phạm vi và chính xác phần cũ bị thay tại 04; sửa trực tiếp nguồn quy tắc sở hữu vấn đề. Không chỉ thêm ghi chú mới mà để mệnh lệnh cũ vẫn hoạt động.
2. Đối chiếu danh mục 08; cập nhật vệ tinh, mẫu, README vận hành, profile trạng thái và binding bị ảnh hưởng. Nơi không bị ảnh hưởng ghi không đổi; không sửa hàng loạt tài sản tham chiếu.
3. Thu hồi trạng thái xin duyệt của phần ứng viên đã biết trái quy tắc mới; mở lại lỗi trong hồ sơ. Báo cáo/receipt giữ nguyên lịch sử; chỉ kết quả chịu ảnh hưởng không còn chứng nhận phần đã đổi. Không gọi đổi metadata là đã sửa sản phẩm.
4. Kiểm ma trận tình huống 01/2.2.2 và quan hệ thực: mạch chính, nơi gọi, hỗ trợ, nơi về, bằng chứng và ngoại lệ Kiểm tra. Kiểm từ khóa, số hộp hoặc cùng CSS không đủ. Tách quyết định/câu chữ biên tập nội bộ khỏi nội dung công bố.
5. Theo QD_022, ghi quy tắc đang có hiệu lực theo từng chủ đề tại `hop_dong_dieu_hanh.json`: quyết định, chủ sở hữu và phần cũ bị thay. Khi thay ý nghĩa quy tắc, cập nhật quyết định của đúng chủ đề và guard chịu ảnh hưởng cùng lượt. Registry không sở hữu kiến trúc; hash chỉ ghi provenance, không khóa mọi byte. Chạy `python scripts/zo_python.py scripts/zo_2027_governance_check.py --self-test`. Chỉ thêm `--report <đường_dẫn_JSON_mới_trong_audit>` khi phạm vi cho phép ghi báo cáo; không ghi đè báo cáo/bản xem cũ.
6. Được sửa nguồn còn lỗi trong phạm vi nhiệm vụ đã giao; trạng thái BLOCKED chặn xin duyệt phần chưa đạt, không chặn sửa chữa. Trước xin duyệt, giải quyết xung đột thẩm quyền, chạy lại các kiểm chịu ảnh hưởng và không còn lỗi chặn. Kết quả không bị ảnh hưởng có thể dùng lại sau khi xác minh đầu vào và phép kiểm tương ứng không đổi; không kế thừa kết quả của quy tắc đã bị thay.

**Chống hồi quy, không đóng băng:** sửa lỗi chính tả, cách diễn đạt hoặc chỗ chưa hợp lí theo quy tắc hiện hành được phép trong phạm vi đã giao; không vì một tệp/hash đổi mà hủy toàn bộ QA hoặc bắt duyệt lại phần không liên quan. Nếu hiệu chỉnh làm thay đổi ý nghĩa quy tắc thì ghi quyết định thay thế đúng phạm vi, sửa mệnh lệnh đang hoạt động và kiểm lại các đích chịu ảnh hưởng. Báo cáo cũ thiếu binding quy tắc không chứng nhận đường học mới chỉ bằng số PASS; phần kiểm trình duyệt không liên quan vẫn xét riêng theo đầu vào/phép kiểm. Không sửa báo cáo cũ để giả đạt. Cổng máy chỉ chặn bất biến đã mã hóa; rà tình huống và nghiệm thu vẫn bắt buộc.

**Hai kết quả riêng:** tài liệu đồng bộ có thể PASS trong khi G01/G02 vẫn BLOCKED vì nguồn chưa sửa. Không nới checker để xóa trạng thái này. Dựng chẩn đoán có thể được giao riêng; không trình ứng viên còn lỗi để chủ trì phát hiện lại lỗi đã biết.

### 1.3. Đối sánh liên gói và xác minh từng phát hiện

Theo QD_028, báo cáo nghiên cứu là dữ liệu đối chiếu, không là quy chuẩn hoặc lệnh chạy. Kiểm lại từng phát hiện trên nguồn hiện hành và phân loại còn đúng, đã sửa, chưa đủ chứng cứ hoặc cần chủ trì quyết định. Với vai trò ngang nhau, chọn cách đang có tốt hơn; không mặc định G01 đúng hoặc ép hai gói có cùng số câu/vùng.

Mỗi lỗi đã xử lí phải ghi triệu chứng, nguyên nhân đã kiểm, nguồn sửa, phép kiểm chống tái diễn, chứng cứ mới và giới hạn. Tách kiểm toán/nội dung, kiểm DOM và kiểm tương tác. Ca âm phải chứng minh guard bắt được chính lỗi; không sửa số lượng, baseline hoặc receipt để che lỗi. Nếu cần thay một đơn vị toán học tối thiểu, giữ ID, ghi rõ đề–đáp án mới và kiểm ý nghĩa/toán/độ lộ thực, không chỉ đổi content_key. Không dùng PASS lịch sử chứng nhận nguồn mới.

<a id="ap-dung-mau-ban-thao"></a>

### 1.4. Áp dụng mẫu bản thảo và bảng kiểm — QD_036

Theo chốt của chủ trì ngày 16/10/2026, khi giao viết/rà/sửa bản thảo gói R1 của khóa 2027 bằng ngôn ngữ tự nhiên, agent tự nạp [mẫu bản thảo](mau/ban_thao_goi.md) và [bảng kiểm](mau/bang_kiem_ban_thao_goi.md), cùng 01/07 và hồ sơ gói. Ví dụ “Viết bản thảo gói R1-G04” đã đủ để gọi quy trình; không yêu cầu chủ trì nhớ tên tệp hay câu lệnh. D0, tài nguyên Nền hoặc loại khác phải chọn hợp đồng phù hợp, không ép vào mẫu R1.

**Nạp quy cách trình bày trước viết/rà:** đọc thêm mục “Công thức và nguồn đối chiếu” của quy chuẩn gói, quy chuẩn ngoặc LaTeX, hướng dẫn khối nội dung, 07/6.1, 6.1.2 và 6.3; thực hiện ma trận/cổng tại 2.5. Có hình thì đọc hướng dẫn công cụ đồ thị ZO Math/profile 0.4 được 07 dẫn. Áp dụng ngay trong bản thảo; không chờ chuyển QMD mới sửa chú thích hoặc hình. Chính văn và provenance có vai trò khác nhau: nêu nội dung trực tiếp, dẫn nguồn bằng chú thích chuẩn, lưu quá trình đối chiếu trong hồ sơ. Số kiểm tính toán/liên kết không chứng nhận đạt biên tập hay thị giác.

1. Trước viết: xác minh nguồn, phiên bản mẫu và bản G01/G02 đang dùng; hoàn thành phần A cùng bản đồ tương ứng từng chức năng. Đọc kĩ các phần liên quan của gói mẫu và tài liệu chính thức. Khác biệt phải nêu nội dung, lí do và phạm vi; khác biệt ảnh hưởng cấu trúc/chức năng đã chốt cần trình chốt trước khi viết phần đó, vẫn tiếp tục phần độc lập đã được giao. Không sao cứng số bài/mục/hình hoặc mã riêng của gói trước.
2. Viết vào đúng `hoc_lieu/<ma_goi>/_quy_trinh/ban_thao/noi_dung.md`; tài nguyên ở vùng bản thảo đã thống nhất. Thực hiện tổ chức tệp theo quy chuẩn gói, không tạo nơi lưu trữ mới hoặc gói tương lai. Ghi phiên bản mẫu áp dụng trong hồ sơ, không sao toàn bộ bộ mẫu thành nhiều bản sửa độc lập.
3. Trước trình: đọc toàn bản, hoàn thành phần B bằng tệp/mục/anchor và kết quả thực; kiểm ý nghĩa tuyến hỗ trợ, độ phủ câu còn mới, đề–lời giải, điểm thành phần và từng hình. Đếm số, liên kết tồn tại hoặc kiểm vector không thay kiểm mục tiêu và xem trực quan. Khép lỗi chịu ảnh hưởng trước khi báo đạt; phần được chủ trì cho hoãn phải có căn cứ, đích xử lí và điều kiện khép, không ghi Đạt.
4. Lưu kết quả áp dụng trong `ho_so/` của chính gói, có phiên bản/hash bản thảo, mẫu và nguồn đối chiếu; tách thời điểm trước viết/trước trình. Gói đã có bản thảo chỉ áp dụng hồi cứu trước bước kế tiếp, không tuyên bố đã làm phần A trước khi viết. Trạng thái và việc tiếp theo chỉ ghi ở 03; biểu mẫu trống không mang trạng thái riêng của gói.
5. Sau chủ trì duyệt bản thảo mới chuyển QMD theo quy chuẩn gói; tài nguyên chính thức dựng lại bằng công cụ ZO Math, rồi kiểm hình và bản xuất thực. Hai mẫu này điều hành biên soạn/kiểm nội dung; kit `_design/web_2027_mau_dung_chung/` điều hành hiện thực trang theo 07. Mẫu bản thảo không chứa CSS/JS và không tự cấp quyền render, commit, PDF hoặc phát hành.

Khi có cải tiến được chốt, cập nhật mẫu/bảng kiểm và các đích bị ảnh hưởng cùng lượt, tăng phiên bản và ghi phạm vi tại 04/08. Gói đang làm chỉ kiểm lại phần chịu ảnh hưởng; kết quả cũ giữ theo phiên bản, không tự sửa hồi tố gói đã có. Cơ chế gọi hiện tại là chỉ dẫn bắt buộc trong AGENTS và quy trình này; chưa phải chương trình tự sinh hay cổng tự động đánh giá chất lượng lời giảng. Cổng tài liệu hiện có kiểm phụ thuộc/quy tắc đã mã hóa; kết quả bảng kiểm vẫn cần đọc có trách nhiệm.

## 2. Quy trình một lượt làm việc

1. Đọc điểm vào, bảng điều hành và hồ sơ gói. Đọc hướng dẫn repo áp dụng; kiểm nhánh, trạng thái Git, diff hiện có và nguồn thực. Không coi đường dẫn trong bàn giao là đã được xác minh.
2. Xác nhận bằng báo cáo ngắn: việc được giao, tệp dự kiến tác động và tiêu chí kết thúc. Nếu người chủ trì đã giao rõ việc sửa, tiến hành trong phạm vi ấy; không yêu cầu duyệt lại chỉ vì chuyển công cụ.
3. Nếu được giao kiểm trước khi sửa, chỉ ghi báo cáo dưới `_audit/`; không sửa học liệu, CSS, cấu hình, checker hoặc tự nâng trạng thái nghiệm thu. Việc điền đường dẫn và ghi kết quả vào bộ điều hành chỉ làm khi nằm trong nhiệm vụ được giao.
4. Khi được giao triển khai, sửa nguồn chính. Kiểm toán học và đường học, dựng HTML đúng phạm vi, quan sát bản thực chạy. Kiểm công cụ hiện có trước khi tạo checker mới.
5. Báo cáo kết quả và giới hạn; đưa bản HTML cho người chủ trì duyệt. Nếu chỉ mới kiểm mã, ghi rõ chưa kiểm thị giác/tương tác.
6. Khi HTML được chấp nhận và được giao đồng bộ, tạo các PDF bị ảnh hưởng từ cùng nguồn; kiểm tính nhất quán.
7. Khi được giao phát hành, dùng quy trình phát hành thực tế của repo; kiểm bản công khai và tệp tải. Không xem render thành công là đã phát hành.
8. Kết thúc phiên theo checklist tại hướng dẫn sử dụng. Commit/push theo phạm vi đã được giao, không tự thêm quyền phát hành từ một prompt lịch sử.

### 2.1. Nhập hoặc hợp nhất một bộ tài liệu tham khảo

Khi nhận một thư mục bàn giao, ZIP, bản thảo hoặc prompt cũ, không chép nguyên bộ vào nguồn điều hành. Với từng tệp:

1. ghi tên, phiên bản, hash hoặc dấu nhận diện đủ để truy nguyên;
2. xác định nó là quy chuẩn, nội dung gói, lệnh triển khai theo thời điểm hay bằng chứng lịch sử;
3. đối chiếu với chỉ thị hiện hành, `AGENTS.md`, nguồn repo và các quyết định mới hơn;
4. gắn một trong bốn trạng thái: **kế thừa**, **kế thừa có điều chỉnh**, **đã bị thay thế**, **chỉ lưu lịch sử**;
5. đưa quy tắc còn hiệu lực vào đúng một nguồn canonical và ghi đích ấy trong tệp nguồn/chuyển tiếp;
6. không dùng điều kiện commit, worktree sạch, số lượng, quyền commit hoặc “việc tiếp theo” của prompt cũ làm lệnh hiện hành.

Nếu một tài liệu có cả phần còn đúng và phần đã lỗi thời, ghi riêng từng phần; không tuyên bố toàn tệp còn hiệu lực hoặc hết hiệu lực chỉ theo tên phiên bản. Yêu cầu hiện tại của người chủ trì và quyết định đã ghi có thẩm quyền cao hơn bộ tham khảo.

### 2.2. Tiếp quản sau checkpoint và quyết định thay đổi nhiều lần

Đọc mục A của bảng điều hành trước hồ sơ lịch sử. Xác minh nguồn và bản xuất bằng hash, nội dung và quan hệ dựng; không chọn bản theo tên hoặc ngày. Checkpoint là bản chụp bảo toàn, không là lệnh phục hồi cả worktree. Receipt chỉ chứng nhận đúng bản/phạm vi đã được chủ trì chấp nhận; receipt FB033 không chứng nhận ứng viên FB036.

Với mỗi vấn đề, truy yêu cầu sau cùng và phần quyết định cũ bị thay; phân biệt chỉ thị triển khai, kết quả kiểm và nghiệm thu. Đưa quy tắc còn hiệu lực vào đúng chủ sở hữu (01: kiến trúc; 07: trang; chuẩn QMD/kit: hiện thực; hồ sơ: tham số; 03: việc hiện hành). Giữ lịch sử, không đổi receipt hoặc baseline để làm PASS. Góp ý đang yêu cầu khảo sát không tự trở thành phương án biên tập đã duyệt.

### 2.3. Đối sánh liên gói theo vai trò

Kiểm nguồn → đầu ra của từng gói trước, rồi lập cặp đối sánh theo chức năng: Bắt đầu/Cách học, định hướng, khởi động, khái niệm, ví dụ, tự kiểm, chặng/checkpoint, Nền, Sửa lỗi, Nhật kí, nhóm Lời giải, Ôn lại, Nguồn và Tải PDF. Ghi cấp tiêu đề, vùng sở hữu, bảng, disclosure, hành động và đích quay về cho từng cặp. Cùng vai trò phải cùng cách trình bày; khác bản chất toán được giữ và giải thích. Không dùng cùng CSS, phần tử đầu tiên hoặc cùng số vùng làm bằng chứng nhất quán.

Thiếu nội dung bắt buộc phải ghi CÒN THIẾU; không tạo thẻ rỗng để đủ số. Kiểm nhãn nguồn/adapter không lặp; nhóm lời giải khớp nhiệm vụ; xác nhận Nền thuộc đúng tài nguyên; bài mới còn chưa lộ. Lỗi đã xử lí phải ghi nguyên nhân, nguồn sửa, guard, bằng chứng và phần chưa kiểm. Các kiểm này chỉ được chạy/sửa công cụ khi nhiệm vụ cho phép.

### 2.4. Cổng hệ nhãn QD_025 trước sửa nguồn

Nạp danh mục nhãn, 01, 07 và hợp đồng QMD; xác minh bằng `zo_2027_governance_check.py --self-test`. Lập bảng áp dụng từ QMD/include và manifest thật: ID hoặc locator khi chưa có ID riêng, loại, nơi sở hữu, nhóm chức năng, số/tên dự kiến, đáp án, nơi quay về, nơi dẫn chiếu và trạng thái duyệt. Không sửa học liệu để làm bảng có vẻ đã áp dụng.

Khi rà/di trú hệ cũ, chạy `python scripts/zo_python.py scripts/zo_learning_architecture.py labels --self-test --application <bảng_JSON_canonical> --output <thư_mục_mới_trong_audit>`. Cổng này kiểm danh mục, độ phủ nguồn, quan hệ và bảng di trú; không là nghiệm thu QMD/HTML. Kiểm nguồn sau áp dụng phải xác minh owner Ôn nền độc lập, ID không đổi, chức năng/độ lộ không bị đổi bởi tên, dãy số không đặt lại qua chặng, đề–đáp án khớp và nhãn không lặp. Trạng thái mapping_only không được báo là source_applied.

Những câu chữ riêng, số cụ thể, anchor con dự kiến hoặc phân loại cần quyết định phải ghi riêng, không âm thầm chốt bằng checker. Không dùng regex đếm hộp làm số định nghĩa/ví dụ; kiểm đơn vị thực và nguồn dùng lại. Test metadata không thay kiểm hiển thị/trình duyệt, toán và DH01–DH14. Khi sửa QMD sau này, cập nhật binding/hợp đồng đầu ra đúng phạm vi rồi kiểm lại; lượt đồng bộ này không cho phép render/PDF/phát hành.

**Kích hoạt tại bước dựng nguồn/bản xuất:** yêu cầu “dựng QMD”, “dựng HTML” hoặc chuyển một gói mới tự kích hoạt [07/6.2](07_quy_chuan_cau_truc_trang_nguoi_hoc.md#hệ-nhãn-qd_025-và-mục-lục). Với gói dựng mới, `giao_dien/he_nhan.json` là bảng áp dụng hiển thị hiện hành; không tạo thêm một bảng số/tên độc lập cạnh nó. Bảng `ap_dung_he_nhan.json` và cổng `labels --application` ở trên phục vụ rà/di trú hệ cũ và giữ đúng phạm vi của chúng. Không lấy kết quả mapping_only hoặc kiểm metadata làm bằng chứng nhãn đã hiện trong HTML.

Thứ tự bắt buộc: kiểm kê vai trò và ngữ cảnh → hoàn chỉnh binding → kiểm nguồn → áp dụng nhãn dùng chung → dựng HTML → kiểm nhãn DOM và nhìn thực tế. `zo_course_labels.py` đọc từ vựng/mẫu hiển thị trong danh mục; cổng nguồn và đầu ra được gọi trong vòng đời QMD/Quarto, không phụ thuộc agent nhớ chạy một lệnh ngoài. Kiểm âm tối thiểu: mất nhãn nhưng metadata còn nguyên, thiếu context/binding, reset số sau chặng, sai owner, và nhãn VÍ DỤ thừa. Chỉ trình HTML sau khi khép các lỗi trong phạm vi; không mở PDF/phát hành qua bước này.

### 2.5. Tài nguyên toán trước viết và trước chuyển nguồn

Tự nạp 07/6.1.2 khi công việc có đồ thị/BBT. GRAPH-G03-01 lấy G03 làm đối chứng khung và tỉ lệ đồ thị, gọi `--layout lesson-g03` cùng bộ đặt cỡ dùng chung; kiểm hình ghép theo từng ô. Không quay về cỡ CSS tự nhiên đã bị thay. Lập ma trận theo vai trò trước sản xuất; đối chứng gói có đúng loại tài nguyên, không chọn G03 vì mới hơn để suy rằng JSON BBT rỗng là hợp lệ. BBT dùng một JSON và lời gọi từ QMD; hình trong bài và bìa có cấu hình riêng. Đọc và xem sản phẩm đối chứng thực, không dùng bảng kiểm chỉ ghi “profile 0.4” hoặc “đã phân loại” làm kết luận nhất quán.

Chạy cổng nguồn tự động trước render, cổng HTML sau render và các thử âm của 07. Khi dữ liệu/phần triển khai đổi, kiểm lại đúng tài nguyên chịu ảnh hưởng; không dựng PDF học liệu hoặc website toàn bộ. Nếu bộ dựng chung chưa diễn đạt được giới hạn một phía, sửa bộ dựng và kiểm tương thích, không chuyển sang bảng thường hoặc gộp mất dữ kiện. Hồ sơ phải chỉ ra nguyên nhân → nguồn sửa → guard → kết quả thực → phần chờ duyệt. Không chỉnh receipt lịch sử; ưu tiên báo cáo mới dẫn đúng bản nguồn.

## 3. Báo cáo đối chiếu tối thiểu

Với lượt sửa bảng QD_030, kiểm kê toàn bộ bảng của từng bề mặt (kể cả trong disclosure), ánh xạ theo chức năng tại 07/6.1.1 trước dựng. So từng ô văn bản/TeX/JSON và ID; kiểm kiểu, ngữ nghĩa hàng/cột, lưới, cỡ chữ, màu nhấn hợp lệ, local scroll/focus khi cần và no page overflow. Có ca âm chặn bảng thiếu/trùng/chưa phân loại, dữ liệu native sai và runtime căn sai/mất lưới. Bằng chứng cần mang revision `table_language` của cổng điều hành; báo cáo cũ dùng quy tắc căn trái đại trà không chứng nhận phần bảng mới. Không đổi toán hoặc sao chép quota G01; chỉ 03 ghi trạng thái, 07 sở hữu quy tắc.

Khi sản xuất hoặc rà hoạt động Kiểm tra của bất kỳ gói nào trong chương trình, kiểm QD_024 tại 01/2.3.1: điểm vào không đòi bài làm độc lập trước đó; một lượt không được chia thành nhiều đợt; tự tin không thay bằng chứng đạt mục tiêu. Đối chiếu đồng thời Cách học, Khởi động/định tuyến, hướng dẫn trước đề, Nhật kí và bản xuất có liên quan. Ghi riêng trạng thái quy tắc đã đồng bộ và sản phẩm chưa áp dụng/chưa kiểm; không dùng PASS tài liệu để chứng nhận nội dung người học. Bằng chứng kiểm hai quy tắc này phải gắn chủ đề `assessment_policy`/QD_024; không tái sử dụng kiểm theo điều kiện vào Kiểm tra cũ.

Mỗi phát hiện cần có mã, yêu cầu nguồn, vị trí repo, điều quan sát được, mức ảnh hưởng, sửa đề xuất và phép kiểm. Không viết “cần đồng bộ kiến trúc” nếu chưa chỉ được đường học nào hở.

| ID | Yêu cầu | Bằng chứng trong repo | Kết luận | Sửa và phép kiểm |
|---|---|---|---|---|
| Điền khi kiểm | Tệp và mục cụ thể | Đường dẫn + anchor/hàm/đoạn; ảnh nếu cần | Đã đáp ứng / Còn thiếu / Không còn áp dụng / Chưa kiểm | Việc cụ thể và kết quả mong đợi |

Ưu tiên lỗi toán, phạm vi và đường bắt buộc bị tắc. Đề xuất đẹp hơn hoặc thêm tiện ích đi vào danh sách làm sau nếu không phá điều kiện nghiệm thu.

## 4. Bốn trạng thái độc lập


| Trạng thái | Bằng chứng cần có |
|---|---|
| Nội dung đã kiểm tra | Đề, lời giải, hình và tiêu chí đúng; phạm vi phù hợp |
| Đường học đã kiểm tra | Mọi quyết định có đích dùng được; có câu xác nhận và đường quay về |
| Bản xuất đã kiểm tra | HTML/PDF thể hiện đúng nội dung, vai trò và tương tác cần thiết |
| Đã phát hành | Bản công khai và tệp tải khớp phiên bản đã được chấp nhận |

`planned=0`, đủ số câu, liên kết tồn tại hoặc dựng thành công chỉ là một phần của bằng chứng. Không dùng chúng thay cho bốn trạng thái trên. Đồng thời không bắt R1-G01 phải chứng minh hiệu quả dài hạn trên điểm thi rồi mới được phát hành một bản học liệu đúng và có thể dùng.


## 5. Hợp đồng HTML dùng chung


Nguồn QMD/DOM cần có trật tự đúng trước khi chạy JavaScript. Bài học và Luyện tập không xen kẽ; liên kết xem lại theo nhu cầu có đường đi/về rõ, không biến thành thứ tự luân phiên bắt buộc. Tài nguyên sửa lỗi chỉ có một bản nội dung, được gọi từ nhiều nơi.

Lưu ngữ cảnh tối thiểu gồm: bài hoặc Điểm dừng đang gọi hỗ trợ, lượt học hiện tại và đích quay về. URL hoặc cơ chế tương đương phải bảo toàn ngữ cảnh khi chuyển giữa phần học, lời giải và sửa lỗi. Không dùng một biến “lượt ôn gần nhất” chung cho mọi tab nếu nó có thể làm hai lượt ghi đè nhau.

Khi truy cập trực tiếp vào bài sửa mà không có nơi gọi, hiển thị rõ các Điểm dừng phù hợp để người học chọn lại. Không giả định CP-ON1. Bản in ghi tên và vị trí các điểm quay về, không giả vờ có cơ chế động.

Các yêu cầu trước khi làm Kiểm tra và trước khi tự làm câu xác nhận phải hiển thị sẵn. Lời giải của bài độc lập mặc định đóng. Ví dụ đang dùng để hướng dẫn được trình bày theo mục đích dạy học. Việc giấu đáp án không bảo đảm người học chưa thấy bài; nhật kí vẫn phải ghi mức hỗ trợ và lịch sử gặp câu.

Không cần đăng nhập hay hệ thống theo dõi tự động để đạt hợp đồng tự học đầu tiên. Nhật kí giấy và liên kết rõ ràng đủ cho bản này, miễn không quảng bá chức năng lưu tiến độ tự động khi chưa có.

[Quy chuẩn cấu trúc trang người học](07_quy_chuan_cau_truc_trang_nguoi_hoc.md) là hợp đồng đầy đủ về mạch chính, lớp hỗ trợ, thứ tự DOM, bảng, trạng thái thu gọn, responsive, khả năng truy cập và cổng khóa PDF. Hồ sơ gói chỉ ghi các tình huống và ngoại lệ riêng, không tạo một quy chuẩn giao diện song song.


## 6. Điều kiện nghiệm thu chung

- Nội dung: đề, dữ kiện, lời giải, hình và phạm vi nhất quán; mỗi mục tiêu thiết yếu có bằng chứng phù hợp.
- Đường học: mỗi quyết định có tài nguyên thật, cách xác nhận và đường quay về; có xử lý khi đã xem lời giải hoặc hết câu mới.
- Bản HTML: điều hướng, lời giải, liên kết sâu, Back/tải lại và bố cục thực chạy được kiểm trên máy tính, điện thoại và bàn phím ở các đường có ảnh hưởng.
- Bản PDF: kiểm danh sách tệp thực, phiên bản, nội dung và vị trí tra cứu; không mặc định số PDF của gói khác.
- Chấp nhận: ghi rõ người chủ trì chấp nhận bản nào, lúc nào, còn giới hạn gì. Chỉ đánh dấu phần đã có bằng chứng.

Hồ sơ từng gói phải có tình huống kiểm cụ thể. R1-G01 dùng Mục 5.4 trong hồ sơ G01; G02 có bảng kiểm riêng.

Đối với component dùng chung, kiểm HTML phải phân biệt: kiểm mã/DOM; kiểm trình duyệt trên bản vừa dựng; kiểm hồi quy các gói bị tác động; và sự chấp nhận của người chủ trì. Bằng chứng hình ảnh dùng lát cắt đủ đọc ở 1440, 430 và 390 px; ảnh toàn trang thu nhỏ không thay cho việc quan sát nội dung.

Sau kiểm nội bộ, tổ chức thử với người học phù hợp khi có điều kiện. Ghi đúng “chưa thử với người học” nếu chưa có; không dùng tự đánh giá của AI thay cho quan sát thật, không tự tuyên bố hiệu quả điểm thi.

Được dừng vòng sửa khi mọi lỗi chặn trong phạm vi đã xử lý và điều kiện nghiệm thu được đáp ứng. Không kéo dài vòng sửa vì một cải tiến ngoài phạm vi không chặn người học.

## 7. Bảo toàn repo và kiểm ảnh hưởng

- Không dùng `git add .`; stage từng tệp có chủ đích. Không reset/checkout/revert đè lên diff sẵn có của người dùng.
- Báo cáo, ảnh kiểm, bản thử và đầu ra tạm để dưới `_audit/`. Bản phát hành đi đúng quy trình repo.
- Không sửa thủ công CSS đã xuất trong `docs/`; sửa nguồn. Giữ URL và tên tệp hiện hành trừ khi việc đổi được giao rõ.
- Tránh CSS riêng lẻ khi đã có thành phần chung. Không tái thiết kế thương hiệu trong lượt sửa kiến trúc học tập. Dùng token Đỏ ZO, Vàng ZO, Xám ZO đã được chốt trong nguồn thực; bộ điều hành này không quy định mã màu.
- Nếu sửa CSS/script/filter dùng chung, liệt kê gói bị tác động và kiểm hồi quy trên các gói ấy. Không chỉ kiểm trang đang sửa.
- Dùng “tập xác định”. Công thức Markdown dùng `$...$`, `$$...$$`; ưu tiên giải thích bằng câu văn, không dùng `\qquad`.
- Không tạo phụ thuộc mới, tài khoản hay tự động chấm chỉ để đạt đường tự học đầu tiên.

## 8. Phân loại sau phát hành

Lỗi làm sai kiến thức, sai lời giải hoặc tắc đường bắt buộc cần một lượt sửa có phạm vi rõ và cập nhật bản xuất chịu ảnh hưởng. Cải tiến không chặn được xếp sau công việc sản xuất đang mở. Một lỗi riêng của gói chỉ mở lại chuẩn chung khi chứng minh được quy tắc chung gây lỗi.

## 9. Ghi bằng chứng

Báo cáo trong `_audit/` có thể không được Git theo dõi. Vì vậy hồ sơ gói phải giữ kết luận, đường dẫn nguồn, lệnh kiểm cần thiết, kết quả và hạn chế đủ để tiếp quản; không chỉ ghi “xem file trong _audit”. Với bằng chứng cần giữ lâu dài, trích kết luận vào hồ sơ và gắn commit thật khi có. Không bịa hash hoặc ngày chấp nhận.

## Ch?n ?nh ??i di?n khi d?ng g?i m?i

Theo ph? duy?t c?a ch? tr? ng?y 17/10/2026, khi chu?n b? d?ng QMD/HTML,
agent ph?i kh?o s?t h?nh trong n?i dung g?i, ch?n ph??ng ?n ??i di?n r?
cho ki?n th?c ch?nh, gi?i th?ch l? do v? tr?nh ch? tr? duy?t tr??c khi d?ng.
Kh?ng m?c nhi?n k? th?a ?nh c?a g?i m?u. N?u ch?a c? h?nh ph? h?p, ?? xu?t
h?nh m?i; t?i nguy?n ch?nh th?c ???c t?o b?ng c?ng c? ZO Math hi?n h?nh.
?nh trong su?t; khung hi?n th? thu?c m?u trang, kh?ng thu?c b?n th?n ?nh.

Sau duy?t, khai b?o t?i `giao_dien/anh_bia.json` c?a ch?nh g?i:
`schema_version: 1`, `package`, `image` (t??ng ??i t? th? m?c g?i),
`sha256`, `selection_reason`, `approval: approved`, `approval_evidence`.
B?ng ch?ng duy?t ph?i ch? ??n ph?n h?i/h? s? th?c t?; agent kh?ng t? duy?t.
?nh ??i ph?i ???c xem x?t l?i, kh?ng ch? c?p nh?t hash ?? v??t c?ng.
Kh?ng t?o tr??c th? m?c g?i t??ng lai.

???ng d?ng HTML canonical t? g?i `scripts/zo_course_cover.py` tr??c v? sau
adapter: thi?u khai b?o, ?nh ngo?i g?i, ?nh ch?a duy?t, hash sai, tr?ng ?nh
?? khai b?o c?a g?i kh?c ho?c HTML hi?n sai ?nh ??u ch?n d?ng. M?y ki?m
binding v? b?n ?nh; m?c ?? ??i di?n do agent ?? xu?t v? ch? tr? ??nh gi?.
Kh?ng c? ?nh m?c ??nh khi thi?u khai b?o. Ki?m tr?c quan sau d?ng v?n c?n
x?c nh?n ?nh ??ng n?i dung, trong su?t, kh?ng m?o/c?t ? m?n h?nh r?ng/h?p.

### Bổ sung cổng nhãn cấp chứa, 17/10/2026 (mục 2.4)

Khi dựng/hiệu chỉnh nhãn, nạp quy tắc 07/6.2 và label_contract.display_contract.context_labels. Kiểm kê owner/tiêu đề/nhãn trước–sau; G04 và gói mới khai context_labels: parent-context-v1. Cổng nguồn/HTML kiểm cấp cha, dấu “ · ” và nhãn cùng vùng; không chép nhãn riêng của adapter hoặc lấy giá trị tương thích cũ làm mẫu. Kiểm phần nhãn/bố cục/điều hướng chịu ảnh hưởng; không dựng lại hình/PDF. Bằng chứng và việc tiếp theo ở hồ sơ gói/03. Hiệu chỉnh hiển thị không đổi nghĩa toán, ID hoặc dãy số.

### Kiểm component shell trước bàn giao — DRAWER-ICON01

Nút mục lục trong trang theo 07/6 và hợp đồng kit là component dùng chung, không thuộc mục tải PDF. Nạp template/CSS/runtime shell canonical; không lấy hiện thực nằm trong mô-đun PDF của G01/G02 làm tiền đề cho gói mới. scripts/zo_web_2027_shell.py kiểm template trước ghép và HTML/runtime CSS sau adapter. Kiểm thực tế trên màn hình hẹp cả trang chưa có PDF, sau đổi view/tải lại, bàn phím/đóng/chọn đích/resize; đối chiếu với nút icon đã chốt. Cổng chỉ kiểm click được hoặc tệp CSS tồn tại không chứng nhận đúng thiết kế. Thử âm phải bắt chữ view lộ ra, thiếu icon/tên truy cập, sai kích thước hoặc đích dialog. Không dựng lại hình/PDF chỉ vì sửa nút.
