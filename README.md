# leetcode-animate

to manager python code of making animations for leetcode problems and solutions. 

## 1. LeetCode

### (1). 001-100

[文档](src/leetcode/e001_100/README.md)

## 文档备注

使用sphinx创建文档的步骤如下，所有文档操作在docs目录下进行

### A. sphinx操作

(1) 生成文档工程

```shell
sphinx-quickstart
```

(2) 修改 conf.py

将工程目录和源码目录加入到环境变量中

```python
sys.path.append(os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../src'))
```

(3) 生成rst文件

```shell
sphinx-apidoc -o source/ ../src
```

(4) 添加文档

添加生成的rst文件到index.rst文件中

(5) 编译生成文档

```shell
make html
```

在build目录下查看index.html文件。如果想生成latex并编译为pdf文件，需要在conf.py中设置latex参数，然后运行

```shell
make latexpdf
```

或者

```shell
make latex
cd build/latex
make
```

### B. 添加扩展

修改conf.py中变量如下：

```python
extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon'
]
```

### C. 更换默认html主题

修改conf.py中变量如下：

```python
#html_theme = 'alabaster'
# html_theme = 'classic'
# html_theme = 'sphinxdoc'
# html_theme = 'scrolls'
html_theme = 'sphinx_rtd_theme'
```

### D. 更换语言

设置语言为中文，修改conf.py文件如下：

```python
language = 'zh_CN'
```

### E. 生成latex

添加conf.py中的变量如下：

```python
latex_engine = 'xelatex'
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'preamble': r'''
\usepackage{xeCJK}
\setCJKmainfont[BoldFont=SimHei, ItalicFont=SimHei]{SimSun}
\setCJKsansfont[BoldFont=SimHei]{SimSun}
\setCJKmonofont{SimHei}
\XeTeXlinebreaklocale "zh"
\XeTeXlinebreakskip = 0pt plus 1pt
\parindent 2em
\definecolor{VerbatimColor}{rgb}{0.95,0.95,0.95}
\setcounter{tocdepth}{3}
\renewcommand\familydefault{\ttdefault}
\renewcommand\CJKfamilydefault{\CJKrmdefault}
'''
}
```

