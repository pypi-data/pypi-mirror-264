import numpy as np

from spacerescue.constants import AU
from spacerescue.core.math import lerp, normalize
from spacerescue.core.pyray import is_skip_key
from spacerescue.gameplay.game_scene import GameSceneEnd
from spacerescue.gameplay.scenes.travel_in_space import TravelInSpace
from spacerescue.physic.galaxy.galaxy import ALL_PORTALS
from spacerescue.physic.galaxy.spaceship import Spaceship
from spacerescue.render.effects.star_field import StarField


class TravelToHyperspace(TravelInSpace):

    def enter(self):
        super().enter()
        self.star_field = StarField()
        
        self.start_portal = self.game_state.game_board.context["start_portal"]
        self.rescue_portal = self.game_state.context["clues"]["rescue_portal"]
        self.state = 0
        self.timer = 0
        
        self.spaceship.position = self.start_portal.position + self.start_portal.heading * 2.55 * AU
        self.spaceship.velocity = 0
        self.spaceship.heading = -self.start_portal.heading
        self.spaceship.arrive(self.start_portal, dist = 2.54 * AU)

    def update_simulation(self, dt: float):
        super().update_simulation(dt)
        if self.state in (1, 2, 3):
            self.star_field.update(dt)
        if self.state == 2:
            self.spaceship.position = lerp(self.start_position, self.final_position, self.timer)
            self.spaceship.heading = normalize(self.final_position - self.spaceship.position)
            self.timer += dt * 0.1

    def update(self):
        match self.state:
            case 0:
                if is_skip_key():
                    self.state = 3
                elif self.spaceship.is_arrived():
                    self.spaceship.arrive(self.start_portal, dist = 2.50 * AU)
                    self.state = 1

            case 1:
                if is_skip_key():
                    self.state = 3
                elif self.spaceship.is_arrived():
                    self.start_position = self.spaceship.position.copy()
                    self.final_position = self.rescue_portal.position + self.rescue_portal.heading * 0.5 * AU
                    self.spaceship.velocity = 0
                    self.timer = 0
                    self.state = 2

            case 2:
                if self.timer >= 1.0 or is_skip_key():
                    self.state = 3

            case 3:
                self.spaceship.position = self.rescue_portal.position + self.rescue_portal.heading * 0.5 * AU
                self.spaceship.velocity = 0
                self.spaceship.heading = normalize(self.rescue_portal.parent.position - self.spaceship.position)
                return GameSceneEnd(self)

        return super().update()

    def draw_effect(self):
        if self.state >= 1:
            self.star_field.draw()
