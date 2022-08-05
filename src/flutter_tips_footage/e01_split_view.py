# encoding: utf-8

from manim import *


class E01Opening(Scene):
    def construct(self):
        # 大标题
        title = Text("Flutter小技巧", t2s={"Flutter小技巧": ITALIC}).scale(2)
        # 小标题
        subtitle = Text("分栏视图").next_to(title, DOWN)
        # 图标
        icon = (
            ImageMobject("assets/icon/flutter.png").scale(0.2).shift(UP * 5 + RIGHT * 5)
        )
        # 大标题
        self.play(Write(title), run_time=1)
        # 变颜色
        self.play(title.animate.set_color(BLUE), Create(subtitle), run_time=1)
        # 大小标题转换
        title_pos = title.get_center()
        self.play(
            title.animate.scale(0.5).move_to(UP * 3 + LEFT * 3).set_opacity(0.5),
            subtitle.animate.set_color(PINK).scale(1.5).move_to(title_pos),
            run_time=1,
        )
        self.wait()
        # 图片出现
        self.play(icon.animate.scale(1.5).move_to(subtitle.get_center() + DOWN * 2))
        self.wait()
        # 图片消失
        self.play(icon.animate.scale(0.5).move_to(title.get_center() + DOWN))
        self.wait()
        # 图片到右下角
        self.play(icon.animate.move_to(LEFT * 6 + DOWN * 3))
        self.play(icon.animate.rotate(TAU / 2))
        self.play(icon.animate.rotate(TAU / 2))
        self.wait(1)
