import pyray as pr

from spacerescue.resources import GLOBAL_RESOURCES
from spacerescue.resources.resource_manager import ResourceManager
from spacerescue.render.widget import Widget
from spacerescue.tools.util import wait_while_true


class Button(Widget):

    FONT_SIZE = 20
    FG_COLOR = pr.Color(38, 51, 59, 255)
    
    RED = pr.Color(252, 127, 104, 192)
    YELLOW = pr.Color(254, 201, 123, 192)
    BLUE = pr.Color(64, 191, 182, 192)

    def __init__(
        self,
        id: str,
        position: pr.Vector2,
        size: pr.Vector2,
        text: str,
        color: pr.Color,
        callback = None,
    ):
        super().__init__(id, self._get_bound(position, size))
        self.text = text
        self.color_up = color
        self.color_dn = pr.Color(color.r // 2, color.g // 2, color.b // 2, 255)
        self.callback = callback
        
        self.clicked = False
        self.action = False
        
        self.sound = GLOBAL_RESOURCES.load_sound("button_click")
        wait_while_true(lambda: not pr.is_sound_ready(self.sound))

    def update(self):
        pos = pr.get_mouse_position()
        if pr.check_collision_point_rec(pos, self.bound):
            if not self.clicked and pr.is_mouse_button_down(
                pr.MouseButton.MOUSE_BUTTON_LEFT
            ):
                self.clicked = True
                self.action = False
            if self.clicked and pr.is_mouse_button_released(
                pr.MouseButton.MOUSE_BUTTON_LEFT
            ):
                pr.play_sound(self.sound)
                self.clicked = False
                self.action = True
            if self.action:
                if self.callback is not None:
                    self.callback(self)
                self.action = False
        else:
            self.clicked = False
            self.action = False

    def draw(self):
        if self.clicked:
            pr.draw_rectangle_rounded(self.bound, 0.5, 4, self.color_dn)  # type: ignore
        else:
            pr.draw_rectangle_rounded(self.bound, 0.5, 4, self.color_up)  # type: ignore
        pr.draw_rectangle_rounded_lines(self.bound, 0.5, 4, 4, Button.FG_COLOR)  # type: ignore

        hw = pr.measure_text(self.text, Button.FONT_SIZE) / 2
        px = int(self.bound.x + self.bound.width / 2 - hw)
        py = int(self.bound.y + self.bound.height / 2 - Button.FONT_SIZE / 2)
        pr.draw_text(self.text, px, py, Button.FONT_SIZE, Button.FG_COLOR)  # type: ignore

    def _get_bound(self, position: pr.Vector2, size: pr.Vector2) -> pr.Rectangle:
        return pr.Rectangle(position.x, position.y, size.x, size.y)