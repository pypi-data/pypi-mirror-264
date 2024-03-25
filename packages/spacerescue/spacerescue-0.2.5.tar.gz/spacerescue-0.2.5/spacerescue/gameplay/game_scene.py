from __future__ import annotations
from typing import Any

from spacerescue.core.types import Monad, Stateable
from spacerescue.gameplay.game_state import GameState
from spacerescue.resources import SCENE_RESOURCES


class GameSceneResult(Monad):
    pass


class GameSceneEnd(GameSceneResult):
    pass


class GameSceneLoop(GameSceneResult):
    def or_else(self, _) -> Any:
        return self.value


class GameSceneNext(GameSceneLoop):
    pass


class GameScene(Stateable):

    def __init__(self, game_state: GameState):
        self.game_state = game_state

    def enter(self) -> GameScene:
        self.game_state.stacked_scenes.append(self)
        return self

    def leave(self) -> GameScene:
        self.game_state.stacked_scenes.pop()
        SCENE_RESOURCES.unload_all()
        return self

    def update(self) -> GameSceneResult:
        return GameSceneLoop(self)  # type: ignore

    def draw(self):
        pass

class GameSubScene(GameScene):
    def __init__(self, scene: GameScene):
        super().__init__(scene.game_state)
        self.scene = scene
        
    def leave(self) -> GameScene:
        self.game_state.stacked_scenes.pop()
        return self