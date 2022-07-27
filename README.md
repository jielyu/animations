# manim动画制作

***说明： 当前项目仅可以使用社区版manim运行，不支持其它版本***

建议使用社区版manim，无论是文档、示例还是代码规范都更清晰和丰富。

[社区版manim仓库](https://github.com/ManimCommunity/manim)
[社区版manim文档](https://docs.manim.community/en/stable/)

## 运行指令示例

默认配置预览

```shell
manim test/test_animation.py TransformExample -p
```

低质量，480p15

```shell
manim test/test_animation.py TransformExample -p -ql
```

控制帧率，480p30

```
manim test/test_animation.py TransformExample -p -ql --fps 30
```

说明： -ql: 480P, -qm: 720P, -qh: 1080P, -qp: 2K, -qk: 4K 

