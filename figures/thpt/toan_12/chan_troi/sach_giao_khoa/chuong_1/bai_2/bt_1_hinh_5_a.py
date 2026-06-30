import numpy as np
from scipy.interpolate import make_interp_spline

# B1: Nhập các điểm của bạn tại đây
x = np.array([1,2,2.5,3,3.5,4,4.5,5,5.5,6])
y = np.array([6,3,2.25,2,2.5,3,2,1,2.25,5])

# B2: Tạo spline bậc 3
spline = make_interp_spline(x, y, k=4)

# B3: Tạo các điểm nội suy mịn
x_dense = np.linspace(min(x), max(x), 300)
y_dense = spline(x_dense)

# B4: In ra TikZ coordinates
print(r"\addplot[smooth, line width=1.5pt, color=den-2, opacity=.8] coordinates {")
for xi, yi in zip(x_dense, y_dense):
    print(f"  ({xi:.3f}, {yi:.3f})")
print("};")
