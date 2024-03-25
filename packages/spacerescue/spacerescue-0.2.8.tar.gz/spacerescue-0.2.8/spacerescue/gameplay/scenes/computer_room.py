import pyray as pr

from spacerescue.gameplay.challenges.challenge2 import Challenge2
from spacerescue.gameplay.challenges.challenge3 import Challenge3
from spacerescue.gameplay.scenes.travel_to_home import TravelToHome
from spacerescue.gameplay.scenes.travel_to_hyperspace import TravelToHyperspace
from spacerescue.gameplay.scenes.travel_to_portal import TravelToPortal
from spacerescue.render.widgets.blueprint_box import BlueprintBox
from spacerescue.render.widgets.message_box import MessageBox
from spacerescue.resources import (
    GLOBAL_RESOURCES,
    STRING_ALL_CHALLENGES_UNLOCKED,
    STRING_MUSIC_ONOFF,
    STRING_ONE_CHALLENGE_UNLOCKED,
    STRING_QUIT,
)
from spacerescue.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from spacerescue.gameplay.challenges.challenge1 import Challenge1
from spacerescue.gameplay.game_scene import (
    GameScene,
    GameSceneEnd,
    GameSceneNext,
    GameSceneResult,
    GameSubScene,
)
from spacerescue.render.animators.open_horizontal import OpenHorizontal
from spacerescue.render.effects.fade_scr import FadeScr
from spacerescue.render.widgets.button import Button
from spacerescue.render.effects.fade_inout import FadeInOut
from spacerescue.render.widgets.screen import Screen


class ComputerRoom(GameScene):

    def enter(self):
        super().enter()
        self._build_ui()
        self.state = 0
        self.unlocked_challenges = self.game_state.context["unlocked"]
        self.played_challenges = self.game_state.context["played"]
        self.last_challenge = None
        self.cinematic_scenes: list[GameSubScene] = []

    def update(self) -> GameSceneResult:
        match self.state:
            case 0:
                if self.fade_in.is_playing():
                    self.fade_in.update()
                else:
                    self.state = 1

            case 1:
                if self.blueprint_animator.is_playing():
                    self.blueprint_animator.update()
                else:
                    self.state = 2

            case 2:
                self.blueprint_animator.update()
                for button in self.buttons:
                    button.update()
                self._check_unlocked()

            case 3:
                assert self.last_challenge is not None
                self.state = 4
                return GameSceneNext(self.last_challenge.get_scene().enter())

            case 4:
                self.fade_in.reset()
                self.blueprint_animator.reset()
                self.state = 0

            case 5:
                if len(self.cinematic_scenes) > 0:
                    return GameSceneNext(self.cinematic_scenes.pop(0).enter())
                else:
                    self.fade_in.reset()
                    self.blueprint_animator.reset()
                    self.state = 0

            case 6:
                assert self.message_box is not None
                self.message_box.update()

            case 7:
                if self.fade_out.is_playing():
                    self.fade_out.update()
                else:
                    self.game_state.context["next_state"] = "menu_state"
                    self.state = 9

            case 8:
                self.game_state.context["next_state"] = "game_over_state"
                self.state = 10

            case 9:
                return GameSceneEnd(self)

            case 10:
                return GameSceneEnd(self)

        return super().update()

    def draw(self):
        pr.begin_drawing()
        self.menu.draw()
        if self.state >= 1:
            self.blueprint_animator.draw()
        if self.state >= 2:
            for button in self.buttons:
                button.draw()
        if self.state == 6:
            assert self.message_box is not None
            self.message_box.draw()
        if self.state == 0:
            self.fade_in.draw()
        if self.state in (7, 9):
            self.fade_out.draw()
        pr.end_drawing()

    def _build_ui(self):
        self.menu = Screen("room", "room")
        self.fade_in = FadeScr(1.0)
        self.fade_out = FadeInOut(255, 0, 1.0, pr.Color(*pr.BLACK))
        self.message_box = None
        self.blueprint = BlueprintBox(
            "blueprint", self.game_state.context["unlocked"], self._blueprint_is_clicked
        )
        self.blueprint_animator = OpenHorizontal(
            self.blueprint, 0.3, BlueprintBox.BG_COLOR
        )
        self.buttons = [
            Button(
                "button_quit",
                pr.Vector2(SCREEN_WIDTH - 220, SCREEN_HEIGHT - 45),
                pr.Vector2(200, 38),
                STRING_QUIT,
                Button.RED,
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

    def _blueprint_is_clicked(self, blueprint):
        match blueprint.action:
            case 0:
                self.last_challenge = Challenge1(self)
                self.state = 3

            case 1:
                self.last_challenge = Challenge2(self)
                self.state = 3

            case 2:
                self.last_challenge = Challenge3(self)
                self.state = 3

    def _button_is_clicked(self, button: Button):
        match button.id:
            case "button_quit":
                self.state = 7

            case "button_music_onoff":
                self._stop_music()

    def _message_box_is_closed(self, message_box: MessageBox):
        self.message_box = None
        match message_box.id:
            case "mb_one_unlocked":
                self.state = 2
                self._check_for_cinematic_scenes()

            case "mb_all_unlocked":
                self.state = 8

    def _check_unlocked(self):
        if all(self.unlocked_challenges) and all(self.played_challenges):
            mb = MessageBox(
                "mb_all_unlocked",
                pr.Vector2(500, 300),
                STRING_ALL_CHALLENGES_UNLOCKED,
                self._message_box_is_closed,
            )
            self.message_box = OpenHorizontal(mb, 0.3, MessageBox.BG_COLOR)
            self.state = 6
        elif self.last_challenge is not None and self.last_challenge.unlocked:
            mb = MessageBox(
                "mb_one_unlocked",
                pr.Vector2(500, 300),
                STRING_ONE_CHALLENGE_UNLOCKED,
                self._message_box_is_closed,
            )
            self.message_box = OpenHorizontal(mb, 0.3, MessageBox.BG_COLOR)
            self.last_challenge = None
            self.state = 6

    def _check_for_cinematic_scenes(self):
        self.cinematic_scenes = []
        if self.unlocked_challenges[0] and not self.played_challenges[0]:
            self.cinematic_scenes.append(TravelToPortal(self))
            self.played_challenges[0] = True
            self.state = 5
        if self.unlocked_challenges[0] and self.unlocked_challenges[1] and not self.played_challenges[1]:
            self.cinematic_scenes.append(TravelToHyperspace(self))
            self.played_challenges[1] = True
            self.state = 5
        if self.unlocked_challenges[0] and self.unlocked_challenges[1] and self.unlocked_challenges[2] and not self.played_challenges[2]:
            self.cinematic_scenes.append(TravelToHome(self))
            self.played_challenges[2] = True
            self.state = 5

    def _stop_music(self):
        music = GLOBAL_RESOURCES.load_music("music")
        if pr.is_music_stream_playing(music):
            pr.stop_music_stream(music)
        else:
            pr.play_music_stream(music)
