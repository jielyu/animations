# encoding: utf-8

from manim import *


class Scene01(Scene):
    def construct(self):
        ffi = Text("FFI")
        ffi_all = Text("foreign function interface")
        self.play(Write(ffi))
        self.play(ffi.animate.set_color(BLUE))
        self.play(ReplacementTransform(ffi, ffi_all))
        self.play(ffi_all.animate.set_color(GREEN))
        self.wait()
        self.play(FadeOut(ffi_all, shift=DOWN))


class Scene03(Scene):
    def construct(self):
        rect = Rectangle(height=3, width=6)
        seperator = Line(1.5 * UP, 1.5 * DOWN)
        self.play(Write(rect))
        log_text = Text("逻辑").move_to(1.5 * LEFT)
        ui_text = Text("UI").move_to(1.5 * RIGHT)
        self.play(Write(log_text), Write(ui_text))
        self.play(log_text.animate.set_color(BLUE), ui_text.animate.set_color(GREEN))
        self.play(Write(seperator))
        self.play(*[obj.animate.set_color(RED) for obj in [seperator, rect]])
        self.wait()
        self.play(
            *[FadeOut(obj, shift=DOWN) for obj in [log_text, ui_text]],
            *[FadeOut(obj) for obj in [seperator, rect]]
        )
