# encoding: utf-8

from manim import *


class TexExample(Scene):
    def construct(self):
        tex = Tex(
            r"The horse does not eat cucumber salad.\\ $E=mc^2$. 测试中文的支持情况",
            tex_template=TexTemplateLibrary.ctex,
        )
        self.add(tex)
