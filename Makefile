
XX=manim
ARGS=-pl
#ARGS=-t --high_quality

all: e03_problem
	@echo "create all animations completely"

e01_file=src/s01/groupsize.py
e01: e01_problem e01_solution01 e01_solution02
	@echo "create e01 animations finished"
e01_problem:
	${XX} ${e01_file} Problem ${ARGS}
e01_solution01:
	${XX} ${e01_file} Solution01 ${ARGS}
e01_solution02:
	${XX} ${e01_file} Solution02 ${ARGS}

e02_file=src/s01/server.py
e02: e02_problem e02_solution01
	@echo "create e02 animations finished"
e02_problem:
	${XX} ${e02_file} Problem ${ARGS}
e02_solution01:
	${XX} ${e02_file} Solution01 ${ARGS}

e03_file=src/s01/divide_3.py
e03: e03_problem e03_solution01
	@echo "create e03 animations finished"
e03_problem:
	${XX} ${e03_file} Problem ${ARGS}
e03_solution01:
	${XX} ${e03_file} Solution01 ${ARGS}

# clean all output
clean:
	@rm -rf output/*
clean480:
	@rm -rf output/videos/*/480*