"""用于制作感知机算法思想原理的动画
"""

import os, math
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pickle
import io
import PIL

from manimlib.imports import *

# set numpy and tensorflow random seed
np.random.seed(0)
tf.random.set_seed(0)

def gen_data(num_samples, pos_ratio=0.5, margin=0.2, candidate_scale=5, shuffle=True):
    """用于生成样本数据，每个样本由二维特征和一个标签组成

    Args:
        num_samples (int): 样本数量
        pos_ratio (float): 默认值=0.5， 正样本占比，数值范围 (0, 1.0)
        margin (float): 默认值=0.2，正负样本点集与分类直线的平移亮
        candidate_scale (int): 默认值=5，样本候选集规模
        shuffle (bool): 默认值=True，打乱排列 

    Returns:
        np.ndarray, (num_samples, 2)，二维样本特征
        np.ndarray, (num_samples,)，样本标签，取值{-1, 1}

    Raises:
        ValueError: 传入数值范围不满足要求
    """
    # check args

    # generate lots of samples
    sams = np.random.rand(num_samples * 5, 2)
    # select positive samples
    num_pos = int(num_samples * pos_ratio)
    pos_sams = []
    for feat in sams:
        if feat[0] + feat[1] - (1+margin) > 0:
            pos_sams.append(feat)
            if len(pos_sams) >= num_pos:
                break
    pos_feats = np.stack(pos_sams, axis=0)
    pos_labels = np.ones((pos_feats.shape[0],))
    #print(pos_feats.shape, pos_labels.shape)

    # select negative samples
    num_neg = num_samples - num_pos
    neg_sams = []
    for feat in sams:
        if feat[0] + feat[1] - (1-margin) < 0:
            neg_sams.append(feat)
            if len(neg_sams) >= num_neg:
                break
    neg_feats = np.stack(neg_sams, axis=0)
    neg_labels = -np.ones((neg_feats.shape[0],))
    #print(neg_feats.shape, neg_labels.shape)
    feats, labels = np.concatenate([pos_feats, neg_feats], axis=0), \
        np.concatenate([pos_labels, neg_labels], axis=0)
    # shuffle
    if shuffle is True:
        shuffle_idx = np.arange(labels.shape[0])
        shuffle_rng = np.random.RandomState(123)
        shuffle_rng.shuffle(shuffle_idx)
        feats, labels = feats[shuffle_idx], labels[shuffle_idx]
    return feats, labels

def plot_samples(feats, labels):
    """可视化样本数据
    
    Args:
        feats (np.ndarray): 样本特征集合
        labels (np.ndarray): 样本标签集合

    Returns:
        None

    Raises:
        None
    """
    plt.figure()
    pos_feats = feats[labels==1, :]
    #print(pos_feats.shape)
    plt.scatter(pos_feats[:, 0], pos_feats[:, 1], c='green', marker='s')

    neg_feats = feats[labels==-1, :]
    #print(neg_feats.shape)
    plt.scatter(neg_feats[:, 0], neg_feats[:, 1], c='blue', marker='o')
    plt.show()


class Model:
    """用于建立感知机模型并提供参数训练接口
    """
    def __init__(self, feat_dim=2):
        self.feat_dim = feat_dim
        self.W = tf.Variable(tf.random.truncated_normal((self.feat_dim, 1)), name='features')
        self.b = tf.Variable(tf.random.truncated_normal((1,)), name='target')
        
    def __call__(self, x):
        """使得对象可以被函数式调用

        Args:
            x (np.ndarray): (1, 2), 样本数据

        Returns:
            Tensor, (1,), 感知机输出
        """
        return tf.sign(tf.matmul(x, self.W) + self.b)

    def loss(self, x, y):
        """用于计算损失函数

        Args:
            x (np.ndarray): (1,2), 样本特征
            y (np.ndarray): (1,), 样本标签

        Returns:
            Tensor, (1,) 损失函数值
        """
        l = -y * tf.matmul(x, self.W) + self.b
        return tf.reduce_sum(l)
    
    def train(self, x, y, lr):
        """根据当前样本训练模型

        Args:
            x (np.ndarray): (1,2), 样本特征
            y (np.ndarray): (1,), 样本标签
            lr (float): 学习率，数值范围(0,1)

        Returns:
            Tensor, W, (2, 1)模型权重参数
            Tensor, b, (1, )模型的偏移量参数
        """
        error = y - self(x)
        # compute derivate of params
        dW = tf.reduce_mean(tf.constant(x*error), axis=0)
        db = tf.reduce_mean(error, axis=0)
        dW = tf.reshape(dW, shape=(2, 1))
        db = tf.reshape(db, shape=(1,))
        # update params
        self.W.assign_sub(-dW*lr)
        self.b.assign_sub(-db*lr)
        return error, self.W, self.b

    def train_model(self, feats, labels, epochs=100, plot=True, skip_right=True):
        """训练一个感知机模型，并记录每一步优化的状态

        Args:
            feats (np.ndarray): (num_samples, 2), 样本的二维特征
            labels (np.ndarray): (num_samples,), 样本的标签，取值{-1, 1}
            epochs (int): 默认值=10，数据集循环使用次数
            plot (bool): 默认值=True，是否绘制结果图像
            skip_right (bool): 默认值=True，是否跳过已经预测正确的样本

        Returns:
            list, 返回每一步优化的状态

        Raises:
            ValueError: 传入的样本数据不符合要求
        """
        #model = Model()
        feats = feats.astype(dtype=np.float32)
        # train model
        train_states = []
        iter_count = 0
        for epoch in range(epochs):
            for x, y in zip(feats, labels):
                x = x.reshape((1, self.feat_dim))
                y = np.array(y, dtype=np.float32)
                y = y.reshape((1,))
                if skip_right is True and (y * self(x)).numpy() > 0:
                    continue
                e, W, b = self.train(x, y, 1e-3)
                loss = self.loss(x, y)
                e, W, b, loss = e.numpy(), W.numpy(), b.numpy(), loss.numpy()
                iter_count += 1
                train_states.append({'epoch':epoch, 'iter':iter_count, 'loss':loss,
                    'x':x.squeeze().tolist(), 'y':y.tolist(), 'e':e.tolist(), 
                    'W':W.squeeze().tolist(), 'b':b.squeeze()})
                print('epoch={}, iter={}, loss={}, x={}, y={}, e={}, W={}, b={}'\
                    .format(epoch, iter_count, loss, x.squeeze(), y, e.squeeze(),\
                        W.squeeze(), b.squeeze()))
        if plot is True:
            x0 = 0.0
            y0 = (-b-W[0]*x0)/W[1]
            x1 = 1.0
            y1 = (-b-W[0]*x1)/W[1]
            plt.plot([x0, x1], [y0, y1], '-')
            pos_feats = feats[labels==1, :]
            plt.scatter(pos_feats[:, 0], pos_feats[:, 1], c='green', marker='s')
            neg_feats = feats[labels==-1, :]
            plt.scatter(neg_feats[:, 0], neg_feats[:, 1], c='blue', marker='o')
            plt.axis([0,1,0,1])
            plt.show()
        return train_states

class StateTape(object):
    """用于管理数据的状态
    """
    
    def __init__(self, buff_dir='output/buff/thinking/perceptron'):
        self._buff_dir = buff_dir
        self._model = Model()
        self._is_init = True
        self._feats, self._labels = None, None
        if not os.path.exists(self._buff_dir):
            os.makedirs(self._buff_dir)

    def get_init_param(self):
        if not self._is_init:
            return None, None
        return self._model.W.numpy(), self._model.b.numpy()

    def get_samples(self, num_samples=100):
        if self._feats is None or self._labels is None:
            filepath = os.path.join(self._buff_dir, 'samples_data.pkl')
            if not os.path.exists(filepath):
                self._feats, self._labels = gen_data(num_samples=num_samples)
                with open(filepath, 'wb') as fid:
                    pickle.dump([self._feats, self._labels], fid)
            else:
                with open(filepath, 'rb') as fid:
                    tmp = pickle.load(fid)
                    self._feats, self._labels = tmp[0], tmp[1]
        return self._feats, self._labels

    def get_train_states(self, retrain=False):
        filepath = os.path.join(self._buff_dir, 'train_state.pkl')
        if (not os.path.exists(filepath)) or retrain is True:
            self._is_init = False
            feats, labels = self.get_samples()
            train_states = self._model.train_model(feats, labels, plot=False)
            with open(filepath, 'wb') as fid:
                pickle.dump(train_states, fid)
        else:
            with open(filepath, 'rb') as fid:
                train_states = pickle.load(fid)
        return train_states


class PosObj(Square):
    """ 用于标示正样本
    """
    
    def __init__(self, *args, **kwargs):
        self.side_length = 0.1
        self.color = GREEN
        self.fill_opacity = 1.0 
        super().__init__(*args, **kwargs)

class NegObj(Dot):
    """用于表示负样本
    """

    def __init__(self, *args, **kwargs):
        self.color = BLUE
        super().__init__(*args, **kwargs)

class ClassifierLine(Line):
    """用于表示分类直线，即分类超平面

    笔记记录： 
        继承manim提供的对象时，如果需要改变一些属性，需要在super().__init__()调用之前进行设置
    """

    def __init__(self, *args, **kwargs):
        self.color = PINK
        self.buff = 10
        super().__init__(*args, **kwargs)

def convert_geometry_to_params(point, degree):
    """将直线的几何信息转换为参数信息

    Args:
        point (list), 1x2, 直线经过的点的坐标[x1, x2]
        degree (float), 直线相对于横轴旋转的角度

    Returns:
        float, 参数 w1
        float, 参数 w2
        float, 参数 b
    """
    if degree >= 180:
        degree %= 180
    if degree > 90:
        degree -= 180
    if degree < -180:
        degree += (-degree) // 180 * 180
    if degree < -90:
        degree += 180
    if degree == 90 or degree == -90:
        return 1, 0, -point[0]
    # 计算斜率
    k = math.tan(degree/180*math.pi)
    if k < 0:
        return -k, 1, k*point[0] - point[1]
    return k, -1, -k*point[0] + point[1]

def convert_params_to_geometry(w1, w2, b):
    """将直线的参数信息转换为几何信息

    Args:
        w1 (float): 参数 w1
        w2 (float): 参数 w2
        b  (float): 参数 b

    Returns:
        list, 1x2, 直线与y=x直线的交点
        float，直线相对于横轴的旋转角度
    """
    if abs(w2) < 1e-5:
        x1 = -w1/b
        return [x1, x1], 90
    x1 = - b / (w1 + w2)
    # 计算角度
    degree = math.atan(-w1/w2)/math.pi*180
    return [x1, x1], degree

class Perceptron(GraphScene):
    """用于生成感知机算法讲解动画

    笔记记录1: 局部修改latex文本字体
        局部修改英文字体需要使用fontspec宏包，\\usepackage{fontspec}
        (1). 需要先将宏包加载的代码加到manimlib的ctex_template.tex文件
        (2). 使用实例：{\\setmainfont{BrushScriptStd} Hello}
        (3). 局部修改中文字体实例：{\\CJKfontspec{STKaitiSC-Regular} 你好}
    """
    CONFIG = {
        "x_min": -0.2,
        "x_max":  1.2,
        "x_axis_width": 6.0,
        "x_tick_frequency": 0.1,
        "x_labeled_nums": [0, 1],
        "x_axis_label": "$x_1$",
        "y_min": -0.2,
        "y_max":  1.2,
        "y_axis_height": 6.0,
        "y_tick_frequency": 0.1,
        "y_labeled_nums": [0, 1],
        "y_axis_label": "$x_2$",
        "graph_origin": 2.5*DOWN + 5.5*LEFT,
        "exclude_zero_label": True,
    }
    
    def construct(self):
        # 创建坐标轴
        self.setup_axes(animate=True)
        # 获取数据
        st = StateTape()
        # init_W, init_b = st.get_init_param()
        feats, labels = st.get_samples()

        # 创建正样本
        pos_mark = PosObj()
        pos_mark.move_to(self.coords_to_point(1.0, 1.2))
        self.play(Write(pos_mark))
        pos_anno = TextMobject(r'正样本', r'$y=+1$')
        pos_anno.move_to(self.coords_to_point(1.3, 1.2))
        pos_anno.scale(0.5)
        self.play(ShowCreation(pos_anno))
        self.wait()

        pos_samples = []
        pos_feats = feats[labels==1]
        for r in pos_feats:
            p = PosObj()
            p.move_to(self.coords_to_point(r[0], r[1]))
            pos_samples.append(p)
        self.play(*[ReplacementTransform(pos_mark.copy(), p) for p in pos_samples], run_time=3)
        self.wait(1)

        # 创建负样本
        neg_mark = NegObj()
        neg_mark.move_to(self.coords_to_point(1.0, -0.2))
        self.play(Write(neg_mark))
        neg_anno = TextMobject(r'负样本', r'$y=-1$')
        neg_anno.move_to(self.coords_to_point(1.3, -0.2))
        neg_anno.scale(0.5)
        self.play(ShowCreation(neg_anno))
        self.wait(1)

        neg_samples = []
        neg_feats = feats[labels==-1]
        for r in neg_feats:
            n = NegObj()
            n.move_to(self.coords_to_point(r[0], r[1]))
            neg_samples.append(n)
        self.play(*[ReplacementTransform(neg_mark.copy(), n) for n in neg_samples], run_time=3)
        self.wait(1)

        # 说明样本表示
        ppx1, ppx2 = 1.0, 1.0
        for p in pos_samples:
            x1, x2 = self.point_to_coords(p.get_center())
            if x2 < ppx2:
                ppx1, ppx2 = x1, x2
        pp = PosObj()
        pp.set_color(RED)
        pp.move_to(self.coords_to_point(ppx1, ppx2))
        self.play(ShowCreation(pp))
        self.wait()

        pp_coor = TextMobject(r'({:0.2f}, {:0.2f})'.format(ppx1, ppx2))
        pp_coor.set_color(RED)
        pp_coor.move_to(self.coords_to_point(ppx1+0.2, ppx2+0.1))
        pp_coor.scale(0.5)
        self.play(ShowCreation(pp_coor))
        self.wait()

        # x的向量形式
        x_form = TexMobject(r'{\bf{x}}=[x_1, x_2]^T')
        x_form.move_to(3.5*RIGHT+1.5*UP)
        x_form.set_color(RED)
        pp_group = VGroup(pp, pp_coor)
        self.play(ReplacementTransform(pp_group.copy(), x_form), run_time=2)
        self.wait()

        # 样本数据的向量形式
        sam_form = TextMobject(r'$\{{\bf{x}}, y\}$', r', 构成一个样本')
        sam_form.move_to(x_form)
        sam_form.shift(DOWN)
        self.play(ReplacementTransform(x_form.copy(), sam_form), run_time=2)
        self.play(FadeOutAndShift(x_form), FadeOutAndShift(sam_form))
        self.play(FadeOut(pp_group))
        self.wait()

        # 创建一个可分的超平面
        l = ClassifierLine()
        l.move_to(self.coords_to_point(0.5, 0.5))
        l.rotate(DEGREES*135)
        l.set_length(8)
        self.play(Write(l), run_time=2)
        self.wait()
        
        # 超平面的方程
        l_form = TexMobject(r'f(x_1, x_2)=w_1x_1+w_2x_2+b', r'=0')
        l_form.move_to(3.5*RIGHT+0.5*DOWN)
        l_form.set_color(PINK)
        l_form.scale(0.7)
        self.play(ReplacementTransform(l.copy(), l_form), run_time=2)
        self.wait()

        # 向量形式的直线方程
        l_form2 = TexMobject(r'f({\bf{x}})=', r'{\bf{w}}',r'{\bf{x}}+ b', r'=0')
        l_form2.move_to(3.5*RIGHT+2.0*DOWN)
        #darrow = DoubleArrow(begin=l_form, end=l_form2)
        #ßself.play(Write(darrow))
        self.play(ReplacementTransform(l_form, l_form2), run_time=2)
        self.play(l_form2.shift, 3*UP, run_time=2)
        self.play(l_form2[1].set_color, YELLOW, run_time=2)
        self.wait()
        # 参数w的向量形式
        w_form = TexMobject(r'{\bf{w}}=[w_1, w_2]')
        w_form.set_color(YELLOW)
        w_form.move_to(l_form2)
        w_form.shift(1.5*DOWN)
        self.play(ReplacementTransform(l_form2[1].copy(), w_form), run_time=2)
        self.play(FadeOutAndShift(w_form))
        self.wait()

        # 标记正样本特点
        arrow = Arrow()
        arrow.move_to(l.get_center()+0.55*RIGHT+0.55*UP)
        arrow.rotate(45*DEGREES)
        self.play(Write(arrow))
        self.wait()
        
        pos_form = TexMobject(r'f({\bf{x}})', r'>0')
        pos_form.move_to(1.5*LEFT)
        self.play(ReplacementTransform(arrow.copy(), pos_form))
        self.play(pos_form.set_color, RED, run_time=2)
        self.wait()
        self.play(FadeOutAndShift(pos_form))
        self.wait()

        # 标记负样本特点
        self.play(arrow.rotate, 180*DEGREES)
        self.play(arrow.move_to, l.get_center()-0.55*RIGHT-0.55*UP)
        neg_form = TexMobject(r'f({\bf{x}})', r'<0')
        neg_form.move_to(3.5*LEFT+2*DOWN)
        self.play(ReplacementTransform(arrow.copy(), neg_form))
        self.play(neg_form.set_color, RED, run_time=2)
        self.wait()
        self.play(FadeOutAndShift(neg_form))
        self.wait()

        # 感知机模型
        self.play(arrow.rotate, 145*DEGREES)
        self.play(arrow.move_to, l_form2.get_center()+DOWN+LEFT)
        self.play(FadeOut(arrow), run_time=0.5)
        self.wait()
        self.play(FocusOn(l_form2))
        m = TexMobject(r'f({\bf{x}})=', r'sign', r'({\bf{w}}',r'{\bf{x}}+ b)')
        m.move_to(l_form2)
        self.play(ReplacementTransform(l_form2, m))
        self.wait()

        # 符号函数的表达式
        sign_form = TexMobject(r'sign(x) =\begin{cases}+1&, x \geq 0\\-1&, x < 0 \end{cases}')
        sign_form.move_to(m)
        sign_form.shift(1.5*DOWN)
        self.play(ReplacementTransform(m[1].copy(), sign_form), run_time=2)
        self.play(sign_form.set_color, YELLOW, run_time=2)
        self.wait()
        self.play(FadeOutAndShiftDown(sign_form), run_time=2)
        self.wait()
        
        # # 标记误分类点
        self.play(l.rotate, DEGREES*35, run_time=2)
        self.wait()
        #self.wait()
        w1, w2, b = convert_geometry_to_params([0.5, 0.5], 170)
        marks, pph, ppl = [], [0,0], [1.0,1.0]
        for f, label in zip(feats, labels):
            if (w1*f[0]+w2*f[1]+b) * label < 0:
                t = TextMobject(r'*')
                t.move_to(self.coords_to_point(f[0], f[1]))
                #t.set_opacity(50)
                t.scale(0.5)
                t.set_color(RED)
                marks.append(t)
                # record high point
                if f[1] > pph[1]:
                    pph = f
                # record low point
                if f[1] < ppl[1]:
                    ppl = f
        self.play(*[ShowCreation(m) for m in marks])
        self.wait(2)
        
        # # 加入误分类标注
        v1 = Arrow(start=self.coords_to_point(0.5, 1.2), 
                   end=self.coords_to_point(*ppl), color=RED)
        v2 = Arrow(start=self.coords_to_point(0.5, 1.2),
                   end=self.coords_to_point(*pph), color=RED)
        self.play(Write(v1), Write(v2), run_time=2)
        t = TextMobject(r'误分类点集 ', r'M')
        t.move_to(self.coords_to_point(0.5, 1.3))
        t.scale(0.7)
        self.play(FadeIn(t))
        self.play(t[1].set_color, YELLOW)
        self.wait()
        
        # 移除标注
        self.play(FadeOut(t[0]), FadeOut(v1), FadeOut(v2))
        self.wait()

        # 损失函数
        loss_form = TexMobject(r'L({\bf{w}}, b)=-\sum_{{\bf{x}_i} \in M}y_i({\bf{w}}{\bf{x}}_i+b)')
        loss_form.move_to(m)
        loss_form.shift(1.5*DOWN)
        self.play(ReplacementTransform(t[1], loss_form)) 
        self.wait()

        # 梯度
        grad_form = TexMobject(
            r'&\nabla_{{\bf{w}}}L({\bf{w}}, b)=-\sum_{{\bf{x}}_i \in M} y_i{\bf{x}}_i^T\\',
            r'&\nabla_bL({\bf{w}}, b)=-\sum_{{\bf{x}}_i \in M} y_i\\')
        grad_form.move_to(loss_form)
        grad_form.shift(DOWN)
        grad_form.scale(0.7)
        self.play(ReplacementTransform(loss_form, grad_form))
        self.wait()

        # 随机梯度下降迭代
        iter_form = TexMobject(
            r'&{\bf{w}} \leftarrow {\bf{w}} + ', r'\eta', r' y_i{\bf{x}}_i^T\\',
            r'&b \leftarrow b + ', r'\eta', r' y_i')
        iter_form.move_to(grad_form)
        # iter_form.scale(0.7)
        self.play(ReplacementTransform(grad_form, iter_form))
        self.play(iter_form[1].set_color, YELLOW)
        self.play(iter_form[4].set_color, YELLOW)
        self.wait()

        # 学习率
        eta_text = TextMobject(r'$\eta$是学习率')
        eta_text.scale(0.7)
        eta_text.move_to(iter_form)
        eta_text.shift(DOWN)
        self.play(ReplacementTransform(iter_form[1].copy(), eta_text))
        self.play(eta_text.set_color, YELLOW)
        self.wait()
        self.play(FadeOutAndShiftDown(eta_text))

        # 绘制迭代过程
        train_states = st.get_train_states()
        chosen_point = train_states[0]['x']
        tri = Triangle()
        tri.move_to(self.coords_to_point(*chosen_point))
        tri.scale(0.2)
        tri.set_color(RED)
        self.play(Write(tri))
        self.wait()

        # 迭代信息
        info = TextMobject(r'开始迭代训练优化参数')
        info_pos = self.coords_to_point(0.5, -0.2)
        info.scale(0.5)
        info.move_to(info_pos)
        self.play(Write(info))
        self.wait()
        #return
        for idx,ts in enumerate(train_states[1:]):
            if idx < 382:
                continue
            # 标记选中的误分类点
            chosen_point = ts['x']
            new_tri = Triangle()
            new_tri.move_to(self.coords_to_point(*chosen_point))
            new_tri.scale(0.2)
            new_tri.set_color(RED)
            self.play(ReplacementTransform(tri, new_tri), run_time=0.5)
            tri = new_tri
            # 显示当前迭代信息
            W, b = ts['W'], ts['b']
            point, degree = convert_params_to_geometry(*W, b)
            if point[0] < -0.2 and point[1] < -0.2:
                new_info = TextMobject(r'第{}次迭代，分类直线超出范围'.format(idx+1))
            else:
                new_info = TextMobject(r'第{}次迭代'.format(idx+1))
            new_info.scale(0.5)
            new_info.move_to(info_pos)
            self.play(ReplacementTransform(info, new_info), run_time=0.5)
            info = new_info
            # 画分类超平面
            new_l = ClassifierLine()
            new_l.set_length(8)
            new_l.move_to(self.coords_to_point(*point))
            new_l.rotate(degree*DEGREES)
            self.play(ReplacementTransform(l, new_l), run_time=0.5)
            l = new_l
            # 重新设置误分类点集
            self.remove(*marks)
            marks= []
            for f, label in zip(feats, labels):
                if (W[0]*f[0]+W[1]*f[1]+b) * label < 0:
                    t = TextMobject(r'*')
                    t.move_to(self.coords_to_point(f[0], f[1]))
                    #t.set_opacity(50)
                    t.scale(0.5)
                    t.set_color(RED)
                    marks.append(t)
            self.play(*[ShowCreation(m) for m in marks], run_time=0.5)
            

def fig2ndarray(format='png', transparent=True, dpi=200):
    buff = io.BytesIO()
    plt.savefig(buff, format=format, transparent=transparent, dpi=dpi)
    img = np.asarray(PIL.Image.open(buff))
    buff.close()
    return img

from mpl_toolkits.mplot3d import Axes3D
class PerceptronParamSpace(ThreeDScene):
    """用于可视化感知机参数变换的过程，以(w1, w2)为自变量，以损失函数为因变量的三维图
    """

    def construct(self):
        # 获取数据
        st = StateTape()
        train_states = st.get_train_states()

        W, b = train_states[0]['W'], train_states[0]['b']
        x, y = train_states[0]['x'], train_states[0]['y']
        p = [W[0], W[1], -y[0]*(W[0]*x[0]+W[1]*x[1]+b)]

        # 迭代信息
        info = TextMobject(r'开始迭代训练优化参数')
        info_pos = 3*DOWN + 5*LEFT
        info.scale(0.5)
        info.move_to(info_pos)
        self.play(Write(info))
        self.wait()

        img_obj = None
        for idx, ts in enumerate(train_states[1:]):
            # if idx < 382:
            #     continue
            W, b = ts['W'], ts['b']
            x, y = ts['x'], ts['y']
            p = [p[0], p[1], -y[0]*(p[0]*x[0]+p[1]*x[1]+b)]
            new_p = [W[0], W[1], -y[0]*(W[0]*x[0]+W[1]*x[1]+b)]
            min_w0 = min(p[0], new_p[0])
            max_w0 = max(p[0], new_p[0])
            min_w1 = min(p[1], new_p[1])
            max_w1 = max(p[1], new_p[1])
            print(min_w0, max_w0, min_w1, min_w1)
            # 绘制3d图
            plt.clf()
            plt.close()
            fig = plt.figure(figsize=(9.6, 5.4))
            ax = fig.gca(projection='3d')
            # X = np.linspace(-0.2, 3.0, 100)
            # Y = np.linspace(-0.2, 3.0, 100)
            X = np.linspace(min_w0-0.05, max_w0+0.05, 100)
            Y = np.linspace(min_w1-0.05, max_w1+0.05, 100)
            XX, YY = np.meshgrid(X, Y)
            Z = -y[0] * (x[0]*XX + x[1]*YY + b)
            ax.plot_surface(XX, YY, Z, alpha=0.5)
            print(p, new_p)
            ax.scatter3D([p[0], new_p[0]], [p[1], new_p[1]], [p[2], new_p[2]], 'o', color='red', lw=7)
            ax.quiver([p[0]], [p[1]], [p[2]], [new_p[0]-p[0]], [new_p[1]-p[1]], [new_p[2]-p[2]], color='yellow')
            p = new_p
            # 修改坐标轴
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.zaxis.label.set_color('white')
            ax.tick_params(axis='x',colors='white')
            ax.tick_params(axis='y',colors='white')
            ax.tick_params(axis='z',colors='white')
            #plt.show()
            # convert figure to array
            img = fig2ndarray()
            #print(img.shape)
            if img_obj is None:
                img_obj = ImageMobject(img)
                img_obj.scale(4)
                self.add(img_obj)
            else:
                new_img_obj = ImageMobject(img)
                new_img_obj.scale(4)
                self.play(ReplacementTransform(img_obj, new_img_obj))
                img_obj = new_img_obj
            # 打印迭代次数信息
            new_info = TextMobject(r'第{}次迭代'.format(idx+1))
            new_info.scale(0.5)
            new_info.move_to(info_pos)
            self.play(ReplacementTransform(info, new_info), run_time=0.5)
            info = new_info

        # # 添加3d坐标轴
        # self.set_camera_orientation(phi=80 * DEGREES,theta=-60*DEGREES)
        # axis_config = {'unit_size':4, 'tick_size':0.1, 
        #                'tick_frequency':0.2, 
        #                'numbers_with_elongated_ticks':[0,1]}
        # axes = ThreeDAxes(
        #     x_min=-0.2, x_max=2.0,y_min=-0.2, y_max=2.0, 
        #     z_min=-0.2, z_max=2.0, num_axis_pieces=20, 
        #     x_axis_config=axis_config,
        #     y_axis_config=axis_config,
        #     z_axis_config=axis_config)
        # #axes.scale(3)
        # #axes.move_to(3*LEFT+2*DOWN)
        # self.play(Write(axes))
        # self.wait()

        # # 获取数据
        # st = StateTape()
        # train_states = st.get_train_states()

        # # 绘制初始损失图
        # W, b = train_states[0]['W'], train_states[0]['b']
        # x, y = train_states[0]['x'], train_states[0]['y']
        # loss_func = lambda WW,bb,xx,yy : -yy[0]*(WW[0]*xx[0] + WW[1]*xx[1] + bb) 
        # ps = ParametricSurface(
        #     lambda u, v: np.array([u, v, loss_func([u,v], b, x, y)]), # 
        #     u_min=-0.2, u_max=2.0, v_min=-0.2, v_max=2.0,
        #     checkerboard_colors=[BLUE_D, BLUE_E]).scale(2)
        # ps.move_to(axes.c2p(0,0,0))
        # self.play(Write(ps))
        # # 绘制当前参数点
        # d = Sphere()
        # d.scale(0.2)
        # d.move_to(axes.c2p(W[0], W[1], loss_func(W, b, x, y)))
        # d.set_color(RED)
        # self.play(Write(d))
        # self.begin_ambient_camera_rotation(rate=0.1) 
        # self.wait()

def main():
    """用于测试本文件所提供的工具函数运行状况
    """
    #feats, labels = gen_data(num_samples=100)
    #plot_samples(feats, labels)
    #model = Model()
    #states = model.train_model(feats, labels)
    #print(states[-1])

    st = StateTape()
    train_states = st.get_train_states()
    st.get_samples()


if __name__ == '__main__':
    main()
