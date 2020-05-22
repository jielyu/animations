from manimlib.imports import *

import math

class CoorDemo(ThreeDScene):
    """三维坐标轴例程"""

    def construct(self):
        title = TextMobject('数轴')
        title.shift(UP*2.5+LEFT*2)
        self.play(Write(title), title.set_color, BLUE)
        # NUmberLine
        nl = NumberLine()
        self.play(Write(nl))
        self.wait()
        self.play(*[FadeOut(x) for x in [title, nl]])

        title = TextMobject('二维坐标')
        title.shift(UP*2.5+LEFT*2)
        self.play(Write(title), title.set_color, BLUE)
        # Axes
        coor = Axes()
        self.play(Write(coor))
        self.wait()
        self.play(*[FadeOut(x) for x in [title, coor]])

        title = TextMobject('平面')
        title.shift(UP*2.5+LEFT*2)
        self.play(Write(title), title.set_color, BLUE)
        # NumberPlane
        np = NumberPlane()
        self.play(Write(np))
        self.wait()
        self.play(*[FadeOut(x) for x in [title, np]])

        title = TextMobject('复数空间')
        title.shift(UP*2.5+LEFT*2)
        self.play(Write(title), title.set_color, BLUE)
        # ComplexPlane
        cp = ComplexPlane(
                        y_axis_config={"decimal_number_config":{"unit": "i"}},
                        number_line_config={"include_numbers":True}
                        )

        x_axis = cp[-2]
        y_axis = cp[-1]
        x_axis.set_color(RED)
        y_axis.set_color(PURPLE)
        x_labels = x_axis[0]
        x_labels.set_color(ORANGE)
        y_labels = y_axis[0]
        y_labels.set_color(YELLOW)
        for y in y_labels:
            y.rotate(-PI/2)

        x_label = TexMobject("x")
        x_label.move_to(cp.c2p(1.8,x_label.get_height()))
        y_label = TexMobject("y")
        y_label.move_to(cp.c2p(-3.8,3.8))
        self.add(cp,x_label,y_label)
        self.wait(2)
        self.play(*[FadeOut(x) for x in [title, cp, x_label, y_label]])

        title = TextMobject('三维坐标')
        title.shift(UP*2.5)
        self.play(Write(title), title.set_color, BLUE)
        # ThreeDAxes
        coor3d = ThreeDAxes()
        self.set_camera_orientation(phi=30 * DEGREES,theta=-30*DEGREES)
        self.play(Write(coor3d))
        self.wait()
        self.play(*[FadeOut(x) for x in [title, coor3d]])
        self.wait()


class Coor2dDemo(GraphScene):
    """二维坐标图实例"""

    CONFIG = {
        "x_min": -1,
        "x_max": 6,
        "x_axis_width": 10,
        "x_axis_label": "time",
        #"x_label_color": RED,
        "y_min": -1,
        "y_max": 20,
        "y_axis_height": 8,
        "y_axis_label": "amp",
        #"y_label_color": YELLOW,
        "y_tick_frequency": 1,
    }

    def func(self, x):
        return 3*math.sin(2*x)

    def construct(self):
        title = TextMobject('二维坐标轴')
        title.shift(UP*2.5)
        self.play(Write(title), title.set_color, BLUE)

        self.setup_axes(animate=True)
        graph = self.get_graph(self.func, color=GREEN, x_min=0, x_max=4)
        graph.move_to(DOWN)
        self.play(ShowCreation(graph), run_time=2)
        graph2 = graph.copy()
        self.play(graph2.shift, 2*UP)
        self.wait()


class Coor3dDemo(ThreeDScene):
    """三维场景实例"""

    def construct(self):
        title = TextMobject('三维坐标轴')
        title.shift(UP*2.5)
        self.play(Write(title), title.set_color, BLUE)

        axes = ThreeDAxes()
        self.add(axes)
        self.set_camera_orientation(phi=30 * DEGREES,theta=-30*DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1) 
        self.wait(4)