from spacerescue.gameplay.game_scene import GameScene
from spacerescue.gameplay.challenge import ChallengeError, CodeChallenge
from spacerescue.gameplay.scenes.simulator_console import SimulatorConsole
from spacerescue.resources import SCENE_RESOURCES


class Challenge2(CodeChallenge):

    def __init__(self, scene: GameScene):
        challenge = SCENE_RESOURCES.load_yaml("challenge2")
        title = challenge["title"]
        mission = challenge["mission"].format(**challenge)
        super().__init__(1, title, mission, scene)

    def get_scene(self):
        return SimulatorConsole(self.scene, self)

    def check_answer(self, answer):
        if answer is None or answer.get_drones is None or answer.fit is None:
            raise ChallengeError("Answer do not match the specification of a Drone.")

    def on_good_answer(self):
        self.context["unlocked"][1] = True
        self.unlocked = True
