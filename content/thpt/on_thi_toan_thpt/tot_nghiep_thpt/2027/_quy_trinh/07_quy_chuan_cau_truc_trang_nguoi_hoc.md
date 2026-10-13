# Quy chuẩn cấu trúc trang người học

Phiên bản: 0.8 · Ngày biên tập: 12/10/2026 · Đường học QD_033 (kế thừa phần không bị thay của QD_021); hệ nhãn QD_025 (kế thừa QD_023); Kiểm tra QD_024.

Tài liệu này quy định cấu trúc thông tin, điều hướng và tiêu chí nghiệm thu giao diện cho các gói học liệu R1 của ấn bản 2027. [Điểm vào](README.md).

Kế thừa đặc tả trang R1-G01 0.2 có điều chỉnh theo QD_003–018 và FB022–036. [Kiến trúc học tập](01_kien_truc_hoc_tap.md) sở hữu đường học; [quy chuẩn gói QMD](quy_chuan_goi_qmd.md) và [hợp đồng kit](../../../../../../_design/web_2027_mau_dung_chung/hop_dong_vung_doc.md) sở hữu ánh xạ kỹ thuật. Nhật kí sáu trường, khởi động mở sẵn, tiêu đề ngoài vùng và cơ chế điều hướng ngang cũ không là quy phạm hiện hành. Duyệt thiết kế 9/10 không chứng nhận bản sửa FB036 hoặc toàn bộ nội dung.

## Liên kết thẩm quyền và giới hạn hiện thực

[08](08_danh_muc_tham_quyen_dieu_hanh.md) phân vai chuẩn trang, chuẩn QMD, kit, profile và lịch sử. Cùng vai trò học tập phải có cùng cấp/chức năng trước khi chọn component; cùng typography chưa chứng minh đã sắp đúng vùng. Số vùng/view của từng bản chỉ là thống kê. Audit G01 ngày 10/10 ghi RD21 về vùng sở hữu bảng kết quả; trạng thái sửa lấy từ hồ sơ G01/03, không lấy audit cũ làm hiện trạng hoặc ngoại lệ thiết kế được duyệt.

Quy tắc “mặc định đóng” áp dụng **hộp có trạng thái đóng/mở**, không biến toàn bộ mạch chính thành disclosure. Điều kiện bắt buộc không được chỉ tồn tại trong phần hỗ trợ có thể bỏ qua. Một bảng lời giải/routing đúng không bù được lời dẫn khác đang dẫn sai; nghiệm thu phải đối chiếu toàn bộ nơi nói cùng chức năng.

### Bổ sung đối sánh QD_028

Vùng chỉ có tiêu đề nhóm không phải một nhịp đọc: ghép tiêu đề vào vùng nội dung đầu tiên thuộc chính nhóm đó, không đổi owner hoặc thứ tự. Omit nhãn ngữ cảnh khi nó chỉ lặp tiêu đề/chức năng đã rõ; giữ nhãn chính thức giúp xác định nhiệm vụ và nơi học. Không gán Tự kiểm tra của Bài học cho đầu trang Kiểm tra hoặc câu Xác nhận nền.

Bảng chọn nơi ôn sau Khởi động phải phân biệt dấu hiệu, kiến thức cần xem lại, đích và nơi quay về; không giấu đường vào Kiểm tra trong một dòng của bảng ôn. Đọc kết quả thuộc Kiểm tra sau khi lượt làm kết thúc, không phụ thuộc JavaScript kéo bảng từ Lời giải. Lịch Ôn lại phải có mốc ngày gốc và nhiệm vụ tương ứng; bảng khác nhau về nội dung vẫn giữ cùng component đúng vai trò. Phạm vi xác nhận theo 01/2.5.1.

## 1. Phạm vi và bốn lớp không được trộn

### Điều hướng toàn khóa học — QD_032

Trên Nhà, D0, R1-G01 và R1-G02, thay liên kết tên khóa học và liên kết chữ giữa thanh bằng ba điều khiển icon, từ trái sang phải: **Nhà → Danh sách toàn khóa học → Đầu trang**. Logo ZO Math giữ nguyên. Không dùng logo/tên thương hiệu thay cho thao tác Đầu trang; không có nút “Đi tới” hoặc hàng liên kết khóa học thường trực thứ hai.

Danh sách mặc định đóng, chứa Nhà khóa học, Khảo sát đầu vào, Đơn điệu và cực trị, Giá trị lớn nhất và nhỏ nhất; đánh dấu trang hiện tại. Liên kết thật cho phép chuyển trực tiếp giữa các gói, dùng URL/ID hiện hữu. Danh mục nguồn tại `_data/chuong_trinh.yml`; binding hiển thị/đích có một nguồn tại `scripts/zo_web_2027_navigation.py`. Danh mục đổi phải cập nhật binding và kiểm lại, không âm thầm bỏ sót gói mới.

Sáu màu nền và sắc xám giữ bên phải. Màn hình hẹp được xuống hàng cho nhóm màu, không biến danh sách đích thành hàng liên kết thường trực. Điều khiển có tên truy cập, focus thấy rõ, dùng được bằng bàn phím; Escape đóng danh sách và trả focus. Đầu trang không đổi view/URL ngữ cảnh khi JavaScript hoạt động; không JavaScript vẫn có liên kết đầu trang và danh sách native. Thanh khóa học độc lập với mục lục nội bộ từng trang.

Phạm vi QD_032 chỉ là điều hướng. Phương án phân cấp tiêu đề chưa được duyệt: giữ nguyên tiêu đề, nhãn, vùng đọc, toán, luồng học và footer. Duyệt mẫu không là nghiệm thu toàn bộ bốn HTML hoặc phát hành.

Trang người học phải giữ riêng bốn lớp:

1. **Kiến trúc học tập:** mục tiêu, hoạt động, bằng chứng, phản hồi và việc tiếp theo.
2. **Nội dung toán học:** đề, lời giải, hình, bảng và tiêu chí đúng.
3. **Dữ liệu vận hành:** ID, mã mục tiêu, mã lỗi, manifest, checkpoint và trạng thái.
4. **Giao diện xuất bản:** thứ tự đọc, nhãn, khối, bảng, điều hướng và hành vi responsive.

Mã quản lí phục vụ máy không được thay tên chính thức trong văn bản người học. Một thay đổi giao diện không tự cho phép đổi toán học, schema hoặc trạng thái nghiệm thu.

Quy chuẩn này được rút ra từ R1-G01 để dùng chung có kiểm chứng. Khi áp dụng cho R1-G02 hoặc gói mới, giữ hợp đồng chung nhưng đối chiếu nội dung và đường học riêng; không sao chép máy móc số chặng, số bài hoặc ngoại lệ của G01.

## 2. Mạch chính, lớp hỗ trợ và tiện ích

Điều hướng mạch chính giữ năm khu vực; Bắt đầu định hướng, còn bốn khu vực học có chức năng riêng theo QD_033/01/2.2.1. **Bài học → Luyện tập → Kiểm tra → Ôn lại là tiến trình chuẩn được khuyến nghị** và là thứ tự mục lục, nhưng không phải điều kiện bắt buộc phải hoàn thành tuần tự. Học sinh chọn điểm vào theo nhu cầu, mức chuẩn bị và bằng chứng học tập hiện có:

1. **Bắt đầu** — biết mục tiêu, điều kiện cần và hành động đầu tiên.
2. **Bài học** — học hoặc tra đúng phần kiến thức cần thiết.
3. **Luyện tập** — tự làm theo chặng và dừng ở checkpoint.
4. **Kiểm tra** — tạo bằng chứng độc lập chưa xem lời giải.
5. **Ôn lại** — khơi lại sau khoảng trễ bằng nhiệm vụ dành riêng.

**Ôn nền, Sửa lỗi, Nhật kí và Lời giải** là lớp hỗ trợ ngang. Chúng được gọi khi cần và phải đưa người học về đúng hoạt động đang dừng; không trình bày như các chặng tuyến tính bắt buộc. **Tải PDF, Nguồn và Toàn văn** là tiện ích, không phải bước học.

Sơ đồ toàn gói phân biệt bốn khu vực **Bài học, Luyện tập, Kiểm tra, Ôn lại** với các hỗ trợ độc lập. Nếu dùng mũi tên Bài học → Luyện tập → Kiểm tra → Ôn lại thì phải thể hiện rõ đó là thứ tự tổ chức/tra đọc, không phải quy trình bắt buộc hoặc khóa điểm vào. Ôn nguồn (xem lại Bài học hoặc Ôn nền), đối chiếu–sửa lỗi và Nhật kí được gọi theo ngữ cảnh, có đường trở về. Không nối Đọc kết quả, Sửa lỗi, Nhật kí hoặc Hẹn ôn thành các chặng chen giữa Kiểm tra và Ôn lại. Trong một lượt Kiểm tra phải tự lực; muốn nhận trợ giúp thì kết thúc lượt và giữ riêng bài làm ban đầu trước khi mở hỗ trợ.

Nhãn công bố dùng tên ngắn người học cần, như **Bài học**; không thêm “gồm Khởi động” để giải thích quyết định biên tập vốn thuộc nội bộ. Khởi động vẫn ở trong Bài học. Đối chiếu sơ đồ, lời dẫn và link với ma trận 01/2.2.2 trước khi dựng bản xin duyệt; không chọn hình thức rồi ép đường học vào nó. Không đổi thiết kế đã duyệt trong nhiệm vụ khép kiến trúc.

Trong kit hiện hành, desktop dùng rail trái; mobile dùng nút biểu tượng mở hộp điều hướng. Ba nhóm có nhãn/phân cấp rõ, không dàn thành một hàng thẻ phẳng. **Ôn lại đứng ngay sau Kiểm tra**. Mọi khu vực quan trọng truy cập được bằng liên kết sâu và bàn phím. Bài học/Luyện tập không xen kẽ; chỉ dẫn xem lại là hỗ trợ, không là bước luân phiên bắt buộc. Không ép cơ chế R1 lên Nhà/D0.

## 3. Thứ tự nguồn và hành vi JavaScript

Nguồn QMD và cây DOM phải có thứ tự sư phạm đúng trước khi JavaScript chạy. JavaScript chỉ điều khiển trạng thái hiển thị, điều hướng và ngữ cảnh; không được di chuyển các vùng nội dung lớn để sửa một cấu trúc nguồn sai.

Chế độ Toàn văn dùng cùng một cây DOM, không nhân bản nội dung thành nguồn thứ hai. Khi JavaScript không chạy, người học vẫn đọc được toàn bộ nội dung, liên kết tới đúng đích và nhận biết được trật tự học.

QD_031: thứ tự các khu vực nguồn/Toàn văn là **Bắt đầu → Bài học → Luyện tập → Kiểm tra → Ôn lại → Ôn nền → Sửa lỗi → Nhật kí → Lời giải → Nguồn → Tải PDF**. Đây là thứ tự tra đọc, không phải tuyến học bắt buộc qua tất cả hỗ trợ. Khởi động thuộc Bài học; Nhật kí là khu vực độc lập. Trong Sửa lỗi, nhóm theo thứ tự **Sau Luyện tập → Sau Kiểm tra → Sau Ôn lại**; nhánh Sau Chuyển giao của G02 đi sau Sau Luyện tập. Nhiệm vụ là con của đúng nhóm, không là heading ngang hàng với nhóm. Số chạy liên tục trong nhóm chức năng; đổi thứ tự phải cập nhật tiêu đề, bảng chọn, dẫn chiếu và đáp án cùng lượt, giữ ID. Trong Lời giải, thứ tự/cây nhóm phản chiếu nơi sở hữu nhiệm vụ; không dồn các phần độc lập vào một phần lớn.

Đề và đáp án trong cùng một tài nguyên/vùng đọc dùng hộp đối chiếu mặc định đóng, không thêm liên kết “Xem lời giải”/“Xem đề bài” chỉ nhảy giữa hai chỗ kề nhau. Hai nơi thực sự tách biệt vẫn giữ vòng dẫn đề–đáp án. Cùng trang HTML không đủ để coi là cùng vùng; guard kiểm chủ sở hữu cụ thể và binding nhiệm vụ.

Bảng Chọn bài sửa lỗi dùng bốn cột **Dấu hiệu cần sửa / Sau Luyện tập / Sau Kiểm tra / Sau Ôn lại**; ô đầu là dấu hiệu ngắn, ba ô đích dùng **Nhiệm vụ NN – tên nhiệm vụ**. Hướng dẫn dài thuộc phần giải thích riêng, không nhồi vào ô dấu hiệu hoặc bỏ đi. Đích Ôn nền vẫn nêu đúng tài nguyên. Viết hoa đầu ô/câu, không viết hoa máy móc mọi từ “nhiệm vụ”. Quy tắc kiểu bảng QD_030 vẫn áp dụng.

Lớp thị giác thử nghiệm phải là tăng cường lũy tiến: CSS mặc định đã tạo bề mặt đọc rõ trước khi JavaScript thêm điều khiển; điều khiển chọn nền hoặc chế độ màu có thể vắng khi không có JavaScript nhưng nội dung không được mất nền đọc, tương phản hoặc cấu trúc. Một bộ điều khiển dùng chung chỉ có một nguồn canonical và được giới hạn bằng body class/phạm vi rõ, không sao chép riêng vào từng trang.

Điều hướng tiếp tục truy cập được trong view dài: rail desktop ổn định; mobile có nút mở chỉ biểu tượng, tên truy cập, focus và Escape trả focus. Resize không nhân bản điều hướng hoặc để dialog kẹt. Hình thức bảng ngang/thanh thu gọn ở QD_007–009 là lịch sử; giữ các yêu cầu chức năng về ba nhóm, không giật và đúng ngữ cảnh.

Cuộn, đổi view và mở/đóng điều hướng không được tự làm đổi chiều rộng cấp trang hoặc gây bước tiến/lùi ngoài thao tác được yêu cầu. Không dùng vòng gọi `scrollTo` để giành quyền điều khiển cuộn của người học. Chi tiết selector và kích thước lấy từ kit, không áp cơ chế spacer cũ lên rail mới.

Mỗi mục điều hướng là một view có phạm vi rõ. **Nhật kí** và **Ôn lại** là hai khu vực độc lập trong nguồn/DOM, không chỉ được tách bằng JavaScript. Cơ chế giới hạn nhánh sâu chỉ giữ để tương thích nguồn cũ, không dùng làm mẫu sản xuất mới. `Back`, tải lại, liên kết sâu và `Toàn văn` phải lần lượt khôi phục đúng phạm vi đã chọn hoặc toàn bộ cây canonical; không tạo bản sao nội dung thứ hai.

## 4. Hợp đồng của các vùng chính

### 4.1. Bắt đầu

- Hiển thị mục tiêu bằng ngôn ngữ người học và chỉ rõ hành động đầu tiên.
- Không dùng bảng mã, ma trận quản lí hoặc một bảng “cách học” biến Sửa lỗi thành chặng tuyến tính.
- Chỉ dẫn ngắn có thể đặt trong khối `guidance`; theo `QD_004`, mọi khối `Cách thực hiện`, kể cả ở Câu hỏi khởi động, mặc định đóng nếu không có quyết định mới cho một khối cụ thể.
- Sau câu hỏi khởi động phải có đường đi theo kết quả: học tiếp, mở đúng tài nguyên Nền hoặc quay về câu đang vướng. Bảng chọn phần cần ôn dùng tên chính thức và mô tả người học hiểu được.

### 4.2. Bài học

- Mục kiến thức được đánh số liên tục `1.`, `2.`, …; mục con dùng `1.1.`, `1.2.`, … trong cả G01 và G02. Khởi động và Khép lại là khu vực cấu trúc, không lấy số mục kiến thức. Số Nhiệm vụ thuộc nhóm chức năng riêng, không chen vào hoặc làm khuyết dãy số mục kiến thức; không đặt lại số Luyện tập qua chặng. Giữ ID/đích liên kết khi sửa số hiển thị. Quy tắc được kiểm bằng guard ký pháp/số mục theo QD_029, không suy số mục G02 phải bằng G01.
- Mỗi mục tiêu có giải thích, ví dụ hoặc câu dừng phù hợp; không lặp nguyên văn tiêu đề ngay bên dưới.
- Định hướng dài được thu gọn; yêu cầu bắt buộc trước một nhiệm vụ độc lập phải nhìn thấy đúng lúc.
- Sau một cụm tự kiểm phải có đích rõ: đối chiếu lời giải, hỗ trợ đúng nhu cầu và tiếp tục mạch Bài học. Tham chiếu bài luyện không biến Bài học/Luyện tập thành luân phiên bắt buộc.

### 4.3. Luyện tập và checkpoint

- Mỗi chặng nêu mục tiêu, nhiệm vụ và checkpoint kết thúc.
- Checkpoint cho biết bằng chứng cần đọc, tên lỗi hoặc thiếu nền bằng ngôn ngữ chính thức, đích hỗ trợ, câu xác nhận và điều kiện đi tiếp.
- Tổng điểm không được che một lỗi thiết yếu. Bài đã lộ lời giải không được đổi mã để tính là bằng chứng mới.

### 4.4. Kiểm tra

Hai quy tắc Kiểm tra QD_024 tại Mục 2.3.1 của [01](01_kien_truc_hoc_tap.md) có phạm vi **toàn bộ các gói của chương trình**, không chỉ R1. Không vì phạm vi giao diện R1 của tệp này mà thu hẹp chúng hoặc ép Khảo sát D0 thành Kiểm tra.

- Cách học và lời dẫn trước đề phải nhất quán: đã chuẩn bị kĩ lưỡng hoặc đủ tự tin thì có thể thực hiện Kiểm tra; không yêu cầu bài làm độc lập trước đó để được vào.
- Trước đề, nói rõ một lượt Kiểm tra không chia thành nhiều đợt/buổi. Hướng dẫn chia việc học thành nhiều buổi phải giữ ngoại lệ này. Tự tin không tự chứng nhận đã đạt mục tiêu.
- Điều kiện tự làm và yêu cầu chưa xem lời giải phải hiển thị trước đề.
- Kết quả ban đầu được giữ riêng với kết quả sau sửa.
- Sai mục tiêu nào thì gọi đúng tuyến Sửa lỗi hoặc Nền của mục tiêu ấy; không bắt học lại toàn gói nếu bằng chứng khác còn hợp lệ.

### 4.5. Ôn lại

- Nhiệm vụ Ôn lại là nhiệm vụ mới theo khoảng trễ, không phải làm lại nguyên bài đã sai.
- Khi mở hỗ trợ, URL hoặc cơ chế tương đương phải giữ đúng lượt Ôn lại, checkpoint và nhiệm vụ gọi. Click, Back, tải lại, truy cập trực tiếp và nhiều tab không được làm mất hoặc ghi đè ngữ cảnh của nhau.

## 5. Hợp đồng của lớp hỗ trợ

### 5.1. Ôn nền

Mỗi tài nguyên Nền sở hữu trọn dấu hiệu cần dùng, giải thích, ví dụ, câu xác nhận, đáp án/tiêu chí và điểm quay về. Câu xác nhận nằm trong tài nguyên này, không rơi thành vùng Tự kiểm tra của mạch chính. Gói gọi nguồn canonical dùng chung khi phù hợp; không sao chép thành nhiều bản sửa độc lập.

### 5.2. Sửa lỗi

Người học phải tra được theo **nơi phát hiện** và theo **tên lỗi**. Bảng định tuyến dùng nhãn chính thức, không phơi mã `G01-E..`, `S-L`, `S-K`, `S-O` trong ô nhìn thấy. Một nhiệm vụ sửa chỉ có một nguồn nội dung và có thể được gọi từ nhiều checkpoint với ngữ cảnh riêng.

### 5.3. Lời giải

Mỗi nhiệm vụ độc lập có một đích lời giải xác định. Chỉ yêu cầu liên kết quay lại đề khi đề và lời giải thực sự ở hai vị trí tách biệt; khi cùng tài nguyên/vùng đọc thì dùng đối chiếu tại chỗ, không thêm liên kết nhảy thừa (Mục 3). Lời giải mặc định đóng; toàn bộ đáp án, lời giải hoặc hướng dẫn chấm tách khỏi đề phải nằm trong khối `solution`. Ví dụ đã giải trong mạch chính không được lặp lại thành một lời giải thứ hai. Nhóm Khởi động/Tự kiểm/Luyện tập/Kiểm tra/Ôn lại/S-L/S-K/S-O phải khớp nhiệm vụ thật; Chuyển giao riêng khi gói có nhánh ấy, không tạo nhóm rỗng để bằng số nhóm gói khác.

### 5.4. Nhật kí

Giao diện và bản in dùng đúng **14 trường** đã duyệt tại Mục 2.8 của [kiến trúc học tập](01_kien_truc_hoc_tap.md). Không rút riêng một gói còn sáu trường, không đổi tên trường và không thêm cụm giải thích vào tên trường. Giá trị ví dụ dùng tên bài, mục tiêu, lỗi và checkpoint chính thức; mã máy chỉ nằm ở dữ liệu hoặc thuộc tính kỹ thuật.

QD_033: lưu bài làm/kết quả đối chiếu tại Điểm dừng không đồng nghĩa phải mở Nhật kí. Không yêu cầu ghi Nhật kí ở mọi Điểm dừng hoặc dùng việc ghi làm khóa điều hướng; ghi theo ngữ cảnh tại 01/2.4, chỉ điền dữ liệu đã có.

## 6. Vùng đọc và nhịp đọc

Mỗi vùng sở hữu trọn một bước đọc có nghĩa: nhãn, tiêu đề, lời dẫn, công thức, hình/chú thích và hành động liên quan ở **bên trong** cùng vùng. Chia theo kết quả đọc hoặc thao tác, không theo số heading, độ cao màn hình hay số hộp. Không thả link ngược/giới thiệu trên nền trống; hero, điều hướng, Ủng hộ và footer có vai trò riêng.

Một cấp giấy, một inset, cùng trục nhãn–heading–summary–nội dung; không cộng thụt lề hoặc giấy trong giấy. Bản đồ từng trang ghi owner/ID nguồn, kết quả đọc, lí do ghép/ngắt và liên kết chuyển bước. G01 154 vùng/12 view và cột 816px là hiện thực của kit, không là chỉ tiêu kiến trúc cho G02/Nhà/D0. Bìa chiếm workspace; cột đọc có lề thở phải.

Giấy nội dung trắng tách canvas sáu nền. Token, font, cỡ và controller lấy từ kit đã chốt, không tạo palette khác. Câu nhận diện đầy đủ và bộ chọn sáu radio tròn một hàng/Sắc xám bằng biểu tượng được quy định tại hợp đồng kit; không bỏ tên trợ năng khi bỏ chữ hiển thị. Không mở lại art direction 9/10 hoặc coi 1 điểm tương lai là lỗi chặn.

Trong G01/G02, **mọi hộp có cơ chế đóng/mở mặc định đóng** theo FB036; deep-link mở đúng ancestor chứa đích. Điều kiện tự làm bắt buộc phải nhìn thấy trước nhiệm vụ, không bị giấu trong hộp đóng. Nội dung mạch chính không có cơ chế thu gọn vẫn hiện; không suy quy tắc này sang Nhà/D0.

## 6.1. Thẻ nhiệm vụ, bảng, hình và nhãn

- Mỗi nhiệm vụ, gợi ý và lời giải có ID duy nhất; tiêu đề nhìn thấy mô tả nội dung, không dùng mã quản lí làm tên.
- Bảng dùng ngôn ngữ tám loại của Design 0.4 theo Mục 6.1.1/QD_030. Header lời văn và Nhật kí căn trái; bảng giá trị, ma trận số, bảng dấu và BBT có căn riêng theo quan hệ toán. Bảng có liên kết vẫn nhận đủ component và ngữ nghĩa, không bị bỏ qua bởi bộ dựng.
- Chọn cách responsive theo vai trò: bảng hẹp có thể co; bảng quan hệ hoặc bảng biến thiên cuộn ngang trong vùng riêng. Không áp dụng một phép biến đổi mobile cho mọi bảng nếu làm sai quan hệ hàng–cột.
- Đồ thị SVG theo profile 0.4 opt-in, cỡ tự nhiên/nhãn tương đương chữ, không kéo `width:100%` để lấp giấy; hình và chú thích cùng vùng, thiếu chỗ cuộn cục bộ. BBT web native/MathML từ JSON canonical, giữ mốc/dấu/giới hạn/cột loại và lỗi sai có chủ ý. Pipeline cũ giữ tương thích ngoài phạm vi đã chuyển. Kiểm tải hình thật, không chỉ tồn tại `img`.
- Không lặp nguyên văn tiêu đề bằng một dòng nhãn ngay dưới. Không dùng màu để thay ý nghĩa hoặc trang trí mã quản lí.

Tên khu vực lấy từ danh mục nhãn QD_023; tên bảng/tiêu đề cụ thể của gói lấy từ nguồn và ánh xạ được duyệt, không áp một tên riêng bằng suy luận từ loại Nhiệm vụ. Một nhãn vai trò không lặp từ nguồn và adapter. Hai hành động khác chức năng phải khác nhãn, như “Xem công thức để kiểm tra” và “Xem lời giải”. Trang Nguồn giữ vai trò/cỡ chữ như vùng tham khảo, không dùng wrapper footer.

Ảnh toán trên bìa không nền; khung vuông/dọc/ngang, mỗi loại hai cỡ, sáu nền sáng/tối Đỏ/Vàng/Xám ZO là lựa chọn biên soạn, không thêm controls cho học sinh. Gói dùng hình tiêu biểu của chính mình. Thẻ tải PDF có ba phần tiêu đề/mô tả–số trang–nút tải, thích ứng mobile; số trang từ PDF thật không chứng minh PDF đã đồng bộ. Footer website ngoài `main`, lấy thông tin từ cấu hình, không bị Ủng hộ thay thế hoặc làm đổi phần phía trên đã duyệt.

### 6.1.1. Ngôn ngữ bảng 0.4 — QD_030, dùng chung toàn khóa

Chủ trì yêu cầu ngày 11/10/2026 đưa ngôn ngữ bảng 0.4 thành quy tắc chung của khóa. Phạm vi là các trang và gói thuộc khóa, không tự thay mặc định toàn repository hoặc nâng Design lên 0.5. Căn cứ: `02_quy_chuan/02_noi_dung_toan_hinh_bang.md`, `07_mau_thi_giac/design/table_samples.json`, `07_mau_thi_giac/source/table_engine.py` và các selector bảng trong `source/system.css` của package Design 0.4. Đây là chủ sở hữu quy tắc; kit giữ hiện thực và binding vai trò, không thêm từ điển cạnh tranh.

| Loại | Chức năng và cách đọc | Cách trình bày |
|---|---|---|
| Giá trị (`values`) | Mỗi cột nối một đầu vào với giá trị tương ứng | Ô toán căn giữa cả hai hàng, cỡ tự nhiên, không trải rộng bảng ngắn; giữ đúng cặp đầu vào–giá trị |
| Dữ liệu/tần số (`frequency`) | Đọc số theo cột, giữ đơn vị ở đầu cột | Số căn phải, số có bề rộng ổn định; nhãn căn trái. Bản chuyển vị vẫn giữ hướng nguồn, không đảo hàng/cột để giống mẫu |
| Đối chiếu (`comparison`) | So khái niệm, điều kiện, biểu diễn hoặc nhận định theo tiêu chí | Lời văn căn trái, cột tiêu chí ổn định; hai khái niệm đặt cạnh nhau không biến toàn cột đầu thành row header |
| Hai chiều (`matrix`) | Hai đầu hàng–cột định vị từng ô | Ô số căn giữa; nhãn hàng/cột lời văn căn trái; ô góc có tên trợ năng khi không có chữ nhìn thấy |
| Dấu (`sign`) | Giữ phân biệt mốc và khoảng, đọc dấu của từng hàng | Lưới toán căn giữa; hàng kết quả nhấn Vàng 1, dấu không mang nghĩa qua màu. Bản giải thích có cột kết luận giữ chữ trái, chỉ các cột dấu căn giữa |
| Biến thiên (`variation`) | Nối mốc, dấu/trạng thái và chiều biến thiên | Native HTML/MathML từ JSON; hàng hàm số phẳng; giữ điểm loại, giới hạn một phía, ô khoảng và lỗi sai có chủ ý. Không thêm hàng đạo hàm còn thiếu |
| Tiêu chí (`rubric`) | Đọc tiêu chí, bằng chứng hoặc cách chấm | Nhãn/diễn giải căn trái; biến thể tiêu chí giữ cột tên 18% theo mẫu, phần diễn giải rộng. Cột điểm thuần số căn phải, cột mô tả cách chấm căn trái. Biến thể mục tiêu–bằng chứng không tự thêm các mức đạt/chưa đạt không có trong nguồn |
| Quy trình/thuật ngữ (`process`) | Tra việc cần làm, nguồn hỗ trợ, nơi quay về, trường ghi hoặc thuật ngữ | Nhãn và mô tả căn trái; số bước hẹp/mờ chỉ khi thật sự có số bước. Bảng hỗ trợ không tự trở thành tiến trình bắt buộc |

Mọi loại có lưới ngang–dọc đầy đủ, nét 1 px đồng đều; header Xám 2, row header xám rất nhạt; chữ bảng lời văn 0,88 lần chữ xung quanh, bảng dấu/BBT toán 1 lần. Công thức render từ LaTeX và giữ baseline native theo QD_029. Không dùng màu thương hiệu để tự gán đúng/sai. Vàng 1 chỉ hàng/cột có vai trò đọc đã xác định, Vàng 2 chỉ ô giao đã xác định, Xám 2 cho tổng thật; không tạo tổng hoặc nhấn ngẫu nhiên khi dữ liệu không yêu cầu.

Giữ cấu trúc, nội dung, ID, liên kết, thứ tự và đơn vị. Ngữ nghĩa `th/scope` theo vai trò thật, không chỉ theo vị trí. Bảng hẹp co tự nhiên; bảng rộng cuộn ngang cục bộ có focus/tên trợ năng, không thu chữ đến khó đọc hoặc làm tràn trang. Không chuyển bảng thành thẻ mobile khi mất quan hệ hàng–cột. Caption/tên trợ năng lấy nguồn hiện hành; không lặp caption nhìn thấy nếu nội dung đã có lời dẫn/chú thích.

Mỗi bảng thường có binding loại/chức năng tường minh trong `profiles/course-tables.json` của kit; width/nhãn nguồn R1 vẫn từ metadata QMD. Bảng toán lấy loại từ các hàng/chiều literal của JSON đã kiểm, không suy toán từ tiêu đề hoặc CSS. Bảng mới chưa phân loại, selector thiếu/trùng hoặc dữ liệu JSON lệch phải làm build FAIL; không được fallback về một kiểu chung. Một nguồn Nhật kí và cùng vai trò liên gói dùng cùng loại/biến thể. Nhà không có bảng thì không tạo bảng để đủ quota. PDF được điều hành cùng vai trò nhưng hiện thực/kiểm dàn trang riêng khi được giao, không xem HTML PASS là PDF đồng bộ.

### 6.2. Hệ nhãn QD_025 và mục lục

[Danh mục kiến trúc](danh_muc_kien_truc_hoc_tap.yml), phần `label_contract`, là từ vựng chính thức. Phân biệt nhãn kiến trúc, loại nội dung, chức năng nhiệm vụ, tiêu đề cụ thể và dòng nhãn hiển thị. Nhãn kiến trúc cấp gốc cho tên điều hướng ổn định; các mục toán học bên trong có tiêu đề riêng. Nhãn loại phục vụ trình bày/kiểm kê, không tự tạo menu, bộ lọc hoặc một hộp mới.

Nhãn hiển thị chỉ bổ sung ngữ cảnh chưa rõ từ tiêu đề/vùng đọc. Tiêu đề Ôn nền, Nhật kí, Nguồn hoặc Lời giải không cần dòng nhãn cùng chữ; Ví dụ 03 không cần nhãn VÍ DỤ lặp tiền tố. Metadata, heading và tên truy cập vẫn giữ đủ nghĩa. Không trải toàn bộ cây cha–con thành một nhãn dài, không thay heading bằng chữ nhỏ hoặc thêm aria-label khiến đọc lặp.

Một nhóm nhiệm vụ cùng chức năng dùng một dãy liên tục trong gói. Chặng, lượt, mục toán và vùng đọc không làm dãy số bắt đầu lại. Giữ phân biệt Khởi động/Tự kiểm tra/Luyện tập/Kiểm tra/Ôn lại/Sửa lỗi/Xác nhận nền theo danh mục. Nhiệm vụ con có ID và bằng chứng riêng; không tự hòa vào số bài chính. Số và tên cụ thể cần bảng áp dụng của gói, không sao chép số G01 sang G02.

Trong Lời giải, tên nhóm phản chiếu nơi chứa nhiệm vụ; không thêm tiền tố Lời giải ở mọi tiêu đề. Đề, đáp án, routing và dẫn chiếu dùng cùng một ánh xạ theo ID; dẫn từ nơi khác phải đủ nhóm/ngữ cảnh, không chỉ ghi số trần. Mục lục chọn các điểm thật sự giúp tìm nơi đọc từ cây nguồn; không quét mọi nhãn thành TOC hoặc dựng TOC thủ công cạnh tranh.

Giữ nhãn/heading/nội dung bên trong vùng, cùng trục đã duyệt. QD_023 không đổi kiểu chữ, màu, inset, controller hoặc thiết kế 9/10; không là nâng Design 0.5. G01 đã áp dụng tại DH_015, G02 tại DH_016; trạng thái nguồn, phép kiểm và duyệt HTML ghi riêng ở 03/profile, không được nhận là đã nghiệm thu chỉ vì cùng CSS.

## 7. Responsive, khả năng truy cập và trạng thái bền

- Không tràn ngang cấp trang ở desktop 1440 px, mobile 430 px và 390 px. Vùng cuộn ngang cục bộ phải nhận biết và thao tác được.
- Kiểm rail/toolbar/nút mobile trên view dài và ngắn; chiều rộng layout không đổi và cuộn thực không tự tiến/lùi. Kiểm resize, dialog, focus và vị trí đích dưới toolbar.
- Nội dung mobile giữ cỡ chữ đọc được; nút và summary có vùng thao tác phù hợp; focus nhìn thấy; thứ tự Tab theo thứ tự đọc.
- `details` dùng đúng `summary`; trạng thái đóng/mở không làm mất anchor hoặc focus.
- Liên kết sâu, Back, tải lại, truy cập trực tiếp và nhiều tab phải được kiểm ở các nhánh có lưu ngữ cảnh.
- Không quảng bá lưu tiến độ tự động nếu sản phẩm chưa có chức năng ấy.

## 8. Cổng nghiệm thu HTML và khóa PDF

Kiểm tự động chỉ chứng minh các bất biến đã mã hóa; không thay nghiệm thu của con người. Một lượt xin duyệt HTML tối thiểu phải có:

- nguồn/checker đạt trong phạm vi;
- kiểm trình duyệt ở 1440, 430 và 390 px;
- phép đo cuộn trên mọi view và các trạng thái điều hướng: không có bước lùi, không có sai số vị trí cuộn ngoài thao tác quá 1 px và không đổi chiều rộng cấp trang;
- bàn phím và trạng thái không JavaScript;
- ở trạng thái không JavaScript, kiểm cả ảnh và computed style của bề mặt đọc; không chỉ kiểm nội dung còn tồn tại trong DOM;
- đường hỗ trợ đại diện qua click, Back, tải lại, truy cập trực tiếp và nhiều tab;
- lát cắt hình ảnh đủ đọc cho đầu trang, một checkpoint, một tuyến Nền/Sửa lỗi, Nhật kí, bảng và lời giải;
- kiểm hồi quy mọi gói dùng component chung bị tác động.

Ảnh toàn trang thu nhỏ không thay các lát cắt có thể đọc. Báo cáo phải phân biệt HTML vừa dựng với đầu ra cũ và phân biệt PASS kỹ thuật với việc người chủ trì chấp nhận.

Trong thời gian HTML chờ duyệt, không dựng hoặc sửa các PDF học liệu, metadata số trang hay provenance PDF. Việc người chủ trì chấp nhận HTML chỉ mở khả năng giao một nhiệm vụ PDF riêng; không tự cấp quyền dựng PDF, commit, push hoặc phát hành.

## 9. Hàng rào chống tái diễn

Checker và rà thủ công phải chặn ít nhất các lỗi sau:

- mã quản lí xuất hiện thay tên chính thức trong văn bản người học;
- disclosure G01/G02 vô cớ mở sẵn; điều kiện bắt buộc bị giấu;
- tên trường Nhật kí khác schema 14 trường đã duyệt;
- lời giải hoặc đáp án nằm ngoài khối `solution`;
- tiêu đề bị lặp ngay bên dưới;
- bảng có liên kết mất khung, header hoặc cách đọc responsive;
- đồ thị không tải, BBT native thiếu MathML/dữ liệu hoặc alt/caption mang mã kỹ thuật;
- JavaScript sửa thứ tự sư phạm bằng cách di chuyển vùng nội dung lớn;
- điều hướng làm mất ngữ cảnh checkpoint/lượt học khi Back, tải lại, truy cập trực tiếp hoặc dùng nhiều tab;
- điều hướng trộn Mạch học chính, Hỗ trợ khi cần và Tiện ích thành một hàng phẳng, hoặc đặt Sửa lỗi chen giữa Kiểm tra và Ôn lại trong mạch chính;
- rail/nút mobile mất khi cuộn; điều hướng tạo tràn cấp trang, đổi chiều rộng hoặc giật; dialog thiếu Escape/focus;
- một khu vực hiển thị lẫn hỗ trợ độc lập do sai ownership/phạm vi, đặc biệt gộp Nhật kí vào Ôn lại, hoặc view hỗ trợ không được cô lập khi click, Back và tải lại;
- biến thứ tự mục lục thành quy trình học bắt buộc; ép ghi Nhật kí ở mọi Điểm dừng; thêm liên kết quay lại đề vô điều kiện dù cặp đề–lời giải đã ở cùng vùng;
- lớp thị giác thử nghiệm chỉ tạo bề mặt đọc sau khi JavaScript chạy, hoặc nhân bản bộ chọn nền/chế độ màu thành nhiều nguồn độc lập;
- ghi “đã nghiệm thu” khi mới chỉ có kết quả checker hoặc ảnh do agent tạo.

Trạng thái sản phẩm chỉ ở [bảng điều hành](03_dieu_hanh_chuong_trinh.md) và hồ sơ gói. QD_021 thu hồi sơ đồ DH_011; G01 đã sửa tại DH_015, G02 đã áp dụng/kiểm tại DH_016. Trạng thái duyệt vẫn ghi riêng theo từng bản. Giữ thiết kế 9/10 và nghiệm thu lịch sử đúng bản. Hợp nhất chuẩn không tự sửa học liệu, mở PDF/phát hành hoặc khóa Design 0.5.
## Bổ sung đã duyệt QD_025

`function.guided_thinking` (Gợi mở) là chức năng Nhiệm vụ trước lời giải thích trong Bài học. Nhãn BÀI HỌC • GỢI MỞ; số liên tục riêng toàn nhóm. Lời dẫn: “Thử trả lời trước khi đọc tiếp.” Không gộp với Tự kiểm tra, không tạo nhóm đáp án trống hoặc chép lại lời giảng. Nguồn Nền dùng định danh trung tính; số/tên hiển thị của từng gói nằm ở binding của gói, không ghi cứng số G01 vào include dùng chung. Bổ sung này mở rộng danh mục QD_023, không thay kiến trúc hoặc thiết kế đã duyệt.

