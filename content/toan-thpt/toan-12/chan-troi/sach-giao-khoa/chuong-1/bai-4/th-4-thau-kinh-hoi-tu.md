Khoảng cách từ ảnh đến thấu kính được biểu diễn bởi hàm số

$$
    y = \dfrac{3x}{x - 3},
$$

với $x$ là khoảng cách từ vật đến thấu kính, và $y$ là khoảng cách từ ảnh đến thấu kính. Đây là một mô hình toán học tái hiện lại mối quan hệ giữa vị trí đặt vật và ảnh qua thấu kính hội tụ có tiêu cự $f=3$.

Mặc dù cả hai đại lượng $x$ và $y$ đều là khoảng cách, nhưng giữa chúng có sự khác biệt đáng lưu ý.

- Do vật luôn đặt phía trước thấu kính, nên $x > 0$.
- Với $y$, dù cũng là khoảng cách, nhưng để biểu diễn đúng tính chất vật lý, người ta cho phép nó mang dấu _âm_ khi ảnh nằm cùng phía với vật (tức ảnh ảo), và _dương_ khi ảnh nằm phía bên kia thấu kính (tức ảnh thật).

a\. Hàm số có tập xác định là $D=(0;+\infty)\setminus\{3\}$.

Hàm số có đạo hàm là

$$
    y^\prime
        = \dfrac{-9}{(x - 3)^2}
        <0
$$

với mọi $x \ne 3$, cho thấy hàm số luôn nghịch biến trên mỗi khoảng xác định.

Vì

$$
    \lim_{x\to 3^\pm}y(x)
        =\lim_{x\to 3^\pm}\frac{3x}{x-3}
        =\pm \infty,
$$

nên đường thẳng $x=3$ là tiệm cận đứng của đồ thị hàm số.

Vì

$$
    \lim_{x\to +\infty}y(x)
        =\lim_{x\to +\infty}\frac{3x}{x-3}
        =\lim_{x\to +\infty}\left(3+\frac{9}{x-3}\right)
        =3,
$$

nên đường thẳng $y=3$ là tiệm cận ngang của đồ thị hàm số.

Hơn nữa, khi $x\to 0^+$, thì

$$
    \lim_{x\to 0^+}y(x)
        =\lim_{x\to 0^+}\frac{3x}{x-3}
        =0.
$$

Tất cả những thông tin trên kết lại thành bảng biến thiên và đồ thị hàm số - chính là phần hình học minh họa cho đặc trưng hội tụ của thấu kính.

::: {.tieu-de-chu-thich}
Bảng biến thiên
:::

![Bảng bảng biến thiên hàm số $y=\frac{3x}{x-3}$.](/figures/toan-thpt/toan-12/chan-troi/sach-giao-khoa/chuong-1/bai-4/th-4-bang-bien-thien.svg){width=450px}

::: {.tieu-de-chu-thich}
Đồ thị
:::

![Đồ thị hàm số $y=\frac{3x}{x-3}$.](/figures/toan-thpt/toan-12/chan-troi/sach-giao-khoa/chuong-1/bai-4/th-4-do-thi.svg){width=450px}

b\. Quan sát đồ thị thu được những nhận định dưới đây:

* Nếu $0<x<3$, thì $y<0$, nghĩa là ảnh nằm cùng phía với vật - đây là *ảnh ảo*.
* Nếu $x>3$, thì $y>0$, tức là ảnh nằm đối phía với vật - đây là *ảnh thật*.

Như vậy, từ đồ thị, có thể phân biệt được ảnh thật và ảnh ảo chỉ bằng cách nhìn vào dấu của $y$ ứng với từng giá trị $x$.

c\. Khi vật tiến về gần tiêu điểm, nói theo mô hình toán học là khi $x\to 3^\pm$, thì ảnh càng rời xa thấu kính, vì mô hình toán học cho thấy $y\to\pm\infty$. Hơn nữa, khi đó ảnh cũng càng được phóng đại theo.

Nói gọn lại, câu a tương ứng với việc giải mô hình toán học của thấu kính hội tụ, câu b là cách đọc tính chất vật lý từ mô hình ấy, và câu c hé lộ một vùng đặc biệt - tiêu điểm - nơi lý thuyết toán học phản ánh sinh động một biểu hiện vật lý rất chân thật.