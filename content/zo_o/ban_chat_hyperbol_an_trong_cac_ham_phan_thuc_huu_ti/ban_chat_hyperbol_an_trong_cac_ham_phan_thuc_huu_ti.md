# LUẬN ĐỀ TOÁN HỌC: BẢN CHẤT HYPERBOL ẨN TRONG CÁC HÀM PHÂN THỨC HỮU TỈ

> **Tác giả:** [Tên của bạn]  
> **Mục đích:** Tài liệu lưu trữ phục vụ viết luận học thuật và xây dựng kịch bản video Manim (3Blue1Brown style).  
> **Ý tưởng cốt lõi:** Phá vỡ "điểm mù trực giác" bằng cách chứng minh đồ thị hàm phân thức (bậc 1/bậc 1 và bậc 2/bậc 1) thực chất chính là đường Hyperbol chính tắc bị dịch tâm và xoay nghiêng qua phép dời hình (Isometry).

---

## PHẦN I: ĐẶT VẤN ĐỀ & TRIẾT HỌC TOÁN HỌC

### 1. Điểm mù của hình học phẳng phổ thông

Trong chương trình phổ thông, học sinh được tiếp cận Hyperbol qua hai thế giới hoàn toàn tách biệt:

- **Thế giới Conic (Hình học giải tích):** Phương trình chính tắc $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$. Đồ thị đứng thẳng, nhận các trục tọa độ làm trục đối xứng.
- **Thế giới Hàm số (Đại số & Giải tích):** Hàm bậc nhất/bậc nhất $y = \frac{ax+b}{cx+d}$ hoặc bậc hai/bậc nhất $y = \frac{ax^2+bx+c}{px+q}$. Đồ thị nằm nghiêng, né trục tọa độ, có các đường tiệm cận chéo.

Sự phân mảnh này tạo ra một ảo ảnh thị giác khiến đại đa số người học tin rằng đây là các loại đồ thị khác nhau.

### 2. Nguyên lý "Vật thể và Thước đo"

- **Bản chất hình học nội tại (Intrinsic Geometry):** Hình dạng, độ cong, khoảng cách giữa các tiêu điểm, góc giữa các đường tiệm cận của vật thể là **bất biến tuyệt đối**.
- **Biểu thức đại số ngoại tại (Extrinsic Algebra):** Phương trình của đường cong phức tạp hay đơn giản phụ thuộc hoàn toàn vào vị trí ta đặt chiếc thước đo (Hệ trục tọa độ $Oxy$) so với vật thể.
- **Chính tắc hóa (Canonicalization):** Là quá trình xoay và dịch chuyển hệ trục tọa độ sao cho gốc tọa độ trùng với tâm đối xứng, và các trục tọa độ trùng với trục đối xứng của vật thể. Khi thước đo đặt ngay ngắn, phương trình phức tạp sẽ tự động co về dạng tối giản (Chính tắc).

---

## PHẦN II: CHỨNG MINH TOÁN HỌC TỔNG QUÁT (BẤT BIẾN ĐẠI SỐ)

Mọi đường cong bậc hai trên mặt phẳng đều có thể biểu diễn qua phương trình tổng quát:
$$Ax^2 + Bxy + Cy^2 + Dx + Ey + F = 0$$

Bản chất hình học nội tại của đường cong được quyết định bởi biệt thức bất biến $\Delta = B^2 - 4AC$.

- Nếu $\Delta > 0$, đường cong **bắt buộc là một Hyperbol không suy biến** (hoặc cặp đường thẳng cắt nhau trong trường hợp suy biến).

### 1. Đối với hàm bậc hai trên bậc nhất

Xét hàm số tổng quát sau khi nhân chéo mẫu số:
$$y = \frac{ax^2+bx+c}{px+q} \iff ax^2 - pxy + bx - qy + c = 0$$

Đối chiếu hệ số: $A = a$, $B = -p$, $C = 0$.
Tính biệt thức:
$$\Delta = B^2 - 4AC = (-p)^2 - 4(a)(0) = p^2$$
Vì điều kiện mẫu số có nghĩa nên $p \neq 0 \implies \Delta = p^2 > 0$.  
$\rightarrow$ **Kết luận:** Đồ thị luôn luôn là một Hyperbol phẳng.

### 2. Đối với hàm bậc nhất trên bậc nhất

Xét hàm số tổng quát sau khi nhân chéo mẫu số:
$$y = \frac{ax+b}{cx+d} \iff cxy + dy - ax - b = 0$$

Đối chiếu hệ số: $A = 0$, $B = c$, $C = 0$.
Tính biệt thức:
$$\Delta = B^2 - 4AC = c^2 - 4(0)(0) = c^2$$
Vì điều kiện hàm số không suy biến thành đường thẳng nên $c \neq 0 \implies \Delta = c^2 > 0$.  
$\rightarrow$ **Kết luận:** Đồ thị luôn luôn là một Hyperbol phẳng.

---

## PHẦN III: HAI NGHIÊN CỨU TÌNH HUỐNG CỤ THỂ (CASE STUDIES)

### CASE STUDY 1: Hàm bậc nhất/bậc nhất siêu tối giản $y = \frac{1}{x}$ (Hyperbol đều)

- **Phương trình ẩn:** $xy - 1 = 0 \implies A=0, B=1, C=0, F=-1$.
- **Tâm đối xứng:** Giao hai tiệm cận $x=0, y=0 \implies I(0,0)$ (Trùng gốc tọa độ, không cần tịnh tiến).
- **Tìm góc quay $\theta$:**
  $$\cot(2\theta) = \frac{A - C}{B} = \frac{0 - 0}{1} = 0 \implies 2\theta = 90^\circ \implies \theta = 45^\circ$$
- **Phép quay trục góc $45^\circ$:**
  $$\begin{cases} x = x'\cos(45^\circ) - y'\sin(45^\circ) = \frac{\sqrt{2}}{2}(x' - y') \\ y = x'\sin(45^\circ) + y'\cos(45^\circ) = \frac{\sqrt{2}}{2}(x' + y') \end{cases}$$
- **Thế vào phương trình gốc:**
  $$\left[\frac{\sqrt{2}}{2}(x' - y')\right] \cdot \left[\frac{\sqrt{2}}{2}(x' + y')\right] = 1 \iff \frac{1}{2}(x'^2 - y'^2) = 1$$
- **Phương trình chính tắc cuối cùng:**
  $$\frac{x'^2}{2} - \frac{y'^2}{2} = 1$$
  Đây là Hyperbol đều với hai bán trục bằng nhau: $a = b = \sqrt{2}$. Trục đối xứng thực là đường thẳng $y=x$, trục ảo là $y=-x$.

---

### CASE STUDY 2: Hàm bậc hai/bậc nhất điển hình $y = x + \frac{1}{x}$ (Hyperbol lệch)

- **Phương trình ẩn:** $x^2 - xy + 1 = 0 \implies A=1, B=-1, C=0, F=1$.
- **Tâm đối xứng:** Giao của tiệm cận đứng $x=0$ và tiệm cận xiên $y=x \implies I(0,0)$ (Không cần tịnh tiến).
- **Tìm góc quay $\theta$:**
  $$\cot(2\theta) = \frac{A - C}{B} = \frac{1 - 0}{-1} = -1 \implies 2\theta = 135^\circ \implies \theta = 67.5^\circ$$
- **Giá trị lượng giác góc $67.5^\circ$ (Hạ bậc):**
  $$\cos(67.5^\circ) = \frac{\sqrt{2-\sqrt{2}}}{2}, \quad \sin(67.5^\circ) = \frac{\sqrt{2+\sqrt{2}}}{2}$$
- **Phép quay trục và rút gọn:**
  Sau khi thế vào phương trình và triệt tiêu số hạng chéo $x'y'$, ta thu được phương trình hệ số mới:
  $$\left(\frac{1-\sqrt{2}}{2}\right)x'^2 + \left(\frac{1+\sqrt{2}}{2}\right)y'^2 = -1$$
- **Phương trình chính tắc cuối cùng:**
  $$\frac{x'^2}{2(\sqrt{2}+1)} - \frac{y'^2}{2(\sqrt{2}-1)} = 1$$
  Đây là Hyperbol lệch có cấu trúc kích thước:
  - Bán trục thực: $a = \sqrt{2\sqrt{2}+2}$
  - Bán trục ảo: $b = \sqrt{2\sqrt{2}-2}$
  - Trục đối xứng thực (Chứa đỉnh đồ thị): Đường thẳng chéo góc $67.5^\circ \implies y = (\sqrt{2}+1)x$.

---

## PHẦN IV: KỊCH BẢN PHÂN CẢNH VIDEO MANIM (VISUAL STORYBOARD)

### Cảnh 1: Đặt câu hỏi trực giác (The Hook)

- **Hình ảnh:** Hiển thị màn hình chia đôi. Bên trái là đồ thị hàm số $y = 1/x$ uốn lượn chéo góc phẳng. Bên phải là phương trình chính tắc $\frac{x^2}{2} - \frac{y^2}{2} = 1$ đứng thẳng cân đối.
- **Văn bản/Giọng đọc:** _"Trong sách giáo khoa, chúng có hai cái tên và hình thức khác nhau. Nhưng toán học đỉnh cao khẳng định: Chúng là một vật thể duy nhất. Tại sao mắt ta lại bị đánh lừa?"_

### Cảnh 2: Khám phá trục đối xứng ẩn

- **Hình ảnh:** Tập trung vào đồ thị $y = 1/x$. Vẽ hai đường tiệm cận $Ox, Oy$.
- **Hiệu ứng Manim:** Dùng `FadeIn` làm xuất hiện đường thẳng chéo $y=x$ màu vàng rực lấp lánh. Tạo hiệu ứng một nhánh đồ thị lật đối xứng (Mirror flip) qua đường thẳng này để chứng minh tính đối xứng chéo trực quan.

### Cảnh 3: Phép thuật dời hình (The Climax Animation)

- **Hiệu ứng Manim:** Dùng lệnh quay hệ trục tọa độ hoặc quay camera góc $-45^\circ$.
- **Hình ảnh chuyển động:** Người xem sẽ thấy toàn bộ lưới tọa độ cũ quay nghiêng đi. Đồ thị hàm số vốn đang nằm chéo, qua phép quay bỗng từ từ đứng thẳng dậy, ôm khít lấy hệ trục tọa độ vuông vắn mới.
- **Văn bản/Giọng đọc:** _"Chúng ta không thay đổi đồ thị. Chúng ta chỉ xoay chiếc camera của hệ tọa độ một góc đúng 45 độ để nhìn thẳng vào bản chất của nó."_

### Cảnh 4: Sự biến đổi của các ký tự (Mathematical Morph)

- **Hiệu ứng Manim:** Dùng `ReplacementTransform`. Phương trình đại số chữ chạy trên màn hình từ dạng $xy = 1$ từ từ rã ra, các ký tự di chuyển và tự sắp xếp lại thành dạng phân thức chính tắc $\frac{x'^2}{2} - \frac{y'^2}{2} = 1$.
- **Văn bản/Giọng đọc:** _"Khi thước đo vuông góc với trục đối xứng nội tại, các nhiễu số biến mất. Hyperbol chính thức lộ diện tấm chân dung chính tắc của mình."_

---

## PHẦN V: ĐOẠN CODE MANIM PYTHON MẪU ĐỂ KHỞI ĐẦU

_(Đoạn code thô này dùng để test nhanh việc vẽ đồ thị ẩn bằng Manim)_

```python
from manim import *

class HyperbolaTransformation(LinearTransformationScene):
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            leave_ghost_vectors=False,
            **kwargs
        )

    def construct(self):
        # 1. Vẽ hàm số y = 1/x bằng ImplicitFunction (đại diện cho xy = 1)
        hyperbola = ImplicitFunction(
            lambda x, y: x * y - 1,
            color=RED
        )

        # 2. Vẽ đường đối xứng y = x
        symmetry_line = Line(start=[-5, -5, 0], end=[5, 5, 0], color=YELLOW)

        self.add_transformable_mobject(hyperbola)
        self.play(FadeIn(symmetry_line))
        self.wait(1)

        # 3. Ma trận quay góc -45 độ để chính tắc hóa đồ thị
        # cos(-45) = sqrt(2)/2, sin(-45) = -sqrt(2)/2
        matrix = [[0.707, 0.707], [-0.707, 0.707]]

        # 执行坐标轴旋转矩阵变换 (Phép dời hình hệ trục)
        self.apply_matrix(matrix)
        self.wait(2)
```

---

_Tài liệu đã được đóng gói đầy đủ dữ liệu đại số và kịch bản trực quan. Sẵn sàng cho việc triển khai nghiên cứu nâng cao._

---

Chúc video hiện tại của bạn gặt hái được nhiều thành công! Khi nào bạn hoàn thành dự án đó và muốn quay lại thực hiện "siêu phẩm" Hyperbol này, tệp tài liệu này sẽ là người bạn đồng hành hoàn hảo nhất giúp bạn tiết kiệm thời gian tính toán và lên ý tưởng.
