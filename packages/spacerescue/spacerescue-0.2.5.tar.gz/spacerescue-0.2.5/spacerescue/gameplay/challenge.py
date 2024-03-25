from __future__ import annotations
from multiprocessing import Process

import logging
import traceback
import duckdb

from spacerescue.core.types import Monad
from spacerescue.gameplay.game_scene import GameScene
from spacerescue.tools.dynamic_code import DynamicCode
from spacerescue.tools.util import secret_token


class ChallengeError(ValueError):
    pass


class ChallengeAnswer(Monad):
    pass


class ChallengeGoodAnswer(ChallengeAnswer):

    def __init__(self, result=None):
        self.result = result

    def or_else(self, func):
        return self.result

    def map(self, func) -> ChallengeAnswer:
        return ChallengeGoodAnswer(func(self.result))


class ChallengeBadAnswer(ChallengeAnswer):

    def __init__(self, exception: Exception | None = None):
        self.exception = exception

    def or_else(self, func):
        return func(self.exception)

    def map(self, func) -> ChallengeAnswer:
        return self


class Challenge:

    def __init__(self, id: int, description: str, scene: GameScene):
        self.token = self._generate_token(id)
        self.description = description
        self.scene = scene
        self.context = self.scene.game_state.context
        self.unlocked = False

    def get_scene(self):
        raise NotImplementedError

    def check_answer(self, *args):
        raise NotImplementedError

    def on_good_answer(self):
        raise NotImplementedError

    def _generate_token(self, id: int):
        con = duckdb.connect("resources/data/spacerescue.db")
        result = con.sql(f"SELECT token FROM IDDB WHERE id={id}").fetchone()
        assert result is not None
        token = result[0]
        con.close()
        return token


class CodeChallenge(Challenge):

    def __init__(self, id: int, description: str, mission: str, scene: GameScene):
        super().__init__(id, description, scene)
        self.mission = mission
        self.code = DynamicCode("brain")

    def get_answer(self):
        return self.code.get_execute_code_result()

    def validate(self) -> Process:
        return self.code.validate_code()

    def commit(self) -> ChallengeAnswer:
        if self.code.get_validate_code_result().returncode == 0:
            try:
                answer = self.check_answer(
                    self.code.execute_code(self.token, self.context["clues"])
                )
                return ChallengeGoodAnswer(answer)
            except Exception as x:
                logging.error(traceback.format_exc())
                return ChallengeBadAnswer(x)
        else:
            return ChallengeBadAnswer(
                Exception("Test Coverage failed to meet the criteria")
            )


class QuizzChallenge(Challenge):

    def __init__(self, id: int, description: str, mission: str, scene: GameScene):
        super().__init__(id, description, scene)
        self.mission = mission

    def commit(self) -> ChallengeAnswer:
        try:
            answer = self.check_answer()
            return ChallengeGoodAnswer(answer)
        except Exception as x:
            logging.error(traceback.format_exc())
            return ChallengeBadAnswer(x)
