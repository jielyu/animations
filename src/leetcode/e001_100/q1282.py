"""
#Leetcode短视频# 第01集
Q1282 将人员按给定组的大小归为同一组
"""

from manimlib.imports import *


class BasicScene(Scene):
    """用于提供一些公共的函数
    """

    def disp_input(self, groupsize):
        # 创建矩形框
        rect_arr = VGroup(*[Rectangle(height=1, width=1).shift(RIGHT*(idx+1)+2*UP) 
                               for idx, s in enumerate(groupsize)])
        rect_arr.shift(4*LEFT)
        self.play(Write(rect_arr))
        # 打印提示信息
        prompt = TextMobject('每个人都有一个id')
        prompt.move_to(rect_arr.get_center() + UP)
        self.play(Write(prompt))
        self.wait()
        self.play(FadeOut(prompt), run_time=0.5)
        # 创建人员编号
        id_arr = TextMobject(*[str(idx) for idx, s in enumerate(groupsize)])
        for idx, rect in enumerate(rect_arr):
            person = TextMobject('人员[{}]'.format(idx))
            person.move_to(rect.get_center() + UP)
            a = Arrow(person.get_center(), rect.get_center()+0.2*UP, color=GREEN)
            self.play(id_arr[idx].move_to, rect.get_center(), Write(person), Write(a), run_time=0.5)
            self.play(FadeOut(a), FadeOut(person), run_time=0.25)
        self.play(id_arr.set_color, BLUE)
        # 打印提示信息
        prompt = TextMobject('每个人要求所在组的大小必须满足')
        prompt.move_to(rect_arr.get_center() + 2*DOWN)
        self.play(Write(prompt))
        self.wait()
        self.play(FadeOut(prompt))
        # 增加人员要求所在组大小
        size_arr = TextMobject(*[str(s) for idx, s in enumerate(groupsize)])
        anims = []
        for idx, s in enumerate(size_arr):
            s.move_to(rect_arr[idx].get_center()+DOWN)
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
            rects = VGroup(*[Rectangle(height=1, width=1).shift(RIGHT*(i+1))
                                 for i, v in enumerate(gid)])
            if idx > 0:
                rects.shift((5.5-(idx+len(group_id[idx-1]))*1.5)*LEFT + 1.5*DOWN)
            else:
                rects.shift((5.5-idx*1.5)*LEFT + 1.5*DOWN)
            prompt = TextMobject('大小为', '{}'.format(len(rects)),'的组')
            prompt.move_to(rects.get_center() + DOWN*1.2)
            prompt[1].set_color(RED)
            anims = [ReplacementTransform(size_arr[pid].copy(), prompt[1]) for pid in gid]
            self.play(Write(rects), Write(prompt), *anims, run_time=0.5)

            # 放置属于该分组的人员
            ids = TextMobject(*['{}'.format(v) for i, v in enumerate(gid)])
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
        title = TextMobject('Q1282', '将人们按给定组的大小归为同一组')
        self.play(Write(title))
        self.wait()

class Example01(BasicScene):

    def construct(self):
        # 开头
        title = TextMobject('示例 1')
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))
        # 例子
        groupsize = [3,3,3,3,3,1,3]
        group_id = [[5],[0,1,2],[3,4,6]]
        self.disp_example(groupsize, group_id)

class Example02(BasicScene):

    def construct(self):
        # 开头
        title = TextMobject('示例 2')
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))
        # 例子
        groupsize = [2,1,3,3,3,2]
        group_id = [[1],[0,5],[2,3,4]]
        self.disp_example(groupsize, group_id, is_clear=True)


class Solution01(BasicScene):
    """用于生成第一种解决方案讲解动画
    """
    def construct(self):
        # 开头
        title = TextMobject('Q1282的 ', r'解决方案 1\\', '按顺序，不够用就创建新的组')
        title[2].scale(0.8)
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))
        # 解决方案
        groupsize = [3,3,3,3,3,1,3]
        self.disp_slt(groupsize)
        self.wait()
        # 时间复杂度
        self.clear()
        prompt = TextMobject(r'最坏情况的时间复杂度\\', '$O(n^2)$')
        self.play(Write(prompt))
        self.play(prompt[1].set_color, GREEN, prompt[1].shift(DOWN*0.5))
        self.wait()
        
    def disp_slt(self, groupsize):
        rect_arr, id_arr, size_arr = self.disp_input(groupsize)
        print('输入绘制完成')
        # explain algorithm
        group_list = []
        idx_arrow = None
        for idx, s in enumerate(groupsize):
            # change color of rect
            c = rect_arr[idx].get_center()
            if idx > 0:
                self.play(rect_arr[idx-1].set_color, WHITE, 
                          rect_arr[idx].set_color, RED,
                          idx_arrow.move_to, c + 0.5*UP)
            else:
                idx_arrow = Arrow(c + UP, c, color=GREEN)
                self.play(rect_arr[idx].set_color, RED, Write(idx_arrow))
            success = False
            for _, g in enumerate(group_list):
                if g[0] == s and g[1] < g[0]:
                    # arrange person in g[2][g[1]]
                    t = TextMobject(str(idx)).set_color(BLUE)
                    #self.play(Write(g[2][g[1]]), run_time=0.5)
                    t.move_to(g[2][g[1]].get_center())
                    self.play(ReplacementTransform(id_arr[idx].copy(), t), run_time=1)
                    g[3].append(t)
                    # change flags
                    g[1] += 1
                    success = True
                    break
            if success is False:
                # 说明创建新的组
                prompt_head = TextMobject('创建新的组...')
                self.play(Write(prompt_head))
                self.wait()
                self.play(FadeOut(prompt_head))
                # 绘制组的矩形框
                g_mobj = VGroup(*[Rectangle(height=1, width=1).shift(RIGHT*i*1) for i in range(s)])
                g_mobj.shift((4-len(group_list)*4.4)*LEFT + 2*DOWN)
                g_mobj.set_color(GREEN)
                # 组大小说明
                prompt = TextMobject('大小为', '{}'.format(len(g_mobj)),'的组')
                prompt[1].set_color(RED)
                prompt.scale(0.8)
                prompt.move_to(g_mobj.get_center() + 1.2*DOWN)
                self.play(Write(g_mobj), Write(prompt), 
                          ReplacementTransform(size_arr[idx].copy(), prompt[1]), 
                          run_time=1)
                # 分配人员
                t = TextMobject(str(idx)).set_color(BLUE)
                t.move_to(g_mobj[0].get_center())
                self.play(ReplacementTransform(id_arr[idx].copy(), t), run_time=1)
                # record the new group
                group_list.append([s, 1, g_mobj, [t]])



class Solution02(BasicScene):
    """用于生成第二种解决方案讲解动画
    """
    def construct(self):
        # 开头
        title = TextMobject('Q1282的 ', r'解决方案 2\\', '先分类，再拆分到组')
        title[2].scale(0.8)
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))
        # 解决方案
        groupsize = [2,1,3,3,3,2]
        self.disp_slt(groupsize)
        self.wait()
        # 时间复杂度
        self.clear()
        prompt = TextMobject(r'最坏情况的时间复杂度\\', '$O(n)$')
        self.play(Write(prompt))
        self.play(prompt[1].set_color, GREEN, prompt[1].shift(DOWN*0.5))
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
                self.play(rect_arr[idx-1].set_color, WHITE, 
                          rect_arr[idx].set_color, RED, 
                          idx_arrow.move_to, c + 0.5*UP)
            else:
                idx_arrow = Arrow(c + UP, c, color=GREEN)
                self.play(rect_arr[idx].set_color, RED, Write(idx_arrow))
                

            if s not in g_dict:
                # 提示
                prompt_head = TextMobject('根据组大小创建新的组...')
                prompt_head.move_to(rect_arr.get_center() + UP*1.3)
                self.play(Write(prompt_head))
                self.wait()
                self.play(FadeOut(prompt_head))

                # 绘制组大小
                group_text = TextMobject('大小为', '{}'.format(s),'的组')
                group_text.scale(0.8)
                num = len(g_dict)
                group_text.shift(5*LEFT + 1.5*num*DOWN)
                self.play(Write(group_text), group_text[1].set_color, RED, 
                          ReplacementTransform(size_arr[idx].copy(), group_text[1]))
                # 绘制矩形框
                rect = Rectangle(height=1, width=1).shift(DOWN * num * 1.5)
                self.play(Write(rect))
                arrow = Arrow(group_text.get_center()+RIGHT*1.5, rect.get_center()+LEFT)
                self.play(Write(arrow), run_time=0.5)
                # 分配人员
                id_text = TextMobject(str(idx))
                id_text.move_to(rect.get_center())
                id_text.set_color(BLUE)
                self.play(ReplacementTransform(id_arr[idx].copy(), id_text))

                g_dict[s] = [[idx], [rect]]
                
            else:
                # 创建矩形框
                rect = Rectangle(height=1, width=1).shift(g_dict[s][1][-1].get_center() + RIGHT)
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
        prompt_head = TextMobject('拆分大于1的组...')
        prompt_head.move_to(DOWN*1.5 + RIGHT*3.5)
        self.play(Write(prompt_head))
        self.wait()
        self.play(FadeOut(prompt_head))
        # split into multiple groups with the same size
        for size, idxes in g_dict.items():
            n = len(idxes[0]) // size
            end_point = idxes[1][-1].get_center()
            arrow = Arrow(end_point+RIGHT, end_point+2*RIGHT)
            self.play(Write(arrow))
            num_text = TextMobject(str(n), ' 个 group')
            num_text.move_to(end_point + 3.5*RIGHT)
            self.play(Write(num_text))

            