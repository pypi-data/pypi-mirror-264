import pyray as pr

from spacerescue.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from spacerescue.core.pyray import is_skip_key
from spacerescue.gameplay.game_scene import GameScene, GameSceneEnd, GameSceneResult
from spacerescue.render.effects.fade_inout import FadeInOut
from spacerescue.render.widgets.screen import Screen
from spacerescue.resources.resource_manager import ResourceManager


class Title(GameScene):

    def enter(self):
        super().enter()
        self.title = Screen("title", "title")
        self.fade_in = FadeInOut(0, 255, 1.0, pr.Color(*pr.WHITE))
        self.fade_out = FadeInOut(255, 0, 1.0, pr.Color(*pr.BLACK))
        self.timer = 0
        self.state = 0
        self._start_play_music()

    def update(self) -> GameSceneResult:
        match self.state:
            case 0:
                if self.fade_in.is_playing():
                    self.fade_in.update()
                else:
                    self.timer = 0
                    self.state = 1

            case 1:
                if 0.0 <= self.timer < 30.0 and not is_skip_key():
                    pass  # wait on the logo
                else:
                    self.state = 2

            case 2:
                if self.fade_out.is_playing():
                    self.fade_out.update()
                else:
                    self.state = 3

        self.timer += max(pr.get_frame_time(), 1 / 60)
        return super().update() if self.state < 3 else GameSceneEnd(self)
    
    def draw(self):
        pr.begin_drawing()
        self.title.draw()
        if self.state == 0:
            self.fade_in.draw()
        if self.state in (2, 3):
            self.fade_out.draw()
        pr.end_drawing()

    def _start_play_music(self):
        music = ResourceManager.get_instance().load_music("music")
        if not pr.is_music_stream_playing(music):
            pr.set_music_volume(music, 0.5)
            pr.play_music_stream(music)
