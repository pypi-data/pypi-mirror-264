import pyray as pr

from spacerescue.resources import GLOBAL_RESOURCES, SCENE_RESOURCES
from spacerescue.render.widget import Widget
from spacerescue.tools.util import wait_while_true


class CheckBox(Widget):

    FONT_SIZE = 28
    FONT_SPACING = 2
    
    def __init__(
        self,
        id: str,
        position: pr.Vector2,
        size: pr.Vector2,
        text: str,
        color: pr.Color,
        callback=None,
    ):
        super().__init__(id, pr.Rectangle(position.x, position.y, size.x, size.y))
        self.text = text
        self.color = color
        self.callback = callback
        self.clicked = False
        self.action = False
        
        self.font = SCENE_RESOURCES.load_font("mono_font28")
        self.sound = GLOBAL_RESOURCES.load_sound("button_click")
        wait_while_true(lambda: not pr.is_sound_ready(self.sound))

    def update(self):
        pos = pr.get_mouse_position()
        if pr.check_collision_point_rec(pos, self.bound):
            if pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT):
                pr.play_sound(self.sound)
                self.clicked = not self.clicked
                self.action = self.clicked
            if self.action:
                if self.callback is not None:
                    self.callback(self)
                self.action = False
        else:
            self.action = False

    def draw(self):
        if self.clicked:
            pr.draw_rectangle_rounded(self.bound, 0.5, 4, self.color)  # type: ignore
        pr.draw_rectangle_rounded_lines(self.bound, 0.5, 4, 2, self.color)  # type: ignore
        pos = pr.Vector2(self.bound.x + self.bound.width * 2, self.bound.y - 5)
        pr.draw_text_ex(self.font, self.text, pos, CheckBox.FONT_SIZE, CheckBox.FONT_SPACING, self.color)
