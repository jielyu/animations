# encoding: utf-8

from manim import *
from sympy import substitution


class E00IntroOpening(Scene):
    def construct(self):
        # 大标题
        title = Text("Flutter小技巧").scale(2)
        # 小标题
        subtitle = Text("简介").next_to(title, DOWN)
        # 图标
        icon = (
            ImageMobject("assets/icon/flutter.png").scale(0.2).shift(UP * 5 + RIGHT * 5)
        )
        # 大标题
        self.play(Write(title), run_time=1)
        # 变颜色
        self.play(title.animate.set_color(BLUE), Create(subtitle), run_time=1)
        # 大小标题转换
        title_pos = title.get_center()
        self.play(
            title.animate.scale(0.5).move_to(UP * 3 + LEFT * 3).set_opacity(0.5),
            subtitle.animate.set_color(PINK).scale(1.5).move_to(title_pos),
            run_time=1,
        )
        self.wait()
        # 图片出现
        self.play(icon.animate.scale(1.5).move_to(subtitle.get_center() + DOWN * 2))
        self.wait()
        # 图片消失
        self.play(icon.animate.scale(0.5).move_to(title.get_center() + DOWN))
        self.wait()
        # 图片到右下角
        self.play(icon.animate.move_to(LEFT * 6 + DOWN * 3))
        self.play(icon.animate.rotate(TAU / 2))
        self.play(icon.animate.rotate(TAU / 2))
        self.wait(1)


class FlutterIconAnimation(Scene):
    def construct(self):
        # 图标
        icon = (
            ImageMobject("assets/icon/flutter.png").scale(0.2).shift(UP * 5 + RIGHT * 5)
        ).move_to(LEFT * 6 + DOWN * 3)
        for i in range(10):
            self.play(icon.animate.rotate(TAU / 2), run_time=3)
            self.play(icon.animate.rotate(TAU / 2), run_time=3)


class FlutterTipsEnding(Scene):
    def construct(self):
        youtube = ImageMobject("assets/image/youtube.png").scale(0.5)
        bili = ImageMobject("assets/image/bilibili.png").scale(1.0)
        wechat = ImageMobject("assets/image/wechat_public.png").scale(0.5)

        youtube.move_to(UP * 1.5)
        bili.move_to(UP * 1.5 + RIGHT * 3)
        wechat.move_to(DOWN * 1.5 + RIGHT * 1.4)
        video = Text("视频").scale(1.5).move_to(UP * 1.5 + LEFT * 4)
        article = Text("图文").scale(1.5).move_to(DOWN * 1.5 + LEFT * 4)
        vid_arrow = Arrow(video.get_right(), youtube.get_left(), buff=0.5)
        art_arrow = Arrow(article.get_right(), wechat.get_left())
        # self.add(video, article)
        # self.add(vid_arrow, art_arrow)
        # self.add(youtube, bili, wechat)

        self.play(Write(video))
        self.play(video.animate.set_color(RED), Create(vid_arrow))
        youtube.move_to(UP * 6)

        bili.move_to(UP * 6 + RIGHT * 3)
        self.play(
            youtube.animate.move_to(UP * 1.5),
            bili.animate.move_to(UP * 1.5 + RIGHT * 3),
        )
        self.play(Write(article))
        self.play(article.animate.set_color(GREEN), Create(art_arrow))
        wechat.move_to(DOWN * 1.5 + RIGHT * 8)
        self.play(wechat.animate.move_to(DOWN * 1.5 + RIGHT * 1.4))
        self.wait(3)
