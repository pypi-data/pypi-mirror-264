import pyray as pr

from spacerescue.resources import GLOBAL_RESOURCES, SCENE_RESOURCES
from spacerescue.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from spacerescue.render.widget import Widget
from spacerescue.tools.util import wait_while_true


class BlueprintBox(Widget):
    
    BG_COLOR = pr.Color(22, 39, 58, 192)

    def __init__(self, id: str, unlocked: list[bool], callback=None):
        super().__init__(id, self._get_bound())
        self.unlocked = unlocked
        self.callback = callback
        
        self.background = SCENE_RESOURCES.load_texture("blueprint")
        self.bitmask = SCENE_RESOURCES.load_image("blueprint_bitmask")
        self.masks = [
            SCENE_RESOURCES.load_texture(f"blueprint_mask{i}")
            for i in range(1, len(self.unlocked) + 1)
        ]
        self.selected = [False] * len(self.unlocked)
        self.clicked = -1
        self.action = -1
        
        self.sound = GLOBAL_RESOURCES.load_sound("button_click")
        wait_while_true(lambda: not pr.is_sound_ready(self.sound))

    def update(self):
        self.selected = [False] * len(self.unlocked)
        pos = pr.get_mouse_position()
        if pr.check_collision_point_rec(pos, self.bound):
            mask = min(self._get_mask(pos), len(self.masks) - 1)
            self.selected[mask] = mask >= 0
            if self.clicked > 0 and pr.is_mouse_button_down(
                pr.MouseButton.MOUSE_BUTTON_LEFT
            ):
                self.clicked = mask
                self.action = -1
            if pr.is_mouse_button_released(pr.MouseButton.MOUSE_BUTTON_LEFT):
                pr.play_sound(self.sound)
                self.clicked = -1
                self.action = mask
            if self.action >= 0 and not self.unlocked[mask]:
                if self.callback is not None:
                    self.callback(self)
                self.action = -1
        else:
            self.clicked = -1
            self.action = -1

    def draw(self):
        pr.draw_texture_pro(
            self.background,
            pr.Rectangle(0, 0, self.background.width, self.background.height),
            self.bound,
            pr.vector2_zero(),
            0.0,
            pr.Color(255, 255, 255, 192),  # type: ignore
        )
        for i, mask in enumerate(self.masks):
            if not self.selected[i] and not self.unlocked[i]:
                pr.draw_texture_pro(
                    mask,
                    pr.Rectangle(0, 0, mask.width, mask.height),
                    self.bound,
                    pr.vector2_zero(),
                    0.0,
                    pr.Color(255, 255, 255, 128),  # type: ignore
                )

    def _get_bound(self) -> pr.Rectangle:
        surface = SCENE_RESOURCES.load_texture("blueprint")
        return pr.Rectangle(
            SCREEN_WIDTH / 2 - surface.width / 2,
            SCREEN_HEIGHT / 2 - surface.height / 2,
            surface.width,
            surface.height,
        )

    def _get_mask(self, pos: pr.Vector2) -> int:
        color = pr.get_image_color(
            self.bitmask, int(pos.x - self.bound.x), int(pos.y - self.bound.y)
        )
        return int(color.r // 64) if color.a > 0 else -1
