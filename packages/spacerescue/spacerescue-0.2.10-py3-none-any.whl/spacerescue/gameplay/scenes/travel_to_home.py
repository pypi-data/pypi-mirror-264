import numpy as np
from spacerescue.constants import (
    AU,
)
from spacerescue.core.math import lerp, normalize
from spacerescue.gameplay.game_scene import GameSceneEnd
from spacerescue.gameplay.scenes.travel_in_space import TravelInSpace
from spacerescue.physic.galaxy.galaxy import (
    ALL_STAR_SYSTEM_HABITABLE_PLANETS,
    ALL_STARS,
)
from spacerescue.core.pyray import is_skip_key


class TravelToHome(TravelInSpace):

    def enter(self):
        super().enter()
        self.planet = self.game_state.context["clues"]["rescue_planet"]
        self.rescue_portal = self.game_state.context["clues"]["rescue_portal"]
        
        self.spaceship.position = self.rescue_portal.position + self.rescue_portal.heading * 0.5 * AU
        self.spaceship.velocity = 0
        self.spaceship.heading = normalize(self.rescue_portal.parent.position - self.spaceship.position)
        self.spaceship.heading_speed = 2e-5
        self.spaceship.arrive(self.planet, dist = 0.08 * AU, pulse_speed = 1.8e5)
        
        
    def update(self):
        if self.spaceship.is_arrived() or is_skip_key():
            return GameSceneEnd(self)
        else:
            return super().update()
