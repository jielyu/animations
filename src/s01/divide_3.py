from manimlib.imports import *
from itertools import chain

class Divide3Scene(Scene):
    pass

class Problem(Divide3Scene):

    def construct(self):
        t = TextMobject('Problem')
        self.play(Write(t))


class Solution01(Divide3Scene):

    def construct(self):
        t = TextMobject('Solution01')
        self.play(Write(t))

