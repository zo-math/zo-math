---
author:
- ZO \| 2025-03-02
authors:
- ZO \| 2025-03-02
execute:
  cache: true
header-includes:
- |
  <script src="bai_tap_bai_1_chuong_v_toan_11_bo_canh_dieu_files/libs/kePrint-0.0.1/kePrint.js"></script>
  <link href="bai_tap_bai_1_chuong_v_toan_11_bo_canh_dieu_files/libs/lightable-0.0.1/lightable.css" rel="stylesheet" />
lang: vi
subtitle: BÀI TẬP TOÁN LỚP 11 \| SÁCH CÁNH DIỀU
title: CÁC SỐ ĐẶC TRƯNG ĐO XU THẾ TRUNG TÂM CHO MẪU SỐ LIỆU GHÉP NHÓM
toc-title: Table of contents
---

<script src="bai_tap_bai_1_chuong_v_toan_11_bo_canh_dieu_files/libs/kePrint-0.0.1/kePrint.js"></script>
<link href="bai_tap_bai_1_chuong_v_toan_11_bo_canh_dieu_files/libs/lightable-0.0.1/lightable.css" rel="stylesheet" />


::: {.alert .alert-info}
Đây là các bài tập của Bài 1: *Các số đặc trưng đo xu thế trung tâm cho
mẫu số liệu ghép nhóm*, Chương V: *Một số yếu tố thống kê và xác suất*,
bộ *Cánh Diều*, Toán 11 (trang 14, tập 2).
:::

1\. Mẫu số liệu dưới đây ghi lại tốc độ của 40 ô-tô khi đi qua một trạm
đo tốc độ (đơn vị: km/h):

:::: cell
::: cell-output-display
  ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
   48,5   43,0   50,0   55,0   45,0   60,0   53,0   55,5   44,0   65,0
   51,0   62,5   41,0   44,5   57,0   57,0   68,0   49,0   46,5   53,5
   61,0   49,5   54,0   62,0   59,0   56,0   47,0   50,0   60,0   61,0
   49,5   52,5   57,0   47,0   60,0   55,0   45,0   47,5   48,0   61,5
  ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
:::
::::

a\) Lập bảng tần số ghép nhóm cho mẫu số liệu trên có sáu nhóm ứng với
sáu nửa khoảng:

b\) Xác định trung bình cộng, trung vị, tứ phân vị của mẫu số liệu ghép
nhóm trên.

c\) Mốt của mẫu số liệu ghép nhóm trên là bao nhiêu?

[Lời giải]{.smallcaps}

<!-- NHẬP SỐ LIỆU -->

::::::::::::::: cell
::: {.cell-output .cell-output-stdout}
     [1] 48.5 43.0 50.0 55.0 45.0 60.0 53.0 55.5 44.0 65.0 51.0 62.5 41.0 44.5 57.0
    [16] 57.0 68.0 49.0 46.5 53.5 61.0 49.5 54.0 62.0 59.0 56.0 47.0 50.0 60.0 61.0
    [31] 49.5 52.5 57.0 47.0 60.0 55.0 45.0 47.5 48.0 61.5
:::

::: {.cell-output .cell-output-stdout}
     [1] 41.0 43.0 44.0 44.5 45.0 45.0 46.5 47.0 47.0 47.5 48.0 48.5 49.0 49.5 49.5
    [16] 50.0 50.0 51.0 52.5 53.0 53.5 54.0 55.0 55.0 55.5 56.0 57.0 57.0 57.0 59.0
    [31] 60.0 60.0 60.0 61.0 61.0 61.5 62.0 62.5 65.0 68.0
:::

::: {.cell-output .cell-output-stdout}
    [1] 40 45 50 55 60 65 70
:::

::: {.cell-output .cell-output-stdout}
    [1] 42.5 47.5 52.5 57.5 62.5 67.5
:::

::: {.cell-output .cell-output-stdout}
    [1]  4 11  7  8  8  2
:::

::: {.cell-output .cell-output-stdout}
    [1]  4 15 22 30 38 40
:::

::: {.cell-output .cell-output-stdout}
         Nhóm Mút trái Mút phải Giá trị đại diện Tần số Tần số tích lũy
    1 [40,45)       40       45             42.5      4               4
    2 [45,50)       45       50             47.5     11              15
    3 [50,55)       50       55             52.5      7              22
    4 [55,60)       55       60             57.5      8              30
    5 [60,65)       60       65             62.5      8              38
    6 [65,70)       65       70             67.5      2              40
:::

::: {.cell-output .cell-output-stdout}
    [1] 431/8
:::

::: {.cell-output .cell-output-stdout}
    [1] 375/7
:::

::: {.cell-output .cell-output-stdout}
    [1] 334/7
:::

::: {.cell-output .cell-output-stdout}
    [1] 60
:::

::: {.cell-output .cell-output-stdout}
    [1] 530/11
:::
:::::::::::::::

a\) Để tránh nhầm lẫn trong việc phân phối số liệu vào từng nhóm thích
hợp, trước tiên, mình sẽ sắp xếp lại số liệu theo thứ tự tăng dần:

:::: cell
::: cell-output-display
  ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
   41,0   43,0   44,0   44,5   45,0   45,0   46,5   47,0   47,0   47,5
   48,0   48,5   49,0   49,5   49,5   50,0   50,0   51,0   52,5   53,0
   53,5   54,0   55,0   55,0   55,5   56,0   57,0   57,0   57,0   59,0
   60,0   60,0   60,0   61,0   61,0   61,5   62,0   62,5   65,0   68,0
  ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
:::
::::

Khi các số liệu đã được sắp theo thứ tự tăng dần, bạn dễ dàng thấy rằng
thuộc vào nhóm $[40,45)$ có 4 số liệu bao gồm 41; 43; 44; 44,5. Tương tự
với các nhóm còn lại.

Bảng tần số ghép nhóm là

:::: cell
::: cell-output-display
        Nhóm          Tần số
  ---------------- ------------
   \\(\[40,45)\\)       4
   \\(\[45,50)\\)       11
   \\(\[50,55)\\)       7
   \\(\[55,60)\\)       8
   \\(\[60,65)\\)       8
   \\(\[65,70)\\)       2
                    \\(n=40\\)
:::
::::

b\) Để giải đáp câu này, bạn cần các giá trị đại diện và các tần số tích
lũy, do đó mình sẽ mở rộng bảng ở câu a thành bảng

:::: cell
::: cell-output-display
        Nhóm        Giá trị đại diện     Tần số     Tần số tích lũy
  ---------------- ------------------ ------------ -----------------
   \\(\[40,45)\\)         42.5             4               4
   \\(\[45,50)\\)         47.5             11             15
   \\(\[50,55)\\)         52.5             7              22
   \\(\[55,60)\\)         57.5             8              30
   \\(\[60,65)\\)         62.5             8              38
   \\(\[65,70)\\)         67.5             2              40
                                       \\(n=40\\)  
:::
::::

-   Kích thước mẫu là $n=40$. Nhóm thứ nhất, $[40;45)$, có trung điểm
    $x_1=42,5$ làm giá trị đại diện và có tần số $n_1=4$. Ký hiệu tương
    tự cho các nhóm còn lại. Trung bình cộng là `\begin{align*}
      \bar{x} 
          & = \frac{n_1\cdot x_1 + n_2\cdot x_2 + n_3\cdot x_3 + n_4\cdot x_4 + n_5\cdot x_5 + n_6\cdot x_6}{n} \\
          & = \frac{4\cdot 42,5 + 11\cdot 47,5 + 7\cdot 52,5 + 8\cdot 57,5 + 8\cdot 62,5 + 2\cdot 67,5}{40} \\
          & = \frac{431}{8} \\
          & = 53,8750 \text{ (km/h)}.
    \end{align*}`{=tex}

-   Nhóm thứ ba, $[50;55)$, với $cf_3=22$ là nhóm đầu tiên có tần số
    tích lũy lớn hơn $$ 
      \frac{n}{2}=\frac{40}{2}=20.
      $$ Nhóm này có đầu mút trái $r=50$, độ dài $d=5$ và tần số
    $n_3=7$. Nhóm thứ hai có tần số tích lũy $cf_2=15$. Giá trị trung vị
    là `\begin{align*}
          M_e
              & = r+\left(\frac{\frac{n}{2}-cf_2}{n_3}\right)\cdot d \\
              & = 50 + \left(\frac{20-15}{7}\right)\cdot 5 \\
              & = \frac{375}{7} \\
              & \approx 53,5714 \text{ (km/h).}
      \end{align*}`{=tex}

-   Nhóm thứ hai $[45;50)$ với $cf_2=15$ là nhóm đầu tiên có tần số tích
    lũy lớn hơn $$
      \frac{n}{4}=\frac{40}{4}=10.
      $$ Nhóm này có đầu mút trái $s=45$, độ dài $h=5$ và tần số
    $n_2=11$. Nhóm thứ nhất có tần số tích lũy là $cf_1=4$. Giá trị tứ
    phân vị thứ nhất là `\begin{align*}
          Q_1
              & = s + \left( \frac{\frac{n}{4}-cf_1}{n_2}\right)\cdot h \\
              & = 45 + \left(\frac{10-4}{11}\right)\cdot 5 \\
              & = \frac{525}{11} \\
              & \approx 47,7273 \text{ (km/h).}
      \end{align*}`{=tex}

-   Tứ phân vị thứ hai $Q_2$ chính là trung vị $M_e$.

-   Nhóm thứ tư $[55;60)$ với $cf_4=30$ là nhóm đầu tiên có tần số tích
    lũy bằng $$
      \frac{3n}{4}=\frac{3\cdot 40}{4}=30.
      $$ Nhóm này có đầu mút trái $t=55$, độ dài $l=5$ và tần số
    $n_4=8$. Nhóm thứ ba có tần số tích lũy là $cf_3=22$. Giá trị tứ
    phân vị thứ ba là `\begin{align*}
          Q_3
              & = t + \left(\frac{\frac{3n}{4}-cf_3}{n_4}\right)\cdot l \\
              & = 55 + \left(\frac{30-22}{8}\right)\cdot 5 \\
              & = 60 \text{ (km/h).}
      \end{align*}`{=tex}

c\) Nhóm hai $[45;50)$ là nhóm có tần số lớn nhất $n_2=11$. Nó có đầu
mút trái $u=45$ và độ dài $g=5$. Nhóm một có tần số $n_1=4$ và nhóm ba
có tần số $n_3=7$. Giá trị mốt là `\begin{align*}
        M_o
            & = u + \left(\frac{n_2-n_1}{2n_2-n_1-n_3}\right) \cdot g \\
            & = 45 + \left(\frac{11-4}{2\cdot 11-4-7}\right)\cdot 5 \\
            & = \frac{530}{11} \\
            & \approx 48,1818 \text{ (km/h)}.
    \end{align*}`{=tex}

2\. Mẫu số liệu sau ghi lại cân nặng của 30 bạn học sinh (đơn vị: kg):

:::: cell
::: cell-output-display
  ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
   17,0   40,0   39,0   40,5   42,0   51,0   41,5   39,0   41,0   30,0
   40,0   42,0   40,5   39,5   41,0   40,5   37,0   39,5   40,0   41,0
   38,5   39,5   40,0   41,0   39,0   40,5   40,0   38,5   39,5   41,5
  ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
:::
::::

a\) Lập bảng tần số ghép nhóm cho mẫu số liệu trên có tám nhóm ứng với
tám nửa khoảng:

b\) Xác định trung bình cộng, trung vị, tứ phân vị của mẫu số liệu ghép
nhóm trên.

c\) Mốt của mẫu số liệu ghép nhóm trên là bao nhiêu?

[Lời giải]{.smallcaps}

<!-- NHẬP SỐ LIỆU -->

::::::::::::::: cell
::: {.cell-output .cell-output-stdout}
     [1] 17.0 40.0 39.0 40.5 42.0 51.0 41.5 39.0 41.0 30.0 40.0 42.0 40.5 39.5 41.0
    [16] 40.5 37.0 39.5 40.0 41.0 38.5 39.5 40.0 41.0 39.0 40.5 40.0 38.5 39.5 41.5
:::

::: {.cell-output .cell-output-stdout}
     [1] 17.0 30.0 37.0 38.5 38.5 39.0 39.0 39.0 39.5 39.5 39.5 39.5 40.0 40.0 40.0
    [16] 40.0 40.0 40.5 40.5 40.5 40.5 41.0 41.0 41.0 41.0 41.5 41.5 42.0 42.0 51.0
:::

::: {.cell-output .cell-output-stdout}
    [1] 15 20 25 30 35 40 45 50 55
:::

::: {.cell-output .cell-output-stdout}
    [1] 17.5 22.5 27.5 32.5 37.5 42.5 47.5 52.5
:::

::: {.cell-output .cell-output-stdout}
    [1]  1  0  0  1 10 17  0  1
:::

::: {.cell-output .cell-output-stdout}
    [1]  1  1  1  2 12 29 29 30
:::

::: {.cell-output .cell-output-stdout}
         Nhóm Mút trái Mút phải Giá trị đại diện Tần số Tần số tích lũy
    1 [15,20)       15       20             17.5      1               1
    2 [20,25)       20       25             22.5      0               1
    3 [25,30)       25       30             27.5      0               1
    4 [30,35)       30       35             32.5      1               2
    5 [35,40)       35       40             37.5     10              12
    6 [40,45)       40       45             42.5     17              29
    7 [45,50)       45       50             47.5      0              29
    8 [50,55)       50       55             52.5      1              30
:::

::: {.cell-output .cell-output-stdout}
    [1] 40
:::

::: {.cell-output .cell-output-stdout}
    [1] 695/17
:::

::: {.cell-output .cell-output-stdout}
    [1] 151/4
:::

::: {.cell-output .cell-output-stdout}
    [1] 1465/34
:::

::: {.cell-output .cell-output-stdout}
    [1] 995/24
:::
:::::::::::::::

Nội dung được trình bày lần này sẽ ngắn gọn hơn, mình không nhắc lại các
kí hiệu và cách làm như ở Bài 1 nữa.

a\) Bảng tần số ghép nhóm là

:::: cell
::: cell-output-display
        Nhóm          Tần số
  ---------------- ------------
   \\(\[15,20)\\)       1
   \\(\[20,25)\\)       0
   \\(\[25,30)\\)       0
   \\(\[30,35)\\)       1
   \\(\[35,40)\\)       10
   \\(\[40,45)\\)       17
   \\(\[45,50)\\)       0
   \\(\[50,55)\\)       1
                    \\(n=30\\)
:::
::::

b\) Bảng tần số ghép nhóm bao gồm giá trị đại diện và tần số tích lũy là

:::: cell
::: cell-output-display
        Nhóm        Giá trị đại diện     Tần số     Tần số tích lũy
  ---------------- ------------------ ------------ -----------------
   \\(\[15,20)\\)         17.5             1               1
   \\(\[20,25)\\)         22.5             0               1
   \\(\[25,30)\\)         27.5             0               1
   \\(\[30,35)\\)         32.5             1               2
   \\(\[35,40)\\)         37.5             10             12
   \\(\[40,45)\\)         42.5             17             29
   \\(\[45,50)\\)         47.5             0              29
   \\(\[50,55)\\)         52.5             1              30
                                       \\(n=30\\)  
:::
::::

-   Trung bình là `\begin{align*}
    \bar{x}
      & = \frac{1}{30} (1\cdot 17,5 + 0\cdot 22,5 + 0\cdot 27,5+ 1\cdot 32,5 + 10\cdot 37,5 + 17\cdot 42,5 + 0\cdot 47,5 + 52,5 \cdot 1) \\
      & = 40.
    \end{align*}`{=tex}

-   Có $n=30$ số liệu, nhóm thứ sáu $[40;45)$ là nhóm đầu tiên có tần số
    tích lũy $cf_6=29$ không nhỏ hơn $\frac{n}{2}=15$. Nhóm này có đầu
    mút trái $r=40$, độ dài $d=5$ và tần số $n_6=17$. Nhóm thứ năm liền
    trước nó có tần số tích lũy $cf_5=12$. Trung vị là `\begin{align*}
    M_e
      & = r + \left(\frac{\frac{n}{2}-cf_5}{n_6}\right)\cdot d \\
      & = 40 + \left(\frac{15-12}{17}\right)\cdot 5 \\
      & = \frac{695}{17} \\
      & \approx 40,8824 \text{ (kg).}
    \end{align*}`{=tex}

-   Nhóm thứ năm $[35;40)$ là nhóm đầu tiên có tần số tích lũy $cf_5=12$
    không nhỏ hơn $\frac{n}{4}=7,5$. Nhóm này có đầ mút trái $s=35$, độ
    dài $h=5$ và tần số $n_5=10$. Nhóm thứ tư liền trước nó có tần số
    tích lũy $cf_4=2$. Tứ phân vị thứ nhất là `\begin{align*}
    Q_1
      & = s + \left( \frac{\frac{n}{4}-cf_4}{n_5}\right)\cdot h \\
      & = 35 + \left(\frac{7,5-2}{10}\right)\cdot 5 \\
      & = \frac{151}{4} \\
      & = 37,75 \text{ (kg).}
    \end{align*}`{=tex}

-   Tứ phân vị thứ hai $Q_2$ chính là trung vị $M_e$, hay \$Q_2=M_e
    `\approx 40`{=tex},8824 \$ (kg).

-   Nhóm thứ sáu $[40;45)$ là nhòm đầu tiên có tần số tích lũy $cf_6=29$
    không nhỏ hơn $\frac{3n}{4}=22,5$. Nhóm này có đầu mút trái $t=40$,
    độ dài $l=5$ và tần số $n_6=17$. Nhóm thứ năm liền trước nó có tần
    số tích lũy là $cf_5=12$. Tứ phân vị thứ ba là `\begin{align*}
    Q_3
      & = t + \left(\frac{\frac{3n}{4}-cf_5}{n_6}\right)\cdot l \\
      & = 40 +\left(\frac{22,5-12}{17}\right) \cdot 5 \\
      & = \frac{1465}{34} \\
      & \approx 43,0882 \text{ (kg).}
    \end{align*}`{=tex}

-   Nhóm thứ sáu $[40,45)$ là nhóm có tần số lớn nhất $n_6=40$. Nhóm này
    có đầu mút trái $u=40$ và độ dài $g=5$. Nhóm thứ tư liền trước nó có
    tần số $n_5=10$ và nhóm thứ bảy liền sau nó có tần số $n_7=0$. Mốt
    là `\begin{align*}
    M_o 
      & = u + \left(\frac{n_6-n_5}{2n_6 - n_5 - n_7}\right)\cdot g \\
      & = 40 + \left(\frac{17-10}{2\cdot 17 - 10 - 0}\right)\cdot 5 \\
      & = \frac{995}{24} \\
      & \approx 41,4583 \text{ (kg).}
    \end{align*}`{=tex}

3\. Bảng 15 cho ta bảng tần số ghép nhóm số liệu thống kê chiều cao của
40 mẫu cây ở một vườn thực vật (đơn vị: cm).

a\) Xác định trung bình cộng, trung vị, tứ phân vị của mẫu số liệu ghép
nhóm trên.

b\) Mốt của mẫu số liệu ghép nhóm trên là bao nhiêu?
