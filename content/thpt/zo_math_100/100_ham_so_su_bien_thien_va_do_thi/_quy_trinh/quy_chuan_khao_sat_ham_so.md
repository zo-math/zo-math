# Quy chuẩn khảo sát hàm số dành cho AI

## 1. Mục đích, phạm vi và thẩm quyền

### 1.1. Mục đích

Tài liệu này hướng dẫn AI đi từ một hàm số hoặc họ hàm đến một bài khảo sát `.qmd`:

- đúng về đối tượng, miền, mệnh đề và chứng cứ;
- lựa chọn nội dung theo cấu trúc riêng của hàm;
- làm hiện rõ một hiện tượng trung tâm thay vì kê khai tính chất;
- tổ chức công thức, bảng, đồ thị và văn xuôi thành một mạch nhận thức;
- có thể kiểm tra, tái tạo và bàn giao.

Quy chuẩn không cung cấp một mục lục cố định cho mọi bài. Nó quy định cách xác lập, lựa chọn, tổ chức và kiểm định nội dung.

### 1.2. Phạm vi

Quy chuẩn áp dụng cho:

- một hàm số thực;
- một hàm được cho từng phần;
- một hàm được cho bằng công thức, bảng, thuật toán, quan hệ hoặc đồ thị toán học;
- một hàm hạn chế trên một miền;
- một họ hàm có tham số;
- một bài tập trung vào toàn bộ hàm hoặc vào một hiện tượng đã xác định.

Quy chuẩn điều chỉnh kiến trúc toán học và mạch giải thích của toàn bài. Nó không tự quy định chi tiết màu, nét, trục, phông, mã TikZ/PGFPlots hoặc một phong cách viết cụ thể.

### 1.3. Nguồn lí thuyết và các tài liệu phối hợp

Nguồn lí thuyết có thẩm quyền của quy chuẩn này là:

`_quy_trinh/nguon_li_thuyet/khung_khao_sat_ham_so_hoan_chinh_04.qmd`

Bản nguồn được nhận diện bằng:

```text
SHA-256: c9a6ff3040a38658c9e55068395672da1fdb04d58bdd21c4ec027b85ac0d48aa
Cấu trúc: 6 phần, 21 chương, 212 kết quả được đánh số
```

Bản nguồn ấy giải thích sâu các khái niệm, điều kiện và giới hạn của phương pháp. Khi gặp trường hợp không được nén hết trong quy chuẩn này, phải trở về bản nguồn để lập luận; không tự bổ sung một quy tắc trái với bản nguồn.

Hai tài liệu phối hợp có ranh giới riêng:

| Tài liệu                                          | Thẩm quyền trực tiếp                                                                                                    |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `quy_chuan_khao_sat_ham_so.md`                    | Đối tượng khảo sát, hồ sơ toán học, hiện tượng trung tâm, mạch lập luận, kiến trúc bài và nghiệm thu toàn bài           |
| `huong_dan_su_dung_khoi_noi_dung.md`              | Quyết định có dùng khối hay không; trạng thái mở cố định hoặc thu gọn; màu theo chức năng; cú pháp và kiểm định hệ khối |
| `quy_chuan_do_thi_sinh_ma_nguon_tikz_pgfplots.md` | Phân tích và sinh tệp `.tex`, miền quan sát, lấy mẫu, hệ trục, ngôn ngữ thị giác, render và nghiệm thu hình             |
| Tài liệu phong cách được chỉ định                 | Giọng, nhịp, ngôn ngữ và thẩm mỹ của văn xuôi                                                                           |

Quy chuẩn khảo sát xác định vị trí và mức hiển thị của nội dung trong mạch bài. `huong_dan_su_dung_khoi_noi_dung.md` quyết định nội dung ấy có cần tách thành khối hay không và, nếu có, khối được triển khai bằng trạng thái, màu và cú pháp nào.

Quy chuẩn khảo sát xác định **hình phải biểu diễn điều gì**. Quy chuẩn đồ thị quyết định **dựng hình ấy như thế nào**.

Trong dự án **100+ Hàm số: Sự biến thiên và đồ thị**, `AGENTS.md` cục bộ chỉ định **Học thuật tĩnh tại** là phong cách mặc định cho bài khảo sát một hàm số cụ thể. Yêu cầu trực tiếp của người dùng có thể thay đổi lựa chọn này. Phạm vi mặc định ấy không được suy rộng ra ngoài dự án.

### 1.4. Thứ tự ưu tiên

Khi các chỉ dẫn cùng điều chỉnh một nhiệm vụ, áp dụng theo thứ tự:

1. yêu cầu hiện tại của người dùng;
2. quy ước và chỉ dẫn tại đúng repository, thư mục hoặc tệp đang làm việc;
3. quy chuẩn khảo sát này;
4. quy chuẩn chuyên biệt được quy chuẩn này chuyển giao;
5. bản nguồn lí thuyết dùng để giải thích trường hợp chưa được nén hết.

Không được dùng một chỉ dẫn ở mức thấp hơn để âm thầm thay đổi phạm vi người dùng đã giao.

### 1.5. Ba mức quy tắc

| Mức                         | Cách thực hiện                                                                                      |
| --------------------------- | --------------------------------------------------------------------------------------------------- |
| **Bắt buộc**                | Luôn thực hiện; nếu một tiêu chí không liên quan, phải ghi _không áp dụng_ và nêu lí do             |
| **Kích hoạt khi thích hợp** | Chỉ thực hiện khi đối tượng, phạm vi hoặc câu hỏi dẫn đường tạo ra nhu cầu                          |
| **Chuyển giao**             | Quy chuẩn này lập đặc tả chức năng, sau đó giao phần triển khai chi tiết sang quy chuẩn chuyên biệt |

“Bắt buộc rà” không có nghĩa là “bắt buộc đưa thành đề mục”.

## 2. Nhiệm vụ của AI và chuỗi sản phẩm

### 2.1. Nhiệm vụ

AI phải:

1. xác lập đúng đơn vị khảo sát;
2. lập hồ sơ toán học rộng hơn bài cuối;
3. xác định hiện tượng trung tâm và câu hỏi dẫn đường;
4. xây bản đồ hiện tượng;
5. chọn nội dung theo chức năng;
6. tạo các mạch lập luận và mạng phụ thuộc;
7. lập đề cương vận hành;
8. đặc tả bảng và hình;
9. viết bài `.qmd`;
10. thực hiện ba lượt kiểm định và kiểm định hệ thống bài tập khi được kích hoạt;
11. chỉ bàn giao khi đạt điều kiện dừng.

Không được đi thẳng từ công thức đến văn xuôi dài khi chưa có hồ sơ và đề cương vận hành.

Chuỗi trên không phải quy trình một chiều. Khi chứng cứ làm thay đổi hiện tượng trung tâm, khi đề cương làm lộ một khoảng trống toán học hoặc khi bản viết làm chìm mạch chính, phải quay lại sản phẩm gần nhất cần sửa rồi cập nhật các sản phẩm phụ thuộc.

### 2.2. Hồ sơ khảo sát

Hồ sơ khảo sát là kho làm việc rộng, gồm:

- đối tượng, miền, tham số và quy ước;
- các mệnh đề dự kiến;
- mệnh đề đã xác lập cùng chứng cứ;
- điều kiện áp dụng;
- phản ví dụ, ngoại lệ và trường hợp biên;
- kết quả biểu tượng và kết quả số;
- yêu cầu đối với bảng và hình;
- giới hạn của dữ liệu và biểu diễn;
- nội dung được giữ lại hoặc loại khỏi bài.

Hồ sơ có thể chứa nhiều nội dung hơn bài cuối cùng. Không đưa toàn bộ hồ sơ vào bài chỉ vì các kết quả đều đúng.

### 2.3. Bản đồ hiện tượng

Bản đồ hiện tượng nối năm thành phần:

| Thành phần | Câu hỏi                                                 |
| ---------- | ------------------------------------------------------- |
| Hiện tượng | Điều gì cần được hiểu?                                  |
| Cơ chế     | Cấu trúc nào tạo ra điều ấy?                            |
| Dấu hiệu   | Hiện tượng biểu hiện ở đâu?                             |
| Chứng cứ   | Dựa vào đâu để xác lập quan hệ?                         |
| Biểu diễn  | Làm thế nào để quan hệ trở nên nhìn thấy hoặc đọc được? |

### 2.4. Đề cương vận hành

Đề cương vận hành là bản thiết kế có thể kiểm tra trước khi viết. Nó phải ghi ít nhất:

- đối tượng, phạm vi và người đọc;
- hiện tượng trung tâm;
- câu hỏi dẫn đường và câu trả lời dự kiến;
- bản đồ hiện tượng;
- các mạch lập luận;
- mạng phụ thuộc;
- trật tự nhận thức;
- mức hiển thị của từng nội dung;
- điểm kết tinh;
- điều kiện dừng.

### 2.5. Bài khảo sát và hồ sơ nghiệm thu

Đầu ra cuối cùng gồm:

- bài khảo sát `.qmd`;
- các bảng và hình được bài sử dụng;
- tệp nguồn phụ trợ khi nhiệm vụ yêu cầu;
- kết quả của ba lượt kiểm định;
- kết quả kiểm định hệ thống bài tập, nếu bài có bài tập;
- các tiêu chí _không áp dụng_ kèm lí do;
- giới hạn của bài và hướng mở rộng còn lại, nếu có.

Khi AI trực tiếp tạo hoặc sửa bài theo quy chuẩn này, các sản phẩm trung gian có thể là tệp tạm nếu người dùng không yêu cầu bàn giao riêng, nhưng AI vẫn phải tạo và kiểm tra chúng trong quá trình làm việc.

Khi AI chỉ kiểm định một bài đã tồn tại, sự vắng mặt của hồ sơ khảo sát, bản đồ hiện tượng hoặc đề cương vận hành không phải là bằng chứng cho thấy bài không đạt. Trong trường hợp ấy, phải kiểm định đầu ra từ những gì có thể truy trực tiếp trong bài và tài nguyên đi kèm; chỉ kiểm định việc tuân thủ quy trình khi các sản phẩm trung gian được cung cấp.

## 3. Đầu vào và cách xử lí thông tin thiếu

### 3.1. Đơn vị khảo sát

Trước khi khảo sát, phải xác lập:

| Trường          | Nội dung cần ghi                                                           |
| --------------- | -------------------------------------------------------------------------- |
| Đối tượng       | Hàm số, họ hàm, quan hệ hoặc quy tắc đang xét                              |
| Tập đích        | Ghi khi nó ảnh hưởng đến toàn ánh, song ánh, hàm ngược hoặc cách phát biểu |
| Phạm vi         | Miền tự nhiên hay miền hạn chế; khảo sát địa phương hay toàn cục           |
| Tham số         | Tham số tự do, miền tham số và trường hợp suy biến                         |
| Người đọc       | Kiến thức dự kiến và những cầu nối khái niệm cần thiết                     |
| Mục tiêu        | Khảo sát toàn diện trong phạm vi nào hoặc tập trung vào hiện tượng nào     |
| Đầu ra          | Tệp `.qmd`, bảng, hình và nguồn phụ trợ cần bàn giao                       |
| Phong cách      | Phong cách được chỉ định; để trống nếu chưa có                             |
| Ràng buộc dự án | Tệp mẫu, metadata, đường dẫn, quy ước và lệnh kiểm tra                     |

Cùng một công thức trên hai miền khác nhau là hai đơn vị khảo sát khác nhau. Cùng một hàm với hai người đọc hoặc hai hiện tượng trung tâm khác nhau cũng có thể dẫn đến hai bài hoàn chỉnh khác nhau.

### 3.2. Điều AI được tự quyết

AI được tự quyết các chi tiết không làm thay đổi bản chất nhiệm vụ, chẳng hạn:

- kí hiệu phụ nhất quán;
- thứ tự tạm thời của các phép tính trong hồ sơ;
- lựa chọn chứng cứ tương đương về sức mạnh và phù hợp với người đọc;
- tên đề mục phát sinh từ mạch bài;
- việc giữ một kết quả trong hồ sơ thay vì đưa vào bài.

Mọi suy định phải được ghi trong hồ sơ khi nó ảnh hưởng đến kết luận, miền, tham số hoặc đầu ra.

### 3.3. Điều kiện phải hỏi lại

Chỉ hỏi lại khi thiếu thông tin tạo ra nhiều cách hiểu hợp lí nhưng dẫn đến các đơn vị khảo sát khác nhau rõ rệt, đặc biệt khi:

- chưa xác định được đối tượng là một hàm hay một họ hàm;
- miền khảo sát có nhiều lựa chọn làm thay đổi kết quả;
- tham số chưa có miền và các miền khác nhau tạo ra các chế độ khác nhau;
- nhiệm vụ có thể là khảo sát toàn diện hoặc chỉ một hiện tượng;
- đầu ra hoặc mức độ chứng minh cần thiết thay đổi đáng kể theo người đọc;
- các chỉ dẫn có thẩm quyền ngang nhau mâu thuẫn trực tiếp.

Không hỏi lại chỉ để chuyển cho người dùng những quyết định nhỏ mà quy chuẩn đã cho phép AI tự xử lí.

### 3.4. Kiểm tra tài nguyên trước khi viết

Khi làm trong một dự án có sẵn, phải đọc các tệp cần thiết trước khi sửa:

- chỉ dẫn của repository và thư mục;
- tệp `.qmd` đích hoặc tệp mẫu cùng loại;
- các quy chuẩn được nhiệm vụ kích hoạt;
- hình, dữ liệu hoặc mã nguồn mà bài đang dẫn tới;
- trạng thái hiện tại của những tệp sẽ bị thay đổi.

Không được giả định một quy ước dự án từ trí nhớ khi có thể kiểm tra trực tiếp.

## 4. Nguyên tắc vận hành bất biến

### 4.1. Không khảo sát bằng danh sách máy móc

Không có một danh sách hữu hạn các phép tính bắt buộc cho mọi hàm số. Đạo hàm, bảng biến thiên, độ cong, tiệm cận, ứng dụng và liên hệ mở rộng chỉ xuất hiện khi có chức năng thực.

Quy trình bắt buộc AI rà để bảo vệ tính đúng đắn, rồi lựa chọn theo cấu trúc của hàm và câu hỏi dẫn đường.

### 4.2. Miền là một phần của đối tượng

Mọi phát biểu phải đi cùng đúng miền:

- giới hạn chỉ xét theo những cách tiếp cận được miền cho phép;
- liên tục, biến thiên và độ cong phải ghi trên tập hoặc khoảng thích hợp;
- nghiệm, tập mức và tập giá trị phụ thuộc vào miền;
- phép biến đổi, hàm ngược và tham số có thể thay đổi miền;
- hình và miền lấy mẫu không được nối qua phần ngoài tập xác định.

Không xem tập xác định như một thủ tục mở đầu rồi bỏ quên trong phần còn lại.

### 4.3. Phân biệt thuộc tính, công cụ và biểu diễn

Phải tách rõ:

- điều đúng về hàm số;
- công cụ dùng để xác lập điều ấy;
- bảng, hình hoặc ngôn ngữ dùng để biểu diễn điều ấy.

Đạo hàm là công cụ; đồng biến là thuộc tính. Hình vẽ là biểu diễn; đồ thị toán học là một tập hợp các cặp có thứ tự. Không dùng tên công cụ thay cho kết luận.

Không mặc định chọn công cụ mạnh hơn chỉ vì nó sẵn có. Khi so sánh trực tiếp, biến đổi đại số, bất đẳng thức, sai phân hoặc một công cụ sơ cấp khác làm lộ cơ chế rõ hơn, phải cân nhắc cách ấy trước khi chuyển sang đạo hàm. Khi hai phương pháp tự nhiên cho hai cách nhìn bổ sung, có thể đặt chúng cạnh nhau để người đọc thấy sự khác nhau giữa thuộc tính và công cụ xác lập thuộc tính.

Khi giữ **hai phương pháp cho cùng một tính chất**, không dùng phương pháp thứ hai chỉ để “xác nhận” kết quả đã có. Đề cương phải nêu rõ:

- tính chất chung mà cả hai phương pháp đang xác lập;
- đối tượng mà mỗi phương pháp thao tác trực tiếp;
- cơ chế hoặc thông tin mà phương pháp thứ nhất làm lộ;
- mức khái quát, tính cục bộ/toàn cục hoặc khả năng chuyển giao mà phương pháp thứ hai bổ sung;
- lí do sư phạm để giữ cả hai trong bài.

Với biến thiên, một so sánh trực tiếp, biến đổi đại số hoặc bất đẳng thức có thể làm lộ quan hệ giữa \(f(x_1)\) và \(f(x_2)\), trong khi \(f^\prime\) mã hóa chiều thay đổi qua dấu của tốc độ biến thiên cục bộ. Với tính lồi/lõm hoặc độ cong, một bất đẳng thức dây cung/trung điểm hay biến đổi đại số có thể cho cách nhìn không vi phân, còn \(f^{\prime\prime}\), khi áp dụng được, cho một tiêu chuẩn vi phân. Chỉ giữ cả hai khi sự đối sánh này đem lại giá trị nhận thức thật.


### 4.4. Hình không thay chứng minh

Một số hữu hạn điểm không xác định duy nhất đồ thị của một hàm: qua cùng một tập điểm có thể có vô số đường cong. Khi các điểm neo được dùng để dựng hoặc đọc đồ thị, bài phải chỉ rõ chúng hoạt động cùng những ràng buộc nào đã được chứng minh, chẳng hạn công thức, tính liên tục, đối xứng, biến thiên, cực trị, độ cong và hành vi tại biên. Tính liên tục, khi có vai trò trong mạch, bảo đảm rằng giá trị hàm tại các đầu vào đủ gần một điểm cũng gần giá trị tại điểm ấy; vì vậy nó loại trừ các đứt gãy cục bộ tại điểm liên tục. Tuy nhiên, tính liên tục tự nó vẫn không làm hữu hạn điểm xác định duy nhất một đường cong.

Với hàm đơn giản mà tính liên tục có thể làm lộ trực tiếp bằng một ước lượng hoặc phân tích hiệu, phải cân nhắc cách chứng minh ấy nếu nó nối tự nhiên đại số với việc đọc đồ thị; không mặc định viện dẫn một định lí mạnh hơn chỉ để rút ngắn.


Hình và dữ liệu hữu hạn có thể:

- gợi ra dự đoán;
- hỗ trợ giải thích;
- kiểm tra chéo;
- kết tinh nhiều kết quả đã xác lập.

Chúng không chứng minh một mệnh đề toàn cục hoặc vô hạn, trừ khi nhiệm vụ chỉ yêu cầu một kết luận số với mức bảo đảm đã công bố.

### 4.5. Mỗi kết luận phải truy được về chứng cứ

Với mỗi kết luận quan trọng, phải biết:

- mệnh đề chính xác là gì;
- phạm vi và lượng từ là gì;
- giả thiết nào đang dùng;
- chứng cứ quyết định là gì;
- điều kiện áp dụng đã được kiểm tra ở đâu;
- có ngoại lệ hoặc trường hợp biên nào không.

Phân biệt rõ quan sát, dự đoán, kết luận đã chứng minh, kết quả số gần đúng và hướng còn mở.

### 4.6. Nội dung được chọn theo chức năng

Một dữ kiện không vào bài chỉ vì nó quen thuộc, khó, đẹp hoặc đã được tính xong. Nó phải phục vụ ít nhất một chức năng:

- xác lập hiện tượng;
- giải thích cơ chế;
- cung cấp tiền đề bắt buộc;
- kiểm soát cách hiểu sai;
- kết nối các mạch;
- kết tinh quan hệ;
- tạo một phép soi chiếu hoặc mở rộng có giá trị.

### 4.7. Mức hiển thị không thay mức chứng cứ

Đưa một kết luận vào khối nổi bật không làm nó mạnh hơn. Đưa một tiền đề vào khối ẩn không làm nó bớt cần thiết.

Không giấu mắt xích bắt buộc trong phần tùy chọn. Không dùng chú thích, bảng hoặc hình để né việc phát biểu điều kiện.

### 4.8. Tính đúng đi trước độ trôi chảy

Khi mạch văn hấp dẫn xung đột với độ chính xác, phải sửa mạch văn. Không:

- nói “luôn luôn” khi chỉ đúng cuối cùng hoặc trên một thành phần miền;
- nói “tiệm cận” khi mới quan sát thấy đường cong gần một đường;
- nói “cực trị” khi chưa phân biệt địa phương và toàn cục;
- nói “chu kì” khi mới thấy sự lặp hình;
- nói “xấp xỉ” mà không nêu miền hoặc mức bảo đảm cần thiết;
- nói một phép biến đổi “giữ” hoặc “bảo toàn” một đại lượng khi chứng cứ mới chỉ cho thấy giá trị đầu ra *phụ thuộc vào* đại lượng ấy;
- để một ẩn dụ trực giác làm thay đổi hoặc thay thế phát biểu toán học chính xác.

Với những quan hệ như *phụ thuộc vào*, *bảo toàn*, *làm mất*, *xác định được từ* và *có thể khôi phục từ*, phải dùng đúng động từ tương ứng với mệnh đề đã chứng minh.

Nếu một quan hệ trở thành hiện tượng trung tâm, phải ghi được một phép thử ngắn cho chính quan hệ ấy trong hồ sơ. Đặc biệt, “bảo toàn” phải chịu phép thử bằng đúng mệnh đề bất biến mà từ ấy khẳng định; đẳng thức của đại lượng trước–sau chỉ là trường hợp một biến. “Phụ thuộc vào” và “khôi phục được từ” phải có chứng cứ riêng. Không chấp nhận một ẩn dụ hoặc một ví dụ đơn lẻ làm phép thử cho động từ quan hệ.


### 4.9. Điều kiện dừng phụ thuộc vào phạm vi

Một bài hoàn chỉnh không cần nói hết mọi điều đúng về hàm. Nó phải giải quyết trọn vẹn câu hỏi đã công bố, bảo toàn các mắt xích thiết yếu và gọi đúng tên phần còn mở.

## 5. Lập hồ sơ khảo sát

### 5.1. Vòng rà nền tảng

Tất cả các mục dưới đây đều phải được rà. Chỉ đưa vào bài những nội dung cần cho tính đúng đắn hoặc mạch giải thích.

| Phương diện              | Câu hỏi bắt buộc                                                                                                    |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| Đối tượng                | Hàm được cho bằng cách nào? Có phải phân biệt hàm với biểu thức không? Miền và tập đích nào thuộc cách công bố hàm? |
| Tập xác định             | Điều kiện xác định là gì? Miền có những thành phần, đầu mút, điểm biên, điểm bị loại, điểm cô lập hoặc điểm tụ nào? |
| Tập giá trị và tập mức   | Tập dự kiến đã được chứng minh đủ hai phía: không có giá trị nào vượt ra ngoài và mọi giá trị được nêu đều thực sự đạt được chưa? Các mức quan trọng có nghịch ảnh nào? |
| Nghiệm, dấu và giao trục | Nghiệm có đầy đủ không? Dấu thay đổi ở đâu? Giao trục nào thực sự tồn tại?                                          |
| Hành vi tại biên miền    | Có giới hạn hữu hạn, vô hạn, một phía, tại vô cực hoặc không tồn tại không? Cơ chế nào tạo ra hành vi ấy?           |
| Liên tục và gián đoạn    | Liên tục ở đâu? Gián đoạn theo cơ chế nào? Có thể mở rộng liên tục không?                                           |
| Biến thiên               | Có thể so sánh trực tiếp, dùng đại số/bất đẳng thức/sai phân hay thực sự cần đạo hàm? Phát biểu trên miền nào? Có vô hạn khoảng biến thiên không? |
| Điểm đặc biệt            | Điểm tới hạn, cực trị, điểm góc, điểm nhọn, tiếp tuyến đứng, điểm uốn hoặc mức đặc biệt nào có chức năng?           |
| Ràng buộc đồ thị         | Những mệnh đề nào quyết định hình dạng, nhánh, điểm, giới hạn và miền quan sát?                                     |

Với miền tổng quát, không được dùng ngôn ngữ khoảng một cách máy móc. Phải lập bản đồ những cách tiếp cận được phép từ trong miền.

### 5.2. Vòng rà kích hoạt

Các phương diện sau chỉ được triển khai khi cấu trúc của hàm hoặc câu hỏi dẫn đường kích hoạt:

| Phương diện              | Dấu hiệu kích hoạt                                                                            |
| ------------------------ | --------------------------------------------------------------------------------------------- |
| Bị chặn và cực biên      | Tập giá trị, giới hạn, mô hình hoặc hình dạng phụ thuộc vào cận hay giá trị đạt được          |
| Độ cong                  | Chiều biến thiên chưa đủ giải thích hình dạng hoặc cần kiểm soát tiếp tuyến, điểm uốn         |
| Đối xứng                 | Miền và công thức được bảo toàn qua phản xạ hoặc có trục, tâm đối xứng                        |
| Tuần hoàn                | Có độ dời bảo toàn giá trị; cần phân biệt với lặp lại không tuần hoàn                         |
| Hợp hàm                  | Cơ chế phụ thuộc vào cách hàm trong biến đổi đầu vào và hàm ngoài biến đổi giá trị trung gian |
| Hàm ngược                | Cần đảo chiều quan hệ hoặc hạn chế miền; phải phân biệt miền của hàm bị hạn chế, tập giá trị của nó và miền của hàm ngược |
| Phép biến đổi            | Hàm được đọc từ một hàm chuẩn qua tịnh tiến, co giãn, phản xạ hoặc phối hợp                   |
| Tham số                  | Tham số làm đổi miền, số nghiệm, cực trị, hình dạng hoặc chế độ                               |
| Tiệm cận và sai lệch     | Cần mô tả mô hình gần biên và phần sai lệch khỏi mô hình                                      |
| Tốc độ tăng trưởng       | Hai hàm cùng xu hướng nhưng cần so sánh bậc, tỉ lệ hoặc thành phần trội                       |
| Dãy điểm đặc biệt        | Nghiệm, cực trị, mức hoặc điểm khác tạo thành cấu trúc vô hạn                                 |
| Dao động                 | Giá trị thay đổi lặp lại hoặc không thu hẹp; cần hàm bao, mật độ hay tập giá trị tụ           |
| Tính toán số             | Không có biểu thức đóng thích hợp hoặc cần kết quả gần đúng có mức bảo đảm                    |
| Nhiều cửa sổ             | Một miền quan sát không thể biểu hiện đồng thời các hành vi thiết yếu                         |
| Soi chiếu                | Một hàm hoặc mô hình gần giúp phân biệt cơ chế đang xét                                       |
| Ứng dụng và mô hình hóa  | Hàm gắn với đại lượng, đơn vị, dữ liệu hoặc quyết định trong bối cảnh thực                    |
| Liên hệ toán học mở rộng | Một kết quả khảo sát tự nhiên dẫn tới công cụ hoặc câu hỏi mới làm sáng rõ hàm                |

Không kích hoạt một phương diện chỉ để làm bài có vẻ đầy đủ.

### 5.3. Hồ sơ mệnh đề–chứng cứ

Mỗi kết luận dự kiến phải đi qua các bước:

1. phát biểu đúng đối tượng, miền và lượng từ;
2. ghi trạng thái: dự đoán, đã xác lập, gần đúng hoặc còn mở;
3. ghi giả thiết và công cụ;
4. kiểm tra điều kiện áp dụng;
5. xác định chứng cứ quyết định;
6. kiểm tra tồn tại, duy nhất và tính đầy đủ khi có liên quan;
7. tìm phản ví dụ hoặc trường hợp biên có thể bác bỏ một phát biểu mạnh hơn;
8. đối chiếu với công thức, bảng, số và hình.

Các nguồn chứng cứ có thể gồm:

- định nghĩa;
- đồng nhất thức trên đúng miền;
- bất đẳng thức;
- định lí đã kiểm tra đủ điều kiện;
- dãy phản chứng;
- phân tích trường hợp;
- phép tính biểu tượng;
- tính toán số có sai số hoặc mức bảo đảm được công bố.

### 5.4. Kết quả biểu tượng và kết quả số

Ưu tiên kết quả biểu tượng khi nó:

- xác lập được cấu trúc;
- cho thấy tính đầy đủ;
- giải thích được cơ chế;
- giúp kiểm tra hình hoặc dữ liệu số.

Kết quả số phải ghi:

- phương pháp;
- miền tìm kiếm;
- độ chính xác hoặc sai số;
- điều kiện dừng;
- mức bảo đảm: quan sát, xấp xỉ, bao hàm hay chứng nhận.

Không nâng một nghiệm số quan sát được thành danh sách nghiệm đầy đủ khi chưa có chứng cứ.

### 5.5. Kiểm tra chéo hồ sơ

Trước khi chọn nội dung, phải kiểm tra:

- miền trong mọi công thức có thống nhất không;
- kí hiệu, thuật ngữ và tham số có một nghĩa xuyên suốt không;
- nghiệm và cực trị có phù hợp với dấu, biến thiên và tập giá trị không;
- giới hạn có phù hợp với bị chặn, tiệm cận và hình dạng dự kiến không;
- đối xứng hoặc tuần hoàn có truyền đúng các kết quả không;
- bảng, dữ liệu số và hình có vi phạm ràng buộc giải tích nào không.

Mâu thuẫn phải được giải quyết ở hồ sơ, không để văn xuôi che khuất.

## 6. Hiện tượng trung tâm và bản đồ hiện tượng

### 6.1. Chọn hiện tượng trung tâm

Hiện tượng trung tâm phải:

- thật sự xảy ra trong phạm vi bài;
- có chứng cứ đủ để giải thích;
- kết nối được nhiều dữ kiện quan trọng;
- giúp người đọc thay đổi hoặc làm sâu cách đọc hàm số;
- đủ cụ thể để dẫn đường, nhưng không hẹp đến mức chỉ còn một phép tính.

Hiện tượng trung tâm ban đầu là một giả thuyết tổ chức. Phải sửa hoặc thay nó nếu hồ sơ không nâng đỡ được. Phát biểu trung tâm phải tách rõ quan hệ toán học đã chứng minh với hình ảnh trực giác dùng để giải thích; không giữ một trục nhận thức dựa trên một từ quan hệ mơ hồ hoặc sai.

### 6.2. Viết câu hỏi dẫn đường

Câu hỏi dẫn đường là một chức năng tổ chức, không bắt buộc phải mang hình thức nghi vấn. Nó có thể được biểu đạt bằng một câu hỏi hoặc một phát biểu nhiệm vụ tương đương, miễn là gọi đúng quan hệ cần giải thích và có thể được giải quyết trong phạm vi bài.

Câu hỏi dẫn đường phải:

- gọi đúng đối tượng và phạm vi;
- hướng tới một quan hệ cần giải thích;
- không chứa sẵn kết luận chưa được kiểm tra;
- ngắn vừa đủ để gọi đúng vấn đề, không dồn cả bản tóm tắt của bài vào một câu hỏi;
- có thể được trả lời bằng một chuỗi chứng cứ hữu hạn trong phạm vi bài.

Câu hỏi yếu:

> Hàm số có những tính chất gì?

Câu hỏi vận hành:

> Cấu trúc nào khiến hai vùng của miền biểu hiện hai kiểu hành vi khác nhau, và các dấu hiệu ấy kết tinh trên đồ thị ra sao?

Phát biểu nhiệm vụ tương đương:

> Phần còn lại của bài sẽ làm rõ cấu trúc tạo nên hai kiểu hành vi khác nhau trên hai vùng của miền và cách các dấu hiệu ấy kết tinh trên đồ thị.

### 6.3. Lập bản đồ hiện tượng

Với mỗi hiện tượng, ghi:

1. **Hiện tượng:** mô tả chính xác điều xảy ra.
2. **Cơ chế:** xác định cấu trúc tạo ra hiện tượng.
3. **Dấu hiệu:** nghiệm, dấu, dãy điểm, giới hạn, cực trị, hàm bao hoặc quan hệ khác.
4. **Chứng cứ:** chỉ ra mệnh đề và phương pháp xác lập.
5. **Biểu diễn:** xác định bảng, hình, công thức hoặc phép soi chiếu làm hiện rõ quan hệ.

### 6.4. Kiểm tra các đường nối

- Có dấu hiệu nhưng thiếu cơ chế: mới mô tả.
- Có cơ chế nhưng thiếu chứng cứ: mới phỏng đoán.
- Có chứng cứ nhưng thiếu giải nghĩa: mới tính toán.
- Có hình nhưng không truy về mệnh đề: mới minh họa bề mặt.
- Có nhiều kết quả nhưng không quay lại hiện tượng: mới tích lũy dữ liệu.

Không viết bài khi bản đồ còn một khoảng trống làm thay đổi câu trả lời trung tâm.

### 6.5. Nhiều hiện tượng

Nếu có nhiều hiện tượng:

- chọn một hiện tượng làm trục chính;
- giữ hiện tượng phụ khi nó giải thích, soi chiếu hoặc kết tinh trục chính;
- tách thành bài khác khi hiện tượng phụ cần một câu hỏi dẫn đường, mạng chứng cứ và điểm kết tinh riêng.

Không ép hai cuộc khảo sát độc lập vào một bài chỉ vì chúng cùng xét một hàm.

## 7. Lựa chọn nội dung

### 7.1. Gán vai trò

Mỗi dữ kiện được cân nhắc phải có một vai trò chính:

| Vai trò    | Chức năng                                            |
| ---------- | ---------------------------------------------------- |
| Định hướng | Làm hiện câu hỏi hoặc trực giác ban đầu              |
| Thiết lập  | Xác định đối tượng, miền, kí hiệu và tiền đề         |
| Chứng minh | Xác lập một mệnh đề thiết yếu                        |
| Giải thích | Làm rõ cơ chế hoặc ý nghĩa của kết quả               |
| Tổng hợp   | Kết tinh nhiều kết quả trong bảng, hình hoặc quan hệ |
| Soi chiếu  | Làm rõ bằng đối chiếu với một đối tượng gần          |
| Mở rộng    | Dẫn tới nhận thức mới sau khi mạch chính đã hoàn tất |

Một dữ kiện có thể hỗ trợ nhiều vai trò, nhưng phải biết vai trò chính để quyết định vị trí và độ dài.

### 7.2. Tiêu chuẩn vào mạch chính

Một kết quả chỉ thuộc mạch chính khi có đường nối rõ đến câu trả lời trung tâm bằng ít nhất một cách:

- xác lập hiện tượng;
- giải thích cơ chế;
- cung cấp tiền đề bắt buộc;
- loại một cách hiểu sai quan trọng;
- nối hai mạch thiết yếu;
- kết tinh quan hệ trên bảng hoặc hình.

Kết quả đúng nhưng không có chức năng được giữ trong hồ sơ hoặc để ngoài bài.

### 7.3. Ứng dụng và mô hình hóa

Chỉ kích hoạt khi hàm thực sự biểu diễn một bối cảnh. Khi đó phải:

- xác định đầu vào, đầu ra và đơn vị;
- phân biệt tập xác định toán học với miền có ý nghĩa thực tế;
- nêu các giả định tạo nên mô hình;
- diễn giải nghiệm, cực trị, tốc độ thay đổi và tiệm cận theo bối cảnh;
- loại các nghiệm toán học không có nghĩa thực tế;
- nêu phạm vi dữ liệu, yếu tố bị bỏ qua và độ nhạy theo tham số;
- không biến một khớp số thành quan hệ nhân quả nếu chưa có chứng cứ.

Ứng dụng không được gắn thêm như một câu chuyện trang trí sau khi bài đã kết thúc.

### 7.4. Liên hệ toán học mở rộng

Chỉ kích hoạt khi liên hệ:

- phát sinh tự nhiên từ kết quả khảo sát;
- bắt đầu bằng một câu hỏi nối kết;
- chỉ cần lượng kiến thức mới tối thiểu;
- có điều kiện áp dụng được kiểm tra;
- quay lại làm sáng rõ hàm số đang xét;
- phân biệt kết quả đã chứng minh với hướng mới được gợi ra.

Phải dừng hoặc tách bài khi vấn đề mới cần một hệ khái niệm, chứng cứ và câu hỏi dẫn đường độc lập. Khi một tên lớp toán học hoặc hình học đóng vai trò quan trọng trong cách đọc đối tượng, một định nghĩa hoặc tiêu chuẩn nhận diện đủ dùng có thể là liên hệ mở rộng tự nhiên; không dùng dáng hình thay cho căn cứ của tên gọi.

### 7.5. Kiểm soát độ dài và độ sâu

Rút gọn theo thứ tự:

1. bỏ dữ kiện không có chức năng;
2. chuyển chi tiết phụ sang khối mở rộng;
3. nén phép tính lặp nhưng giữ chứng cứ quyết định;
4. dùng bảng hoặc hình để tổng hợp những quan hệ đã xác lập;
5. tách nhánh độc lập thành bài khác.

Không rút gọn bằng cách bỏ điều kiện, ngoại lệ, bước suy luận thiết yếu hoặc phần đọc ngược sau biểu diễn.

Độ sâu không được đo bằng số đề mục hoặc số phép tính. Một bài đạt chiều sâu khi làm rõ được cơ chế, quan hệ giữa các kết quả, lựa chọn hoặc đối sánh công cụ, giới hạn của kết luận và ít nhất một cách nhìn có thể chuyển sang đối tượng khác. Không thêm nội dung chỉ để làm bài dài; cũng không cắt bỏ những lớp giải thích khiến bài chỉ còn một bản tóm tắt kiến thức.

## 8. Tạo mạch lập luận và mạng phụ thuộc

### 8.1. Cấu trúc một mạch

Mỗi mạch lập luận phải thực hiện sáu chức năng:

1. nêu vấn đề cục bộ;
2. đưa ra tiền đề;
3. cung cấp chứng cứ;
4. phát biểu kết luận đúng phạm vi;
5. giải nghĩa kết luận đối với hàm số;
6. nối về câu hỏi trung tâm hoặc mạch tiếp theo.

Không nhất thiết mỗi chức năng là một đoạn riêng, nhưng không được thiếu chức năng.

### 8.2. Chứng cứ quyết định và chứng cứ hỗ trợ

Phải phân biệt:

- **chứng cứ quyết định:** đủ sức xác lập mệnh đề;
- **chứng cứ hỗ trợ:** giúp quan sát, giải thích hoặc kiểm tra chéo.

Ví dụ, một dãy phản chứng có thể quyết định việc giới hạn không tồn tại; một đồ thị chỉ hỗ trợ người đọc nhìn thấy dao động.

### 8.3. Mạng phụ thuộc

Lập quan hệ “cần trước” giữa:

- định nghĩa và nơi sử dụng;
- kí hiệu và công thức;
- điều kiện và định lí;
- mệnh đề và biểu diễn;
- cơ chế và phép giải nghĩa;
- kết quả nền và phép soi chiếu.

Tiền đề, định nghĩa, kí hiệu và điều kiện phải xuất hiện trước nơi chúng được dùng theo nghĩa quyết định.

### 8.4. Phá vòng tròn phụ thuộc

Không được:

- dùng hình để chứng minh mệnh đề đã dùng để dựng hình;
- dùng bảng biến thiên để xác lập dấu đạo hàm khi bảng được dựng từ chính dấu ấy;
- dùng kết quả số làm đầy đủ danh sách nghiệm rồi dùng danh sách ấy để xác nhận miền tìm số;
- lấy trực giác từ hiện tượng làm giả thiết ngầm cho chứng minh hiện tượng.

Phá vòng tròn bằng chứng cứ độc lập, thay đổi thứ tự hoặc thu hẹp phạm vi kết luận.

### 8.5. Trật tự nhận thức

Sau khi tôn trọng trật tự logic, chọn thứ tự giúp người đọc:

1. nhận ra vấn đề;
2. hình thành dự đoán có kiểm soát;
3. gặp chứng cứ cần thiết;
4. sửa trực giác nếu cần;
5. thấy các kết quả kết tinh thành một quan hệ.

Không gom bài theo tên phép tính nếu các phép tính phục vụ những hiện tượng khác nhau.

### 8.6. Điểm nối

Cuối mỗi mạch, phải làm rõ ít nhất một điều:

- kết quả vừa có trả lời phần nào của câu hỏi;
- nó tạo tiền đề gì cho phần sau;
- nó thay đổi cách đọc đồ thị thế nào;
- nó loại bỏ cách hiểu sai nào;
- nó cần được tổng hợp với kết quả nào.

Chuyển đoạn không chỉ báo “tiếp theo xét”; nó phải cho thấy lí do nhận thức của bước tiếp theo.

## 9. Kiến trúc và mức hiển thị của bài

### 9.1. Sáu chức năng kiến trúc

Bài hoàn chỉnh phải thực hiện các chức năng:

1. **Khơi mở:** làm hiện hiện tượng hoặc căng thẳng nhận thức.
2. **Nhận diện:** xác lập đối tượng, miền và cấu trúc ban đầu.
3. **Triển khai:** xây các mạch chứng cứ và giải thích.
4. **Kết tinh:** tổng hợp bằng quan hệ, bảng, hình hoặc kết luận trung tâm.
5. **Soi chiếu:** đối chiếu khi nó làm rõ cơ chế.
6. **Khép lại:** trả lời câu hỏi và nêu nhận thức có thể chuyển giao.

Đây là sáu chức năng, không phải sáu tiêu đề bắt buộc. Tên và số đề mục phải phát sinh từ mạch của chính bài.

### 9.2. Bốn mức hiển thị

Mỗi nội dung thuộc một mức:

1. mạch chính;
2. khối mở rộng;
3. bảng, hình hoặc chú thích;
4. ngoài bài.

Mắt xích bắt buộc phải nằm trong mạch đọc chính. Khối mở rộng không được chứa điều kiện mà kết luận chính phụ thuộc vào.

### 9.2.1. Chuyển giao sang hướng dẫn khối nội dung

Việc một nội dung thuộc mạch chính hoặc phần mở rộng chưa tự động quyết định rằng nội dung ấy phải được đặt trong khối.

Với mỗi nội dung dự kiến tách thành khối, phải thực hiện đúng thứ tự:

1. xác định văn bản thông thường và hệ tiêu đề đã đủ biểu đạt vai trò của nội dung hay chưa;
2. nếu thực sự cần khối, xác định nội dung thuộc mạch chính hay phần đọc thêm để chọn khối mở cố định hoặc khối thu gọn;
3. chỉ sau đó mới chọn màu đỏ, vàng hoặc xám theo chức năng nội dung;
4. triển khai và kiểm định cú pháp theo `quy_trinh_xay_dung/huong_dan_su_dung_khoi_noi_dung.md`.

Không bắt buộc một bài phải có khối nội dung. Không dùng khối để trang trí hoặc thay thế cấu trúc lập luận. Không đặt mắt xích bắt buộc trong khối thu gọn.

Khi tạo nội dung mới, chỉ dùng hệ lớp hiện hành được tài liệu chuyên trách quy định. Khi kiểm định bài cũ, phải phân biệt lớp được giữ để tương thích lịch sử với lớp phù hợp cho nội dung mới; sự tồn tại của CSS tương thích không chứng minh rằng khối cũ đạt chuẩn hiện hành.

### 9.3. Khơi mở

Phần mở đầu phải:

- chỉ ra điều đáng khảo sát;
- tạo câu hỏi thật, không phô diễn;
- đủ dữ kiện để người đọc hiểu vấn đề;
- không công bố trước toàn bộ lời giải;
- không mở bằng một danh sách mục lục trá hình.

### 9.4. Nhận diện và triển khai

Phần nhận diện chỉ giữ những dữ kiện cần để bắt đầu đúng. Phần triển khai được tổ chức theo mạch lập luận, không theo danh sách “tập xác định – đạo hàm – bảng biến thiên – đồ thị” nếu danh sách ấy không phản ánh cơ chế.

### 9.5. Kết tinh

Điểm kết tinh phải nối nhiều kết quả đã được xác lập. Có thể là:

- một bảng biến thiên;
- một đồ thị hoặc hệ nhiều hình;
- một công thức tổng hợp;
- một bản đồ chế độ theo tham số;
- một mô tả cơ chế thống nhất.

Bảng biến thiên không phải thành phần mặc định.

### 9.6. Soi chiếu và khép lại

Phép soi chiếu phải làm rõ một khác biệt cơ chế, không chỉ đặt hai công thức cạnh nhau.

Phần khép lại phải:

- trả lời câu hỏi dẫn đường trong đúng phạm vi;
- gọi tên mối quan hệ trung tâm;
- không thêm một định lí mới chưa được chuẩn bị;
- chỉ ra cách nhìn có thể chuyển sang đối tượng khác;
- vẫn nhắc người đọc kiểm tra lại điều kiện ở đối tượng mới.

## 10. Bảng, đồ thị và tính toán số

### 10.1. Nguyên tắc chung

Mọi biểu diễn phải có:

- mục đích;
- mệnh đề trọng tâm;
- phạm vi đọc;
- nguồn dữ liệu hoặc chứng cứ;
- giới hạn;
- phần đọc ngược trong bài.

Không tạo bảng hoặc hình chỉ vì một bài khảo sát “thường có”.

### 10.2. Đặc tả bắt buộc trước khi dựng

Trước mỗi bảng hoặc hình, ghi:

| Trường             | Nội dung                                                             |
| ------------------ | -------------------------------------------------------------------- |
| Mệnh đề trọng tâm  | Quan hệ toán học nào phải được biểu diễn                             |
| Chức năng          | Định hướng, chứng minh hỗ trợ, giải thích, tổng hợp hay soi chiếu    |
| Miền               | Miền toán học và miền quan sát                                       |
| Chi tiết bắt buộc  | Nhánh, điểm, mức, đường tham chiếu, giới hạn hoặc cấu trúc phải thấy |
| Chi tiết lược bỏ   | Điều không cần cho câu hỏi hiện tại                                  |
| Giới hạn biểu diễn | Phần nào không thể kết luận từ hình hoặc bảng                        |
| Đọc ngược          | Văn xuôi sau biểu diễn phải chỉ ra điều gì                           |

### 10.3. Bảng giá trị

Bảng giá trị chỉ thể hiện một tập hữu hạn. Phải:

- chọn điểm theo câu hỏi, không chọn tùy tiện;
- ghi giá trị chính xác khi có thể;
- ghi độ chính xác cho giá trị gần đúng;
- không suy ra hành vi giữa các điểm chỉ từ bảng;
- không dùng bảng hữu hạn để chứng minh một cấu trúc vô hạn.

### 10.4. Bảng dấu và bảng biến thiên

Chỉ dùng khi chúng nén được một cấu trúc đã xác lập. Phải:

- phân đoạn đúng theo miền;
- biểu diễn đúng điểm bị loại, đầu mút và nhánh;
- không ngầm gộp các thành phần không liên thông;
- phân biệt giá trị đạt được với giới hạn;
- không dùng mũi tên để khẳng định điều chưa được chứng minh.

### 10.5. Đồ thị và nhiều cửa sổ

Miền quan sát phải được chọn theo mệnh đề trọng tâm. Khi một hình không thể biểu hiện đồng thời các hành vi thiết yếu, dùng các cửa sổ có chức năng khác nhau, chẳng hạn:

- toàn cảnh;
- phóng đại;
- soi chiếu;
- miền đại diện.

Mỗi cửa sổ phải có lí do và phạm vi đọc. Không coi phần bị cắt khỏi cửa sổ là không tồn tại.

### 10.6. Miền lấy mẫu

Phải:

- phân đoạn theo các thành phần miền và điểm đặc biệt;
- không nối qua điểm ngoài tập xác định;
- kiểm tra rủi ro bỏ sót dao động, nghiệm hoặc nhánh;
- dùng đổi biến, mốc chính xác hoặc lấy mẫu thích nghi khi lấy mẫu đều không trung thực;
- đối chiếu đường hiển thị với các ràng buộc giải tích.

Một tập điểm hữu hạn không phải đồ thị.

### 10.7. Chuyển giao sang quy chuẩn đồ thị

Khi cần tệp TikZ/PGFPlots:

1. hoàn thành đặc tả tại Mục 10.2;
2. chuyển đặc tả sang `quy_chuan_do_thi_sinh_ma_nguon_tikz_pgfplots.md`;
3. để quy chuẩn ấy quyết định phương pháp dựng, lớp hình, màu, trục, nhãn, mật độ mẫu, cấu trúc `.tex`, render và nghiệm thu;
4. đưa kết quả render về kiểm định chéo với bài.

Quy chuẩn khảo sát không được tự tạo một hệ thông số hình cạnh tranh với quy chuẩn đồ thị.

### 10.8. Đọc ngược sau biểu diễn

Sau bảng hoặc hình, bài phải:

- gọi tên quan hệ đang thấy;
- nối quan hệ ấy về các mệnh đề đã xác lập;
- chỉ ra phần nào là minh họa, phần nào là kết luận;
- nêu giới hạn đọc nếu hình có thể gây hiểu quá mức;
- giải thích vai trò của biểu diễn đối với câu hỏi trung tâm.

Không để chú thích hình làm toàn bộ công việc giải nghĩa.

## 11. Viết và hoàn thiện tệp `.qmd`

### 11.1. Viết từ đề cương đã kiểm tra

Chỉ bắt đầu viết toàn bài khi:

- đơn vị khảo sát đã rõ;
- hồ sơ không còn mâu thuẫn thiết yếu;
- hiện tượng trung tâm có chứng cứ;
- bản đồ hiện tượng đủ năm thành phần;
- mạng phụ thuộc không có vòng tròn;
- đề cương vận hành đã xác định điểm kết tinh.

### 11.2. Tính nhất quán

Giữ nhất quán:

- công thức;
- tập xác định và phạm vi;
- kí hiệu;
- thuật ngữ;
- chỉ số;
- tham số và miền tham số;
- quy ước về đầu mút, nhánh và chiều tiếp cận;
- mức chính xác của số.

Khi thay kí hiệu hoặc quy ước, phải sửa toàn bộ các nơi phụ thuộc.

### 11.3. Mức độ khẳng định

Dùng ngôn ngữ phân biệt:

- **quan sát:** điều thấy từ dữ liệu hoặc hình;
- **dự đoán:** mệnh đề đang chờ xác lập;
- **kết luận:** mệnh đề đã có chứng cứ;
- **xấp xỉ:** kết quả số với độ chính xác xác định;
- **gợi mở:** hướng chưa được chứng minh trong bài.

Không dùng “suy ra” khi mới có một dấu hiệu thị giác.

### 11.4. Công thức và giải nghĩa

Mỗi công thức quan trọng phải có chức năng rõ. Sau một chuỗi tính toán, phải trả lời:

- kết quả nói gì về hàm;
- nó giải thích hiện tượng nào;
- nó thay đổi cách đọc bảng hoặc đồ thị ra sao;
- vì sao người đọc cần kết quả ấy tại vị trí này.

Không để bài biến thành chuỗi biến đổi biểu thức không có điểm nối.

Nếu cùng một công thức hoặc kết quả xuất hiện lại, lần xuất hiện sau phải phát triển thêm chức năng hoặc ý nghĩa; không lặp chỉ để nhắc lại.

### 11.5. Khái niệm và người đọc

Khái niệm mới phải xuất hiện đúng lúc và ở mức cần thiết:

- định nghĩa trước khi dùng theo nghĩa quyết định;
- không giả định kiến thức vượt quá người đọc đã xác lập;
- không mở một nhánh lí thuyết dài nếu chỉ cần một công cụ nhỏ;
- dùng ví dụ hoặc phản ví dụ khi nó kiểm soát một nhầm lẫn có khả năng xảy ra.

Khi một khái niệm chính thức hoặc một lớp đối tượng có tên trở thành mắt xích quyết định của mạch, phải đưa định nghĩa, điều kiện hoặc tiêu chuẩn nhận diện ở mức đủ dùng trước khi dựa vào tên gọi ấy. Với hàm ngược, phải nói rõ miền của hàm gốc sau hạn chế, tập giá trị tương ứng và miền của hàm ngược; không để một câu văn làm nhập nhằng các tập này.

Tên lớp toán học xuất hiện trong **heading, caption, kết luận hoặc bài tập mở rộng** được xem là một tín hiệu kích hoạt kiểm tra này. Nếu tên gọi có vai trò tổ chức cách hiểu của bài và không thuộc kiến thức đã được khai báo của người đọc, phải đưa căn cứ nhận diện trước lần dùng mang tính kết luận; hình dáng nhìn thấy hoặc thói quen gọi tên không thay thế tiêu chuẩn.


### 11.6. Quy ước dự án và metadata

Phải tuân theo tệp mẫu và quy ước hiện hành của dự án về:

- YAML;
- cấp tiêu đề;
- nhãn và dẫn chiếu;
- cú pháp công thức;
- khối nội dung;
- đường dẫn;
- hình dùng cho HTML và PDF;
- metadata tải xuống;
- lệnh render và kiểm tra.

Không tự sao chép metadata từ một trang khác khi chưa kiểm tra tên, mô tả, hình và đường dẫn của trang hiện tại.

### 11.7. Phong cách viết

Đọc và áp dụng tài liệu phong cách có hiệu lực trong phạm vi nhiệm vụ sau khi kiến trúc toán học đã ổn định. Đối với bài khảo sát hàm số cụ thể trong dự án này, Học thuật tĩnh tại là mặc định cục bộ theo `AGENTS.md`, trừ khi yêu cầu trực tiếp của người dùng chỉ định khác.

Phong cách không được:

- thay đổi mệnh đề;
- xóa điều kiện;
- làm mờ mức chứng cứ;
- đảo trật tự phụ thuộc;
- thêm một kết luận không có trong hồ sơ.

Khi Học thuật tĩnh tại có hiệu lực, dùng `hoc_thuat_tinh_tai.md`. Không suy rộng mặc định cục bộ của dự án này sang phạm vi khác.

### 11.8. Kiểm tra tệp

Trước nghiệm thu nội dung:

- kiểm tra cú pháp Markdown/Quarto;
- kiểm tra dẫn chiếu, đường dẫn và tài nguyên;
- kiểm tra khoảng trắng và mã hóa theo quy ước dự án;
- render bằng đúng quy trình khi môi trường cho phép;
- kiểm tra cả đầu ra HTML và PDF khi nhiệm vụ yêu cầu cả hai;
- xem bản render thật đối với bảng, hình và bố cục quan trọng.

## 12. Ba lượt kiểm định và kiểm định có điều kiện

### 12.1. Giao thức xác nhận

Quy chuẩn phân biệt hai chế độ:

1. **Kiểm định đầu ra:** đánh giá những gì có thể truy trực tiếp trong bài, công thức, bảng, hình, tệp nguồn và kết quả kiểm tra. Đây là chế độ mặc định khi kiểm nghiệm một bài đã tồn tại.
2. **Kiểm định tuân thủ quy trình:** đánh giá việc lập hồ sơ khảo sát, bản đồ hiện tượng, đề cương vận hành và các sản phẩm trung gian khác. Chỉ thực hiện chế độ này khi AI đang trực tiếp tạo hoặc sửa bài theo quy chuẩn, hoặc khi các sản phẩm trung gian được cung cấp.

Không được suy từ việc thiếu sản phẩm trung gian rằng đầu ra không đạt. Nếu không có đủ căn cứ để kiểm định việc tuân thủ quy trình, ghi rõ phạm vi ấy chưa được kiểm chứng.

Trong báo cáo chẩn đoán, được dùng các trạng thái `Đạt`, `Đạt một phần`, `Không đạt` và `Không áp dụng`. `Đạt một phần` dùng khi cốt lõi đã đúng nhưng còn một mắt xích, cách diễn đạt hoặc chứng cứ cần bổ sung. Nếu thiếu tệp, tài nguyên hoặc công cụ để xác nhận, ghi `Chưa kiểm chứng`; trạng thái này không đồng nghĩa với `Không đạt`.

Trong quyết định nghiệm thu cuối, mỗi trạng thái `Đạt một phần` phải được giải quyết thành `Đạt`, `Không đạt` hoặc `Không áp dụng`. Một tiêu chí bắt buộc còn `Chưa kiểm chứng` thì chưa được tuyên bố nghiệm thu đạt.

Mỗi tiêu chí chỉ được đánh dấu đạt khi chỉ ra được căn cứ cụ thể trong:

- một vị trí của bài;
- một công thức;
- một bảng;
- một hình;
- một tệp nguồn hoặc kết quả kiểm tra.

Nếu tiêu chí không liên quan, ghi _không áp dụng_ và nêu lí do. Không đánh giá bằng cảm giác chung.

Nếu một tiêu chí không đạt:

1. ghi lỗi và mức ảnh hưởng;
2. truy về hồ sơ, mạch hoặc biểu diễn tạo ra lỗi;
3. sửa tại nguồn gần nhất;
4. chạy lại tiêu chí bị ảnh hưởng và các tiêu chí phụ thuộc.

### 12.2. Lượt thứ nhất: kiểm định toán học

Kiểm tra:

- đối tượng và tập xác định có đúng không;
- công thức, miền, kí hiệu, thuật ngữ, tham số và quy ước có nhất quán không;
- mỗi mệnh đề có đúng lượng từ và phạm vi không;
- điều kiện của định nghĩa và định lí đã được kiểm tra chưa;
- các trường hợp biên, suy biến và ngoại lệ đã được xử lí chưa;
- tồn tại, duy nhất và tính đầy đủ đã được phân biệt chưa;
- khi xác định một tập giá trị, hai chiều logic “không vượt ra ngoài” và “mọi giá trị được nêu đều đạt” đã đủ chưa;
- khi dùng tính chẵn, tính lẻ hoặc một tính chất đối xứng, điều kiện miền và định nghĩa đã được xử lí chưa;
- khi gọi một lớp toán học hoặc hình học bằng tên riêng, căn cứ cho tên gọi đã đủ chưa;
- khi dùng hàm ngược sau hạn chế miền, các miền và tập giá trị liên quan có được tách đúng không;
- kết luận có vượt quá chứng cứ không;
- kết quả số có đúng mức bảo đảm không;
- công thức, bảng, hình và văn xuôi có mâu thuẫn không;
- có vòng tròn chứng cứ nào không.

Không sang lượt hai khi còn lỗi có thể thay đổi kết luận trung tâm.

### 12.3. Lượt thứ hai: kiểm định mạch giải thích

Kiểm tra:

- hiện tượng trung tâm và câu hỏi dẫn đường có đủ đặc trưng cho chính đơn vị khảo sát, dùng đúng quan hệ toán học và đủ ngắn để dẫn đường không;
- câu hỏi dẫn đường có thật sự điều khiển việc chọn nội dung không;
- hiện tượng, cơ chế, dấu hiệu, chứng cứ và biểu diễn có nối đủ không;
- mỗi mạch có vấn đề, tiền đề, chứng cứ, kết luận, giải nghĩa và điểm nối không;
- quan hệ phụ thuộc có được tôn trọng không;
- trật tự nhận thức có giúp người đọc tiến từ câu hỏi đến kết tinh không;
- mỗi phần có chức năng rõ không;
- bảng và hình có tổng hợp kết quả đã xác lập không;
- phần đọc ngược sau biểu diễn có đủ không;
- phần kết có trả lời câu hỏi mở đầu trong đúng phạm vi không.

### 12.4. Lượt thứ ba: kiểm định giá trị nhận thức

Kiểm tra:

- hiện tượng trung tâm có đủ đặc trưng cho đơn vị khảo sát không;
- bài có làm rõ cơ chế hay chỉ liệt kê tính chất;
- bài có mặc định dùng một công cụ mạnh hơn khi một cách sơ cấp làm lộ cấu trúc tốt hơn không;
- khi có hai phương pháp tự nhiên với giá trị nhận thức khác nhau, bài đã cân nhắc việc đối sánh chúng chưa;
- khái niệm mới có xuất hiện đúng lúc không;
- chi tiết kĩ thuật có che khuất quan hệ chính không;
- phần mở rộng có cắt mạch chính không;
- phép soi chiếu có tạo ra khác biệt nhận thức không;
- điểm kết tinh có làm hiện mối quan hệ giữa các kết quả không;
- bài có để lại một cách nhìn có thể chuyển sang đối tượng khác không;
- cách nhìn ấy có giữ yêu cầu kiểm tra lại điều kiện ở đối tượng mới không.

### 12.5. Kiểm định hệ thống bài tập

Bài production chuẩn về một hàm số cụ thể trong dự án này có hệ thống bài tập như một phần tiếp tục của bài học. Chỉ coi mục này là _không áp dụng_ khi yêu cầu trực tiếp của người dùng loại bỏ bài tập hoặc loại nhiệm vụ thực sự không phải một bài học hoàn chỉnh; ngoại lệ phải được ghi rõ trong hồ sơ. Không dùng một quyết định tự khai của agent để bỏ hệ bài tập mặc định.

Phải kiểm định:

- giả thiết và dữ liệu của từng bài có đủ và nhất quán không;
- yêu cầu có xác định, phù hợp với dữ liệu và giải được không;
- kết quả mong đợi hoặc lời giải tham chiếu có đúng không;
- thứ tự các bài có tôn trọng quan hệ phụ thuộc không;
- hệ bài tập có giúp người học từng bước tái dựng mạch cốt lõi của bài không;
- hệ bài tập có mở ra ít nhất một hệ quả, biến thể hoặc lớp sâu chưa tiện triển khai trong thân bài không;
- hai chức năng thiết kế trên có được giữ ở mức nội bộ, không biến thành nhãn công khai như “Mục tiêu A/B” không;
- bài tập vượt khỏi phạm vi chính có được gọi đúng là mở rộng không.

Kết quả kiểm định này có thể được trình bày cùng ba lượt chính, nhưng phải có căn cứ riêng cho hệ thống bài tập.

### 12.6. Kiểm định lại sau chỉnh sửa

Sửa ở lượt sau có thể làm hỏng lượt trước. Vì vậy:

- sửa nội dung toán học: chạy lại cả ba lượt và kiểm định bài tập nếu phần sửa ảnh hưởng đến bài tập;
- đổi kiến trúc hoặc cắt đoạn: chạy lại lượt hai và ba, đồng thời kiểm tra các mệnh đề hoặc bài tập bị di chuyển;
- đổi bảng hoặc hình: chạy lại kiểm tra chéo toán học và toàn bộ tiêu chí biểu diễn;
- chỉ sửa chính tả không ảnh hưởng công thức hay nghĩa: kiểm tra cục bộ và kiểm tra kĩ thuật tệp.

## 13. Điều kiện dừng và bàn giao

### 13.1. Điều kiện dừng

Chỉ bàn giao khi:

1. câu hỏi dẫn đường đã được giải quyết trong phạm vi công bố;
2. mọi kết luận thiết yếu có chứng cứ;
3. không còn ngoại lệ làm đổi kết luận;
4. các mạch tạo thành một con đường liên tục;
5. mỗi thành phần trong bài có chức năng;
6. biểu diễn không vượt quá chứng cứ;
7. người đọc dự kiến không phải tự bổ sung mắt xích quan trọng;
8. phần còn mở được gọi đúng là mở rộng;
9. ba lượt kiểm định có căn cứ;
10. hệ thống bài tập vượt qua kiểm định có điều kiện, nếu được kích hoạt;
11. tệp và tài nguyên vượt qua các kiểm tra kĩ thuật thuộc phạm vi nhiệm vụ.

Bài cuối phải có thể được nén thành chuỗi:

> hiện tượng → cơ chế → chứng cứ → hình dạng → nhận thức.

Nếu không thể nén như vậy, cần xem lại hiện tượng trung tâm hoặc kiến trúc bài.

### 13.2. Thành phần bàn giao

Tùy phạm vi nhiệm vụ, bàn giao:

- tệp `.qmd` cuối;
- các hình, bảng và tệp nguồn phụ trợ;
- báo cáo ngắn về những gì đã tạo hoặc sửa;
- kết quả render và kiểm tra;
- kết quả kiểm định hệ thống bài tập, nếu được kích hoạt;
- các tiêu chí _không áp dụng_;
- giới hạn còn lại;
- tệp chưa sửa nhưng có liên quan, nếu cần tránh hiểu nhầm phạm vi.

Không tuyên bố hoàn tất khi chưa kiểm tra được một đầu ra bắt buộc. Nếu môi trường chặn một phép kiểm tra, phải nói rõ phép kiểm tra nào chưa thực hiện và vì sao.

### 13.3. Nhận thức có thể chuyển giao

Phần kết nên để lại một cách hỏi hoặc một cơ chế có thể dùng cho hàm khác, chẳng hạn:

- phép biến đổi đầu vào làm đổi mật độ hiện tượng thế nào;
- thành phần nhân bên ngoài làm đổi biên độ ra sao;
- tham số nào làm hệ chuyển chế độ;
- mô hình tiệm cận nào chi phối hình dạng;
- miền và cửa sổ nào cần chọn để thấy đúng cấu trúc.

Không biến sự chuyển giao thành khẳng định rằng hàm mới có cùng kết quả. Mỗi đối tượng mới phải được kiểm tra lại miền, điều kiện và chứng cứ.

### 13.4. Cập nhật quy chuẩn

Sau mỗi ca kiểm nghiệm:

1. phân biệt lỗi của bài, lỗi áp dụng và lỗi của chính quy chuẩn;
2. chỉ sửa quy chuẩn khi vấn đề có tính lặp lại hoặc cho thấy một khoảng trống vận hành;
3. truy thay đổi về bản nguồn lí thuyết;
4. không sửa âm thầm bản nguồn `_04`;
5. ghi rõ trường hợp kiểm nghiệm và lí do thay đổi.

Ca kiểm nghiệm đầu tiên của quy chuẩn này là:

$$
y=\sin\left(\frac{1}{x}\right).
$$

Ca này phải kiểm tra được ít nhất: miền nhiều thành phần, hợp hàm, đối xứng, biên bị loại, dao động, dãy điểm đặc biệt, tập giá trị tụ, nhiều cửa sổ và rủi ro lấy mẫu.

# Phụ lục A. Mẫu đầu vào

```markdown
## Đơn vị khảo sát

- Đối tượng:
- Cách cho hàm:
- Tập xác định hoặc miền hạn chế:
- Tập đích, nếu có vai trò:
- Phạm vi địa phương/toàn cục:
- Tham số và miền tham số:
- Trường hợp suy biến:
- Người đọc:
- Kiến thức được giả định:
- Mục tiêu:
- Hiện tượng được người dùng chỉ định, nếu có:
- Đầu ra cần bàn giao:
- Phong cách được chỉ định:
- Tệp mẫu và quy ước dự án:
- Quy chuẩn chuyên biệt được kích hoạt:
- Thông tin còn thiếu:
- Suy định được phép:
- Câu hỏi bắt buộc phải làm rõ:
```

# Phụ lục B. Mẫu hồ sơ khảo sát

## B.1. Bản đồ miền

| Thành phần                | Nội dung |
| ------------------------- | -------- |
| Tập xác định              |          |
| Các thành phần liên thông |          |
| Đầu mút và điểm biên      |          |
| Điểm bị loại              |          |
| Điểm cô lập               |          |
| Điểm tụ                   |          |
| Cách tiếp cận hợp lệ      |          |
| Trường hợp tham số        |          |

## B.2. Bảng mệnh đề–chứng cứ

| Mã  | Mệnh đề | Miền/phạm vi | Trạng thái                         | Chứng cứ quyết định | Điều kiện | Ngoại lệ | Kiểm tra chéo | Vai trò |
| --- | ------- | ------------ | ---------------------------------- | ------------------- | --------- | -------- | ------------- | ------- |
| M1  |         |              | Dự đoán/đã xác lập/gần đúng/còn mở |                     |           |          |               |         |

## B.3. Hai vòng rà

| Phương diện              | Đã rà | Kết quả chính | Kích hoạt     | Đưa vào bài | Lí do |
| ------------------------ | ----- | ------------- | ------------- | ----------- | ----- |
| Đối tượng                |       |               | Nền tảng      |             |       |
| Tập xác định             |       |               | Nền tảng      |             |       |
| Tập giá trị và tập mức   |       |               | Nền tảng      |             |       |
| Nghiệm, dấu và giao trục |       |               | Nền tảng      |             |       |
| Hành vi tại biên miền    |       |               | Nền tảng      |             |       |
| Liên tục và gián đoạn    |       |               | Nền tảng      |             |       |
| Biến thiên               |       |               | Nền tảng      |             |       |
| Điểm đặc biệt            |       |               | Nền tảng      |             |       |
| Ràng buộc đồ thị         |       |               | Nền tảng      |             |       |
| Bị chặn và cực biên      |       |               | Khi thích hợp |             |       |
| Độ cong                  |       |               | Khi thích hợp |             |       |
| Đối xứng                 |       |               | Khi thích hợp |             |       |
| Tuần hoàn                |       |               | Khi thích hợp |             |       |
| Hợp hàm                  |       |               | Khi thích hợp |             |       |
| Hàm ngược                |       |               | Khi thích hợp |             |       |
| Phép biến đổi            |       |               | Khi thích hợp |             |       |
| Tham số                  |       |               | Khi thích hợp |             |       |
| Tiệm cận và sai lệch     |       |               | Khi thích hợp |             |       |
| Tốc độ tăng trưởng       |       |               | Khi thích hợp |             |       |
| Dãy điểm đặc biệt        |       |               | Khi thích hợp |             |       |
| Dao động                 |       |               | Khi thích hợp |             |       |
| Tính toán số             |       |               | Khi thích hợp |             |       |
| Nhiều cửa sổ             |       |               | Khi thích hợp |             |       |
| Soi chiếu                |       |               | Khi thích hợp |             |       |
| Ứng dụng và mô hình hóa  |       |               | Khi thích hợp |             |       |
| Liên hệ toán học mở rộng |       |               | Khi thích hợp |             |       |

## B.4. Hồ sơ biểu diễn

| Biểu diễn | Mệnh đề trọng tâm | Chức năng | Miền/phạm vi đọc | Chi tiết bắt buộc | Giới hạn | Đọc ngược |
| --------- | ----------------- | --------- | ---------------- | ----------------- | -------- | --------- |
|           |                   |           |                  |                   |          |           |

# Phụ lục C. Mẫu bản đồ hiện tượng

```markdown
## Hiện tượng trung tâm

- Phát biểu hiện tượng:
- Phạm vi:
- Vì sao hiện tượng đáng khảo sát:
- Câu hỏi dẫn đường:
- Câu trả lời dự kiến:
- Trạng thái của câu trả lời:

## Bản đồ hiện tượng
```

| Hiện tượng | Cơ chế | Dấu hiệu | Chứng cứ | Biểu diễn |
| ---------- | ------ | -------- | -------- | --------- |
|            |        |          |          |           |

```markdown
## Kiểm tra đường nối

- Dấu hiệu đã có cơ chế:
- Cơ chế đã có chứng cứ:
- Chứng cứ đã được giải nghĩa:
- Biểu diễn truy được về mệnh đề:
- Mọi kết quả chính quay lại hiện tượng:
- Khoảng trống còn lại:
- Quyết định giữ/sửa/thay hiện tượng trung tâm:
```

# Phụ lục D. Mẫu đề cương vận hành

```markdown
## 1. Đối tượng và phạm vi

- Hàm, miền, tham số:
- Người đọc:
- Mục tiêu:
- Ràng buộc đầu ra:

## 2. Trục nhận thức

- Hiện tượng trung tâm:
- Câu hỏi dẫn đường:
- Câu trả lời đã kiểm tra:
- Nhận thức có thể chuyển giao:

## 3. Bản đồ hiện tượng

- Cơ chế:
- Dấu hiệu:
- Chứng cứ:
- Biểu diễn:

## 4. Các mạch lập luận

### Mạch 1

- Vấn đề:
- Tiền đề:
- Chứng cứ:
- Kết luận:
- Giải nghĩa:
- Điểm nối:

### Mạch 2

- Vấn đề:
- Tiền đề:
- Chứng cứ:
- Kết luận:
- Giải nghĩa:
- Điểm nối:

## 5. Mạng phụ thuộc

- Mạch cần trước:
- Mệnh đề cần trước:
- Biểu diễn phụ thuộc:
- Vòng tròn đã phát hiện và cách phá:

## 6. Trật tự nhận thức

- Thứ tự:
- Lí do:
- Điểm hình thành dự đoán:
- Điểm sửa trực giác:
- Điểm kết tinh:

## 7. Mức hiển thị

| Nội dung | Vai trò | Mức hiển thị                           | Lí do |
| -------- | ------- | -------------------------------------- | ----- |
|          |         | Mạch chính/mở rộng/biểu diễn/ngoài bài |       |

## 8. Bảng và hình

- Đặc tả từng biểu diễn:
- Quy chuẩn được chuyển giao:
- Phần đọc ngược:

## 9. Kiến trúc bài

- Khơi mở:
- Nhận diện:
- Triển khai:
- Kết tinh:
- Soi chiếu:
- Khép lại:

## 10. Điều kiện dừng riêng của bài

- Câu hỏi đã được giải quyết khi:
- Chứng cứ thiết yếu gồm:
- Ngoại lệ phải xử lí:
- Đầu ra kĩ thuật phải đạt:
```

# Phụ lục E. Phiếu nghiệm thu

Khi dùng phiếu để chẩn đoán, mỗi dòng ghi `Đạt`, `Đạt một phần`, `Không đạt` hoặc `Không áp dụng`, kèm căn cứ. Nếu chưa đủ tệp, tài nguyên hoặc công cụ để xác nhận, ghi `Chưa kiểm chứng` và nêu rõ giới hạn.

Khi dùng phiếu để quyết định nghiệm thu cuối, mỗi dòng phải được quy về `Đạt`, `Không đạt` hoặc `Không áp dụng`. Không kết luận nghiệm thu đạt khi còn tiêu chí bắt buộc ở trạng thái `Đạt một phần` hoặc `Chưa kiểm chứng`.

## E.1. Kiểm định toán học

| Tiêu chí                                                          | Trạng thái | Căn cứ | Hành động sửa |
| ----------------------------------------------------------------- | ---------- | ------ | ------------- |
| Đúng đối tượng và tập xác định                                    |            |        |               |
| Nhất quán công thức, miền, kí hiệu, thuật ngữ, tham số và quy ước |            |        |               |
| Đúng điều kiện và phạm vi của từng mệnh đề                        |            |        |               |
| Xử lí trường hợp biên, suy biến và ngoại lệ                       |            |        |               |
| Phân biệt tồn tại, duy nhất và tính đầy đủ                        |            |        |               |
| Không kết luận vượt quá chứng cứ                                  |            |        |               |
| Kết quả số có mức bảo đảm đúng                                    |            |        |               |
| Công thức, bảng, hình và văn xuôi không mâu thuẫn                 |            |        |               |
| Không có vòng tròn chứng cứ                                       |            |        |               |

## E.2. Kiểm định mạch giải thích

| Tiêu chí                                        | Trạng thái | Căn cứ | Hành động sửa |
| ----------------------------------------------- | ---------- | ------ | ------------- |
| Câu hỏi dẫn đường điều khiển việc chọn nội dung |            |        |               |
| Bản đồ hiện tượng đủ năm thành phần             |            |        |               |
| Mỗi mạch đủ sáu chức năng                       |            |        |               |
| Quan hệ phụ thuộc được tôn trọng                |            |        |               |
| Trật tự nhận thức hợp lí                        |            |        |               |
| Mỗi phần có chức năng                           |            |        |               |
| Bảng và hình tổng hợp kết quả đã xác lập        |            |        |               |
| Có phần đọc ngược sau biểu diễn                 |            |        |               |
| Kết luận trả lời câu hỏi mở đầu                 |            |        |               |

## E.3. Kiểm định giá trị nhận thức

| Tiêu chí                                         | Trạng thái | Căn cứ | Hành động sửa |
| ------------------------------------------------ | ---------- | ------ | ------------- |
| Hiện tượng trung tâm đủ đặc trưng                |            |        |               |
| Bài làm rõ cơ chế, không chỉ liệt kê             |            |        |               |
| Khái niệm mới xuất hiện đúng lúc                 |            |        |               |
| Chi tiết kĩ thuật không che mạch chính           |            |        |               |
| Phần mở rộng không cắt mạch chính                |            |        |               |
| Phép soi chiếu có giá trị                        |            |        |               |
| Điểm kết tinh làm hiện quan hệ                   |            |        |               |
| Bài để lại một cách nhìn có thể chuyển giao      |            |        |               |
| Cách nhìn mới vẫn giữ yêu cầu kiểm tra điều kiện |            |        |               |

## E.4. Kiểm định có điều kiện cho hệ thống bài tập

| Tiêu chí                                         | Trạng thái | Căn cứ | Hành động sửa |
| ------------------------------------------------ | ---------- | ------ | ------------- |
| Giả thiết và dữ liệu đầy đủ, nhất quán           |            |        |               |
| Yêu cầu xác định và giải được                    |            |        |               |
| Kết quả mong đợi hoặc lời giải tham chiếu đúng   |            |        |               |
| Thứ tự tôn trọng quan hệ phụ thuộc               |            |        |               |
| Hệ bài tập tiếp tục mục tiêu nhận thức của bài   |            |        |               |
| Phần vượt phạm vi chính được gọi đúng là mở rộng |            |        |               |

## E.5. Điều kiện dừng và kĩ thuật

| Tiêu chí                                            | Trạng thái | Căn cứ | Hành động sửa |
| --------------------------------------------------- | ---------- | ------ | ------------- |
| Câu hỏi dẫn đường đã được giải quyết                |            |        |               |
| Mọi kết luận thiết yếu có chứng cứ                  |            |        |               |
| Không còn ngoại lệ làm đổi kết luận                 |            |        |               |
| Các mạch tạo thành một con đường liên tục           |            |        |               |
| Người đọc không phải tự bổ sung mắt xích quan trọng |            |        |               |
| Phần còn mở được gọi đúng là mở rộng                |            |        |               |
| Cú pháp, dẫn chiếu và đường dẫn đạt                 |            |        |               |
| Render bắt buộc đạt                                 |            |        |               |
| Tệp và tài nguyên bàn giao đầy đủ                   |            |        |               |

## E.6. Kết luận nghiệm thu

```markdown
- Kết luận: Đạt/Không đạt
- Chuỗi nén của bài:
  hiện tượng → cơ chế → chứng cứ → hình dạng → nhận thức
- Lỗi còn lại:
- Tiêu chí không áp dụng:
- Kiểm định hệ thống bài tập:
- Kiểm tra chưa thực hiện được:
- Giới hạn đã công bố:
- Tệp bàn giao:
```
