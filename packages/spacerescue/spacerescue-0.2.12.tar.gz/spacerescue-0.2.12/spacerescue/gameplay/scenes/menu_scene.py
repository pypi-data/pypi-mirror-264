import pyray as pr

from spacerescue.resources import (
    GLOBAL_RESOURCES,
    SCENE_RESOURCES,
    STRING_EXIT,
    STRING_MUSIC_ONOFF,
    STRING_START,
)
from spacerescue.constants import SCREEN_WIDTH
from spacerescue.gameplay.game_scene import GameScene, GameSceneEnd, GameSceneResult
from spacerescue.render.animators.open_vertical import OpenVertical
from spacerescue.render.widgets.button import Button
from spacerescue.render.widgets.markdown_box import MarkdownBox
from spacerescue.render.effects.fade_inout import FadeInOut
from spacerescue.render.widgets.screen import Screen


class Menu(GameScene):

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
                self.avatar_animator.update()
                self.console_animator.update()
                for button in self.buttons:
                    button.update()

            case 3:
                self.game_state.context["next_state"] = "main_state"
                self.state = 7

            case 5:
                if self.fade_out.is_playing():
                    self.fade_out.update()
                else:
                    self.game_state.context["next_state"] = "exit_state"
                    self.state = 6

        return super().update() if self.state < 6 else GameSceneEnd(self)

    def draw(self):
        pr.begin_drawing()
        self.menu.draw()
        if self.state in (1, 2, 3, 4, 5, 6):
            self.avatar_animator.draw()
            self.console_animator.draw()
        if self.state in (2, 3, 4, 5, 6):
            for button in self.buttons:
                button.draw()
        if self.state == 0:
            self.fade_in.draw()
        if self.state in (5, 6):
            self.fade_out.draw()
        pr.end_drawing()

    def _build_ui(self):
        self.menu = Screen("menu", "menu")
        self.fade_in = FadeInOut(0, 255, 1.0, pr.Color(*pr.BLACK))
        self.fade_out = FadeInOut(255, 0, 1.0, pr.Color(*pr.BLACK))
        self.avatar = MarkdownBox(
            "widget",
            pr.Vector2(100, 100),
            pr.Vector2(256, 256),
            ["![avatar](resources/images/avatar.png)"],
        )
        self.avatar_animator = OpenVertical(self.avatar, 0.3, MarkdownBox.BG_COLOR)
        self.console = MarkdownBox(
            "widget",
            pr.Vector2(400, 100),
            pr.Vector2(SCREEN_WIDTH / 2, 19 * MarkdownBox.FONT_SIZE),
            [SCENE_RESOURCES.load_yaml("strings")["story"]],
        )
        self.console_animator = OpenVertical(self.console, 0.3, MarkdownBox.BG_COLOR)
        self.buttons = [
            Button(
                "button_start",
                pr.Vector2(SCREEN_WIDTH - 220, 100),
                pr.Vector2(200, 38),
                STRING_START,
                pr.Color(254, 201, 123, 192),
                self._button_is_clicked,
            ),
            Button(
                "button_music_onoff",
                pr.Vector2(SCREEN_WIDTH - 220, 150),
                pr.Vector2(200, 38),
                STRING_MUSIC_ONOFF,
                pr.Color(64, 191, 182, 192),
                self._button_is_clicked,
            ),
            Button(
                "button_exit",
                pr.Vector2(SCREEN_WIDTH - 220, 200),
                pr.Vector2(200, 38),
                STRING_EXIT,
                pr.Color(252, 127, 104, 192),
                self._button_is_clicked,
            ),
        ]

    def _button_is_clicked(self, button: Button):
        if button.id == "button_start":
            self.state = 3
        elif button.id == "button_music_onoff":
            self._toggle_music_onoff()
        elif button.id == "button_exit":
            self.state = 5

    def _toggle_music_onoff(self):
        music = GLOBAL_RESOURCES.load_music("music")
        if pr.is_music_stream_playing(music):
            pr.stop_music_stream(music)
        else:
            pr.play_music_stream(music)
