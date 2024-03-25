import pyray as pr

from spacerescue.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from spacerescue.gameplay.game_scene import GameScene, GameSceneEnd, GameSceneResult
from spacerescue.gameplay.game_state import GameState
from spacerescue.render.animators.open_vertical import OpenVertical
from spacerescue.core.pyray import is_skip_key
from spacerescue.render.widgets.markdown_box import MarkdownBox
from spacerescue.render.effects.fade_inout import FadeInOut
from spacerescue.render.effects.fade_scr import FadeScr
from spacerescue.render.widgets.screen import Screen
from spacerescue.resources import GLOBAL_RESOURCES


class GameOver(GameScene):

    def __init__(self, game_state: GameState, success: bool):
        super().__init__(game_state)
        self.success = success

    def enter(self):
        super().enter()
        self._build_ui()
        self.state = 0

    def update(self) -> GameSceneResult:
        match self.state:
            case 0:
                if self.fade_in.is_playing():
                    self.fade_in.update()
                else:
                    self.state = 1

            case 1:
                if (
                    self.avatar_animator.is_playing()
                    or self.avatar_animator.is_playing()
                ):
                    self.avatar_animator.update()
                    self.console_animator.update()
                else:
                    self.state = 2

            case 2:
                if not is_skip_key():
                    self.avatar_animator.update()
                    self.console_animator.update()
                else:
                    self.state = 3

            case 3:
                if self.fade_out.is_playing():
                    self.fade_out.update()
                else:
                    self.state = 4

        return super().update() if self.state < 4 else GameSceneEnd(self)

    def draw(self):
        pr.begin_drawing()
        self.menu.draw()
        if self.state in (1, 2, 3, 4):
            self.avatar_animator.draw()
            self.console_animator.draw()
        if self.state == 0:
            self.fade_in.draw()
        if self.state in (3, 4):
            self.fade_out.draw()
        pr.end_drawing()

    def _build_ui(self):
        msg = "game_over_success" if self.success else "game_over_failure"
        self.menu = Screen("menu", "menu")
        self.fade_in = FadeScr(1.0)
        self.fade_out = FadeInOut(255, 0, 1.0, pr.Color(*pr.BLACK))
        self.avatar = MarkdownBox(
            "widget",
            pr.Vector2(100, 100),
            pr.Vector2(256, 256),
            ["![avatar](resources/images/avatar.png)"],
        )
        self.avatar_animator = OpenVertical(self.avatar, 0.5, MarkdownBox.BG_COLOR)
        self.console = MarkdownBox(
            "widget",
            pr.Vector2(400, 100),
            pr.Vector2(SCREEN_WIDTH / 2, 19 * MarkdownBox.FONT_SIZE),
            [GLOBAL_RESOURCES.load_yaml("strings")[msg]],
        )
        self.console_animator = OpenVertical(self.console, 0.5, MarkdownBox.BG_COLOR)
