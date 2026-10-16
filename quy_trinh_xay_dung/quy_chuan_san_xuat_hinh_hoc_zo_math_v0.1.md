# Quy chuẩn sản xuất hình học ZO Math

**Phiên bản:** 0.1
**Trạng thái:** baseline production ban đầu, chốt từ spike đã nghiệm thu ngày 2026-10-01.

## 1. Phạm vi

Áp dụng cho hình học phẳng và hình học không gian mới được mô tả bằng YAML rồi
dựng qua TikZ, `tkz-euclide` hoặc `tikz-3dplot`. Không tự động hồi tố tài sản cũ.

Nguồn production:

- bộ độc lập: `../zo_math_graphics` (hoặc `ZO_MATH_GRAPHICS_ROOT`);
- CLI: `zo_geometry.py` ở gốc bộ công cụ; compiler nguyên byte ở `geometry/zo_geometry.py`;
- checker: `geometry/zo_geometry_check.py`;
- self-test: `tests/zo_geometry_selftest.py`;
- style: `assets/tex/zo-geometry-styles.tex` của bộ công cụ;
- adapter trong repo nội dung: `scripts/zo_graphics.py`.

Fixture hồi quy được quản lý tại `tests/fixtures/geometry/` của bộ công cụ,
helper ma trận tại `geometry/zo_geometry_stress.py`; self-test chỉ gọi
compiler/checker và style canonical. Nguồn YAML và sản phẩm TEX/PDF/SVG/PNG,
receipt của từng bài vẫn giữ trong dự án `zo_math`. Chỉ fixture nội bộ được
chuyển theo bộ kiểm, không mang tài nguyên học liệu đang sử dụng sang đó.
Nội dung trong `_audit/zo_geometry_spike/` là bằng chứng
thiết kế lịch sử, không là đầu vào biên dịch hoặc kiểm thử chính thức.

## 2. Điểm vào vận hành

Mọi lệnh Python phải qua trình khởi chạy repository-local:

```text
python scripts/zo_python.py scripts/zo_graphics.py geometry check <source.yml>
python scripts/zo_python.py scripts/zo_graphics.py geometry compile <source.yml> <output.tex>
python scripts/zo_python.py scripts/zo_graphics.py geometry build <source.yml> <output-prefix>
python scripts/zo_python.py scripts/zo_graphics.py geometry-check --strict-labels <source.yml> <output.svg>
python scripts/zo_python.py scripts/zo_graphics.py geometry-test -q
```

`build` sinh TeX, PDF vector, SVG, PNG kiểm tra và receipt `<output-prefix>.geometry.json`. Receipt khóa SHA-256 của nguồn YAML, compiler, style và bốn đầu ra. Với dự án QMD khai báo `extensions.geometry.assets`, `zo_qmd check` dùng receipt để phát hiện tài sản lỗi thời, còn `zo_qmd render` tự dựng lại trước khi dựng trang. PDF/SVG/PNG là đầu ra sinh,
không sửa tay.

Đường dẫn nguồn/đích tương đối được hiểu theo thư mục gọi. Công cụ ngoài repo
tự cấp đường tìm style/phông khi dựng; có thể đọc YAML trong `zo_math` và
ghi sản phẩm vào đích dự án chỉ định. Lượt di dời 15/10/2026 giữ nguyên byte
compiler/style để receipt và hình cũ tiếp tục được kiểm đúng hash; không sửa
receipt hoặc tái sinh sản phẩm hiện hành chỉ vì đổi chỗ công cụ.

## 3. Bất biến thị giác

- dùng STIX Two Text và STIX Two Math;
- nét thấy, nét khuất, nét nhấn, điểm và nhãn lấy từ style dùng chung;
- không dùng màu chỉ để trang trí; nét đứt đã đủ phân biệt thì giữ màu trung tính,
  trừ khi đối tượng đồng thời cần nhấn mạnh;
- nhãn phải ưu tiên tránh đường và điểm; chỉ dùng nền cục bộ khi không còn neo sạch;
- cạnh thấy được vẽ sau cấu trúc khuất hoặc nằm trong khối;
- mọi ký hiệu góc, kể cả góc vuông, chỉ có đường biên và tuyệt đối không tô nền.

## 4. Kiểm định bắt buộc

Nguồn mới phải qua validator, checker nhãn nghiêm ngặt, biên dịch PDF/SVG và
kiểm tra trực quan ở kích thước dùng thật. Trường hợp suy biến phải bị từ chối.
Kết quả tự động không thay nghiệm thu của con người.

## 5. Giới hạn phiên bản 0.1

Auto-visibility chỉ hỗ trợ các họ đã có trong compiler. Tối ưu nhãn dùng tập neo
hữu hạn và ước lượng hộp chữ; hình dày đặc vẫn cần kiểm tra trực quan. Việc thêm
họ hình hoặc thay đổi token thị giác phải bổ sung fixture, self-test và bằng chứng
nghiệm thu trước khi nâng baseline.
