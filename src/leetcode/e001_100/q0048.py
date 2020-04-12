"""
Q0048
"""

from manimlib.imports import *
from itertools import chain

class BasicScene(Scene):
    pass

class Problem(BasicScene):

    def construct(self):
        t = TextMobject('Problem')
        self.play(Write(t))


class Solution01(BasicScene):

    def construct(self):
        t = TextMobject('Solution01')
        self.play(Write(t))