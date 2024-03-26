import pyray as pr

from spacerescue.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from spacerescue.gameplay.databases.database import Database
from spacerescue.gameplay.game_scene import GameScene, GameSceneEnd, GameSceneResult
from spacerescue.render.effects.fade_inout import FadeInOut
from spacerescue.resources import SCENE_RESOURCES


class Logo(GameScene):

    def enter(self):
        super().enter()
        self.fade_in = FadeInOut(0, 255, 1.0, pr.Color(*pr.WHITE))
        self.fade_out = FadeInOut(255, 0, 1.0, pr.Color(*pr.WHITE))
        self.logo = SCENE_RESOURCES.load_texture("logo")
        self.boot_progress = 0
        self.state = 0
        self.timer = 0
       
    def update(self) -> GameSceneResult:
        match self.state:
            case 0:
                if self.fade_in.is_playing():
                    self.fade_in.update()
                else:
                    self.timer = 0
                    self.state = 1
                    
            case 1:
                self._boot()
                if self.boot_progress >= 1 and self.timer > 2:
                    self.state = 2
                    
            case 2:
                if self.fade_out.is_playing():
                    self.fade_out.update()
                else:
                    self.fade_in.reset()
                    self.fade_out.reset()
                    self.state = 3
                    
            case 3:
                if self.fade_in.is_playing():
                    self.fade_in.update()
                else:
                    self.timer = 0
                    self.state = 4
                    
            case 4:
                self._boot()
                if self.boot_progress >= 4 and self.timer > 2:
                    self.state = 5

            case 5:
                if self.fade_out.is_playing():
                    self.fade_out.update()
                else:
                    self.state = 6
                    
        self.timer += max(pr.get_frame_time(), 1/60)
        return super().update() if self.state < 6 else GameSceneEnd(self)
                
            
    def draw(self):
        pr.begin_drawing()
        pr.clear_background(pr.WHITE) # type: ignore
        
        if self.state in (0, 1, 2):
            pos_x = int(SCREEN_WIDTH / 2 - self.logo.width / 2)
            pos_y = int(SCREEN_HEIGHT / 2 - self.logo.height / 2)
            pr.draw_texture(self.logo, pos_x, pos_y, pr.WHITE) # type: ignore
            
        if self.state in (3, 4, 5):
            hw = pr.measure_text("present", 20) / 2
            pos_x = int(SCREEN_WIDTH / 2 - hw)
            pos_y = int(SCREEN_HEIGHT / 2 - hw)
            pr.draw_text("present", pos_x, pos_y, 20, pr.BLACK) # type: ignore
        
        if self.state in (0, 2, 3, 5):
            self.fade_in.draw()
            self.fade_out.draw()
        
        pr.end_drawing()
        
    def _boot(self):
        match self.boot_progress:
            case 1:
                Database.create_mldb_table(self.game_state.game_board.context["rescue_planet"])
            case 2:
                Database.create_sodb_table(self.game_state.game_board.context["galaxy"])
            case 3:
                Database.create_htdb_table(self.game_state.game_board.context["galaxy"])
            case 4:
                Database.create_iddb_table()
        self.boot_progress += 1
