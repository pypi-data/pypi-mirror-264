import pyray as pr

from spacerescue.render.animator import Animator
from spacerescue.render.widget import Widget
from spacerescue.core.math import EPSILON, clamp


class OpenHorizontal(Animator):

    def __init__(self, widget: Widget, duration: float, color: pr.Color):
        super().__init__(duration)
        self.widget = widget
        self.color = color

    def update(self):
        super().update()
        if not self.is_playing():
            self.widget.update()

    def draw(self):
        if not self.is_playing():
            self.widget.draw()
        else:
            t = self.timer / (self.duration + EPSILON)
            width = int(
                clamp(self.widget.bound.width * t, 0, self.widget.bound.width)
            )
            if width > 0.0:
                rec = pr.Rectangle(
                    self.widget.bound.x + (self.widget.bound.width - width) / 2,
                    self.widget.bound.y,
                    width,
                    self.widget.bound.height,
                )
                pr.draw_rectangle_rec(rec, self.color)
