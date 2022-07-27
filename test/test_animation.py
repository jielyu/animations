"""测试动画效果组件的使用"""

from manim import *


class TransformExample(Scene):
    """变换效果实例"""

    def construct(self):
        # FadeXXX
        t1 = Text("FadeIn")
        self.play(FadeIn(t1))
        self.wait()
        self.remove(t1)
        t1 = Text("FadeInFromDown")
        self.play(FadeIn(t1))
        self.wait()
        self.remove(t1)
        t1 = Text("FadeOutAndShiftDown")
        self.play(FadeOut(t1))
        self.wait()
        self.remove(t1)
        t1 = Text("FadeInFromPoint")
        # self.play(FadeIn(t1, ORIGIN))
        self.play(FadeIn(t1))
        self.wait()
        self.remove(t1)
        t1 = Text("FadeInFromLarge")
        self.play(FadeIn(t1))
        self.wait()
        self.remove(t1)
        # ShowCreation
        t1 = Text("ShowCreation")
        self.play(Create(t1))
        self.wait()
        self.remove(t1)
        t1 = Text("ShowCreationThenDestructionAround")
        self.play(Create(t1))
        self.wait()
        self.remove(t1)
        t1 = Text("ShowPassingFlash")
        self.play(ShowPassingFlash(t1))
        self.wait()
        self.remove(t1)
        # UnCreate
        t1 = Text("Uncreate")
        self.play(Uncreate(t1))
        self.wait()
        self.remove(t1)
        # DrawBorderThenFill
        t1 = Text("DrawBorderThenFill")
        self.play(DrawBorderThenFill(t1))
        self.wait()
        self.remove(t1)
        # Write
        t1 = Text("Write")
        self.play(Write(t1))
        self.wait()
        self.remove(t1)
        # Transform
        t1 = Text("Transform")
        t2 = Text("Change")
        self.play(Transform(t1, t2))
        self.wait()
        self.remove(t1, t2)
        # ReplacementTransform
        t1 = Text("ReplacementTransform")
        t2 = Text("Replace")
        self.play(ReplacementTransform(t1, t2))
        self.wait()
        self.remove(t1, t2)
        # MoveToTarget
        t1 = Text("Origin")
        self.play(Write(t1))
        t1.generate_target()
        t1.target = Text("MoveToTarget")
        t1.target.set_color(RED)
        t1.target.scale(3)
        t1.target.shift(LEFT * 2)
        self.play(MoveToTarget(t1), run_time=2)
        self.wait()
        self.remove(t1)
