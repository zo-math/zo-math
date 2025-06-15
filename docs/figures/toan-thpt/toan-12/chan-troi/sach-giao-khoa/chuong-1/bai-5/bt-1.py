import numpy as np
from scipy.interpolate import make_interp_spline

# x = np.array([-2, -1.79, -1.55, -1.18, -0.59, 
#                 0, 0.8, 1.22, 1.5, 2.2, 
#                 2.6, 3, 3.4, 3.79, 4, 
#                 4.5, 5, 5.41, 5.7, 
#                 6, 6.38])
# y = np.array([-6, -4.02, -1.99, -0.61, -0.16, 
#                 0, 0.49, 1.2, 2, 3.45, 
#                 3.8, 4, 3.8, 3.02, 2, 
#                 0.5, 0, 0.5, 1.51, 
#                 3, 6])

# B2: Tạo spline bậc 3
spline = make_interp_spline(x, y, k=3)

# B3: Tạo các điểm nội suy mịn
x_dense = np.linspace(min(x), max(x), 300)
y_dense = spline(x_dense)

# B4: In ra TikZ coordinates
print(r"\addplot[smooth, line width=1.5pt, color=den-2, opacity=.8] coordinates {")
for xi, yi in zip(x_dense, y_dense):
    print(f"  ({xi:.3f}, {yi:.3f})")
print("};")
