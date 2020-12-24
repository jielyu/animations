"""测试场景组件的使用"""

from manimlib.imports import *

class Graph2DExample(GraphScene):
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
        return x**2

    def construct(self):
        self.setup_axes(animate=True)
        graph = self.get_graph(self.func, color=GREEN, x_min=0, x_max=4)
        graph.move_to(DOWN)
        self.play(ShowCreation(graph), run_time=2)
        self.wait()

class ThreeDExample(ThreeDScene):
    """三维场景实例"""

    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)
        self.set_camera_orientation(phi=80 * DEGREES,theta=-60*DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1) 
        self.wait()

class MovingCameraExample(MovingCameraScene):
    """运动摄像机实例"""

    def construct(self):
        t = TextMobject('Hello, World')
        self.play(Write(t))
        self.camera.set_frame_center(UR*3)
        self.wait()

class SampleSpaceExample(SampleSpaceScene):
    """概率采样空间实例"""

    def construct(self):
        ss = self.get_sample_space()
        self.play(Write(ss))
        self.wait()

class ZoomedExample(ZoomedScene):
    """缩放摄像机实例"""

    def construct(self):
        t = TextMobject('Hello, World')
        self.play(Write(t))
        self.activate_zooming()
        self.wait(5)

class VectorExample(LinearTransformationScene):
    """向量场实例"""

    def construct(self):
        self.add_vector(UR*2)
        self.add_title('Hello')
        self.wait(2)


class ConfigSceneExample(Scene):
    """CONFIG参数修改设置实例"""

    CONFIG = {
        "camera_config": {
            "frame_rate": 30, 
       },
    }
    def construct(self):
        t = TexMobject("A", "{B", "\\over", "C}", "D", "E")
        t[0].set_color(RED)
        t[1].set_color(ORANGE)
        t[2].set_color(YELLOW)
        t[3].set_color(GREEN)
        t[4].set_color(BLUE)
        t[5].set_color(BLUE)
        self.play(Write(t))
        self.wait(2)
        t.shift(LEFT*2)
        self.play(Write(t))
        self.wait()

class UpdateExample(Scene):
    """更新器设置实例"""

    def construct(self):
        dot = Dot()
        text = TextMobject('Updater')
        text.next_to(dot, RIGHT*2, buff=SMALL_BUFF)
        self.add(dot, text)

        def update(obj):
            obj.next_to(dot, RIGHT*2, buff=SMALL_BUFF)
        text.add_updater(update)
        self.add(text)
        
        self.play(dot.shift, UP * 2)
        self.wait()
        self.play(dot.shift, DOWN * 2, rate_func=smooth)
        self.wait()
        text.remove_updater(update)
        self.wait()

class CoorExample(Scene):
    """三维坐标轴例程"""

    def construct(self):
        # NUmberLine
        nl = NumberLine()
        self.play(Write(nl))
        self.wait()
        self.remove(nl)

        # Axes
        coor = Axes()
        self.play(Write(coor))
        self.wait()
        self.remove(coor)

        # ThreeDAxes
        coor3d = ThreeDAxes()
        self.play(Write(coor3d))
        self.wait()
        self.remove(coor3d)

        # NumberPlane
        np = NumberPlane()
        self.play(Write(np))
        self.wait()
        self.remove(np)

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
        print(cp.c2p(-1,1))

        self.add(cp,x_label,y_label)
        self.wait(5)