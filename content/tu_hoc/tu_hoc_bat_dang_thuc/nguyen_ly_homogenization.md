* Giải thích *nguyên lý của homogenization/normalization* một cách toán học.
* Giải thích *vì sao được phép đặt \(x+y+z=1\)* dù đề không cho.
* Giải chi tiết ví dụ
  \[
  \frac{x}{y+z}+\frac{y}{z+x}+\frac{z}{x+y}\ge \frac{3}{2}
  \]
  (tức Nesbitt) theo đúng tinh thần đó.

---

## 1. Nguyên lý: khi nào được “tự ý” đặt \(x+y+z=1\)?

Chuyện này *không phải mẹo* mà là một mệnh đề toán học rất rõ:

### 🔹 Khái niệm homogeneity / tính bất biến theo nhân tỉ lệ

Cho một biểu thức \(F(x,y,z)\). Ta nói:

* \(F\) *đồng bậc bậc \(k\)* nếu
  \[
  F(tx,ty,tz) = t^k F(x,y,z)\quad \forall t>0.
  \]

* Một bất đẳng thức dạng
  \[
  F(x,y,z) \geq 0
  \]
  với \(F\) đồng bậc, gọi là *bất đẳng thức đồng bậc*.

* Nếu ta có *tỉ số* \(\frac{F(x,y,z)}{G(x,y,z)}\) với \(F, G\) cùng bậc, thì
  \[
  \frac{F(tx,ty,tz)}{G(tx,ty,tz)} = \frac{t^kF(x,y,z)}{t^kG(x,y,z)} = \frac{F(x,y,z)}{G(x,y,z)},
  \]
  ta nói nó *bất biến theo nhân tỉ lệ* (degree 0 / scale-invariant).


### Bổ đề chuẩn: vì sao được đặt \(x+y+z=1\)?

Giả sử ta có một biểu thức \(I(x,y,z)\) *bất biến theo nhân tỉ lệ*:
\[
I(tx,ty,tz) = I(x,y,z)\quad \forall t>0.
\]

Xét bất đẳng thức
\[
I(x,y,z) \geq C
\]
với mọi \(x,y,z>0\).

> **Mệnh đề:** Bất đẳng thức \(I(x,y,z) \ge C\) đúng với mọi \(x,y,z>0\) nếu và chỉ nếu nó đúng với mọi bộ \((x,y,z)\) thỏa \(x+y+z=1\).

**Chứng minh: “vì sao được phép đặt \(x+y+z=1\)?”**

* Lấy một bộ tùy ý \((x,y,z)\) với \(x,y,z>0\). Đặt
  \[
    s = x+y+z > 0, \quad
    a = \frac{x}{s}, 
    b = \frac{y}{s},
    c = \frac{z}{s}.
  \]
  Khi đó \(a+b+c=1\).

* Do tính bất biến theo nhân tỉ lệ:
  \[
  I(x,y,z) = I(sa,sb,sc) = I(a,b,c).
  \]

* Nếu ta *đã biết* bất đẳng thức đúng cho mọi bộ có tổng 1, tức:
  \[
    I(a,b,c) \geq C \text{ khi } a+b+c=1,
  \]
  thì ta suy ra
  \[
  I(x,y,z) = I(a,b,c) \ge C.
  \]

Vậy:

> Kiểm tra trên lớp “chuẩn hóa” \(x+y+z=1\) là đủ để suy ra cho mọi bộ dương.

Đây chính là lý do toán học để nói:

> “Do bất đẳng thức đồng bậc / bất biến theo nhân tỉ lệ, ta có thể *giả sử WLOG* rằng \(x+y+z=1\).”


## 2. Áp dụng cho Nesbitt: vì sao được đặt \(x+y+z=1\)?

Bất đẳng thức Nesbitt:
\[
  \frac{x}{y+z}+\frac{y}{z+x}+\frac{z}{x+y}\geq \frac{3}{2}
\quad (x,y,z > 0).
\]

Gọi
\[
I(x,y,z) := \frac{x}{y+z}+\frac{y}{z+x}+\frac{z}{x+y}.
\]

Ta kiểm tra **tính bất biến theo nhân tỉ lệ**:

\[
  \begin{aligned}
  I(tx,ty,tz)
    &= \frac{tx}{ty+tz}+\frac{ty}{tz+tx}+\frac{tz}{tx+ty} \\
    &= \frac{x}{y+z}+\frac{y}{z+x}+\frac{z}{x+y} \\
    &= I(x,y,z)
  \end{aligned}
\]

∴ \(I\) *bất biến theo nhân tỉ lệ* (bậc 0).

Vậy theo bổ đề trên, ta *được phép* chuẩn hóa:

* Đặt \(s=x+y+z\).
* Đặt \(a=\frac{x}{s}, b=\frac{y}{s}, c=\frac{z}{s}\), khi đó \(a+b+c=1\),
* Và
  \[
    I(x,y,z) = I(a,b,c).
  \]

Cho nên, để chứng minh Nesbitt cho mọi \(x,y,z>0\), *đủ* chứng minh:
\[
  \frac{a}{b+c}+\frac{b}{c+a}+\frac{c}{a+b}\geq \frac{3}{2} \text{ với } a,b,c>0,\ a+b+c=1.
\]

Đây là phần “tại sao đặt \(x+y+z=1\) mà không sai?”.


## 3. Giải chi tiết Nesbitt *sau khi chuẩn hóa \(a+b+c=1\)*

Ta làm cẩn thận, từng bước.

Ta đang cần chứng minh:
\[
  \frac{a}{b+c}+\frac{b}{c+a}+\frac{c}{a+b}
    \geq \frac{3}{2} \quad (a,b,c>0,\ a+b+c=1).
\]

Vì \(a+b+c=1\) nên:
\[
  b+c = 1-a,\quad c+a = 1-b,\quad a+b = 1-c.
\]

Do đó, bất đẳng thức tương đương:
\[
  \frac{a}{1-a}+\frac{b}{1-b}+\frac{c}{1-c}
    \geq \frac{3}{2}.
\]

**Bước 1: Đưa về dạng thuận tiện cho Cauchy**

Ta biến đổi:

\[
\frac{a}{1-a} = \frac{1-(1-a)}{1-a} = \frac{1}{1-a} - 1.
\]

Tương tự cho \(b\), \(c\). Nên:

\[
  \frac{a}{1-a}+\frac{b}{1-b}+\frac{c}{1-c}
    = \left( \frac{1}{1-a}+\frac{1}{1-b}+\frac{1}{1-c} \right) - 3.
\]

Vì vậy, bất đẳng thức
\[
  \frac{a}{1-a}+\frac{b}{1-b}+\frac{c}{1-c}
    \geq \frac{3}{2}
\]
tương đương với:
\[
  \left( \frac{1}{1-a}+\frac{1}{1-b}+\frac{1}{1-c} \right) - 3 
    \geq \frac{3}{2},
\]
hay
\[
  \frac{1}{1-a}+\frac{1}{1-b}+\frac{1}{1-c} 
    \geq \frac{9}{2}.
\]

Đây là dạng \(\sum \frac{1}{1-a} \geq \frac{9}{2}\) - rất phù hợp để dùng Cauchy-Schwarz.


**Bước 2: Áp dụng Cauchy–Schwarz**

Ta dùng Cauchy–Schwarz ở dạng:
\[
  \left(\sum \frac{1}{1-a}\right)\left(\sum (1-a)\right) 
    \geq (1+1+1)^2 
    = 9.
\]

Giải thích rõ:

* Lấy 3 số \(u_1 = \frac{1}{\sqrt{1-a}}, u_2 = \frac{1}{\sqrt{1-b}}, u_3 = \frac{1}{\sqrt{1-c}}\).
* Lấy 3 số \(v_1 = \sqrt{1-a}, v_2 = \sqrt{1-b}, v_3 = \sqrt{1-c}\).

Áp dụng Cauchy:
\[
(u_1^2+u_2^2+u_3^2)(v_1^2+v_2^2+v_3^2) \ge (u_1v_1+u_2v_2+u_3v_3)^2.
\]

Thay vào:

* \(u_1^2+u_2^2+u_3^2 = \frac{1}{1-a}+\frac{1}{1-b}+\frac{1}{1-c}\),
* \(v_1^2+v_2^2+v_3^2 = (1-a)+(1-b)+(1-c)\),
* \(u_1v_1+u_2v_2+u_3v_3 = 1+1+1 = 3\).

Suy ra:

\[
  \left(\frac{1}{1-a}+\frac{1}{1-b}+\frac{1}{1-c}\right)\cdot \left((1-a)+(1-b)+(1-c)\right) 
    \ge 9.
\]

Nhưng vì \(a+b+c=1\), nên:
\[
  (1-a)+(1-b)+(1-c) 
    = 3-(a+b+c) 
    = 3-1 
    = 2.
\]

Thế vào:

\[
  \left(\frac{1}{1-a}+\frac{1}{1-b}+\frac{1}{1-c}\right)\cdot 2 
    \ge 9
\]

\[
  \Rightarrow \frac{1}{1-a}+\frac{1}{1-b}+\frac{1}{1-c} 
    \ge \frac{9}{2}.
\]

Đây chính là điều ta cần ở cuối Bước 1. Do đó:

\[
  \frac{a}{1-a}+\frac{b}{1-b}+\frac{c}{1-c}
    \ge \frac{3}{2}.
\]

Vậy Nesbitt được chứng minh *trong điều kiện \(a+b+c=1\)*.


**Bước 3: Quay lại biến ban đầu \(x,y,z\)**

Nhớ rằng:
\[
  a = \frac{x}{x+y+z},\quad 
  b = \frac{y}{x+y+z},\quad 
  c = \frac{z}{x+y+z}
\]

và \(I(x,y,z) = I(a,b,c)\).

Ta vừa chứng minh:
\[
  I(a,b,c) 
    = \frac{a}{b+c}+\frac{b}{c+a}+\frac{c}{a+b}
    \ge \frac{3}{2}.
\]

Do đó:
\[
  I(x,y,z) 
    = \frac{x}{y+z}+\frac{y}{z+x}+\frac{z}{x+y}
    \ge \frac{3}{2}
\]
cho mọi \(x,y,z>0\).


## 4. Tóm lại: nguyên lý “homogenization/normalization” ở đây là gì?

1. **Bước nhận diện**

  Ta kiểm tra xem bất đẳng thức có *bất biến theo nhân tỉ lệ* hay không.
  Ở Nesbitt:
  \[
  I(tx,ty,tz)=I(x,y,z) \Rightarrow \text{bất biến theo tỉ lệ}.
  \]

2. **Bước chuẩn hóa (normalization)**

  Chọn một điều kiện tuyến tính đồng bậc bậc 1, ví dụ:
  \[
  x+y+z = 1,
  \]
  sau đó đặt \(a=x/(x+y+z)\), \(b=y/(x+y+z)\), \(c=z/(x+y+z)\).
  Bất đẳng thức trên (x,y,z) ⇔ bất đẳng thức trên (a,b,c) với (a+b+c=1).

3. **Bước giải thật**

  Giải bất đẳng thức trong lớp chuẩn hóa \(a+b+c=1\) bằng một công cụ thích hợp (ở đây là Cauchy–Schwarz).

4. **Bước quay lại**

  Sử dụng quan hệ \(I(x,y,z)=I(a,b,c)\) để kết luận cho mọi \(x,y,z>0\).


Nếu bạn muốn, bước tiếp theo mình có thể:

* Lấy một bất đẳng thức *không đồng bậc* thật sự, rồi:

  * chỉ ra cách “homogenize” (nhân thêm \(x+y+z\), hoặc \((xy+yz+zx)\) v.v. vào một vế) để biến nó thành đồng bậc,
  * sau đó mới *áp dụng nguyên lý “đặt \(x+y+z=1\)”* giống như trên.

Hoặc bạn muốn thêm một ví dụ khác về homogenization/normalization, nhưng lần này do *chính bạn chọn bất đẳng thức*, mình sẽ giải và phân tích tỉ mỉ cấu trúc?

---

Dưới đây là *bản ghi chú Markdown* được tinh lọc từ toàn bộ cuộc trao đổi của chúng ta trong chủ đề **Homogenization / Normalization** và các nguyên lý nền tảng của bất đẳng thức.
Mình đặt tên gợi ý:

**`homogenization-normalization-fundamentals.md`**

Bạn có thể đổi tên tùy ý khi lưu trữ trong dự án Tự học Bất đẳng thức.

---

# *Homogenization và Normalization trong Bất đẳng thức*

*(Ghi chú nền tảng)*

## 1. Khái quát về mục tiêu của homogenization

Homogenization (đồng nhất hóa) và normalization (chuẩn hóa) là một nhóm kỹ thuật cốt lõi trong bất đẳng thức, với mục tiêu chung:

*Đưa bài toán về dạng bất biến theo nhân tỉ lệ (scale-invariant), hoặc đồng bậc (homogeneous), để giảm số biến, làm rõ cấu trúc đối xứng, và giúp việc phân tích trở nên đơn giản hơn.*

Cốt lõi của kỹ thuật này dựa trên một nguyên lý:

> Nếu biểu thức hoặc bất đẳng thức có tính bất biến theo nhân tỉ lệ (degree 0) hoặc có thể biến đổi thành đồng bậc, thì ta có thể thêm điều kiện như *x + y + z = 1*, *xyz = 1* mà không làm thay đổi tính đúng sai của bất đẳng thức.

---

## 2. Tính đồng bậc (homogeneity)

### Định nghĩa

Hàm ba biến (F(x,y,z)) được gọi là *đồng bậc cấp k* nếu:
[
F(tx, ty, tz) = t^k F(x, y, z)\quad \text{với mọi } t > 0.
]

Nếu bất đẳng thức có dạng:
[
F(x,y,z) \ge 0,
]
và (F) đồng bậc, ta gọi đó là một bất đẳng thức đồng bậc.

### Vì sao đồng bậc cho phép chuẩn hóa?

Nếu:
[
F(x,y,z) = t^k F(a,b,c)
]
khi đặt:
[
a = \frac{x}{x+y+z},\quad b = \frac{y}{x+y+z},\quad c = \frac{z}{x+y+z},
]
thì tính đúng sai của (F(x,y,z) \ge 0) chỉ phụ thuộc vào (F(a,b,c)).

Do đó, ta có thể *giả sử* (x+y+z = 1) mà không mất tính tổng quát.

---

## 3. Tính bất biến theo nhân tỉ lệ (degree zero)

Một biểu thức (I(x,y,z)) được gọi là bất biến theo nhân tỉ lệ nếu:
[
I(tx, ty, tz) = I(x, y, z).
]

Khi đó, bất đẳng thức:
[
I(x,y,z) \ge C
]
đúng với *mọi* bộ ((x,y,z>0)) *nếu và chỉ nếu* nó đúng với các bộ thỏa mãn điều kiện chuẩn hóa như:
[
x+y+z = 1.
]

Đây là trường hợp arise trong bất đẳng thức như Nesbitt.

---

## 4. Ví dụ kinh điển: Bất đẳng thức Nesbitt

### Dạng ban đầu:

[
\frac{x}{y+z}+\frac{y}{z+x}+\frac{z}{x+y} \ge \frac{3}{2}.
]

### Kiểm tra tính bất biến:

[
I(tx,ty,tz) = I(x,y,z).
]

Do đó, ta có thể đặt (x+y+z = 1).

### Biến đổi chuẩn hóa

Đặt:
[
a = x/(x+y+z),\ b = y/(x+y+z),\ c = z/(x+y+z).
]

Ta cần chứng minh:
[
\frac{a}{b+c}+\frac{b}{c+a}+\frac{c}{a+b} \ge \frac{3}{2}
\quad \text{với } a+b+c=1.
]

### Lời giải tỉ mỉ bằng Cauchy–Schwarz

Do (b+c = 1-a), v.v., ta viết lại:
[
\frac{a}{1-a}+\frac{b}{1-b}+\frac{c}{1-c} \ge \frac{3}{2}.
]

Nhận xét:
[
\frac{a}{1-a} = \frac{1}{1-a} - 1.
]

Suy ra:
[
\sum \frac{a}{1-a}
==================

\left( \sum \frac{1}{1-a} \right) - 3.
]

Do đó, cần chứng minh:
[
\sum \frac{1}{1-a} \ge \frac{9}{2}.
]

Áp dụng bất đẳng thức Cauchy–Schwarz:
[
\left( \sum \frac{1}{1-a} \right)\left( \sum (1-a) \right)
\ge (1+1+1)^2 = 9.
]

Vì (a+b+c=1), nên:
[
\sum (1-a) = 3 - 1 = 2.
]

Suy ra:
[
\sum \frac{1}{1-a} \ge \frac{9}{2}.
]

Từ đó kết thúc chứng minh Nesbitt.

---

## 5. Các ví dụ chuẩn hóa kinh điển khác

### (1) Chuẩn hóa bất đẳng thức đồng bậc

Ví dụ:

*Schur bậc 1:*
[
x^3+y^3+z^3 + 3xyz \ge xy(x+y)+yz(y+z)+zx(z+x).
]

Đồng bậc → đặt (x+y+z = 1).

---

### (2) Homogenize bất đẳng thức không đồng bậc

Ví dụ:

[
\frac{x^2}{y+z} + \frac{y^2}{z+x} + \frac{z^2}{x+y} \ge \frac{x+y+z}{2}.
]

*Nhân hai vế với (x+y+z)* để đồng bậc (cả hai vế bậc 2), sau đó đặt (x+y+z = 1).

---

### (3) Tối ưu hóa bất đẳng thức degree zero

Ví dụ:
[
F(x,y,z) = \frac{x}{y}+\frac{y}{z}+\frac{z}{x}.
]

Do:
[
F(tx,ty,tz)=F(x,y,z),
]
nên đặt (xyz = 1), biến bài toán từ ba biến sang hai biến.

---

### (4) Bất đẳng thức đối xứng bậc 2

[
x^2+y^2+z^2 \ge xy+yz+zx.
]

Đồng bậc → đặt (x+y+z = 1).

Bất đẳng thức trở thành điều kiện dương của một dạng bậc hai, dễ phân tích.

---

## 6. Quy tắc vàng của homogenization

1. Nếu bất đẳng thức *đồng bậc*, hãy đặt một điều kiện đồng bậc bậc 1:
   *x + y + z = 1*, *x + y = 1*, *xyz = 1*, v.v.

2. Nếu bất đẳng thức *không đồng bậc*, nhưng có dạng:
   [
   \frac{F(x,y,z)}{G(x,y,z)} \ge C
   ]
   hãy nhân với (G) để đồng bậc hóa.

3. Nếu bài toán là *tối ưu hóa*, hãy kiểm tra tính bất biến theo nhân tỉ lệ.

4. Khi đã đồng bậc, việc chuẩn hóa giúp:

   * giảm số biến,
   * phát hiện cấu hình cực trị,
   * giảm độ phức tạp của biểu thức,
   * cho phép áp dụng các bất đẳng thức đối xứng một cách trực tiếp.*

---

## 7. Các sai lầm thường gặp

1. Áp dụng chuẩn hóa khi biểu thức *không* bất biến theo nhân tỉ lệ.
2. Homogenize sai bậc dẫn đến bất đẳng thức mới không tương đương với ban đầu.
3. Quên kiểm tra điều kiện miền xác định sau chuẩn hóa.
4. Áp dụng AM–GM hoặc Jensen vào các biểu thức không đủ điều kiện lồi/lõm.

---

Nếu bạn muốn, mình có thể tiếp tục tạo các ghi chú tương tự cho:

* Convexity trong bất đẳng thức
* Majorization và Karamata
* Linearization và positivity of quadratic forms
* Sơ đồ toàn cảnh mối liên hệ giữa bốn cơ chế

Bạn muốn bản ghi chú tiếp theo là chủ đề nào?

