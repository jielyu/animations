# encoding: utf-8

from manim import *


class Scene01(Scene):
    def construct(self):
        plugin = Text("Plugin").move_to(LEFT * 6 + UP).scale(2)
        package = Text("Package").move_to(RIGHT * 6 + DOWN).scale(2)
        vs = Text("vs").scale(0.8)
        self.play(
            plugin.animate.move_to(LEFT + UP), package.animate.move_to(RIGHT + DOWN)
        )
        self.wait()
        self.play(Write(vs))
        self.wait()
        self.play(
            plugin.animate.set_color(BLUE),
            package.animate.set_color(GREEN),
            vs.animate.set_color(RED),
        )
        self.wait(2)
        self.play(
            FadeOut(plugin, shift=LEFT * 2),
            FadeOut(package, shift=RIGHT * 2),
            FadeOut(vs),
        )


class Scene02(Scene):
    def construct(self):
        plugin = (
            Text(
                "flutter create --template=plugin --platform=macos plg_test",
                t2c={"plugin": BLUE, "macos": GREEN, "flutter": RED},
            )
            .scale(0.8)
            .move_to(UP)
        )
        package = (
            Text(
                "flutter create --template=package pkg_test",
                t2c={"package": BLUE, "flutter": RED},
            )
            .scale(0.8)
            .move_to(DOWN)
        )
        self.play(Write(plugin))
        self.play(Write(package))
        plugin_anno = Text("创建plugin").scale(0.8).move_to(UP * 2)
        plugin_arrow = Arrow(plugin_anno.get_center(), plugin.get_center())
        self.play(Create(plugin_anno))
        self.play(plugin_anno.animate.set_color(YELLOW))
        self.play(GrowFromPoint(plugin_arrow, plugin_anno.get_center()))

        package_anno = Text("创建package").scale(0.8).move_to(DOWN * 2)
        package_arrow = Arrow(package_anno.get_center(), package.get_center())
        self.play(Create(package_anno))
        self.play(package_anno.animate.set_color(YELLOW))
        self.play(GrowFromPoint(package_arrow, package_anno.get_center()))
        self.wait(2)
        self.play(
            FadeOut(plugin_anno),
            FadeOut(plugin_arrow),
            FadeOut(package_anno),
            FadeOut(package_arrow),
        )
        self.play(FadeOut(plugin, shift=LEFT), FadeOut(package, shift=RIGHT))


class Scene03(Scene):
    def construct(self):
        plg_box = Square(side_length=3).move_to(UP * 2 + LEFT * 3)
        pkg_box = Square(side_length=3).move_to(UP * 2 + RIGHT * 3)
        plg_text = Text("Plugin").move_to(UP * 2.5 + LEFT * 3)
        pkg_text = Text("Package").move_to(UP * 2.5 + RIGHT * 3)
        self.play(Create(plg_box), Create(pkg_box))
        self.play(FadeIn(plg_text), FadeIn(pkg_text))
        self.play(plg_box.animate.set_color(BLUE), pkg_box.animate.set_color(GREEN))
        self.wait()

        plg_ch_text = Text("插件").next_to(plg_text, direction=DOWN).scale(0.5)
        pkg_ch_text = Text("包").next_to(pkg_text, direction=DOWN).scale(0.5)
        self.play(FadeIn(plg_ch_text, shift=DOWN), FadeIn(pkg_ch_text, shift=DOWN))
        self.wait()

        plg_anno1 = Text("平台相关的操作").move_to(LEFT * 3 + DOWN).scale(0.7)
        plg_anno2 = Text("调用其他语言程序").move_to(LEFT * 3 + DOWN * 2).scale(0.7)
        plg_arrow1 = Arrow(plg_anno1.get_left() + LEFT, plg_anno1.get_left())
        plg_arrow2 = Arrow(plg_anno2.get_left() + LEFT, plg_anno2.get_left())
        self.play(Create(plg_arrow1))
        self.play(Write(plg_anno1))
        self.play(Create(plg_arrow2))
        self.play(Write(plg_anno2))
        plg_temp = [plg_anno1, plg_anno2, plg_arrow1, plg_arrow2]
        self.play(*[obj.animate.set_color(BLUE) for obj in plg_temp])
        self.wait()

        pkg_anno = Text("完全使用dart编写").move_to(RIGHT * 3 + DOWN * 1.5).scale(0.7)
        pkg_arrow = Arrow(pkg_anno.get_left() + LEFT, pkg_anno.get_left())
        self.play(Create(pkg_arrow))
        self.play(Write(pkg_anno))
        pkg_temp = [pkg_anno, pkg_arrow]
        self.play(*[obj.animate.set_color(GREEN) for obj in pkg_temp])
        self.wait()

        self.play(*[FadeOut(obj) for obj in plg_temp])
        plg_anno = Text("无法完全使用dart编写").move_to(LEFT * 3 + DOWN * 1.5).scale(0.7)
        plg_arrow = Arrow(plg_anno.get_left() + LEFT, plg_anno.get_left())
        self.play(Create(plg_arrow))
        self.play(Write(plg_anno))
        plg_temp = [plg_anno, plg_arrow]
        self.play(*[obj.animate.set_color(BLUE) for obj in plg_temp])
        self.wait()
