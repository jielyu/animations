"""测试动画效果组件的使用"""

from manimlib.imports import *

class TransformExample(Scene):
    """变换效果实例"""

    def construct(self):
        # FadeXXX
        t1 = TextMobject("FadeIn")
        self.play(FadeIn(t1))
        self.wait()
        self.remove(t1)
        t1 = TextMobject("FadeInFromDown")
        self.play(FadeInFromDown(t1))
        self.wait()
        self.remove(t1)
        t1 = TextMobject("FadeOutAndShiftDown")
        self.play(FadeOutAndShiftDown(t1))
        self.wait()
        self.remove(t1)
        t1 = TextMobject("FadeInFromPoint")
        self.play(FadeInFromPoint(t1, ORIGIN))
        self.wait()
        self.remove(t1)
        t1 = TextMobject("FadeInFromLarge")
        self.play(FadeInFromLarge(t1))
        self.wait()
        self.remove(t1)
        # ShowCreation
        t1 = TextMobject("ShowCreation")
        self.play(ShowCreation(t1))
        self.wait()
        self.remove(t1)
        t1 = TextMobject("ShowCreationThenDestructionAround")
        self.play(ShowCreationThenDestructionAround(t1))
        self.wait()
        self.remove(t1)
        t1 = TextMobject("ShowPassingFlash")
        self.play(ShowPassingFlash(t1))
        self.wait()
        self.remove(t1)
        # UnCreate
        t1 = TextMobject("Uncreate")
        self.play(Uncreate(t1))
        self.wait()
        self.remove(t1)
        # DrawBorderThenFill
        t1 = TextMobject("DrawBorderThenFill")
        self.play(DrawBorderThenFill(t1))
        self.wait()
        self.remove(t1)
        # Write
        t1 = TextMobject("Write")
        self.play(Write(t1))
        self.wait()
        self.remove(t1)
        # Transform
        t1 = TextMobject("Transform")
        t2 = TextMobject("Change")
        self.play(Transform(t1, t2))
        self.wait()
        self.remove(t1, t2)
        # ReplacementTransform
        t1 = TextMobject("ReplacementTransform")
        t2 = TextMobject("Replace")
        self.play(ReplacementTransform(t1, t2))
        self.wait()
        self.remove(t1, t2)
        # MoveToTarget
        t1 = TextMobject("Origin")
        self.play(Write(t1))
        t1.generate_target()
        t1.target = TextMobject("MoveToTarget")
        t1.target.set_color(RED)
        t1.target.scale(3)
        t1.target.shift(LEFT * 2)
        self.play(MoveToTarget(t1), run_time=2)
        self.wait()
        self.remove(t1)