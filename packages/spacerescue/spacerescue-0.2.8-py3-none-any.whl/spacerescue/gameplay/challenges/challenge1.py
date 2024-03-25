import numpy as np

from spacerescue.physic.galaxy.galaxy import (
    ALL_STAR_SYSTEM_HABITABLE_PLANETS,
    ALL_STAR_SYSTEM_PORTALS,
)
from spacerescue.resources import SCENE_RESOURCES
from spacerescue.gameplay.challenge import ChallengeError, CodeChallenge
from spacerescue.gameplay.game_scene import GameScene
from spacerescue.gameplay.scenes.computer_console import ComputerConsole
from spacerescue.physic.galaxy.hyperspace_portal import HyperspacePortal
from spacerescue.physic.galaxy.planet import Planet
from spacerescue.physic.galaxy.star import Star


class Challenge1(CodeChallenge):

    def __init__(self, scene: GameScene):
        challenge = SCENE_RESOURCES.load_yaml("challenge1")
        title = challenge["title"]
        mission = challenge["mission"].format(**challenge)
        super().__init__(0, title, mission, scene)
        self.galaxy = self.scene.game_state.game_board.context["galaxy"]
        self.rescue_planet = self.scene.game_state.game_board.context["rescue_planet"]
        self.errors = challenge["errors"]

    def get_scene(self):
        return ComputerConsole(self.scene, self)
    
    def check_answer(self, some_position):
        if (
            some_position is None
            or not isinstance(some_position, np.ndarray)
            or not some_position.shape[0] == 3
        ):
            raise ChallengeError(self.errors[0])

        planet = self.galaxy.find_closest_stellar_object(
            some_position, ALL_STAR_SYSTEM_HABITABLE_PLANETS
        )
        if (
            planet is None
            or not isinstance(planet, Planet)
            or not self.rescue_planet.name == planet.name
        ):
            raise ChallengeError(self.errors[1])

        star = planet.parent
        if (
            star is None
            or not isinstance(star, Star)
            or self.rescue_planet.parent is not star
        ):
            raise ChallengeError(self.errors[2])

        portal = next(
            self.galaxy.filter_stellar_objects(ALL_STAR_SYSTEM_PORTALS(star)),
            None,
        )
        if (
            portal is None
            or not isinstance(portal, HyperspacePortal)
            or portal.parent is not star
        ):
            raise ChallengeError(self.errors[3])

        self.context["clues"]["rescue_planet"] = planet
        self.context["clues"]["rescue_star"] = star
        self.context["clues"]["rescue_portal"] = portal
        self.on_good_answer()
        
    def on_good_answer(self):
        self.context["unlocked"][0] = True
        self.unlocked = True
