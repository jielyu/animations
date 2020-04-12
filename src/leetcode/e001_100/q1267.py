"""
Q1267
"""

from manimlib.imports import *
from itertools import chain

class BasicScene(Scene):
    def disp_input(self, server):
        # create rectangles and numbers
        rect_list2d, text_list2d = [], []
        for i, row in enumerate(server):
            for j, col in enumerate(row):
                rect = Rectangle(height=1, width=1).shift(RIGHT*j+DOWN*i)
                rect_list2d.append(rect)
                self.play(Write(rect), run_time=0.5)

                t = TexMobject(str(col))
                t.move_to(rect.get_center())
                self.play(Write(t), run_time=0.5)
                text_list2d.append(t)
        rect_vg = VGroup(*rect_list2d)
        text_vg = VGroup(*text_list2d)
        self.play(rect_vg.shift, UL*2, text_vg.shift, UL*2)
        # mark servers
        for i, row in enumerate(server):
            for j, col in enumerate(row):
                idx = i*len(server[i])+j
                if col > 0:
                    self.play(text_vg[idx].set_color, BLUE)
        return rect_vg, text_vg

class Problem(BasicScene):

    def construct(self):
        server = [[1,1,0,0],[0,0,1,0],[0,0,1,0],[0,0,0,1]]
        # create rectangles and numbers
        rect_vg, text_vg = self.disp_input(server)

        # mark servers which can comunicate with others
        m1 = Ellipse().move_to((text_vg[0].get_center() + text_vg[1].get_center())/2)
        self.play(Write(m1))
        m2 = Ellipse(width=1, height=2).move_to((text_vg[6].get_center() + text_vg[10].get_center())/2)
        self.play(Write(m2))
        r = Rectangle(height=1, width=1).move_to(text_vg[15].get_center())
        self.play(r.set_color, YELLOW)

        # display result
        indexes = [0, 1, 6, 10]
        ret = TextMobject('0')
        ret.scale(2).set_color(GREEN)
        ret.move_to(rect_vg.get_center() + 4*LEFT)
        self.play(Write(ret))
        for i, idx in enumerate(indexes):
            new_ret = TextMobject(str(i+1))
            new_ret.scale(2).set_color(GREEN)
            new_ret.move_to(rect_vg.get_center() + 4*LEFT)
            tmp = text_vg[idx].copy()
            self.play(tmp.move_to, ret.get_center())
            self.play(FadeOut(tmp), ReplacementTransform(ret, new_ret))
            ret = new_ret


class Solution01(BasicScene):

    def construct(self):
        server = [[1,1,0,0],[0,0,1,0],[0,0,1,0],[0,0,0,1]]
        # create rectangles and numbers
        rect_vg, text_vg = self.disp_input(server)
        self.play(rect_vg.shift, DOWN+RIGHT, text_vg.shift, DOWN+RIGHT)
        
        # 行累加
        m, n = len(server), len(server[0])
        row_vg = VGroup(*[rect_vg[i*n].copy() for i in range(m)])
        row_sum = [0 for i in range(m)]
        row_sum_text = [0 for i in range(m)]
        self.play(row_vg.shift, LEFT*1.5)
        for i, row in enumerate(server):
            row_text = TextMobject('0')
            row_text.move_to(row_vg[i].get_center())
            self.play(Write(row_text))
            for j, col in enumerate(row):
                if col > 0:
                    tmp = text_vg[i*n+j].copy()
                    self.play(tmp.move_to, row_vg[i].get_center())
                    row_sum[i] += 1
                    new_row_text = TextMobject(str(row_sum[i]))
                    new_row_text.move_to(row_vg[i].get_center())
                    self.play(FadeOut(tmp), ReplacementTransform(row_text, new_row_text))
                    row_text = new_row_text
            row_sum_text[i] = row_text
        # 列累加
        col_vg = VGroup(*[rect_vg[j].copy() for j in range(n)])
        col_sum = [0 for j in range(n)]
        col_sum_text = [0 for j in range(n)]
        self.play(col_vg.shift, UP*1.5)
        for j in range(n):
            col_text = TextMobject('0')
            col_text.move_to(col_vg[j].get_center())
            self.play(Write(col_text))
            for i in range(m):
                if server[i][j] > 0:
                    tmp = text_vg[i*n+j].copy()
                    self.play(tmp.move_to, col_vg[j].get_center())
                    col_sum[j] += 1
                    new_col_text = TextMobject(str(col_sum[j]))
                    new_col_text.move_to(col_vg[j].get_center())
                    self.play(FadeOut(tmp), ReplacementTransform(col_text, new_col_text))
                    col_text = new_col_text
            col_sum_text[j] = col_text

        # 接受>1的行，检查等于1的行
        ret = 0
        ret_text = TextMobject(str(ret))
        ret_text.move_to(row_vg.get_center()+LEFT*2)
        self.play(Write(ret_text))
        for i, row in enumerate(server):
            if row_sum[i] > 1:
                ret += row_sum[i]
                tmp = row_sum_text[i].copy()
                self.play(tmp.move_to, ret_text.get_center())
                new_ret_text = TextMobject(str(ret))
                new_ret_text.move_to(row_vg.get_center()+LEFT*2)
                self.play(FadeOut(tmp), ReplacementTransform(ret_text, new_ret_text))
                ret_text = new_ret_text
            elif row_sum[i] == 1:
                for j, col in enumerate(row):
                    if col > 0 and col_sum[j] > 1:
                        ret += col
                        tmp = row_sum_text[i].copy()
                        self.play(tmp.move_to, ret_text.get_center())
                        new_ret_text = TextMobject(str(ret))
                        new_ret_text.move_to(row_vg.get_center()+LEFT*2)
                        self.play(FadeOut(tmp), ReplacementTransform(ret_text, new_ret_text))
                        ret_text = new_ret_text

                
