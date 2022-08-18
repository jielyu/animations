# encoding: utf-8

from manim import *


class ScalarToTensor(ThreeDScene):
    def construct(self):

        question = Text("深度学习中的标量、向量、矩阵和张量有什么区别？").scale(0.8)
        self.play(Write(question))
        self.play(question.animate.set_color(RED))
        self.wait(2)
        self.play(FadeOut(question))

        scalar_ch = Text("标量")
        scalar_en = Text("Scalar")
        scalar_label = VGroup(scalar_ch, scalar_en)
        scalar_label.arrange(DOWN, buff=0.5)
        self.play(Write(scalar_label))
        text = (
            Text("标量是一个数字, 维度是0", t2c={"标量": BLUE})
            .next_to(scalar_label, DOWN)
            .scale(0.5)
        )
        self.play(FadeIn(text, shift=UP), scalar_ch.animate.set_color(BLUE))
        self.play(text.animate.set_color(RED))
        self.wait(2)
        self.play(
            scalar_label.animate.move_to(UP * 3 + LEFT * 5), FadeOut(text, shift=DOWN)
        )
        scalar = DecimalNumber(3.14).move_to(UP + LEFT * 3)
        scalar_arrow = Arrow(scalar_en.get_center(), scalar.get_center(), buff=0.7)
        self.play(Create(scalar), Write(scalar_arrow))
        self.wait()

        scalar_ch = Text("向量")
        scalar_en = Text("Vector")
        scalar_label = VGroup(scalar_ch, scalar_en)
        scalar_label.arrange(DOWN, buff=0.5)
        self.play(Write(scalar_label))
        text = (
            Text("向量是数字序列, 维度是1", t2c={"向量": BLUE})
            .next_to(scalar_label, DOWN)
            .scale(0.5)
        )
        self.play(FadeIn(text, shift=UP))
        self.play(text.animate.set_color(RED))
        self.wait(2)
        self.play(
            scalar_label.animate.move_to(UP * 3 + RIGHT * 5), FadeOut(text, shift=DOWN)
        )
        vector = m0 = Matrix([[0], [1]]).move_to(UP + RIGHT * 3)
        vector_arrow = Arrow(scalar_en.get_center(), vector.get_center(), buff=0.7)
        self.play(Write(vector), Write(vector_arrow))

        scalar_ch = Text("矩阵")
        scalar_en = Text("Matrix")
        scalar_label = VGroup(scalar_ch, scalar_en)
        scalar_label.arrange(DOWN, buff=0.5)
        self.play(Write(scalar_label))
        text = (
            Text("矩阵是数字表格, 维度是2", t2c={"矩阵": BLUE})
            .next_to(scalar_label, DOWN)
            .scale(0.5)
        )
        self.play(FadeIn(text, shift=UP))
        self.play(text.animate.set_color(RED))
        self.wait(2)
        self.play(
            scalar_label.animate.move_to(DOWN * 3 + LEFT * 5), FadeOut(text, shift=UP)
        )
        matrix = m0 = Matrix([[1, "\pi"], [0, 1]]).move_to(DOWN + LEFT * 3)
        matrix_arrow = Arrow(scalar_en.get_center(), matrix.get_center(), buff=0.9)
        self.play(Write(matrix), Write(matrix_arrow))

        scalar_ch = Text("张量")
        scalar_en = Text("Tensor")
        scalar_label = VGroup(scalar_ch, scalar_en)
        scalar_label.arrange(DOWN, buff=0.5)
        self.play(Write(scalar_label))
        text = (
            Text("张量是多维数表, 维度大于2", t2c={"张量": BLUE})
            .next_to(scalar_label, DOWN)
            .scale(0.5)
        )
        self.play(FadeIn(text, shift=UP))
        self.play(text.animate.set_color(RED))
        self.wait(2)
        self.play(
            scalar_label.animate.move_to(DOWN * 3 + RIGHT * 5), FadeOut(text, shift=UP)
        )
        tensor = (
            Prism([2, 2, 2], fill_color=GREEN)
            .move_to(DOWN + RIGHT * 3)
            .rotate(TAU / 8)
            .scale(0.7)
        )
        tensor_arrow = Arrow(scalar_en.get_center(), tensor.get_center(), buff=0.9)
        self.play(Write(tensor), Write(tensor_arrow))
        self.wait()
