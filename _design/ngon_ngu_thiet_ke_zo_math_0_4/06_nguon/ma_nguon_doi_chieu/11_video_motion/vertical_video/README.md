# ZO Video

Công cụ sản xuất video Toán học cho ZO Math. Hiện ở giai đoạn M0 (nền móng kỹ thuật).

Video chuẩn: dọc 9:16, 1080 × 1920, 30 fps. Engine: Manim Community; FFmpeg; LaTeX.

## Cài đặt

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev]"
```

## Render demo

```powershell
.\.venv\Scripts\manim render examples\vertical_demo\scene.py VerticalDemo --media_dir media
```

Kết quả: `media\videos\scene\1920p30\VerticalDemo.mp4` (kiểm tra bằng `ffprobe`).
