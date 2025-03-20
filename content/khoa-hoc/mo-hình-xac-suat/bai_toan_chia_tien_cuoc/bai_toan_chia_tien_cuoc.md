---
title: "BÀI TOÁN CHIA TIỀN CƯỢC"
author: "Nguyễn Tấn Nhựt"
date: "2024-10-31"
output:
  html_document:
    keep_md: true
  pdf_document: 
    latex_engine: lualatex
header-includes:
  - \usepackage{forest}
---



**Ghi chú.** Trong tiếng Anh bài toán này thường được gọi bằng cái tên "the problem of points" thay vì "the problem of division of the stakes". Theo mình nghĩ, lí do, là vì muốn nhấn mạnh vào phương pháp kỳ vọng để giải quyết bài toán. Điểm số có thể xem là một biến ngẫu nhiên.

## Bài toán

**Chúng mình hãy cùng chơi trò tung đồng xu, mỗi người chọn một mặt để ghi điểm cho mình. Ai ghi đủ 3 điểm trước sẽ thắng toàn bộ số tiền cược. Nếu trò chơi phải dừng vào lúc bạn có 2 điểm và mình có 1 điểm, chúng mình phải chia tiền cược như thế nào?**

### Tỷ số điểm

Một cách chia đơn giản là dựa vào *tỷ số điểm hiện tại*, tức là 2:1. Theo cách này, bạn sẽ nhận 2 phần vì đang có 2 điểm, còn mình nhận 1 phần vì có 1 điểm. Nhưng liệu điều đó có thật sự hợp lý? Để làm rõ, hãy xét hai trường hợp dưới đây.

Giả sử bạn có 1 điểm và mình chưa có điểm nào. Theo cách chia trên, bạn sẽ nhận toàn bộ tiền cược, còn mình ra về tay trắng. Điều này quá bất công, vì trò chơi chưa ngã ngũ, và chỉ một ván thắng của bạn không đủ để quyết định kết cục toàn bộ trò chơi.

Bây giờ, giả sử luật chơi yêu cầu 55 điểm để chiến thắng, và lúc dừng lại, bạn có 54 điểm, còn mình có 45 điểm. Nếu chia theo tỷ lệ 54:45, tiền cược sẽ được chia gần như đồng đều, nhưng rõ ràng tình thế của chúng mình rất khác nhau: chỉ cần một chiến thắng nữa là bạn có thể nhận toàn bộ số tiền, trong khi mình sẽ cần đến 10 lần chiến thắng liên tiếp để đạt được điều đó. Chắc chắn bạn sẽ không hài lòng với cách chia này, vì lợi thế đang nghiêng về phía bạn.

Chia theo tỷ số điểm chỉ dựa vào số vòng thắng của mỗi người chơi đến thời điểm dừng, nhưng điều này bỏ qua khả năng thắng thua trong những vòng tiếp theo. Cách suy luận này không tính đến cơ hội còn lại của mỗi người chơi, dẫn đến việc chia tiền cược không công bằng nếu trò chơi dừng lại sớm, hoặc có một người sắp về đích.

<!--Chính các khả năng này mới là yếu tố then chốt để chia tiền một cách công bằng hơn.-->

**Câu hỏi.** *Nhằm sửa chữa sai lầm trong việc chia theo tỷ số điểm, mình lập luận rằng: Vì bạn hơn mình 1 điểm và nó chiếm 1/3 số điểm chiến thắng, nên bạn sẽ nhận 1/3 phần tiền cược của mình góp vào. Do đó, phần tiền mà bạn nhận được là $\frac{1}{2}+\frac{1}{2}\cdot\frac{1}{3}=\frac{2}{3}$, hay nói cách khác chúng mình vẫn chia theo tỷ số 2:1 nghiêng về bạn. Với cách lập luận này, khi bạn có 1 điểm và mình chưa có điểm, cũng chia theo tỷ số 2:1, có vẻ như đã khắc phục được tình trạng cực đoan tạo ra bởi tỷ số điểm. Theo bạn chúng mình có nên áp dụng cách chia này?*

### Tỷ số kịch bản thắng

Chúng mình đang ở tình huống bạn có 2 điểm và mình có 1 điểm, nghĩa là đã trải qua 3 ván. Nếu trò chơi tiếp tục, các kịch bản có thể xảy là:

- Bạn thắng ván thứ tư: bạn thắng chung cuộc, ký hiệu là $(\_,\_,\_,b)$.

- Mình thắng ván thứ tư, và bạn thắng ván thứ năm: bạn thắng chung cuộc, ký hiệu là $(\_,\_,\_,m,b)$.

- Mình thắng ván thứ tư và thứ năm: mình thắng chung cuộc, ký hiệu là $(\_,\_,\_,m,m)$.

Dựa vào các kịch bản trên, chúng mình vẫn chia theo tỷ số 2:1 không khác gì việc dựa theo tỷ số điểm đã bàn qua trước kia. Tuy nhiên, luận giải theo hướng này lại tránh được một trường hợp cực đoan: tại thời điểm dừng mà bạn có 1 điểm và mình chưa có điểm nào, sẽ chia theo tỷ số 3:2 thay vì 1:0 mà vừa nhìn vào đã thấy phi lý. Chính chỗ tốt này sẽ khiến chúng mình vội chấp nhận cách chia có vấn đề này. Cách đếm kịch bản chỉ dựa vào số lượng mà chưa xét đến khả năng xảy ra của từng kịch bản, dẫn đến sự không chính xác. Giả sử kịch bản thắng của bạn dễ xảy ra hơn, hoặc ngược lại, kịch bản thắng của mình lại dễ xảy ra hơn cả hai kịch bản của bạn gộp lại thì sao?

### Tỷ số kịch bản thắng mở rộng

Giải pháp là mở rộng các kịch bản để chúng có độ dài bằng nhau, bất kể kết quả dừng sớm. Như vậy, mỗi kịch bản có khả năng đóng góp công bằng vào kết quả cuối cùng. Chúng mình sẽ mở rộng các kịch bản như sau:

- Nếu bạn thắng ván thứ tư $(\_,\_,\_,b)$, thì vẫn tiếp tục chơi ván thứ năm, dù không thực sự cần thiết, tạo ra hai kịch bản mở rộng là $(\_,\_,\_,b,b)$ và $(\_,\_,\_,b,m)$.

- Với hai kịch bản còn lại là $(\_,\_,\_,m,b)$ và $(\_,\_,\_,m,m)$, chúng ta không cần mở rộng.

Bây giờ, chúng mình có đến 4 kịch bản, trong đó bạn thắng 3 kịch bản, còn mình thắng 1 kịch bản. Tỷ lệ chia tiền lúc này là 3:1 nghiêng về phía bạn. Đây là phương pháp chia tiền được nhà toán học Fermat đề xuất vào thế kỷ giữa 17, trong những lá thư trao đổi với Pascal, và được xem là công bằng vì đã xem xét đến tất cả khả năng diễn ra trò chơi.

Tại sao phương pháp mở rộng kịch bản là hợp lý? 

Để minh họa ý tưởng mở rộng kịch bản, mình sẽ thay đổi quy tắc trò chơi như sau:

**Chúng mình chơi trò tung đồng xu, với tổng cộng 5 lần tung, ai ghi đủ 3 điểm trước sẽ thắng. Nếu trò chơi bị dừng khi bạn có 2 điểm và mình có 1 điểm, chúng mình phải chia tiền cược như thế nào?**

Với thay đổi nhỏ này, các kịch bản mở rộng đã trở thành các kịch bản chính thức của trò chơi: $(\_,\_,\_,b,b)$, $(\_,\_,\_,b,m)$, $(\_,\_,\_,m,b)$ và $(\_,\_,\_,m,m)$.

Lúc này, tỷ lệ chia tiền là 3:1 nghiêng về phía bạn, hoàn toàn hợp lý. Sự thay đổi nhỏ này chỉ thêm một quy tắc "giả định" về số lần tung đồng xu tối đa, nhưng không làm thay đổi điều kiện chiến thắng ban đầu là người nào ghi được 3 điểm trước sẽ thắng trò chơi. Vì vậy, khi một người đạt 3 điểm, trò chơi vẫn sẽ kết thúc ngay tại đó. Điều này có nghĩa là số lần tung đồng xu tối đa chỉ tạo ra thêm các kịch bản giúp chúng ta có thể đánh giá công bằng hơn về khả năng thắng của mỗi người tại thời điểm trò chơi dừng lại.

Bằng cách giữ nguyên điều kiện chiến thắng và thêm quy tắc 5 lần tung, chúng mình chỉ đang mở rộng không gian kịch bản nhưng không thay đổi bản chất của trò chơi. Điều này giúp đảm bảo rằng mọi khả năng đều được tính đến mà không làm trò chơi trở nên khác biệt về cách kết thúc hay kết quả cuối cùng. Việc thêm vào quy tắc 5 lần tung không gây cản trở gì nếu bạn thắng ván thứ tư và không muốn đi tiếp ván thứ năm (có đi cũng vậy). Như thế, có hay không có quy tắc 5 lần tung, hai trò chơi này là một.

**Câu hỏi.** *Giả sử trò chơi dừng lại khi bạn cần thêm $m$ điểm và mình cần thêm $n$ điểm để giành chiến thắng. Hỏi số tiền cược nên chia thế nào?*

**Gợi ý.** Số tiền cược nên được chia theo tỷ số $\sum_{i=m}^{m+n-1}\binom{m+n-1}{i}:\sum_{i=0}^{m-1}\binom{m+n-1}{i}$ tương ứng cho bạn và mình. Trong đó, ký hiệu $\binom{r}{s}$ là số tập con $s$ phần tử của tập $r$ phần tử, hay tổ hợp chập $s$ của $r$.

### Xác suất 

Như đã phân tích, việc phân chia tiền cược dựa trên các kịch bản mở rộng giúp khắc phục hạn chế về mức độ xảy ra không đồng đều giữa các kịch bản khác nhau. Trong bài toán đang xét, kịch bản $(\_,\_,\_,b)$ có khả năng xảy ra cao hơn so với các kịch bản $(\_,\_,\_,m,b)$ và $(\_,\_,\_,m,m)$. Nguyên nhân là do kịch bản $(\_,\_,\_,b)$ chỉ cần bạn thắng một lần ở ván thứ tư để trò chơi kết thúc, trong khi kịch bản $(\_,\_,\_,m,b)$ đòi hỏi bạn phải thua ở ván thứ tư và sau đó thắng ở ván thứ năm. Cái nào cần nhiều điều kiện hơn sẽ khó xảy ra hơn.

Vì vậy, để có cách chia phần thưởng công bằng, chúng mình cần tìm một cách đo lường mức độ xảy ra của các kịch bản này, bất kể độ dài ngắn của chúng. Từ đó, chúng mình có thể xác định được mức độ thắng của mỗi bên.

Cụ thể, chúng mình đã đồng ý chia tiền cược theo tỷ số 3:1, nghĩa là bạn sẽ nhận $\frac{3}{4}$ số tiền cược và mình thì nhận $\frac{1}{4}$ còn lại. Ở đây, các con số $\frac{3}{4}$ và $\frac{1}{4}$ được xem là thước đo mức độ thắng tương ứng của bạn và của mình. Những tỷ lệ này dựa trên số lượng kịch bản thắng cho mỗi bên, từ đó phản ánh khả năng tương đối của từng bên để đạt được chiến thắng.

Cùng nhớ lại rằng có 3 kịch bản dẫn đến chiến thắng của bạn, chúng bao gồm:  $(\_,\_,\_,b,b)$, $(\_,\_,\_,b,m)$ và $(\_,\_,\_,m,b)$; và chỉ có 1 kịch bản dẫn đến chiến thắng của mình là $(\_,\_,\_,m,m)$. Tổng cộng có 4 kịch bản, và không có lý do gì để cho rằng cái nào đó trong chúng được ưu tiên hơn những cái còn lại. Do đó, chúng mình sẽ xem mức độ xảy ra của mỗi cái trong chúng là bằng nhau. Hơn nữa, mức độ xảy ra của mỗi kịch bản phải được xem xét trong khuôn khổ so sánh đối chiếu với các kịch bản còn lại, hay con số này phải thể hiện được tỷ lệ giữa kịch bản mà nó đại diện so với toàn bộ các kịch bản đang có. Như vậy, mức độ xảy ra của mỗi kịch bản trong 4 kịch bản này nên là $\frac{1}{4}$.



Thực tế, nếu tỉ lệ thắng ở mỗi lần tung xu là 50%, thì kịch bản bạn thắng ngay ván tiếp theo có xác suất cao hơn so với kịch bản mình thắng 2 ván liên tiếp. Vậy, **không phải kịch bản nào cũng có khả năng xảy ra như nhau**, và cách đếm đơn thuần số lượng kịch bản không phản ánh đúng "khả năng thắng" thực tế của mỗi người.

**Không thể mở rộng cho các trò chơi phức tạp hơn**

Trong một trò chơi với nhiều điểm hơn (ví dụ: ai đạt 5 điểm trước sẽ thắng), số lượng kịch bản có thể tăng lên rất nhiều, và việc đếm từng kịch bản trở nên không thực tế. Đồng thời, có thể có các chuỗi chiến thắng dài cho mỗi bên với những xác suất hoàn toàn khác nhau. Trong trường hợp này, cách đếm kịch bản sẽ không thể hiện đúng lợi thế của mỗi người khi trò chơi dừng lại, vì chỉ số lượng kịch bản không đủ để phân tích sự chênh lệch về khả năng thắng thực tế.

Hãy tưởng tượng rằng mỗi kịch bản đều có thể xảy ra trong một bối cảnh rất khác nhau. Ví dụ, trong kịch bản thứ nhất, bạn đã có một lợi thế rõ rệt về điểm số và có khả năng thắng rất cao. Trong khi đó, ở kịch bản thứ hai, mình có thể vừa tạo ra một bước ngoặt trong trò chơi. Do đó, cách phân chia dựa vào số lượng kịch bản này không thể hiện được một cách công bằng cơ hội và khả năng thắng cuộc của từng người.

Chia theo tỷ số kịch bản, cũng như chia theo tỷ số điểm, chỉ dựa trên kết quả tạm thời mà không xem xét đến quy trình và động lực của trò chơi. Điều này có thể dẫn đến những quyết định không công bằng và không phản ánh đúng thực tế của cơ hội chiến thắng của mỗi người.

Vì vậy, cần phải xem xét một phương pháp chia khác, nơi mà các yếu tố ảnh hưởng đến cơ hội chiến thắng được đánh giá một cách đầy đủ hơn, để đảm bảo rằng cách chia tiền cược thực sự công bằng và hợp lý.

**Câu hỏi.** Phải chăng một khi bạn có nhiều điểm hơn mình tại thời điểm dừng thì số kịch bản thắng cuộc của bạn nếu trò chơi được tiếp tục luôn nhiều hơn mình, hơn nữa còn có những kịch bản có khả năng xảy ra lớn hơn các kịch bản khác?

**Câu hỏi.** Số điểm bạn và mình có khi trò chơi dừng lại có liên hệ với số kịch bản diễn ra sau đó. Có thể tìm một công thức cho mối liên hệ này không?

## Mô hình toán học cho bài toán

Để tìm cách mô hình hóa bài toán này, các câu hỏi đầu tiên mà mình tự đặt ra là:

- Trò chơi này sẽ diễn ra như thế nào nếu không kết thúc giữa chừng?

- Cần tối thiểu và tối đa bao nhiêu ván đấu để phân thắng bại?

- Ngay cả khi nó kết thúc giữa chừng, mình cũng muốn biết trước đó nó đã diễn ra như thế nào? Và sẽ tiếp tục diễn ra như thế nào nếu không dừng lại?

Rõ ràng khi trò kết thúc, hoặc bạn là người chiến thắng hoặc mình là người chiến thắng. Nếu đó là bạn, diễn biến của trò chơi có thể đã xảy ra theo trình tự

1. Ván 1: bạn thắng;

2. Ván 2: mình thắng;

3. Ván 3: bạn thắng;

4. Ván 4: mình thắng;

5. Ván 5: bạn thắng.

Mình sẽ viết gọn lại diễn biến này là (bạn, mình, bạn, mình, bạn) và gọi nó là một kịch bản. Đây chỉ là một trong những kịch bản chiến thắng của bạn, nếu thay đổi vai trò của chúng mình cho nhau, (mình, bạn, mình, bạn, mình) là một kịch bản chiến thắng dành cho mình. Nếu đặc biệt may mắn, kịch bản (bạn, bạn, bạn) xảy ra, lúc này bạn chiến thắng liên tiếp 3 ván ngay từ đầu. Và ngược lại, (mình, mình, mình) là kịch bản may mắn của mình. Bất kỳ kịch bản chiến thắng nào dành cho bạn cũng có thể trở thành kịch bản chiến thắng dành cho mình miễn là thay đổi vai trò của chúng mình cho nhau. 

Trò chơi sẽ kết thúc ngay khi có một người ghi được 3 điểm, ví dụ người đó là bạn. Trò chơi sẽ kết thúc nếu bạn ghi liên tiếp 3 điểm. Để bạn ghi liên tiếp 3 điểm, cần ít nhất 3 ván đấu đã diễn ra và đó cũng chính là số ván đấu tối thiểu để phân thắng bại. Ngược lại, nếu sau 3 ván mà trò chơi chưa kết thúc, khi đó số điểm mà mình đã ghi được chỉ có thể là một trong ba con số 0 hoặc 1 hoặc 2. Từ đó suy ra số ván đấu tối đa để bạn giành chiến thắng là 5.

Việc liệt kê ra tất cả các kịch bản của trò chơi không phải đơn giản nếu không có một chút thủ thuật. Mình sử dụng một sơ đồ cây để tránh nhầm lẫn và tầm soát đầy đủ các kịch bản, sơ đồ đó như dưới đây.

<img src="images/cay_kich_ban_tro_choi_chia_phan_thuong/cay_kich_ban_tro_choi_chia_phan_thuong.svg" alt="Hình vẽ TikZ dưới dạng SVG">

Dựa vào sơ đồ cây 

Dựa vào sơ đồ cây này, mình có thể liệt kê được các kịch bản sau đây:

<table style="border-collapse: separate; border-spacing: 20px;">
  <tr>
    <td style="padding: 10px;">(mình, mình, mình)</td>
    <td style="padding: 10px;">(mình, mình, bạn, mình)</td>
    <td style="padding: 10px;">(mình, mình, bạn, bạn, mình)</td>
    <td style="padding: 10px;">(mình, mình, bạn, bạn, bạn)</td>
  </tr>
  <tr>
    <td style="padding: 10px;">(mình, bạn, mình, mình)</td>
    <td style="padding: 10px;">(mình, bạn, mình, bạn, mình)</td>
    <td style="padding: 10px;">(mình, bạn, mình, bạn, bạn)</td>
    <td style="padding: 10px;">(mình, bạn, bạn, mình, mình)</td>
  </tr>
  <tr>
    <td style="padding: 10px;">(mình, bạn, bạn, mình, bạn)</td>
    <td style="padding: 10px;">(mình, bạn, bạn, bạn)</td>
    <td style="padding: 10px;">(bạn, mình, mình, mình)</td>
    <td style="padding: 10px;">(bạn, mình, mình, bạn, mình)</td>
  </tr>
  <tr>
    <td style="padding: 10px;">(bạn, mình, mình, bạn, bạn)</td>
    <td style="padding: 10px;">(bạn, mình, bạn, mình, mình)</td>
    <td style="padding: 10px;">(bạn, mình, bạn, mình, bạn)</td>
    <td style="padding: 10px;">(bạn, mình, bạn, bạn)</td>
  </tr>
  <tr>
    <td style="padding: 10px;">(bạn, bạn, mình, mình, mình)</td>
    <td style="padding: 10px;">(bạn, bạn, mình, mình, bạn)</td>
    <td style="padding: 10px;">(bạn, bạn, mình, bạn)</td>
    <td style="padding: 10px;">(bạn, bạn, bạn)</td>
  </tr>
</table>

### Không gian mẫu

### Xác suất

### Biến cố

### Biến ngẫu nhiên

### Phân phối xác suất

## Tổng quát hóa

Để thực hiện nhiệm vụ này, chúng mình thử tập trung vào những câu hỏi dưới đây:

-   Chơi tối đa bao nhiêu vòng sẽ có người thắng toàn bộ số tiền cược?

-   Cần tối đa bao nhiêu vòng nữa để thắng toàn bộ số tiền cược nếu giả sử trò chơi được tiếp tục?

-   Chúng mình đã chơi bao nhiêu vòng trước khi dừng lại?

Cần thực hiện ít nhất 5 lần và nhiều nhất 9 lần tung đồng xu cho đến khi một mặt xuất hiện đủ 5 lần. Vì sao? Vì nếu một mặt đã xuất hiện đủ 5 lần, mặt còn lại có thể xuất hiện từ 0 đến 4 lần, số lần tung tối thiểu là $5+0=5$ và tối đa là $5+4=9$.

Trường hợp biên trên, người có điểm số cao hơn nắm ưu thế rõ ràng. Trường hợp biên dưới, người có điểm số ban đầu cao cũng có lợi thế không tương xứng.

## Thư mục

[Problem of Points](https://en.wikipedia.org/wiki/Problem_of_points)
