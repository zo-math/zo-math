# Đối chiếu và thống nhất bốn học liệu R1 — 18/10/2026

Trạng thái: đã sửa nguồn và dựng bản HTML để duyệt; chưa nghiệm thu chủ trì, chưa dựng lại PDF, chưa commit/push hoặc xuất bản. Phạm vi do chủ trì giao là đối chiếu HTML, chọn cách trình bày phù hợp và áp dụng cho G01–G04.

## Bản xem và nguồn

[Bản xem chung bốn trang](http://127.0.0.1:8877/_audit/r1_consistency_20261018/index.html).

Nguồn chính thức vẫn là `E:/zo_math/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd` và ba đường dẫn tương ứng `r1_g02`, `r1_g03`, `r1_g04`. Không tạo bản QMD chính thức thứ hai. HTML để duyệt nằm tại `E:/zo_math/_audit/r1_consistency_20261018/html/content/thpt/on_thi_toan_thpt/hoc_lieu/`. Các tệp QMD trong `.quarto/r1_consistency_20261018` chỉ là bản sao làm đầu vào dựng cô lập.

Đối chứng đầu lượt là HTML mới nhất của G01/G02/G04 trong `_audit/graph_g03_standard_20261017/html/` và G03 trong `_audit/g03_graph_display_20261018/html/`. Đây là các bản sửa chờ duyệt, khác bản công khai trong `docs/`. Đã đọc toàn bộ cây nội dung HTML, trích toàn văn và kiểm các vùng Bài học, Luyện tập, Kiểm tra, Ôn lại, hỗ trợ, lời giải; không dùng PASS lịch sử để thay sản phẩm. Đường dẫn và hash đối chứng lưu trong `before.json` của vùng audit.

## Kiểm kê và phương án đã áp dụng

| Điểm chưa nhất quán | Cách chọn và áp dụng |
|---|---|
| G01/G02 còn tên chung “Nhiệm vụ” cho các chức năng khác nhau; G03/G04 có Gợi mở chỉ mang số | Tên theo chức năng và nội dung: Gợi mở, Tự kiểm tra, Nhiệm vụ Khởi động. Giữ dãy số hiện hành; đồng bộ đề, lời giải và bảng nhãn. |
| G02 chưa có Gợi mở trong năm mục kiến thức | Bổ sung năm câu hỏi ngắn từ nội dung đang có, sau Cách thực hiện và trước lời giải thích; có lời dẫn chung và cầu nối tại chỗ, không mở kho đáp án mới. |
| Nhãn câu hỏi G01/G02 cỡ nhỏ hơn tiêu đề cùng chức năng ở G03/G04 | Cùng lớp tiêu đề chức năng, cỡ 23 px trên màn hình rộng và 21 px trên điện thoại, độ đậm 600; không phụ thuộc nguồn dùng heading hay nhãn trong đoạn. |
| Cầu nối Gợi mở G02 bị bộ dựng tách riêng một khối khi xem thử | Câu hỏi và cầu nối cùng khối nội dung trong QMD; thêm kiểm chống tách cầu nối. |
| G01 còn chú thích lẫn chính văn; G02 có lời kể về cách người viết dùng sách; G03 dùng chú thích cuối và “Theo SGK…” | Phát biểu trực tiếp, chú thích nguồn thành đoạn riêng sau nội dung liên quan; thống nhất tên sách và tiền tố nguồn. Giữ thông tin thư mục và các anchor cũ. |
| Cây Lời giải G03/G04 chưa phản ánh đầy đủ nơi chứa đề; G04 có khối chỉ chứa tiêu đề Sửa lỗi | Nhóm Bài học chứa Khởi động/Tự kiểm tra; nhóm Sửa lỗi chứa các nhóm theo nơi phát hiện. Không để khối đọc trống. |
| Nhãn nhóm con trong Lời giải thiếu mục cha | Khai đường ngữ cảnh tại `heading_context` của từng bảng nhãn, gọi thành phần nhãn chung; không ghép chuỗi riêng theo trang. |
| G04 lặp nơi phát hiện lỗi trong từng tên nhiệm vụ | Đặt ngữ cảnh ở nhóm Sửa lỗi; nhiệm vụ giữ tên nội dung. Hướng dẫn vẫn chỉ rõ các điểm có thể gọi hỗ trợ. |
| Bảng Khởi động G04 thiếu cấu trúc hỗ trợ đủ chức năng | Bốn cột: câu còn vướng, kiến thức cần ôn, đi đến, sau đó. Đích cụ thể giữ theo gói. |
| G04 thiếu bảng tổng quan chặng Luyện tập | Thêm bảng hai chặng thật và nơi đối chiếu; giữ quyền chọn cách học theo điều hành. |
| Lịch Ôn lại khác hình thức và thiếu cột Điểm dừng | Cùng ba cột ngày hẹn, nhiệm vụ, Điểm dừng; giữ lịch và nhiệm vụ riêng. G04 chuyển lịch có sẵn thành bảng. |
| G03/G04 gộp nhiều tài nguyên Ôn nền độc lập vào một khối | Mỗi tài nguyên một khối đọc, đóng/mở độc lập; phần dẫn và bảng chọn vẫn theo nội dung từng trang. |
| Một số bảng thông thường G03/G04 nhận kiểu bảng điều hướng | Phân loại theo chức năng trong ánh xạ bảng chung; chỉnh độ rộng cột cho bảng tiêu chí/kết quả/lịch, giữ nguyên dữ kiện toán. |
| G04 dùng chín liên kết tuyệt đối về bản công khai cũ của các gói khác | Dùng liên kết nguồn tương đối, giữ query và anchor, để các trang trong cùng bản dựng liên kết đúng nhau. |
| Đổi tiêu đề có thể làm mất anchor tự sinh cũ của G02 | Ghi rõ các anchor cũ trong nguồn; giữ liên kết đến đúng nội dung. |

## Khác biệt có lý do được giữ

Không đồng nhất số mục kiến thức, nhiệm vụ, chặng hoặc nguồn Ôn nền. G02 giữ nhánh Chuyển giao có điều kiện; các gói khác không được thêm nhánh chỉ để giống nhau. Khởi động ngắn của G01/G02 có thể chung khối đọc, còn câu dài/có hình của G03/G04 tách khối. Gợi mở luôn thuộc từng mục Bài học; không trở thành tuyến độc lập. Hỗ trợ được gọi khi cần, không biến thành chuỗi bắt buộc. G04 chưa có PDF nên không thêm nút tải giả.

Năm Gợi mở G02 là bổ sung nội dung dẫn dắt cần chủ trì xem trong HTML mới. Không thêm định nghĩa, định lí hoặc bài kiểm tra. Đề và lời giải cũ được đối chiếu tự động sau khi bỏ nhãn/tiêu đề và chuẩn hóa biểu thức, khoảng trắng, dấu câu; phép so sánh này không thay một cuộc kiểm chứng toán học độc lập từng lời giải.

## Nguyên nhân và cơ chế ngăn tái diễn

G01 dùng bố cục đã gắn với nội dung, G02 dùng bộ chuyển cấu trúc cũ, G03/G04 dùng bộ dựng mới. Cùng vai trò nhưng DOM/tiêu đề/khối đọc khác nhau; các kiểm trước tập trung số lượng, nhãn và tính hợp lệ từng trang, chưa kiểm diện mạo tương ứng giữa trang. Ánh xạ bảng G04 còn chọn kiểu điều hướng quá rộng; liên kết tuyệt đối có thể đưa người đọc sang sản phẩm cũ.

Quy tắc tái sử dụng nằm tại 07/6.4 và quy trình 02, không tạo bộ chuẩn riêng trong hồ sơ này. Nguồn sở hữu: `zo_course_labels.py` cùng `he_nhan.json` cho nhãn; `zo_web_2027_consistency.py` và `r1-consistency.css` cho trình bày; `profiles/course-tables.json` cho bảng. Bộ dựng gọi cổng chung. `scripts/zo_r1_presentation_check.py` thử cả sản phẩm đúng và các biến thể sai: tên trống nghĩa, thiếu lớp kiểu chữ, Gợi mở ngoài Bài học, nguồn lẫn chính văn, lịch thiếu cột, khối chỉ có tiêu đề, tài nguyên nền bị gộp, liên kết tuyệt đối và cầu nối tách rời.

G01 được cập nhật bố cục từ hai bản dựng thô trước/sau và đối chiếu bảo toàn, không chỉ ghi lại hash. Không sửa receipt nghiệm thu cũ. Phần giới hạn phạm vi hồi tố của lượt 17/10 được ghi rõ là lịch sử; yêu cầu 18/10 mở sửa bốn QMD/HTML nhưng không mở PDF/phát hành.

## Bằng chứng và giới hạn bàn giao

Bảng kết quả cuối, fingerprint QMD/HTML, các tệp kiểm và trạng thái bảo toàn nằm trong [hồ sơ máy đọc](ho_so_nhat_quan_bon_goi_20261018.json). Audit đầy đủ ở `E:/zo_math/_audit/r1_consistency_20261018/`, gồm toàn văn/outline trước sửa, ảnh trình duyệt, log dựng và kết quả kiểm.

Kiểm trình duyệt bao gồm 1440/430/390 px, các tuyến đọc, nút mục lục, đề–lời giải–quay lại, hỗ trợ/Back/tải lại/nhiều tab và trạng thái không JavaScript. Đồ thị tiếp tục theo cỡ G03 đã chọn; nguồn SVG/TEX và dữ liệu BBT không đổi. Không tái dựng hình chỉ vì chỉnh chữ/bố cục.

Các lần thử trung gian giữ nguyên bằng chứng: một phép kiểm ban đầu yêu cầu anchor cả với liên kết đến đầu trang đã được sửa đúng; một lượt đọc HTML trùng lúc đang dựng gặp bản thô tạm thời, không được dùng làm kết quả cuối. Các kiểm cuối chỉ chạy sau khi dựng xong.

Cảnh báo dựng còn lại là các đích menu toàn site không được đưa vào mirror giới hạn; bản xem dùng cơ chế liên kết về thành phẩm hiện hành cho phần ngoài bốn trang. Không phải bản dựng toàn website. Chủ trì cần duyệt diện mạo/nội dung bổ sung trong bản HTML mới; PDF, xuất bản và commit là bước riêng khi được giao.

## Ghi chú lưu mốc sau bàn giao

Theo yêu cầu tiếp theo của chủ trì ngày 18/10/2026, nguồn đã được commit cục bộ tại `ec904d8dcedf0866f4df46207b78340c1daf2a99`. Hồ sơ bàn giao và điều hành được lưu ở mốc tài liệu kế tiếp. [Biên nhận commit](ho_so_commit_nhat_quan_bon_goi_20261018.json) giữ liên hệ với bằng chứng kiểm; các trạng thái chưa commit trong JSON bàn giao là ảnh chụp tại thời điểm trước yêu cầu lưu mốc. HTML tiếp tục chờ duyệt; chưa PDF, push hoặc xuất bản.
