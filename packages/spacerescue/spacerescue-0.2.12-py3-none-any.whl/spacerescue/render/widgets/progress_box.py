from multiprocessing import Process

import pyray as pr

from spacerescue.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from spacerescue.render.widget import Widget


class ProgressBox(Widget):

    FONT_SIZE = 20
    FONT_COLOR = pr.Color(216, 216, 216, 255)
    BORDER_SIZE = 10
    BUTTON_WIDTH = 100
    BUTTON_HEIGHT = 38
    BUTTON_COLOR = pr.Color(255, 125, 109, 192)
    FG_COLOR = pr.Color(38, 51, 59, 255)
    BG_COLOR = pr.Color(82, 96, 105, 216)

    def __init__(self, id: str, size: pr.Vector2, message: str, process: Process, callback):
        super().__init__(id, self._get_bound(size))
        self.message = message
        self.process = process
        self.callback = callback

    def update(self):
        if not self.process.is_alive():
            self.callback(self)

    def draw(self):
        pr.draw_rectangle_rec(self.bound, ProgressBox.BG_COLOR)
        pr.draw_rectangle_lines_ex(self.bound, 2, ProgressBox.FG_COLOR)
        pos = self._get_text_position()
        pr.draw_text(
            self.message,
            int(pos.x),
            int(pos.y),
            ProgressBox.FONT_SIZE,
            ProgressBox.FONT_COLOR,
        )

    def _get_bound(self, size: pr.Vector2) -> pr.Rectangle:
        return pr.Rectangle(
            (SCREEN_WIDTH - size.x) / 2,
            (SCREEN_HEIGHT - size.y) / 2,
            size.x,
            size.y,
        )
        
    def _get_text_position(self) -> pr.Vector2:
        hw = pr.measure_text(self.message, ProgressBox.FONT_SIZE) / 2
        pos_x = int(self.bound.x + self.bound.width / 2 - hw - ProgressBox.BORDER_SIZE)
        pos_y = int(
            self.bound.y
            + self.bound.height / 2
            - ProgressBox.FONT_SIZE / 2
            - ProgressBox.BUTTON_HEIGHT / 2
            - ProgressBox.BORDER_SIZE
        )
        return pr.Vector2(pos_x, pos_y)