from manim import *


class Indications(Scene):
    def construct(self):
        indications = [
            ApplyWave,
            Circumscribe,
            Flash,
            FocusOn,
            Indicate,
            ShowPassingFlash,
            Wiggle,
        ]
        names = [Tex(i.__name__).scale(3) for i in indications]

        self.add(names[0])
        for i in range(len(names)):
            if indications[i] is Flash:
                self.play(Flash(UP))
            elif indications[i] is ShowPassingFlash:
                self.play(ShowPassingFlash(Underline(names[i])))
            else:
                self.play(indications[i](names[i]))
            self.play(
                AnimationGroup(
                    FadeOut(names[i], shift=UP * 1.5),
                    FadeIn(names[(i + 1) % len(names)], shift=UP * 1.5),
                )
            )
