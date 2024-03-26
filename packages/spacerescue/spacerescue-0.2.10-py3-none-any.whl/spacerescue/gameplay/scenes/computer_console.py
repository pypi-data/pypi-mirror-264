import pyray as pr
import pyperclip as pc

from spacerescue.resources import (
    GLOBAL_RESOURCES,
    SCENE_RESOURCES,
    STRING_COMMIT,
    STRING_COPY_ID,
    STRING_MISSION_CAPTION,
    STRING_CODE_UNDER_VALIDATION,
    STRING_ANSER_IS_INCORRECT,
    STRING_ANSWER_IS_CORRECT,
    STRING_MUSIC_ONOFF,
    STRING_QUIT,
)
from spacerescue.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from spacerescue.gameplay.challenge import CodeChallenge
from spacerescue.gameplay.game_scene import GameScene, GameSubScene, GameSceneEnd, GameSceneResult
from spacerescue.render.animators.open_horizontal import OpenHorizontal
from spacerescue.render.widgets.progress_box import ProgressBox
from spacerescue.render.widgets.markdown_box import MarkdownBox
from spacerescue.render.widgets.button import Button
from spacerescue.render.effects.fade_scr import FadeScr
from spacerescue.render.widgets.message_box import MessageBox
from spacerescue.render.widgets.screen import Screen


class ComputerConsole(GameSubScene):

    BORDER_SIZE = 80
    
    def __init__(self, scene: GameScene, challenge: CodeChallenge):
        super().__init__(scene)
        self.challenge = challenge
        self.buffers = [
            SCENE_RESOURCES.load_yaml("strings")["help"],
            self.challenge.mission,
        ]

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
                self.console.update()
                for button in self.buttons:
                    button.update()

            case 2:
                assert self.message_box is not None
                self.message_box.update()

            case 3:
                return GameSceneEnd(self)
            
            case 4:
                return GameSceneEnd(self)

        return super().update()

    def draw(self):
        pr.begin_drawing()
        pr.clear_background(MarkdownBox.BG_COLOR)
        self.console.draw()
        self.screen.draw()
        for button in self.buttons:
            button.draw()
        if self.state == 2 and self.message_box is not None:
            self.message_box.draw()
        if self.state == 0:
            self.fade_in.draw()
        pr.end_drawing()

    def _build_ui(self):
        self.fade_in = FadeScr(0.5)
        self.screen = Screen("widget", "console")
        self.message_box = None
        self.console = MarkdownBox(
            "widget",
            pr.Vector2(200, 112),
            pr.Vector2(SCREEN_WIDTH - 390, SCREEN_HEIGHT - 240),
            self.buffers,
            caption=STRING_MISSION_CAPTION.format(self.challenge.token),
            first_buffer=1,
            border_size=ComputerConsole.BORDER_SIZE,
        )
        self.buttons = [
            Button(
                "button_commit",
                pr.Vector2(SCREEN_WIDTH - 220, SCREEN_HEIGHT - 94),
                pr.Vector2(200, 38),
                STRING_COMMIT,
                Button.YELLOW,
                self._button_is_clicked,
            ),
            Button(
                "button_quit",
                pr.Vector2(SCREEN_WIDTH - 220, SCREEN_HEIGHT - 45),
                pr.Vector2(200, 38),
                STRING_QUIT,
                Button.RED,
                self._button_is_clicked,
            ),
            Button(
                "button_copy_id",
                pr.Vector2(20, SCREEN_HEIGHT - 94),
                pr.Vector2(200, 38),
                STRING_COPY_ID,
                Button.BLUE,
                self._button_is_clicked,
            ),
            Button(
                "button_music_onoff",
                pr.Vector2(20, SCREEN_HEIGHT - 45),
                pr.Vector2(200, 38),
                STRING_MUSIC_ONOFF,
                Button.BLUE,
                self._button_is_clicked,
            ),
        ]

    def _validate_code(self):
        mb = ProgressBox(
            "mb_progress",
            pr.Vector2(500, 300),
            STRING_CODE_UNDER_VALIDATION,
            self.challenge.validate(),
            self._message_box_is_closed,
        )
        self.message_box = OpenHorizontal(mb, 0.3, MessageBox.BG_COLOR)
        self.state = 2

    def _commit_code(self):
        mb = (
            self.challenge.commit()
            .map(
                lambda _: MessageBox(
                    "mb_sucess",
                    pr.Vector2(500, 300),
                    STRING_ANSWER_IS_CORRECT,
                    self._message_box_is_closed,
                )
            )
            .or_else(
                lambda x: MessageBox(
                    "mb_failure",
                    pr.Vector2(max(pr.measure_text(str(x), 20) + 40, 500), 300),
                    STRING_ANSER_IS_INCORRECT.format(reason=x),
                    self._message_box_is_closed,
                )
            )
        )
        self.message_box = OpenHorizontal(mb, 0.3, MessageBox.BG_COLOR)
        self.state = 2

    def _button_is_clicked(self, button: Button):
        match button.id:
            case "button_commit":
                self._validate_code()

            case "button_quit":
                self.state = 3
                
            case "button_copy_id":
                self._copy_challenge_id()

            case "button_music_onoff":
                self._stop_music()

    def _message_box_is_closed(self, message_box: MessageBox):
        self.message_box = None
        match message_box.id:
            case "mb_progress":
                self._commit_code()
            
            case "mb_sucess":
                self.state = 4
                
            case "mb_failure":
                self.state = 1

    def _stop_music(self):
        music = GLOBAL_RESOURCES.load_music("music")
        if pr.is_music_stream_playing(music):
            pr.stop_music_stream(music)
        else:
            pr.play_music_stream(music)

    def _copy_challenge_id(self):
        pc.copy(self.challenge.token)
