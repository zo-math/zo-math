# Bộ nguồn video Manim — Vì sao đồ thị hàm số được vẽ bằng hai trục vuông góc?

Bộ nguồn này được dựng từ bài luận Quarto `.qmd`:

`source/vi_sao_do_thi_duoc_ve_bang_hai_truc_vuong_goc.qmd`

Mục tiêu là tạo một quy trình mẫu cho các video ZO Math dạng “Vì sao...?”: bài luận → lời dẫn thu âm → kịch bản hoạt ảnh → mã Manim → bản đối chiếu để rà soát.

## Cấu trúc thư mục

```text
vi_sao_do_thi_hai_truc_vuong_goc_video/
├── 00_README.md
├── 01_loi_dan_thu_am.md
├── 02_kich_ban_hoat_anh.md
├── 03_bang_doi_chieu_loi_dan_hoat_anh.tex
├── 04_manim_scene.py
├── assets/
│   └── README.md
└── source/
    └── vi_sao_do_thi_duoc_ve_bang_hai_truc_vuong_goc.qmd
```

## Cách dùng khuyến nghị

### Bước 1. Đọc bài luận gốc

Đọc tệp `.qmd` trong thư mục `source/` để nắm mạch tư tưởng. Bài luận không dùng trực tiếp làm lời dẫn vì câu văn bài viết thường dài hơn câu văn thu âm.

### Bước 2. Thu âm từ tệp lời dẫn

Dùng:

`01_loi_dan_thu_am.md`

Đây là bản sạch để đọc. Người đọc không đọc các mã `[Sxx-yy]`. Các mã này chỉ dùng để dựng video.

### Bước 3. Dựng hoạt ảnh theo kịch bản

Dùng:

`02_kich_ban_hoat_anh.md`

Tệp này nói mỗi cảnh cần hiện gì, chuyển động ra sao, và mục tiêu sư phạm là gì. Khi sửa hoạt ảnh, ưu tiên sửa tệp này trước, rồi mới sửa Manim.

### Bước 4. Chạy Manim

Tệp mã:

`04_manim_scene.py`

Lệnh chạy đề xuất:

```bash
manim -pqh 04_manim_scene.py ViSaoDoThiHaiTrucVuongGoc
```

Trong đó:

- `-p` mở video sau khi render.
- `-q h` xuất chất lượng cao.
- Nếu cần bản nháp nhanh, dùng:

```bash
manim -pql 04_manim_scene.py ViSaoDoThiHaiTrucVuongGoc
```

### Bước 5. Rà soát bằng bản LaTeX đối chiếu

Dùng:

`03_bang_doi_chieu_loi_dan_hoat_anh.tex`

Tệp này dùng để in hoặc đọc song song: bên trái là lời dẫn, bên phải là hoạt ảnh. Đây không phải nguồn chính để sửa dài hạn. Nguồn chính vẫn là:

1. `01_loi_dan_thu_am.md`
2. `02_kich_ban_hoat_anh.md`
3. `04_manim_scene.py`

## Nguyên tắc sản xuất

Bộ nguồn này tách ba lớp:

```text
Lớp 1: Lời nói
Lớp 2: Hình ảnh
Lớp 3: Mã dựng hình
```

Không nên trộn ba lớp này vào một tệp duy nhất. Khi lời dẫn và Manim bị trộn quá chặt, mỗi lần sửa một câu nói sẽ dễ làm lệch hoạt ảnh, và mỗi lần sửa hoạt ảnh sẽ làm rối bản thu âm.

## Gợi ý nhịp video

Bản lời dẫn hiện tại phù hợp với video khoảng 8–10 phút nếu đọc chậm, rõ. Nếu muốn làm video ngắn 60–90 giây, nên cắt riêng từ các cảnh:

- S05: đặt $x$ lên trục ngang
- S06: dựng $y$ theo phương thẳng đứng
- S10: hai phương đo không lẫn vào nhau
- S12: câu trả lời cuối

## Ghi chú kỹ thuật

- Mã Manim không phụ thuộc vào ảnh ngoài.
- Tiếng Việt được dựng bằng `Text`, công thức được dựng bằng `MathTex`.
- Nếu máy thiếu font tiếng Việt, hãy đổi hằng `FONT_TEXT` trong `04_manim_scene.py`.
- Màu sắc đặt ở đầu tệp Manim để dễ đổi toàn bộ phong cách.
- Mã được viết thiên về dễ học, dễ sửa, không tối ưu cực đoan.
