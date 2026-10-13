# Profile hình web — ứng viên, chưa khóa 0.5

Phạm vi: thực hiện yêu cầu ngày 08/10/2026 về khung bìa, đồ thị theo 0.4,
bảng biến thiên native và vùng chèn hình. Đây là nguồn tái sinh mẫu riêng.
Mẫu riêng là bằng chứng FB030; profile đã được nối opt-in vào nguồn HTML G01 ở FB031 và G02 ở DH_019. DH_021/QD_028 kiểm hai adapter canonical bằng bản dựng cô lập; không dùng HTML audit làm nguồn. Không đổi mặc định công cụ toàn repo hoặc suy PDF đã đồng bộ. Trạng thái và bằng chứng hiện hành ở 03 của bộ điều hành khóa; FB030–036 giữ lịch sử. Không thay CSS/JS đã duyệt trong một lượt chỉ cập nhật tài liệu.

## Hai vai trò không trộn

**Khung bìa:** SVG trong suốt; nền thuộc HTML/CSS. Ba dạng × hai kích thước
trong `frame-tokens.json`. Sáu nền lấy đúng token palette 0.4: đỏ sáng/tối,
vàng sáng/tối, xám sáng/tối. Sáng dùng red-1/yellow-1/gray-1; tối dùng
red-7/yellow-7/gray-8. Khung thu theo màn hình, không kéo méo hoặc cắt hình;
`object-fit:contain` giữ tỉ lệ. Chữ/trục có biến thể sáng/tối được dựng tại
nguồn, không dùng CSS invert. Bộ chọn trong mẫu là **công cụ biên soạn**,
không thêm tùy chọn cho người học. Sáu số đo là token của mẫu FB030 được duyệt, không là tùy chọn bắt người học chọn hoặc tuyên bố toàn Design 0.5 đã khóa.

**Vùng hình trong bài:** nằm trong vùng đọc sở hữu nhiệm vụ/lập luận, cùng
nhãn/tiêu đề/chú thích/alt. SVG giữ kích thước tự nhiên; bảng native theo cỡ
văn bản. Không dùng width:100% cho ảnh để lấp dòng. Nếu rộng hơn vùng đọc,
cuộn ngang cục bộ, có focus bằng bàn phím. Không ép thu nhỏ chữ.

## Nguồn và cách dựng

- Công cụ đồ thị hiện hành có lựa chọn `--style 0.4`; mặc định vẫn `v0.2`.
- `tex/zo_graph_v04.tex` là binding opt-in kế thừa lớp/nét/math fonts v0.2,
  đổi nền/miền tô sang token 0.4 và cỡ nhãn khoảng 17 CSS px ở SVG tự nhiên.
- `--surface transparent-light|transparent-dark` chỉ dùng cho bìa đã xem
  bố trí. Chặn point open/pagecolor: không được tự xóa lõi điểm rỗng để đạt
  “trong suốt”, vì sẽ làm sai toán. Các dạng đó cần giải pháp mask riêng
  trước khi dùng cho bìa. Profile không tự giải quyết mọi va chạm nhãn.
- `absolute-value-labels.json` chỉ dịch hộp chữ và chuẩn hóa cỡ tiêu đề nguồn
  của mẫu giá trị tuyệt đối; không dịch điểm/đường, không sửa nội dung nhãn.
  CLI yêu cầu mỗi nhãn khớp đúng một node, dịch trong [-60,60] pt.
- `zo_variation_html.py` nạp/kiểm đúng JSON hiện hành, dùng converter token
  của công cụ bảng rồi Pandoc MathML; bảng nhìn thấy là bảng native. Giữ số
  hàng, mọi giá trị, dấu, mũi tên, giới hạn một phía, cột loại và cờ cố ý sai.
  Nguồn Unicode được giữ trong `data-source-value`; điểm loại có aria-label
  nguyên văn và ký hiệu phân cách. Không bổ sung dữ kiện đạo hàm cho bảng
  chỉ hai hàng; hàng giá trị phẳng theo mẫu 0.4. Đường cũ SVG/Lua giữ nguyên.

```text
python scripts/zo_python.py scripts/zo_math_figure_specimen.py
python scripts/zo_python.py scripts/zo_math_figure_check.py
```

Đầu ra: `_audit/zo_math_figure_profile_2026-10-08/index.html`. Dựng lại cùng
phạm vi dùng `--force`. Chỉ khi nguồn hình và từng tài sản SVG/PDF đã kiểm
hash không đổi mới dùng thêm `--reuse-figures` để tái sinh HTML/CSS nhanh.
PDF vector ở audit là tài sản dựng hình/kiểm font, **không phải PDF học liệu**.
Không có đường dựng bình thường nào của G01 lấy audit này làm phụ thuộc.

## Điều kiện chuyển bước

Chủ trì xem HTML này trước. Sau khi duyệt mới hoàn thiện bộ hồi quy đa dạng
đồ thị, bộ nối QMD/native BBT và áp dụng thử vào G01; giữ ID/luồng/nội dung,
đối chiếu nguồn và kiểm lại toàn trang. Chưa tự khóa Design 0.5, dựng tám
PDF học liệu, chuyển G02, commit/push hoặc phát hành.

## Mốc chủ trì duyệt và tích hợp HTML — 08/10/2026

Chủ trì đã duyệt bảng thiết kế FB030 và giao bắt đầu tích hợp vào R1-G01.
Mẫu HTML riêng vẫn là bảng xem thiết kế, không thay nguồn giao diện đã chốt.
Sáu kích thước khung được duyệt trong phạm vi thử nghiệm này, không tự khóa 0.5.
`production-figures.css` là lớp opt-in riêng cho payload hình/bảng G01;
không sửa CSS khung trang, rail, vùng đọc hoặc controller đã duyệt.
Nguồn chọn hình/khung: `r1_g01/giao_dien/web_2027_figures.json`;
builder `scripts/zo_web_2027_figures.py`, adapter HTML
`scripts/zo_web_2027_production.py`. SVG web mới nằm riêng ở
`r1_g01/giao_dien/assets/figures_0_4/`; không ghi đè SVG/PDF lịch sử ở `hinh/`.
Các mô tả chờ duyệt phía trên ghi trạng thái khi dựng mẫu, không hạ lại mốc
duyệt này. Bằng chứng toàn trang và trạng thái nghiệm thu xem
`_audit/zo_g01_figure_integration_2026-10-08/README.md`.
