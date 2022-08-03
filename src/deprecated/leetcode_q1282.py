"""
#Leetcode短视频# 第01集
Q1282 将人员按给定组的大小归为同一组
"""

"""过时
当前文档仅仅适用于旧版manim，在新版的manimgl和社区版manim上无法运行。
由于迁移麻烦，因此不考虑进行相应迁移。
"""


from manimlib.imports import *


class BasicScene(Scene):
    """用于提供一些公共的函数"""

    def disp_input(self, groupsize):
        # 创建矩形框
        rect_arr = VGroup(
            *[
                Rectangle(height=1, width=1).shift(RIGHT * (idx + 1) + 2 * UP)
                for idx, s in enumerate(groupsize)
            ]
        )
        rect_arr.shift(4 * LEFT)
        self.play(Write(rect_arr))
        # 打印提示信息
        prompt = TextMobject("每个人都有一个id")
        prompt.move_to(rect_arr.get_center() + UP)
        self.play(Write(prompt))
        self.wait()
        self.play(FadeOut(prompt), run_time=0.5)
        # 创建人员编号
        id_arr = TextMobject(*[str(idx) for idx, s in enumerate(groupsize)])
        for idx, rect in enumerate(rect_arr):
            person = TextMobject("人员[{}]".format(idx))
            person.move_to(rect.get_center() + UP)
            a = Arrow(person.get_center(), rect.get_center() + 0.2 * UP, color=GREEN)
            self.play(
                id_arr[idx].move_to,
                rect.get_center(),
                Write(person),
                Write(a),
                run_time=0.5,
            )
            self.play(FadeOut(a), FadeOut(person), run_time=0.25)
        self.play(id_arr.set_color, BLUE)
        # 打印提示信息
        prompt = TextMobject("每个人要求所在组的大小必须满足")
        prompt.move_to(rect_arr.get_center() + 2 * DOWN)
        self.play(Write(prompt))
        self.wait()
        self.play(FadeOut(prompt))
        # 增加人员要求所在组大小
        size_arr = TextMobject(*[str(s) for idx, s in enumerate(groupsize)])
        anims = []
        for idx, s in enumerate(size_arr):
            s.move_to(rect_arr[idx].get_center() + DOWN)
            s.set_color(RED)
            anims.append(ReplacementTransform(id_arr[idx].copy(), s))
        self.play(*anims, run_time=1)
        self.wait()

        return rect_arr, id_arr, size_arr

    def disp_example(self, groupsize, group_id, is_clear=False):
        rect_arr, id_arr, size_arr = self.disp_input(groupsize)
        # 绘制要求的输出结果
        for idx, gid in enumerate(group_id):
            # 创建分组矩形框
            rects = VGroup(
                *[
                    Rectangle(height=1, width=1).shift(RIGHT * (i + 1))
                    for i, v in enumerate(gid)
                ]
            )
            if idx > 0:
                rects.shift(
                    (5.5 - (idx + len(group_id[idx - 1])) * 1.5) * LEFT + 1.5 * DOWN
                )
            else:
                rects.shift((5.5 - idx * 1.5) * LEFT + 1.5 * DOWN)
            prompt = TextMobject("大小为", "{}".format(len(rects)), "的组")
            prompt.move_to(rects.get_center() + DOWN * 1.2)
            prompt[1].set_color(RED)
            anims = [
                ReplacementTransform(size_arr[pid].copy(), prompt[1]) for pid in gid
            ]
            self.play(Write(rects), Write(prompt), *anims, run_time=0.5)

            # 放置属于该分组的人员
            ids = TextMobject(*["{}".format(v) for i, v in enumerate(gid)])
            anims = []
            for i, rect in enumerate(rects):
                ids[i].move_to(rect.get_center())
                ids[i].set_color(BLUE)
                anims.append(ReplacementTransform(id_arr[gid[i]].copy(), ids[i]))
            self.play(*anims, run_time=0.5)
            self.wait(1)


class Opening(BasicScene):
    def construct(self):
        # display title
        title = TextMobject("Q1282", "将人员分配到指定大小的群")
        self.play(Write(title))
        self.wait()


class Example01(BasicScene):
    def construct(self):
        # 开头
        title = TextMobject("示例 1")
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))
        # 例子
        groupsize = [3, 3, 3, 3, 3, 1, 3]
        group_id = [[5], [0, 1, 2], [3, 4, 6]]
        self.disp_example(groupsize, group_id)


class Example02(BasicScene):
    def construct(self):
        # 开头
        title = TextMobject("示例 2")
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))
        # 例子
        groupsize = [2, 1, 3, 3, 3, 2]
        group_id = [[1], [0, 5], [2, 3, 4]]
        self.disp_example(groupsize, group_id, is_clear=True)


class Solution01(BasicScene):
    """用于生成第一种解决方案讲解动画"""

    def construct(self):
        # 开头
        title = TextMobject("Q1282的 ", r"解决方案 1\\", "按顺序，不够用就创建新的组")
        title[2].scale(0.8)
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))
        # 解决方案
        groupsize = [3, 3, 3, 3, 3, 1, 3]
        self.disp_slt(groupsize)
        self.wait()
        # 时间复杂度
        self.clear()
        prompt = TextMobject(r"最坏情况的时间复杂度\\", "$O(n^2)$")
        self.play(Write(prompt))
        self.play(prompt[1].set_color, GREEN, prompt[1].shift(DOWN * 0.5))
        self.wait()

    def disp_slt(self, groupsize):
        rect_arr, id_arr, size_arr = self.disp_input(groupsize)
        print("输入绘制完成")
        # explain algorithm
        group_list = []
        idx_arrow = None
        for idx, s in enumerate(groupsize):
            # change color of rect
            c = rect_arr[idx].get_center()
            if idx > 0:
                self.play(
                    rect_arr[idx - 1].set_color,
                    WHITE,
                    rect_arr[idx].set_color,
                    RED,
                    idx_arrow.move_to,
                    c + 0.5 * UP,
                )
            else:
                idx_arrow = Arrow(c + UP, c, color=GREEN)
                self.play(rect_arr[idx].set_color, RED, Write(idx_arrow))
            success = False
            for _, g in enumerate(group_list):
                if g[0] == s and g[1] < g[0]:
                    # arrange person in g[2][g[1]]
                    t = TextMobject(str(idx)).set_color(BLUE)
                    # self.play(Write(g[2][g[1]]), run_time=0.5)
                    t.move_to(g[2][g[1]].get_center())
                    self.play(ReplacementTransform(id_arr[idx].copy(), t), run_time=1)
                    g[3].append(t)
                    # change flags
                    g[1] += 1
                    success = True
                    break
            if success is False:
                # 说明创建新的组
                prompt_head = TextMobject("创建新的组...")
                self.play(Write(prompt_head))
                self.wait()
                self.play(FadeOut(prompt_head))
                # 绘制组的矩形框
                g_mobj = VGroup(
                    *[
                        Rectangle(height=1, width=1).shift(RIGHT * i * 1)
                        for i in range(s)
                    ]
                )
                g_mobj.shift((4 - len(group_list) * 4.4) * LEFT + 2 * DOWN)
                g_mobj.set_color(GREEN)
                # 组大小说明
                prompt = TextMobject("大小为", "{}".format(len(g_mobj)), "的组")
                prompt[1].set_color(RED)
                prompt.scale(0.8)
                prompt.move_to(g_mobj.get_center() + 1.2 * DOWN)
                self.play(
                    Write(g_mobj),
                    Write(prompt),
                    ReplacementTransform(size_arr[idx].copy(), prompt[1]),
                    run_time=1,
                )
                # 分配人员
                t = TextMobject(str(idx)).set_color(BLUE)
                t.move_to(g_mobj[0].get_center())
                self.play(ReplacementTransform(id_arr[idx].copy(), t), run_time=1)
                # record the new group
                group_list.append([s, 1, g_mobj, [t]])


class Solution02(BasicScene):
    """用于生成第二种解决方案讲解动画"""

    def construct(self):
        # 开头
        title = TextMobject("Q1282的 ", r"解决方案 2\\", "先分类，再拆分到组")
        title[2].scale(0.8)
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))
        # 解决方案
        groupsize = [2, 1, 3, 3, 3, 2]
        self.disp_slt(groupsize)
        self.wait()
        # 时间复杂度
        self.clear()
        prompt = TextMobject(r"最坏情况的时间复杂度\\", "$O(n)$")
        self.play(Write(prompt))
        self.play(prompt[1].set_color, GREEN, prompt[1].shift(DOWN * 0.5))
        self.wait()

    def disp_slt(self, groupsize):
        rect_arr, id_arr, size_arr = self.disp_input(groupsize)
        # create mapping from size to id
        g_dict = {}
        idx_arrow = None
        for idx, s in enumerate(groupsize):
            # change color of rect
            c = rect_arr[idx].get_center()
            if idx > 0:
                self.play(
                    rect_arr[idx - 1].set_color,
                    WHITE,
                    rect_arr[idx].set_color,
                    RED,
                    idx_arrow.move_to,
                    c + 0.5 * UP,
                )
            else:
                idx_arrow = Arrow(c + UP, c, color=GREEN)
                self.play(rect_arr[idx].set_color, RED, Write(idx_arrow))

            if s not in g_dict:
                # 提示
                prompt_head = TextMobject("根据组大小创建新的组...")
                prompt_head.move_to(rect_arr.get_center() + UP * 1.3)
                self.play(Write(prompt_head))
                self.wait()
                self.play(FadeOut(prompt_head))

                # 绘制组大小
                group_text = TextMobject("大小为", "{}".format(s), "的组")
                group_text.scale(0.8)
                num = len(g_dict)
                group_text.shift(5 * LEFT + 1.5 * num * DOWN)
                self.play(
                    Write(group_text),
                    group_text[1].set_color,
                    RED,
                    ReplacementTransform(size_arr[idx].copy(), group_text[1]),
                )
                # 绘制矩形框
                rect = Rectangle(height=1, width=1).shift(DOWN * num * 1.5)
                self.play(Write(rect))
                arrow = Arrow(
                    group_text.get_center() + RIGHT * 1.5, rect.get_center() + LEFT
                )
                self.play(Write(arrow), run_time=0.5)
                # 分配人员
                id_text = TextMobject(str(idx))
                id_text.move_to(rect.get_center())
                id_text.set_color(BLUE)
                self.play(ReplacementTransform(id_arr[idx].copy(), id_text))

                g_dict[s] = [[idx], [rect]]

            else:
                # 创建矩形框
                rect = Rectangle(height=1, width=1).shift(
                    g_dict[s][1][-1].get_center() + RIGHT
                )
                self.play(Write(rect))
                # 分配人员
                id_text = TextMobject(str(idx))
                id_text.move_to(rect.get_center())
                id_text.set_color(BLUE)
                self.play(ReplacementTransform(id_arr[idx].copy(), id_text))
                # 记录当前人员
                g_dict[s][0].append(idx)
                g_dict[s][1].append(rect)

        # 拆分大于1的组
        prompt_head = TextMobject("拆分大于1的组...")
        prompt_head.move_to(DOWN * 1.5 + RIGHT * 3.5)
        self.play(Write(prompt_head))
        self.wait()
        self.play(FadeOut(prompt_head))
        # split into multiple groups with the same size
        for size, idxes in g_dict.items():
            n = len(idxes[0]) // size
            end_point = idxes[1][-1].get_center()
            arrow = Arrow(end_point + RIGHT, end_point + 2 * RIGHT)
            self.play(Write(arrow))
            num_text = TextMobject(str(n), " 个 group")
            num_text.move_to(end_point + 3.5 * RIGHT)
            self.play(Write(num_text))


def create_peole(idx, color=RED):
    p = ImageMobject("assets/leetcode/start/people.png")
    i = TextMobject(str(idx), color=RED)
    i.move_to(p.get_center() + 0.6 * DOWN + 0.3 * LEFT)
    people = Group(p, i)
    return people


class Problem(Scene):
    """用于生成描述问题的动画"""

    def construct(self):
        groupsize = [3, 3, 3, 3, 3, 1, 3]
        # group_id = [[5],[0,1,2],[3,4,6]]

        # 创建人物并标号
        persons = self.create_persons(groupsize)

        # 分群
        group_id = [[5], [0, 1, 2], [3, 4, 6]]
        self.play(persons[5].move_to, DOWN + 5 * LEFT)
        c1 = Circle(radius=5, color=YELLOW)
        self.play(c1.move_to, persons[5].get_center() + LEFT * 0.2, c1.scale, 0.3)
        self.play(persons[0].move_to, 0.5 * LEFT + DOWN + UL * 1.3)
        self.play(persons[1].move_to, 0.5 * LEFT + DOWN + UR * 1.3)
        self.play(persons[2].move_to, 0.5 * LEFT + DOWN + 1.5 * DOWN)
        c2 = Circle(radius=5)
        self.play(c2.move_to, DOWN + LEFT * 0.8 + UR * 0.2, c2.scale, 0.6)
        self.play(persons[3].move_to, DOWN - 5 * LEFT + UL * 1.3)
        self.play(persons[4].move_to, DOWN - 5 * LEFT + UR * 1.3)
        self.play(persons[6].move_to, DOWN - 5 * LEFT + 1.5 * DOWN)
        c3 = Circle(radius=5, color=GREEN)
        self.play(c3.move_to, DOWN - 5 * LEFT, c3.scale, 0.6)
        self.wait()

        # 多个解
        self.swap(persons[0], persons[6])
        self.wait()
        self.swap(persons[2], persons[3])
        self.wait()
        self.swap(persons[1], persons[0])
        self.wait()

    def create_persons(self, groupsize):
        persons = []
        for idx, gs in enumerate(groupsize):
            p = create_peole(idx)
            persons.append(p)
            p.move_to(UP * 4)
            self.play(p.move_to, 2 * LEFT * (3 - idx) + 0.3 * RIGHT)
        self.wait()

        # 标号闪烁
        # for idx, gs in enumerate(groupsize):
        anims = [[persons[idx][1].shift, DOWN] for idx, gs in enumerate(groupsize)]
        self.play(*[x for anim in anims for x in anim])
        anims = [[persons[idx][1].set_color, GREEN] for idx, gs in enumerate(groupsize)]
        self.play(*[x for anim in anims for x in anim])
        anims = [[persons[idx][1].set_color, BLUE] for idx, gs in enumerate(groupsize)]
        self.play(*[x for anim in anims for x in anim])
        anims = [
            [persons[idx][1].set_color, YELLOW] for idx, gs in enumerate(groupsize)
        ]
        self.play(*[x for anim in anims for x in anim])
        anims = [[persons[idx][1].set_color, RED] for idx, gs in enumerate(groupsize)]
        self.play(*[x for anim in anims for x in anim])
        anims = [[persons[idx][1].shift, UP] for idx, gs in enumerate(groupsize)]
        self.play(*[x for anim in anims for x in anim])
        self.wait()

        # 整体上移
        anims = [[persons[idx].shift, UP * 2.0] for idx, gs in enumerate(groupsize)]
        self.play(*[x for anim in anims for x in anim])
        self.wait()

        # 创建群大小
        for idx, gs in enumerate(groupsize):
            size = TextMobject(str(gs), color=BLUE)
            size.move_to(persons[idx].get_center())
            self.play(size.move_to, persons[idx].get_center() + 1.5 * UP)
            persons[idx].add(size)
        self.wait()

        return persons

    def swap(self, obj1, obj2):
        pos1 = obj1.get_center()
        pos2 = obj2.get_center()
        self.play(obj1.move_to, pos2, obj2.move_to, pos1)


class Solution(Problem):
    """用于生成解决方案描述动画"""

    def construct(self):
        groupsize = [3, 3, 3, 3, 3, 1, 3]
        # 创建人员
        persons = self.create_persons(groupsize)
        # 创建索引框
        self.rect = Rectangle(width=2, height=3, color=YELLOW)
        self.index(persons[0])
        self.wait()

        # 创建第一个群
        self.play(persons[0].move_to, 5 * LEFT + DOWN)
        c1 = Circle(radius=5, color=RED)
        self.play(c1.move_to, LEFT * 4 + 1.5 * DOWN, c1.scale, 0.6)
        cap = TextMobject("3人群", color=RED)
        self.play(FadeIn(cap), cap.move_to, c1.get_center() + DL * 2)

        # 安排第2个人
        self.index(persons[1])
        self.play(persons[1].move_to, persons[0].get_center() + UR * 2 + DOWN)

        # 安排第3个人
        self.index(persons[2])
        self.play(persons[2].move_to, persons[0].get_center() + DR * 2 + 0.2 * UP)

        # 安排第4个人
        self.index(persons[3])
        self.play(persons[3].move_to, DOWN)
        c2 = Circle(radius=5, color=GREEN)
        self.play(c2.move_to, DOWN + RIGHT, c2.scale, 0.6)
        cap = TextMobject("3人群", color=GREEN)
        self.play(FadeIn(cap), cap.move_to, c2.get_center() + DL * 2 + RIGHT)

        # 安排第5个人
        self.index(persons[4])
        self.play(persons[4].move_to, persons[3].get_center() + UR * 2 + DOWN)

        # 安排第6个人
        self.index(persons[5])
        self.play(persons[5].move_to, DOWN + RIGHT * 5.5)
        c3 = Circle(radius=5, color=PINK)
        self.play(c3.move_to, persons[5].get_center() + LEFT * 0.2, c3.scale, 0.3)
        cap = TextMobject("1人群", color=PINK)
        self.play(FadeIn(cap), cap.move_to, c3.get_center() + 2 * DOWN)

        # 安排第7个人
        self.index(persons[6])
        self.play(persons[6].move_to, persons[3].get_center() + DR * 2 + UP * 0.5)

        # 去除索引框
        self.play(FadeOut(self.rect))

        self.clear()
        self.wait()
        cap = TextMobject(r"$T = O(n^2)$")
        self.play(ShowCreation(cap), cap.scale, 2)

    def index(self, person):
        self.play(self.rect.move_to, person.get_center() + 0.3 * LEFT)


class SolutionOpt(Solution):
    def construct(self):
        groupsize = [3, 3, 3, 3, 3, 1, 3]
        # 创建人员
        persons = self.create_persons(groupsize)
        # 创建索引框
        self.rect = Rectangle(width=2, height=3, color=YELLOW)
        self.index(persons[0])
        self.wait()

        # 找出要求3人群的人员
        cap = TextMobject("3人群", color=RED)
        self.play(cap.move_to, LEFT * 3 + DOWN * 2)
        c1 = Circle(radius=1, color=RED)
        self.play(c1.move_to, cap.get_center())
        arrow0 = Arrow(c1.get_center() + UL * 0.5, persons[0].get_center() + DOWN)
        self.play(ShowCreation(arrow0))
        self.wait()

        # 第2个人员
        self.index(persons[1])
        arrow1 = Arrow(c1.get_center() + UL * 0.5, persons[1].get_center() + DOWN)
        self.play(ShowCreation(arrow1))

        # 第3个人员
        self.index(persons[2])
        arrow2 = Arrow(c1.get_center() + UL * 0.5, persons[2].get_center() + DOWN)
        self.play(ShowCreation(arrow2))

        # 第4个人员
        self.index(persons[3])
        arrow3 = Arrow(c1.get_center() + UL * 0.5, persons[3].get_center() + DOWN)
        self.play(ShowCreation(arrow3))

        # 第5个人员
        self.index(persons[4])
        arrow4 = Arrow(c1.get_center() + UL * 0.5, persons[4].get_center() + DOWN)
        self.play(ShowCreation(arrow4))
        self.wait()

        # 第6个人员
        self.index(persons[5])
        self.play(persons[5].move_to, DOWN * 2.5 + RIGHT * 5)
        cap = TextMobject("1人群", color=PINK)
        self.play(cap.move_to, DOWN * 3)
        c2 = Circle(radius=1, color=PINK)
        self.play(c2.move_to, cap.get_center())
        arrow5 = Arrow(
            c2.get_center() + 0.5 * RIGHT, persons[5].get_center() + 0.5 * LEFT
        )
        self.play(ShowCreation(arrow5))
        self.wait()

        # 第7个人员
        self.index(persons[6])
        arrow6 = Arrow(c1.get_center() + UL * 0.5, persons[6].get_center() + DOWN)
        self.play(ShowCreation(arrow6))
        self.wait()

        # 移除索引框
        self.play(FadeOut(self.rect))

        # 第一个3人群
        r1 = Rectangle(width=6, height=3, color=RED)
        self.play(r1.move_to, persons[1].get_center() + 0.3 * LEFT)
        cap = TextMobject("第一个3人群", color=RED)
        self.play(ShowCreation(cap), cap.move_to, r1.get_center())
        self.wait()

        # 第二个3人群
        r2 = Rectangle(width=7.5, height=3, color=RED)
        self.play(r2.move_to, persons[4].get_center() + RIGHT)
        cap = TextMobject("第二个3人群", color=RED)
        self.play(ShowCreation(cap), cap.move_to, r2.get_center())
        self.wait()

        # 第一个1人群
        r3 = Rectangle(width=2, height=3, color=PINK)
        self.play(r3.move_to, persons[5].get_center() + 0.3 * LEFT)
        cap = TextMobject("第一个1人群", color=PINK)
        self.play(ShowCreation(cap), cap.move_to, r3.get_center() + 2 * UP)
        self.wait()

        # 去除索引框
        self.play(FadeOut(self.rect))

        self.clear()
        self.wait()
        cap = TextMobject(r"$T = O(nlog(n))$")
        self.play(ShowCreation(cap), cap.scale, 2)


class Tail(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": "#ffffff",
        },
    }

    def construct(self):
        wechat = ImageMobject("assets/leetcode/start/wechat.png")
        xigua = ImageMobject("assets/leetcode/start/xigua.png")
        bili = ImageMobject("assets/leetcode/start/bilibili.png")
        youtube = ImageMobject("assets/leetcode/start/youtube.png")
        wechat.move_to(4 * UP)
        xigua.move_to(4 * UP)
        bili.move_to(4 * UP)

        text = self.make_title()
        self.play(
            wechat.move_to,
            3 * LEFT + UP,
            xigua.move_to,
            ORIGIN + UP,
            bili.move_to,
            3 * RIGHT + UP,
            run_time=1,
        )

        self.make_slogan(text)
        self.wait()

    def make_title(self):
        text = TextMobject(r"青衣", r"极客", r"频道", r"视频发布平台", color=BLACK)
        text.move_to(4 * UP)
        self.play(ShowCreation(text), text.move_to, 3 * UP, run_time=1)
        self.play(text[0].shift, 0.5 * LEFT, text[1].shift, 0.5 * LEFT, run_time=0.5)
        self.play(text[0].set_color, BLUE, text[1].set_color, GREEN, run_time=0.5)
        self.play(text[:2].scale, 1.3, run_time=0.5)
        return text

    def make_slogan(self, text):
        slogan = TextMobject(r"一个", r"“有用”", r"的频道", color=BLACK)
        slogan.move_to(DOWN * 1.5 + 2 * RIGHT)
        slogan.rotate(8 * DEGREES)
        self.play(ShowCreation(slogan))
        self.play(text[:2].copy().move_to, 1.7 * DOWN + 2 * LEFT, run_time=0.5)
        self.play(slogan[1].set_color, RED, run_time=0.5)


class Tail2(Tail):
    CONFIG = {
        "camera_config": {
            "background_color": "#ffffff",
        },
    }

    def construct(self):
        wechat = ImageMobject("assets/leetcode/start/wechat.png")
        xigua = ImageMobject("assets/leetcode/start/xigua.png")
        bili = ImageMobject("assets/leetcode/start/bilibili.png")
        youtube = ImageMobject("assets/leetcode/start/youtube.png")
        wechat.move_to(4 * UP)
        xigua.move_to(4 * UP)
        bili.move_to(4 * UP)
        youtube.move_to(4 * UP)

        text = self.make_title()

        self.play(
            wechat.move_to,
            4 * LEFT + UP,
            xigua.move_to,
            1.33 * LEFT + UP,
            bili.move_to,
            1.33 * RIGHT + UP,
            youtube.move_to,
            4 * RIGHT + UP,
        )

        self.make_slogan(text)
        self.wait()
