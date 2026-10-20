# Quy chuẩn tổ chức học liệu Ôn thi Toán THPT

Phiên bản tài liệu: 0.9 · Ngày biên tập: 16/10/2026 · Căn cứ: phần còn hiệu lực của QD_016–032 và QD_033.

Tài liệu nội bộ, chỉ áp dụng cho chuyên mục này. Tài liệu quy định kiến trúc nguồn, ranh giới xuất bản và hợp đồng canonical cho thành phần học liệu; việc một component được mô tả ở đây không tự động có nghĩa component đó đã được triển khai hoặc kiểm định kỹ thuật.

## Một bộ nguồn hiện hành

- Mỗi gói dùng lại nằm tại `hoc_lieu/<ma_goi>/`, độc lập với năm thi.
- `index.qmd` là nguồn biên soạn văn bản duy nhất của gói sau khi chuyển đổi được nghiệm thu. Dữ liệu có cấu trúc và tài sản hình được dẫn chiếu, không chép thành một nguồn bài học thứ hai.
- HTML/PDF là đầu ra sinh, không sửa tay. Mốc lịch sử không được tiếp tục dùng như nguồn phát triển song song.
- Trang khóa `tot_nghiep_thpt/<nam>/index.qmd` dẫn tới học liệu dùng lại; không sao chép bài vào từng khóa.
- Điều hành khóa và hồ sơ nội bộ nằm trong `_quy_trinh`, không đưa nguyên tài liệu điều hành lên trang người học.

## Khởi tạo gói mới và quản lí bản thảo

Theo yêu cầu chủ trì ngày 16/10/2026, cách tổ chức G03 là cách khởi tạo dùng cho R1-G04 và các gói tiếp theo khi được giao. Đây là nền tổ chức hiện hành để tiếp tục cải tiến theo thực tế, không phải khuôn cố định về số bài, số hình hoặc nội dung học.

Việc biên soạn dùng [mẫu bản thảo](mau/ban_thao_goi.md) và [bảng kiểm](mau/bang_kiem_ban_thao_goi.md); quy trình tự gọi từ yêu cầu tự nhiên, đối chiếu trước viết và kiểm trước trình do [02/1.4](02_quy_trinh_va_nghiem_thu.md#ap-dung-mau-ban-thao) sở hữu. Mẫu nội dung khác mẫu trang: mẫu trang tiếp tục dùng kit theo 07, không chép CSS/JS vào bản thảo. Kết quả áp dụng và phiên bản mẫu nằm trong `ho_so/` của gói; mẫu chung không ghi trạng thái riêng.

Trước khi tạo thư mục của một gói, trình bày mã gói, đường dẫn, vai trò các phần và phạm vi sẽ tạo; chỉ thực hiện trong nhiệm vụ đã được chủ trì giao/chốt. Không tạo trước các gói tương lai. Nếu cần thêm nơi lưu trữ hoặc thay cấu trúc đã thống nhất, trình phương án để chủ trì chốt trước khi tạo; không tự sinh bản sao hoặc kho lưu trữ song song.

Khi bắt đầu biên soạn, dùng cấu trúc sau trong `hoc_lieu/<ma_goi>/`:

```text
_quy_trinh/
├── README.md
├── ban_thao/
│   ├── noi_dung.md
│   └── hinh/       # khi bản thảo có tài nguyên hình
└── ho_so/          # khi có biên nhận/kết quả kiểm cần giữ
```

- `_quy_trinh/README.md` là điểm vào quản lí gói, dẫn tới bản thảo và hồ sơ của khóa. Bản thảo đang sửa chỉ có một nguồn `ban_thao/noi_dung.md`; tài nguyên của nó nằm trong vùng bản thảo, tách khỏi tài nguyên chính thức.
- Hồ sơ phạm vi đặt tại `tot_nghiep_thpt/<nam>/_quy_trinh/goi/`; đề cương và ma trận chỉ lập khi cần, giữ vai trò chỉ mục/độ phủ và dẫn tới bản nội dung, không chép thành ngân hàng song song. Trạng thái và việc tiếp theo của khóa chỉ ghi tại 03.
- Chỉ chuyển bản thảo sang `index.qmd` sau khi chủ trì duyệt. Giữ bản đã duyệt cùng tài nguyên làm căn cứ đối chiếu; sau khi chuyển đổi được kiểm và nghiệm thu, QMD là nguồn biên soạn chính thức duy nhất, không sửa tiếp hai bản song song.
- Tài nguyên chính thức được tạo từ đầu vào toán đã duyệt bằng công cụ ZO Math đang áp dụng, theo cùng hợp đồng nguồn/dữ liệu/hình/giao diện của G01/G02. Dựng và kiểm lại đầu ra; không lấy SVG/PDF bản thảo làm tài sản chính thức bằng cách sao chép hoặc đổi tên, không cho build chính thức phụ thuộc `ban_thao/`.
- Cấu hình QMD, manifest, binding, `du_lieu/`, `hinh/`, `giao_dien/` và công cụ riêng chỉ tạo lúc thực sự triển khai. Không sao cấu hình, mã nhiệm vụ, quota, script hoặc trạng thái nghiệm thu riêng của gói trước để lấp cấu trúc.
- Khi khép một mốc tổ chức/bản thảo, kiểm liên kết, nguồn đang sửa duy nhất, tài nguyên và phạm vi thay đổi. Commit khi được chủ trì giao; commit bảo toàn mốc làm việc không thay nghiệm thu nội dung hoặc quyền phát hành.

Nếu thực tế cho thấy cần cải tiến, ghi yêu cầu và phạm vi ảnh hưởng, cập nhật quy tắc tại mục này cùng các chỉ dẫn/mẫu bị ảnh hưởng trong cùng lượt được giao. README gói và mẫu hồ sơ dẫn về đây; không duy trì nhiều định nghĩa độc lập về cách khởi tạo.

## Cổng điều hành trước sản xuất

Theo QD_033 và QD_022/02/1.2, xác minh registry phụ thuộc trước biên tập và kiểm đầu ra. Khi đổi quy tắc/guard, báo cáo cũ mất hiệu lực trong phạm vi bị ảnh hưởng; không đổi QMD hoặc metadata để giả đạt. Sơ đồ/lời dẫn/routing phải khớp 14 tình huống 01/2.2.2. Không để adapter suy kiến trúc hoặc chép ghi chú biên tập lên trang người học. Đây là cổng điều hành/nghiệm thu; không tuyên bố CLI Quarto/PDF đã tự khóa mọi trường hợp. Chưa cho phép dựng PDF hoặc phát hành từ việc tài liệu đạt.

QD_033: thứ tự mục lục không là quy trình học bắt buộc. Bốn khu vực và các hỗ trợ giữ chức năng/owner độc lập theo 01/2.2.1, 07/2–3; điểm vào theo nhu cầu, mức chuẩn bị và bằng chứng. Kiểm tra tự lực trong lượt; kết thúc lượt trước trợ giúp, giữ riêng bài ban đầu. Lưu bằng chứng ở Điểm dừng không bắt ghi Nhật kí ở mọi điểm; giữ 14 trường, ghi theo ngữ cảnh. Các ngoại lệ liên kết tại chỗ dưới đây thay mệnh lệnh hai chiều vô điều kiện, không thay ID hoặc trạng thái thu gọn.

## Hợp đồng nhãn QD_025 (kế thừa QD_023)

Danh mục tên/khóa/phạm vi chỉ ở `danh_muc_kien_truc_hoc_tap.yml:label_contract`, phiên bản 1. ID, văn bản, tiêu đề nội dung và loại của đơn vị thuộc QMD canonical; manifest sở hữu các quan hệ chức năng/mục tiêu/độ lộ đã có; layout chỉ sở hữu nhịp đọc và phép chiếu. Không nhập cùng một tiêu đề toán độc lập vào nhiều tệp.

Bảng áp dụng `_quy_trinh/ap_dung_he_nhan.json` giữ selector, quan hệ và trạng thái; không được nạp làm nguồn nội dung build. Hợp đồng bảng nằm trong `schema_kien_truc_hoc_tap.json#/$defs/label_application`, có `schema_version: 1`, `label_contract_version: 1`, `decision: QD_025`; `status` phân biệt `mapping_only` và `source_applied_pending_html_acceptance`. Loader báo lỗi trường/phiên bản lạ. G01 đã áp dụng nguồn: `giao_dien/he_nhan.json` là binding hiển thị canonical theo bản chốt, không chép toán; `zo_r1_g01_labels.py` nối metadata vào phép chiếu HTML và từ chối đích thiếu. G02 đã có binding riêng cùng hợp đồng hiển thị tại DH_016; `zo_r1_g02_labels_check.py build/check` nối/kiểm tường minh 59 nhiệm vụ và xuất kiểm kê nguồn tươi. Không nạp bảng kiểm kê audit làm nguồn build; CLI bảng di trú G01 vẫn không tự thành renderer cho mọi gói. Schema manifest kiến trúc 1/0.2 giữ nguyên.

Phép kiểm `zo_learning_architecture.py labels` xuất kiểm kê từ nguồn mới và annotations đã đọc, gồm heading, ID, các khối có vai trò, include, nhiệm vụ/đáp án, bảng/hình và dẫn chiếu. Locator chưa có ID được báo rõ, không giả thành anchor đã tồn tại. Mỗi đơn vị có một owner; số theo gói không ghi cứng vào include dùng chung. Một ví dụ nhiều bước, hai định nghĩa cùng hộp và một nguồn Nền dùng ở hai gói phải được đếm đúng quan hệ. Mỗi loại hiển thị dùng một dãy số liên tục riêng từ 01 theo thứ tự xuất hiện trong toàn gói; không đặt lại theo mục, chức năng, chặng, lượt hoặc khu vực. Tất cả nhiệm vụ, kể cả tự làm trong Bài học, Khởi động, Luyện tập, Kiểm tra, Ôn lại, Ôn nền và Sửa lỗi, dùng chung dãy Nhiệm vụ. “Tự kiểm tra” đổi thành “Nhiệm vụ”; chức năng nội bộ vẫn giữ để phân biệt vai trò sư phạm. Gợi mở, Ví dụ và Điểm dừng có dãy riêng. Đề và lời giải dùng cùng số, không đếm lại lời giải; ID giữ nguyên. Include dùng chung không chứa số riêng của gói. Dẫn chiếu, bảng, mục lục và liên kết đi–về dùng cùng ánh xạ theo ID.

Metadata/nhãn thiếu không được bỏ qua để build tiếp. Bản nguồn chưa di trú tiếp tục dùng hợp đồng kỹ thuật cũ cho chẩn đoán, nhưng không được chứng nhận là sản phẩm đã đạt QD_025. Sau khi có quyền sửa QMD, ánh xạ được duyệt phải được tích hợp vào nguồn/manifest/binding và filter cùng lượt; không dùng bảng audit hoặc fallback đoán theo heading để dựng production. Gợi mở là chức năng riêng trong danh mục, không nhập vào nhiệm vụ tự làm sau học hoặc tạo lời giải trùng lời giảng. Hệ nhãn áp dụng toàn bộ các gói chương trình; chỉ dùng những loại/chức năng thật sự có trong gói.

### Cổng nhãn khi chuyển QMD và dựng HTML

Khi bắt đầu dựng gói, tự nạp 07/6.2 và 02/2.4, hoàn chỉnh `giao_dien/he_nhan.json` từ nội dung thật. Gói dựng mới khai `display_contract: qd025-display-v1`; danh mục chung sở hữu mẫu nhãn, binding gói sở hữu ngữ cảnh, số/tên và owner. Dùng `scripts/zo_course_labels.py`, không sao bộ gán nhãn riêng của một gói. CLI QMD, launcher Quarto và cổng HTML kiểm việc áp dụng; metadata đúng nhưng thiếu nhãn nhìn thấy vẫn thất bại. G01/G02 giữ adapter hiện hành, không tự mở lượt di trú lại. Mô tả/ngoại lệ và kiểm thực tế theo 07; không lập thêm tài liệu chuẩn nhãn song song.

## Lớp tương thích và binding HTML 2027

Chủ sở hữu chức năng học tập là 01, cấu trúc người học là 07; danh mục 08 phân vai nguồn. Bảng vai trò dưới đây giữ ngữ nghĩa và lớp khối QMD tương thích. Với HTML opt-in kit 2027 đã duyệt, màu/surface trình bày do binding kit ánh xạ (một cấp giấy, nhãn trong vùng); không bọc thêm khối đỏ/xám/vàng bên trong giấy chỉ để tái hiện CSS legacy. Không vì binding cục bộ mà đổi quy chuẩn khối toàn repo hoặc PDF.

`guidance` là hướng dẫn bổ trợ có thể thu gọn; nếu chứa điều kiện bắt buộc của hoạt động thì phải kiểm vai trò và vị trí theo 01/07, không máy móc giấu hết dưới hộp đóng. “Mặc định đóng” chỉ áp dụng hộp có trạng thái đóng/mở; nhiệm vụ và mạch chính vẫn mở cố định. Hình/bảng/action nằm trong vùng sở hữu, một đích lời giải mỗi nhiệm vụ, không chèn link lặp.

Nguồn QMD/cấu hình của D0, G01, G02 đã tồn tại; đoạn về pha tích hợp bên dưới là hợp đồng cho gói mới, không trạng thái “chưa tích hợp” của ba gói này. HTML G01 đã nối kit/hình native; G02 đã nối adapter canonical và dựng HTML cô lập; D0 dùng hợp đồng HTML-only riêng. Schema/checker không kiểm hết ý nghĩa của văn bản. Ma trận số trang PDF và số vùng ở các mục lịch sử chỉ đúng bản cũ; khi được giao PDF phải đối chiếu đầu ra thật, không lấy số cũ làm tiêu chuẩn cho nguồn đã đổi.

## Hợp đồng cho pha tích hợp gói mới

Mỗi gói sẽ có cấu hình kỹ thuật cục bộ với định danh duy nhất và hồ sơ `_quy_trinh/ho_so/index.yml`, cùng dùng hợp đồng và bộ kiểm định chung của chuyên mục. Cách này tránh va chạm hồ sơ giữa các nguồn cùng tên `index.qmd`.

Mẫu `mau/ho_so_goi.md` ghi các quyết định cần có nhưng không phải schema được CLI hỗ trợ. Không suy trạng thái tích hợp, nghiệm thu hoặc xuất bản từ việc đã tạo hồ sơ theo mẫu.

Khi chuyển đổi được giao ở pha sau, phải bảo toàn nội dung, nhiệm vụ, thuật ngữ, ID, bảng và hình; kiểm chứng HTML tương tác và toàn bộ PDF. Phân biệt kiểm định tự động, nghiệm thu của con người và quyết định xuất bản. Không tự đổi trạng thái nghiệm thu/xuất bản.

## Hợp đồng canonical cho thành phần học liệu

Hợp đồng này là quy chuẩn cục bộ dùng chung cho các gói học liệu trong chuyên mục. R1-G01 và R1-G02 là hai trang kiểm chứng hợp đồng, không gói nào tự thân là toàn bộ quy chuẩn. Hiện trạng riêng của một gói chỉ trở thành baseline dùng chung khi thay đổi tương ứng đã được ghi vào tài liệu này, triển khai trên thành phần dùng chung và nghiệm thu trên các gói chịu ảnh hưởng.

### Trình tự quyết định

Khi tổ chức một nội dung, thực hiện theo thứ tự:

1. Xác định nội dung có cần tách thành khối hay hệ tiêu đề và văn bản thông thường đã đủ rõ.
2. Xác định vai trò nhận thức của nội dung theo bảng dưới đây.
3. Xác định nội dung thuộc mạch chính hay phần hỗ trợ để chọn trạng thái mở hoặc thu gọn.
4. Chọn biến thể trình bày và màu theo chức năng; không chọn màu để trang trí.
5. Gắn ID và quan hệ điều hướng nếu nội dung có gợi ý, lời giải hoặc tham chiếu chéo.

Không biến mọi đoạn quan trọng thành khối. Không đặt nhiều khối liên tiếp nếu chúng không tạo thành một đơn vị đọc có quan hệ nội tại rõ ràng.

### Các vai trò canonical

| Vai trò | Chức năng | Trạng thái mặc định | Yêu cầu |
|---|---|---|---|
| `guidance` | Chỉ dẫn cách học hoặc một tiến trình thực hiện | Thu gọn | Dùng danh sách số khi thứ tự bắt buộc, dấu chấm khi các ý song song, hoặc một đoạn văn cho chỉ dẫn ngắn. |
| `task-pause` | Câu hỏi dừng trong mạch bài học | Mở cố định | Ngắn, có hành động rõ và có ID nếu dẫn tới gợi ý hoặc lời giải. |
| `task-item` | Bài luyện tập, kiểm tra, sửa lỗi hoặc nhiệm vụ độc lập | Mở cố định | Có ID riêng; dùng trình bày trung tính để một dãy bài không tạo quá nhiều khối nặng. |
| `example` | Ví dụ đã được giải hoặc phân tích ngay trong mạch chính | Mở cố định | Không tạo thêm lời giải trùng lặp ở phần cuối. |
| `theory` | Định nghĩa, định lí, tính chất hoặc kết quả tổng quát | Mở cố định nếu thuộc mạch chính | Dùng khối đỏ theo quy chuẩn khối nội dung chung. |
| `context-note` | Giải thích, phân biệt, chứng minh hoặc lưu ý phụ thuộc ngữ cảnh | Mở hoặc thu gọn theo vai trò trong mạch | Dùng khối xám theo quy chuẩn khối nội dung chung. |
| `extension` | Bài viết nhỏ tương đối độc lập hoặc nội dung mở rộng | Thu gọn | Dùng khối vàng; không dùng màu vàng chỉ vì nội dung là ví dụ hoặc hoạt động. |
| `hint` | Gợi ý cho một nhiệm vụ cụ thể | Thu gọn | Tách khỏi `guidance`, đặt gần nhiệm vụ và có quan hệ đích rõ ràng. |
| `solution` | Lời giải, đáp án hoặc hướng dẫn chấm | Thu gọn | Một nhiệm vụ độc lập có một đích lời giải xác định; chỉ cần liên kết quay lại đề khi đề và lời giải thực sự ở hai vị trí tách biệt. |
| `answer-link` | Điều hướng giữa nhiệm vụ, gợi ý và lời giải | Không phải khối nội dung | Đặt sát đối tượng nguồn hoặc đích; nhãn phải mô tả đúng hành động và đích đến. |
| `figure-table` | Bảng, bảng biến thiên, hình hoặc đồ thị | Mở cố định | Dùng component và caption chuyên biệt; không dùng khối màu để thay thế cấu trúc hình hoặc bảng. |

Không bắt buộc một gói phải dùng đủ mọi vai trò hoặc đủ ba màu. Số lượng khối phải do nội dung quyết định, không dùng chỉ tiêu số lượng để làm trang giống một gói khác.

### Quy tắc cho khối `guidance`

`guidance` chỉ chứa hướng dẫn điều phối việc học hoặc một quy trình có phạm vi rõ. Không xếp câu hỏi, bài tập, ví dụ, kết luận, tiêu chí toán học, gợi ý cục bộ hoặc lời giải vào `guidance` chỉ vì nội dung có động từ mệnh lệnh.

- Dùng danh sách đánh số khi bước sau phụ thuộc bước trước hoặc thứ tự thao tác ảnh hưởng kết quả.
- Dùng danh sách dấu chấm khi các thao tác độc lập, có thể đổi thứ tự hoặc chỉ là các điểm cần lưu ý.
- Dùng một đoạn văn khi chỉ có một chỉ dẫn ngắn và không cần tách thành nhiều ý.
- Không trộn thời lượng, mục đích và chuỗi thao tác thành các bước ngang hàng nếu chúng không cùng cấp logic.

### Quy tắc cho nhiệm vụ và ví dụ

`task-pause` và `task-item` là hai biến thể của cùng vai trò nhiệm vụ, nhưng khác cường độ trình bày:

- `task-pause` dùng để ngắt mạch đúng lúc và buộc người học tự dự đoán, kiểm tra hoặc trả lời trước khi đọc tiếp;
- `task-item` dùng cho các bài trong một dãy luyện tập, kiểm tra hoặc sửa lỗi; phải đủ rõ để được dẫn chiếu độc lập nhưng không cần hình thức thị giác nặng như một khối nhấn mạnh.

Một nội dung đã trình bày cả đề, lập luận và kết quả trong mạch bài là `example`, không phải `task`. Nếu người học phải tự làm trước rồi mới xem phần xử lí tách riêng, nội dung đó là `task` và phần xử lí là `solution`.

### Quy tắc tham chiếu nhiệm vụ, gợi ý và lời giải

- Nhiệm vụ độc lập có một đích lời giải xác định. Chỉ yêu cầu liên kết quay lại đề khi đề và lời giải thực sự ở hai vị trí tách biệt; khi tách vị trí, liên kết hai chiều một-một phải trỏ đúng cặp. Khi cùng tài nguyên/vùng đọc, dùng đối chiếu tại chỗ và đáp án thu gọn, không thêm liên kết nhảy thừa (07/3, 5.3).
- Nếu có gợi ý, nhiệm vụ dẫn tới đúng gợi ý; gợi ý phải cho phép quay lại nhiệm vụ mà không thay thế đích lời giải.
- Một nhóm câu hỏi rất ngắn có thể dùng lời giải tổng hợp khi việc nhóm có chủ ý sư phạm; mỗi câu vẫn phải có anchor đủ chính xác để người đọc quay lại vị trí tương ứng.
- Nhãn liên kết phải nêu đúng loại đích. Cặp đề–lời giải dùng hai nhãn ngắn `Xem lời giải` và `Xem đề bài`; chỉ thêm định danh vào nhãn khi một đích khác không thể được nhận biết từ ngữ cảnh.
- Không tạo liên kết tới một lời giải lặp lại đối với `example` đã được giải ngay trong mạch bài.

### Tiêu đề và ID

- Ưu tiên tiêu đề mô tả nội dung cụ thể; chỉ dùng tên chức năng như `Gợi ý` hoặc `Lời giải` khi không có tên cụ thể rõ hơn.
- Khối thuộc hệ `zo-block` phải dùng cấu trúc tiêu đề canonical của hệ khối; không giả lập tiêu đề bằng một dòng chữ đậm trong thân khối.
- Mọi nhiệm vụ, gợi ý và lời giải tham gia tham chiếu chéo phải có ID duy nhất, ổn định và không phụ thuộc vào số dòng hoặc văn bản tiêu đề tự sinh.
- Sau khi một gói được phát hành, không đổi ID nếu chưa có cơ chế tương thích cho liên kết cũ.
- Mã quản lí chỉ được đặt trong ID, thuộc tính dữ liệu, manifest, hồ sơ và checker. Văn bản người học nhìn thấy phải dùng tên học liệu, tên mục tiêu, tên lỗi, tên bài và tên điểm kiểm soát chính thức; không dùng mã mục tiêu, mã lỗi, mã tuyến sửa, mã Nền hoặc mã bảng biến thiên thay cho nhãn có nghĩa.
- Không lặp lại nguyên văn tiêu đề bằng một dòng nhãn ngay bên dưới. Nếu phần mở đầu cần mô tả, câu đó phải bổ sung thông tin mới.

## Baseline component 1.0 và trạng thái nghiệm thu hiện hành

Định danh baseline: `on-thi-learning-components/1.0`.

Baseline component 1.0 là nền kỹ thuật và tương thích của hai gói. Shell HTML hiện hành G01 đã nối kit opt-in; G02 có nguồn và HTML audit FB036. Thiết kế G01/HTML FB033 đã duyệt; bản sửa FB036 không tự kế thừa nghiệm thu ấy. Trạng thái ở 03/hồ sơ, không suy từ kiểm component. Ma trận PDF bên dưới là lịch sử; PDF hai gói chưa đồng bộ với nguồn mới và cần nhiệm vụ riêng.

[Quy chuẩn cấu trúc trang người học](07_quy_chuan_cau_truc_trang_nguoi_hoc.md) điều hành cấu trúc thông tin, thứ tự DOM, lớp hỗ trợ và cổng nghiệm thu. Tệp này điều hành component, ánh xạ kỹ thuật và phép chiếu đầu ra; không dùng một trong hai tệp để ghi đè trạng thái gói ở hồ sơ và bảng điều hành.

### Nguồn kỹ thuật dùng chung

- `assets/css/_zo_learning_components.scss` là nguồn trình bày chung cho các vai trò học liệu.
- `assets/lua/zo_learning_components.lua` là nguồn chuyển đổi chung từ vai trò QMD sang cấu trúc HTML.
- `assets/css/zo_on_thi_learning_package.css` cung cấp khung trang, thanh thẻ, bảng và hình dùng chung; scope canonical là `.zo-on-thi-package` và `body.zo-on-thi-package-page`.
- `assets/html/zo_on_thi_learning_package_script.html` cung cấp hành vi điều hướng, trạng thái thẻ, mục lục trong bài học và hỗ trợ cuộn bảng dùng chung.
- Hai tệp lịch sử `hoc_lieu/r1_g01/giao_dien/r1_g01.css` và `r1_g01_script.html` chỉ được giữ tạm để bảo toàn hồ sơ provenance của các PDF R1-G01 hiện có; QMD không được tham chiếu chúng. Chúng được loại bỏ cùng lúc tái lập provenance PDF ở pha PDF kế tiếp.
- CSS riêng của mỗi gói chỉ chứa ngoại lệ thật sự của gói; không sao chép component dùng chung để tạo baseline song song.
- `_design/web_2027_mau_dung_chung/` sở hữu shell/reading-region/controller/profile; `scripts/zo_web_2027_production.py` nối HTML Quarto mới từ QMD với layout G01. Layout chỉ là ánh xạ, không nguồn toán thứ hai; phải kiểm binding tươi trước dùng, không bỏ strict check khi QMD đổi. G02 dùng adapter canonical và lệnh cô lập trong README gói, không suy đã promotion vào `docs`.
- Hình web mới được nối qua `scripts/zo_web_2027_figures.py` và profile opt-in; tài sản nguồn/JSON canonical giữ nguyên. Script mới không biến HTML audit thành nguồn production.

### Bổ sung ánh xạ QD_028

Layout giữ toàn bộ DOM của bảng định tuyến, gồm href và ngữ nghĩa header, không chỉ gắn lại chữ trong ô. Khi nguồn đổi số đoạn hoặc thêm bảng, di trú binding tường minh từ raw trước/sau; strict fingerprint và kiểm ID/toán vẫn bắt buộc. Vùng tiêu đề rỗng phải bị guard từ chối. BBT bổ sung lấy dữ liệu canonical và có phép kiểm độc lập; cập nhật provenance HTML mới không được sửa receipt lịch sử hoặc tuyên bố PDF đã đồng bộ.

G02 dùng adapter canonical `zo_web_2027_g02_production.py` nhận raw Quarto mới như README vận hành; các lệnh audit trước DH_019 chỉ là lịch sử. Chưa promotion root docs không có nghĩa nguồn canonical chưa được tích hợp.

### Khung trang và điều hướng

- Một trang có bìa/nhận diện và vùng đọc theo hợp đồng 07; bìa phủ workspace, cột đọc có lề thở. Vùng đọc sở hữu nhãn/heading/nội dung/hình/chú thích/link, một inset và không giấy lồng. Tham số kit không là chỉ tiêu số vùng/số view cho gói khác.
- Điều hướng canonical có ba nhóm, không phải một dãy mục ngang hàng: **Mạch học chính** gồm `Bắt đầu/Cách học`, `Bài học`, `Luyện tập`, `Kiểm tra`, `Ôn lại`; **Hỗ trợ khi cần** gồm `Ôn nền`, `Sửa lỗi`, `Nhật kí`, `Lời giải`; **Tiện ích** gồm `Tải PDF`, `Nguồn`, `Toàn văn`. Chỉ hiện mục mà trang có nội dung thật; không đổi vai trò để lấp đủ nhóm.
- Kit dùng rail trái desktop, nút biểu tượng/dialog mobile; tên truy cập, bàn phím, Escape/focus và resize đúng hợp đồng. Ba nhóm giữ riêng, đặc biệt `Kiểm tra` → `Ôn lại`. Điều hướng không mất khi cuộn hoặc gây tràn cấp trang. Bảng ngang/thanh thu gọn trước kit là lịch sử tương thích, không đích giao diện hiện hành.
- Chiều rộng viewport/vị trí cuộn không tự đổi do trạng thái điều hướng; kiểm rail, toolbar và nút/dialog trên view dài/ngắn. Không dùng vòng `scrollTo` tranh quyền cuộn hoặc áp selector spacer cũ vào shell mới.
- Theo QD_025/031/033, `Ôn nền` và `Nhật kí` đều có owner cấp gốc độc lập; Ôn nền không thuộc Bài học/Khởi động, Nhật kí không thuộc Ôn lại. Nhánh tương thích sâu chỉ phục vụ đọc nguồn lịch sử, không cho phép sản xuất mới giữ owner sai. `Back`, tải lại, liên kết sâu và `Toàn văn` giữ đúng phạm vi; không nhân bản/di chuyển DOM lớn để sửa nguồn sai.
- `Toàn văn` dùng cùng một cây DOM canonical, không sao chép nội dung sang cây thứ hai. Khi JavaScript không chạy, nội dung vẫn phải đọc được.

### Khối thu gọn và bề mặt

- Tiêu đề của mọi khối thu gọn có chiều cao tối thiểu 44 px và dùng cùng cơ chế dấu mở–đóng.
- `guidance` có tiêu đề `Cách thực hiện`, bề mặt trắng, chữ tiêu đề xám cùng màu với `Mục lục`; nội dung dùng đoạn văn, danh sách dấu chấm hoặc danh sách đánh số theo quan hệ logic.
- `solution` dùng bề mặt xám nhạt và tiêu đề mô tả đúng lời giải hoặc bài tương ứng.
- `hint` là vai trò riêng, không được đếm hoặc trình bày như `guidance`; tiêu đề ngắn gọn như `Cần một gợi ý?`.
- Nội dung thông thường không được đóng khối chỉ để tạo nền, viền hoặc cảm giác nhấn mạnh. Công thức hiển thị không dùng khối trang trí `equation` và không dùng `\boxed{...}`.
- `guidance` mặc định đóng. Theo FB036, **mọi disclosure G01/G02 mặc định đóng**; deep-link chỉ mở ancestor cần thiết. Không tự kế thừa ngoại lệ mở sẵn trước đó, không giấu điều kiện bắt buộc trong hộp đóng. Quy tắc này không ép nội dung mở cố định thành disclosure hoặc áp sang Nhà/D0.
- Mọi đáp án, lời giải hoặc hướng dẫn chấm tách khỏi đề phải nằm trọn trong một khối `solution`; không để các nhóm lời giải nằm ngoài hộp do đóng sai ranh giới fenced div.

### Nhiệm vụ, ví dụ và liên kết

- `task-pause` dùng `.zo-learning-task.zo-learning-task--pause`; `task-item` dùng `.zo-learning-task.zo-learning-task--item`.
- Nhãn nhiệm vụ nằm trong chính khối nhiệm vụ. Khi gợi ý/lời giải tách vị trí cần liên kết, link nằm cuối khối nguồn và link quay lại nằm cuối khối đích; cặp đề–lời giải tại chỗ không cần hai link nhảy.
- Hai nhãn ngắn canonical cho cặp đề–lời giải là `Xem lời giải` và `Xem đề bài`. Nhãn khác chỉ dùng khi đích không phải lời giải hoặc đề bài.
- `example` dùng `.zo-learning-example` hoặc `.zo-learning-example-heading` và không tạo lời giải lặp lại ở cuối trang.
- Anchor phải chi tiết, duy nhất; nếu cặp đề–lời giải tách vị trí thì liên kết hai chiều phải trỏ đúng cặp.

### Bảng, bảng biến thiên và hình

Cổng nguồn/bản xuất theo 07/6.1.2: dùng zo_course_math_assets.py và binding course-math-assets.json của kit. QMD gọi BBT bằng div .zo-native-bbt có data-bbt trỏ JSON duy nhất; không giữ bảng Markdown BBT song song hoặc khai ordinary kind=variation. Surface/cỡ hình trong bài khác vai trò ảnh bìa; giữ đúng manifest duyệt bìa.

- Ngôn ngữ bảng dùng chung toàn khóa theo 07/6.1.1, QD_030: tám loại giá trị, dữ liệu/tần số, đối chiếu, hai chiều, dấu, biến thiên, tiêu chí và quy trình/thuật ngữ. Không dùng một kiểu căn cho mọi bảng. Header/row header khai đúng vai trò; Nhật kí lời văn trái, bảng giá trị toán giữa và dữ liệu số phải. Nét lưới/cỡ chữ/nhấn theo hợp đồng ấy, không tạo palette riêng.
- `scripts/zo_course_tables.py` nối binding `profiles/course-tables.json` và `course-tables.css` từ kit vào cả Nhà/D0/G01/G02 sau phép chiếu nội dung; bảng thường có liên kết cũng nhận đủ lớp/ngữ nghĩa/width. Từ chối bảng chưa phân loại hoặc binding thiếu/trùng; BBT so từng ô với JSON trước áp dụng. D0 opt-in bảng dấu native giữ nguyên JSON và caption, không tái sinh nguồn D0 từ generator cũ. Các selector căn trái legacy chỉ áp bảng chưa opt-in, không đè loại mới. Không thay đường PDF mặc định.
- Chọn `fit` khi bảng vẫn đọc thoải mái trên mobile; chọn `scroll` và `min_width` khi co bảng làm cột quá hẹp. Bảng `scroll` cuộn ngang trong vùng riêng, có chỉ dẫn khi thật sự tràn và không làm trang tràn ngang.
- Bảng có liên kết vẫn phải nhận đủ lớp bảng canonical, tên trợ năng, header cột và row header như bảng không có liên kết; không chấp nhận ngoại lệ làm mất khung bảng hoặc ngữ nghĩa chỉ vì cell chứa anchor.
- Bảng điều hướng hoặc sửa lỗi phải ghi bằng tên chính thức và mô tả người học hiểu được. Mã quản lí được giữ ở anchor hoặc thuộc tính dữ liệu, không hiện trong ô bảng.
- Bảng nút thắt nhận thức trong Sửa lỗi theo 07/6.1.7/BOTTLENECKS-20261019, dùng bốn cột và tỉ lệ 17/22/36/25 từ profiles/course-tables.json. Quy tắc này thay mẫu định tuyến 40/20/20/20 cũ; không ép bảng khác cùng mẫu. Giữ nhóm nhiệm vụ theo nơi phát hiện, ID và trường Nhật kí; ràng buộc remediation trong he_nhan.json được cổng nguồn kiểm.
- BBT web opt-in native/MathML lấy cùng JSON canonical; giữ mốc/dấu/giới hạn/cột loại/lỗi cố ý. Đồ thị SVG profile 0.4 dùng cỡ tự nhiên, nhãn phù hợp chữ, không kéo đầy giấy. Caption nằm dưới hình trong cùng vùng; viewport hình cuộn cục bộ khi cần. Vector lịch sử/PDF giữ tương thích ngoài phạm vi đã chuyển.
- Hình phải tải thật; BBT native phải đủ dữ liệu và MathML trong HTML mới. Alt/caption mô tả nội dung, không thêm mã kỹ thuật.
- Không gán công thức hàm số vào nhãn đồ thị nếu đề bài không cung cấp công thức ấy.

### Bìa, điều khiển, tải và footer

Chi tiết kích thước/token/selector lấy từ [hợp đồng kit](../../../../../../_design/web_2027_mau_dung_chung/hop_dong_vung_doc.md), không sao chép thành bộ giá trị cạnh tranh. Ảnh toán bìa không nền, đặt trong khung biên soạn vuông/dọc/ngang × hai cỡ, sáu nền sáng/tối Đỏ/Vàng/Xám; hình phải của đúng gói. Bộ chọn nền người học là sáu radio tròn trực tiếp một hàng, không chữ Nền/tên màu nhìn thấy nhưng có tên trợ năng/tooltip; Sắc xám giữ bằng biểu tượng và `aria-pressed`. Câu nhận diện dùng nguyên văn: “Học trong kỉ nguyên trí tuệ nhân tạo, học để tìm lại chính mình.”

Thẻ PDF gồm tiêu đề/mô tả, số trang và nút tải; mobile thích ứng. Số trang lấy tệp thật, giữ cảnh báo chưa đồng bộ khi còn stale. Nút drawer chỉ biểu tượng nhưng có tên truy cập/focus. Footer website ngoài main, thông tin từ cấu hình, không thay section Ủng hộ. Trang Nguồn dùng typography vùng tham khảo, không wrapper footer. Các điều khiển/khung đã chốt không được mở lại thiết kế trong nhiệm vụ biên tập nội dung.

### Nhật kí học tập

- Nhật kí G01/G02 include cùng `hoc_lieu/_dung_chung/nhat_ki_hoc_tap.qmd`; tên 14 trường đúng Mục 2.8 của `01_kien_truc_hoc_tap.md`, không viết mẫu riêng hoặc đổi “Bài khắc phục mới” theo tên UI. Header hàng/cột căn trái.
- Giá trị ví dụ dành cho người học dùng tên mục, tên bài và tên điểm kiểm soát chính thức. Mã máy đọc được tiếp tục nằm trong dữ liệu kiến trúc và không thay thế cách gọi trên giao diện.

### Ánh xạ canonical sang PDF

- Theo chỉ thị chủ trì ngày 21/10/2026, mọi PDF (toàn văn, học sinh và từng chức năng) đều có phần **Bảo trợ cuối tài liệu**. Dùng component nguồn chung; cấm lược bỏ theo biến thể. Bộ dựng và cổng PDF phải kiểm trang cuối trước thay đầu ra. Hướng dẫn nguồn: `_design/ngon_ngu_thiet_ke_zo_math_0_4/04_ap_dung/06_pdf.md`.

- PDF giữ nguyên vai trò nội dung của QMD/HTML nhưng dùng quy tắc dàn trang phù hợp khổ A4; không sao chép máy móc kích thước hoặc hành vi thu gọn của trình duyệt.
- `guidance` dùng khung nền trắng, viền xám nhạt và tiêu đề xám; `solution` dùng nền xám nhạt; `theory` tiếp tục dùng khung đỏ. Nội dung thường không được tự động đóng khung khi chuyển sang PDF.
- Bảng thường có khung ngoài và đường kẻ ngang–dọc đầy đủ trong PDF. Tỉ lệ cột lấy từ hợp đồng bảng của gói; bảng dài được phép ngắt trang nhưng phải lặp hàng tiêu đề.
- Bảng biến thiên và đồ thị dùng PDF vector, căn giữa; caption nằm dưới tài sản, dùng cỡ chữ phụ và màu xám.
- Dòng `.zo-source-note` được đặt sau nội dung được dẫn, dùng cỡ chữ phụ và màu xám; văn bản và dấu câu phải giữ nguyên từ nguồn QMD.
- Liên kết nội bộ còn đích trong phép chiếu được giữ nội bộ. Liên kết vượt phạm vi biến thể được đổi sang URL canonical có chế độ xem tương ứng; nhãn liên kết không được tự ý đổi nghĩa.
- Tránh tách tiêu đề khỏi phần mở đầu của khối, bảng hoặc hình; không buộc toàn bộ khối dài nằm trên một trang nếu điều đó tạo khoảng trắng lớn hoặc tràn trang.

Baseline PDF canonical đầu tiên của hệ thành phần dùng chung là
`on-thi-learning-pdf/1.0`, được chốt từ tám biến thể R1-G01 sau nghiệm thu thị
giác ngày 2026-09-30. Ma trận hồi quy của gói là: `full` 41 trang, `student` 31
trang, `bai_hoc` 22 trang, `luyen_tap` 7 trang, `kiem_tra` 5 trang, `sua_loi` 5
trang, `on_lai` 3 trang và `loi_giai` 12 trang. Đây là baseline hồi quy riêng
của R1-G01, không phải chỉ tiêu số trang cho gói khác. Metadata thẻ tải phải lấy
đúng số trang của đầu ra hiện hành; checker của gói phải khóa toàn bộ ma trận,
provenance và quan hệ phép chiếu thay vì chỉ kiểm tra PDF tồn tại.

Baseline này xác nhận cách ánh xạ component, bảng, bảng biến thiên, hình, liên
kết và dàn trang A4. R1-G02 đã được nghiệm thu thị giác và chốt ở Pha 6C ngày
2026-09-30 với ma trận hồi quy riêng: `full` 26 trang, `student` 17 trang,
`bai_hoc` 10 trang, `luyen_tap` 6 trang, `kiem_tra` 4 trang, `sua_loi` 5 trang,
`on_lai` 3 trang và `loi_giai` 10 trang. Mọi thay đổi đầu vào đã được khai trong
provenance phải làm biến thể chịu ảnh hưởng thành `STALE` cho tới khi được dựng
lại bằng pipeline canonical và kiểm nghiệm hồi quy.

### Công thức và nguồn đối chiếu

- Dấu ngoặc chứa phân số/biểu thức cao phải dùng cặp `\left…\right`, theo `quy_trinh_xay_dung/quy_chuan_dau_ngoac_latex.md` được chủ trì xác nhận ngày 11/10/2026 cho toàn ZO Math. Giữ nguyên loại đầu mút; áp dụng cả khoảng, đối số hàm và ngoặc trong biểu thức. Guard chung `scripts/zo_latex_delimiters.py` được cổng `zo_math_notation.py` gọi trước dựng G01/G02; không dùng ngoặc ngắn hoặc CSS kéo dấu để thay cú pháp đúng.

- Theo xác nhận của chủ trì ngày 11/10/2026 (QD_029), biểu thức toán trong văn bản phải ở math mode LaTeX. Phân số dùng `\frac{...}{...}`, không viết `1/x` hoặc `(x+1)/2`; đạo hàm dùng `^\prime`, không dùng dấu `'` hoặc ký tự `′` trong nguồn công thức; căn dùng `\sqrt{...}` (chỉ số căn nếu có cũng phải đúng cú pháp). Đơn vị và URL trong văn xuôi không phải phân số toán.
- MathML trong câu giữ bố trí toán native và baseline; không ép mọi công thức thành `inline-block`, căn giữa theo chiều dọc hoặc cắt tràn của căn/phân số. Công thức dài dùng dòng riêng/vùng cuộn cục bộ khi cần, không làm tràn trang. Kiểm hình trên desktop/mobile sau đổi nguồn hoặc CSS.
- `scripts/zo_math_notation.py` kiểm G01/G02 và include đang dùng, số mục Bài học theo 07, cùng quy tắc inline MathML trong shell. Hai adapter HTML gọi guard trước dựng phép chiếu. Guard không thay thế đọc trực quan, kiểm toán độc lập, nghiệm thu hay phát hành; không tuyên bố đã triển khai tự động trên toàn repository.
- Công thức dài được đặt trên dòng riêng khi việc đặt trong câu làm giảm khả năng đọc; việc tách dòng không tạo thêm khối nền hoặc viền.
- Với công thức phân nhánh, mỗi nhánh viết theo mẫu `biểu thức & \text{khi } điều kiện`. Không đặt dấu phẩy giữa biểu thức và điều kiện. Dấu phẩy đặt sau điều kiện của các nhánh chưa cuối; dấu chấm đặt sau điều kiện của nhánh cuối khi công thức kết thúc câu.
- Dòng nguồn đối chiếu dùng `.zo-source-note`, đặt sau nội dung được dẫn, viết thành câu hoàn chỉnh, không dùng ngoặc vuông, không viết tắt tên sách hoặc từ `trang`.

### Hàng rào kiểm định

- Checker của từng gói khóa số lượng và quan hệ component theo nội dung riêng, đồng thời khóa các bất biến dùng chung nêu trên.
- Checker HTML/mobile phải phân biệt tràn ngang cấp trang với cuộn ngang cục bộ có chủ ý của thanh thẻ và bảng.
- Checker/QA phải khóa ownership/trục/inset, binding tươi, rail/dialog, chống tràn/giật và cô lập view sâu theo kit hiện hành. Browser QA cuộn mọi view desktop/mobile, sai số vị trí cuộn ngoài thao tác tối đa 1 px; kiểm Ôn lại/Nhật kí riêng qua click, Back và tải lại. Không dùng gate sentinel/spacer cũ làm toàn bộ nghiệm thu shell mới.
- Nghiệm thu thị giác tối thiểu dùng desktop, 430 px và 390 px; phải xem cả trạng thái mặc định và các khối thu gọn đã mở.
- Thay đổi nguồn CSS, Lua hoặc JavaScript dùng chung phải chạy checker của cả R1-G01 và R1-G02. Render và nghiệm thu lại chỉ được thực hiện khi nhiệm vụ cho phép.
- Checker gói phải chặn mã quản lí lọt vào văn bản người học, lời giải nằm ngoài `solution`, bảng liên kết thiếu xử lí canonical, tên trường Nhật kí sai, khối hướng dẫn vô cớ mở sẵn và tiêu đề bị lặp ngay bên dưới.
- Kiểm trình duyệt xác nhận ảnh tải với kích thước tự nhiên khác $0$ và BBT native đầy đủ dữ liệu/MathML; chỉ thấy `img` hoặc bảng không đủ. Kiểm đề–lời giải theo nhóm thật, nhãn nguồn/adapter không lặp, câu xác nhận Nền thuộc đúng thẻ và hai action khác chức năng có nhãn khác.

## Ánh xạ kỹ thuật và chuyển tiếp

Các tên dưới đây ghi baseline component tương thích trước shell kit. Chúng không chứng nhận ứng viên FB036 đã được chủ trì duyệt. Lớp `r1-*` còn xuất hiện để giữ tương thích; vai trò canonical và ánh xạ vùng hiện hành lấy từ QMD/profile/kit, không từ số lượng trong bảng lịch sử.

| Vai trò canonical | Ánh xạ kỹ thuật đã chốt | Trạng thái trên hai gói |
|---|---|---|
| `guidance` | `.zo-learning-guidance`; lớp `r1-details.r1-guidance` được giữ tương thích | Đã áp dụng và kiểm định trên cả hai gói. |
| `task-pause` | `.zo-learning-task.zo-learning-task--pause` | Đã áp dụng và kiểm định trên cả hai gói. |
| `task-item` | `.zo-learning-task.zo-learning-task--item` | Đã áp dụng và kiểm định trên cả hai gói. |
| `example` | `.zo-learning-example`, `.zo-learning-example-heading` | Đã áp dụng và kiểm định trên cả hai gói. |
| `theory` | `.zo-block.zo-block-red` với `.zo-block-title` | Đã áp dụng; số lượng do nội dung từng gói quyết định. |
| `context-note` | `.zo-learning-context-note` hoặc khối xám sau khi phân loại | R1-G01 có một khối đọc thêm; R1-G02 không đóng khối cho giải thích thông thường. |
| `extension` | `.zo-block.zo-block-yellow` khi đúng vai trò mở rộng | Không bắt buộc xuất hiện; không chuyển máy móc từ class cũ. |
| `hint` | `.zo-learning-hint` | Đã áp dụng cho các gợi ý của R1-G02; tách khỏi `guidance`. |
| `solution` | `.zo-learning-solution`; lớp `r1-details.r1-solution` được giữ tương thích | Đã áp dụng và kiểm định trên cả hai gói. |
| `answer-link` | `.answer-link` với anchor hai chiều | Đã áp dụng và kiểm định trên cả hai gói. |
| `source-note` | `.zo-source-note` | Đã áp dụng và kiểm định trên cả hai gói. |
| `figure-table` | `.r1-table-*`, `.r1-bbt`, `.r1-figure`, `.r1-figcaption` | Đã kiểm định trên hai gói; tiếp tục dùng component chuyên biệt và tài sản vector. |

### Ranh giới chuyển đổi hai gói hiện có

- Baseline component 1.0 đã có lượt kiểm nội bộ; thiết kế G01/HTML FB033 sau đó đã được duyệt. FB036 mở lại lỗi cụ thể hai gói và còn chờ xem; các góp ý nội dung mới ở hồ sơ G01. Mọi thay đổi tiếp phải giữ toán, thứ tự nhận thức, ID, bảng/hình nếu không được giao biên tập đúng phạm vi.
- R1-G01 và R1-G02 có ma trận PDF canonical lịch sử riêng; đó là bất biến hồi quy của đúng bản lịch sử, không phải số trang bắt buộc cho nguồn mới hoặc chỉ tiêu dùng chung. PDF của cả hai gói chưa đồng bộ với nguồn đã đổi; khi được giao PDF phải kiểm lại toàn bộ biến thể/nội dung/số trang thật và cập nhật kỳ vọng có căn cứ, không sửa provenance bằng tay để gọi `CURRENT`.
- Không sao chép CSS hoặc JavaScript riêng từ gói này sang gói khác để tạo thêm một baseline ngầm. Thành phần dùng chung phải có một nguồn kỹ thuật chính thức trước khi được dùng cho các gói tiếp theo.
- Một sửa lỗi cục bộ trong R1-G01 không tự động thay đổi baseline. Baseline chỉ đổi khi hợp đồng này được cập nhật, thành phần dùng chung được triển khai và các gói chịu ảnh hưởng được nghiệm thu lại.

## Hàng rào bắt buộc

Các trang và tài sản đã duyệt của chuyên mục chỉ được chọn qua allowlist trong `publish_public.yml`. `_quy_trinh` luôn bị chặn kể cả khi mở các trang học. Không đưa liên kết, dữ liệu chỉ mục hay resources chứa đường dẫn nội bộ vào cây public.

Preview dùng profile `on-thi-preview`, chỉ ở `127.0.0.1`; không phải pipeline xuất bản. `zo_publish.py` phải từ chối profile này và kiểm tra đường dẫn bị cấm sau chuẩn hóa trong manifest, HTML, `search.json` và sitemap.

## Hiệu chỉnh nhãn ngữ cảnh, 17/10/2026

Nhãn cấp chứa theo 07/6.2 thay các bảng mỹ thuật cũ khi dựng G04/gói mới: Bài học → MẠCH HỌC CHÍNH; Khởi động → MẠCH HỌC CHÍNH · BÀI HỌC. Từ vựng/chức năng/số QD_025 không đổi. Binding khai context_labels: parent-context-v1; label_contract.display_contract.context_labels là nguồn giá trị, zo_course_labels.py ghép/kiểm từ owner/context tươi. Adapter không ghi đè nhãn bằng chuỗi riêng. Dùng .role và đúng dấu “ · ”; kiểm kê trước–sau, kiểm nhãn nhìn thấy desktop/mobile. Các giá trị cũ chỉ tương thích gói chưa di trú, không là mẫu cho gói mới.
