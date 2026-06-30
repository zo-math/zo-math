"""
04_manim_scene.py

Bài: Vì sao đồ thị hàm số được vẽ bằng hai trục vuông góc?
Mục tiêu: Mã Manim mẫu để dựng hoạt ảnh theo kịch bản 02_kich_ban_hoat_anh.md.

Cách chạy:
    manim -pqh 04_manim_scene.py ViSaoDoThiHaiTrucVuongGoc

Bản nháp nhanh:
    manim -pql 04_manim_scene.py ViSaoDoThiHaiTrucVuongGoc

Ghi chú:
- Tiếng Việt dùng Text.
- Công thức dùng MathTex.
- Mã này không cần assets ngoài.
- Khi dựng video thật, nên nhập file âm thanh lời dẫn vào phần mềm dựng video,
  rồi cắt/giãn từng cảnh theo các mã [Sxx-yy] trong 01_loi_dan_thu_am.md.
"""

from manim import *

# ============================================================
# 1. CẤU HÌNH CHUNG
# ============================================================

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30

# Màu ZO Math
ZO_RED = "#ef5350"
ZO_YELLOW = "#ffca28"
ZO_TEAL = "#1de8b5"

# Màu nền và chữ
BG = "#fbfaf7"
INK = "#222222"
MUTED = "#777777"
GRID = "#dddddd"

# Font chữ. Nếu máy không có DejaVu Sans, đổi tại đây.
FONT_TEXT = "DejaVu Sans"


# ============================================================
# 2. HÀM PHỤ TRỢ
# ============================================================

def f(x: float) -> float:
    """Hàm số chính của video."""
    return x**3 - 3*x


def fmt_num(value: float) -> str:
    """Định dạng số ngắn gọn để hiển thị trên bảng."""
    if abs(value) < 1e-9:
        value = 0
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.3f}".rstrip("0").rstrip(".")


def txt(
    content: str,
    size: int = 34,
    color: str = INK,
    weight: str = NORMAL,
    line_spacing: float = 0.9,
) -> Text:
    """Tạo Text tiếng Việt thống nhất toàn video."""
    return Text(
        content,
        font=FONT_TEXT,
        font_size=size,
        color=color,
        weight=weight,
        line_spacing=line_spacing,
    )


def formula(tex: str, size: int = 44, color: str = INK) -> MathTex:
    """Tạo công thức toán học thống nhất toàn video."""
    mob = MathTex(tex, color=color, font_size=size)
    return mob


def title_block(title: str, subtitle: str | None = None) -> VGroup:
    """Khối tiêu đề dùng cho cảnh mở hoặc chuyển phần."""
    main = txt(title, size=46, weight=BOLD)
    if subtitle:
        sub = txt(subtitle, size=28, color=MUTED)
        return VGroup(main, sub).arrange(DOWN, buff=0.35)
    return VGroup(main)


def make_axes(include_y_axis: bool = True) -> Axes:
    """Tạo hệ trục dùng cho đồ thị y = x^3 - 3x."""
    y_range = [-9, 9, 3] if include_y_axis else [-9, 9, 3]
    axes = Axes(
        x_range=[-3, 3, 1],
        y_range=y_range,
        x_length=9.2,
        y_length=5.8,
        tips=True,
        axis_config={
            "color": INK,
            "stroke_width": 2,
            "include_numbers": False,
        },
    )
    axes.set_z_index(1)
    return axes


def x_number_labels(axes: Axes, values: list[float]) -> VGroup:
    """Tạo nhãn số trên trục x cho các giá trị mẫu."""
    labels = VGroup()
    for x in values:
        label = txt(fmt_num(x), size=18, color=MUTED)
        label.next_to(axes.coords_to_point(x, 0), DOWN, buff=0.12)
        labels.add(label)
    return labels


def y_number_labels(axes: Axes, values: list[float]) -> VGroup:
    """Tạo nhãn số trên trục y."""
    labels = VGroup()
    for y in values:
        label = txt(fmt_num(y), size=18, color=MUTED)
        label.next_to(axes.coords_to_point(0, y), LEFT, buff=0.12)
        labels.add(label)
    return labels


def make_xy_table(scale: float = 0.78) -> VGroup:
    """Tạo bảng giá trị nhỏ bằng các Text đơn giản.

    Không dùng Table để mã dễ sửa và hạn chế lỗi font.
    """
    data = [
        (-2.5, -8.125),
        (-2.0, -2.000),
        (-1.5, 1.125),
        (-1.0, 2.000),
        (-0.5, 1.375),
        (0.0, 0.000),
        (0.5, -1.375),
        (1.0, -2.000),
        (1.5, -1.125),
        (2.0, 2.000),
        (2.5, 8.125),
    ]

    header_x = txt("x", size=24, weight=BOLD)
    header_y = txt("y", size=24, weight=BOLD)

    rows = VGroup(VGroup(header_x, header_y).arrange(RIGHT, buff=1.2))
    for x, y in data:
        row = VGroup(
            txt(fmt_num(x), size=22),
            txt(fmt_num(y), size=22),
        ).arrange(RIGHT, buff=0.8)
        rows.add(row)

    rows.arrange(DOWN, buff=0.12, aligned_edge=LEFT)

    # Khung bảng
    box = SurroundingRectangle(rows, buff=0.18, color=GRID, stroke_width=1.5)
    result = VGroup(box, rows).scale(scale)
    return result


def sample_values() -> list[float]:
    """Các giá trị x dùng trong bảng của bài luận."""
    return [-2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5]


def make_vertical_segments(axes: Axes, values: list[float]) -> VGroup:
    """Các đoạn thẳng đứng biểu diễn y tại từng mốc x."""
    segs = VGroup()
    for x in values:
        y = f(x)
        start = axes.coords_to_point(x, 0)
        end = axes.coords_to_point(x, y)
        color = ZO_TEAL if y >= 0 else ZO_RED
        seg = Line(start, end, color=color, stroke_width=4)
        segs.add(seg)
    return segs


def make_dots(axes: Axes, values: list[float], radius: float = 0.055) -> VGroup:
    """Các điểm (x, f(x))."""
    dots = VGroup()
    for x in values:
        dot = Dot(
            axes.coords_to_point(x, f(x)),
            radius=radius,
            color=INK,
        )
        dot.set_z_index(5)
        dots.add(dot)
    return dots


def scene_label(code: str) -> Text:
    """Nhãn cảnh nhỏ ở góc, dùng để đối chiếu khi dựng."""
    label = txt(code, size=18, color=MUTED)
    label.to_corner(UR, buff=0.25)
    return label


# ============================================================
# 3. SCENE CHÍNH
# ============================================================

class ViSaoDoThiHaiTrucVuongGoc(Scene):
    """Toàn bộ video trong một Manim Scene.

    Khi cần dựng chuyên nghiệp hơn, có thể tách mỗi hàm scene_XX
    thành một class riêng để render từng đoạn.
    """

    def construct(self):
        self.camera.background_color = BG

        self.scene_00_title()
        self.scene_01_question()
        self.scene_02_function()
        self.scene_03_input_output()
        self.scene_04_table()
        self.scene_05_x_axis()
        self.scene_06_vertical_segments()
        self.scene_07_endpoints()
        self.scene_08_curve()
        self.scene_09_y_axis()
        self.scene_10_read_point()
        self.scene_11_table_vs_graph()
        self.scene_12_answer()
        self.scene_13_outro()

    # --------------------------------------------------------
    # S00. TIÊU ĐỀ
    # --------------------------------------------------------
    def scene_00_title(self):
        self.clear()

        logo = txt("ZO Math", size=28, color=ZO_RED, weight=BOLD)
        logo.to_corner(UL, buff=0.45)

        question = title_block(
            "Vì sao đồ thị hàm số",
            "được vẽ bằng hai trục vuông góc?"
        )
        question.move_to(ORIGIN + UP * 0.3)

        eq = formula(r"y=f(x)", size=54, color=INK)
        eq.next_to(question, DOWN, buff=0.65)

        # VO [S00-01] - [S00-02]
        self.play(FadeIn(logo, shift=DOWN * 0.2), run_time=0.8)
        self.play(Write(question), run_time=1.6)
        self.play(FadeIn(eq, shift=UP * 0.15), run_time=0.8)
        self.wait(1.2)
        self.play(FadeOut(VGroup(logo, question, eq)), run_time=0.8)

    # --------------------------------------------------------
    # S01. ĐIỀU TƯỞNG NHƯ HIỂN NHIÊN
    # --------------------------------------------------------
    def scene_01_question(self):
        self.clear()
        self.add(scene_label("S01"))

        axes = make_axes(include_y_axis=True).scale(0.78)
        axes.move_to(ORIGIN + DOWN * 0.25)

        curve = axes.plot(lambda x: 0.35 * x**3 - x, x_range=[-2.4, 2.4], color=ZO_RED)
        curve.set_stroke(width=5)

        label_x = txt("trục ngang", size=24, color=MUTED).next_to(axes.x_axis, DOWN, buff=0.45)
        label_y = txt("trục dọc", size=24, color=MUTED).next_to(axes.y_axis, LEFT, buff=0.45)
        label_curve = txt("đường cong", size=24, color=ZO_RED).next_to(curve, UP, buff=0.25)

        # VO [S01-01] - [S01-03]
        self.play(Create(axes), run_time=1.2)
        self.play(Create(curve), run_time=1.3)
        self.play(FadeIn(label_x), FadeIn(label_y), FadeIn(label_curve), run_time=0.9)
        self.wait(0.6)

        group = VGroup(axes, curve, label_x, label_y, label_curve)
        self.play(group.animate.set_opacity(0.22), run_time=0.8)

        q = txt("Vì sao lại như vậy?", size=48, color=INK, weight=BOLD)
        q.move_to(ORIGIN)

        # VO [S01-04]
        self.play(Write(q), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(VGroup(group, q, *self.mobjects)), run_time=0.7)

    # --------------------------------------------------------
    # S02. HÀM SỐ ĐỒNG HÀNH
    # --------------------------------------------------------
    def scene_02_function(self):
        self.clear()
        self.add(scene_label("S02"))

        eq = formula(r"y=x^3-3x", size=76, color=INK)
        badges = VGroup(
            txt("dễ tính", size=26, color=INK),
            txt("có đổi chiều", size=26, color=INK),
            txt("đủ để quan sát", size=26, color=INK),
        ).arrange(RIGHT, buff=0.5)

        for b, c in zip(badges, [ZO_TEAL, ZO_YELLOW, ZO_RED]):
            rect = RoundedRectangle(
                corner_radius=0.15,
                width=b.width + 0.5,
                height=b.height + 0.28,
                color=c,
                stroke_width=2,
                fill_color=c,
                fill_opacity=0.12,
            )
            rect.move_to(b)
            b.add_to_back(rect)

        badges.next_to(eq, DOWN, buff=0.7)

        # VO [S02-01] - [S02-04]
        self.play(Write(eq), run_time=1.1)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in badges], lag_ratio=0.25), run_time=1.2)
        self.wait(1.0)

        self.play(
            eq.animate.scale(0.48).to_corner(UL, buff=0.45),
            FadeOut(badges),
            run_time=0.8,
        )
        self.wait(0.4)
        self.play(FadeOut(eq), FadeOut(*self.mobjects), run_time=0.5)

    # --------------------------------------------------------
    # S03. x LÀ CÂU HỎI, y LÀ CÂU TRẢ LỜI
    # --------------------------------------------------------
    def scene_03_input_output(self):
        self.clear()
        self.add(scene_label("S03"))

        x_mob = formula(r"x", size=68, color=ZO_TEAL).move_to(LEFT * 4.2)
        y_mob = formula(r"y", size=68, color=ZO_RED).move_to(RIGHT * 4.2)

        box = RoundedRectangle(corner_radius=0.18, width=3.2, height=1.35, color=INK, stroke_width=2)
        eq = formula(r"y=x^3-3x", size=42, color=INK).move_to(box)
        machine = VGroup(box, eq)

        arr1 = Arrow(x_mob.get_right(), box.get_left(), buff=0.25, color=INK, stroke_width=4)
        arr2 = Arrow(box.get_right(), y_mob.get_left(), buff=0.25, color=INK, stroke_width=4)

        caption = txt("Ta chọn x để hỏi; hàm số trả lời bằng y.", size=32, color=INK)
        caption.next_to(machine, DOWN, buff=0.85)

        # VO [S03-01] - [S03-04]
        self.play(FadeIn(x_mob), FadeIn(machine), run_time=0.8)
        self.play(GrowArrow(arr1), run_time=0.7)
        self.play(Indicate(machine, color=ZO_YELLOW), run_time=0.9)
        self.play(GrowArrow(arr2), FadeIn(y_mob), run_time=0.7)
        self.play(Write(caption), run_time=1.1)
        self.wait(1.0)
        self.play(FadeOut(VGroup(x_mob, y_mob, machine, arr1, arr2, caption, *self.mobjects)), run_time=0.7)

    # --------------------------------------------------------
    # S04. BẢNG GIÁ TRỊ
    # --------------------------------------------------------
    def scene_04_table(self):
        self.clear()
        self.add(scene_label("S04"))

        eq = formula(r"y=x^3-3x", size=46, color=INK).to_corner(UL, buff=0.45)
        table = make_xy_table(scale=0.82)
        table.move_to(ORIGIN)

        note = txt("Chính xác từng dòng,\nnhưng khó thấy hình dạng chung.", size=30, color=INK)
        note.next_to(table, RIGHT, buff=0.9)

        need = txt("Ta cần một hình ảnh.", size=42, color=ZO_RED, weight=BOLD)
        need.to_edge(DOWN, buff=0.7)

        # VO [S04-01] - [S04-05]
        self.play(FadeIn(eq), run_time=0.5)
        self.play(FadeIn(table, shift=UP * 0.2), run_time=1.1)
        self.wait(0.4)
        self.play(Write(note), run_time=1.0)
        self.wait(0.4)
        self.play(FadeIn(need, shift=UP * 0.2), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(VGroup(eq, table, note, need, *self.mobjects)), run_time=0.7)

    # --------------------------------------------------------
    # S05. ĐẶT x LÊN TRỤC NGANG
    # --------------------------------------------------------
    def scene_05_x_axis(self):
        self.clear()
        self.add(scene_label("S05"))

        values = sample_values()
        axes = make_axes(include_y_axis=False)
        x_axis_only = axes.x_axis
        x_axis_only.move_to(DOWN * 0.6)

        # Tạo nhãn x theo vị trí của một Axes đầy đủ để tận dụng coords_to_point.
        axes_for_position = make_axes(include_y_axis=False)
        axes_for_position.move_to(DOWN * 0.6)
        labels = x_number_labels(axes_for_position, values)

        title = txt("Các giá trị x được xếp theo thứ tự", size=36, weight=BOLD)
        title.to_edge(UP, buff=0.8)

        x_label = formula(r"x", size=42, color=ZO_TEAL)
        x_label.next_to(axes_for_position.x_axis.get_right(), RIGHT, buff=0.25)

        question = txt("Mỗi mốc x là một câu hỏi gửi vào hàm số.", size=30, color=INK)
        question.to_edge(DOWN, buff=0.75)

        # VO [S05-01] - [S05-04]
        self.play(Write(title), run_time=0.8)
        self.play(Create(axes_for_position.x_axis), FadeIn(x_label), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(l, shift=DOWN * 0.1) for l in labels], lag_ratio=0.05), run_time=1.4)
        self.play(Write(question), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(VGroup(title, axes_for_position.x_axis, x_label, labels, question, *self.mobjects)), run_time=0.7)

    # --------------------------------------------------------
    # S06. DỰNG y THEO PHƯƠNG THẲNG ĐỨNG
    # --------------------------------------------------------
    def scene_06_vertical_segments(self):
        self.clear()
        self.add(scene_label("S06"))

        values = sample_values()
        axes = make_axes(include_y_axis=False)
        axes.move_to(ORIGIN + DOWN * 0.2)

        x_labels = x_number_labels(axes, values)
        x_axis = axes.x_axis
        x_label = formula(r"x", size=42, color=ZO_TEAL).next_to(x_axis.get_right(), RIGHT, buff=0.25)

        segs = make_vertical_segments(axes, values)

        headline = txt("Biểu diễn y bằng độ cao có dấu", size=38, weight=BOLD)
        headline.to_edge(UP, buff=0.65)

        note = txt("Độ cao thay đổi,\nnhưng mốc x giữ nguyên.", size=32, color=INK)
        note.to_corner(DR, buff=0.75)

        # Một đoạn xiên mờ để gợi ý vì sao không chọn tùy tiện.
        sample_x = 1.5
        base = axes.coords_to_point(sample_x, 0)
        top = axes.coords_to_point(sample_x, f(sample_x))
        slanted = Line(base, top + RIGHT * 0.65, color=MUTED, stroke_width=3).set_opacity(0.3)
        cross = Cross(slanted, stroke_color=ZO_RED, stroke_width=4).scale(0.8)

        # VO [S06-01] - [S06-07]
        self.play(Write(headline), run_time=0.8)
        self.play(Create(x_axis), FadeIn(x_label), FadeIn(x_labels), run_time=0.9)
        self.play(LaggedStart(*[Create(s) for s in segs], lag_ratio=0.08), run_time=2.0)
        self.play(Write(note), run_time=0.9)
        self.play(Create(slanted), FadeIn(cross), run_time=0.9)
        self.wait(0.8)
        self.play(FadeOut(VGroup(headline, axes, x_labels, x_label, segs, note, slanted, cross, *self.mobjects)), run_time=0.7)

    # --------------------------------------------------------
    # S07. GIỮ LẠI ĐẦU MÚT
    # --------------------------------------------------------
    def scene_07_endpoints(self):
        self.clear()
        self.add(scene_label("S07"))

        values = sample_values()
        axes = make_axes(include_y_axis=False)
        axes.move_to(ORIGIN + DOWN * 0.2)

        x_labels = x_number_labels(axes, values)
        segs = make_vertical_segments(axes, values)
        dots = make_dots(axes, values)

        headline = txt("Giữ lại đầu mút: ta được điểm (x, y)", size=38, weight=BOLD)
        headline.to_edge(UP, buff=0.65)

        # Điểm mẫu x=2, y=2
        px = 2.0
        py = f(px)
        p = axes.coords_to_point(px, py)
        base = axes.coords_to_point(px, 0)

        dashed = DashedLine(base, p, color=MUTED, stroke_width=2)
        label = formula(r"(x,y)", size=42, color=ZO_RED).next_to(p, UR, buff=0.15)

        # VO [S07-01] - [S07-05]
        self.play(Write(headline), run_time=0.8)
        self.play(Create(axes.x_axis), FadeIn(x_labels), run_time=0.7)
        self.play(FadeIn(segs), run_time=0.7)
        self.play(FadeIn(dots), segs.animate.set_opacity(0.22), run_time=0.9)
        self.play(Create(dashed), FadeIn(label), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(VGroup(headline, axes, x_labels, segs, dots, dashed, label, *self.mobjects)), run_time=0.7)

    # --------------------------------------------------------
    # S08. NHIỀU ĐIỂM GỢI RA ĐƯỜNG CONG
    # --------------------------------------------------------
    def scene_08_curve(self):
        self.clear()
        self.add(scene_label("S08"))

        axes = make_axes(include_y_axis=False)
        axes.move_to(ORIGIN + DOWN * 0.2)

        values_sparse = sample_values()
        values_dense = [round(-2.5 + i * 0.1, 2) for i in range(51)]

        dots_sparse = make_dots(axes, values_sparse, radius=0.06)
        dots_dense = make_dots(axes, values_dense, radius=0.025).set_opacity(0.55)

        curve = axes.plot(lambda x: x**3 - 3*x, x_range=[-2.5, 2.5], color=ZO_RED)
        curve.set_stroke(width=5)

        headline = txt("Từ nhiều điểm, đường cong hiện ra", size=38, weight=BOLD)
        headline.to_edge(UP, buff=0.65)

        caption = txt("Đường cong là hình ảnh của rất nhiều câu trả lời.", size=30, color=INK)
        caption.to_edge(DOWN, buff=0.75)

        # VO [S08-01] - [S08-06]
        self.play(Write(headline), run_time=0.8)
        self.play(Create(axes.x_axis), run_time=0.6)
        self.play(FadeIn(dots_sparse), run_time=0.7)
        self.play(FadeIn(dots_dense), dots_sparse.animate.set_opacity(0.35), run_time=1.0)
        self.play(Create(curve), run_time=1.4)
        self.play(Write(caption), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(VGroup(headline, axes, dots_sparse, dots_dense, curve, caption, *self.mobjects)), run_time=0.7)

    # --------------------------------------------------------
    # S09. TRỤC y
    # --------------------------------------------------------
    def scene_09_y_axis(self):
        self.clear()
        self.add(scene_label("S09"))

        axes = make_axes(include_y_axis=True)
        axes.move_to(ORIGIN + DOWN * 0.15)

        curve = axes.plot(lambda x: x**3 - 3*x, x_range=[-2.5, 2.5], color=ZO_RED)
        curve.set_stroke(width=5)

        x_lab = formula(r"x", size=38, color=ZO_TEAL).next_to(axes.x_axis.get_right(), RIGHT, buff=0.2)
        y_lab = formula(r"y", size=38, color=ZO_RED).next_to(axes.y_axis.get_top(), UP, buff=0.2)

        headline = txt("Cần một trục đo chung cho y", size=38, weight=BOLD)
        headline.to_edge(UP, buff=0.65)

        # Một số nhãn y đặt cạnh điểm, cố ý cho rối.
        messy_labels = VGroup()
        for x in [-2, -1, 0.5, 1.5, 2.0]:
            y = f(x)
            lab = txt(f"y={fmt_num(y)}", size=20, color=MUTED)
            lab.next_to(axes.coords_to_point(x, y), RIGHT, buff=0.06)
            messy_labels.add(lab)

        origin_dot = Dot(axes.coords_to_point(0, 0), radius=0.07, color=ZO_YELLOW).set_z_index(6)
        origin_label = formula(r"(0,0)", size=34, color=INK).next_to(origin_dot, DL, buff=0.12)

        # VO [S09-01] - [S09-06]
        self.play(Write(headline), run_time=0.8)
        self.play(Create(axes.x_axis), Create(curve), FadeIn(x_lab), run_time=1.1)
        self.play(FadeIn(messy_labels), run_time=0.8)
        self.wait(0.3)
        self.play(FadeOut(messy_labels), run_time=0.5)
        self.play(Create(axes.y_axis), FadeIn(y_lab), run_time=0.9)
        self.play(FadeIn(origin_dot), Write(origin_label), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(VGroup(headline, axes, curve, x_lab, y_lab, origin_dot, origin_label, *self.mobjects)), run_time=0.7)

    # --------------------------------------------------------
    # S10. ĐỌC MỘT ĐIỂM
    # --------------------------------------------------------
    def scene_10_read_point(self):
        self.clear()
        self.add(scene_label("S10"))

        axes = make_axes(include_y_axis=True)
        axes.move_to(ORIGIN + DOWN * 0.1)

        curve = axes.plot(lambda x: x**3 - 3*x, x_range=[-2.5, 2.5], color=ZO_RED)
        curve.set_stroke(width=5)

        x_lab = formula(r"x", size=38, color=ZO_TEAL).next_to(axes.x_axis.get_right(), RIGHT, buff=0.2)
        y_lab = formula(r"y", size=38, color=ZO_RED).next_to(axes.y_axis.get_top(), UP, buff=0.2)

        px = 2.0
        py = f(px)
        p_point = axes.coords_to_point(px, py)
        p = Dot(p_point, radius=0.08, color=INK).set_z_index(7)

        v_line = DashedLine(axes.coords_to_point(px, 0), p_point, color=ZO_TEAL, stroke_width=3)
        h_line = DashedLine(axes.coords_to_point(0, py), p_point, color=ZO_RED, stroke_width=3)

        p_label = formula(r"P(2,2)", size=38, color=INK).next_to(p, UR, buff=0.18)
        read_x = txt("đọc x", size=26, color=ZO_TEAL).next_to(v_line, DOWN, buff=0.15)
        read_y = txt("đọc y", size=26, color=ZO_RED).next_to(h_line, LEFT, buff=0.15)

        headline = txt("Hai phương đo không lẫn vào nhau", size=38, weight=BOLD)
        headline.to_edge(UP, buff=0.65)

        # VO [S10-01] - [S10-06]
        self.play(Write(headline), run_time=0.8)
        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab), Create(curve), run_time=1.2)
        self.play(FadeIn(p), Write(p_label), run_time=0.8)
        self.play(Create(v_line), FadeIn(read_x), run_time=0.8)
        self.play(Create(h_line), FadeIn(read_y), run_time=0.8)
        self.wait(1.1)
        self.play(FadeOut(VGroup(headline, axes, x_lab, y_lab, curve, p, p_label, v_line, h_line, read_x, read_y, *self.mobjects)), run_time=0.7)

    # --------------------------------------------------------
    # S11. BẢNG VÀ ĐỒ THỊ
    # --------------------------------------------------------
    def scene_11_table_vs_graph(self):
        self.clear()
        self.add(scene_label("S11"))

        table = make_xy_table(scale=0.55)
        table.to_edge(LEFT, buff=0.8).shift(DOWN * 0.15)

        axes = make_axes(include_y_axis=True).scale(0.62)
        axes.to_edge(RIGHT, buff=0.75).shift(DOWN * 0.1)
        curve = axes.plot(lambda x: x**3 - 3*x, x_range=[-2.5, 2.5], color=ZO_RED)
        curve.set_stroke(width=4)

        dot = Dot(axes.coords_to_point(2, 2), radius=0.055, color=INK).set_z_index(7)

        left_title = txt("Bảng", size=34, weight=BOLD).next_to(table, UP, buff=0.25)
        right_title = txt("Đồ thị", size=34, weight=BOLD).next_to(axes, UP, buff=0.25)

        cap1 = txt("chính xác từng dòng", size=24, color=MUTED).next_to(table, DOWN, buff=0.25)
        cap2 = txt("hình ảnh tổng thể", size=24, color=MUTED).next_to(axes, DOWN, buff=0.25)

        arrow = Arrow(table.get_right() + RIGHT * 0.1, dot.get_left(), buff=0.2, color=ZO_YELLOW, stroke_width=4)

        # VO [S11-01] - [S11-04]
        self.play(FadeIn(left_title), FadeIn(table), FadeIn(cap1), run_time=0.9)
        self.play(FadeIn(right_title), Create(axes), Create(curve), FadeIn(cap2), run_time=1.1)
        self.play(GrowArrow(arrow), FadeIn(dot), run_time=0.8)
        self.play(Indicate(curve, color=ZO_YELLOW), run_time=0.9)
        self.wait(1.0)
        self.play(FadeOut(VGroup(table, axes, curve, dot, left_title, right_title, cap1, cap2, arrow, *self.mobjects)), run_time=0.7)

    # --------------------------------------------------------
    # S12. CÂU TRẢ LỜI CUỐI
    # --------------------------------------------------------
    def scene_12_answer(self):
        self.clear()
        self.add(scene_label("S12"))

        axes = make_axes(include_y_axis=True).scale(0.72)
        axes.move_to(ORIGIN + DOWN * 0.2)
        curve = axes.plot(lambda x: x**3 - 3*x, x_range=[-2.5, 2.5], color=ZO_RED)
        curve.set_stroke(width=5)
        bg_graph = VGroup(axes, curve).set_opacity(0.18)

        question = txt("Vì sao hai trục vuông góc?", size=42, weight=BOLD)
        question.to_edge(UP, buff=0.65)

        line1 = txt("Trục ngang: đi qua các giá trị x", size=34, color=INK)
        line2 = txt("Trục dọc: đo các giá trị y", size=34, color=INK)
        line3 = txt("Vuông góc: hai việc không lẫn vào nhau", size=34, color=ZO_RED, weight=BOLD)

        answer = VGroup(line1, line2, line3).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        answer.move_to(ORIGIN + DOWN * 0.1)

        # VO [S12-01] - [S12-06]
        self.play(FadeIn(bg_graph), Write(question), run_time=1.0)
        self.play(FadeIn(line1, shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(line2, shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(line3, shift=UP * 0.15), run_time=0.9)
        self.wait(1.3)
        self.play(FadeOut(VGroup(bg_graph, question, answer, *self.mobjects)), run_time=0.7)

    # --------------------------------------------------------
    # S13. OUTRO
    # --------------------------------------------------------
    def scene_13_outro(self):
        self.clear()
        self.add(scene_label("S13"))

        table_icon = make_xy_table(scale=0.38)
        table_icon.move_to(LEFT * 4)

        axes = make_axes(include_y_axis=True).scale(0.36)
        axes.move_to(ORIGIN)
        dots = make_dots(axes, sample_values(), radius=0.035)

        axes2 = make_axes(include_y_axis=True).scale(0.36)
        axes2.move_to(RIGHT * 4)
        curve = axes2.plot(lambda x: x**3 - 3*x, x_range=[-2.5, 2.5], color=ZO_RED)
        curve.set_stroke(width=4)

        arrow1 = Arrow(table_icon.get_right(), axes.get_left(), buff=0.25, color=MUTED)
        arrow2 = Arrow(axes.get_right(), axes2.get_left(), buff=0.25, color=MUTED)

        conclusion = txt("Đồ thị là hình ảnh của sự biến thiên.", size=42, color=INK, weight=BOLD)
        conclusion.to_edge(DOWN, buff=0.9)

        # VO [S13-01] - [S13-03]
        self.play(FadeIn(table_icon), run_time=0.7)
        self.play(GrowArrow(arrow1), Create(axes), FadeIn(dots), run_time=0.9)
        self.play(GrowArrow(arrow2), Create(axes2), Create(curve), run_time=1.0)
        self.play(Write(conclusion), run_time=1.1)
        self.wait(1.4)
        self.play(FadeOut(VGroup(table_icon, axes, dots, axes2, curve, arrow1, arrow2, conclusion, *self.mobjects)), run_time=0.9)
