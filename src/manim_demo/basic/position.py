from manimlib.imports import *

class PositionDemo(Scene):
    """对象位置操作实例"""

    def construct(self):
        title = TextMobject('绝对运动')
        title.shift(UP*2.5)
        self.play(Write(title), title.set_color, BLUE)
        # to_edge
        t1 = TextMobject("to\_edge(UP)")
        self.play(t1.to_edge, UP)
        t2 = TextMobject("to\_edge(DOWN)")
        self.play(t2.to_edge, DOWN)
        t3 = TextMobject("to\_edge(LEFT)")
        self.play(t3.to_edge, LEFT)
        t4 = TextMobject("to\_edge(RIGHT)")
        self.play(t4.to_edge, RIGHT)
        self.remove(t1, t2, t3, t4)
        self.wait()
        # to_corner
        t1 = TextMobject("to\_corner(UL)")
        self.play(t1.to_corner, UL)
        t2 = TextMobject("to\_corner(UR)")
        self.play(t2.to_corner, UR)
        t3 = TextMobject("to\_corner(DR)")
        self.play(t3.to_corner, DR)
        t4 = TextMobject("to\_corner(DL)")
        self.play(t4.to_corner, DL)
        self.remove(t1, t2, t3, t4)
        self.wait()
        # move_to
        t1 = TextMobject("move\_to()")
        self.play(t1.move_to, UL)
        self.play(t1.move_to, UR)
        self.play(t1.move_to, DR)
        self.play(t1.move_to, DL)
        self.play(t1.move_to, UL)
        self.wait()
        self.remove(t1, title)
        self.wait()

        title = TextMobject('相对运动')
        title.shift(UP*2.5)
        self.play(Write(title), title.set_color, BLUE)
        # next_to
        t1 = TextMobject("Text")
        t2 = TexMobject("next\_to(Text)")
        self.play(Write(t1))
        self.play(t2.next_to, t1)
        self.wait()
        self.remove(t1, t2)
        self.wait()
        # shift
        t1 = TextMobject("shift()")
        (3*LEFT)
        self.play(t1.shift, 3*LEFT)
        self.play(t1.shift, -3*LEFT)
        self.wait()
        self.remove(t1)
        self.wait()
        # rotate
        t1 = TextMobject('rotate()')
        for i in range(8):
            self.play(t1.rotate, PI/4)
            self.wait(0.3)
        self.wait()
        self.remove(t1)
        self.wait()
        # flip
        t1 = TextMobject('flip')
        self.play(t1.flip, UP)
        self.play(t1.flip, LEFT)
        self.play(t1.flip, RIGHT)
        self.play(t1.flip, DOWN)
        self.wait()
        self.remove(t1, title)
        self.wait()