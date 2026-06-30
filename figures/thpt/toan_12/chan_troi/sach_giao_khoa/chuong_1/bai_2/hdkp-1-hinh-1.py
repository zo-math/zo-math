import numpy as np
from scipy.interpolate import make_interp_spline

# B1: Nhập các điểm của bạn tại đây
x = np.array([0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13, 15, 16, 17, 20, 22, 24])
y = np.array([25, 24.35, 22.5, 20.5, 20, 21.5, 29.5, 31, 30.25, 28.25, 28, 29.3, 33, 34, 33, 27, 24.55, 24])

# B2: Tạo spline bậc 3
spline = make_interp_spline(x, y, k=4)

# B3: Tạo các điểm nội suy mịn
x_dense = np.linspace(min(x), max(x), 300)
y_dense = spline(x_dense)

# B4: In ra TikZ coordinates
print(r"\addplot[smooth, thick] coordinates {")
for xi, yi in zip(x_dense, y_dense):
    print(f"  ({xi:.3f}, {yi:.3f})")
print("};")
