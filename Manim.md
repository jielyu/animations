# Manim使用总结

## 源码改动

### 1. Tex模版

将constants.py中的`TEX_USE_CTEX = False` 改为 `TEX_USE_CTEX = True`以支持中文

### 2. 帧速率

将constants.py中的

```python
PRODUCTION_QUALITY_CAMERA_CONFIG = {
    "pixel_height": 1440,
    "pixel_width": 2560,
    "frame_rate": 60,
}

HIGH_QUALITY_CAMERA_CONFIG = {
    "pixel_height": 1080,
    "pixel_width": 1920,
    "frame_rate": 60,
}
```

修改为：

```python
PRODUCTION_QUALITY_CAMERA_CONFIG = {
    "pixel_height": 2160,
    "pixel_width": 3840,
    "frame_rate": 30,
}

HIGH_QUALITY_CAMERA_CONFIG = {
    "pixel_height": 1080,
    "pixel_width": 1920,
    "frame_rate": 30,
}
```

默认4k画质30fps
以保证--high_quality参数下输出的帧速率为30fps，后续可能会在命令行参数中加入fps

### 3. 输出目录

将constants.py中`MEDIA_DIR = "./media"` 修改为 `MEDIA_DIR = "./output"` 以避免每次传入命令行参数修改该变量

### 4. 进度条

将 `--leave_progress_bars` 改为 `--remove_progress_bars`， 使得默认情况下的进度条是逐行保留的。该修改涉及以下几个文件：

```shell
config.py
extract_scene.py
scene/scene.py
```

### 5. 修复ComplexPlane实现中的bug

```shell
mobject/coordinate_systems.py:171
```

原始代码：

```python
    def coords_to_point(self, *coords):
        origin = self.x_axis.number_to_point(0)
        result = np.array(origin)
        for axis, coord in zip(self.get_axes(), coords):
            result += (axis.number_to_point(coord) - origin)
        return result
```

修改为：

```python
    def coords_to_point(self, *coords):
        origin = self.x_axis.number_to_point(0)
        result = np.array(origin)
        # TODO: @jielyu fix bug, wrong axis assign
        dim = 0
        for axis, coord in zip(self.get_axes(), coords):
            mid = axis.number_to_point(coord) - origin
            if dim == 0:
                result += mid
            else:
                mid[dim] = mid[0]
                mid[0] = origin[0]
                result += mid
            dim += 1
        return result
```

## 场景 Scene

所有Scene都是Container的派生类，必须实现两个方法：add和remove。

### 1. Scene

声明原型：
`class Scene(Container)`

默认的CONFIG配置如下：

```python
CONFIG = {
    "camera_class": Camera,
    "camera_config": {},
    "file_writer_config": {},
    "skip_animations": False,
    "always_update_mobjects": False,
    "random_seed": 0,
    "start_at_animation_number": None,
    "end_at_animation_number": None,
    "leave_progress_bars": False,
}
```

提供的函数接口如下：

```python
def __init__(self, **kwargs):
    """ Construct Scene object
    Note: kwargs 传入的参数将会覆盖默认的CONFIG参数，并最终转换为对象成员
    """

def setup(self):
    """ 用于子类对象需要在构造之前调用的功能
    Return: None
    """

def tear_down(self):
    """ 用于子类对象在构造完成之后需要调用的功能
    Return: None
    """

def construct(self):
   """ 用于构造当前场景下动画，在构造函数中调用
   Return: None
   """

def __str__(self):
    """ 重定义对象输出形式
    Return: str
    """

def print_end_message(self):
    """ 打印动画完成后的信息
    Return: None
    """

def set_variables_as_attrs(self, *objects, **newly_named_objects):
   """ 设置对象成员
   Note： 行为诡异，不建议使用
   Return: None
   """

def get_attrs(self, *keys):
    """ 获取对象成员
    Return: list
    """

def set_camera(self, camera):
    """ 设置当前场景的摄像机
    Note： 唯一修改摄像机的接口
    Return: None
    """

def get_frame(self):
    """ 获取摄像机中的当前帧
    Return: numpy.ndarray
    """

def get_image(self):
    """ 获取摄像机中的当前图像
    Return: PIL.Image
    """

def set_camera_pixel_array(self, pixel_array):
    """ 设置摄像机中的当前画面
    Return: None
    """

def set_camera_background(self, background):
    """ 设置摄像机的背景图像
    Return: None
    """

def reset_camera(self):
    """ 重置摄像机
    Return: None
    """

def capture_mobjects_in_camera(self, mobjects, **kwargs):
    """ 捕获当前摄像机下的对象
    Return: None
    """

def update_frame(
            self,
            mobjects=None,
            background=None,
            include_submobjects=True,
            ignore_skipping=True,
            **kwargs):
    """ 更新当前帧
    Return: None
    """

def freeze_background(self):
    """ 固定背景
    Return: None
    """

def update_mobjects(self, dt):
    """ 在时间轴上更新对象状态
    Return: None
    """

def should_update_mobjects(self):
    """ 询问是否应当更新对象状态
    Return: boolean
    """

def get_time(self):
    """ 获取当前场景下的时间
    Return: None
    """

def increment_time(self, d_time):
    """ 当前场景下时间正向流动一个dt
    Return: None
    """

def get_top_level_mobjects(self):
    """ 返回不在其他对象族系中的对象
    Return: list
    """

def get_mobject_family_members(self):
    """ 获取当前场景下对象的族系
    Return: list
    """

def add(self, *mobjects):
    """ 向场景中增加对象
    Note: 只是增加对象，没有动画效果
    Return: self
    """

def add_mobjects_among(self, values):
    """ 用于快速增加大量对象，比如由一些点定义的对象
    Return: self 
    """

def remove(self, *mobjects):
    """ 移除对象
    Return: self 
    """

def restructure_mobjects(self, to_remove,
                             mobject_list_name="mobjects",
                             extract_families=True):
    """ 移除一个对象
    Note: 被remove函数调用
    Return: self 
    """

def get_restructured_mobject_list(self, mobjects, to_remove):
    """ 获取删除元素的列表
    Return: list
    """

""" 加入和移除前景对象的系列函数
Return: self 
"""
def add_foreground_mobjects(self, *mobjects):

def add_foreground_mobject(self, mobject):

def remove_foreground_mobjects(self, *to_remove):

def remove_foreground_mobject(self, mobject):

def bring_to_front(self, *mobjects):

def bring_to_back(self, *mobjects):

def clear(self):
    """ 清楚所有元素
    Return: self 
    """

def get_mobjects(self):
    """ 获取当前场景的所有对象
    Return: self 
    """

def get_mobject_copies(self):
    """ 获取当前场景的所有对象的拷贝
    Return: self 
    """

def get_moving_mobjects(self, *animations):
    """ 获取正在移动的对象，这些对象需要更新状态参数
    Return: list
    """

def get_time_progression(self, run_time, n_iterations=None, override_skip_animations=False):
    """ 获取进度条
    Return: ProgressDisplay
    """

def get_run_time(self, animations):
    """ 获取运行时间，即所有动画最大的运行时间
    Return: float
    """

def get_animation_time_progression(self, animations):
    """ 获取指定动画的运行进度条
    Return: ProgressDisplay
    """

def compile_play_args_to_animation_list(self, *args, **kwargs):
    """ 将参数写入到动画
    Return: list
    """

def update_skipping_status(self):
    """ 更新跳过状态
    """

def handle_play_like_call(func):
    """ 用于修饰play函数的修饰期
    Return: wrapper函数
    """

def begin_animations(self, animations):
    """ 开始动画
    Return: None
    """

def progress_through_animations(self, animations):
    """ 渲染动画
    Return: None
    """

def finish_animations(self, animations):
    """ 动画结束
    Return: None
    """

@handle_play_like_call
def play(self, *args, **kwargs):
    """ 添加动画
    Note: 实现调用顺序 begin_animations -> progress_through_animations -> finish_animations
    Return: None
    """

def idle_stream(self):
    """ 用于及时显示，一般在交互环境中使用
    Return: None
    """

def clean_up_animations(self, *animations):
    """ 清除动画
    Return: self
    """

def get_mobjects_from_last_animation(self):
    """ 获取上一个动画的对象
    Return: list
    """

def get_wait_time_progression(self, duration, stop_condition):
    """ 获取等待进度条
    Return: ProgressDisplay
    """

@handle_play_like_call
def wait(self, duration=DEFAULT_WAIT_TIME, stop_condition=None):
    """ 等待
    Return: self
    """

def wait_until(self, stop_condition, max_time=60):
    """ 等待到条件满足
    Return: None
    """

def force_skipping(self):
    """ 跳过
    Return: self
    """

def revert_to_original_skipping_status(self):
    """ 反转原先的跳转状态
    Return: self
    """

def add_frames(self, *frames):
    """ 向写入器添加一帧
    Return: None
    """

def add_sound(self, sound_file, time_offset=0, gain=None, **kwargs):
    """ 写入声音
    Return: None
    """

def show_frame(self):
    """ 展现一帧图像
    Return: None
    """

def tex(self, latex):
    """ 用于tex文本，一般用于交互式环境
    """

```

该类所提供的函数签名如下

### 2. GraphScene

用于绘制二维坐标图

声明原型：
`class GraphScene(Scene):`

默认的CONFIG配置如下：

```python
CONFIG = {
    "x_min": -1,
    "x_max": 10,
    "x_axis_width": 9,
    "x_tick_frequency": 1,
    "x_leftmost_tick": None,  # Change if different from x_min
    "x_labeled_nums": None,
    "x_axis_label": "$x$",
    "y_min": -1,
    "y_max": 10,
    "y_axis_height": 6,
    "y_tick_frequency": 1,
    "y_bottom_tick": None,  # Change if different from y_min
    "y_labeled_nums": None,
    "y_axis_label": "$y$",
    "axes_color": GREY,
    "graph_origin": 2.5 * DOWN + 4 * LEFT,
    "exclude_zero_label": True,
    "default_graph_colors": [BLUE, GREEN, YELLOW],
    "default_derivative_color": GREEN,
    "default_input_color": YELLOW,
    "default_riemann_start_color": BLUE,
    "default_riemann_end_color": GREEN,
    "area_opacity": 0.8,
    "num_rects": 50,
}
```

提供的函数接口如下：

``` python

def setup(self):
    """ 用于初始化
    Return: None
    """

def setup_axes(self, animate=False):
    """ 创建坐标轴
    Return: None
    """

def coords_to_point(self, x, y):
    """ 将坐标转换为图像中的点
    Return: numpy.dnarray, 1x3
    """

def point_to_coords(self, point):
    """ 将图像中的点转换为坐标
    Return: tuple(x, y)
    """

def get_graph(self, func, color=None, x_min=None, x_max=None, **kwargs):
    """ 获取图像
    Return: ParametricFunction
    """

def input_to_graph_point(self, x, graph):
    """ 将参数化函数转换为图像上的点
    Return: numpy.dnarray, 1x3
    """

def angle_of_tangent(self, x, graph, dx=0.01):
    """ 坐标转换为角度
    Return: float
    """

def slope_of_tangent(self, *args, **kwargs):
    """ 角度转换为斜率
    Return: float
    """

def get_derivative_graph(self, graph, dx=0.01, **kwargs):
    """ 获取子图
    Return: ParametricFunction
    """

def get_graph_label(self, graph, label="f(x)", x_val=None,
        direction=RIGHT, buff=MED_SMALL_BUFF, color=None,):
    """ 获取图标签
    Return: TexMobject
    """

def get_riemann_rectangles(
        self, graph, x_min=None, x_max=None, dx=0.1, input_sample_type="left",
        stroke_width=1, stroke_color=BLACK, fill_opacity=1, start_color=None,
        end_color=None, show_signed_area=True, width_scale_factor=1.001):
    """ 获取黎曼矩形
    Return: VGroup()
    """

def get_riemann_rectangles_list(
        self, graph, n_iterations, max_dx=0.5, power_base=2, stroke_width=1, **kwargs):
    """ 获取黎曼矩形
    Return: list
    """

def get_area(self, graph, t_min, t_max):
    """ 获取图，并填充指定时间内的区域
    Return: VGroup()
    """

def transform_between_riemann_rects(self, curr_rects, new_rects, **kwargs):
    """ 在黎曼矩形间运用变换动画
    Return: None
    """

def get_vertical_line_to_graph(self, x, graph, line_class=Line, **line_kwargs):
    """ 获取纵轴图
    Return: line_class
    """

def get_vertical_lines_to_graph(
        self, graph, x_min=None, x_max=None, num_lines=20, **kwargs):
    """ 获取黎曼矩形
    Return: VGroup()
    """

def get_secant_slope_group(
        self, x, graph, dx=None, dx_line_color=None, df_line_color=None,
        dx_label=None, df_label=None, include_secant_line=True,
        secant_line_color=None, secant_line_length=10,):
    """ 获取切割线
    Return: VGroup()
    """

def add_T_label(self, x_val, side=RIGHT, label=None, color=WHITE, animated=False, **kwargs):
    """ 加入标注轴
    Return: None
    """

def get_animation_integral_bounds_change(
        self, graph, new_t_min, new_t_max, fade_close_to_origin=True, run_time=1.0):
""" 获取动画积分边界的变化
Return: UpdateFromAlphaFunc
"""

def animate_secant_slope_group_change(
        self, secant_slope_group, target_dx=None, target_x=None,
        run_time=3, added_anims=None, **anim_kwargs):
""" 获取动画切割线的变化
Return: None
"""
```

### 3. MovingCameraScene

用于可以移动摄像机的场景

声明原型：
`class MovingCameraScene(Scene):`

默认的CONFIG配置如下：

```python
CONFIG = {
    "camera_class": MovingCamera
}
```

### 4. SampleSpaceScene

用于展现概率空间

声明原型：
`class SampleSpaceScene(Scene):`


### 5. SceneFileWriter

用于场景渲染文件写入器

声明原型：
`class SceneFileWriter(object):`

默认的CONFIG配置如下：

```python
CONFIG = {
    "write_to_movie": False,
    # TODO, save_pngs is doing nothing
    "save_pngs": False,
    "png_mode": "RGBA",
    "save_last_frame": False,
    "movie_file_extension": ".mp4",
    "gif_file_extension": ".gif",
    "livestreaming": False,
    "to_twitch": False,
    "twitch_key": None,
    # Previous output_file_name
    # TODO, address this in extract_scene et. al.
    "file_name": None,
    "input_file_path": "",  # ??
    "output_directory": None,
}
```

### 6. ThreeDScene

用于绘制三维场景

***声明原型：***
`class ThreeDScene(Scene):`

默认的CONFIG配置如下：

```python
CONFIG = {
    "camera_class": ThreeDCamera,
    "ambient_camera_rotation": None,
    "default_angled_camera_orientation_kwargs": {
        "phi": 70 * DEGREES,
        "theta": -135 * DEGREES,
    }
}
```

***声明原型：***
`class SpecialThreeDScene(ThreeDScene):`

默认的CONFIG配置如下：

```python
CONFIG = {
    "cut_axes_at_radius": True,
    "camera_config": {
        "should_apply_shading": True,
        "exponential_projection": True,
    },
    "three_d_axes_config": {
        "num_axis_pieces": 1,
        "axis_config": {
            "unit_size": 2,
            "tick_frequency": 1,
            "numbers_with_elongated_ticks": [0, 1, 2],
            "stroke_width": 2,
        }
    },
    "sphere_config": {
        "radius": 2,
        "resolution": (24, 48),
    },
    "default_angled_camera_position": {
        "phi": 70 * DEGREES,
        "theta": -110 * DEGREES,
    },
    # When scene is extracted with -l flag, this
    # configuration will override the above configuration.
    "low_quality_config": {
        "camera_config": {
            "should_apply_shading": False,
        },
        "three_d_axes_config": {
            "num_axis_pieces": 1,
        },
        "sphere_config": {
            "resolution": (12, 24),
        }
    }
}
```

### 7. VectorScene, LinearTransformationScene

***原型声明：***
`class VectorScene(Scene):`

默认的CONFIG配置如下：

```python
CONFIG = {
    "basis_vector_stroke_width": 6
}
```

***声明原型：***
`class LinearTransformationScene(VectorScene):`

默认的CONFIG配置如下：

```python
CONFIG = {
    "include_background_plane": True,
    "include_foreground_plane": True,
    "foreground_plane_kwargs": {
        "x_max": FRAME_WIDTH / 2,
        "x_min": -FRAME_WIDTH / 2,
        "y_max": FRAME_WIDTH / 2,
        "y_min": -FRAME_WIDTH / 2,
        "faded_line_ratio": 0
    },
    "background_plane_kwargs": {
        "color": GREY,
        "axis_config": {
            "stroke_color": LIGHT_GREY,
        },
        "axis_config": {
            "color": GREY,
        },
        "background_line_style": {
            "stroke_color": GREY,
            "stroke_width": 1,
        },
    },
    "show_coordinates": False,
    "show_basis_vectors": True,
    "basis_vector_stroke_width": 6,
    "i_hat_color": X_COLOR,
    "j_hat_color": Y_COLOR,
    "leave_ghost_vectors": False,
    "t_matrix": [[3, 0], [1, 2]],
}
```

### 8. ZoomedScene

***声明原型：***
`class ZoomedScene(MovingCameraScene)`

默认的CONFIG配置如下

```python
CONFIG = {
    "camera_class": MultiCamera,
    "zoomed_display_height": 3,
    "zoomed_display_width": 3,
    "zoomed_display_center": None,
    "zoomed_display_corner": UP + RIGHT,
    "zoomed_display_corner_buff": DEFAULT_MOBJECT_TO_EDGE_BUFFER,
    "zoomed_camera_config": {
        "default_frame_stroke_width": 2,
        "background_opacity": 1,
    },
    "zoomed_camera_image_mobject_config": {},
    "zoomed_camera_frame_starting_position": ORIGIN,
    "zoom_factor": 0.15,
    "image_frame_stroke_width": 3,
    "zoom_activated": False,
}
```

## 目标 Mobject

### 1. Mobject

### 2. ImageMobject, ImageMobjectFromCamera

### 3. PMobject, Mobject1D, Mobject2D, PGroup, PointCloudDot, Point

### 4. VMobject, VGroup, VectorizedPoint, CurvesAsSubmobjects, DashedVMobject

### 5. SVGMobject, VMobjectFromSVGPathstring

### 6. TexMobject, TextMobject, BulletedList, TexMobjectFromPresetString, Title, Text

### 7. changing

### 8. frame

### 9. geometry

### 10. matirx

### 11. numbre_line

### 12. numbers

### 13. probability

### 14. shape_matchers

### 15. 3d

### 16. value_tracker

### 17. vector_field

## 动画 Animation

### 1. Animation

### 2. composition

### 3. creation

### 4. fading

### 5. growing

### 6. indication

### 7. movement

### 8. numbers

### 9. rotation

### 10. specialized

### 11. tramsform

### 12. update

## 相机 Camera

### 1. Camera

声明原型：
`class Camera(object):`

默认的CONFIG配置如下

```python
CONFIG = {
    "background_image": None,
    "pixel_height": DEFAULT_PIXEL_HEIGHT,
    "pixel_width": DEFAULT_PIXEL_WIDTH,
    "frame_rate": DEFAULT_FRAME_RATE,
    # Note: frame height and width will be resized to match
    # the pixel aspect ratio
    "frame_height": FRAME_HEIGHT,
    "frame_width": FRAME_WIDTH,
    "frame_center": ORIGIN,
    "background_color": BLACK,
    "background_opacity": 1,
    # Points in vectorized mobjects with norm greater
    # than this value will be rescaled.
    "max_allowable_norm": FRAME_WIDTH,
    "image_mode": "RGBA",
    "n_channels": 4,
    "pixel_array_dtype": 'uint8',
    # z_buff_func is only used if the flag above is set to True.
    # round z coordinate to nearest hundredth when comparring
    "z_buff_func": lambda m: np.round(m.get_center()[2], 2),
    "cairo_line_width_multiple": 0.01,
}
```

提供的函数接口如下：

```python
def __init__(self, background=None, **kwargs):

def __deepcopy__(self, memo):

def reset_pixel_shape(self, new_height, new_width):

def get_pixel_height(self):

def get_pixel_width(self):

def get_frame_height(self):

def get_frame_width(self):

def get_frame_center(self):

def set_frame_height(self, frame_height):

def set_frame_width(self, frame_width):

def set_frame_center(self, frame_center):

def resize_frame_shape(self, fixed_dimension=0):

def init_background(self):

def get_image(self, pixel_array=None):

def get_pixel_array(self):

def convert_pixel_array(self, pixel_array, convert_from_floats=False):

def set_pixel_array(self, pixel_array, convert_from_floats=False):

def set_background(self, pixel_array, convert_from_floats=False):

def make_background_from_func(self, coords_to_colors_func):

def set_background_from_func(self, coords_to_colors_func):

def reset(self):

def extract_mobject_family_members(
            self, mobjects, only_those_with_points=False):

def get_mobjects_to_display(
            self, mobjects, include_submobjects=True, excluded_mobjects=None):

def is_in_frame(self, mobject):

def capture_mobject(self, mobject, **kwargs):

def capture_mobjects(self, mobjects, **kwargs):

def get_cached_cairo_context(self, pixel_array):

def cache_cairo_context(self, pixel_array, ctx):

def get_cairo_context(self, pixel_array):

def display_multiple_vectorized_mobjects(self, vmobjects, pixel_array):

def display_multiple_non_background_colored_vmobjects(self, vmobjects, pixel_array):

def display_vectorized(self, vmobject, ctx):

def set_cairo_context_path(self, ctx, vmobject):

def set_cairo_context_color(self, ctx, rgbas, vmobject):

def apply_fill(self, ctx, vmobject):

def apply_stroke(self, ctx, vmobject, background=False):

def get_stroke_rgbas(self, vmobject, background=False):

def get_fill_rgbas(self, vmobject):

def get_background_colored_vmobject_displayer(self):

def display_multiple_background_colored_vmobject(self, cvmobjects, pixel_array):

def display_multiple_point_cloud_mobjects(self, pmobjects, pixel_array):

def display_point_cloud(self, pmobject, points, rgbas, thickness, pixel_array):

def display_multiple_image_mobjects(self, image_mobjects, pixel_array):

def display_image_mobject(self, image_mobject, pixel_array):

def overlay_rgba_array(self, pixel_array, new_array):

def overlay_PIL_image(self, pixel_array, image):

def adjust_out_of_range_points(self, points):

def transform_points_pre_display(self, mobject, points):

def points_to_pixel_coords(self, mobject, points):

def on_screen_pixels(self, pixel_coords):

def adjusted_thickness(self, thickness):

def get_thickening_nudges(self, thickness):

def thickened_coordinates(self, pixel_coords, thickness):

def get_coords_of_all_pixels(self):

```

***声明原型：***
`class BackgroundColoredVMobjectDisplayer(object):`



### 2. mapping_camera

***声明原型：***
`class MappingCamera(Camera):`

默认的CONFIG配置如下

```python
CONFIG = {
    "mapping_func": lambda p: p,
    "min_num_curves": 50,
    "allow_object_intrusion": False
}
```

***声明原型：***
`class OldMultiCamera(Camera):`


### 3. moving_camera

***声明原型：***
`class MovingCamera(Camera):`

默认的CONFIG配置如下

```python
CONFIG = {
    "fixed_dimension": 0,  # width
    "default_frame_stroke_color": WHITE,
    "default_frame_stroke_width": 0,
}
```

### 4. multi_camera

***原型声明：***
`class MultiCamera(MovingCamera):`

默认的CONFIG配置如下

```python
CONFIG = {
    "allow_cameras_to_capture_their_own_display": False,
}
```

### 5. 3d camera

***声明原型：***
`class ThreeDCamera(Camera):`

默认的CONFIG配置如下

```python
CONFIG = {
    "shading_factor": 0.2,
    "distance": 20.0,
    "default_distance": 5.0,
    "phi": 0,  # Angle off z axis
    "theta": -90 * DEGREES,  # Rotation about z axis
    "gamma": 0,  # Rotation about normal vector to camera
    "light_source_start_point": 9 * DOWN + 7 * LEFT + 10 * OUT,
    "frame_center": ORIGIN,
    "should_apply_shading": True,
    "exponential_projection": False,
    "max_allowable_norm": 3 * FRAME_WIDTH,
}
```