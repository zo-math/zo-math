# Quy chuẩn sản xuất hình học ZO Math

**Phiên bản:** 0.1
**Trạng thái:** baseline production ban đầu, chốt từ spike đã nghiệm thu ngày 2026-10-01.

## 1. Phạm vi

Áp dụng cho hình học phẳng và hình học không gian mới được mô tả bằng YAML rồi
dựng qua TikZ, `tkz-euclide` hoặc `tikz-3dplot`. Không tự động hồi tố tài sản cũ.

Nguồn production:

- compiler và CLI: `scripts/zo_geometry.py`;
- checker: `scripts/zo_geometry_check.py`;
- self-test: `scripts/zo_geometry_selftest.py`;
- style: `assets/tex/zo-geometry-styles.tex`.

Nội dung trong `_audit/zo_geometry_spike/` là bằng chứng thiết kế và fixture hồi
quy; không còn là phụ thuộc chạy của học liệu.

## 2. Điểm vào vận hành

Mọi lệnh Python phải qua trình khởi chạy repository-local:

```text
python scripts/zo_python.py scripts/zo_geometry.py check <source.yml>
python scripts/zo_python.py scripts/zo_geometry.py compile <source.yml> <output.tex>
python scripts/zo_python.py scripts/zo_geometry.py build <source.yml> <output-prefix>
python scripts/zo_python.py scripts/zo_geometry_check.py --strict-labels <source.yml> <output.svg>
python scripts/zo_python.py scripts/zo_geometry_selftest.py -q
```

`build` sinh TeX, PDF vector, SVG, PNG kiểm tra và receipt `<output-prefix>.geometry.json`. Receipt khóa SHA-256 của nguồn YAML, compiler, style và bốn đầu ra. Với dự án QMD khai báo `extensions.geometry.assets`, `zo_qmd check` dùng receipt để phát hiện tài sản lỗi thời, còn `zo_qmd render` tự dựng lại trước khi dựng trang. PDF/SVG/PNG là đầu ra sinh,
không sửa tay.

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
