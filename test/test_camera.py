"""测试相机组件的使用"""

from manim import *


class CameraExample(ThreeDScene):
    """三维相机操作例程"""

    def construct(self):

        # move_camera
        axes = ThreeDAxes()
        circle = Circle()
        self.set_camera_orientation(phi=80 * DEGREES)
        self.play(Create(circle), Create(axes))
        # Start move camera
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
        # Stop move camera
        self.stop_ambient_camera_rotation()
        # Return the position of the camera
        self.move_camera(phi=80 * DEGREES, theta=-PI / 2)
        self.wait()
        self.remove(axes, circle)

        # add_fixed_in_frame_mobjects
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        text3d = Text("This is a 3D text")

        self.add_fixed_in_frame_mobjects(text3d)  # <----- Add this
        text3d.to_corner(UL)

        self.add(axes)
        self.begin_ambient_camera_rotation()
        self.play(Write(text3d))

        sphere = Surface(
            lambda u, v: np.array(
                [
                    1.5 * np.cos(u) * np.cos(v),
                    1.5 * np.cos(u) * np.sin(v),
                    1.5 * np.sin(u),
                ]
            ),
            v_range=[0, TAU],
            u_range=[-PI / 2, PI / 2],
            checkerboard_colors=[RED_D, RED_E],
            resolution=(15, 32),
        ).scale(2)

        self.play(Create(sphere))
        self.wait(2)
