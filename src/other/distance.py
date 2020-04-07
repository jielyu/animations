from manimlib.imports import *
from itertools import chain

class E03Scene(GraphScene):
    CONFIG = {
        'x_min': -2,
        'x_max': 5,
        'x_axis_width': 7,
        'y_min': -1,
        'y_max': 5,
        'y_axis_height': 7,
        "graph_origin": 2.5 * DOWN + 2 * LEFT,
    }
    
    def disp_example(self, pts, paths, is_clear=True):
        axes = self.setup_axes(animate=True)
        dot_list, pt_list = [], []
        for p in pts:
            dot = Dot()
            dot.move_to(self.coords_to_point(*p))
            dot.set_color(RED)
            dot_list.append(dot)
            self.play(Write(dot))

            pt = TextMobject('({},{})'.format(p[0], p[1]))
            pt.move_to(self.coords_to_point(*p))
            pt.scale(0.6)
            pt.set_color(RED)
            pt.shift((RIGHT+DOWN)*0.3)
            self.play(Write(pt))
            pt_list.append(pt)
        self.play(*[FadeOut(pt) for pt in pt_list])

        result = TextMobject('0')
        result.shift(2*RIGHT)
        result.scale(2)
        result.set_color(GREEN)
        self.play(Write(result))
        arrow_paths = []
        for idx, p in enumerate(paths):
            if idx == 0:
                pt = TextMobject('({},{})'.format(p[0], p[1]))
                pt.move_to(self.coords_to_point(*p))
                pt.scale(0.6)
                pt.set_color(BLUE)
                self.play(Write(pt))
                continue
            arrow = Arrow(self.coords_to_point(*paths[idx-1]), self.coords_to_point(*p))
            arrow_paths.append(arrow)
            self.play(Write(arrow))

            pt = TextMobject('({},{})'.format(p[0], p[1]))
            pt.move_to(self.coords_to_point(*p))
            pt.scale(0.6)
            pt.set_color(BLUE)
            self.play(Write(pt))

            new_res = TextMobject(str(idx))
            new_res.shift(2*RIGHT)
            new_res.scale(2)
            new_res.set_color(GREEN)
            self.play(ReplacementTransform(result, new_res))
            result = new_res
        if is_clear is True:
            self.clear()
        self.wait()
        return axes, dot_list, arrow_paths, result


class Problem(E03Scene):
    def construct(self):
        pts = [[1,1],[3,4],[-1,0]]
        paths = [[1,1], [2,2], [3,3], [3,4], [2,3], [1,2], [0, 1], [-1, 0]]
        self.disp_example(pts, paths, False)

class Solution01(E03Scene):

    def disp_path_x(self, start, end, mark_len, offsize, text_offsize, mark_color=RED):
        arrow = DoubleArrow(self.coords_to_point(*start), self.coords_to_point(*end))
        sl = Line(color=mark_color)
        sl.set_length(mark_len)
        sl.rotate(90*DEGREES)
        sl.move_to(self.coords_to_point(*start))
        el = Line(color=mark_color)
        el.set_length(mark_len)
        el.rotate(90*DEGREES)
        el.move_to(self.coords_to_point(*end))
        self.play(*[Write(x.shift(offsize)) for x in [arrow, sl, el]])
        x_text = TextMobject(str(abs(end[0]-start[0])), color=BLUE)
        x_text.move_to(self.coords_to_point((start[0]+end[0])/2, (start[1]+end[1])/2))
        self.play(Write(x_text.shift(offsize+text_offsize)))

        return arrow, sl, el, x_text

    def disp_path_y(self, start, end, mark_len, offsize, text_offsize, mark_color=RED):
        arrow = DoubleArrow(self.coords_to_point(*start), self.coords_to_point(*end))
        sl = Line(color=mark_color)
        sl.set_length(mark_len)
        sl.move_to(self.coords_to_point(*start))
        el = Line(color=mark_color)
        el.set_length(mark_len)
        el.move_to(self.coords_to_point(*end))
        self.play(*[Write(x.shift(offsize)) for x in [arrow, sl, el]])
        y_text = TextMobject(str(abs(end[1]-start[1])), color=BLUE)
        y_text.move_to(self.coords_to_point((start[0]+end[0])/2, (start[1]+end[1])/2))
        self.play(Write(y_text.shift(offsize+RIGHT*0.3)))
        return arrow, sl, el, y_text
    
    def construct(self):
        pts = [[1,1],[3,4],[-1,0]]
        paths = [[1,1], [2,2], [3,3], [3,4], [2,3], [1,2], [0, 1], [-1, 0]]
        axes, dot_list, arrow_paths, result = self.disp_example(pts, paths, False)
        self.play(FadeOut(result))

        # from [1,1] -> [3,4]
        mark_len = 0.5
        offsize = DOWN*0.5
        arrow, sl, el, xt = self.disp_path_x([1,1], [3,1], mark_len, offsize, 0.3*DOWN)
        offsize = RIGHT*0.7
        arrow, sl, el, yt = self.disp_path_y([3,1], [3,4], mark_len, offsize, 0.3*RIGHT)

        max_text = TexMobject('max(', '-', ',', '-', ')')
        max_text.shift(RIGHT*3.5)
        self.play(Write(max_text))
        tmp1 = xt.copy()
        self.play(tmp1.move_to, max_text[1].get_center())
        self.play(ReplacementTransform(max_text[1], tmp1))
        tmp2 = yt.copy()
        self.play(tmp2.move_to, max_text[3].get_center())
        self.play(ReplacementTransform(max_text[3], tmp2))

        # from [3,4] -> [-1,0]
        mark_len = 0.5
        offsize = UP*0.5
        arrow, sl, el, xt = self.disp_path_x([3,4], [-1,4], mark_len, offsize, 0.3*UP)
        offsize = LEFT*0.7
        arrow, sl, el, yt = self.disp_path_y([-1,4], [-1,0], mark_len, offsize, 0.3*LEFT)

        max_text = TexMobject('max(', '-', ',', '-', ')')
        max_text.shift(LEFT*5.5)
        self.play(Write(max_text))
        tmp3 = xt.copy()
        self.play(tmp3.move_to, max_text[1].get_center())
        self.play(ReplacementTransform(max_text[1], tmp3))
        tmp4 = yt.copy()
        self.play(tmp4.move_to, max_text[3].get_center())
        self.play(ReplacementTransform(max_text[3], tmp4))

        # construct result
        result = TextMobject('7')
        result.shift(5*RIGHT+3*DOWN)
        result.scale(2)
        result.set_color(GREEN)
        self.play(Write(result))

        max1 = tmp2.copy()
        max2 = tmp4.copy()
        self.play(max1.move_to, result.get_center()+UL*0.5, max1.scale, 0.6,
                  max2.move_to, result.get_center()+UR*0.5, max2.scale, 0.6, run_time=2)
        self.wait()



