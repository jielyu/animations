
XX=manim
ARGS=-pl
#ARGS=-t --high_quality

all: q1262 q1267 q1282 manim_demo test
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
q1282_file=src/leetcode/start/q1282.py
q1282: q1282o q1282p q1282s q1282sopt
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
q1282p:
	${XX} ${q1282_file} Problem ${ARGS}
q1282s:
	${XX} ${q1282_file} Solution ${ARGS}
q1282sopt:
	${XX} ${q1282_file} SolutionOpt ${ARGS}

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

# For s01_think

# command for perception animations
perceptron_file=src/s01_thinking/perceptron.py
perceptron:
	${XX} ${perceptron_file} Perceptron ${ARGS}
perceptron_ps:
	${XX} ${perceptron_file} PerceptronParamSpace ${ARGS}

test: testanim testcamera testmobject test_scene
	@echo "create all tests completely"

# command for animation test
anim_file=src/test/test_animation.py
testanim:
	${XX} ${anim_file}  TransformExample ${ARGS}

# command for camera test
camera_file=src/test/test_camera.py
testcamera:
	${XX} ${camera_file} CameraExample ${ARGS}

# command for mobject test
mobj_file=src/test/test_mobject.py
testmobject: testmobj_text testmobj_position testmobj_sizetext \
                 testmobj_textarray testmobj_vgroup testmobj_shape testmobj_shape3d
testmobj_text:
	${XX} ${mobj_file} TextExample ${ARGS}
testmobj_position:
	${XX} ${mobj_file} PositionExample ${ARGS}
testmobj_sizetext:
	${XX} ${mobj_file} SizeTextExample ${ARGS}
testmobj_textarray:
	${XX} ${mobj_file} TextArrayExample ${ARGS}
testmobj_vgroup:
	${XX} ${mobj_file} VGroupExample ${ARGS}
testmobj_shape:
	${XX} ${mobj_file} ShapeExample ${ARGS}
testmobj_shape3d:
	${XX} ${mobj_file} Shape3DExample ${ARGS}

# command for scene test
scene_file=src/test/test_scene.py
test_scene: test_graph2d test_scene3d test_movingcamerascene \
            test_samplespacescene test_zoomedscene test_ltscene \
			test_configscene test_updatescene test_coorscene
test_graph2d:
	${XX} ${scene_file} Graph2DExample ${ARGS}
test_scene3d:
	${XX} ${scene_file} ThreeDExample ${ARGS}
test_movingcamerascene:
	${XX} ${scene_file} MovingCameraExample ${ARGS}
test_samplespacescene:
	${XX} ${scene_file} SampleSpaceExample ${ARGS}
test_zoomedscene:
	${XX} ${scene_file} ZoomedExample ${ARGS}
test_ltscene:
	${XX} ${scene_file} VectorExample ${ARGS}
test_configscene:
	${XX} ${scene_file} ConfigSceneExample ${ARGS}
test_updatescene:
	${XX} ${scene_file} UpdateExample ${ARGS}
test_coorscene:
	${XX} ${scene_file} CoorExample ${ARGS}

# clean all output
clean:
	@rm -rf output/*
clean480:
	@rm -rf output/videos/*/480*