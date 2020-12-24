"""测试一般对象的操作和使用"""

from manimlib.imports import *

class TextExample(Scene):
    """文本对象测试实例"""

    def construct(self):
        title1 = TextMobject("Hello, world")
        title2 = TextMobject("你好，中国")
        title1.move_to(UL)
        title2.move_to(DR)
        self.play(Write(title1))
        self.wait()
        self.play(Write(title2))
        self.wait()
        self.remove(title1)
        self.wait()

class PositionExample(Scene):
    """对象位置操作实例"""

    def construct(self):
        # to_edge
        t1 = TextMobject("to\_edge(UP)")
        t1.to_edge(UP)
        self.play(Write(t1))
        t2 = TextMobject("to\_edge(DOWN)")
        t2.to_edge(DOWN)
        self.play(Write(t2))
        t3 = TextMobject("to\_edge(LEFT)")
        t3.to_edge(LEFT)
        self.play(Write(t3))
        t4 = TextMobject("to\_edge(RIGHT)")
        t4.to_edge(RIGHT)
        self.play(Write(t4))
        self.remove(t1, t2, t3, t4)
        self.wait()
        # to_corner
        t1 = TextMobject("to\_corner(UL)")
        t1.to_corner(UL)
        self.play(Write(t1))
        t2 = TextMobject("to\_corner(UR)")
        t2.to_corner(UR)
        self.play(Write(t2))
        t3 = TextMobject("to\_corner(DR)")
        t3.to_corner(DR)
        self.play(Write(t3))
        t4 = TextMobject("to\_corner(DL)")
        t4.to_corner(DL)
        self.play(Write(t4))
        self.remove(t1, t2, t3, t4)
        self.wait()
        # move_to
        t1 = TextMobject("move\_to()")
        t1.move_to(UL)
        self.play(Write(t1))
        t1.move_to(UR)
        self.play(Write(t1))
        t1.move_to(DR)
        self.play(Write(t1))
        t1.move_to(DL)
        self.play(Write(t1))
        t1.move_to(UL)
        self.play(Write(t1))
        self.wait()
        self.remove(t1)
        self.wait()
        # next_to
        t1 = TextMobject("Text")
        t2 = TexMobject("next\_to(Text)")
        t2.next_to(3*RIGHT)
        self.play(Write(t1))
        self.play(Write(t2))
        self.wait()
        self.remove(t1, t2)
        self.wait()
        # shift
        t1 = TextMobject("shift()")
        t1.shift(3*LEFT)
        self.play(Write(t1))
        t1.shift(3*RIGHT)
        self.play(Write(t1))
        self.wait()
        self.remove(t1)
        self.wait()
        # rotate
        t1 = TextMobject('rotate()')
        for i in range(8):
            t1.rotate(PI/4)
            self.play(Write(t1))
            self.wait()
        self.wait()
        self.remove(t1)
        self.wait()
        # flip
        t1 = TextMobject('flip')
        t1.flip(UP)
        self.play(Write(t1))
        t1.flip(LEFT)
        self.play(Write(t1))
        t1.flip(RIGHT)
        self.play(Write(t1))
        t1.flip(DOWN)
        self.play(Write(t1))
        self.wait()
        self.remove(t1)
        self.wait()

class SizeTextExample(Scene):
    """改变文本大小测试实例"""

    def construct(self):
        textHuge = TextMobject("{\\Huge Huge Text 012.\\#!?} Text")
        texthuge = TextMobject("{\\huge huge Text 012.\\#!?} Text")
        textLARGE = TextMobject("{\\LARGE LARGE Text 012.\\#!?} Text")
        textLarge = TextMobject("{\\Large Large Text 012.\\#!?} Text")
        textlarge = TextMobject("{\\large large Text 012.\\#!?} Text")
        textNormal = TextMobject("{\\normalsize normal Text 012.\\#!?} Text")
        textsmall = TextMobject("{\\small small Text 012.\\#!?} Texto normal")
        textfootnotesize = TextMobject("{\\footnotesize footnotesize Text 012.\\#!?} Text")
        textscriptsize = TextMobject("{\\scriptsize scriptsize Text 012.\\#!?} Text")
        texttiny = TextMobject("{\\tiny tiny Texto 012.\\#!?} Text normal")
        textHuge.to_edge(UP)
        texthuge.next_to(textHuge,DOWN,buff=0.1)
        textLARGE.next_to(texthuge,DOWN,buff=0.1)
        textLarge.next_to(textLARGE,DOWN,buff=0.1)
        textlarge.next_to(textLarge,DOWN,buff=0.1)
        textNormal.next_to(textlarge,DOWN,buff=0.1)
        textsmall.next_to(textNormal,DOWN,buff=0.1)
        textfootnotesize.next_to(textsmall,DOWN,buff=0.1)
        textscriptsize.next_to(textfootnotesize,DOWN,buff=0.1)
        texttiny.next_to(textscriptsize,DOWN,buff=0.1)
        self.add(textHuge, texthuge, textLARGE, textLarge, textlarge,
            textNormal, textsmall, textfootnotesize, textscriptsize, texttiny)
        self.wait(3)

class TextArrayExample(Scene):
    """文本数组测试实例"""

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

class VGroupExample(Scene):
    """向量组测试实例"""

    def construct(self):
        text1 = TextMobject("text1")
        text2 = TextMobject("text2 text2")
        text3 = TextMobject("text3 text3 text3")
        textgroup = VGroup(text1,text2,text3)
        textgroup.arrange(
            UP,
            aligned_edge = LEFT,
            buff=0.4
        )
        self.add(textgroup)
        self.wait()

class ShapeExample(Scene):
    """常用几何形状实例"""

    def construct(self):
       
        # Dot
        dot = Dot(radius=1, color=YELLOW)
        dot.move_to(LEFT*3)
        self.play(Write(dot))
        self.wait()
        self.remove(dot)

        # Circle
        c = Circle(color=BLUE)
        c.move_to(RIGHT*3)
        self.play(Write(c))
        self.wait()
        self.remove(c)

        # Annulus
        a = Annulus()
        a.move_to(UP*3)
        self.play(Write(a))
        self.wait()
        self.remove(a)
        
        # Rectangle
        rect = Rectangle()
        rect.move_to(DOWN*3)
        self.play(Write(rect))
        self.wait()
        self.remove(rect)

        # Square
        rect = Square()
        rect.move_to(UL*3)
        self.play(Write(rect))
        self.wait()
        self.remove(rect)
        
        # Ellipse
        e = Ellipse()
        e.move_to(UR*3)
        self.play(Write(e))
        self.wait()
        self.remove(e)

        # Arc
        arc = Arc()
        arc.move_to(DR*3)
        self.play(Write(arc))
        self.wait()
        self.remove(arc)

        # Line
        l = Line()
        self.play(Write(l))
        self.wait()
        self.remove(l)

class Shape3DExample(ThreeDScene):
    """三维对象例程"""

    def construct(self):
        # Sphere
        s = Sphere()
        s.move_to(LEFT*3)
        self.play(Write(s))
        self.wait()
        self.remove(s)

        # Cube
        c = Cube()
        c.move_to(RIGHT*3)
        self.play(Write(c))
        self.wait()
        self.remove(c)

        # Prism
        p = Prism()
        p.move_to(UP)
        self.play(Write(p))
        self.wait()
        self.remove(p)

        # ParametricSurface
        axes = ThreeDAxes()
        cylinder = ParametricSurface(
            lambda u, v: np.array([
                np.cos(TAU * v),
                np.sin(TAU * v),
                2 * (1 - u)
            ]),
            resolution=(6, 32)).fade(0.5) #Resolution of the surfaces

        paraboloid = ParametricSurface(
            lambda u, v: np.array([
                np.cos(v)*u,
                np.sin(v)*u,
                u**2
            ]),v_max=TAU,
            checkerboard_colors=[PURPLE_D, PURPLE_E],
            resolution=(10, 32)).scale(2)

        para_hyp = ParametricSurface(
            lambda u, v: np.array([
                u,
                v,
                u**2-v**2
            ]),v_min=-2,v_max=2,u_min=-2,u_max=2,checkerboard_colors=[BLUE_D, BLUE_E],
            resolution=(15, 32)).scale(1)

        cone = ParametricSurface(
            lambda u, v: np.array([
                u*np.cos(v),
                u*np.sin(v),
                u
            ]),v_min=0,v_max=TAU,u_min=-2,u_max=2,checkerboard_colors=[GREEN_D, GREEN_E],
            resolution=(15, 32)).scale(1)

        hip_one_side = ParametricSurface(
            lambda u, v: np.array([
                np.cosh(u)*np.cos(v),
                np.cosh(u)*np.sin(v),
                np.sinh(u)
            ]),v_min=0,v_max=TAU,u_min=-2,u_max=2,checkerboard_colors=[YELLOW_D, YELLOW_E],
            resolution=(15, 32))

        ellipsoid=ParametricSurface(
            lambda u, v: np.array([
                1*np.cos(u)*np.cos(v),
                2*np.cos(u)*np.sin(v),
                0.5*np.sin(u)
            ]),v_min=0,v_max=TAU,u_min=-PI/2,u_max=PI/2,checkerboard_colors=[TEAL_D, TEAL_E],
            resolution=(15, 32)).scale(2)

        sphere = ParametricSurface(
            lambda u, v: np.array([
                1.5*np.cos(u)*np.cos(v),
                1.5*np.cos(u)*np.sin(v),
                1.5*np.sin(u)
            ]),v_min=0,v_max=TAU,u_min=-PI/2,u_max=PI/2,checkerboard_colors=[RED_D, RED_E],
            resolution=(15, 32)).scale(2)


        self.set_camera_orientation(phi=75 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2)


        self.add(axes)
        self.play(Write(sphere))
        self.wait()
        self.play(ReplacementTransform(sphere,ellipsoid))
        self.wait()
        self.play(ReplacementTransform(ellipsoid,cone))
        self.wait()
        self.play(ReplacementTransform(cone,hip_one_side))
        self.wait()
        self.play(ReplacementTransform(hip_one_side,para_hyp))
        self.wait()
        self.play(ReplacementTransform(para_hyp,paraboloid))
        self.wait()
        self.play(ReplacementTransform(paraboloid,cylinder))
        self.wait()
        self.play(FadeOut(cylinder))
        self.remove(axes, sphere, ellipsoid, cone, hip_one_side, 
            para_hyp, paraboloid, cylinder)

        # ParametricFunction
        curve1=ParametricFunction(
                lambda u : np.array([
                1.2*np.cos(u),
                1.2*np.sin(u),
                u/2
            ]),color=RED,t_min=-TAU,t_max=TAU,
            )
        curve2=ParametricFunction(
                lambda u : np.array([
                1.2*np.cos(u),
                1.2*np.sin(u),
                u
            ]),color=RED,t_min=-TAU,t_max=TAU,
            )

        curve1.set_shade_in_3d(True)
        curve2.set_shade_in_3d(True)

        axes = ThreeDAxes()
        self.add(axes)
        self.set_camera_orientation(phi=80 * DEGREES,theta=-60*DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1) 
        self.play(ShowCreation(curve1))
        self.wait()
        self.play(Transform(curve1,curve2),
                     rate_func=there_and_back,run_time=3)
        self.wait()
