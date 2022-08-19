# encoding: utf-8

from manim import *


class Scene01(Scene):
    def construct(self):
        ocv = Text("OpenCV").shift(RIGHT * 2)
        flt = Text("Flutter").shift(LEFT * 2)
        ocv_icon = (
            ImageMobject("assets/icon/opencv.png").move_to(UP * 6 + RIGHT * 2).scale(3)
        )
        flt_icon = (
            ImageMobject("assets/icon/flutter.png")
            .scale(0.3)
            .move_to(RIGHT * 6 + DOWN * 1)
        )
        self.add(ocv_icon)
        self.play(flt_icon.animate.move_to(LEFT * 2 + DOWN * 1))
        flt.next_to(flt_icon, direction=DOWN)
        self.play(Write(flt))
        self.play(
            ocv_icon.animate.move_to(RIGHT * 2 + DOWN * 1.4),
            flt.animate.set_color(BLUE),
        )
        plus = Text("+").scale(2).move_to(DOWN * 1)
        self.play(FadeIn(plus))
        self.play(plus.animate.set_color(YELLOW))
        self.wait()
        self.play(
            flt_icon.animate.move_to(LEFT * 8 + DOWN * 1),
            FadeOut(plus),
            FadeOut(flt),
            ocv_icon.animate.move_to(RIGHT * 2 + DOWN * 6),
        )


class Scene01_2(Scene):
    def construct(self):
        cmd = Text(
            "python platforms/osx/build_framework.py osx --macos_archs x86_64,arm64",
            t2c={"python": YELLOW, "x86_64": GREEN, "arm64": BLUE},
        ).scale(0.6)
        self.play(AddTextLetterByLetter(cmd))
        self.wait()
