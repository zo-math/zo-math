# Bộ công cụ đồ thị hàm số ZO Math v0.1

Bộ công cụ này hiện thực Quy chuẩn sản xuất đồ thị hàm số ZO Math v0.2 cho các sản phẩm mới. Nó nhận một nguồn TikZ/PGFPlots và sinh từ cùng nguồn:

- PDF vector dùng cho tài liệu in;
- SVG dùng cho web;
- kết quả kiểm tra kỹ thuật cơ bản khi bật `--check`.

Nguồn đồ thị của từng sản phẩm thuộc về gói sản phẩm đó. Thư mục này chỉ chứa bộ máy dựng, style có phiên bản, mẫu khởi đầu và kiểm thử dùng chung. Không đặt nguồn sản xuất riêng của một bài học vào đây.

## 1. Chọn mẫu

| Mẫu | Dùng khi |
| --- | --- |
| `mau/do_thi_mot_duong.tex` | Một đường cong và một yếu tố phụ như tiếp tuyến |
| `mau/do_thi_nhan_truc_tiep.tex` | Có tối đa ba đường, công thức ngắn và vùng đặt nhãn thoáng |
| `mau/do_thi_hop_chu_thich.tex` | Có ba đường, công thức dài, nhiều giao cắt hoặc vùng vẽ chật |

Sao chép đúng một mẫu vào thư mục nguồn của gói học liệu rồi đổi tên theo chức năng, chẳng hạn `tiep_tuyen_ngang_khong_cuc_tri.tex`. Không sửa trực tiếp mẫu dùng chung để làm một sản phẩm cụ thể.

## 2. Sửa nguồn đã sao chép

Trong tệp `.tex`, sửa lần lượt:

1. phần chú thích đầu tệp: mục đích và điều người học cần nhận ra;
2. `xmin`, `xmax`, `ymin`, `ymax`: cửa sổ quan sát;
3. `domain`, `samples` và biểu thức trong `\addplot`: miền lấy mẫu và công thức;
4. `xtick`, `ytick`: các vạch thật sự cần đọc;
5. `coordinates`: điểm đặc, điểm rỗng hoặc điểm nhấn;
6. các `\node`: nội dung và vị trí nhãn;
7. vị trí `legend style` nếu dùng hộp chú thích.

Giữ `\input{zo_graph_v02.tex}`. Chương trình dựng tự cấp đường tìm style và phông, vì vậy nguồn sản phẩm không cần đường dẫn tuyệt đối hoặc số cấp `../` phụ thuộc dự án.

Không đổi màu để phân biệt các đường ngang hàng. Ba đường lần lượt dùng:

- `zo graph v02 curve solid`;
- `zo graph v02 curve dashed`;
- `zo graph v02 curve dashdot`.

Mọi đường dùng đỏ ZO Math `#EF5350` và dày mặc định 1,1 pt. Khi có hơn ba đường, cần xem lại việc tách hình thay vì tự thêm màu.

Nhãn trực tiếp dùng `zo graph v02 protected label`. Hãy chọn vị trí thoáng trước rồi mới dùng nền bảo vệ nhỏ. Nhãn điểm nên cách marker khoảng 2–3 mm, không che marker, giao điểm, tiếp điểm hoặc làm đường cong trông gián đoạn.

Đường phụ dùng style đúng vai trò:

- `zo graph v02 tangent` cho tiếp tuyến;
- `zo graph v02 asymptote` cho tiệm cận;
- `zo graph v02 auxiliary` cho đường chiếu hoặc tham chiếu phụ.

## 3. Dựng PDF và SVG

Chạy từ gốc repository qua launcher Python chuẩn. Ba lệnh mẫu tương ứng ba nguồn dùng chung:

```text
python scripts/zo_python.py quy_trinh_xay_dung/cong_cu_do_thi_ham_so_zo_math/zo_graph_build.py quy_trinh_xay_dung/cong_cu_do_thi_ham_so_zo_math/mau/do_thi_mot_duong.tex --out-dir quy_trinh_xay_dung/cong_cu_do_thi_ham_so_zo_math/_output --check
python scripts/zo_python.py quy_trinh_xay_dung/cong_cu_do_thi_ham_so_zo_math/zo_graph_build.py quy_trinh_xay_dung/cong_cu_do_thi_ham_so_zo_math/mau/do_thi_nhan_truc_tiep.tex --out-dir quy_trinh_xay_dung/cong_cu_do_thi_ham_so_zo_math/_output --check
python scripts/zo_python.py quy_trinh_xay_dung/cong_cu_do_thi_ham_so_zo_math/zo_graph_build.py quy_trinh_xay_dung/cong_cu_do_thi_ham_so_zo_math/mau/do_thi_hop_chu_thich.tex --out-dir quy_trinh_xay_dung/cong_cu_do_thi_ham_so_zo_math/_output --check
```

Trong công việc thật, thay đường dẫn mẫu bằng đường dẫn nguồn đã sao chép và chọn `--out-dir` thuộc gói sản phẩm. Nếu bỏ `--out-dir`, PDF và SVG được đặt cạnh nguồn.

## 4. Tùy chọn

| Tùy chọn | Ý nghĩa |
| --- | --- |
| `--out-dir THU_MUC` | Chọn thư mục nhận PDF và SVG |
| `--check` | Kiểm PDF một trang, không chứa ảnh raster, có hai phông STIX; kiểm SVG hợp lệ, có `viewBox` và không tham chiếu tài nguyên ngoài |
| `--force` | Cho phép thay PDF/SVG cùng tên đã tồn tại |
| `--keep-build` | Giữ thư mục build tạm và in đường dẫn để chẩn đoán lỗi |

Mặc định công cụ không ghi đè. Khi một trong hai đầu ra đã tồn tại, hãy kiểm tra đúng nguồn và thư mục đích trước khi chạy lại với `--force`.

Nguồn phải nằm trong repository ZO Math. Công cụ tự tìm gốc repository từ vị trí của chính nó, nên lệnh vẫn hoạt động khi thư mục gọi lệnh thay đổi.

## 5. Dùng đầu ra trong học liệu

- HTML hoặc Quarto HTML: chèn tệp `.svg` và cung cấp nội dung thay thế phù hợp.
- Tài liệu in hoặc Quarto PDF: chèn tệp `.pdf` vector.
- Không dùng PNG thay hai đầu ra chuẩn nếu không có lí do riêng.
- Chú thích hình, ID và mô tả truy cập thuộc nguồn QMD hoặc nguồn nội dung của sản phẩm, không vẽ số hình vào SVG.

SVG chuyển từ chính PDF nên hai bản có cùng hình học. Glyph trong SVG có thể được chuyển thành path; mô tả ngữ nghĩa vẫn phải nằm trong học liệu.

## 6. Lỗi thường gặp

### Thiếu `lualatex` hoặc `pdf2svg`

Công cụ dừng sớm và nêu tên chương trình thiếu. Cài chương trình vào `PATH`, sau đó chạy lại đúng lệnh qua `scripts/zo_python.py`.

### Thiếu phông STIX hoặc gói TeX

Không đổi sang phông hệ thống. Kiểm tra `assets/fonts/` còn đủ các tệp STIX Two và đọc đoạn log cuối mà công cụ in. Dùng `--keep-build` khi cần giữ `.log` để chẩn đoán.

### Đầu ra đã tồn tại

Đây là bảo vệ mặc định. Xác nhận đúng đích rồi thêm `--force`; không xóa hoặc ghi đè hàng loạt.

### LuaLaTeX báo lỗi công thức

Kiểm tra cú pháp PGFPlots, dấu ngoặc, miền và việc tách nhánh. Không nối qua điểm loại hoặc tiệm cận chỉ để làm mã biên dịch.

### Nhãn bị cắt hoặc đường xuyên chữ

Dời nhãn trong nguồn sản phẩm, kiểm tra ở kích thước dùng thật, rồi mới điều chỉnh nền bảo vệ. Không tắt clipping toàn hình để cứu một nhãn đặt sai.

### SVG hoặc PDF không đạt `--check`

Không dùng đầu ra đó làm canonical. Đọc điều kiện thất bại, sửa nguồn hoặc môi trường, dựng lại từ nguồn; không chỉnh path SVG hay PDF bằng tay.

## 7. Chạy kiểm thử công cụ

Từ gốc repository:

```text
python scripts/zo_python.py quy_trinh_xay_dung/cong_cu_do_thi_ham_so_zo_math/kiem_thu/kiem_tra_cong_cu.py
```

Kiểm thử tạo đầu ra trong thư mục tạm riêng rồi dọn sau khi kết thúc. Nó không chuyển đổi R1-G01, dự án 100+ Hàm số hoặc tài sản canonical khác.

