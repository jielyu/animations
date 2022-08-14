# encoding: utf-8

from manim import *


class E02Samples(Scene):
    def construct(self):
        title = Text("flutter create").set_color(BLUE).move_to(UP * 3)
        self.play(Write(title))
        self.play(title.animate.scale(2))
        tips = Text("flutter create  --sample=<id> <your_app_name>")

        self.play(Write(tips))
        self.play(tips.animate.set_color(RED))
        self.wait()
        id_pos = tips.submobjects[22].get_center()

        id_info = Text("示例对应的ID").move_to(4 * LEFT + 2 * DOWN)
        id_arrow = Arrow(id_pos, id_info.get_right(), buff=0.7)
        self.play(Write(id_arrow))
        self.play(Create(id_info))
        self.play(id_info.animate.set_color(GREEN))
        self.wait()
        example = (
            Text("flutter create  --sample=material.FloatingActionButton.1 my_demo_app")
            .scale(0.5)
            .move_to(2 * RIGHT + 3 * DOWN)
        )
        ex_pos = tips.submobjects[28].get_center()
        ex_arrow = Arrow(ex_pos, example.get_top(), buff=0.7)
        self.play(Write(example))
        self.play(Write(ex_arrow))
        self.play(example.animate.set_color(YELLOW))
        self.wait()
