import pyray as pr

from spacerescue.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from spacerescue.render.animator import Animator
from spacerescue.core.math import EPSILON, clamp


class FadeInOut(Animator):

    def __init__(self, min: int, max: int, duration: float, color: pr.Color):
        super().__init__(duration)
        self.min = min
        self.max = max
        self.color = color

    def draw(self):
        t = self.timer / (self.duration + EPSILON)
        alpha = float(clamp(self.max * (1.0 - t) + self.min * t, 0, 255))
        if alpha > 0.0:
            pr.draw_rectangle(
                0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, pr.fade(self.color, alpha / 255.0)
            )
