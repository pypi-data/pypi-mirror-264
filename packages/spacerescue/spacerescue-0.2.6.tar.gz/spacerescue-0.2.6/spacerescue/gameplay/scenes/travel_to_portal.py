from spacerescue.constants import (
    AU,
)

from spacerescue.core.pyray import is_skip_key
from spacerescue.gameplay.game_scene import GameSceneEnd
from spacerescue.gameplay.scenes.travel_in_space import TravelInSpace
from spacerescue.physic.galaxy.hyperspace_portal import HyperspacePortal


class TravelToPortal(TravelInSpace):
    
    def enter(self):
        super().enter()
        self.start_portal: HyperspacePortal = self.game_state.game_board.context["start_portal"]
        self.spaceship.arrive(self.start_portal, dist = 2.55 * AU)
 
    def update(self):
        if self.spaceship.is_arrived() or is_skip_key():
            self.spaceship.position = self.start_portal.position + self.start_portal.heading * 2.55 * AU
            self.spaceship.velocity = 0
            self.spaceship.heading = -self.start_portal.heading
            return GameSceneEnd(self)
        else:
            return super().update()
           