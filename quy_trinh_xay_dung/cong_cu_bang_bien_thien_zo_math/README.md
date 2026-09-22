# Bộ công cụ bảng biến thiên ZO Math v0.1

Công cụ nhận một JSON canonical chứa các hàng mốc, dấu/trạng thái đạo hàm và chiều
biến thiên, kiểm tra cấu trúc rồi sinh đồng thời TEX, PDF vector và SVG. HTML dùng
SVG; PDF học liệu dùng PDF. Cùng một JSON phục vụ cả hai đầu ra.

Kiến trúc có ba lớp tách biệt:

1. `zo_variation_build.py` và `tex/` là công cụ sinh tài sản vector dùng chung;
2. `assets/lua/zo_variation_qmd.lua` cùng `assets/css/zo_variation.css` là hợp
   đồng nhúng QMD dùng chung, chọn SVG/PDF và tạo bảng ngữ nghĩa trợ năng;
3. mỗi gói chỉ sở hữu JSON, các tài sản đã sinh và khai báo chúng trong cấu hình
   build. Adapter của gói nạp module dùng chung với đường dẫn JSON/thư mục tài sản;
   không sao chép mã Lua hoặc CSS của R1-G01.

## Lệnh dùng

```text
python scripts/zo_python.py quy_trinh_xay_dung/cong_cu_bang_bien_thien_zo_math/zo_variation_build.py check DU_LIEU.json
python scripts/zo_python.py quy_trinh_xay_dung/cong_cu_bang_bien_thien_zo_math/zo_variation_build.py build DU_LIEU.json --out-dir THU_MUC --check --force
```

Mỗi bản ghi cần `id`, `title`, `rows`. Hàng đầu là các mốc xen kẽ khoảng; bảng có
thể gồm hàng dấu đạo hàm và hàng biến thiên, hoặc chỉ một trong hai. `excluded_columns`
đánh dấu điểm bị loại khỏi miền. Trường `intentional_error: true` chỉ dành cho ví dụ
sai có chủ ý: validator vẫn kiểm cấu trúc nhưng không bác mâu thuẫn dấu–chiều.
Trường tùy chọn `column_min_widths_mm` là object ánh xạ chỉ số cột tính từ 0 sang
chiều rộng tối thiểu 8–60 mm. Chỉ khai trường này khi một ô chứa nội dung dài; mọi
node trong cột nhận cùng chiều rộng tối thiểu và hai đường biên kề cột bám vào cạnh
node. Bảng không khai trường này giữ nguyên hình học mặc định.

Trong PDF học liệu, lớp tích hợp đặt bảng theo kích thước vật lí của PDF asset.
`max width` và `max totalheight` chỉ thu nhỏ bảng vượt khối chữ; không phóng bảng
hẹp lên theo chiều rộng dòng. Vì vậy cỡ chữ canonical trong asset được giữ gần cỡ
chữ nội dung, bảng đơn giản vẫn gọn và toàn khối tiếp tục căn trái.

Ví dụ tối thiểu:

```json
[{"id":"BBT01","title":"Bảng biến thiên","rows":[
  ["x","−∞","","1","","+∞"],
  ["f′(x)","","+","0","+",""],
  ["f(x)","−∞","↗","2","↗","+∞"]
]}]
```

Trong QMD, chỉ đặt mã `bbt="BBT01"`; filter tích hợp tra mã này và chọn SVG/PDF
phù hợp định dạng. Không chép lại dữ liệu bảng trong QMD. Khi thêm một gói mới:

- cung cấp JSON theo hợp đồng trên;
- gọi mã bảng trong QMD;
- khai báo JSON, TEX/PDF/SVG và adapter nạp module chung trong `artifact_inputs`.

Không fork template TikZ, Lua hay CSS theo từng gói. Hiện công cụ dành cho Codex và
người viết mã; giao diện nhập liệu trực quan là hướng phát triển sau.

Khung bảng dùng trực tiếp token canonical của đồ thị v0.2: nền
`zoGraphVTwoPlotBackground`, đường `zoGraphVTwoPlotBorder`, nét `0.45pt` và góc bo
`2mm`. Các đường bên trong dùng cùng token, được clip trong khung bo tròn.
