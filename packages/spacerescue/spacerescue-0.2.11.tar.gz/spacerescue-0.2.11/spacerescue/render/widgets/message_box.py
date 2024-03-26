import pyray as pr

from spacerescue.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from spacerescue.resources import STRING_OK
from spacerescue.resources.resource_manager import ResourceManager
from spacerescue.render.widgets.button import Button
from spacerescue.render.widget import Widget


class MessageBox(Widget):

    RESOURCE_MANAGER = ResourceManager.get_instance("scene")

    FONT_SIZE = 20
    FONT_COLOR = pr.Color(216, 216, 216, 255)
    BORDER_SIZE = 10
    BUTTON_WIDTH = 100
    BUTTON_HEIGHT = 38
    BUTTON_COLOR = pr.Color(255, 125, 109, 192)
    FG_COLOR = pr.Color(38, 51, 59, 255)
    BG_COLOR = pr.Color(82, 96, 105, 216)

    def __init__(self, id: str, size: pr.Vector2, message: str, callback = None):
        super().__init__(id, self._get_bound(size))
        self.message = message
        self.callback = callback
        self.button = Button(
            "button_ok",
            self._get_button_position(),
            pr.Vector2(MessageBox.BUTTON_WIDTH, MessageBox.BUTTON_HEIGHT),
            STRING_OK,
            MessageBox.BUTTON_COLOR,
            self._button_is_clicked,
        )

    def update(self):
        self.button.update()

    def draw(self):
        pr.draw_rectangle_rec(self.bound, MessageBox.BG_COLOR)
        pr.draw_rectangle_lines_ex(self.bound, 2, MessageBox.FG_COLOR)
        pos = self._get_text_position()
        pr.draw_text(
            self.message,
            int(pos.x),
            int(pos.y),
            MessageBox.FONT_SIZE,
            MessageBox.FONT_COLOR,
        )
        self.button.draw()

    def _get_bound(self, size: pr.Vector2) -> pr.Rectangle:
        return pr.Rectangle(
            (SCREEN_WIDTH - size.x) / 2,
            (SCREEN_HEIGHT - size.y) / 2,
            size.x,
            size.y,
        )
        
    def _get_button_position(self) -> pr.Vector2:
        pos_x = (
            self.bound.x
            + self.bound.width
            - MessageBox.BORDER_SIZE
            - MessageBox.BUTTON_WIDTH
        )
        pos_y = (
            self.bound.y
            + self.bound.height
            - MessageBox.BORDER_SIZE
            - MessageBox.BUTTON_HEIGHT
        )
        return pr.Vector2(pos_x, pos_y)
    
    def _get_text_position(self) -> pr.Vector2:
        hw = pr.measure_text(self.message, MessageBox.FONT_SIZE) / 2
        pos_x = int(self.bound.x + self.bound.width / 2 - hw - MessageBox.BORDER_SIZE)
        pos_y = int(
            self.bound.y
            + self.bound.height / 2
            - MessageBox.FONT_SIZE / 2
            - MessageBox.BUTTON_HEIGHT / 2
            - MessageBox.BORDER_SIZE
        )
        return pr.Vector2(pos_x, pos_y)

    def _button_is_clicked(self, button: Button):
        if button.id == "button_ok":
            if self.callback is not None:
                self.callback(self)