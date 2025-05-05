Trong chương trình phổ thông, học sinh được học rằng phương trình bậc hai $ax^2 + bx + c = 0$ có nghiệm hay không được quyết định bởi biểu thức quen thuộc 

$$
    \Delta = b^2 - 4ac.
$$

- Khi $\Delta < 0$, phương trình vô nghiệm.
- Khi $\Delta = 0$, phương trình có nghiệm kép.
- Khi $\Delta > 0$, phương trình có hai nghiệm phân biệt. 

Tuy nhiên, có bao giờ bạn tự hỏi: **Tại sao biểu thức này lại xuất hiện? Tại sao lại là nó mà không phải một thứ gì khác?**

Câu trả lời nằm ở một kỹ thuật đại số cổ điển nhưng rất mạnh mẽ - *đưa về bình phương* (tiếng Anh: *completing the square*). Đây là một thao tác biến đổi biểu thức thành bình phương của một nhị thức, từ đó làm hiện rõ cấu trúc của bài toán. Hãy cùng lần theo con đường này để khám phá sự ra đời của biệt thức $\Delta$.

Xuất phát từ phương trình bậc hai tổng quát

$$
    ax^2 + bx + c = 0,
$$

giả sử $a \ne 0$ để đảm bảo đây thực sự là một phương trình bậc hai. Chia hai vế cho $a$, thu được phương trình 

$$
x^2 + \frac{b}{a}x + \frac{c}{a} = 0.
$$

Mục tiêu lúc này là biến đổi vế trái thành một bình phương hoàn chỉnh. Để làm được điều đó, bạn có nhận ra rằng:

$$
x^2 + \frac{b}{a}x = x^2 + 2 \cdot \frac{b}{2a} \cdot x,
$$

và biểu thức này gợi ý nên cộng và trừ thêm $\left( \frac{b}{2a} \right)^2$ để có đủ một bình phương. Khi đó,

$$
    \begin{aligned}
        x^2 + \frac{b}{a}x + \frac{c}{a}
            &= \left( x + \frac{b}{2a} \right)^2 - \left( \frac{b}{2a} \right)^2 + \frac{c}{a} \\
            &= \left( x + \frac{b}{2a} \right)^2 + \frac{4ac - b^2}{4a^2}.
    \end{aligned}
$$

Phương trình ban đầu trở thành

$$
\left( x + \frac{b}{2a} \right)^2 = \frac{b^2 - 4ac}{4a^2}.
$$

Chính ở bước này, biệt thức $\Delta = b^2 - 4ac$ xuất hiện một cách hoàn toàn tự nhiên, như là phần còn lại sau khi vế trái được biến đổi thành bình phương. Hơn thế, cách biến đổi này còn giúp lý giải vì sao $\Delta$ có vai trò quyết định số nghiệm của phương trình: vì vế trái là một bình phương, thứ luôn lớn hơn hoặc bằng 0, nên để phương trình có nghiệm, vế phải cũng phải không âm. Từ đó, các trường hợp phân biệt nghiệm của phương trình cũng được phân tích rất rõ ràng.

Không dừng lại ở việc giải phương trình, kỹ thuật đưa về bình phương còn là công cụ mạnh mẽ khi cần **xét dấu biểu thức bậc hai**. Xét biểu thức

$$
    f(x) 
        = ax^2 + bx + c.
$$

Đưa về bình phương, tương tự như đã làm khi giải phương trình bậc hai tổng quát,

$$
    f(x) 
        = a \left( x + \frac{b}{2a} \right)^2 - \frac{\Delta}{4a}.
$$

Từ dạng này, dấu của $f(x)$ trở nên dễ quan sát hơn:  

- Nếu $\Delta < 0$, $f(x)$ luôn cùng dấu với $a$.
    
    Thật vậy, vì $\left(x+\frac{b}{2a}\right)^2 \geq 0$ với mọi $x$, nên $f(x)$ không thể nhận giá trị bằng 0. Do đó $f(x)$ luôn dương nếu $a>0$, và luôn âm nếu $a<0$. 

- Nếu $\Delta = 0$, $f(x)$ cùng dấu với $a$ và bằng 0 tại $x=-\frac{b}{2a}$.
    
    Thật vậy, khi đó $f(x)$ trở thành
    
    $$
        f(x)
            =a\left(x+\frac{b}{2a}\right)^2,
    $$

    là một bình phương thực sự. Từ đây, dễ thấy $f(x)\geq 0$ nếu $a>0$, $f(x)\leq0$ nếu $a<0$, và bằng 0 tại đúng điểm $x=-\frac{b}{2a}$. Đây chính là *nghiệm kép* của phương trình.

- Nếu $\Delta>0$, $f(x)$ cùng dấu với $a$ với mọi $x<\frac{-b-\sqrt{\Delta}}{2a}$ và $x>\frac{-b+\sqrt{\Delta}}{2a}$; $f(x)$ trái dấu với $a$ với mọi $\frac{-b-\sqrt{\Delta}}{2a}<x<\frac{-b+\sqrt{\Delta}}{2a}$; và $f(x)$ tại $x=\frac{-b\pm\sqrt{\Delta}}{2a}$.

    Thật vậy,...

So với cách dùng công thức nghiệm rồi lập bảng xét dấu, cách viết lại bằng bình phương đôi khi nhanh gọn và trực quan hơn, nhất là trong các bài toán chứng minh bất đẳng thức, xét tính đồng biến - nghịch biến hay xác định cực trị.

Tóm lại, phương pháp **đưa về bình phương** không chỉ giúp bạn hiểu sâu hơn về cách giải phương trình bậc hai và nguồn gốc của biệt thức $\Delta$, mà còn mở ra nhiều hướng phân tích tinh tế trong các bài toán khảo sát hàm số và biến đổi đại số. Đây chính là một trong những kỹ thuật nền tảng mà bất kỳ học sinh nào cũng nên làm chủ, như một viên gạch đầu tiên trên hành trình học toán lâu dài và bền vững.