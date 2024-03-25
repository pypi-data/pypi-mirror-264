import numpy as np

from spacerescue.constants import AU, GAME_SEED
from spacerescue.core.math import normalize, perpendicular, rotate_by_axis_angle
from spacerescue.gameplay.game_state import GameState
from spacerescue.physic.galaxy.spaceship import Spaceship

class MainStateDelegate(GameState):
    def enter(self) -> GameState:
        self.context["next_state"] = "main_state"
        self.context["unlocked"] = [False, False, False]
        self.context["played"] = [False, False, False]
        self.context["spaceship"] = self._build_spaceship()
        self.context["clues"] = {}
        return self
        
    def _build_spaceship(self):
        galaxy = self.game_board.context["galaxy"]
        portal = self.game_board.context["start_portal"]
        star = portal.parent
        off = normalize(
            rotate_by_axis_angle(
                perpendicular(star.spin_axis),
                star.spin_axis,
                2 * np.pi * np.random.rand(),
            )
        )
        pos = star.position + off * 0.5 * AU
        head = -off
        return Spaceship(galaxy, pos, head)