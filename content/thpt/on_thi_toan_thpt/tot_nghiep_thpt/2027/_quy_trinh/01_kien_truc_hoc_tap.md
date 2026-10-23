# Kiến trúc học tập chung

Phiên bản: 0.8 · Ngày biên tập: 12/10/2026 · Đường học QD_033 (kế thừa phần không bị thay của QD_021); hệ nhãn QD_025 (kế thừa QD_023); Kiểm tra QD_024.

Nguồn chuẩn dùng chung về hành trình học của toàn bộ chương trình Ôn thi Toán THPT 2027. Kế thừa đặc tả 0.2 và phần còn hiệu lực của QD_016–018/QD_021; QD_033 giữ Bài học → Luyện tập → Kiểm tra → Ôn lại là tiến trình chuẩn được khuyến nghị, đồng thời thay cách hiểu coi tiến trình này là điều kiện bắt buộc phải hoàn thành tuần tự, cùng các yêu cầu ghi Nhật kí ở mọi Điểm dừng và liên kết quay lại đề vô điều kiện. Việc cập nhật chuẩn không chứng nhận mọi đường học trong sản phẩm đã đạt. [Điểm vào](README.md).


## Phạm vi và cách thay đổi

Các mã mục 2.x được giữ để đối chiếu PDF ngày 06/10; chúng là mục trong tệp này. Không cần mở PDF để áp dụng phần quy phạm đã chuyển vào đây.

Hạt nhân bắt buộc là quan hệ mục tiêu–hoạt động–bằng chứng–phản hồi–hành động tiếp theo. Số chặng, số câu, thời lượng và lịch ôn là tham số từng gói. Một thay đổi tham số được ghi trong hồ sơ gói; chỉ thay tệp này khi quy tắc chung thực sự cần đổi.

Phân biệt bốn lớp khi áp dụng: kiến trúc học tập; nội dung toán học; dữ liệu vận hành; giao diện xuất bản. Một thay đổi ở một lớp không tự cho phép đổi lớp khác. Cấu trúc và hành vi trang người học được cụ thể hóa tại [Quy chuẩn cấu trúc trang người học](07_quy_chuan_cau_truc_trang_nguoi_hoc.md). [Danh mục 08](08_danh_muc_tham_quyen_dieu_hanh.md) xác định các nguồn cần đồng bộ. Manifest/checker chỉ chứng minh phần dữ liệu đã kiểm; khi nguồn thực khác quy tắc này, ghi khoảng cách ở hồ sơ gói, không sửa quy tắc theo hiện trạng sai hoặc gọi `planned=0` là hoàn thiện.

Khi đổi quy tắc chung: ghi vấn đề và các gói chịu ảnh hưởng; người chủ trì chốt nội dung; cập nhật phiên bản tệp, nhật kí quyết định và danh sách cần rà lại trong bảng điều hành. Không tự áp dụng hồi tố hàng loạt vào gói đã phát hành.

## Hạt nhân kiến trúc

## 2.1. Đơn vị chung là một chu trình có quyết định

Mỗi chặng Luyện tập phục vụ một cụm mục tiêu có quan hệ gần nhau. Học sinh biết cần làm được gì, tự giải một cụm bài, đối chiếu tại Điểm dừng, rồi đi tiếp hoặc nhận hỗ trợ và thử lại. Chặng luyện không phải một chu kì bắt buộc luân phiên Bài học–Luyện tập.

**Cùng kiến trúc không có nghĩa mọi gói phải có cùng số chặng, số câu, số lỗi hoặc số trang.** Điều dùng chung là quan hệ giữa hoạt động, bằng chứng và quyết định. R1-G01 giữ ba chặng; gói hình học hoặc xác suất có thể cần cách chia khác nếu các mục tiêu và tiên quyết đòi hỏi.

| Thành phần | Chức năng bắt buộc | Được thay đổi theo gói |
|---|---|---|
| Bắt đầu | Nêu mục tiêu, tiên quyết và hành động đầu tiên | Số câu khởi động, cách thể hiện |
| Bài học | Giải thích, ví dụ và câu dừng theo mạch toán học | Biểu diễn, độ dài, điểm nghỉ |
| Luyện tập theo chặng | Tự làm, đối chiếu bằng chứng tại Điểm dừng và chọn việc tiếp theo | Số chặng, số bài và tiêu chí theo mục tiêu |
| Kiểm tra độc lập | Thu bài làm chưa xem lời giải và đọc theo mục tiêu | Số câu, định dạng, thời lượng |
| Ôn lại | Gọi lại mục tiêu sau khoảng trễ bằng nhiệm vụ dành riêng | Ngày hẹn, số lượt, mức phối hợp |
| Ôn nền | Bổ sung đúng tiên quyết rồi kiểm tra lại | Những đơn vị nền thực sự cần |
| Sửa lỗi | Xác định bước sai, sửa lý do và thử nhiệm vụ khác | Danh mục lỗi, số biến thể |
| Lời giải | Đối chiếu bài làm với lời giải hoặc tiêu chí | Nhóm đáp án ứng với nhiệm vụ thật |
| Nhật kí | Ghi kết quả, quyết định và nơi tiếp tục khi cần | Nội dung ghi theo 14 trường chung |

D0 là công cụ định vị đầu vào của chương trình; một đơn vị Nền là tài nguyên hỗ trợ hẹp; một đề tổng hợp là công cụ đánh giá và luyện chiến lược. Không ép ba loại này vào nguyên mẫu trang R1-G01. Chúng dùng lại các hợp đồng phù hợp như tự làm, phản hồi, thử lại và ghi kết quả.

## 2.2. Mục lục và hành trình học có quan hệ thế nào

Giữ năm mục điều hướng đã được chọn: **Bắt đầu, Bài học, Luyện tập, Kiểm tra, Ôn lại**. Gọi chúng là “khu vực”, không gọi là năm bước bắt buộc mà ai cũng phải đi qua đúng một lần.

Bài học là nơi lưu lời giảng theo mạch toán học. Luyện tập tổ chức việc tự làm theo chặng. **Bài học và Luyện tập không xen kẽ nhau.** Liên kết từ bài luyện tới đoạn học cần xem lại là hỗ trợ theo nhu cầu, có đường trở về nhiệm vụ; không phải lệnh bắt luân phiên hai khu vực.

Người mới có thể bắt đầu từ Khởi động trong Bài học; người đã nắm phần học có thể vào Luyện tập; quyền vào Kiểm tra theo Mục 2.3.1. Đây là những gợi ý điểm vào, không phải một lộ trình bắt buộc chung. Tự đánh giá diễn ra tại Điểm dừng của hoạt động đang làm, không chờ hoàn thành cả mạch. Ôn lại phục vụ việc khơi lại kiến thức sau khoảng trễ; người học chọn lượt phù hợp với việc đã học, không phải đi lại từ Bài học chỉ để được ôn.

Các mục tiêu cần đạt phải có bản tóm tắt nhìn thấy ở Bắt đầu và đầu mỗi chặng. Phần định hướng dài trong Bài học có thể tiếp tục đặt trong khối đóng/mở. **Ẩn phần diễn giải dài không đồng nghĩa ẩn điều kiện học xong.**

### 2.2.1. Mạch chính và các nhánh không đồng nghĩa một chuỗi bước

**Bài học → Luyện tập → Kiểm tra → Ôn lại là tiến trình chuẩn được khuyến nghị và cũng là thứ tự tổ chức/tra đọc của gói.** Bốn khu vực có chức năng khác nhau; tiến trình chuẩn này không phải điều kiện bắt buộc phải hoàn thành tuần tự hoặc phải hoàn thành khu vực trước mới được vào khu vực sau. Học sinh được chọn điểm vào theo nhu cầu, mức chuẩn bị và bằng chứng học tập hiện có; được đi tới hoặc quay lại theo Mục 2.3. Quyền chọn điểm vào không tự chứng nhận phần bỏ qua đã đạt. Bắt đầu là khu vực định hướng, không thêm một chặng học thứ năm.

**Ôn nền, Lời giải, Sửa lỗi và Nhật kí là các hỗ trợ độc lập, được gọi theo ngữ cảnh.** Không đặt chúng làm con của một khu vực học cố định hoặc bắt đi qua tất cả hỗ trợ. Các chức năng sau có thể được gọi từ hoạt động/nhiệm vụ đang làm:

- **Ôn nguồn:** xem lại đúng phần Bài học trong gói hoặc đúng tài nguyên Ôn nền ngoài nội dung của gói khi gặp trở ngại. Đây là tên chức năng nội bộ bao quát hai đích hỗ trợ, không quyết định đổi tên menu Ôn nền hoặc trang Nguồn (tài liệu tham khảo).
- **Đối chiếu và sửa lỗi:** giữ bài làm tự lực, đối chiếu lời giải/tiêu chí, xác định bước sai và nhận hỗ trợ phù hợp. Có thể diễn ra sau nhiệm vụ trong Bài học, sau chặng Luyện tập, sau bài Kiểm tra đã hoàn tất hoặc sau nhiệm vụ Ôn lại. Không bắt chờ tới cuối Kiểm tra mới được sửa. Dùng tuyến hiện có đúng mục tiêu; không tự tạo ngân hàng S-H hoặc mượn bài không phù hợp để lấp đích.
- **Nhật kí:** ghi nơi đang học, kết quả, hỗ trợ và việc tiếp theo khi có quyết định hoặc kết thúc buổi học. Không yêu cầu ghi sau mọi thao tác, không biến Nhật kí thành chặng trước Ôn lại. Giữ đúng 14 trường tại Mục 2.8.

**Ngoại lệ bắt buộc khi đang Kiểm tra:** tự lực hoàn toàn; không mở Bài học, Ôn nền, Lời giải hoặc Sửa lỗi để trợ giúp bài đang làm. Muốn nhận hỗ trợ thì kết thúc lượt kiểm tra trước, giữ riêng bài làm và kết quả ban đầu; phần sau hỗ trợ không được tính ngược thành bằng chứng độc lập của lượt đó. Nhảy trang không hủy điều kiện này. Giao diện chưa khóa truy cập không có nghĩa được dùng hỗ trợ.

Mỗi nhánh giữ nơi gọi và nhiệm vụ/điểm dừng cần trở về. Sau hỗ trợ, quay đúng nơi đang vướng; chuyển hoạt động khi người học chọn và tiên quyết cho phép. Chỉ yêu cầu liên kết quay lại đề khi đề và lời giải thực sự ở hai vị trí tách biệt. Cặp đề–lời giải cùng tài nguyên/vùng đọc giữ đáp án thu gọn và ngữ cảnh tại chỗ, không thêm liên kết nhảy thừa; cùng trang HTML chưa đủ để coi là cùng vị trí (07/3, 5.3). Đọc kết quả, sửa/xác nhận và hẹn ôn có thể có thứ tự cục bộ, nhưng không trở thành các chặng ngang cấp trên bản đồ toàn gói.

### 2.2.2. Ma trận tình huống kiểm đường học

Hợp đồng nội bộ để kiểm nguồn/đầu ra, **không chép nguyên bảng vào hướng dẫn người học**. Thay đích mô tả bằng ID thật khi kiểm gói; thiếu đích phải ghi lỗi, không đánh dấu đạt vì có đủ menu.

| Ca | Hoạt động/tình huống | Hành động và đích hỗ trợ | Điểm trở về/bằng chứng |
|---|---|---|---|
| DH01 | Bài học, thiếu kiến thức của chính gói | Xem đúng đoạn giải thích/ví dụ trong Bài học | Nhiệm vụ đang vướng; không bắt chuyển sang Luyện tập |
| DH02 | Bài học, thiếu tiên quyết | Đúng tài nguyên Ôn nền và câu xác nhận nền | Nhiệm vụ gọi; đạt nền không tự chứng nhận mục tiêu gói |
| DH03 | Đã tự làm nhiệm vụ Bài học, muốn kiểm lại | Đối chiếu lời giải/tiêu chí; sửa khi có lỗi | Nhiệm vụ/điểm dừng Bài học; không đợi Kiểm tra |
| DH04 | Luyện tập, vướng kiến thức trong gói | Xem lại đúng phần Bài học | Bài luyện đang làm; không tạo lịch luân phiên học–luyện |
| DH05 | Luyện tập, thiếu tiên quyết | Ôn nền đúng nhu cầu | Bài luyện/chặng gọi hỗ trợ |
| DH06 | Hoàn tất chặng Luyện tập | Giữ bài làm; đối chiếu checkpoint; sửa/xác nhận nếu cần | Checkpoint chặng; không bắt sửa khi đã đạt |
| DH07 | Kiểm tra đang diễn ra | Chỉ tự lực; chưa mở nhánh trợ giúp | Giữ lượt độc lập; không dùng lời giải làm tiếp rồi gọi là độc lập |
| DH08 | Kiểm tra đã hoàn tất | Giữ kết quả ban đầu; đối chiếu theo mục tiêu; ôn nguồn/sửa nếu cần | Mục tiêu/điểm dừng sau kiểm tra; ghi riêng kết quả sau hỗ trợ |
| DH09 | Ôn lại, vướng kiến thức hoặc tiên quyết | Xem đúng Bài học hoặc Ôn nền | Đúng nhiệm vụ/lượt Ôn lại đang dừng |
| DH10 | Đã tự làm nhiệm vụ Ôn lại, muốn kiểm lại | Đối chiếu; sửa/xác nhận nếu cần | Đúng nhiệm vụ/checkpoint Ôn lại; giữ kết quả ban đầu |
| DH11 | Có quyết định hoặc kết thúc buổi học | Ghi Nhật kí đúng 14 trường, chỉ điền dữ liệu đã có | Ghi nơi tiếp tục; không đổi Nhật kí thành chặng |
| DH12 | Nhảy tới/quay lại khu vực | Cho phép điều hướng; xét tiên quyết/bằng chứng/trạng thái kiểm tra | Không tự đánh dấu phần bỏ qua là đạt; DH07 vẫn có hiệu lực |
| DH13 | Vào thẳng hỗ trợ, không có nơi gọi | Chọn hoạt động/nhiệm vụ để trở về | Không đoán một checkpoint cố định cho mọi người |
| DH14 | Bài xác nhận đã lộ hoặc đã hết bài mới | Áp dụng giới hạn ngân hàng Mục 2.5 | Không tái dùng làm bằng chứng mới; ghi chưa đủ bằng chứng và nơi tiếp tục |

Kiểm cả trường hợp **không cần hỗ trợ**: đủ tiêu chí thì đi tiếp mạch chính, không buộc qua tất cả nhánh. Sơ đồ, lời dẫn, bảng định tuyến và liên kết đều thuộc cùng hợp đồng; một nơi đúng không bù nơi khác sai.

## 2.3. Cửa vào không được kết luận quá khả năng khảo sát

Bốn câu khởi động R1-G01 kiểm tra một số điều kiện nền; chúng không đủ để chứng nhận năm mục tiêu của cả gói. Làm đúng bốn câu cho phép tiếp tục Bài học, không tự động dẫn tới bỏ qua toàn bộ gói.

Quy tắc dùng chung:

- Không biết làm vì chưa học: mở giải thích và ví dụ của đúng mục tiêu; ghi “chưa học”, không kết luận yếu.
- Có dấu hiệu thiếu tiên quyết: vào đúng thẻ Ôn nền, làm câu xác nhận, rồi quay về nhiệm vụ gốc.
- Nếu đã chuẩn bị kĩ lưỡng hoặc đủ tự tin, người học có thể thực hiện Kiểm tra, kể cả vào trực tiếp. Không yêu cầu phải có bài làm độc lập trước đó để được vào Kiểm tra. Nếu Kiểm tra chưa đạt, quay về đúng phần cần học/luyện; chính đề vừa xem không được tính là đề mới ở lần sau.

Không cần xây thêm một bài thi đầu vào cho mọi gói. Chỉ thêm câu khảo sát khi một quyết định điểm vào thực sự thiếu bằng chứng.

### 2.3.1. Quy tắc Kiểm tra toàn chương trình — QD_024

Hai quy tắc này áp dụng cho **toàn bộ các gói của chương trình Ôn thi Toán THPT 2027**, không chỉ R1, ở hoạt động Kiểm tra của gói:

- **Quyền bắt đầu:** đã chuẩn bị kĩ lưỡng hoặc đủ tự tin thì có thể thực hiện Kiểm tra. Tự tin không phải bằng chứng đạt mục tiêu; quyền bắt đầu khác với điều kiện công nhận kết quả hoặc chuyển gói tại Mục 2.7.
- **Một lượt không chia đợt:** không được chia một lượt Kiểm tra thành nhiều đợt/buổi rồi ghép thành cùng một bài kiểm tra độc lập. Quyền chia việc học thành nhiều buổi không áp dụng cho lượt Kiểm tra đang làm. Nếu dừng để nhận hỗ trợ, kết thúc lượt ấy và giữ bài làm ban đầu; phần làm tiếp sau hỗ trợ không tính ngược vào kết quả độc lập ban đầu.

Giữ điều kiện tự lực hoàn toàn ở Mục 2.2.1, phân biệt kết quả ban đầu/sau sửa và giới hạn nhiệm vụ đã lộ ở Mục 2.5. Thời lượng, số câu và thang điểm vẫn là tham số từng gói. Đây là hợp đồng học tập, không phải tuyên bố đã có bộ đếm giờ hoặc khóa điều hướng tự động. Không đổi Khảo sát D0 thành Kiểm tra, không ép tài nguyên Nền hoặc loại gói khác phải có hoạt động Kiểm tra nếu hợp đồng riêng không yêu cầu.

## 2.4. Một Điểm dừng phải giúp ra quyết định

Điểm dừng dùng để đối chiếu bằng chứng và chọn việc tiếp theo, không đặt ra một nghi thức sáu bước áp dụng nguyên xi cho mọi trường hợp:

- Giữ bài làm ban đầu trước khi mở đáp án; phân biệt bài làm tự lực với phần sau hỗ trợ.
- Đối chiếu đúng tiêu chí, xác định mục tiêu đã làm được và mục tiêu còn vướng.
- Chọn đích tiếp theo; chỉ ôn nguồn, sửa hoặc làm bài xác nhận khi kết quả cho thấy cần.
- Tiếp tục hoạt động phù hợp, không bắt đi qua nhánh hỗ trợ khi đã đủ tiêu chí.

**Lưu bằng chứng tại Điểm dừng khác với ghi Nhật kí.** Bài làm ban đầu, kết quả đối chiếu và mức hỗ trợ phải còn phân biệt được để quyết định dựa trên bằng chứng thật; chúng có thể nằm ngay trên bài làm/phiếu đối chiếu. Không yêu cầu ghi Nhật kí ở mọi Điểm dừng. Nhật kí ghi khi cần lưu quyết định, nơi tiếp tục hoặc kết thúc buổi học theo Mục 2.2.1/2.8; không phải điều kiện để mở khu vực tiếp theo. Giữ 14 trường chung, chỉ điền dữ liệu đã có, không bắt điền đủ 14 trường tại từng lần ghi.

| Kết quả quan sát | Việc tiếp theo | Được ghi nhận |
|---|---|---|
| Đúng kết luận, đúng lý do, đáp ứng tiêu chí và chưa xem lời giải | Đi tiếp theo đích đã chỉ | Có bằng chứng độc lập trong lượt này |
| Đáp số đúng nhưng không giải thích được hoặc đã xem lời giải | Làm một câu tương đương còn chưa lộ | Chưa đủ bằng chứng độc lập |
| Sai vì chưa làm được thao tác tiên quyết | Học đúng thẻ Ôn nền rồi làm câu xác nhận nền | Đủ nền cho hoạt động tiếp theo nếu đạt; chưa tự suy ra đạt mục tiêu gói |
| Biết nền nhưng dùng sai khái niệm hoặc điều kiện | Xem đúng đoạn sửa; tự làm bài sửa lỗi mới | Đã sửa mục tiêu cụ thể trong lượt này nếu đạt |
| Sai một phép tính cục bộ, lập luận còn đúng | Tự sửa phép tính; xem lỗi có làm sai kết luận không | Giữ phần bằng chứng còn hợp lệ; không tự xóa lỗi ở mục tiêu đang đánh giá tính toán |
| Thử lại vẫn sai hoặc đã dùng hết bài mới | Đổi cách hỗ trợ; ghi phần chưa đạt và điểm quay về | Không đánh dấu hoàn tất; tiếp tục phần độc lập nếu đủ điều kiện |

Không yêu cầu đúng tất cả chi tiết mới được tiếp tục một nhánh độc lập. Nhưng một lỗi thiết yếu chưa giải quyết phải giữ nguyên trạng thái, không được dùng tổng điểm cao để che đi.

## 2.5. Sửa lỗi cần một phép thử xác nhận, không cần chuỗi vô hạn

Trong hoạt động sửa lỗi, có hai thời điểm khác nhau: **học từ lỗi** và **tự kiểm tra sau hỗ trợ**. Bài đã sai được giữ để phân tích, không tính là bài xác nhận. Sau khi đọc giải thích, học sinh làm một bài khác chưa xem đáp án. Nếu bài đó được làm độc lập và đạt tiêu chí, nó đã là bằng chứng xác nhận trong lượt này; không mặc định đòi thêm một bài thứ ba chỉ vì nó mang nhãn Sửa lỗi.

Nếu học sinh xem đáp án của bài xác nhận trước khi tự hoàn tất, bài ấy chuyển thành tài nguyên học. Lần xác nhận tiếp theo cần một bài khác. Đây là lý do phải theo dõi việc đã gặp bài; đổi mã không làm bài trở thành mới.

Ngân hàng giữ các vai trò Học, Luyện, Sửa, Kiểm tra, Ôn lại và nhánh P; hai chức năng của nhánh P được phân biệt ở 2.5.1. Với R1-G01, giữ các nhóm sửa lỗi sau Luyện tập, Kiểm tra, Ôn lại hiện có để bảo toàn công sức. Với gói mới, số biến thể được xác định từ đường học và nguy cơ dùng lại, không tự nhân số lỗi với ba cho mọi tình huống.

**Khi hết bài mới:** giao diện phải nói rõ “Chưa có bài mới để xác nhận thêm ở mục tiêu này”, đưa về đoạn học cụ thể và cho phép tiếp tục mục tiêu độc lập. Ghi yêu cầu bổ sung vào hồ sơ sản xuất. Không bảo học sinh “tự tìm một câu mới”, không tự sinh một bài chưa kiểm định rồi coi đó là bằng chứng đạt. Hỗ trợ trực tiếp có thể dùng khi cần, nhưng không phải một khoản trả phí bắt buộc để nối một đường học bị thiếu tài nguyên.

### 2.5.1. Phạm vi xác nhận và hai chức năng nhánh theo QD_028

Bài xác nhận phải kiểm đúng thao tác hoặc mục tiêu đang vướng. Cùng họ lỗi không có nghĩa mọi bài khắc phục đều kiểm đủ mọi biểu hiện của họ đó. Đối chiếu nội dung thực của đề và tiêu chí lời giải trước khi gán tuyến; một câu chỉ về lôgarit không xác nhận cả nhánh mũ. Việc đổi tên hoặc content_key không tạo tính chưa lộ: cả ví dụ đã giải, bài trong Nhật kí mẫu và câu đã gặp ở khu vực khác đều phải tính vào độ lộ của nội dung.

**Phối hợp** kết nối kiến thức giữa các gói; **Chuyển giao** áp dụng phương pháp sang họ hàm hoặc bối cảnh mới. Hai chức năng đã được chủ trì duyệt phân biệt tại QD_028, không là hai tên thay thế tùy ý của một chức năng. Danh mục nhãn giữ khóa/tên/phạm vi tương ứng; chỉ dùng khi có nhánh thật, không tạo chặng bắt buộc. Số lượng nhiệm vụ và tiên quyết là tham số riêng của mỗi gói.

## 2.6. Ôn nền phải là một tài nguyên có thể dùng được

Một tuyến nền đủ dùng có: dấu hiệu cần ôn; giải thích ngắn; ví dụ có lời giải; câu tự làm khác ví dụ; đáp án và tiêu chí; điểm quay về. Một liên kết tới chương dài không tự đáp ứng hợp đồng này.

Kho Nền chung được xây dần. Bảy tài nguyên đầu tiên của R1-G01 có một nguồn canonical cho mỗi tài nguyên tại `content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nen/`; gói gọi lại bằng include, không sao chép thành nguồn sửa độc lập. Vị trí này được chọn sau khi kiểm cấu trúc `hoc_lieu/`: đây là nội dung dùng chung giữa các gói, không phải nhiệm vụ quản lý riêng của G01 và không là trang đứng độc lập trong `_quarto.yml`. Người đang thiếu kiến thức rộng hơn phạm vi thẻ cần học phần nền tương ứng, không bị yêu cầu vượt qua bằng vài thao tác đoán đáp án.

### Làm rõ chức năng Ôn lại — VOICE-CONTEXT-20261023

Ôn lại tạo cơ hội tự huy động kiến thức sau khoảng trễ. Không trình bày lại kiến thức, công thức, cách giải hoặc mục “Nhớ lại trước khi làm” trước đề. Mỗi lượt vẫn cung cấp đủ ngữ cảnh, thuật ngữ và quy ước dữ liệu để hiểu đề độc lập. Lời giải và trợ giúp dùng sau khi tự làm; giữ phần làm độc lập riêng với phần sau hỗ trợ. Giọng văn và ngoại lệ thông tin dữ liệu do [07/6.1.6](07_quy_chuan_cau_truc_trang_nguoi_hoc.md#giong-van-ro-nghia-co-ngu-canh) sở hữu.

## 2.7. Hoàn tất gói được hiểu đúng ở hai thời điểm

**Hoàn tất lượt chính:** các mục tiêu thiết yếu có bài làm độc lập phù hợp; lỗi chặn đã được kiểm tra lại; đã ghi những giới hạn còn lại và ngày Ôn lại. Nếu cần sửa sau Kiểm tra, ghi riêng kết quả lần đầu và bằng chứng sau sửa. Không đổi điểm gốc thành điểm của bài đã chữa.

**Duy trì:** học sinh còn làm được mục tiêu sau khoảng trễ thực tế. Một lượt Ôn lại chỉ xác nhận những mục tiêu mà nó thực sự lấy mẫu. Hoàn thành ba lượt không có nghĩa được chứng nhận làm chủ mọi tình huống của chủ đề.

Sau khi hoàn tất lượt chính, học sinh có thể học gói tiếp theo phù hợp tiên quyết trong khi các lượt ôn R1-G01 vẫn đang chờ. Không bắt chờ hết 3–4 tuần mới được học R1-G02.

Lịch ban đầu giữ khoảng 2–3 ngày, 7 ngày và 3–4 tuần, tính từ ngày hoàn tất lượt chính. Đây là quy ước thiết kế được làm rõ trong bản này. Nếu mục tiêu vừa phải sửa lại, hẹn kiểm tra gần hơn cho chính mục tiêu đó và ghi ngày thực; không xóa lịch sử của lần ôn cũ. Khi sát kỳ thi, chỉ kết luận ở khoảng trễ thực đã quan sát.

## 2.8. Nhật kí 14 trường đã duyệt

Giao diện và bản in dùng cùng schema 14 trường; không rút riêng G01 còn sáu trường. Tên trường dưới đây được kế thừa nguyên văn từ Mục 13.2 của đặc tả kiến trúc 0.2 được ghi nguồn tại [Nguồn và chuyển tiếp](06_nguon_va_chuyen_tiep.md), không tự mở rộng hoặc rút gọn trong từng gói:

| STT | Trường |
|---:|---|
| 1 | Ngày–giờ |
| 2 | Gói / mục tiêu |
| 3 | Nguồn phát hiện |
| 4 | Bài làm ban đầu |
| 5 | Mức hỗ trợ ban đầu |
| 6 | Bằng chứng quan sát |
| 7 | Phân loại |
| 8 | Mã lỗi hoặc mã Nền |
| 9 | Hành động |
| 10 | Bài khắc phục mới |
| 11 | Trạng thái sau sửa |
| 12 | Hẹn Ôn lại |
| 13 | Kết quả sau khoảng trễ |
| 14 | Quyết định tiếp theo |

Ví dụ trên giao diện phải mang đủ 14 trường và ghi rõ là giả lập, không phải kết quả thật. Thông tin suy ra tự động phải phân biệt với thông tin học sinh tự báo. Căn cứ cập nhật: báo cáo `_audit/r1_g01_doi_chieu_2026-10-06.md`, chỉ thị triển khai R1-G01 và phản hồi duyệt HTML ngày 06/10/2026 của người chủ trì.

Nhật kí có một nguồn dùng chung tại `content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nhat_ki_hoc_tap.qmd`; G01/G02 include lại, không viết mẫu khác cho từng gói. Tên trường “Bài khắc phục mới” giữ nguyên schema dù tên giao diện tuyến hỗ trợ là “Sửa lỗi”.

## 2.9. Căn cứ khoa học và giới hạn

IES khuyến nghị phân tán việc học, xen ví dụ đã giải với hoạt động tự giải, kết hợp hình với lời và dùng câu hỏi khơi lại kiến thức. Những khuyến nghị này hỗ trợ hoạt động theo mục tiêu và quay lại sau khoảng trễ; không quyết định số chặng, lịch cố định hoặc bắt hai khu vực Bài học–Luyện tập xen kẽ. [Nghiên cứu 1](06_nguon_va_chuyen_tiep.md)

Tổng quan của Wisniewski, Zierer và Hattie cho thấy tác dụng của phản hồi thay đổi đáng kể giữa các điều kiện; lượng thông tin hữu ích trong phản hồi có vai trò quan trọng. Thiết kế của ZO Math vì thế phải chỉ rõ bước sai và hành động tiếp theo, thay vì chỉ hiện đáp án hoặc điểm. [Nghiên cứu 2](06_nguon_va_chuyen_tiep.md)

Nghiên cứu của Rohrer, Dedrick và Burgess xem xét luyện toán xen kẽ, trong đó người học phải chọn chiến lược từ đề bài. Đây là căn cứ để đưa phối hợp vào sau khi có nền thích hợp; không phải lý do bắt người mới học tự chọn giữa hàng loạt công cụ chưa hiểu. [Nghiên cứu 3](06_nguon_va_chuyen_tiep.md)

Các quyết định cụ thể trong tài liệu này là thiết kế của ZO Math dựa trên nguồn và hiện vật. Chưa có dữ liệu sử dụng đủ để gọi chúng là kiến trúc tối ưu hoặc cam kết tăng điểm thi.

## Hệ nhãn học liệu QD_025 (kế thừa QD_023)

Áp dụng cho toàn bộ các gói của chương trình Ôn thi Toán THPT 2027, không chỉ R1. Nhãn kiến trúc nhận diện khu vực/nhóm/điểm trong cây nội dung; nhãn loại nhận diện đơn vị như Định nghĩa, Ví dụ hoặc Nhiệm vụ. Chức năng nhiệm vụ, mục tiêu, độ lộ và điều kiện tự lực là dữ liệu riêng, không bị tên gọi chung Nhiệm vụ thay thế. Chỉ dùng những khu vực/loại/chức năng có nội dung thực của gói, không ép D0 hoặc tài nguyên Nền có mọi khu vực R1. Danh mục duy nhất về khóa, tên và phạm vi là `label_contract` trong [danh mục kiến trúc](danh_muc_kien_truc_hoc_tap.yml); không chép một từ điển khác vào mỗi gói.

Mỗi đơn vị có một nơi sở hữu cấu trúc trong gói và có thể được gọi từ nhiều nơi. Ôn nền là khu vực hỗ trợ độc lập, không thuộc Bài học/Khởi động; câu xác nhận, đáp án và nơi quay về thuộc tài nguyên Nền. Cây sở hữu không có vòng; các liên kết gọi hỗ trợ/quay về có thể lặp theo nhu cầu. Toàn văn chỉ là chế độ xem. Theo QD_031, Nhật kí là khu vực độc lập ngang cấp Ôn nền, Sửa lỗi và Lời giải; giữ một nguồn chung và đủ 14 trường, không nằm trong Ôn lại.

Một nhiệm vụ nhiều ý là một đơn vị với các ý con; một câu xác nhận độc lập có danh tính riêng, không tự tăng số nhiệm vụ chính. Ví dụ làm mẫu khác với nhiệm vụ tự làm; lời làm mẫu không tự thành một đáp án được đếm lần hai. Một ví dụ có thể có nhiều bước/vùng đọc. Định nghĩa có thể nằm cùng vùng nhưng là những đơn vị khác nhau. Kiểm kê tách số đơn vị khác nhau, số lần bố trí và số nguồn chung sau khử trùng; thiếu phân loại không được ghi là số 0.

Đối sánh gói theo khu vực, chức năng, loại, quan hệ và điều kiện sử dụng, không theo số hộp hay quota nhãn. Nhãn đủ không chứng minh đủ nội dung hoặc đúng toán. Thêm/đổi nghĩa nhãn cần quyết định của chủ trì và ca kiểm; đổi tên giữ khóa/ID và ánh xạ tên cũ. QD_022 tiếp tục cho phép hiệu chỉnh hợp lệ và chỉ kiểm lại phần bị ảnh hưởng.

07 sở hữu tên hiển thị, mục lục và đánh số; quy chuẩn QMD/schema sở hữu hợp đồng kỹ thuật. G01/G02 chưa tự trở thành sản phẩm đã di trú bởi việc danh mục được cập nhật; trạng thái lấy từ 03/hồ sơ gói.

## Quy ước mã để đối chiếu nguồn

| Mã | Vai trò |
|---|---|
| H | Học có hướng dẫn, ví dụ, câu dừng trong Bài học |
| L | Luyện theo chặng |
| K | Kiểm tra độc lập |
| O | Ôn lại sau khoảng trễ |
| S-L / S-K / S-O | Khắc phục theo nguồn phát hiện lỗi, cần kiểm lịch sử gặp nhiệm vụ |
| P | Phối hợp hoặc chuyển giao; ghi rõ tiên quyết và có bắt buộc hay không |
| N | Tài nguyên nền được gọi theo nhu cầu |
| CP | Điểm dừng có tiêu chí và quyết định tiếp theo |

Giữ mã đã tồn tại nếu còn đúng vai trò. Không đổi mọi mã chỉ để phù hợp tên hiển thị; mã trong nguồn và lời gọi thân thiện với người học có thể khác nhau. Các dạng toán khác không bắt buộc có đúng ba tầng sửa cho mọi lỗi; phải đủ đường xác nhận cần thiết và có cách xử lý khi hết câu mới.

## Đối chiếu và tham chiếu

Nguồn dự án và ba nghiên cứu bổ sung được ghi tại [Nguồn và chuyển tiếp](06_nguon_va_chuyen_tiep.md). Các phát biểu về cơ sở khoa học ở Mục 2.9 dẫn tới mục tài liệu tham chiếu trong tệp ấy. [Quy trình nghiệm thu](02_quy_trinh_va_nghiem_thu.md) xác định cách kiểm kiến trúc trong sản phẩm.
## Bổ sung từ vựng QD_025

Gợi mở (`function.guided_thinking`) là chức năng Nhiệm vụ yêu cầu thử suy nghĩ trước lời giải thích của từng mục kiến thức trong Bài học, không phải Tự kiểm tra sau học. Mỗi nhiệm vụ Gợi mở thuộc đúng mục kiến thức mà nó dẫn vào: đặt sau chỉ dẫn thao tác nếu thật sự cần, trước phần giải thích/định nghĩa/ví dụ; phản hồi hoặc cầu nối nằm tại chỗ. Không gom thành mục Gợi mở chung ngang cấp với Khởi động hoặc Bài học. Khởi động thuộc Bài học và giữ chức năng tự kiểm nền riêng. Gợi mở có dãy số liên tục riêng toàn gói, không đặt lại theo mục; phần giảng ngay sau là hướng dẫn, không tạo đáp án trùng hoặc bằng chứng độc lập mới. Nghĩa này bổ sung danh mục QD_023; không thay đường học hiện hành QD_033 hoặc quyền bắt đầu Kiểm tra QD_024. Số nhiệm vụ theo nội dung từng gói, không sao số lượng của gói đối chứng.

### Hiển thị nhãn theo cấp chứa, 17/10/2026

Hiệu chỉnh theo chỉ thị chủ trì: Bài học → MẠCH HỌC CHÍNH; Khởi động → MẠCH HỌC CHÍNH · BÀI HỌC. Đây là quy tắc trình bày ở 07/6.2, không đổi chức năng QD_025, số nhiệm vụ hoặc tạo chuỗi bắt buộc. Metadata giữ loại/chức năng; nhãn nhìn thấy chỉ ngữ cảnh cấp cha và chặng/lượt/nơi phát hiện. G04 và gói dựng mới dùng context_labels: parent-context-v1; nhãn cũ chưa di trú không làm mẫu mới.


### Hiệu chỉnh số và nhãn — NUMBERING-20261018

Mỗi loại hiển thị dùng một dãy số liên tục riêng từ 01 theo thứ tự xuất hiện trong toàn gói; không đặt lại theo mục, chức năng, chặng, lượt hoặc khu vực. Tất cả nhiệm vụ, kể cả tự làm trong Bài học, Khởi động, Luyện tập, Kiểm tra, Ôn lại, Ôn nền và Sửa lỗi, dùng chung dãy Nhiệm vụ. “Tự kiểm tra” đổi thành “Nhiệm vụ”; chức năng nội bộ vẫn giữ để phân biệt vai trò sư phạm. Gợi mở, Ví dụ và Điểm dừng có dãy riêng. Đề và lời giải dùng cùng số, không đếm lại lời giải; ID giữ nguyên. Include dùng chung không chứa số riêng của gói. Dẫn chiếu, bảng, mục lục và liên kết đi–về dùng cùng ánh xạ theo ID. Nhãn hiển thị theo 07/6.2: MẠCH HỌC hoặc HỖ TRỢ ở đầu khu vực; nội dung bên trong thêm đúng tên khu vực bằng dấu “ · ”.


## Bổ sung Sửa lỗi — nút thắt nhận thức (19/10/2026)

Nút thắt nhận thức là chỗ học sinh chưa phân biệt được các đối tượng, điều kiện hoặc quan hệ toán học dẫn đến cách hiểu chưa đúng. Biên soạn để học sinh tự nhận ra và tháo gỡ qua câu hỏi, đối chứng, giải thích và vận dụng; không chủ ý tạo bẫy. Danh mục trong Sửa lỗi cần bao phủ các nút thắt thuộc phạm vi gói theo 07/6.1.7.

Khi đứng lớp, giáo viên có thể lấy các nút thắt làm trục triển khai: nêu tình huống để học sinh bộc lộ cách hiểu, cho các em giải thích và đối chiếu, hình thành kiến thức cần thiết rồi thử vận dụng. Đây là cách tổ chức bài giảng theo mục tiêu và tiên quyết, không thay kiến trúc học liệu hay biến Sửa lỗi thành chặng bắt buộc trước Bài học. Gợi mở vẫn thuộc từng mục Bài học. Nếu dùng trước một nhiệm vụ vốn dành cho tự kiểm tra, ghi nhận nhiệm vụ đã được gặp; không dùng lại nó để xác nhận khả năng tự giải bài mới.
