from manimlib.imports import *

class LatexDemo(Scene):
    """文本数组测试实例"""

    def construct(self):
        title = TextMobject('矢量对象本身构成的数组')
        title.shift(UP*2.5)
        self.play(Write(title), title.set_color, BLUE)
        # 矢量对象本身构成的Array
        t = TexMobject("A", "{B", "\\over", "C}", "D", "E")
        t.scale(3)
        self.play(t[0].set_color, RED)
        self.play(t[1].set_color, ORANGE)
        self.play(t[2].set_color, YELLOW)
        self.play(t[3].set_color, GREEN)
        self.play(t[4].set_color, BLUE)
        self.play(t[5].set_color, BLUE)
        self.wait()
        self.play(FadeOut(t), FadeOut(title))
        self.wait()

        title = TextMobject('自定义组装的数组')
        title.shift(UP*2.5)
        self.play(Write(title), title.set_color, BLUE)
        # 自定义组装的矢量对象
        text1 = TextMobject("第一行文本")
        text2 = TextMobject("第二行文本 VGroup")
        text3 = TextMobject("第三行文本 向上 左对齐")
        textgroup = VGroup(text1,text2,text3)
        textgroup.arrange(DOWN, aligned_edge = LEFT, buff=0.4)
        self.play(Write(textgroup))
        #self.play(Write(textgroup), textgroup.shift, UP*1.5)
        self.play(text1.set_color, RED)
        self.play(text2.set_color, GREEN)
        self.play(text3.set_color, BLUE)
        self.play(FadeOut(title))
        self.remove(textgroup)
        self.wait()

        title = TextMobject('Latex控制的文本大小')
        title.shift(UP*2.5)
        self.play(Write(title), title.set_color, BLUE)
        # latex控制的文本大小
        textHuge = TextMobject("{\\Huge 超大文本}")
        texthuge = TextMobject("{\\huge 巨大文本}")
        textLARGE = TextMobject("{\\LARGE 大文本}")
        textLarge = TextMobject("{\\Large 稍大文本}")
        textlarge = TextMobject("{\\large 中大的文本}")
        textNormal = TextMobject("{\\normalsize 正常的文本}")
        textsmall = TextMobject("{\\small 小文本}")
        textfootnotesize = TextMobject("{\\footnotesize 注释大小的文本}")
        textscriptsize = TextMobject("{\\scriptsize 脚标大小的文本}")
        texttiny = TextMobject("{\\tiny 微小的文本}")
        self.play(textHuge.to_edge, UP)
        self.play(textHuge.shift, LEFT*2)
        self.play(texthuge.next_to, textHuge, DOWN, buff=0.1)
        self.play(textLARGE.next_to, texthuge,DOWN,buff=0.1)
        self.play(textLarge.next_to, textLARGE,DOWN,buff=0.1)
        self.play(textlarge.next_to, textLarge,DOWN,buff=0.1)
        self.play(textNormal.next_to, textlarge,DOWN,buff=0.1)
        self.play(textsmall.next_to, textNormal,DOWN,buff=0.1)
        self.play(textfootnotesize.next_to, textNormal,RIGHT,buff=0.1)
        self.play(textscriptsize.next_to, textfootnotesize,DOWN,buff=0.1)
        self.play(texttiny.next_to, textscriptsize, DOWN,buff=0.1)
        #self.play(*[Write(x) for x in [textHuge, texthuge, textLARGE, textLarge, textlarge,
        #    textNormal, textsmall, textfootnotesize, textscriptsize, texttiny]])
        self.wait()
        self.play(*[FadeOut(x) for x in [title, textHuge, texthuge, textLARGE, textLarge, 
            textlarge, textNormal, textsmall, textfootnotesize, textscriptsize, texttiny]])
        self.wait()

        title = TextMobject('数学公式')
        title.shift(UP*2.5)
        self.play(Write(title), title.set_color, BLUE)
        # 数学公式
        f = TextMobject('$E=mc^2$')
        self.play(Write(f))
        self.wait()
        g = TexMobject(r'sign(x) =\begin{cases}+1&, x \geq 0\\-1&, x < 0 \end{cases}')
        self.play(g.next_to, f, LEFT)
        self.play(f.shift, RIGHT*3, g.shift, RIGHT*1.5)
        self.wait()
        self.play(*[FadeOut(x) for x in [title, f, g]])
        self.wait()

        title = TextMobject('代码')
        title.shift(UP*2.5)
        self.play(Write(title), title.set_color, BLUE)
        # 代码
        c = TextMobject('''
\\begin{lstlisting}[language=C],
int main(int argc, char ** argv) {
    printf("Hello, world!");
    return 0;
}
\\end{lstlisting}''')
        self.play(Write(c))
        self.wait(1)
        self.play(*[FadeOut(x) for x in [title, c]])
        self.wait()
        