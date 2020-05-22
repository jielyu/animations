
XX=manim
ARGS=-pl
#ARGS=-t --high_quality

all: q1262 q1267 q1282
	@echo "create all animations completely"

# For Problem 1262 in Leetcode
q1262_file=src/leetcode/e001_100/q1262.py
q1262: q1262p q1262s1
	@echo "create q1262 animations finished"
q1262p:
	${XX} ${q1262_file} Problem ${ARGS}
q1262s1:
	${XX} ${q1262_file} Solution01 ${ARGS}

# For Problem 1267 in Leetcode
q1267_file=src/leetcode/e001_100/q1267.py
q1267: q1267p q1267s1
	@echo "create q1267 animations finished"
q1267p:
	${XX} ${q1267_file} Problem ${ARGS}
q1267s1:
	${XX} ${q1267_file} Solution01 ${ARGS}

# For Problem 1222 in Leetcode
q1282_file=src/leetcode/e001_100/q1282.py
q1282: q1282e1 q1282e2 q1282s1 q1282s2
	@echo "create q1282 animations finished"
q1282o:
	${XX} ${q1282_file} Opening ${ARGS}
q1282e1:
	${XX} ${q1282_file} Example01 ${ARGS} -n 51
q1282e2:
	${XX} ${q1282_file} Example02 ${ARGS}
q1282s1:
	${XX} ${q1282_file} Solution01 ${ARGS}
q1282s2:
	${XX} ${q1282_file} Solution02 ${ARGS}

# For manim demos
manim_demo: position latex_color shape coordinate animation
	@echo "create manim demo animations finished"

position_file="src/manim_demo/basic/position.py"
position:
	manim ${position_file} PositionDemo ${ARGS}
latex_color_file="src/manim_demo/basic/latex_color.py"
latex_color:
	manim ${latex_color_file} LatexDemo ${ARGS}
shape_file="src/manim_demo/basic/shape.py"
shape:
	manim ${shape_file} ShapeDemo ${ARGS}
	manim ${shape_file} Shape3DDemo ${ARGS}
coordinate_file="src/manim_demo/basic/coordinate.py"
coordinate:
	manim ${coordinate_file} CoorDemo ${ARGS}
animation_file="src/manim_demo/basic/animation.py"
animation:
	manim ${animation_file} EffectDemo ${ARGS}

# clean all output
clean:
	@rm -rf output/*
clean480:
	@rm -rf output/videos/*/480*