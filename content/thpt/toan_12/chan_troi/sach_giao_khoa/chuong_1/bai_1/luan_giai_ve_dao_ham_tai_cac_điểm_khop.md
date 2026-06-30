Để xem xét đạo hàm của hàm số đã cho tại điểm $x = 1$, trước hết cần lưu ý một hiện tượng đặc biệt: tuy công thức được viết dưới dạng phân mảnh, nhưng đồ thị của hai phần hàm lại ghép khớp hoàn hảo tại điểm nối. Cả hai nhánh đều cho giá trị $y = 1$ khi $x = 1$, đồng thời không tạo ra điểm gãy nào trên đồ thị. Nhờ đó, dù có vẻ là hai hàm khác nhau, chúng thực chất cùng tạo nên **một đồ thị duy nhất, liên tục**.

Chính sự “một đồ thị – hai công thức” này khiến cho việc xét đạo hàm tại điểm nối trở nên tế nhị. Học sinh có thể dễ dàng ngộ nhận rằng chỉ cần sử dụng công thức ứng với $x \leq 1$, tức $y = x^2$, để tính đạo hàm tại $x = 1$. Tuy nhiên, điều này không hoàn toàn chính xác, vì đạo hàm yêu cầu sự *thống nhất về cách tiếp cận điểm xét*, không chỉ từ một phía.

Để soi sáng vấn đề này, hãy tạm thời xét đến một hàm số giả lập, đặt tên là $f(x)$, có định nghĩa như sau:

    $$
        f(x) = \begin{cases}
            x^2 &\text{nếu } x < 1, \\
            2 - x &\text{nếu } x \geq 1.
        \end{cases}
    $$

Hàm số này, về mặt đồ thị, hoàn toàn trùng khớp với hàm ban đầu. Tuy nhiên, ở đây dấu bằng được đặt ở vế phải, tạo ra một tình huống đảo ngược so với ban đầu. Khi xét đạo hàm tại điểm $x = 1$ theo định nghĩa, nếu dùng công thức $y = 2 - x$, học sinh lại có thể bị dẫn đến kết luận rằng đạo hàm tại $x = 1$ là $-1$.

Chính mâu thuẫn này – cùng một đồ thị, hai cách biểu diễn công thức, hai kết quả đạo hàm khác nhau – cho thấy rõ ràng: **hàm số không thể có đạo hàm tại điểm $x = 1$**. Không thể có một hệ số góc duy nhất cho tiếp tuyến tại điểm này, vì tuỳ theo cách tiếp cận từ trái hay phải, hệ số góc tính được là khác nhau.
    
Về mặt đại số, điều này có thể giải thích như sau:

- Với nhánh bên trái ($x < 1$), $y = x^2$. Khi tiến dần đến $x = 1$, tỉ số$\frac{y(x) - 1}{x - 1}$ tiến đến $2$.
- Với nhánh bên phải ($x > 1$), $y = 2 - x$. Khi tiến dần đến $x = 1$, tỉ số$\frac{y(x) - 1}{x - 1}$ tiến đến $-1$.

Sự không thống nhất này về giới hạn từ hai phía cho thấy **không thể xác định một tiếp tuyến duy nhất tại điểm $(1; 1)$**. Về mặt hình học, nếu vẽ đồ thị, sẽ thấy không thể đặt một tiếp tuyến nào duy nhất đi qua điểm nối đó mà không vi phạm tính trơn mượt của đường cong từ một phía.

Do đó, kết luận: **Hàm số không có đạo hàm tại $x = 1$**.

===

Rất đồng tình với bạn — mình đã hơi “nhiệt tình” quá mức ở đoạn ấy, khiến vấn đề vốn đơn giản hóa thành khó hiểu hơn. Cảm ơn bạn đã nhắc, và dưới đây là phiên bản điều chỉnh: **giữ nguyên cách lý giải mạch lạc như bạn đã thích ở bản trước**, **bổ sung phần giải thích “rốt cuộc ta đã tính cái gì”** ở vị trí thích hợp, và **không đưa ra khái niệm đạo hàm bên phải cho nhánh không chứa điểm**.

---

### Luận giải

Hàm số đã cho có công thức:

\[
    y = \begin{cases}
        x^2 &\text{khi } x \leq 1, \\
        2 - x &\text{khi } x > 1.
    \end{cases}
\]

Khi khảo sát đạo hàm tại \( x = 1 \), dễ thấy đây là một điểm nối giữa hai nhánh hàm. Tuy nhiên, không như những điểm gãy thường gặp, đồ thị của hàm số tại đây hoàn toàn **liên tục** – không có gián đoạn, không có bước nhảy. Nói cách khác, tuy được định nghĩa bằng hai công thức khác nhau, hai nhánh hàm **cùng tạo nên một đồ thị duy nhất, trơn mịn về hình dạng**.

Chính vì vậy, học sinh rất dễ hiểu nhầm rằng có thể áp dụng trực tiếp đạo hàm của nhánh \( y = x^2 \) tại \( x = 1 \) để kết luận rằng đạo hàm là \( y' = 2x = 2 \). Nhưng kết luận này chỉ đúng **nếu toàn bộ hàm số được định nghĩa bởi công thức \( y = x^2 \) quanh điểm đó**. Trong bài toán này, chỉ bên trái điểm \( x = 1 \) mới tuân theo quy luật đó.

Để thấy rõ hơn sự mâu thuẫn, ta có thể xét thêm một **hàm số “giả lập”**, được xây dựng bằng cách chuyển dấu bằng từ nhánh thứ nhất sang nhánh thứ hai:

\[
    f(x) = \begin{cases}
        x^2 &\text{nếu } x < 1, \\
        2 - x &\text{nếu } x \geq 1.
    \end{cases}
\]

Đáng chú ý: **đồ thị của hàm mới này hoàn toàn trùng khớp với đồ thị ban đầu**. Không có gì thay đổi trên hình vẽ. Nhưng giờ đây, điểm \( x = 1 \) thuộc về nhánh \( 2 - x \), nên nếu dùng công thức này để tính đạo hàm tại \( x = 1 \), ta sẽ thu được kết quả là \( -1 \).

Như vậy, chỉ cần thay đổi nhỏ ở phần “dấu bằng” trong công thức hàm – **đồ thị không thay đổi, nhưng đạo hàm lại khác hẳn!**  
- Trong **hàm ban đầu**, ta tính được đạo hàm tại \( x = 1 \) bằng công thức \( x^2 \), cho kết quả là \( 2 \). Đây thực chất là đạo hàm tại điểm đó **nếu** ta chỉ xét phần bên trái.  
- Trong **hàm giả lập**, ta tính đạo hàm tại \( x = 1 \) bằng công thức \( 2 - x \), cho kết quả là \( -1 \). Đây là kết quả **nếu** ta chỉ xét phần bên phải.

Hai cách viết – một đồ thị – hai kết quả đạo hàm. Điều đó chỉ ra rằng **không thể có một tiếp tuyến duy nhất tại \( x = 1 \)**. Không có một hệ số góc nào có thể đại diện cho cả hai hướng tiến lại điểm đó.

Về hình học, điều này thể hiện rõ: nếu chỉ nhìn từ bên trái, đồ thị giống như một parabol, có tiếp tuyến dốc lên với hệ số góc 2. Nếu nhìn từ bên phải, đồ thị là một đường thẳng đi xuống, với hệ số góc \( -1 \). Không thể tìm ra một đường duy nhất vừa tiếp xúc parabol bên trái, vừa nằm trùng với đường thẳng bên phải.

Về đại số, điều đó cũng được phản ánh trong tỉ số \(\frac{y(x) - 1}{x - 1}\), vốn là công cụ để tìm đạo hàm. Khi \( x \to 1^- \), biểu thức này tiến tới 2; còn khi \( x \to 1^+ \), biểu thức lại tiến tới \( -1 \). Do giới hạn từ hai phía không bằng nhau, nên giới hạn tổng thể không tồn tại, và do đó, đạo hàm tại \( x = 1 \) **không tồn tại**.

---

Nếu bạn muốn, mình có thể viết thêm một đoạn nhẹ nhàng kiểu "văn crush" để khơi gợi tò mò của học sinh trước khi bước vào phần nghiêm túc như trên. Hoặc ngắn gọn hơn một chút nếu bạn muốn đưa vào sách giáo khoa mini.

===

Tuyệt, vậy mình sẽ nối mạch từ đoạn mở đầu mang tính khơi gợi ấy vào phần giải thích nghiêm túc, sao cho dòng chảy không bị đứt mà vẫn giữ hai phong cách riêng biệt — một đoạn như lời thì thầm, một đoạn như ánh sáng soi chiếu. Cấu trúc sẽ gồm:

1. **Mở đầu khơi gợi (văn crush)**
2. **Chuyển nhẹ sang lý giải hình học**
3. **Tiếp nối bằng lập luận đại số**
4. **Tổng kết lại bản chất đạo hàm tại điểm nối**

---

> **Có bao giờ một cái nhìn đến từ hai phía lại cho hai cảm nhận hoàn toàn khác nhau?**  
> Từ bên trái, đồ thị lượn cong như một nét cọ mềm mại đi lên, để rồi bất ngờ, bên phải lại là một đường thẳng lạnh lùng đi xuống.  
>  
> Vậy thì... nếu muốn vẽ tiếp tuyến tại đúng nơi hai thế giới chạm nhau — điểm \( x = 1 \) — có thể nào chỉ vẽ **một** đường thẳng duy nhất không?  
>  
> Một đường vừa chạm được đường cong phía trái, lại vừa khẽ lướt qua đường thẳng phía phải?  
>  
> Hãy thử dừng lại thật lâu ở điểm nối ấy, thử lùi lại nhìn cả hai hướng, rồi xem: liệu có một con đường duy nhất xứng đáng là tiếp tuyến? Hay tất cả chỉ là ảo ảnh khi nhìn từ một phía?

---

**Bây giờ, hãy nhìn vấn đề từ góc độ hình học.**  
Đồ thị hàm số  
\[
y = \begin{cases}
x^2 & \text{khi } x \leq 1, \\
2 - x & \text{khi } x > 1
\end{cases}
\]  
là một đường cong nối với một đường thẳng tại điểm \( (1,1) \). Nếu chỉ nhìn vào hình vẽ, ta thấy đồ thị liên tục – không đứt đoạn – nhưng khi đặt câu hỏi: *"Có thể vẽ tiếp tuyến duy nhất tại đó không?"*, thì chuyện trở nên tinh tế hơn.

Từ bên trái, nhánh \( y = x^2 \) tiến đến điểm \( x = 1 \) theo một đường cong có tiếp tuyến là đường thẳng dốc \( 2 \). Từ bên phải, nhánh \( y = 2 - x \) lại là một đường thẳng với dốc cố định là \( -1 \). Không thể có **một** đường thẳng duy nhất vừa có độ dốc bằng 2 (từ trái), vừa có độ dốc bằng -1 (từ phải). Điều này cho thấy: không thể có tiếp tuyến duy nhất tại điểm nối ấy.

---

**Về mặt đại số**, ta sẽ xác minh bằng cách xây dựng hai hàm số khác nhau:

- **Hàm A** là hàm ban đầu:  
  \[
  y_A = \begin{cases}
  x^2 & \text{khi } x \leq 1, \\
  2 - x & \text{khi } x > 1.
  \end{cases}
  \]
  Với hàm này, \( x = 1 \) thuộc nhánh thứ nhất nên có thể tính đạo hàm tại đó bằng công thức \( y' = 2x \), suy ra:  
  \[
  y'_A(1) = 2.
  \]
  Đây chính là đạo hàm bên **trái** – đo độ dốc đồ thị tiến đến từ bên trái điểm \( x = 1 \).

- **Hàm B** là phiên bản giả lập, đảo ngược điều kiện để \( x = 1 \) thuộc nhánh thứ hai:  
  \[
  y_B = \begin{cases}
  x^2 & \text{khi } x < 1, \\
  2 - x & \text{khi } x \geq 1.
  \end{cases}
  \]
  Với hàm này, \( x = 1 \) thuộc nhánh \( y = 2 - x \), nên đạo hàm tại đó là:  
  \[
  y'_B(1) = -1.
  \]
  Đây là đạo hàm bên **phải** – phản ánh độ dốc khi tiến vào điểm \( x = 1 \) từ phía lớn hơn.

Hai đạo hàm, hai độ dốc, và không trùng nhau. Như vậy, đạo hàm tại \( x = 1 \) **không tồn tại**, vì muốn có đạo hàm thì phải có cùng một tiếp tuyến nhìn từ cả hai phía.

---

**Kết luận.**  
Hai hàm A và B tuy có đồ thị giống hệt nhau, nhưng khi hỏi về đạo hàm tại điểm nối – nơi hai thế giới chạm nhau – thì lại cho hai đáp án khác biệt. Điều này cho thấy, chỉ cần thay đổi cách **gán công thức tại một điểm**, bản chất đạo hàm có thể thay đổi hoàn toàn. Vì vậy, hàm ban đầu **không có đạo hàm tại \( x = 1 \)**, dù đồ thị vẫn liền mạch như chưa từng có gì chia cắt.

---

Bạn thấy mạch như vậy ổn chưa? Có cần mình tách phần hình học và đại số rõ ràng hơn nữa không? Hoặc nếu bạn muốn lùi lại một chút để biến phần mở đầu thành *Hoạt động khám phá* riêng rồi bắt đầu lại phần giải thích sau cũng được nhé.

