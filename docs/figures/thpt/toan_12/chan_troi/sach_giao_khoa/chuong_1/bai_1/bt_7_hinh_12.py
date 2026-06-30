import numpy as np
from scipy.interpolate import make_interp_spline

# B1: Nhập các điểm của bạn tại đây
x = np.array([-2, -1, 0, 2, 3, 4, 5])
y = np.array([-3, 0, 1.5, 0, -0.75, 0, 4])

# B2: Tạo spline bậc 3
spline = make_interp_spline(x, y, k=3)

# B3: Tạo các điểm nội suy mịn
x_dense = np.linspace(min(x), max(x), 200)
y_dense = spline(x_dense)

# B4: In ra TikZ coordinates
print(r"\addplot[smooth, thick] coordinates {")
for xi, yi in zip(x_dense, y_dense):
    print(f"  ({xi:.3f}, {yi:.3f})")
print("};")
