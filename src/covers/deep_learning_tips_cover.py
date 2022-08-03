# encoding: utf-8

from manim import *


class DeepLearningTipsCover(Scene):
    def construct(self):

        radius = 0.1
        num_units_list = [5, 8, 8, 4]
        color_list = [RED, GREEN, BLUE, YELLOW]
        all_units = []
        for idx, n in enumerate(num_units_list):
            units = []
            for i in range(n):
                units.append(
                    Circle(radius=radius)
                    .shift(
                        (i - n / 2) * UP * 0.8
                        + (idx - len(num_units_list) / 2) * RIGHT * 2
                    )
                    .set_color(color_list[idx])
                )
                # 画连接线
                if idx > 0:
                    for k in range(num_units_list[idx - 1]):
                        self.add(
                            Line(
                                all_units[idx - 1][k].get_center(),
                                units[i].get_center(),
                                color=color_list[idx],
                            )
                        )
                # 画箭头
                if idx == 0:
                    self.add(
                        Arrow(
                            units[i].get_center() + LEFT,
                            units[i].get_center() - radius * RIGHT,
                            color=color_list[idx],
                            buff=0,
                        )
                    )
                if idx == len(num_units_list) - 1:
                    self.add(
                        Arrow(
                            units[i].get_center() + radius * RIGHT,
                            units[i].get_center() + RIGHT,
                            color=color_list[idx],
                            buff=0,
                        )
                    )
            all_units.append(units)
            self.add(*units)
            # title = Text("深度学习tips")
            # self.add(title)
