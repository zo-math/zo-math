"""Cấu hình video canonical của MVP."""

WIDTH = 1080
HEIGHT = 1920
ASPECT_RATIO = (9, 16)
FPS = 30

# Manim: frame_height giữ nguyên 8 đơn vị; frame_width suy ra từ tỉ lệ 9:16.
FRAME_HEIGHT = 8.0
FRAME_WIDTH = FRAME_HEIGHT * ASPECT_RATIO[0] / ASPECT_RATIO[1]
