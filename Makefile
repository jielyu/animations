
XX=manim
ARGS=-pl
#ARGS=-t --high_quality

all: e02_solution01
	@echo "create all animations completely"

e01_file=src/s01/e01_groupsize.py
e01: e01_problem e01_solution01 e01_solution02
	@echo "create e01 animations finished"
e01_problem:
	${XX} ${e01_file} Problem ${ARGS}
e01_solution01:
	${XX} ${e01_file} Solution01 ${ARGS}
e01_solution02:
	${XX} ${e01_file} Solution02 ${ARGS}

e02_file=src/s01/e02_server.py
e02: e02_problem e02_solution01
	@echo "create e01 animations finished"
e02_problem:
	${XX} ${e02_file} Problem ${ARGS}
e02_solution01:
	${XX} ${e02_file} Solution01 ${ARGS}

# clean all output
clean:
	@rm -rf output/*
clean480:
	@rm -rf output/videos/*/480*