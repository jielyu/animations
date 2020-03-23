from manimlib.imports import *


class E01Scene(Scene):
    """用于提供一些公共的函数
    """

    def disp_input(self, groupsize):
        # create rectangle
        rect_arr = VGroup(*[Rectangle(height=1, width=1).shift(RIGHT*(idx+1)+2*UP) 
                               for idx, s in enumerate(groupsize)])
        rect_arr.shift(4*LEFT)
        # add annotation for person ids
        pid = TextMobject('PersonId')
        pid.move_to(rect_arr.get_center()+5*LEFT+UP)
        self.play(Write(pid))
        self.play(pid.set_color, YELLOW)
        arrow1 = Arrow(pid.get_center(), rect_arr[0].get_center())
        self.play(Write(arrow1))
        # create id array
        id_arr = TextMobject(*[str(idx) for idx, s in enumerate(groupsize)])
        for idx, rect in enumerate(rect_arr):
            self.play(Write(rect), run_time=0.5)
            self.play(id_arr[idx].move_to, rect.get_center(), run_time=0.5)
        
        # add annotation for group size
        gsize = TextMobject('GroupSize')
        gsize.move_to(rect_arr.get_center()+5*LEFT+2*DOWN)
        self.play(Write(gsize))
        self.play(gsize.set_color, YELLOW)
        arrow2 = Arrow(gsize.get_center(), rect_arr[0].get_center()+DOWN)
        self.play(Write(arrow2))
        # create size array
        size_arr = TextMobject(*[str(s) for idx, s in enumerate(groupsize)])
        for idx, s in enumerate(size_arr):
            s.move_to(rect_arr[idx].get_center()+DOWN)
            s.set_color(RED)
            self.play(ReplacementTransform(id_arr[idx].copy(), s), run_time=0.5)
        self.wait()
        # remove annotations
        self.play(FadeOutAndShiftDown(pid), FadeOut(arrow1))
        self.play(FadeOutAndShiftDown(gsize), FadeOut(arrow2))

        return rect_arr, id_arr, size_arr


class Problem(E01Scene):
    """用于生成问题描述动画
    """
    def construct(self):
        # for example 1
        groupsize = [3,3,3,3,3,1,3]
        group_id = [[5],[0,1,2],[3,4,6]]
        self.disp_example(groupsize, group_id, is_clear=True)
        # for example 2
        groupsize = [2,1,3,3,3,2]
        group_id = [[1],[0,5],[2,3,4]]
        self.disp_example(groupsize, group_id, is_clear=True)

    def disp_example(self, groupsize, group_id, is_clear=False):
        rect_arr, id_arr, size_arr = self.disp_input(groupsize)
        # display results
        rects_list = []
        ids_list = []
        for idx, gid in enumerate(group_id):
            # create objects
            rects = VGroup(*[Rectangle(height=1, width=1).shift(RIGHT*(i+1))
                                 for i, v in enumerate(gid)])
            if idx > 0:
                rects.shift((5.5-(idx+len(group_id[idx-1]))*1.5)*LEFT + 2*DOWN)
            else:
                rects.shift((5.5-idx*1.5)*LEFT + 2*DOWN)
            ids = TextMobject(*[str(v) for i, v in enumerate(gid)])
            # record objects
            rects_list.append(rects)
            ids_list.append(ids)
            # display
            for i, rect in enumerate(rects):
                self.play(Write(rect), run_time=0.5)
                ids[i].move_to(rect.get_center())
                ids[i].set_color(BLUE)
                self.play(ReplacementTransform(id_arr[gid[i]].copy(), ids[i]), run_time=0.5)
            self.wait(2)
        self.wait(2)
        if is_clear is True:
            self.clear()


class Solution01(E01Scene):
    """用于生成第一种解决方案讲解动画
    """
    def construct(self):
        # draw input animation
        groupsize = [3,3,3,3,3,1,3]
        group_id = [[5],[0,1,2],[3,4,6]]
        rect_arr, id_arr, size_arr = self.disp_input(groupsize)
        # explain algorithm
        group_list = []
        for idx, s in enumerate(groupsize):
            # change color of rect
            if idx > 0:
                self.play(rect_arr[idx-1].set_color, WHITE, rect_arr[idx].set_color, RED)
            else:
                self.play(rect_arr[idx].set_color, RED)
            success = False
            for _, g in enumerate(group_list):
                if g[0] == s and g[1] < g[0]:
                    # arrange person in g[2][g[1]]
                    t = TextMobject(str(idx)).set_color(BLUE)
                    #self.play(Write(g[2][g[1]]), run_time=0.5)
                    t.move_to(g[2][g[1]].get_center())
                    self.play(ReplacementTransform(id_arr[idx].copy(), t), run_time=0.5)
                    g[3].append(t)
                    # change flags
                    g[1] += 1
                    success = True
                    break
            if success is False:
                g_mobj = VGroup(*[Rectangle(height=1, width=1).shift(RIGHT*i) for i in range(s)])
                g_mobj.shift((4-len(group_list)*4)*LEFT + 2*DOWN)
                g_mobj.set_color(GREEN)
                self.play(Write(g_mobj), run_time=0.5)
                t = TextMobject(str(idx)).set_color(BLUE)
                t.move_to(g_mobj[0].get_center())
                self.play(ReplacementTransform(id_arr[idx].copy(), t), run_time=0.5)
                # record the new group
                group_list.append([s, 1, g_mobj, [t]])


class Solution02(E01Scene):
    """用于生成第二种解决方案讲解动画
    """
    def construct(self):
        # display input data
        #groupsize = [3,3,3,3,3,1,3]
        #group_id = [[5],[0,1,2],[3,4,6]]
        groupsize = [2,1,3,3,3,2]
        group_id = [[1],[0,5],[2,3,4]]
        rect_arr, id_arr, size_arr = self.disp_input(groupsize)
        # create mapping from size to id
        g_dict = {}
        for idx, s in enumerate(groupsize):
            if s not in g_dict:
                
                group_text = TextMobject('groupsize=', '{}'.format(s))
                group_text[1].set_color(YELLOW)
                num = len(g_dict)
                group_text.shift(5*LEFT + 1.5*num*DOWN)
                self.play(Write(group_text))
                
                rect = Rectangle(height=1, width=1).shift(DOWN * num * 1.5)
                self.play(Write(rect))
                arrow = Arrow(group_text.get_center()+RIGHT*1.5, rect.get_center()+LEFT)
                self.play(Write(arrow))
                
                id_text = TextMobject(str(idx))
                id_text.move_to(rect.get_center())
                id_text.set_color(BLUE)
                self.play(ReplacementTransform(id_arr[idx].copy(), id_text))

                g_dict[s] = [[idx], [rect]]
                
            else:
                # create and display rectangle 
                rect = Rectangle(height=1, width=1).shift(g_dict[s][1][-1].get_center() + RIGHT)
                self.play(Write(rect))
                # create and display string of person id
                id_text = TextMobject(str(idx))
                id_text.move_to(rect.get_center())
                id_text.set_color(BLUE)
                self.play(ReplacementTransform(id_arr[idx].copy(), id_text))
                # record current person id
                g_dict[s][0].append(idx)
                g_dict[s][1].append(rect)


        # split into multiple groups with the same size
        for size, idxes in g_dict.items():
            n = len(idxes[0]) // size
            end_point = idxes[1][-1].get_center()
            arrow = Arrow(end_point+RIGHT, end_point+2*RIGHT)
            self.play(Write(arrow))
            num_text = TextMobject(str(n), ' 个 group')
            num_text.move_to(end_point + 3.5*RIGHT)
            self.play(Write(num_text))
            