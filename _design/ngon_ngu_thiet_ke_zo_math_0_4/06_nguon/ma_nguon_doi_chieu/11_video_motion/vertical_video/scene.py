from manim import (
    DOWN,
    UP,
    MathTex,
    Scene,
    Text,
    VGroup,
    Write,
    config,
)

from zo_video import config as zo

config.pixel_width = zo.WIDTH
config.pixel_height = zo.HEIGHT
config.frame_rate = zo.FPS
config.frame_height = zo.FRAME_HEIGHT
config.frame_width = zo.FRAME_WIDTH
config.background_color = "#101820"


class VerticalDemo(Scene):
    def construct(self):
        title = Text("ZO Math", font_size=96)
        formula = MathTex("y = x^2", font_size=120)
        group = VGroup(title, formula).arrange(DOWN, buff=1)
        self.play(Write(title))
        self.play(Write(formula))
        self.wait(1)
