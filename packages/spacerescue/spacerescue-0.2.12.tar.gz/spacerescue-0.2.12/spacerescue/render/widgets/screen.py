import pyray as pr

from spacerescue.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from spacerescue.resources import SCENE_RESOURCES
from spacerescue.render.widget import Widget


class Screen(Widget):

    def __init__(self, id: str, texture_name: str):
        super().__init__(id, self._get_bound())
        self.surface = SCENE_RESOURCES.load_texture(texture_name)

    def draw(self):
        pr.draw_texture_pro(
            self.surface,
            self.bound,
            self.bound,
            pr.vector2_zero(),
            0.0,
            pr.WHITE,  # type: ignore
        )
        
    def _get_bound(self) -> pr.Rectangle:
        return pr.Rectangle(
                0,
                0,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
            )
