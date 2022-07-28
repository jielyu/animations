from manim import *


class MatrixExamples(Scene):
    def construct(self):
        m0 = Matrix([["\\pi", 0], [-1, 1]])
        m1 = IntegerMatrix(
            [[1.5, 0.0], [12, -1.3]], left_bracket="(", right_bracket=")"
        )
        m2 = DecimalMatrix(
            [[3.456, 2.122], [33.2244, 12.33]],
            element_to_mobject_config={"num_decimal_places": 2},
            left_bracket="\\{",
            right_bracket="\\}",
        )
        m3 = MobjectMatrix(
            [
                [Circle().scale(0.3), Square().scale(0.3)],
                [MathTex("\\pi").scale(2), Star().scale(0.3)],
            ],
            left_bracket="\\langle",
            right_bracket="\\rangle",
        )
        g = Group(m0, m1, m2, m3).arrange_in_grid(buff=2)
        self.add(g)
