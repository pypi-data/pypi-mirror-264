import pyray as pr

from spacerescue.constants import (
    DT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from spacerescue.gameplay.game_scene import GameSubScene
from spacerescue.physic.galaxy.galaxy import Galaxy
from spacerescue.physic.galaxy.spaceship import Spaceship
from spacerescue.render.cameras.camera_entity import CameraEntity
from spacerescue.render.effects.fade_scr import FadeScr
from spacerescue.render.cameras.camera_follower import CameraFollower
from spacerescue.render.widgets.screen import Screen
from spacerescue.resources import SCENE_RESOURCES


class TravelInSpace(GameSubScene):

    SIMULATION_SPEED = 100

    def enter(self):
        super().enter()
        self.fade_in = FadeScr(0.5)

        # Setup scene and camera

        self.galaxy: Galaxy = self.game_state.game_board.context["galaxy"]
        self.spaceship: Spaceship = self.game_state.context["spaceship"]
        self.camera = CameraEntity(self.spaceship)
        self.first_person = True

        # Cockpit image

        self.surface_cockpit = Screen("widget", "cockpit")

        # Bloom effect

        self.surface_bloom = pr.load_render_texture(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.shader_bloom = SCENE_RESOURCES.load_shader("shader_bloom")

    def leave(self):
        pr.unload_render_texture(self.surface_bloom)
        del self.camera
        super().leave()

    def update_simulation(self, dt: float):
        for i in range(TravelInSpace.SIMULATION_SPEED):
            self.galaxy.update(dt * DT, self.camera)
            self.spaceship.update(dt * DT)

    def update_input(self):
        if pr.is_key_pressed(pr.KeyboardKey.KEY_F1):
            self.first_person = not self.first_person
            if self.first_person:
                self.camera = CameraEntity(self.spaceship)
            else:
                self.camera = CameraFollower(self.spaceship, 0.2)

    def update(self):
        dt = pr.get_frame_time()
        self.fade_in.update()
        self.camera.update(dt)
        self.update_simulation(dt)
        self.update_input()
        return super().update()

    def draw(self):
        pr.begin_texture_mode(self.surface_bloom)
        pr.clear_background(pr.BLACK)  # type: ignore
        pr.begin_mode_3d(self.camera.camera)
        self.galaxy.draw(self.camera)
        if not self.first_person:
            self.spaceship.draw(self.camera)
        pr.end_mode_3d()
        self.draw_effect()
        pr.end_texture_mode()

        pr.begin_drawing()
        pr.begin_shader_mode(self.shader_bloom)
        pr.draw_texture_rec(
            self.surface_bloom.texture,
            pr.Rectangle(
                0,
                0,
                self.surface_bloom.texture.width,
                -self.surface_bloom.texture.height,
            ),
            pr.vector2_zero(),
            pr.WHITE,  # type: ignore
        )
        pr.end_shader_mode()
        if self.first_person:
            self.surface_cockpit.draw()
        self.fade_in.draw()
        pr.end_drawing()
        
    def draw_effect(self):
        pass
