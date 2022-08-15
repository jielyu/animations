# encoding: utf-8

from manim import *


class Creation(Scene):
    def construct(self):

        pos_list = [
            (-5.5, 2),
            (-1.83, 2),
            (1.83, 2),
            (5.5, 2),
            (-4.67, -2),
            (0, -2),
            (4.67, -2),
        ]
        effect_list = [
            Write,
            AddTextLetterByLetter,
            Create,
            Uncreate,
            DrawBorderThenFill,
            ShowIncreasingSubsets,
            ShowSubmobjectsOneByOne,
        ]
        boxes, names, samples = [], [], []
        for i, pos in enumerate(pos_list):
            box = Square(side_length=2).move_to(RIGHT * pos[0] + UP * pos[1])
            text = Text(effect_list[i].__name__).next_to(box, direction=UP).scale(0.5)
            self.add(box, text)
            boxes.append(box)
            names.append(text)
            samples.append(text.copy().move_to(box.get_center()).set_color(BLUE))
        for idx, effect in enumerate(effect_list):
            self.play(effect(samples[idx]))
        self.wait()
