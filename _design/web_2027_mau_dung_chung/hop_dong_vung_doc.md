# Hợp đồng vùng đọc của mẫu web 2027

**Home 14/10/2026:** riêng sáu vùng đọc lớn được chủ trì giao bố cục mới
trắng/xám trắng rất nhẹ xen kẽ; không áp giấy trắng tuyệt đối của R1 lên
Home hoặc đổi khối toán. Giới thiệu thuộc hero; Cách học đứng ngay sau
danh mục. Hàng Cách học là các khung toàn chiều ngang, không bốn cột;
kiến thức/FAQ giữ từng hàng độc lập. Học trực tiếp giữ minh họa và điểm
nhấn đã duyệt. QMD sở hữu thứ tự/câu chữ/ảnh, CSS Home sở hữu hình thức;
nguồn ảnh quản lý ở khóa, bản thử audit chỉ để đối chiếu. Thẻ CTA-only và
các chức năng khác giữ nguyên, không đổi hợp đồng D0/R1 hoặc PDF.

**Home DH_038:** nội dung biên tập native ở `2027/index.qmd`; ba component
dữ liệu sinh chỉ dành cho đồng hồ/danh mục/mạch kiến thức. Binding
`zo_home_qmd.py` giữ cây DOM/ID/heading/alt/summary đã có; không đặt câu chữ
trong template hay toàn trang raw HTML. DH_028 trước đó và profile `editorial-home-2027` thay
nhóm đọc/ảnh bìa Home DH_017 trong đúng phạm vi trang Nhà; giấy trắng/font/
token/logo vẫn theo 0.4, không ép map vùng R1 lên trang Nhà. Nội dung từ
Quarto tươi được kiểm projection trước đổi shell; thẻ danh mục lấy metadata
thật và giữ ID/URL. HTML nhập chỉ đối chiếu, ảnh hành trình là minh họa ý
niệm chứ không là đồ thị toán. Không thay hợp đồng vùng/tiêu đề D0/G01/G02.

**Điều hướng QD_032:** toolbar ba icon nằm ngoài main/vùng đọc và độc lập với rail/mục lục trong gói. Module chung bảo toàn nguyên DOM main/rail/footer và logo trong mỗi phép nối; CSS riêng không chọn heading/content. Bốn đích dùng catalog khóa và binding chung. Giữ ID/view/context; Đầu trang dùng scroll thay đổi vị trí, không đổi view khi JS có mặt. Gateway không nhận component mới trong lượt này.

Phạm vi: bộ khung dùng lại, G01 opt-in đã tích hợp nguồn HTML. Thiết kế 9/10/HTML FB033 đã duyệt tại mốc lịch sử; đường học mới phải kiểm theo QD_033 cùng phần kế thừa chưa bị thay của QD_021; không lấy trạng thái chờ xem FB036 làm hiện trạng. Căn cứ thị giác lịch sử: FB022–024, FB027–036; kiến trúc hiện hành do 01/07 sở hữu. Chưa là quy chuẩn toàn ZO Math hoặc phiên bản 0.5 khóa.

[Chuẩn trang của khóa](../../content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/07_quy_chuan_cau_truc_trang_nguoi_hoc.md) sở hữu quy tắc vai trò/vùng đọc; hợp đồng này cụ thể hóa kỹ thuật theo phạm vi kit. Trạng thái/nhiệm vụ chỉ ở bảng 03, toán/ID theo QMD/manifest. Nếu nguồn đổi, kiểm binding tươi, không lấy bản đồ cũ hoặc HTML audit làm nội dung gốc.

## Cổng đường học và bằng chứng

DH_019: G02 đã nối opt-in vào hook canonical chung. Nhịp Cách học/Khởi động và component tổng quan ba chặng đồng bộ theo vai trò với G01, không ép số nhiệm vụ/toán bằng G01. `zo_web_2027_g02_sync_check.py` đối sánh giấy/chữ/bảng trực tiếp; `zo_r1_g02_labels_check.py` có fixture tách nhịp Cách học và bỏ bảng ba chặng. Bản G01 và receipt không thay; HTML G02 mới chờ chủ trì duyệt. Các mô tả G02 chỉ audit trong lịch sử không là đường dựng hiện hành.

QD_033: kit không sở hữu kiến trúc. Đối chiếu 01/2.2–2.4 trước chọn vùng hoặc dựng sơ đồ: Bài học, Luyện tập, Kiểm tra và Ôn lại có chức năng khác nhau, không bắt hoàn thành tuần tự; chọn điểm vào theo nhu cầu, mức chuẩn bị và bằng chứng hiện có. Ôn nền, Lời giải, Sửa lỗi và Nhật kí là hỗ trợ độc lập theo ngữ cảnh. Trong lượt Kiểm tra phải tự lực; muốn trợ giúp thì kết thúc lượt, giữ riêng bài làm ban đầu. Lưu bằng chứng tại Điểm dừng không đồng nghĩa ghi Nhật kí mỗi lần; chỉ cần link quay lại đề khi hai vị trí thực sự tách biệt. Không đưa thao tác đọc kết quả/sửa/ghi/hẹn thành chặng toàn gói, không chép lí do biên tập vào nhãn công bố. Theo QD_022, kết quả phải phù hợp quy tắc hiện hành của phần được kiểm; hash tài liệu không liên quan không hủy toàn bộ QA hoặc chặn hiệu chỉnh. Tài liệu PASS không là sản phẩm PASS. Không đổi inset/token/component trong lượt khép mô hình.

## Các bất biến khi dùng lại

QD_025 kế thừa QD_023 và thêm Gợi mở: nguồn chính thức là `label_contract` của danh mục kiến trúc toàn chương trình và 01/07. Dòng nhãn chỉ bổ sung ngữ cảnh không rõ, không lặp tiêu đề; số liên tục theo nhóm chức năng. Mục lục và vùng đọc cùng cây owner, nhưng vùng không phải đơn vị đếm. Bảng di trú không là nguồn build. Ôn nền là khu hỗ trợ độc lập; G01 đã có owner cấp gốc và binding hiển thị canonical. G02 đã áp dụng Ôn nền cấp gốc và binding riêng tại DH_016; bằng chứng mới kiểm theo nguồn/đích/câu chữ và runtime đại diện, không dùng layout cũ chứng nhận quy tắc mới.

1. **Vùng đọc sở hữu trọn một bước đọc có nghĩa.** Nhãn, tiêu đề, lời dẫn, công thức, hình, chú thích và hành động liên quan nằm trong vùng đó. Không thả heading/link quay lại trên nền trống. Hero, navigation và section ủng hộ là các vùng giao diện riêng, không phải đoạn thân bài rơi ngoài giấy.
2. **Không chia theo số heading, chiều cao màn hình hoặc độ dài tùy ý.** Ghép các mắt xích cùng đạt một kết quả đọc; ngắt khi người đọc chuyển mục tiêu hoặc thao tác. Không tách chú thích/ràng buộc khỏi hình hay câu hỏi khỏi dữ kiện cần dùng.
3. **Một cấp giấy, một khoảng đệm ngang.** `.reading-region` sở hữu inset; nhãn, heading, summary và nội dung lồng không cộng thêm inset. Danh sách có thụt dòng theo quy ước đọc; bảng/hình có viewport cuộn cục bộ khi cần. Không chữa lệch bằng việc xóa toàn bộ padding hoặc giấu tràn bằng `overflow:hidden`.
4. **Phân vai trò bằng nhãn và cấp chữ, không bằng hộp trong hộp.** Ví dụ, nhiệm vụ, tự kiểm tra, hướng dẫn và lời giải được nhận diện; khối chức năng bên trong không tự sinh một tờ giấy mới. Theo phản hồi FB036, mọi hộp có cơ chế đóng/mở của G01/G02 mặc định đóng trong HTML. Deep-link chỉ mở ancestor cần thiết để đọc đích; nội dung mạch chính không có cơ chế thu gọn vẫn hiện bình thường. Quyết định này thay mặc định đóng/mở trước đó trong phạm vi hai gói, không áp sang trang Nhà/D0.
5. **Cùng trục, cùng độ rộng giấy, khoảng nghỉ ổn định.** Desktop giữ cột đọc tối đa 816px với lề thở bên phải, dù hero chiếm hết workspace. Mobile co giấy, không giãn cỡ chữ hình để lấp bề ngang. Các giá trị này là mốc thực hiện đã duyệt của kit, không tự phong thành quy luật chung cho mọi sản phẩm.
6. **Hình toán theo chữ ở zoom 100%.** Dùng `--figure-em` được xác định từ kích thước nhãn SVG và cỡ chữ xung quanh; không `width:100%` lên `.math-illustration`. Thiếu chỗ thì cuộn cục bộ, không tự phóng to/thu nhỏ làm lệch cỡ nhãn. Minh họa trang bìa có vai trò khác và được giới hạn riêng.
7. **Nền canvas không phải giấy.** Sáu nền và sắc xám không đổi giấy nội dung thành cùng màu nền. Theo FB-027 ngày 08/10/2026, sáu chấm màu hiển thị trực tiếp một hàng; radio chính là chấm màu, viền báo lựa chọn hiện hành. Không hiện chữ Nền/tên màu, không giấu trong dropdown. Tên vẫn có cho trình đọc màn hình/tooltip; Sắc xám là nút biểu tượng hai nửa sáng–tối có trạng thái bật/tắt và bàn phím. Chỉ thay cách hiện điều khiển, không thay palette/default hoặc dữ liệu tùy chọn. Quyết định này thay yêu cầu hiện tên trong kit trước, không sửa lịch sử 0.4. Đỏ ZO/Vàng ZO là điểm nhận diện và hành động, không biến mọi vùng đọc thành mảng màu cạnh tranh.
8. **Điều hướng ổn định, không làm đổi bố cục lúc cuộn.** Desktop rail trái, mobile nút mở rõ ràng và dialog; bàn phím/Escape/focus/resize có kiểm. R1 giữ ba nhóm vai trò và Ôn lại ngay sau Kiểm tra; Ôn lại và Nhật kí là hai view riêng. Trang Nhà dùng mục lục theo vai trò của trang Nhà, không gắn các tab R1 vào nó.
9. **Bảo toàn nguồn.** Không sửa câu chữ toán, đáp án, ID, thứ tự đọc, heading cấp nguồn, disclosure hoặc luồng học để phù hợp thiết kế. Nhãn mới chỉ là metadata trình bày và phải được phân biệt trong phép đối chiếu. Link preview được ánh xạ nhưng lưu URL canonical, không đổi URL xuất bản.

### Bảng và quan hệ sở hữu sau FB036

QD_031 thay cơ chế Nhật kí nằm sâu trong Ôn lại bằng owner cấp gốc và thứ tự Toàn văn ở 07/3. Sửa lỗi theo nhóm nơi gọi, nhiệm vụ là con nhóm; Lời giải phản chiếu đúng cây nguồn. Hành động đề–đáp án chỉ có khi hai nơi tách biệt; cùng một vùng/tài nguyên dùng disclosure đóng, không link nhảy trùng. Routing bốn cột giữ kiểu process/routing QD_030, đích ghi số và tên, hướng dẫn dài tách khỏi ô dấu hiệu nhưng giữ nội dung. Cổng `zo_web_2027_backlog_check.py` nối cả hai adapter; receipt FB cũ không được sửa để chứng nhận thay đổi này.

Ngôn ngữ bảng theo 07/6.1.1/QD_030, dùng chung toàn khóa: `profiles/course-tables.json` phân loại chức năng, `course-tables.css` hiện thực tám kiểu 0.4; `zo_course_tables.py` từ chối bảng chưa phân loại và nối vào cả bốn adapter. Header lời văn/Nhật kí trái; giá trị/ma trận số/dấu/BBT giữa, dữ liệu số phải theo vai trò. Bảng chọn khắc phục giữ bốn cột 40/20/20/20 (`profiles/r1-consistency.json`), không ép bảng khác cùng mẫu. Tên khu vực theo QD_023; tên bảng riêng theo nguồn, ID và trường Nhật kí “Bài khắc phục mới” giữ nguyên; một include canonical đủ 14 trường.

Xác nhận Nền/đáp án/điểm quay về thuộc tài nguyên Nền trong khu Ôn nền độc lập; không thành Tự kiểm tra mạch chính. Nhãn source/adapter không lặp; trong trang Lời giải, nhóm dùng tên khu vực/nhóm nguồn nhiệm vụ, không bắt lặp tiền tố Lời giải. Phân biệt nhóm và đơn vị trả lời; phần phối hợp chỉ có khi thực sự tồn tại. Action xem công thức khác xem lời giải phải khác tên. Nguồn dùng typography tham khảo, không wrapper footer. Quy tắc do bộ điều hành sở hữu; selector/guard hiện có chưa tự chứng nhận nguồn đã đạt QD_023.

## Bản đồ riêng từng trang

Mốc G01 đã duyệt FB033: 154 vùng, 12 view; con số thuộc mốc lịch sử, không buộc bản sửa FB036 giữ nguyên số vùng. Bản đồ canonical hiện hành tại `content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/giao_dien/web_2027_layout.json`. `g01-reading-content.json` ở audit discovery chỉ là lịch sử. Mục 3.1–3.2 cùng kết quả từ công thức đến chiều biến thiên; 3.3 dựng bảng và 3.4 đọc hình là các bước tiếp. Đây là ví dụ giải thích nhịp, không phải mẫu đánh số cố định.

Trang Nhà: profile ghi lí do từng nhóm. Định hướng ghép Giới thiệu/Dành cho ai/Mục đích; Cách học, Lộ trình kèm ghi chú, Tám mạch kèm giới hạn, từng gói học liệu, Chọn điểm bắt đầu và Trạng thái là các nhịp khác nhau. Tổng cộng chín vùng nội dung và section ủng hộ riêng. Tiêu đề danh mục nằm trong vùng gói đầu, không thêm một thanh tiêu đề rỗng. Bìa thumbnail chỉ đi cùng nhận diện; mô tả gói dùng đủ bề rộng đọc.

Trang mới phải có bản đồ với: owner/ID nguồn, nội dung bao gồm, kết quả đọc, lí do ghép/ngắt, liên kết chuyển bước và ngoại lệ. Không duyệt bản đồ chỉ vì mỗi vùng có nhãn.

## Mẫu cấu trúc tối thiểu

```html
<div class="reader-content">
  <section class="reading-region" data-reading-beat="id-nguon">
    <span class="role" data-reading-label>Vai trò nội dung</span>
    <h2 id="id-giu-nguyen">Tiêu đề nguồn</h2>
    <!-- Dữ kiện → giải thích → hình/chú thích hoặc nhiệm vụ cùng nhịp. -->
    <!-- Hành động đối chiếu/chuyển đoạn cũng thuộc vùng có chủ sở hữu. -->
  </section>
</div>
```

Wrapper có thể là `div` để không làm thay đổi cấp heading nguồn; vùng mở cố định hoặc `details` phải theo vai trò thật. Ví dụ trên minh họa cấu trúc, không chứa nội dung toán để tái sử dụng.

## Điều kiện nâng thành 0.5

### Hợp đồng dùng lại đã chốt tại G01 — FB033

| Thành phần dùng chung | Phần phải xác định riêng ở từng gói |
|---|---|
| Một cấp giấy; nhãn/heading/nội dung cùng trục bên trong; chia theo kết quả đọc | Bản đồ nhịp đọc, số vùng, ID nguồn và lí do ghép/ngắt; không nhân bản 154 vùng |
| Rail desktop; drawer mobile có nút biểu tượng, tên truy cập và focus | Các view/nhóm theo kiến trúc thật; không tạo tab rỗng để đủ 12 |
| Sáu chấm nền và Sắc xám; câu nhận diện đầy đủ | Không thay palette hoặc mặc định ngoài quyền nhiệm vụ |
| SVG đồ thị nhãn tương đương chữ, chiều rộng tự nhiên; cuộn trong vùng hình | Nguồn toán, tọa độ, scale và sidecar từng hình; không tái dùng đồ thị khác bài |
| BBT native từ JSON, cỡ chữ 1em, caption cùng vùng | Mốc/dấu/giới hạn/cột loại/lỗi cố ý theo dữ kiện từng bài |
| Ảnh toán bìa không nền; khung là lớp trình bày riêng | Ba dạng vuông/dọc/ngang × hai cỡ, sáu nền sáng/tối Đỏ/Vàng/Xám do người biên soạn chọn; không thêm bộ chọn cho học sinh |
| Thẻ PDF: tiêu đề và mô tả / số trang / nút tải; mobile xếp lại | Danh sách PDF và số trang đọc từ tệp thật; tám thẻ chỉ là G01, không là quy định mọi gói |
| Footer ngoài main; Ủng hộ là section riêng | Link/thông tin canonical của trang; không bỏ footer khi thay shell |

GRAPH-G03-01 thay quy tắc cỡ tự nhiên cũ của G01/G02/G04: gọi preset công cụ `lesson-g03` và đặt `--figure-em` bằng viewBox_width / 16.5 qua `zo_graphics.set_lesson_graph_size`; CSS chung dùng đúng biến này. Khung từng ô 11 × 7 cm, ngoại lệ cao 8 cm ghi rõ lí do. Bản chụp G03 trước sửa là đối chứng; nguồn TEX/SVG G03 giữ nguyên nhưng lớp hiển thị được sửa để đủ 11 ảnh nhận cùng quy tắc (GRAPH-G03-02). Hình ghép giữ bố trí các ô. Phông/nét 0.4 giữ nguyên, tỉ lệ trên trang theo G03; không giãn đầy giấy. Nguồn: `figure-profile-candidate/`, bộ nối `scripts/zo_web_2027_figures.py` và config hình G01. Không sửa toán để đạt hình thức.

Nút drawer G01 chỉ hiện biểu tượng, 52×52px; tên truy cập “Mở mục lục học liệu”, Enter mở, Escape đóng/trả focus. Nút tải tối thiểu 44px. Giữ lời cảnh báo PDF chưa đồng bộ tới khi có nhiệm vụ PDF được nghiệm thu; số trang đúng không chứng minh nội dung PDF mới.

Mốc duyệt lịch sử FB033, checksum/phạm vi tại `giao_dien/web_2027_accepted.json` của G01. Receipt không thay QMD, không chứng nhận FB036, không làm nguồn nội dung hoặc tự nâng chuẩn lên 0.5.

Tách rõ quyết định đã duyệt, hiện thực có kiểm, trải nghiệm từng trang và điểm chưa kiểm. Chỉ đề cử phần đã chứng minh; giữ backlog 1 điểm tương lai không bịa thêm lỗi. 0.5 còn cần hồ sơ quy chuẩn/phạm vi/di trú và quyết định của chủ trì; việc dựng được hai HTML không tự hoàn tất bước này.

## Đối sánh hai gói QD_028

Quy tắc vùng đọc và bảng theo 07; phạm vi xác nhận theo 01/2.5.1; phép kiểm theo 02/1.3. Kit chỉ hiện thực: không giấy chỉ có tiêu đề, không nhãn ngữ cảnh lặp, bảng giữ liên kết canonical, mục lục hai gói có cùng tên truy cập. Trạng thái/lệnh hiện hành theo 03/README gói; không dùng lịch sử FB để chứng nhận lượt mới.

## MATH-ASSET01 — đường dựng phải khớp vai trò

Theo 07/6.1.2 và 02/2.5 của khóa: source/HTML guard dùng scripts/zo_course_math_assets.py, binding profiles/course-math-assets.json. Không nối BBT bằng bảng thường được gán kind=variation; bộ nối bảng phải từ chối. Hình trong bài gọi cùng production-figures.css và cỡ tự nhiên, bìa dùng manifest riêng. Ma trận đối chứng phải chỉ ra cả component và đầu ra nhìn được; có thử âm JSON rỗng, thiếu giới hạn/điểm loại, surface bìa trong bài, provenance mã sinh/style/phông và sizing. Tương thích G01–G03 không chứng nhận G04/gói mới; không đổi shell/PDF/receipt hoặc xuất bản.

## DRAWER-ICON01 — chủ sở hữu của nút mở mục lục

Quy tắc nút icon ở trên áp dụng cho mọi gói/trang dùng shell, kể cả chưa có PDF. Template page.html.tpl sở hữu SVG/tên truy cập; web-shell.css sở hữu kích thước/hình tròn; site-ui.js sở hữu mở/đóng/focus/resize. Không phụ thuộc downloads.css hoặc đoạn chèn icon trong adapter PDF. Các đoạn tương thích G01/G02 không là chuẩn để nhân bản. zo_web_2027_shell.py chặn template/HTML/runtime CSS lệch trước bàn giao; kiểm browser vẫn bắt buộc. Nội dung main, rail, các view và điều hướng toàn khóa giữ nguyên.
