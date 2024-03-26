from __future__ import annotations

from spacerescue.core.types import Monad, Option, Stateable
from spacerescue.gameplay.game_board import GameBoard
from spacerescue.resources import STATE_RESOURCES


class GameResult(Monad):
    pass


class GameEnd(GameResult):
    pass


class GameLoop(GameResult):
    def map(self, _) -> Monad:
        return self


class GameState(Stateable):

    def __init__(self, game_board: GameBoard, context: dict = {}):
        self.game_board = game_board
        self.context = context
        self.stacked_scenes: list[Stateable] = []
        self.last_scene_idx = 0

    def enter(self) -> GameState:
        return self

    def leave(self) -> GameState:
        STATE_RESOURCES.unload_all()
        return self

    def update(self) -> GameResult:
        return (
            Option.maybe(self.stacked_scenes)
            .map(self._update_scene)
            .flatmap_or(lambda _: GameLoop(self), lambda _: GameEnd(self))
        )  # type: ignore

    def draw(self):
        # Skip one frame when a scene changes:
        # 1. the previous scene may be in an invalid state (as it is freeing its resources)
        # 2. to give a chance to render effects to grab the screen
        curr_scene_idx = len(self.stacked_scenes)
        skip_frame = self.last_scene_idx != curr_scene_idx
        if not skip_frame:
            Option.maybe(self.stacked_scenes).flatmap(self._draw_scene)
        self.last_scene_idx = curr_scene_idx

    #
    # Privates
    #

    def _update_scene(self, x):
        x[-1].update().or_else(lambda y: y.leave())
        return x

    def _draw_scene(self, x):
        x[-1].draw()
        return x
