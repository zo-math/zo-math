# ĐIỂM TỰA

###### Kiến tạo công thức Bayes từ một tình huống y tế

Trong lý thuyết xác suất hiện đại, các khái niệm như _không gian mẫu_, _biến cố_, _xác suất_ hay _xác suất có điều kiện_ thường được trình bày dưới dạng những định nghĩa và công thức đã hoàn chỉnh. Cách tiếp cận này có ưu điểm là chính xác và súc tích. Tuy nhiên, đối với người học lần đầu tiếp cận, việc các thuật ngữ và ký hiệu xuất hiện quá sớm đôi khi khiến cấu trúc suy luận dẫn đến các công thức trở nên khó nhận ra.

Bài luận này lựa chọn một con đường khác. Thay vì bắt đầu từ các thuật ngữ đã có của xác suất học, ta tạm thời _không sử dụng trước những khái niệm ấy_. Mục đích không phải là thay thế hệ thuật ngữ quen thuộc, mà là để quá trình suy luận có thể được theo dõi một cách tự nhiên. Các khái niệm sẽ dần dần hình thành trong quá trình phân tích chính tình huống đang xét, như những công cụ cần thiết để mô tả và tổ chức lập luận.

Xuất phát từ một tình huống sàng lọc y tế đơn giản, ta sẽ lần theo cách các khả năng của tình huống liên hệ với nhau, cách mức tin cậy của các khả năng bị ràng buộc bởi cấu trúc chung của chúng, và cách sự xuất hiện của thông tin mới làm thay đổi điểm tựa của sự đánh giá. Khi cấu trúc này dần hiện ra, công thức Bayes sẽ không xuất hiện như một quy tắc được đưa vào từ bên ngoài. Nó sẽ xuất hiện như hệ quả tự nhiên của chính cấu trúc suy luận đã được hình thành trong quá trình phân tích.

## I. VẤN ĐỀ TRUNG TÂM

### I. 1. Bối cảnh: một quyết định trong y tế cộng đồng

Một thành phố đang triển khai chương trình sàng lọc một bệnh truyền nhiễm.

Theo số liệu dịch tễ hiện tại, khoảng \(1\%\) dân số đang mắc bệnh. Nói cách khác, nếu nhìn vào toàn bộ cộng đồng, cứ khoảng \(100\) người thì có \(1\) người mang bệnh tại thời điểm này.

<!-- Con số này được gọi là _tỷ lệ hiện mắc_: tỷ lệ người trong cộng đồng đang mang bệnh tại một thời điểm. -->

Cơ quan y tế sử dụng một xét nghiệm nhanh đã được kiểm chứng. Nếu một người thật sự mắc bệnh, xét nghiệm cho kết quả _dương tính_ trong khoảng 99% trường hợp. Nghĩa là phần lớn những người mắc bệnh sẽ được xét nghiệm phát hiện.

<!-- Tỷ lệ này được gọi là _độ nhạy_ của xét nghiệm: khả năng phát hiện đúng bệnh khi bệnh thực sự tồn tại. -->

Tuy nhiên, xét nghiệm không hoàn hảo. Ngay cả khi một người không mắc bệnh, xét nghiệm vẫn có thể cho kết quả dương tính trong khoảng $5\%$ trường hợp.

<!-- Đây là _tỷ lệ dương tính giả_: khả năng báo bệnh khi bệnh không tồn tại. -->

Giả sử một người dân đến xét nghiệm và nhận kết quả dương tính. Người ấy hỏi:

_“Vậy khả năng tôi thật sự mắc bệnh là bao nhiêu?”_

Đây không chỉ là thắc mắc cá nhân. Cơ quan y tế cần câu trả lời để quyết định bước tiếp theo: cách ly, làm thêm xét nghiệm, điều trị sớm hay chỉ theo dõi.

_Nếu chỉ nhìn vào con số \(99\%\), nhiều người sẽ nghĩ rằng kết quả dương tính gần như đồng nghĩa với việc mắc bệnh._

Thử đặt tình huống ban đầu vào một cộng đồng gồm \(10\,000\) người. Trong số đó, khoảng \(100\) người thực sự mắc bệnh. Khi làm xét nghiệm, khoảng \(99\) người trong số này sẽ có kết quả dương tính. Nhưng trong \(9 900\) người không mắc bệnh, sẽ có khoảng \(495\) người cũng nhận kết quả dương tính. _Như vậy, trong tổng số \(594\) người có kết quả dương tính, chỉ \(99\) người thực sự mắc bệnh._

###### Cây minh họa cộng đồng \(10\,000\) người

![](figures/figure_1_cong_dong_10000_dan.svg){width=450}

Ta đang đứng trước một bài toán nhận thức.

Ban đầu ta có một thông tin chung về mức độ phổ biến của bệnh trong cộng đồng. Sau đó xuất hiện một thông tin mới: kết quả xét nghiệm dương tính của một cá nhân cụ thể. Từ hai thông tin này, ta cần đưa ra một đánh giá mới: người vừa được xét nghiệm có khả năng mắc bệnh đến mức nào?

Vấn đề không nằm ở từng con số riêng lẻ. _Vấn đề là làm thế nào để kết hợp thông tin ban đầu và thông tin mới thành một đánh giá không tự mâu thuẫn._

### I.2. Điểm tựa: đánh giá thay đổi khi thông tin thay đổi

Mọi đánh giá đều được thực hiện từ một tập thông tin nhất định.

Trước khi có kết quả xét nghiệm, nếu chọn ngẫu nhiên một người trong cộng đồng, _mức tin cậy_ rằng người đó mắc bệnh là khoảng \(1\%\). Con số này phản ánh bức tranh chung của toàn bộ cộng đồng - đây chính là _điểm tựa_ ban đầu để đưa ra đánh giá.

Khi biết rằng một người cụ thể có kết quả dương tính, tập thông tin thay đổi. Thực tại khách quan không đổi: người đó hoặc mắc bệnh, hoặc không mắc bệnh. Nhưng vị trí nhận thức của ta đã thay đổi, vì điểm tựa đánh giá đã đổi thành nhóm những người có kết quả xét nghiệm dương tính.

Câu hỏi lúc này không còn là:

_“Tỷ lệ mắc bệnh trong cộng đồng là bao nhiêu?”_,

mà là:

_"Trong số những người có kết quả dương tính, khả năng người này thực sự mắc bệnh là bao nhiêu?"_

Vì thế, con số \(1\%\) ban đầu không thể giữ nguyên. Nhưng nó cũng không thể bị bỏ đi. Nó phản ánh bối cảnh chung của cộng đồng. Nếu bỏ nó đi, ta sẽ phóng đại vai trò của xét nghiệm. Nếu giữ nguyên nó, ta lại bỏ qua thông tin mới.

Điều cần làm không phải là thay một con số bằng một con số khác, mà là chuyển điểm tựa của đánh giá. _“Điểm tựa” của một đánh giá là miền khả năng được lấy làm nền chuẩn hóa cho mức tin cậy._

Trong ví dụ \(10\,000\) người ở mục trước:

- nếu điểm tựa là toàn bộ cộng đồng, _mức tin cậy_ rằng một người mắc bệnh là

$$
  \frac{100}{10 000}=1\%;
$$

- nếu điểm tựa chuyển sang nhóm dương tính, mức tin cậy rằng người đó mắc bệnh là

$$
\frac{99}{594}\approx 16.7\%.
$$

Không có mâu thuẫn giữa \(1\%\) và \(16.7\%\). Chúng là hai đánh giá dựa trên hai điểm tựa khác nhau.

Lưu ý, \(10\,000\) người là một trường hợp cụ thể, nơi mọi con số đều được trải ra thành một bảng đếm để quan sát trực tiếp. Khi đó, mức tin cậy mới có thể được tính ngay bằng một tỉ số đơn giản.

###### Bảng minh họa bằng \(10\,000\) người

|                    | Bệnh $B$ | Không bệnh $\neg B$ | Tổng         |
| ------------------ | -------- | ------------------- | ------------ |
| Dương tính \(D\)   | \(99\)   | \(495\)             | \(594\)      |
| Âm tính \(\neg D\) | \(1\)    | \(9\, 405\)         | \(9\, 406\)  |
| **Tổng**           | \(100\)  | \(9\, 900\)         | \(10\, 000\) |

Trong thực tế, ta hiếm khi có sẵn một bảng như vậy. Thông thường, ta chỉ biết những dữ kiện rời rạc: mức độ phổ biến của bệnh trong cộng đồng, khả năng xét nghiệm phát hiện đúng bệnh, và khả năng xét nghiệm báo dương tính ở người không mắc bệnh. Từ những dữ kiện ấy, ta vẫn cần đi đến một đánh giá mới cho trường hợp đang xét.

Vì vậy, điều cần tìm không chỉ là một phép tính cho \(10\,000\) người. Điều cần tìm là một nguyên tắc tổng quát cho phép điều chỉnh mức tin cậy khi thông tin thay đổi, sao cho các dữ kiện ban đầu và thông tin mới vẫn gắn kết với nhau trong cùng một cấu trúc.

Nhưng trọng tâm ghi nhớ không phải là những công thức tìm được, mà là: _khi có thêm thông tin, ta phải thay đổi điểm tựa và tiến hành đánh giá lại theo một nguyên tắc đủ chặt chẽ để mức tin cậy mới không tách rời các dữ kiện đã có_.

### I.3. Ghi lại các đánh giá bằng ký hiệu

Ở hai mục trước, ta đã đi đến một nhận định cốt lõi: khi thông tin thay đổi, đánh giá phải thay đổi theo. Tuy nhiên, sự thay đổi ấy không thể chỉ dựa vào trực giác. Nếu không có một cách trình bày đủ rõ ràng để tổ chức các dữ kiện, mỗi lần xuất hiện thông tin mới ta sẽ dễ điều chỉnh theo cảm tính, và các kết luận sẽ khó giữ được sự nhất quán.

Trong tình huống đang xét, có ít nhất ba loại thông tin cùng tồn tại:

- \(1\%\): mức độ phổ biến của bệnh trong cộng đồng;
- \(99\%\): trong số những người thực sự mắc bệnh, xét nghiệm cho kết quả dương tính trong khoảng \(99\%\) trường hợp;
- \(5\%\): trong số những người không mắc bệnh, xét nghiệm vẫn có thể cho kết quả dương tính trong khoảng \(5\%\) trường hợp.

Ba con số này không nói về cùng một nhóm người. Con số \(1\%\) nói về toàn bộ cộng đồng. Con số \(99\%\) nói về nhóm những người mắc bệnh. Con số \(5\%\) nói về nhóm những người không mắc bệnh. Nếu không phân biệt rõ đang xét trong nhóm nào, ta rất dễ trộn lẫn những đánh giá vốn thuộc về những điều kiện khác nhau.

Để tránh sự nhập nhằng ấy, ta cần một cách ghi lại các đánh giá một cách ngắn gọn và chính xác hơn.

Ta sẽ dùng các chữ cái để biểu thị những mệnh đề mà ta quan tâm. Chẳng hạn:

- \(B\): “mắc bệnh”;
- \(D\): “xét nghiệm cho kết quả dương tính”.

Ta ký hiệu mức tin cậy gắn cho mệnh đề \(X\) bằng \(P(X)\). Nếu mức tin cậy của \(X\) được đánh giá khi mệnh đề \(Y\) là điều kiện ràng buộc, ta viết \(P(X \mid Y)\). Dấu “\(\mid\)” được đọc là “với điều kiện”.

Áp dụng ký hiệu này, các thông tin ban đầu có thể được viết lại gọn gàng như sau:

$$
\begin{aligned}
P(B)&=0.01,\\
P(D\mid B)&=0.99,\\
P(D\mid \neg B)&=0.05.\\
\end{aligned}
$$

Trong đó $\neg B$ biểu thị mệnh đề “không mắc bệnh”.

Câu hỏi của người vừa nhận kết quả xét nghiệm: dương tính thì mắc bệnh với mức tin cậy bao nhiêu? Nghĩa là cần tìm giá trị:

\[
P(B \mid D).
\]

Trong ví dụ \(10\,000\) người, giá trị này chính là tỉ số

\[
\frac{99}{594}.
\]

Phép tính này có được nhờ một bước trung gian: ta tưởng tượng ra một cộng đồng đủ lớn để mọi tỉ lệ đã cho có thể chuyển thành các con số cụ thể, rồi dùng phép đếm để tìm ra kết quả.

Cách làm ấy rất trực quan. Tuy nhiên, nó vẫn chỉ là một _minh họa_. Quy mô \(10\,000\) người không có ý nghĩa đặc biệt. Nếu chọn \(100\,000\) người hay \(1\,000\,000\) người, mọi con số trong bảng sẽ thay đổi, nhưng tỉ số cuối cùng vẫn giữ nguyên.

Điều này cho thấy bảng đếm chỉ là một minh họa cụ thể của một quan hệ tổng quát giữa các tỉ lệ đã cho. Vì vậy điều ta cần tìm không phải là một bảng đếm khác, mà là quy tắc tổng quát chi phối mối quan hệ ấy.

Khi quy tắc này được phát biểu trực tiếp bằng ký hiệu, ta có thể tính toán trong mọi tình huống mà không cần dựng lại một cộng đồng giả định. Quan trọng hơn, quy tắc ấy làm lộ rõ cấu trúc của việc điều chỉnh đánh giá khi thông tin mới xuất hiện.

Trong thực tế, ta hiếm khi biết quy mô một cộng đồng để trải mọi khả năng ra thành bảng đếm. Thông thường, ta chỉ biết các tỉ lệ như

\[
P(B),\quad
P(D\mid B),\quad
P(D\mid \neg B),
\]

tương đối nhờ nhiều lần quan sát và từ đó cần suy ra mức tin cậy mới \(P(B\mid D)\). Vì vậy, ta cần tìm _một quy tắc tổng quát_ cho phép chuyển từ các dữ kiện ban đầu sang mức tin cậy mới khi thông tin thay đổi.

Một điểm đáng chú ý là chính việc đưa vào ký hiệu đã làm cho vấn đề trở nên rõ ràng hơn. Trong ngôn ngữ tự nhiên, câu hỏi ban đầu được diễn đạt như:

_“Nếu xét nghiệm dương tính thì khả năng thật sự mắc bệnh là bao nhiêu?”_

Nhưng khi viết lại bằng ký hiệu, câu hỏi ấy trở thành

\[
P(B\mid D)?
\]

Trong khi các dữ kiện đã biết là

\[
P(B),\quad P(D\mid B),\quad P(D\mid \neg B).
\]

Nhờ cách ghi này, cấu trúc của bài toán hiện ra rất rõ: ta đang tìm một mối liên hệ giữa một mức tin cậy có điều kiện và ba mức tin cậy khác đã biết.

Ở đây, ký hiệu không phải để thay thế suy nghĩ bằng công thức. Ngược lại, khi được dùng đúng chỗ, ký hiệu giúp ta _nhìn thấy chính xác cái cần tìm và những dữ kiện đang ràng buộc nó_. Nó đóng vai trò như một bản đồ gọn gàng của lập luận.

Vấn đề còn lại là: _từ các dữ kiện \(P(B)\), \(P(D\mid B)\) và \(P(D\mid \neg B)\), làm thế nào để suy ra giá trị của \(P(B\mid D)\) mà không cần dựng lại một bảng đếm cụ thể?_

Để trả lời câu hỏi này, ta cần quan sát kỹ hơn cấu trúc của các khả năng trong tình huống đang xét.

> **Bài tập khám phá: Từ bảng đếm đến quy tắc tổng quát.**

### I.4. Đặt các khả năng vào một cấu trúc chung

Để xử lý tình huống một cách nhất quán, cần một cách trình bày trong đó tất cả các khả năng có thể xuất hiện trong tình huống được đặt cạnh nhau và đo trong cùng một chuẩn.

Bối cảnh ban đầu chỉ cung cấp các tỷ lệ: khoảng \(1\%\) dân số mắc bệnh; nếu mắc bệnh thì xét nghiệm dương tính trong \(99\%\) trường hợp; nếu không mắc bệnh thì vẫn có \(5\%\) trường hợp dương tính. Các tỷ lệ này nói về những nhóm khác nhau, nên nếu không có một bức tranh chung, chúng rất dễ bị đọc rời rạc.

Vì vậy, ta tạm hình dung bằng một cộng đồng \(10\,000\) người. Con số \(10\,000\) chỉ giúp làm rõ cấu trúc của tình huống; điều đáng giữ lại không phải là quy mô này, mà là _quan hệ tỷ lệ giữa các phần_.

###### Bảng minh họa bằng \(10\,000\) người

|                    | Bệnh $B$ | Không bệnh $\neg B$ | Tổng         |
| ------------------ | -------- | ------------------- | ------------ |
| Dương tính \(D\)   | \(99\)   | \(495\)             | \(594\)      |
| Âm tính \(\neg D\) | \(1\)    | \(9\, 405\)         | \(9\, 406\)  |
| **Tổng**           | \(100\)  | \(9\, 900\)         | \(10\, 000\) |

Bảng này không chỉ là một phép đếm. Nó đặt tất cả các khả năng của tình huống cạnh nhau: một người có thể mắc bệnh hoặc không mắc bệnh; đồng thời xét nghiệm có thể cho kết quả dương tính hoặc âm tính. Mỗi ô của bảng tương ứng với một trường hợp cụ thể trong sự kết hợp đó.

Tuy nhiên, con số \(10\,000\) không mang ý nghĩa bản chất. Nếu thay bằng \(100\, 000\) hay \(1\, 000\, 000\) người, cấu trúc của bảng vẫn giữ nguyên; chỉ có quy mô thay đổi. _Điều cốt lõi không nằm ở số lượng tuyệt đối, mà ở quan hệ tỷ lệ giữa các phần._

Để quay trở lại ngôn ngữ tỷ lệ - tức là không còn phụ thuộc vào quy mô \(10\, 000\) người - ta chia tất cả các con số trong bảng cho \(10\, 000\). Khi đó, mỗi ô biểu thị phần tương ứng của toàn bộ tình huống.

###### Bảng cấu trúc tỷ lệ của tình huống

|          | $B$        | $\neg B$   | Tổng       |
| -------- | ---------- | ---------- | ---------- |
| $D$      | \(0.0099\) | \(0.0495\) | \(0.0594\) |
| $\neg D$ | \(0.0001\) | \(0.9405\) | \(0.9406\) |
| **Tổng** | \(0.01\)   | \(0.99\)   | \(1\)      |

Trong bảng tỷ lệ này, mỗi ô không còn biểu thị số người cụ thể, mà biểu thị từng phần của tình huống khi lấy toàn bộ làm chuẩn. Tổng của bốn ô đúng bằng \(1\), vì chúng bao phủ toàn bộ những gì có thể xảy ra theo cách ta đã mô tả.

Nói cách khác, ta đã đưa các khả năng của tình huống về cùng một hệ đo chung.

Chính từ “bức tranh tỷ lệ” thống nhất này, việc chuyển điểm tựa của đánh giá - từ toàn bộ cộng đồng sang nhóm những người có kết quả dương tính - sẽ có thể được diễn đạt bằng một quy tắc rõ ràng ở phần sau.

### I. 5. Luận đề trung tâm

Từ bối cảnh ban đầu và các bảng đã xây dựng, một cấu trúc đã lộ rõ.

Ta đang làm việc trong một bức tranh thống nhất của các khả năng, trong đó toàn bộ tình huống được biểu diễn bằng các tỷ lệ và tổng của chúng bằng \(1\). Mỗi phần của bức tranh ấy mang một giá trị xác định, không phải do cảm tính, mà do quan hệ tỷ lệ giữa các phần của tình huống.

Khi xuất hiện thông tin mới - trong trường hợp này là xét nghiệm dương tính \(D\) - ta không tạo ra một tình huống khác, cũng không làm thay đổi thực tại khách quan. Người được xét nghiệm hoặc thuộc \(B\), hoặc thuộc \(\neg B\); điều đó không đổi.

Điều thay đổi là điểm tựa của đánh giá.

Trước khi biết kết quả xét nghiệm, mức tin cậy đối với \(B\) được tính trên toàn bộ bức tranh của tình huống. Sau khi biết rằng \(D\) đã xảy ra, việc đánh giá phải được thực hiện chỉ trong phần của bức tranh tương thích với thông tin đó. Khi đó, toàn bộ bức tranh không còn là điểm tựa; miền \(D\) trở thành điểm tựa mới. Ta chỉ giữ lại những phần của bức tranh tương thích với \(D\), rồi chuẩn hóa lại các phần ấy sao cho tổng của chúng trong miền \(D\) bằng \(1\).

Như vậy, khi thông tin thay đổi, việc điều chỉnh đánh giá không phải là thay thế một con số bằng một con số khác. Điều xảy ra là ta giới hạn sự đánh giá vào phần của bức tranh phù hợp với thông tin mới, rồi chuẩn hóa lại các mức tin cậy trong phần ấy.

Luận đề trung tâm có thể phát biểu như sau:

_"Khi thông tin mới xuất hiện, ta không thay đổi bức tranh khả năng; ta chỉ đổi điểm tựa của đánh giá bằng cách giới hạn vào miền phù hợp với thông tin đó và chuẩn hóa lại các mức tin cậy trên miền ấy."_

Nếu nắm được cấu trúc này, câu hỏi y tế ban đầu chỉ còn là một trường hợp cụ thể của một nguyên tắc tổng quát.

## II. MỘT CẤU TRÚC CHUẨN HÓA CHO CÁC MỨC TIN CẬY

Từ bối cảnh y tế cộng đồng, ta đã thấy rằng các dữ kiện không tồn tại riêng lẻ: mức độ phổ biến của bệnh, khả năng xét nghiệm phát hiện bệnh, khả năng dương tính ở người không mắc bệnh, và câu hỏi về một cá nhân đều thuộc về cùng một tình huống.

Để các dữ kiện ấy liên kết với nhau mà không mâu thuẫn, ta cần một cách tổ chức các mức tin cậy trong toàn bộ tình huống, sao cho mọi con số đều được hiểu trên cùng một chuẩn.

Một cấu trúc như vậy phải trả lời hai câu hỏi cơ bản:

1. những khả năng nào được xem là có thể xảy ra trong tình huống;
2. các mức tin cậy được gán cho những khả năng ấy theo nguyên tắc chuẩn hóa nào.

Khi hai tầng này đã được xác định, việc giới hạn vào miền phù hợp với thông tin mới - như đã mô tả ở phần trước - sẽ trở thành một bước hoàn toàn tự nhiên.

Chính cấu trúc này, trong ngôn ngữ toán học, được gọi là _xác suất_.

### II.1. Xác định các khả năng của tình huống

Trong phần trước, ta đã biểu diễn tình huống bằng một bảng tỷ lệ. Nhưng trước khi có bảng ấy, một bước cơ bản hơn đã xảy ra: ta đã xác định những khả năng nào được xem là có thể xảy ra trong tình huống.

Khi chọn một cá nhân trong chương trình sàng lọc và quan sát hai yếu tố - tình trạng bệnh và kết quả xét nghiệm - thì mỗi yếu tố chỉ có hai khả năng. Người đó hoặc mắc bệnh \(B\) hoặc không mắc bệnh \(\neg B\). Đồng thời, xét nghiệm hoặc cho kết quả dương tính \(D\) hoặc âm tính \(\neg D\).

Từ hai yếu tố nhị phân này, toàn bộ tình huống được cấu thành bởi bốn khả năng kết hợp.

Ta dùng ký hiệu \(X \cap Y\) để chỉ trường hợp hai điều kiện \(X\) và \(Y\) cùng xảy ra. Khi đó bốn khả năng của tình huống là

\[
B \cap D,\quad B \cap \neg D,\quad \neg B \cap D,\quad \neg B \cap \neg D.
\]

Mỗi khả năng mô tả một trạng thái hoàn chỉnh của sự việc: một người có thể mắc bệnh hoặc không mắc bệnh, đồng thời xét nghiệm có thể dương tính hoặc âm tính. Bốn khả năng này loại trừ lẫn nhau và khi gộp lại thì bao phủ toàn bộ những gì có thể xảy ra trong cách ta đã xác định tình huống.

Ta ký hiệu toàn bộ bức tranh các khả năng của tình huống là

\[\Omega.\]

Ký hiệu này không thêm nội dung mới; nó chỉ đặt tên cho bức tranh chung trong đó mọi khả năng của tình huống được đặt cạnh nhau. Trong bức tranh ấy, bốn phần

\[
B \cap D,\quad B \cap \neg D,\quad \neg B \cap D,\quad \neg B \cap \neg D
\]

chính là bốn phần rời nhau tạo nên toàn bộ \(\Omega\).

Điều quan trọng không nằm ở ký hiệu, mà ở việc xác định rõ cách mô tả tình huống.

Nếu ta thay đổi cách mô tả - chẳng hạn ngoài kết quả của xét nghiệm đang xét, ta còn quan sát thêm một lần xét nghiệm thứ hai - thì các khả năng của tình huống cũng phải được mở rộng để phản ánh điều đó. Khi ấy, mỗi người không chỉ có hai thông tin - tình trạng bệnh và kết quả xét nghiệm - mà có ba thông tin: tình trạng bệnh, kết quả xét nghiệm thứ nhất và kết quả xét nghiệm thứ hai. Bức tranh các khả năng vì thế sẽ có nhiều phần hơn và trở thành một bức tranh khác.

Ngược lại, nếu ta giữ nguyên cách xác định tình huống: “chọn một cá nhân và quan sát tình trạng bệnh cùng kết quả xét nghiệm”, thì bức tranh các khả năng vẫn gồm bốn phần đã nêu ở trên. Khi ta biết thêm thông tin - chẳng hạn biết rằng xét nghiệm của người này cho kết quả dương tính - thì điều đó không tạo ra khả năng mới. Bức tranh các khả năng vẫn như cũ.

Điều thay đổi chỉ là: sự đánh giá không còn dựa trên toàn bộ bức tranh nữa, mà được giới hạn vào phần của bức tranh phù hợp với thông tin mới. Trong ví dụ này, nếu biết rằng xét nghiệm dương tính \(D\), thì chỉ còn hai phần của bức tranh phù hợp với thông tin đó:

\[
B \cap D \quad \text{và} \quad \neg B \cap D.
\]

Hai phần còn lại không còn được xét đến trong việc đánh giá.

Chính bức tranh các khả năng này là nền tảng của toàn bộ cấu trúc. Các con số xuất hiện sau đó - dù là \(1\%\), \(99\%\) hay bất kỳ giá trị nào - chỉ có ý nghĩa khi được gắn vào những phần của bức tranh ấy. Khi thông tin mới xuất hiện, việc điều chỉnh đánh giá sẽ được thực hiện bằng cách giới hạn bức tranh vào phần phù hợp với thông tin đó và chuẩn hóa lại các mức tin cậy trong phần ấy.

### II.2. Mức tin cậy và nguyên tắc chuẩn hóa

Khi bức tranh các khả năng \(\Omega\) của tình huống đã được xác định, ta đã có khung cấu trúc để mô tả những gì có thể xảy ra. Nhưng một bức tranh chỉ liệt kê các khả năng vẫn chưa đủ để suy luận. Ta còn phải xác định mỗi phần của bức tranh ấy chiếm bao nhiêu trong toàn bộ.

Trong bối cảnh y tế đang xét, khi nói rằng khoảng \(1\%\) dân số mắc bệnh, ta đang gán một mức tin cậy cho phần \(B\) của bức tranh các khả năng. Khi nói rằng trong số những người mắc bệnh có \(99\%\) cho kết quả dương tính, ta đang nói về mối liên hệ giữa phần \(B\) và phần giao \(B\cap D\) của bức tranh.

Những phát biểu như vậy đòi hỏi một cách gán mức tin cậy chung, sao cho các con số không đứng rời rạc mà được đặt trong cùng một hệ đo lường. Ta ký hiệu cách gán mức tin cậy đó bằng một ký hiệu chung \(P\). Với mỗi phần \(A\) của bức tranh \(\Omega\), giá trị \(P(A)\) biểu thị phần mà \(A\) chiếm trong toàn bộ bức tranh ấy.

Vì \(P(A)\) đo phần của \(A\) trong toàn bộ bức tranh, nên giá trị này luôn nằm giữa \(0\) và \(1\):

\[
0 \le P(A) \le 1,
\]

và toàn bộ bức tranh có mức tin cậy

\[
P(\Omega) = 1.
\]

Điều này không phải là một quy ước tùy ý. Nó chỉ phản ánh việc _lấy toàn bộ bức tranh các khả năng làm đơn vị chuẩn hóa_.

Một hệ quả quan trọng khác xuất phát từ chính cách bức tranh được chia thành các phần. Nếu hai phần của bức tranh không chồng lấn, thì khi gộp chúng lại, mức tin cậy của phần gộp phải bằng tổng mức tin cậy của từng phần.

Trong tình huống đang xét, phần \(B\) được tách thành hai phần rời nhau: \(B \cap D\) và \(B \cap \neg D\). Vì vậy

\[
P(B) = P(B \cap D) + P(B \cap \neg D).
\]

Tương tự, phần \(D\) của bức tranh cũng được tách thành hai phần rời nhau: \(B\cap D\) và \(\neg B\cap D\). Vì vậy

\[
P(D) = P(B \cap D) + P(\neg B \cap D).
\]

Quan hệ này không phải một công thức riêng lẻ, mà phản ánh một nguyên tắc cấu trúc: khi một phần của bức tranh được chia thành các phần rời nhau, mức tin cậy của toàn bộ bằng tổng mức tin cậy của các phần.

Khi một cách gán mức tin cậy thỏa các yêu cầu trên - không âm, tổng bằng \(1\), và cộng được trên các phần rời nhau - ta nói rằng ta đã xây dựng một _cấu trúc xác suất_ trên \(\Omega\).

Chuẩn hóa vì thế không phải là thao tác kỹ thuật phụ trợ. Nó bảo đảm rằng mọi mức tin cậy đều được hiểu trong cùng một hệ quy chiếu. Con số \(1\%\) không có ý nghĩa tự thân; nó chỉ có nghĩa trong quan hệ với toàn bộ bức tranh đã được chuẩn hóa thành \(1\).

Đến đây, ta đã có một hệ đo lường nhất quán cho các phần của bức tranh các khả năng. Điều còn lại là hiểu cách các phần của bức tranh ràng buộc lẫn nhau thông qua các _phần giao_ - tức là những phần nơi hai điều kiện xảy ra đồng thời, như \(B \cap D\). Chính tại đó, cơ chế điều chỉnh mức tin cậy khi thông tin thay đổi sẽ dần lộ rõ.

### II.3. Phần giao và sự ràng buộc giữa các mức tin cậy

Khi các mức tin cậy đã được gán cho các phần của bức tranh các khả năng \(\Omega\), các giá trị ấy không còn tồn tại độc lập. Chính cấu trúc của bức tranh tạo ra những ràng buộc nội tại giữa chúng.

Xét hai phần \(B\) và \(D\). Phần \(B\) biểu thị những trường hợp trong đó người được xét mắc bệnh; phần \(D\) biểu thị những trường hợp trong đó xét nghiệm cho kết quả dương tính. Hai phần này có thể chồng lấn. Phần chồng lấn ấy là

\[
B \cap D,
\]

tức là những trường hợp vừa mắc bệnh vừa có kết quả dương tính.

Vì \(B \cap D\) nằm trong \(B\), nên

\[
P(B \cap D) \le P(B).
\]

Tương tự, vì nó cũng nằm trong \(D\), nên

\[
P(B \cap D) \le P(D).
\]

Những bất đẳng thức này chỉ phản ánh quan hệ _bộ phận - toàn bộ_ trong cấu trúc của bức tranh các khả năng.

Sự ràng buộc trở nên cụ thể hơn khi ta đưa vào các thông tin của bối cảnh.

Phát biểu “trong số những người mắc bệnh, khoảng \(99\%\) cho kết quả dương tính” có nghĩa là: nếu chỉ xét trong \(B\), thì phần \(B\cap D\) chiếm \(99\%\) của toàn bộ phần đó. Vì \(P(A)\) biểu thị kích thước chuẩn hóa của phần \(A\), nên điều này có thể viết lại dưới dạng

\[
P(B \cap D) = 0.99 \cdot P(B).
\]

Tương tự, thông tin “trong số những người không mắc bệnh, khoảng \(5\%\) vẫn cho kết quả dương tính” có nghĩa là

\[
P(\neg B \cap D) = 0.05 \cdot P(\neg B).
\]

Như vậy, một khi \(P(B)\) và các tỷ lệ của bối cảnh đã được chấp nhận, kích thước của các phần giao không còn là những giá trị tùy chọn; chúng được xác định bởi cấu trúc của bức tranh các khả năng. Ví dụ, nếu \(P(B)=0.01\), thì

\[
P(B\cap D)=0.99\times0.01=0.0099.
\]

Đến đây, một câu hỏi tự nhiên xuất hiện.

Cho đến giờ, mọi mức tin cậy đều được đo trên toàn bộ bức tranh \(\Omega\). Nhưng khi một thông tin mới xuất hiện - chẳng hạn ta biết rằng xét nghiệm đã cho kết quả dương tính - thì sự đánh giá không còn diễn ra trên toàn bộ bức tranh nữa, mà chỉ trong phần \(D\).

Khi đó, mức tin cậy của phần \(B\cap D\) trong miền \(D\) phải được xác định ra sao?

Chính câu hỏi này sẽ dẫn đến quy tắc tái chuẩn hóa mức tin cậy khi điểm tựa của đánh giá thay đổi.

Điều đáng chú ý là: cùng một phần \(B\cap D\) có thể được quan sát từ hai phía khác nhau. Nó có thể được xem như một phần của \(B\), nhưng cũng có thể được xem như một phần của \(D\). Vì vậy, các mức tin cậy mới của \(B\cap D\) tương ứng trong \(B\) và \(D\) không thể độc lập; chúng phải phù hợp với nhau trong cùng một hệ chuẩn hóa.

### II.4. Thay đổi chuẩn hóa khi điểm tựa thay đổi

Trong cấu trúc ban đầu, mọi mức tin cậy đều được đo so với toàn bộ bức tranh khả năng \(\Omega\). Vì vậy, giá trị \(P(A)\) cho biết phần mà \(A\) chiếm trong toàn bộ bức tranh này.

Trong tình huống sàng lọc, phần \(D\) của bức tranh bao gồm tất cả những trường hợp cho kết quả xét nghiệm dương tính. Bên trong \(D\) chỉ có hai khả năng: \(B\cap D\) (mắc bệnh và dương tính) và \(\neg B\cap D\) (không mắc bệnh nhưng dương tính). Hai khả năng này loại trừ nhau và khi gộp lại thì đúng bằng toàn bộ \(D\).

Trong hệ đo ban đầu, các giá trị \(P(B\cap D)\) và \(P(\neg B\cap D)\) cho biết kích thước của hai phần này so với toàn bộ \(\Omega\). Tổng của chúng bằng \(P(D)\), nghĩa \(D\) chỉ chiếm một phần của bức tranh ban đầu.

Khi thông tin mới xuất hiện - cụ thể là khi ta biết rằng xét nghiệm cho kết quả dương tính - sự đánh giá không còn liên quan đến toàn bộ \(\Omega\), mà chỉ còn liên quan đến những trường hợp nằm trong \(D\). Nói cách khác, \(D\) trở thành toàn bộ những gì còn có thể xảy ra theo thông tin hiện có.

Nếu ta tiếp tục diễn đạt mức tin cậy trong bối cảnh mới, hai khả năng \(B\cap D\) và \(\neg B\cap D\) phải được đo như những phần của chính miền \(D\). Khi đó, tổng mức tin cậy của chúng phải bằng \(1\) trên \(D\), vì chúng đã bao phủ toàn bộ nó.

Nhưng các giá trị ban đầu \(P(B\cap D)\) và \(P(\neg B\cap D)\) lại được đo so với \(\Omega\), nên tổng của chúng chỉ bằng \(P(D)\). _Vì vậy cần chuyển đơn vị chuẩn hóa của phép đo: từ toàn bộ \(\Omega\) sang miền \(D\)._

Việc chuyển chuẩn này được thực hiện bằng cách so sánh kích thước của từng phần với kích thước của chính miền \(D\). Phần của \(D\) thuộc \(B\) vì thế được xác định bằng tỷ số giữa kích thước của \(B\cap D\) và kích thước của \(D\):

\[
\frac{P(B\cap D)}{P(D)}.  
\]

Tỷ số này biểu thị phần của miền \(D\) thuộc về \(B\). Ta ký hiệu giá trị đó bằng

\[
P(B\mid D)=\frac{P(B\cap D)}{P(D)}, \quad P(D)>0.
\]

Biểu thức này xuất hiện một cách tự nhiên khi ta chuyển chuẩn của phép đo từ toàn bộ \(\Omega\) sang miền \(D\), vì đó là toàn bộ những gì còn có thể xảy ra sau khi thông tin mới được biết.

### II.5. Tên gọi của phép đo mới

Biểu thức

\[
P(B\mid D)=\frac{P(B\cap D)}{P(D)}, \quad P(D)>0.
\]

đo mức tin cậy của \(B\) khi sự đánh giá được thực hiện trong miền \(D\). Trong ngôn ngữ của xác suất học, đại lượng này được gọi là _xác suất có điều kiện_ của \(B\) với điều kiện \(D\).

### II.6. Quay lại câu hỏi y tế ban đầu

Ta quay trở lại câu hỏi đã đặt ra ở đầu bài.

Một người nhận được kết quả xét nghiệm dương tính. Điều cần biết là: _trong số những người có kết quả dương tính, khả năng người này thực sự mắc bệnh là bao nhiêu_.

Theo cấu trúc đã xây dựng, đây chính là mức tin cậy của khả năng \(B\) khi sự đánh giá được thực hiện trong miền \(D\). Giá trị này được xác định bởi

\[
P(B\mid D)=\frac{P(B\cap D)}{P(D)}.
\]

Từ các thông tin của bối cảnh, ta đã có

\[
P(B)=0.01,
\]

\[
P(B\cap D)=0.99\cdot P(B)=0.0099,
\]

\[
P(\neg B\cap D)=0.05\cdot P(\neg B)=0.05\cdot 0.99=0.0495.
\]

Do đó

\[
P(D)=P(B\cap D)+P(\neg B\cap D)=0.0099+0.0495=0.0594.
\]

Vì vậy

\[
P(B\mid D)=\frac{0.0099}{0.0594}\approx 0.167.
\]

Nói cách khác, trong số những người có kết quả xét nghiệm dương tính, khoảng \(16.7\%\) thực sự mắc bệnh.

Trong ví dụ \(10\,000\) người ở phần đầu, ta đã thấy trực tiếp rằng trong \(594\) người có kết quả xét nghiệm dương tính, có \(99\) người thực sự mắc bệnh. Tỷ số

\[
\frac{99}{594}
\]

chính là mức tin cậy rằng một người dương tính thực sự mắc bệnh.

Nhưng phép đếm này chỉ khả thi vì ta đã dựng một bảng minh họa toàn bộ tình huống. Trong thực tế, ta thường không có một bảng như vậy; ta chỉ biết những tỷ lệ rời rạc: mức độ phổ biến của bệnh trong cộng đồng, khả năng xét nghiệm phát hiện đúng bệnh, và khả năng xét nghiệm báo dương tính ở người không mắc bệnh.

Công thức vừa thu được cho phép suy ra đúng tỷ lệ cần tìm chỉ từ những thông tin đó. Nó tái tạo, bằng suy luận, chính kết quả mà bảng \(10\,000\) người cho thấy bằng phép đếm.

Vì vậy, bảng \(10\,000\) người và công thức

\[
\frac{P(B\cap D)}{P(D)}
\]

không phải là hai phương pháp khác nhau. Chúng chỉ là hai cách nhìn của cùng một cấu trúc: một cách nhìn qua các trường hợp cụ thể có thể đếm được, và một cách nhìn qua các mức tin cậy đã được chuẩn hóa.

## III. CẤU TRÚC LIÊN KẾT GIỮA CÁC ĐIỂM TỰA

Đến đây, ta đã thấy rằng khi thông tin thay đổi, mức tin cậy phải được tái chuẩn hóa trên cùng một bức tranh khả năng. Sự thay đổi này có thể được hiểu như sự thay đổi điểm tựa của đánh giá.

Tuy nhiên, một câu hỏi sâu hơn vẫn còn lại: _khi điểm tựa thay đổi, điều gì bảo đảm rằng các đánh giá trước và sau vẫn gắn kết với nhau?_

Nếu mỗi lần xuất hiện thông tin mới ta lại xây dựng một hệ đánh giá hoàn toàn tách biệt, thì việc cập nhật thông tin sẽ chỉ là sự thay thế các con số rời rạc. Khi đó, các đánh giá sẽ không còn được nối với nhau bởi một quá trình suy luận nhất quán.

Điều bảo đảm sự gắn kết ấy chính là việc tất cả các điểm tựa đều được xác định trong cùng một bức tranh khả năng. Các phần của không gian này không tồn tại độc lập: chúng liên hệ với nhau thông qua các phần giao và các quan hệ bộ phận - toàn bộ.

Chính cấu trúc chung của bức tranh khả năng tạo ra những ràng buộc giữa các điểm tựa khác nhau. Nhờ đó, khi điểm tựa thay đổi, các mức tin cậy mới không được đặt ra tùy ý, mà được xác định từ các quan hệ đã tồn tại trong cùng một bức tranh các khả năng.

### III.1. Thu hẹp miền không tạo ra một bức tranh mới

Khi xuất hiện thông tin dương tính, ta chỉ còn xét những khả năng phù hợp với thông tin đó. Điều này có thể tạo cảm giác như ta đã bước sang một bức tranh khác của tình huống.

Thực ra không phải vậy.

Bức tranh khả năng của tình huống đã được xác định bởi bốn khả năng

\[
B\cap D, \quad B\cap \neg D, \quad \neg B\cap D, \quad \neg B \cap \neg D.  
\]

Người được xét nghiệm vẫn chỉ có thể rơi vào một trong bốn khả năng này. Thông tin dương tính không tạo ra khả năng mới nào; nó chỉ loại bỏ những khả năng không phù hợp và giữ lại phần của bức tranh trong đó \(D\) xảy ra.

Vì vậy, ta không thay đổi bức tranh các khả năng đã xác định. Ta chỉ thu hẹp miền xét từ toàn bộ bức tranh xuống phần \(D\) của bức tranh đó.

Chính vì bức tranh nền giữ nguyên, nên các đánh giá trước và sau vẫn gắn kết với nhau. Những mức tin cậy ban đầu không bị thay thế; chúng chỉ được tái chuẩn hóa khi miền xét được thu hẹp từ toàn bộ bức tranh xuống miền \(D\).

Đổi điểm tựa vì thế không phải là đổi thế giới. Đó chỉ là sự thay đổi chuẩn hóa trong cùng một thế giới các khả năng.

### III.2. Phần giao: nơi các điểm tựa gặp nhau

Khi ta nói mắc bệnh và dương tính, ta đang nói về một phần xác định của bức tranh các khả năng đã được thiết lập từ đầu. Phần này được ký hiệu là \(B\cap D\).

Phần giao này không thay đổi khi điểm tựa của đánh giá thay đổi. Trước khi có thông tin mới, nó được nhìn như một phần của toàn bộ bức tranh \(\Omega\). Sau khi biết kết quả dương tính, nó được nhìn như một phần của miền \(D\). Nhưng bản thân nó vẫn là cùng một tập khả năng.

Chính vì phần này giữ nguyên khi điểm tựa thay đổi, nên nó trở thành điểm chung giữa các cách chuẩn hóa khác nhau. Mức tin cậy của \(B\cap D\) có thể được đo theo hai cách: như một phần của toàn bộ bức tranh, hoặc như một phần của miền dương tính.

Hai cách đo ấy không thể mâu thuẫn với nhau. Nếu kích thước của phần giao khi đo trên toàn bộ bức tranh không phù hợp với kích thước của nó khi đo trong miền \(D\), thì hệ thống đánh giá sẽ mất tính nhất quán.

Vì vậy, phần giao chính là nơi các điểm tựa gặp nhau. Nó buộc các cách chuẩn hóa khác nhau phải liên hệ với nhau trong cùng một cấu trúc.

### III.3. Xác suất có điều kiện như hệ quả của sự thay chuẩn

Trong cấu trúc ban đầu, các mức tin cậy được chuẩn hóa trên toàn bộ bức tranh các khả năng \(\Omega\). Mỗi phần của bức tranh được đo so với tổng thể có giá trị \(P(\Omega)=1\).

Khi biết kết quả xét nghiệm dương tính, miền quan sát được thu hẹp lại trên \(D\). Các mức tin cậy khi đó phải được chuẩn hóa lại trên miền này.

Tuy nhiên, phần giao mắc bệnh và dương tính, ký hiệu \(B\cap D\), vẫn là cùng một tập khả năng như trước. Bản thân phần giao này không thay đổi; chỉ cách đo lường nó thay đổi vì tổng thể dùng làm chuẩn đã khác.

Vì vậy, mức tin cậy của khả năng “mắc bệnh trong miền dương tính” phải được xác định bằng cách so sánh kích thước của phần giao \(B\cap D\) với kích thước của toàn bộ miền \(D\). Nếu không thực hiện phép chuẩn hóa này, tổng mức tin cậy trong miền mới sẽ không còn bằng \(1\).

Do đó,

\[
P(B\mid D)=\frac{P(B\cap D)}{P(D)},\quad P(D)>0.
\]

Quan hệ này không phải là một quy ước tùy ý. Nó xuất hiện trực tiếp từ cấu trúc đã xây dựng: cùng một bức tranh các khả năng, cùng một phần giao, và nguyên tắc chuẩn hóa các mức tin cậy trên miền đang xét.

### III.4. Đo cùng một phần giao từ hai điểm tựa

Phần giao \(B\cap D\) là phần chung của hai miền \(B\) và \(D\). Vì vậy nó có thể được nhìn từ hai điểm tựa khác nhau.

Nếu xét trong miền \(B\), phần giao này biểu thị phần của những người mắc bệnh có kết quả dương tính. Nếu xét trong miền \(D\), nó biểu thị phần của những người dương tính thực sự mắc bệnh. Trong cả hai trường hợp, ta vẫn đang nói về cùng một tập khả năng.

Vì vậy, cùng một phần giao có thể được đo theo hai cách chuẩn hóa khác nhau: như một phần của miền \(B\), hoặc như một phần của miền \(D\).

Các phép đo này không thể độc lập với nhau, vì chúng đều mô tả cùng một phần của bức tranh các khả năng. Do đó, các mức tin cậy tương ứng phải liên hệ với nhau trong cùng một cấu trúc.

Chính từ việc đo cùng một phần giao theo hai điểm tựa khác nhau, cấu trúc Bayes sẽ xuất hiện một cách tự nhiên.

### III.5. Ý nghĩa của cấu trúc cập nhật

Cấu trúc vừa phân tích không chỉ nhằm giải thích một công thức. Nó quay trở lại trực tiếp với tình huống y tế ban đầu.

Khi xuất hiện thông tin mới, mức tin cậy phải được điều chỉnh trong cùng một hệ chuẩn hóa. Nếu không nhận ra mối liên hệ giữa các điểm tựa, việc điều chỉnh rất dễ trở nên lệch lạc: hoặc giữ nguyên đánh giá ban đầu như thể chưa có dữ kiện mới, hoặc để dữ kiện mới lấn át hoàn toàn bức tranh ban đầu.

Hiểu quan hệ giữa các điểm tựa giúp tránh hai cực đoan đó. Nó cho phép cập nhật mức tin cậy theo đúng nguyên tắc của mô hình đã thiết lập, và từ đó đưa ra quyết định dựa trên một nền đã được tái chuẩn hóa.

Trong cách nhìn này, xác suất có điều kiện không còn chỉ là một thao tác tính toán. Nó là cơ chế bảo đảm rằng khi điểm tựa của đánh giá thay đổi, mạch suy luận vẫn được giữ liên tục trong cùng một bức tranh các khả năng.

Đến đây, cấu trúc của sự cập nhật đã trở nên rõ ràng: bức tranh các khả năng giữ nguyên, phần giao đóng vai trò cầu nối, và việc tái chuẩn hóa bảo đảm sự liên tục giữa các điểm tựa.

Khi khung liên kết này không được nhận diện đầy đủ, việc điều chỉnh mức tin cậy có thể trở nên tùy tiện. Điều quan trọng không chỉ là thực hiện đúng một phép tính, mà là hiểu điều kiện để suy luận dưới bất định có thể vận hành một cách nhất quán.

## IV. NHẬN DIỆN ĐIỂM TỰA CỦA ĐÁNH GIÁ

Cấu trúc của xác suất có điều kiện cho thấy rằng việc cập nhật mức tin cậy luôn diễn ra trong cùng một bức tranh các khả năng và dưới cùng một nguyên tắc chuẩn hóa. Tuy nhiên, để vận hành đúng cấu trúc ấy, một điều phải được giữ vững: ta phải biết mình đang đánh giá trên nền nào.

Mỗi đánh giá mức tin cậy đều được thực hiện trong một miền được lấy làm chuẩn, tức là miền mà tổng mức tin cậy được xem bằng \(1\). Khi thông tin thay đổi, miền chuẩn này cũng thay đổi theo.

Nếu không nhận ra sự thay đổi đó, các mức tin cậy có thể bị so sánh hoặc kết hợp trong những miền chuẩn khác nhau. Khi ấy, chuỗi suy luận sẽ mất tính nhất quán.

Vì vậy, điều kiện cốt lõi để xác suất có điều kiện vận hành đúng không nằm ở việc ghi nhớ một công thức. Điều quan trọng là nhận diện đúng điểm tựa của mỗi đánh giá. Chỉ khi biết rõ mình đang chuẩn hóa trên miền nào, việc cập nhật mức tin cậy mới có thể diễn ra một cách đúng đắn.

### IV.1. Ba mức tin cậy trong cùng một tình huống

Trong tình huống y tế ban đầu, các con số liên quan đến “mắc bệnh” và “dương tính” không chỉ biểu thị một loại mức tin cậy duy nhất. Chúng tương ứng với những đánh giá được chuẩn hóa trên những miền khác nhau.

Trước hết là mức tin cậy một người bất kỳ trong cộng đồng mắc bệnh. Giá trị này được ký hiệu \(P(B)\) và được chuẩn hóa trên toàn bộ cộng đồng.

Tiếp theo là mức tin cậy xét nghiệm cho kết quả dương tính khi người đó thật sự mắc bệnh. Giá trị này được ký hiệu \(P(D\mid B)\). Trong trường hợp này, miền chuẩn không còn là toàn bộ cộng đồng, mà chỉ là nhóm những người mắc bệnh.

Cuối cùng là mức tin cậy một người thật sự mắc bệnh khi đã biết người đó có kết quả dương tính. Giá trị này được ký hiệu \(P(B\mid D)\), và miền chuẩn lúc này là nhóm những người có kết quả dương tính.

Ba mức tin cậy này cùng xuất hiện trong một tình huống, nhưng chúng được đo trên những miền chuẩn khác nhau. Vì vậy, chúng không thể được đồng nhất hay so sánh trực tiếp với nhau.

Việc phân biệt rõ miền chuẩn của từng mức tin cậy không phải là một thao tác kỹ thuật đơn thuần. Đó là điều kiện để việc cập nhật mức tin cậy diễn ra minh bạch và không lẫn lộn.

### IV.2. Thông tin mới không thay thế nền cũ

Khi xuất hiện thông tin dương tính, đánh giá về khả năng mắc bệnh phải được điều chỉnh. Tuy nhiên, sự điều chỉnh đó không có nghĩa là xóa bỏ đánh giá ban đầu hay thay thế nó bằng một con số hoàn toàn mới.

Đánh giá ban đầu về nguy cơ mắc bệnh trong cộng đồng vẫn giữ vai trò trong cấu trúc chung. Nó tham gia vào việc xác định phần giao giữa mắc bệnh và dương tính, và vì vậy tiếp tục ảnh hưởng đến kết quả sau khi cập nhật.

Thông tin mới làm thay đổi miền chuẩn của việc đánh giá, nhưng không làm mất đi cấu trúc đã được thiết lập trước đó. Mức tin cậy sau khi cập nhật vẫn được xây dựng trên cùng một bức tranh các khả năng và trên cùng những phần giao đã được xác định từ đầu.

Vì vậy, cập nhật không phải là sự thay thế. Cập nhật là sự tái chuẩn hóa mức tin cậy trong cùng một cấu trúc.

Đến đây có thể nói rõ: “điểm tựa” trong toàn bộ chuyên đề này không phải là một hình ảnh ẩn dụ mơ hồ. Nó chính là nền chuẩn hóa của sự đánh giá - tức là miền khả năng mà trên đó tổng mức tin cậy được đặt bằng \(1\).

Khi thông tin thay đổi, nền chuẩn này thay đổi theo. Và việc nhận diện đúng nền ấy là điều kiện để quá trình cập nhật diễn ra một cách hợp lý.

### IV.3. Từ con số đến quyết định

Sau khi tái chuẩn hóa trên nền “dương tính”, ta thu được một mức tin cậy mới cho khả năng mắc bệnh. Con số ấy không còn là một dữ kiện rời rạc; nó là kết quả của toàn bộ quá trình tái chuẩn hóa đã được xây dựng từ đầu.

Chính mức tin cậy này trở thành cơ sở để lựa chọn hành động. Việc có cần xét nghiệm khẳng định, cách ly hay điều trị ngay không thể dựa vào trực giác riêng lẻ, mà phải dựa vào mức tin cậy đã được cập nhật đúng cách.

Xác suất có điều kiện vì thế không chỉ là một phép tính. Nó là cơ chế liên kết thông tin với cấu trúc suy luận, và cấu trúc suy luận với quyết định thực tế. Nhờ cơ chế đó, các con số không đứng rời rạc mà trở thành một hệ thống có thể vận hành.

Cơ chế tái chuẩn hóa cho thấy việc thay đổi điểm tựa có thể được thực hiện một cách nhất quán trong cùng một cấu trúc. Nhưng mối liên hệ ấy không chỉ đi theo một chiều. Nếu có thể đi từ nền chung đến miền thu hẹp, liệu ta cũng có thể đọc cấu trúc theo chiều ngược lại - từ dữ kiện quan sát để suy ra điều ta quan tâm?

Câu hỏi này sẽ dẫn đến hình thức đầy đủ của Bayes, nơi sự liên kết giữa các nền chuẩn hóa trở nên hai chiều một cách minh bạch.

## V. ĐẢO CHIỀU ĐIỂM TỰA VÀ CẤU TRÚC BAYES

Cho đến đây, ta đã đi theo một chiều quen thuộc: từ mức tin cậy ban đầu trong toàn bộ bức tranh các khả năng, khi xuất hiện thông tin “dương tính”, ta thu hẹp miền xét và tái chuẩn hóa để có được mức tin cậy mới cho “mắc bệnh”.

Đó là chiều cập nhật thông tin: từ nền chung sang nền thu hẹp.

Tuy nhiên, cấu trúc giao giữa “mắc bệnh” và “dương tính” cho phép một cách đọc khác. Vì phần giao \(B\cap D\) là chung cho mọi cách chuẩn hóa, nên cùng một phần này có thể được đo từ hai phía: như một phần của miền “mắc bệnh”, hoặc như một phần của miền “dương tính”.

Nhờ vậy, quan hệ giữa các mức tin cậy không chỉ cho phép đi từ nền chung đến nền thu hẹp. Ta cũng có thể đọc cấu trúc theo chiều ngược lại: từ những quan hệ đã biết trong miền “mắc bệnh” để suy ra mức tin cậy trong miền “dương tính”, hoặc ngược lại.

Sự “đảo chiều” này không phải là một thao tác mới. Nó chỉ là cách nhìn khác của cùng một cấu trúc, trong đó cùng một phần giao \(B\cap D\) được đo từ những điểm tựa khác nhau.

Chính từ cách đọc hai chiều này, hình thức đầy đủ của Bayes sẽ xuất hiện.

### V.1. Hai cách nhìn cùng một phần giao

Trong bức tranh các khả năng của tình huống y tế, phần mắc bệnh và dương tính, ký hiệu \(B\cap D\), là một phần của bức tranh đã được xác định từ đầu. Phần này không thay đổi khi ta thay đổi điểm tựa của sự đánh giá.

Tuy nhiên, nó có thể được đo trong những nền chuẩn hóa khác nhau. Nếu xét trong miền mắc bệnh, phần \(B\cap D\) biểu thị tỷ lệ những người mắc bệnh có kết quả dương tính. Nếu xét trong miền dương tính, chính phần đó lại biểu thị tỷ lệ những người dương tính thật sự mắc bệnh.

Hai cách nhìn này không tạo ra hai phần khác nhau của bức tranh. Chúng chỉ là hai cách đo cùng một phần giao trong hai nền chuẩn hóa khác nhau.

Vì phần giao là chung cho cả hai nền, nên cách biểu diễn mức tin cậy của \(B\cap D\) trong miền mắc bệnh phải phù hợp với cách biểu diễn của nó trong miền dương tính. Nói cách khác, cùng một phần giao phải có thể được đo theo hai cách tương thích với hai nền chuẩn hóa.

Chính yêu cầu tương thích này tạo ra mối liên hệ hai chiều giữa các mức tin cậy, và từ đó dẫn đến hình thức của định lý Bayes.

### V.2. Đảo chiều: từ “khi mắc bệnh thì dương tính” đến “khi dương tính thì mắc bệnh”

Trong dữ liệu ban đầu, ta biết mức tin cậy của việc xét nghiệm cho kết quả dương tính khi người đó thật sự mắc bệnh, và biết mức tin cậy nền của việc mắc bệnh trong cộng đồng.

Hai thông tin này cho phép ta xác định kích thước của phần giao mắc bệnh và dương tính. Phần giao ấy có thể được biểu diễn như phần của miền “mắc bệnh” cho kết quả dương tính; nói cách khác, nó bằng mức tin cậy của “mắc bệnh” nhân với mức tin cậy của “dương tính trong miền mắc bệnh”. Khi viết bằng ký hiệu, ta có

\[
P(B\cap D)=P(D\mid B)P(B).
\]

Nhưng cùng một phần giao đó cũng có thể được nhìn từ phía còn lại. Khi xét trong miền dương tính, nó biểu thị phần những người dương tính thật sự mắc bệnh. Vì vậy, nó cũng có thể được biểu diễn như phần của miền dương tính thuộc về mắc bệnh; khi viết bằng ký hiệu,

\[
P(B\cap D)=P(B\mid D)P(D).
\]

Hai biểu thức vừa viết cho thấy cùng một phần của không gian có thể được nhìn từ nhiều điểm tựa khác nhau: như một phần của miền \(B\), hoặc như một phần của miền \(D\). Tuy nhiên bản thân phần của không gian ấy không thay đổi. Vì vậy kích thước của nó khi đo trên không gian chung phải giữ nguyên, bất kể ta đang biểu diễn nó thông qua miền \(B\) hay thông qua miền \(D\). Chính yêu cầu tương thích này buộc hai biểu diễn của phần giao phải bằng nhau.

Từ đó, ta thu được mối liên hệ giữa mức tin cậy của mắc bệnh khi đã biết dương tính và các đại lượng đã biết trước đó:

\[
P(B\mid D)=\frac{P(D\mid B)P(B)}{P(D)}.
\]

Đây chính là công thức quen thuộc mang tên định lý Bayes.

Lưu ý, mẫu số \(P(D)\) không phải là một đại lượng được đưa thêm vào từ bên ngoài. Miền dương tính \(D\) tự nó được cấu thành bởi hai phần rời nhau: phần những trường hợp vừa mắc bệnh vừa dương tính \(B\cap D\), và phần những trường hợp không mắc bệnh nhưng vẫn dương tính \(\neg B\cap D\). Hai phần này loại trừ nhau và khi gộp lại thì đúng bằng toàn bộ miền \(D\). Vì vậy, kích thước của \(D\) bằng tổng kích thước của hai phần cấu thành ấy:

\[
\begin{aligned}
P(D)&=P(B\cap D)+P(\neg B\cap D)\\
&=P(D\mid B)P(B)+P(D\mid \neg B)P(\neg B).
\end{aligned}
\]

Quan hệ này cho biết cách tập hợp lại kích thước của một miền từ các phần rời nhau của nó; trong ngôn ngữ xác suất, đây chính là công thức xác suất toàn phần cho \(D\) trong tình huống đang xét.

Trong ví dụ 10 000 người ở phần đầu, miền dương tính có \(594\) người, nên

\[
P(D)=\frac{594}{10000}=0.0594.
\]

Con số này cũng phù hợp với công thức vừa nêu:

\[
\begin{aligned}
P(D)&=P(D\mid B)P(B)+P(D\mid \neg B)P(\neg B)\\
&=0.99\cdot 0.01+0.05\cdot 0.99\\
&=0.0594.
\end{aligned}
\]

Tuy nhiên, điều cốt lõi không nằm ở công thức. Nó nằm ở việc cùng một phần giao có thể được đọc từ hai điểm tựa khác nhau mà vẫn giữ nguyên cấu trúc. Bayes không phải là một thủ thuật biến đổi ký hiệu; _nó là cách toán học diễn đạt việc nhìn cùng một phần của bức tranh từ hai điểm tựa khác nhau._

### V.3. Vai trò của nền ban đầu

Trong quan hệ hai chiều vừa thiết lập, mức tin cậy ban đầu về việc mắc bệnh, ký hiệu \(P(B)\), không biến mất khi có thông tin mới. Nó tham gia trực tiếp vào việc xác định kích thước của phần giao giữa mắc bệnh và dương tính, và vì vậy ảnh hưởng đến mức tin cậy sau khi cập nhật.

Nếu nguy cơ nền trong cộng đồng rất nhỏ, thì miền “mắc bệnh” cũng rất nhỏ. Khi đó, ngay cả khi xét nghiệm có khả năng phát hiện cao, phần giao \(B\cap D\) vẫn bị giới hạn bởi quy mô của miền này. Ngược lại, khi nguy cơ nền lớn hơn, cùng một đặc tính xét nghiệm sẽ dẫn đến một phần giao lớn hơn, và do đó mức tin cậy sau khi cập nhật cũng cao hơn.

Sự khác biệt này không phải là một sai lệch của suy luận. Nó là hệ quả trực tiếp của cấu trúc chuẩn hóa: kích thước của phần giao phụ thuộc đồng thời vào _mức tin cậy nền_ và _đặc tính của thông tin mới_.

Vì vậy, việc đảo chiều điểm tựa luôn gắn chặt với nền ban đầu. Mọi cập nhật đều diễn ra trong cùng một cấu trúc đã được thiết lập từ trước; không có đánh giá nào xuất hiện độc lập khỏi nền ấy. Trong quan hệ Bayes, mức tin cậy nền \(P(B)\) luôn giữ vai trò thiết yếu trong việc xác định mức tin cậy sau khi quan sát thông tin mới.

### V.4. Bayes như một nguyên lý vận hành

Khi nhìn Bayes từ góc độ điểm tựa, ta thấy rằng bức tranh các khả năng của tình huống không thay đổi. Phần giao giữa các phần của bức tranh ấy vẫn giữ nguyên; điều thay đổi duy nhất là nền chuẩn hóa mà trên đó mức tin cậy được đo lường.

Chính vì phần giao bất biến, nên quan hệ giữa các nền có thể được đọc theo hai chiều. Từ mức tin cậy của quan sát khi giả thuyết đúng, cùng với mức tin cậy nền của giả thuyết, ta có thể suy ra mức tin cậy của giả thuyết khi quan sát đã xảy ra.

Quan hệ này không phải một kỹ thuật tính toán riêng lẻ. Nó là cấu trúc trung tâm của suy luận dưới bất định: mọi cập nhật hợp lý đều dựa trên cùng một bức tranh các khả năng, cùng một phần giao, và sự thay đổi có kiểm soát của nền chuẩn hóa.

Trong bối cảnh y tế cộng đồng, nguyên lý ấy cho phép chuyển từ đặc tính của xét nghiệm sang đánh giá tình trạng bệnh của một cá nhân cụ thể. Từ dữ kiện về cách xét nghiệm phản ứng với bệnh khi bệnh tồn tại, ta suy ra mức tin cậy rằng bệnh thực sự tồn tại khi đã biết kết quả xét nghiệm.

### V.5. Ý nghĩa vượt ra ngoài ví dụ

Trong ví dụ sàng lọc ban đầu, toàn bộ quá trình suy luận dẫn đến kết quả \(P(B\mid D)\approx 16.7\%\). Con số này không phải là kết quả của một phép biến đổi rời rạc, mà là hệ quả tất yếu của cấu trúc chuẩn hóa và của việc đo cùng một phần giao từ hai điểm tựa khác nhau.

Bayes vì thế không chỉ là một công cụ trong chẩn đoán y khoa. Nó là biểu hiện rõ ràng của một nguyên lý rộng hơn: khi thông tin thay đổi, điểm tựa của sự đánh giá thay đổi theo, nhưng sự thay đổi ấy phải được thực hiện trong cùng một cấu trúc bất biến.

Nhờ nguyên lý này, việc cập nhật mức tin cậy không trở thành một hành vi tùy tiện. Mỗi dữ kiện mới được đưa vào hệ thống thông qua phần giao và nguyên tắc chuẩn hóa, bảo đảm rằng toàn bộ suy luận vẫn liên tục và nhất quán.

Đến đây, cấu trúc điểm tựa đã được xác lập đầy đủ trong phạm vi toán học. Từ một ví dụ cụ thể, ta đã đi đến một cơ chế chung cho việc cập nhật dưới bất định.

Vấn đề còn lại không còn thuần túy là toán học. Nó liên quan đến cách con người lựa chọn lập trường và đưa ra quyết định khi phải hành động trong điều kiện thông tin không đầy đủ.

## VI. NGUYÊN LÝ BẤT BIẾN PHẦN GIAO

Qua toàn bộ phân tích trước đó, ta đã đi từ một tình huống cụ thể đến cấu trúc của xác suất có điều kiện và công thức Bayes. Tuy nhiên, điều xuất hiện trong quá trình này không chỉ là một công thức riêng lẻ. Toàn bộ lập luận cho thấy một nguyên lý tổng quát hơn về cách các mức tin cậy liên hệ với nhau trong cùng một bức tranh các khả năng.

Trong cấu trúc đã xây dựng, mỗi mức tin cậy luôn được đo lường trên một nền chuẩn hóa xác định. Khi thông tin thay đổi, nền chuẩn hóa có thể thay đổi theo. Tuy nhiên bức tranh các khả năng và các phần của nó vẫn giữ nguyên.

Đặc biệt, một _phần giao_ của bức tranh có thể được nhìn từ nhiều điểm tựa khác nhau. Nó có thể được đo như một phần của miền này, hoặc như một phần của miền khác. Tuy nhiên bản thân phần giao này của bức tranh ấy không thay đổi. Vì vậy kích thước của nó trong bức tranh chung phải được giữ nguyên, bất kể ta đang chuẩn hóa trên miền nào.

Điều này dẫn đến nguyên lý sau.

**Nguyên lý (bất biến của phần giao).** _Trong cùng một bức tranh khả năng, kích thước của một phần không phụ thuộc vào nền chuẩn hóa được dùng để đo nó._

Áp dụng nguyên lý này cho hai miền \(B\) và \(D\) với \(P(B)>0\) và \(P(D)>0\), phần giao \(B\cap D\) có thể được đo theo hai cách:

- khi chuẩn hóa trên \(B\), kích thước của nó bằng \(P(D\mid B)P(B)\);
- khi chuẩn hóa trên \(D\), kích thước của nó bằng \(P(B\mid D)P(D)\).

Vì cả hai biểu thức đều mô tả cùng một phần của bức tranh các khả năng, chúng phải bằng nhau. Do đó

\[
P(D\mid B)P(B)=P(B\mid D)P(D).
\]

Từ quan hệ này suy ra

\[
P(B\mid D)=\frac{P(D\mid B)P(B)}{P(D)},
\]

chính là công thức Bayes.

Như vậy, định lý Bayes không phải là một công thức rời rạc được đặt ra từ bên ngoài. Nó xuất hiện như hệ quả trực tiếp của một nguyên lý đơn giản hơn: _kích thước của cùng một phần trong bức tranh các khả năng phải bất biến khi thay đổi nền chuẩn hóa_.

Nói ngắn gọn, toàn bộ bài luận này có thể được hiểu như việc làm rõ mệnh đề sau.

**Định lý (Bayes theo cấu trúc).** _Nếu cùng một phần của bức tranh các khả năng được đo theo hai nền chuẩn hóa khác nhau, thì kích thước của phần đó phải giữ nguyên; từ đó suy ra công thức Bayes._

Toàn bộ quá trình phân tích trước đó chính là hành trình dựng cấu trúc để định lý này trở nên hiển nhiên.

## KẾT LUẬN

Từ một tình huống y tế cộng đồng tưởng như đơn giản, ta đã từng bước kiến tạo cấu trúc của xác suất có điều kiện. Cấu trúc ấy bắt đầu từ việc xác định bức tranh các khả năng, chuẩn hóa mức tin cậy trên bức tranh đó, nhận diện phần giao như cầu nối giữa các miền đánh giá, và thực hiện tái chuẩn hóa khi thông tin thay đổi. Trên nền tảng ấy, khả năng đảo chiều điểm tựa trong cấu trúc Bayes xuất hiện như một hệ quả tất yếu.

Luận đề trung tâm vì thế được xác lập: xác suất có điều kiện không chỉ là một công thức, mà là sự thay đổi điểm tựa trong cùng một cấu trúc xác suất. Khi điểm tựa thay đổi, mức tin cậy được phân bố lại, nhưng cấu trúc chung của bức tranh các khả năng vẫn được giữ nguyên.

Nhờ cấu trúc ấy, ta có thể chuyển từ dữ kiện sang đánh giá, từ đánh giá sang quyết định mà không làm đứt gãy suy luận. Trong y tế cộng đồng, điều này bảo đảm rằng hành động được thực hiện trên nền đã được cập nhật đúng cách. Trong phạm vi rộng hơn của tư duy, nó gợi ra một nguyên tắc: thông tin có thể thay đổi, nhưng việc thay đổi điểm tựa phải diễn ra trong một cấu trúc suy luận nhất quán.

Chuẩn hóa trong xác suất có thể được hiểu như việc lựa chọn đơn vị đo. Khi nền chuẩn hóa thay đổi, các phần của bức tranh được đo theo đơn vị mới. _Xác suất có điều kiện chính là hệ số chuyển đổi giữa các chuẩn hóa này._

Thực hiểu xác suất có điều kiện vì thế không chỉ là hiểu một phép tính. Đó là học cách tổ chức thông tin, ý thức điểm tựa của mình, và giữ cho suy luận đứng vững khi phải quyết định trong điều kiện bất định.

---

# CHUẨN HÓA TỪ VỰNG

## Bảng từ vựng sử dụng trong bài

| Thuật ngữ trong bài          | Ý nghĩa trực quan                                                                 | Thuật ngữ xác suất tương ứng           |
| ---------------------------- | --------------------------------------------------------------------------------- | -------------------------------------- |
| **bức tranh khả năng**       | toàn bộ những khả năng có thể xảy ra trong tình huống đang xét                    | không gian mẫu \(\Omega\)              |
| **phần của bức tranh**       | một miền gồm những khả năng cùng thỏa một điều kiện nào đó                        | biến cố                                |
| **phần giao**                | phần chung của hai miền khả năng                                                  | giao của hai biến cố                   |
| **mức tin cậy**              | kích thước chuẩn hóa của một phần trong bức tranh khả năng                        | xác suất                               |
| **nền chuẩn hóa**            | miền được dùng làm chuẩn để đo các mức tin cậy                                    | miền chuẩn hóa của xác suất            |
| **điểm tựa của đánh giá**    | miền đang được dùng làm nền chuẩn hóa                                             | điều kiện                              |
| **tái chuẩn hóa**            | chuyển phép đo mức tin cậy sang một nền chuẩn hóa mới                             | thao tác dẫn đến xác suất có điều kiện |
| **mức tin cậy có điều kiện** | mức tin cậy của một phần khi phép đo được thực hiện trên một nền chuẩn hóa đã cho | xác suất có điều kiện                  |

## Ba ý tưởng trung tâm của bài

Toàn bộ cấu trúc của bài luận có thể tóm tắt bằng ba nguyên tắc:

- **chuẩn hóa** → lựa chọn đơn vị đo
- **phần giao** → đại lượng bất biến trong bức tranh khả năng
- **xác suất có điều kiện** → hệ số chuyển đổi giữa các nền chuẩn hóa

## Ví dụ cách dùng trong văn bản

Sau khi chuẩn hóa thuật ngữ, các câu trong bài sẽ có dạng rất tự nhiên như:

> Ta bắt đầu bằng việc xác định **bức tranh khả năng** của tình huống đang xét.
>
> Mỗi điều kiện xác định một **phần của bức tranh**.
>
> Cho mỗi phần, ta gán một **mức tin cậy**, biểu thị kích thước chuẩn hóa của phần đó trong bức tranh chung.

## Gợi ý nhỏ về tính nhất quán

Trong toàn bài nên giữ quy tắc:

- luôn viết **“bức tranh khả năng”** (không đổi sang “bức tranh các khả năng”)
- luôn viết **“phần”**, không dùng “mảnh”
- luôn dùng **“mức tin cậy”** thay cho “xác suất” cho đến khi công thức Bayes xuất hiện.

Cách này giúp bài giữ đúng tinh thần: _không dùng thuật ngữ xác suất học cho đến khi cấu trúc đã hiện ra._

---

# BA TÌNH HUỐNG DẠY BAYES

Để trả lời câu hỏi này một cách sư phạm, cần nhìn ba ví dụ nổi tiếng dùng để dạy Bayes:

1. _Xét nghiệm y tế_
2. _Bộ lọc thư rác (spam filter)_
3. _Bài toán Monty Hall_

Chúng đều liên quan đến xác suất có điều kiện, nhưng _chúng dạy ba cấu trúc nhận thức khác nhau_. Vì vậy mức độ “lợi hại” của chúng phụ thuộc vào mục tiêu dạy học.

## 1. Ví dụ xét nghiệm y tế

Đây là ví dụ bạn đang dùng trong bài luận.

### Cấu trúc toán học

Ta có ba đại lượng:

\[
P(B),\quad P(D\mid B),\quad P(D\mid \neg B)
\]

và cần suy ra

\[
P(B\mid D).
\]

Đây chính là cấu trúc Bayes điển hình:

\[
P(B\mid D)=\frac{P(D\mid B)P(B)}{P(D)}.
\]

### Điều đặc biệt của ví dụ này

Ở đây tồn tại _một sự xung đột trực giác rất mạnh_:

- xét nghiệm đúng 99%
- nhưng xác suất mắc bệnh sau khi dương tính chỉ khoảng 17%

Điều này buộc người học phải nhận ra vai trò của _base rate_:

\[
P(B)
\]

tức là _tỷ lệ nền của bệnh trong cộng đồng_.

### Giá trị sư phạm

Ví dụ này dạy một điều cực kỳ quan trọng:

> xác suất của một giả thuyết sau khi quan sát không chỉ phụ thuộc vào độ tin cậy của quan sát, mà còn phụ thuộc vào _tần suất nền của giả thuyết_.

Đây là một trong những bài học quan trọng nhất của Bayes.

Trong tâm lý học nhận thức, lỗi bỏ qua base rate được gọi là:

_base rate fallacy._

Ví dụ xét nghiệm y tế là _cách trực quan nhất để nhìn thấy lỗi này_.

## 2. Ví dụ bộ lọc thư rác

Ví dụ này cũng rất nổi tiếng trong dạy Bayes.

Ta có:

- \(S\): email là spam
- \(W\): email chứa từ “viagra”

Ta biết:

\[
P(W\mid S),\quad P(W\mid \neg S),\quad P(S)
\]

và cần tính

\[
P(S\mid W).
\]

### Cấu trúc toán học

Cấu trúc hoàn toàn giống bài xét nghiệm y tế:

\[
P(S\mid W)=\frac{P(W\mid S)P(S)}{P(W)}.
\]

### Điểm mạnh của ví dụ spam

Nó cho thấy _Bayes là một thuật toán học máy thực sự_.

Spam filter hiện đại hoạt động gần đúng theo nguyên lý:

_naive Bayes classifier._

Điều này giúp người học thấy rằng Bayes:

- không chỉ là toán học,
- mà còn là _công nghệ đang vận hành internet_.

### Điểm yếu sư phạm

Ví dụ spam _không tạo ra cú sốc trực giác mạnh_ như xét nghiệm y tế.

Người học thường chấp nhận kết quả dễ dàng hơn.

Nó không làm lộ rõ _base rate fallacy_.

## 3. Ví dụ Monty Hall

Bài toán Monty Hall là một ví dụ rất nổi tiếng:

- 3 cửa
- chọn 1 cửa
- người dẫn chương trình mở một cửa không có giải
- đổi cửa có lợi không?

Kết quả:

\[
P(\text{thắng khi đổi})=\frac{2}{3}.
\]

### Điểm mạnh

Bài toán này tạo ra _cú sốc trực giác rất mạnh_.

Rất nhiều người, kể cả nhà toán học, ban đầu trả lời sai.

Điều này làm cho Monty Hall trở thành một bài toán rất hấp dẫn.

### Nhưng Monty Hall **không phải là Bayes điển hình**

Cấu trúc của Monty Hall không phải là

\[
P(H\mid E).
\]

Nó liên quan nhiều hơn đến:

- _thông tin phụ thuộc vào chiến lược của người dẫn chương trình_
- xác suất có điều kiện trong _quá trình động_

Do đó Monty Hall dạy tốt:

- sự phụ thuộc của thông tin
- vai trò của chiến lược

Nhưng nó _không làm rõ cấu trúc base rate vs likelihood_.

## 4. So sánh ba ví dụ

| Ví dụ           | Cấu trúc Bayes    | Cú sốc trực giác | Giá trị nhận thức   |
| --------------- | ----------------- | ---------------- | ------------------- |
| Xét nghiệm y tế | Rất chuẩn         | Rất mạnh         | Base rate fallacy   |
| Spam filter     | Chuẩn             | Trung bình       | Ứng dụng thực tế    |
| Monty Hall      | Không thuần Bayes | Rất mạnh         | Thông tin phụ thuộc |

## 5. Vì sao ví dụ xét nghiệm y tế gần như “tối ưu”

Ví dụ này có ba đặc điểm hiếm khi cùng xuất hiện:

### 1. Cấu trúc Bayes chuẩn

Nó trực tiếp thể hiện:

\[
P(H\mid E)
\]

### 2. Tạo ra xung đột trực giác

Sự khác biệt giữa:

- 99%
- 17%

làm người học buộc phải thay đổi cách nghĩ.

### 3. Có ý nghĩa thực tế nghiêm túc

Đây không phải trò chơi.

Trong y học, hiểu sai điều này có thể dẫn đến:

- chẩn đoán sai
- điều trị sai.

Vì vậy ví dụ này vừa:

- toán học
- nhận thức
- xã hội.

## 6. Nếu mục tiêu là dạy Bayes thật sâu

Thứ tự tốt nhất thường là:

1️⃣ **xét nghiệm y tế**
→ để thấy base rate

2️⃣ **spam filter**
→ để thấy Bayes như thuật toán học

3️⃣ **Monty Hall**
→ để thấy vai trò của thông tin và chiến lược

## 7. Một nhận xét thú vị

Trong thống kê Bayes hiện đại, cấu trúc của ví dụ y tế chính là:

- **prior**: (P(B))
- **likelihood**: (P(D|B))
- **posterior**: (P(B|D))

Đây là _cấu trúc nền của mọi suy luận Bayes_.

Vì vậy ví dụ y tế thực chất là _mô hình nhỏ nhất của Bayesian inference_.

---

# TẦN SUẤT TỰ NHIÊN

Ví dụ _10 000 người_ mà bạn dùng trong bài luận thực ra trùng với một phát hiện rất nổi tiếng trong tâm lý học nhận thức về xác suất. Khái niệm trung tâm là _natural frequencies_ (tần suất tự nhiên).

## 1. Vấn đề tâm lý học: con người hiểu xác suất rất kém

Trong nhiều thí nghiệm từ thập niên 1970-1990, các nhà nghiên cứu phát hiện một điều đáng chú ý:

Khi người ta được cho các dữ kiện dạng xác suất, ví dụ

- \(P(B)=0.01\)
- \(P(D\mid B)=0.99\)
- \(P(D\mid \neg B)=0.05\)

thì _đa số không suy luận đúng \(P(B\mid D)\)_.

Trong nhiều nghiên cứu, _hơn 80-90% người tham gia trả lời sai_.

Sai lầm phổ biến nhất là:

> nghĩ rằng xác suất mắc bệnh gần bằng 99%.

Tức là họ _bỏ qua base rate_.

Đây chính là hiện tượng _base rate neglect_.

## 2. Thí nghiệm nổi tiếng của Gigerenzer

Nhà tâm lý học _Gerd Gigerenzer_ đã làm một thí nghiệm rất nổi tiếng.

Ông đưa cùng một bài toán theo hai cách trình bày.

### Cách 1: trình bày bằng xác suất

Ví dụ:

- 1% dân số mắc bệnh
- xét nghiệm đúng 99%
- dương tính giả 5%

Câu hỏi:

> Nếu một người có kết quả dương tính, xác suất họ mắc bệnh là bao nhiêu?

Kết quả:

- chỉ khoảng 10-20% người trả lời đúng.

### Cách 2: trình bày bằng tần suất tự nhiên

Cùng dữ kiện nhưng viết lại:

> Trong 10 000 người:
>
> - 100 người mắc bệnh
> - 9 900 người không mắc bệnh
> - 99 người mắc bệnh cho kết quả dương tính
> - 495 người khỏe mạnh vẫn dương tính

Câu hỏi:

> Trong số những người dương tính, bao nhiêu người thật sự mắc bệnh?

Kết quả:

- _hơn 70-80% người trả lời đúng_.

## 3. Điều gì đã thay đổi?

Toán học _không hề thay đổi_.

Chỉ thay đổi _cách biểu diễn thông tin_.

So sánh:

### Dạng xác suất

\[
P(B)=0.01
\]

### Dạng tần suất

> 100 người trong 10 000.

Trong dạng tần suất, cấu trúc Bayes trở nên _nhìn thấy trực tiếp_:

- 99 người bệnh và dương tính
- 495 người khỏe và dương tính

Tổng dương tính:

\[
594
\]

Vì vậy

\[
\frac{99}{594}
\]

được nhìn thấy ngay.

## 4. Vì sao tần suất tự nhiên mạnh hơn

Gigerenzer giải thích rằng:

Bộ não con người _tiến hóa để xử lý tần suất_, không phải xác suất.

Trong đời sống tự nhiên, con người thường gặp thông tin dạng:

- “3 người trong 10”
- “20 người trong làng”

chứ không phải:

- 0.3
- 0.2.

Vì vậy khi thông tin được trình bày dưới dạng _đếm được_, cấu trúc của bài toán trở nên trực quan.

## 5. Ví dụ 10 000 người trong bài của bạn

Khi bạn viết:

> hãy tưởng tượng cộng đồng 10 000 người

bạn đã vô tình sử dụng đúng kỹ thuật này.

Điều xảy ra là:

- \(P(B)\) → 100 người
- \(P(D\mid B)\) → 99 người
- \(P(D\mid \neg B)\) → 495 người

Toàn bộ Bayes biến thành _một bảng đếm_.

Đó chính là lý do phần này của bài luận rất mạnh về mặt sư phạm.

## 6. Một điều thú vị

Khi viết:

\[
P(B\mid D)=\frac{P(B\cap D)}{P(D)}
\]

người học thường không hiểu ý nghĩa.

Nhưng khi viết:

\[
\frac{99}{594}
\]

họ hiểu ngay.

Về toán học:

\[
\frac{99}{594}
\frac{0.0099}{0.0594}
\]

nhưng về _tâm lý học nhận thức_, hai biểu diễn này hoàn toàn khác.

## 7. Điều này làm cho bài luận của bạn mạnh hơn

Cấu trúc của bài luận của bạn thực ra đi qua ba tầng:

1️⃣ trực giác thực tế (tình huống y tế)
2️⃣ tần suất tự nhiên (10 000 người)
3️⃣ chuẩn hóa xác suất.

Đây là _một lộ trình nhận thức rất tốt_.

Nó đi từ:

đếm → tỷ lệ → xác suất.

## 8. Một gợi ý nhỏ cho bài luận

Bạn có thể thêm một câu ngắn ở đoạn 10 000 người:

> Bảng này không chỉ là một phép đếm minh họa. Nó cho phép ta nhìn thấy trực tiếp cấu trúc của bài toán dưới dạng tần suất tự nhiên, nơi mỗi con số biểu thị một nhóm người cụ thể trong cộng đồng.

Câu này giúp người đọc hiểu rằng bảng _không phải chỉ là ví dụ_, mà là một _cách nhìn khác của cấu trúc xác suất_.

## 9. Một nhận xét cuối

Điều thú vị là:

- tâm lý học nhận thức
- thống kê Bayes
- sư phạm toán học

đều hội tụ ở một điểm:

> **đếm các trường hợp cụ thể thường giúp hiểu xác suất sâu hơn so với bắt đầu từ công thức.**

Và đó chính xác là điều bài luận của bạn đang làm.

---
