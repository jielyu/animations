# encoding: utf-8

import random
import math
import numpy
from manim import *


class BernoulliDistribution(Scene):
    def construct(self):
        title = Text("伯努利分布")
        subtitle = Text("Bernoulli Distribution").next_to(title, direction=DOWN)
        self.play(Write(title), Create(subtitle))
        self.wait()
        self.play(
            title.animate.set_color(BLUE).shift(UP * 3),
            subtitle.animate.set_color(RED).shift(UP * 3).scale(0.5),
        )
        self.wait()

        # 定义
        p0 = MathTex("P(x=0)=\phi")
        p1 = MathTex("P(x=1)=1-\phi").next_to(p0, direction=DOWN)
        self.play(Write(p0), Write(p1))
        self.wait()
        self.play(FadeOut(p0), FadeOut(p1))

        # 创建公式
        formula = MathTex("P(x=x) = \phi^x(1-\phi)^{1-x}")
        self.play(FadeIn(formula, shift=UP))
        self.wait()

        # 参数变量
        int_var = 0.5
        theta = Variable(int_var, MathTex("\phi"), num_decimal_places=2).next_to(
            formula, DOWN
        )
        self.play(FadeIn(theta, shift=UP), theta.value.animate.set_color(RED))

        # 位置移动
        text_objs = [title, subtitle, formula, theta]
        self.play(*[obj.animate.shift(LEFT * 4) for obj in text_objs])

        axes = Axes(
            x_range=[0, 1, 0.1],
            y_range=[0, 1, 0.1],
            x_length=6,
            y_length=6,
            axis_config={"color": GREEN},
            x_axis_config={
                "numbers_to_include": np.arange(0, 1.1, 0.2),
                "numbers_with_elongated_ticks": np.arange(0, 1.1, 0.2),
            },
            y_axis_config={
                "numbers_to_include": np.arange(0, 1.1, 0.2),
                "numbers_with_elongated_ticks": np.arange(0, 1.1, 0.2),
            },
            tips=False,
        ).shift(RIGHT * 3)

        def bernoulli_func(p):
            return lambda x: (p**x) * ((1 - p) ** (1 - x))

        theta_tracker = theta.tracker
        axes_labels = axes.get_axis_labels()
        dist_graph = axes.plot(bernoulli_func(theta_tracker.get_value()), color=BLUE)
        dist_graph.add_updater(
            lambda x: x.become(
                axes.plot(bernoulli_func(theta_tracker.get_value()), color=BLUE)
            )
        )
        self.add(axes_labels, axes, dist_graph)

        def calc_prob(x):
            return axes.c2p(x, bernoulli_func(theta_tracker.get_value())(x))

        d1, d2 = Dot(color=BLUE).move_to(calc_prob(0)), Dot(color=GREEN).move_to(
            calc_prob(1)
        )
        dg = VGroup(d1, d2).arrange(RIGHT, buff=1)
        d1.add_updater(lambda z: z.move_to(calc_prob(0)))
        d2.add_updater(lambda z: z.move_to(calc_prob(1)))
        self.add(dg)
        value_list = [0.1, 0.3, 0.5, 0.7, 0.9, 0.99]
        for v in value_list:
            self.play(theta_tracker.animate.set_value(v))
            self.wait()
        self.wait()
        # 概率取值点
        self.play(d1.animate.scale(2), d2.animate.scale(2))
        self.play(FadeOut(dist_graph, shift=DOWN))
        value_list.reverse()
        for v in value_list:
            self.play(theta_tracker.animate.set_value(v))
            self.wait()
        self.wait()


class BinaryDistribution(Scene):
    def construct(self):
        num_coin_row = 4
        num_coin_col = 5
        coins, marks = [], []
        for i in range(num_coin_row):
            coins.append([])
            marks.append([])
            for j in range(num_coin_col):
                is_pos = random.random() > 0.5
                coin = Circle(
                    radius=0.4,
                    color=GREEN if is_pos else RED,
                    fill_opacity=1,
                ).shift(
                    UP * (i - num_coin_row / 2 + 0.5) + LEFT * (j - num_coin_col / 2)
                )

                coins[i].append(coin)
                marks[i].append(is_pos)
        self.play(*[Write(coin) for coin_row in coins for coin in coin_row])
        self.wait()

        names = []
        for i in range(num_coin_row):
            names.append([])
            for j in range(num_coin_col):
                name = Text(
                    "{}".format(int(marks[i][j])),
                    color=WHITE,
                ).move_to(coins[i][j].get_center())
                names[i].append(name)
        self.play(*[FadeIn(name) for name_row in names for name in name_row])
        self.wait()

        self.play(
            *[coin.animate.shift(LEFT * 4) for coin_row in coins for coin in coin_row],
            *[name.animate.shift(LEFT * 4) for name_row in names for name in name_row]
        )
        self.wait()

        binary_dist = MathTex("F(k, n, \phi)=C_n^k \phi^k (1-\phi)^{n-k}").shift(
            RIGHT * 3
        )
        self.play(FadeIn(binary_dist, shift=DOWN))
        self.play(binary_dist.animate.set_color(YELLOW))
        self.wait()

        title = Text("二项分布").scale(2).move_to(UP * 3)
        self.play(FadeIn(title, shift=DOWN))
        self.play(
            title.animate.move_to(binary_dist.get_top() + UP).scale(0.5).set_color(BLUE)
        )
        self.wait()

        self.play(FadeOut(binary_dist, shift=DOWN), title.animate.move_to(UP * 3))

        # 画图
        axes = Axes(
            x_range=[0, 40, 1],
            y_range=[0, 0.25, 0.05],
            x_length=6,
            y_length=4,
            axis_config={"color": GREEN},
            x_axis_config={
                "numbers_to_include": np.arange(0, 40, 4),
                "numbers_with_elongated_ticks": np.arange(0, 40, 4),
            },
            y_axis_config={
                "numbers_to_include": np.arange(0, 0.26, 0.05),
                "numbers_with_elongated_ticks": np.arange(0, 0.26, 0.05),
            },
            tips=False,
        ).shift(RIGHT * 3)
        self.play(FadeIn(axes, shift=RIGHT))

        def binary_func(n, p):
            return lambda k: math.comb(n, k) * (p**k) * ((1 - p) ** (n - k))

        params = [[20, 0.5], [20, 0.7], [40, 0.7]]
        colors = [BLUE, YELLOW, RED]
        all_points = []
        all_dots = []
        for idx, param in enumerate(params):
            n, p = param
            f = binary_func(n, p)
            dots1 = []
            probs = []
            for i in range(n):
                probs.append(f(i))
                dots1.append(Dot(color=colors[idx]).move_to(axes.c2p(i, probs[i])))
            self.play(*[FadeIn(dot) for dot in dots1])
            self.wait()
            all_points.append(probs)
            all_dots.append(dots1)

        # 进行标注
        argmax_n0 = np.array(all_points[0]).argmax()
        text = (
            MathTex("n=20, \phi=0.5")
            .move_to(UP + axes.c2p(argmax_n0, all_points[0][argmax_n0]))
            .scale(0.6)
        )
        arrow = Arrow(all_dots[0][argmax_n0].get_center(), text.get_center())
        self.play(Write(text), Create(arrow))
        self.play(text.animate.set_color(colors[0]))
        self.wait()

        argmax_n1 = np.array(all_points[1]).argmax()
        text = (
            MathTex("n=20, \phi=0.7")
            .move_to(UP + RIGHT * 2 + axes.c2p(argmax_n1, all_points[1][argmax_n1]))
            .scale(0.6)
        )
        arrow = Arrow(all_dots[1][argmax_n1].get_center(), text.get_center(), buff=0.7)
        self.play(Write(text), Create(arrow))
        self.play(text.animate.set_color(colors[1]))
        self.wait()

        argmax_n2 = np.array(all_points[2]).argmax()
        text = (
            MathTex("n=40, \phi=0.7")
            .move_to(UP + RIGHT + axes.c2p(argmax_n2, all_points[2][argmax_n2]))
            .scale(0.6)
        )
        arrow = Arrow(all_dots[2][argmax_n2].get_center(), text.get_center())
        self.play(Write(text), Create(arrow))
        self.play(text.animate.set_color(colors[2]))
        self.wait()


class NormalDistribution(ThreeDScene):
    def gaussian_1d(self, x, mu, sigma):
        prob = (
            1
            / (sigma * np.sqrt(2 * np.pi))
            * np.exp(-((x - mu) ** 2) / (2 * sigma**2))
        )
        return x, prob

    def construct(self):
        axes = Axes(
            x_range=[-2, 2, 0.2],
            y_range=[0, 1, 0.1],
            x_length=8,
            y_length=4,
            axis_config={"color": GREEN},
            x_axis_config={
                "numbers_to_include": np.arange(-2, 2.1, 1),
                "numbers_with_elongated_ticks": np.arange(-2, 2.1, 1),
            },
            y_axis_config={
                "numbers_to_include": np.arange(0, 1.1, 0.2),
                "numbers_with_elongated_ticks": np.arange(0, 1.1, 0.2),
            },
            tips=False,
        )

        self.play(FadeIn(axes, shift=RIGHT))

        axes_labels = axes.get_axis_labels()
        dist_graph = axes.plot(lambda x: self.gaussian_1d(x, 0, 1)[1], color=BLUE)
        self.play(Create(axes_labels), Create(dist_graph))
        self.wait()

        text = MathTex(
            r"N(x;\mu,\sigma^2) = \sqrt{\frac{1}{2\pi\sigma^2}}exp\left ( -\frac{1}{2\sigma^2}(x-\mu)^2 \right )"
        ).shift(RIGHT * 2 + UP * 3)
        text_arrow = Arrow(axes.c2p(0, 0.4), text.get_center(), buff=1)
        self.play(Write(text_arrow))
        self.play(Create(text))
        self.play(text.animate.set_color(YELLOW))
        self.play(FadeOut(text), FadeOut(text_arrow))

        std_tracker = ValueTracker(1)
        mean_tracker = ValueTracker(0)
        dist_graph.add_updater(
            lambda z: z.become(
                axes.plot(
                    lambda x: self.gaussian_1d(
                        x, mean_tracker.get_value(), std_tracker.get_value()
                    )[1],
                    color=BLUE,
                )
            )
        )
        self.play(std_tracker.animate.set_value(2))
        self.wait()
        self.play(std_tracker.animate.set_value(0.5))
        self.wait()
        self.play(std_tracker.animate.set_value(1))
        self.wait()
        self.play(mean_tracker.animate.set_value(0.5))
        self.wait()
        self.play(mean_tracker.animate.set_value(-0.5))
        self.wait()
        self.play(mean_tracker.animate.set_value(0))
        self.wait()


class NormalDistTitle(Scene):
    def construct(self):
        title = Text("正态分布")
        subtitle = Text("Gaussian Distribution").next_to(title, direction=DOWN)
        self.play(Write(title), Create(subtitle))
        self.wait()
        self.play(
            title.animate.set_color(BLUE).shift(UP * 3),
            subtitle.animate.set_color(RED).shift(UP * 3).scale(0.5),
        )
        self.wait()
        self.play(FadeOut(title), FadeOut(subtitle))


class Normal2dDistribution(ThreeDScene):
    def gaussian_2d(self, x, y, mu, sigma):
        prob = (
            1
            / (sigma * np.sqrt(2 * np.pi))
            * np.exp(-((x - mu[0]) ** 2 + (y - mu[1]) ** 2) / (2 * sigma**2))
        )
        return x, y, prob

    def construct(self):
        resolution_fa = 24
        self.set_camera_orientation(phi=75 * DEGREES, theta=-30 * DEGREES)
        gauss_plane = (
            Surface(
                lambda x, y: self.gaussian_2d(x, y, [0, 0], 1),
                resolution=(resolution_fa, resolution_fa),
                v_range=[-2, +2],
                u_range=[-2, +2],
            )
            .scale(2, about_point=ORIGIN)
            .set_style(fill_opacity=1, stroke_color=GREEN)
            .set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)
        )
        self.play(Write(gauss_plane))
        tracker = ValueTracker(1)
        gauss_plane.add_updater(
            lambda z: z.become(
                Surface(
                    lambda x, y: self.gaussian_2d(x, y, [0, 0], tracker.get_value()),
                    resolution=(resolution_fa, resolution_fa),
                    v_range=[-2, +2],
                    u_range=[-2, +2],
                )
                .scale(2, about_point=ORIGIN)
                .set_style(fill_opacity=1, stroke_color=GREEN)
                .set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)
            )
        )
        self.play(tracker.animate.set_value(0.3))
        self.wait()
        self.play(tracker.animate.set_value(3))
        self.wait()
        self.play(tracker.animate.set_value(1))
        self.wait()


class ExponentDistribution(Scene):
    def exponential_1d(self, x, mu):
        prob = mu * np.exp(-x * mu)
        return x, prob

    def construct(self):
        axes = Axes(
            x_range=[0, 4, 0.2],
            y_range=[0, 1, 0.1],
            x_length=8,
            y_length=4,
            axis_config={"color": GREEN},
            x_axis_config={
                "numbers_to_include": np.arange(0, 4.1, 1),
                "numbers_with_elongated_ticks": np.arange(0, 4.1, 1),
            },
            y_axis_config={
                "numbers_to_include": np.arange(0, 1.1, 0.2),
                "numbers_with_elongated_ticks": np.arange(0, 1.1, 0.2),
            },
            tips=False,
        )

        self.play(FadeIn(axes, shift=RIGHT))

        axes_labels = axes.get_axis_labels()
        dist_graph = axes.plot(lambda x: self.exponential_1d(x, 1)[1], color=BLUE)
        self.play(Create(axes_labels), Create(dist_graph))
        self.wait()

        text = MathTex(r"p(x;\lambda)=\lambda exp(-\lambda{x})").shift(
            RIGHT * 2 + UP * 3
        )
        text_arrow = Arrow(axes.c2p(0, 0.4), text.get_center(), buff=1)
        self.play(Write(text_arrow))
        self.play(Create(text))
        self.play(text.animate.set_color(YELLOW))
        self.play(FadeOut(text), FadeOut(text_arrow))

        tracker = ValueTracker(1)
        dist_graph.add_updater(
            lambda z: z.become(
                axes.plot(
                    lambda x: self.exponential_1d(x, tracker.get_value())[1],
                    color=BLUE,
                )
            )
        )
        self.play(tracker.animate.set_value(2))
        self.wait()
        self.play(tracker.animate.set_value(0.5))
        self.wait()
        self.play(tracker.animate.set_value(1))
        self.wait()


class ExponentDistTitle(Scene):
    def construct(self):
        title = Text("指数分布")
        subtitle = Text("Exponent Distribution").next_to(title, direction=DOWN)
        self.play(Write(title), Create(subtitle))
        self.wait()
        self.play(
            title.animate.set_color(BLUE).shift(UP * 3),
            subtitle.animate.set_color(RED).shift(UP * 3).scale(0.5),
        )
        self.wait()
        self.play(FadeOut(title), FadeOut(subtitle))


class LaplaceDistribution(Scene):
    def laplace_1d(self, x, mu, b):
        prob = (1 / (2 * b)) * np.exp(-abs(x - mu) / b)
        return x, prob

    def construct(self):
        axes = Axes(
            x_range=[-2, 2, 0.2],
            y_range=[0, 1, 0.1],
            x_length=8,
            y_length=4,
            axis_config={"color": GREEN},
            x_axis_config={
                "numbers_to_include": np.arange(-2, 2.1, 1),
                "numbers_with_elongated_ticks": np.arange(-2, 2.1, 1),
            },
            y_axis_config={
                "numbers_to_include": np.arange(0, 1.1, 0.2),
                "numbers_with_elongated_ticks": np.arange(0, 1.1, 0.2),
            },
            tips=False,
        )

        self.play(FadeIn(axes, shift=RIGHT))

        axes_labels = axes.get_axis_labels()
        dist_graph = axes.plot(lambda x: self.laplace_1d(x, 0, 1)[1], color=BLUE)
        self.play(Create(axes_labels), Create(dist_graph))
        self.wait()

        text = MathTex(
            r"Laplace(x;\mu;\gamma)=\frac{1}{2\gamma}exp\left(-\frac{|x-\mu|}{\gamma}\right)"
        ).shift(RIGHT * 2 + UP * 3)
        text_arrow = Arrow(axes.c2p(0, 0.4), text.get_center(), buff=1)
        self.play(Write(text_arrow))
        self.play(Create(text))
        self.play(text.animate.set_color(YELLOW))
        self.play(FadeOut(text), FadeOut(text_arrow))

        std_tracker = ValueTracker(1)
        mean_tracker = ValueTracker(0)
        dist_graph.add_updater(
            lambda z: z.become(
                axes.plot(
                    lambda x: self.laplace_1d(
                        x, mean_tracker.get_value(), std_tracker.get_value()
                    )[1],
                    color=BLUE,
                )
            )
        )
        self.play(std_tracker.animate.set_value(2))
        self.wait()
        self.play(std_tracker.animate.set_value(0.5))
        self.wait()
        self.play(std_tracker.animate.set_value(1))
        self.wait()
        self.play(mean_tracker.animate.set_value(0.5))
        self.wait()
        self.play(mean_tracker.animate.set_value(-0.5))
        self.wait()
        self.play(mean_tracker.animate.set_value(0))
        self.wait()


class LaplaceDistTitle(Scene):
    def construct(self):
        title = Text("拉普拉斯分布")
        subtitle = Text("Lapalce Distribution").next_to(title, direction=DOWN)
        self.play(Write(title), Create(subtitle))
        self.wait()
        self.play(
            title.animate.set_color(BLUE).shift(UP * 3),
            subtitle.animate.set_color(RED).shift(UP * 3).scale(0.5),
        )
        self.wait()
        self.play(FadeOut(title), FadeOut(subtitle))


class Cover(Scene):
    def build_bernoulli(self):
        axes = (
            Axes(
                x_range=[0, 1, 0.1],
                y_range=[0, 1, 0.1],
                x_length=6,
                y_length=6,
                axis_config={"color": GREEN},
                x_axis_config={
                    "numbers_to_include": np.arange(0, 1.1, 0.2),
                    "numbers_with_elongated_ticks": np.arange(0, 1.1, 0.2),
                },
                y_axis_config={
                    "numbers_to_include": np.arange(0, 1.1, 0.2),
                    "numbers_with_elongated_ticks": np.arange(0, 1.1, 0.2),
                },
                tips=False,
            )
            .shift(LEFT * 4 + UP * 2)
            .scale(0.6)
        )
        self.play(Create(axes))

        def bernoulli_func(p):
            return lambda x: (p**x) * ((1 - p) ** (1 - x))

        axes_labels = axes.get_axis_labels()
        dist_graph = axes.plot(bernoulli_func(0.8), color=BLUE)
        self.play(Write(axes_labels), Write(dist_graph))

    def build_binary(self):
        axes = (
            Axes(
                x_range=[0, 40, 1],
                y_range=[0, 0.25, 0.05],
                x_length=6,
                y_length=4,
                axis_config={"color": GREEN},
                x_axis_config={
                    "numbers_to_include": np.arange(0, 40, 4),
                    "numbers_with_elongated_ticks": np.arange(0, 40, 4),
                },
                y_axis_config={
                    "numbers_to_include": np.arange(0, 0.26, 0.05),
                    "numbers_with_elongated_ticks": np.arange(0, 0.26, 0.05),
                },
                tips=False,
            )
            .shift(UP * 2)
            .scale(0.5)
        )
        self.play(FadeIn(axes, shift=RIGHT))

        def binary_func(n, p):
            return lambda k: math.comb(n, k) * (p**k) * ((1 - p) ** (n - k))

        params = [[20, 0.5], [20, 0.7], [40, 0.7]]
        colors = [BLUE, YELLOW, RED]
        all_points = []
        all_dots = []
        for idx, param in enumerate(params):
            n, p = param
            f = binary_func(n, p)
            dots1 = []
            probs = []
            for i in range(n):
                probs.append(f(i))
                dots1.append(Dot(color=colors[idx]).move_to(axes.c2p(i, probs[i])))
            self.play(*[FadeIn(dot) for dot in dots1])
            self.wait()
            all_points.append(probs)
            all_dots.append(dots1)

        # 进行标注
        argmax_n0 = np.array(all_points[0]).argmax()
        text = (
            MathTex("n=20, \phi=0.5")
            .move_to(UP + axes.c2p(argmax_n0, all_points[0][argmax_n0]))
            .scale(0.6)
        )
        arrow = Arrow(all_dots[0][argmax_n0].get_center(), text.get_center())
        self.play(Write(text), Create(arrow))
        self.play(text.animate.set_color(colors[0]))
        self.wait()

        argmax_n1 = np.array(all_points[1]).argmax()
        text = (
            MathTex("n=20, \phi=0.7")
            .move_to(UP + RIGHT * 2 + axes.c2p(argmax_n1, all_points[1][argmax_n1]))
            .scale(0.6)
        )
        arrow = Arrow(all_dots[1][argmax_n1].get_center(), text.get_center(), buff=0.7)
        self.play(Write(text), Create(arrow))
        self.play(text.animate.set_color(colors[1]))
        self.wait()

        argmax_n2 = np.array(all_points[2]).argmax()
        text = (
            MathTex("n=40, \phi=0.7")
            .move_to(UP + RIGHT + axes.c2p(argmax_n2, all_points[2][argmax_n2]))
            .scale(0.6)
        )
        arrow = Arrow(all_dots[2][argmax_n2].get_center(), text.get_center())
        self.play(Write(text), Create(arrow))
        self.play(text.animate.set_color(colors[2]))
        self.wait()

    def gaussian_1d(self, x, mu, sigma):
        prob = (
            1
            / (sigma * np.sqrt(2 * np.pi))
            * np.exp(-((x - mu) ** 2) / (2 * sigma**2))
        )
        return x, prob

    def build_normal(self):
        axes = (
            Axes(
                x_range=[-2, 2, 0.2],
                y_range=[0, 1, 0.1],
                x_length=8,
                y_length=4,
                axis_config={"color": GREEN},
                x_axis_config={
                    "numbers_to_include": np.arange(-2, 2.1, 1),
                    "numbers_with_elongated_ticks": np.arange(-2, 2.1, 1),
                },
                y_axis_config={
                    "numbers_to_include": np.arange(0, 1.1, 0.2),
                    "numbers_with_elongated_ticks": np.arange(0, 1.1, 0.2),
                },
                tips=False,
            )
            .shift(RIGHT * 4 + UP * 2)
            .scale(0.6)
        )
        self.play(FadeIn(axes, shift=RIGHT))

        axes_labels = axes.get_axis_labels()
        dist_graph = axes.plot(lambda x: self.gaussian_1d(x, 0, 1)[1], color=BLUE)
        self.play(Create(axes_labels), Create(dist_graph))
        self.wait()

    def exponential_1d(self, x, mu):
        prob = mu * np.exp(-x * mu)
        return x, prob

    def build_exponent(self):
        axes = (
            Axes(
                x_range=[0, 4, 0.2],
                y_range=[0, 1, 0.1],
                x_length=8,
                y_length=4,
                axis_config={"color": GREEN},
                x_axis_config={
                    "numbers_to_include": np.arange(0, 4.1, 1),
                    "numbers_with_elongated_ticks": np.arange(0, 4.1, 1),
                },
                y_axis_config={
                    "numbers_to_include": np.arange(0, 1.1, 0.2),
                    "numbers_with_elongated_ticks": np.arange(0, 1.1, 0.2),
                },
                tips=False,
            )
            .shift(LEFT * 3 + DOWN * 2)
            .scale(0.6)
        )

        self.play(FadeIn(axes, shift=RIGHT))

        axes_labels = axes.get_axis_labels()
        dist_graph = axes.plot(lambda x: self.exponential_1d(x, 1)[1], color=BLUE)
        self.play(Create(axes_labels), Create(dist_graph))
        self.wait()

    def laplace_1d(self, x, mu, b):
        prob = (1 / (2 * b)) * np.exp(-abs(x - mu) / b)
        return x, prob

    def build_laplace(self):
        axes = (
            Axes(
                x_range=[-2, 2, 0.2],
                y_range=[0, 1, 0.1],
                x_length=8,
                y_length=4,
                axis_config={"color": GREEN},
                x_axis_config={
                    "numbers_to_include": np.arange(-2, 2.1, 1),
                    "numbers_with_elongated_ticks": np.arange(-2, 2.1, 1),
                },
                y_axis_config={
                    "numbers_to_include": np.arange(0, 1.1, 0.2),
                    "numbers_with_elongated_ticks": np.arange(0, 1.1, 0.2),
                },
                tips=False,
            )
            .shift(DOWN * 2 + RIGHT * 3)
            .scale(0.6)
        )

        self.play(FadeIn(axes, shift=RIGHT))

        axes_labels = axes.get_axis_labels()
        dist_graph = axes.plot(lambda x: self.laplace_1d(x, 0, 1)[1], color=BLUE)
        self.play(Create(axes_labels), Create(dist_graph))
        self.wait()

    def construct(self):
        self.build_bernoulli()
        self.build_binary()
        self.build_normal()
        self.build_exponent()
        self.build_laplace()
