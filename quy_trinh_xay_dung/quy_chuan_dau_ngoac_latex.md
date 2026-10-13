# Quy chuẩn dấu ngoặc LaTeX ZO Math

Có hiệu lực toàn ZO Math theo xác nhận của chủ trì ngày 11/10/2026.
Đây là quy chuẩn nguồn nội bộ, không phải nội dung hướng dẫn người học.

Khi dấu ngoặc bao một phân số hoặc biểu thức cao (căn, biểu thức xếp tầng,
ma trận, tổng hoặc tích phân), viết cặp `\left…\right` để dấu ngoặc tự
co giãn theo nội dung. Áp dụng cả ngoặc tròn, vuông, nhọn, trị tuyệt đối,
chuẩn và ngoặc góc; kể cả đối số hàm chứa phân số.

- Đúng: `$\left[0;\frac{\pi}{2}\right]$`.
- Không dùng: `$[0;\frac{\pi}{2}]$`.
- Khoảng nửa kín giữ nguyên đầu mút: `$\left(\frac{1}{2};1\right]$`.
- Đối số: `$f\left(\frac{\pi}{2}\right)$`.
- Ngoặc nhọn được in: `$\left\{\frac{1}{x}\right\}$`; không nhầm với
  dấu `{…}` chỉ nhóm đối số LaTeX.

Ngoặc chỉ bao biểu thức thấp như `$[0;1]$` hoặc `$(x-1)^2$` không bắt buộc
thêm `\left…\right`. Không thay đầu mút mở/đóng, dữ kiện, ID hay luồng học.
Không kéo, ép hoặc cắt dấu ngoặc bằng CSS để thay cho nguồn LaTeX đúng.

Guard dùng chung: `scripts/zo_latex_delimiters.py`, hàm `delimiter_errors`.
Cổng `scripts/zo_math_notation.py` gọi guard này cho G01/G02 và các include
được sử dụng trước dựng HTML. Chưa tích hợp tự động vào mọi pipeline khác
của repository; nhiệm vụ ở phạm vi khác phải kiểm nguồn theo quy chuẩn này.
Kiểm nguồn không thay kiểm trực quan HTML/PDF hoặc nghiệm thu của chủ trì.
