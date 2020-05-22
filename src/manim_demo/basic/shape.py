from manimlib.imports import *

class ShapeDemo(Scene):
    """常用几何形状实例"""

    def construct(self):
        title = TextMobject('常用形状')
        title.shift(UP*2.5)
        self.play(Write(title), title.set_color, BLUE)
        # Dot
        dot = Dot(radius=1, color=YELLOW)
        self.play(dot.move_to, LEFT*4)

        # Circle
        c = Circle(color=BLUE)
        self.play(c.move_to, RIGHT*4)

        # Annulus
        a = Annulus()
        self.play(a.move_to, DOWN*3)
        
        # Rectangle
        rect = Rectangle()
        self.play(rect.move_to, UP*3)

        # Square
        s = Square()
        self.play(s.move_to, UL*3+LEFT)
        
        # Ellipse
        e = Ellipse()
        self.play(e.move_to, UR*3+RIGHT)

        # Arc
        arc = Arc()
        self.play(arc.move_to, DR*3+RIGHT)

        # Line
        l = Line()
        self.play(Write(l))
        self.wait()
        self.play(*[FadeOut(x) for x in [title, dot, c, a, rect, s, e, arc, l]])
        self.wait()

class Shape3DDemo(ThreeDScene):
    """三维对象例程"""

    def construct(self):
        title = TextMobject('常用3D形状')
        title.shift(UP*2.5)
        self.play(Write(title), title.set_color, BLUE)
        # Sphere
        s = Sphere()
        self.play(s.move_to, LEFT*4)

        # Cube
        c = Cube()
        self.play(c.move_to, RIGHT*4)

        # Prism
        p = Prism()
        self.play(p.move_to, UP)

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
            checkerboard_colors=[BLUE, GREEN],
            resolution=(10, 32)).scale(2)

        para_hyp = ParametricSurface(
            lambda u, v: np.array([
                u,
                v,
                u**2-v**2
            ]),v_min=-2,v_max=2,u_min=-2,u_max=2,checkerboard_colors=[BLUE, RED],
            resolution=(15, 32)).scale(1)

        cone = ParametricSurface(
            lambda u, v: np.array([
                u*np.cos(v),
                u*np.sin(v),
                u
            ]),v_min=0,v_max=TAU,u_min=-2,u_max=2,checkerboard_colors=[BLUE, YELLOW],
            resolution=(15, 32)).scale(1)

        hip_one_side = ParametricSurface(
            lambda u, v: np.array([
                np.cosh(u)*np.cos(v),
                np.cosh(u)*np.sin(v),
                np.sinh(u)
            ]),v_min=0,v_max=TAU,u_min=-2,u_max=2,checkerboard_colors=[RED, GREEN],
            resolution=(15, 32))

        ellipsoid=ParametricSurface(
            lambda u, v: np.array([
                1*np.cos(u)*np.cos(v),
                2*np.cos(u)*np.sin(v),
                0.5*np.sin(u)
            ]),v_min=0,v_max=TAU,u_min=-PI/2,u_max=PI/2,checkerboard_colors=[RED, YELLOW],
            resolution=(15, 32)).scale(2)

        sphere = ParametricSurface(
            lambda u, v: np.array([
                1.5*np.cos(u)*np.cos(v),
                1.5*np.cos(u)*np.sin(v),
                1.5*np.sin(u)
            ]),v_min=0,v_max=TAU,u_min=-PI/2,u_max=PI/2,checkerboard_colors=[YELLOW, GREEN],
            resolution=(15, 32)).scale(2)


        self.set_camera_orientation(phi=75 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.3)

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
        self.set_camera_orientation(phi=60 * DEGREES,theta=-60*DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1) 
        self.play(ShowCreation(curve1))
        self.wait()
        self.play(Transform(curve1,curve2),
                     rate_func=there_and_back,run_time=4)
        self.wait()