import numpy as np
from scipy.interpolate import BPoly

# Dữ liệu
x = [1, 1.5, 2, 3, 4, 5, 6]
y = [6, 4.15, 3, 2, 3, 1, 5]

# Gợi ý đạo hàm = 0 tại các điểm cực trị
values = [
    [6],       # x=1
    [4.25],
    [3],       # x=2
    [2, 0.0],  # x=3: cực tiểu
    [3, 0.0],  # x=4: cực đại
    [1, 0.0],  # x=5: cực tiểu
    [5]        # x=6
]

spline = BPoly.from_derivatives(x, values)

x_dense = np.linspace(1, 6, 300)
y_dense = spline(x_dense)

print(r"\addplot[smooth, line width=1.5pt, color=den-2, opacity=.8] coordinates {")
for xi, yi in zip(x_dense, y_dense):
    print(f"  ({xi:.3f}, {yi:.3f})")
print("};")
