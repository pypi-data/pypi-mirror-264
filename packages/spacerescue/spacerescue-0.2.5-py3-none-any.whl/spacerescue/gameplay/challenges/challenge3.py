import os
import yaml
import numpy as np

from spacerescue.gameplay.challenge import (
    ChallengeError,
    QuizzChallenge,
)
from spacerescue.gameplay.game_scene import GameScene
from spacerescue.gameplay.scenes.quizz_console import QuizzConsole
from spacerescue.resources import SCENE_RESOURCES


class Challenge3(QuizzChallenge):

    NUMBER_OF_QUESTIONS = 10

    def __init__(self, scene: GameScene):
        challenge = SCENE_RESOURCES.load_yaml("challenge3")
        title = challenge["title"]
        mission = challenge["mission"].format(**challenge)
        super().__init__(2, title, mission, scene)

    def get_scene(self):
        self._generate_quizz()
        return QuizzConsole(self.scene, self)

    def check_answer(self):
        if not os.path.exists("quizz.yml"):
            raise ChallengeError("Could not found 'quizz.yml'")

        pool_of_questions = SCENE_RESOURCES.load_res_yaml("questions")

        with open("quizz.yml", "r") as f:
            questions = yaml.safe_load(f)
            
        def check_question(q1, q2):
            same_question = q1["question"] == q2["question"]
            if same_question and q1["choices"] != q2["choices"]:
                raise ChallengeError(f"{q1['question']}: wrong answer")
            return same_question
                
        for q1 in questions:
            question_found = False
            for q2 in pool_of_questions:
                question_found |= check_question(q1, q2)
            if not question_found:
                raise ChallengeError(f"{q1['question']}: not found")
            
        self.on_good_answer()

    def on_good_answer(self):
        self.context["unlocked"][2] = True
        self.unlocked = True

    def _generate_quizz(self):
        if os.path.exists("quizz.yml"):
            return

        pool_of_questions = SCENE_RESOURCES.load_res_yaml("questions")

        ids = np.arange(len(pool_of_questions))
        np.random.shuffle(ids)

        questions = []
        for i in range(Challenge3.NUMBER_OF_QUESTIONS):
            random_question = pool_of_questions[ids[i]]
 
            question = {}
            question["question"] = random_question["question"]
            question["choices"] = {}
            for choice in random_question["choices"].keys():
                question["choices"][choice] = False

            questions.append(question)

        with open("quizz.yml", "w") as f:
            yaml.safe_dump(questions, f, sort_keys=False)
