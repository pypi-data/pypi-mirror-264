from spacerescue.core.pyray import window_request_close
from spacerescue.gameplay.game_state import GameState
from spacerescue.gameplay.game_states.main_state import MainStateDelegate
from spacerescue.gameplay.scenes.computer_room import ComputerRoom
from spacerescue.gameplay.scenes.game_over import GameOver
from spacerescue.gameplay.scenes.logo_scene import Logo
from spacerescue.gameplay.scenes.menu_scene import Menu
from spacerescue.gameplay.scenes.title import Title


class LogoState(GameState):
    def enter(self) -> GameState:
        super().enter()
        Logo(self).enter()
        return self

    def leave(self) -> GameState:
        super().leave()
        return TitleState(self.game_board)


class TitleState(GameState):
    def enter(self) -> GameState:
        super().enter()
        Title(self).enter()
        return self

    def leave(self) -> GameState:
        super().leave()
        return MenuState(self.game_board)


class MenuState(GameState):
    def enter(self) -> GameState:
        super().enter()
        Menu(self).enter()
        return self

    def leave(self) -> GameState:
        super().leave()
        if self.context.get("next_state") == "main_state":
            return MainState(self.game_board)
        elif self.context.get("next_state") == "exit_state":
            return ExitState(self.game_board)
        else:
            return self


class MainState(MainStateDelegate):
    def enter(self) -> GameState:
        super().enter()
        ComputerRoom(self).enter()
        return self

    def leave(self) -> GameState:
        super().leave()
        if self.context.get("next_state") == "menu_state":
            return MenuState(self.game_board)
        elif self.context.get("next_state") == "game_over_state":
            return GameOverState(self.game_board, self.context)
        else:
            return self


class GameOverState(GameState):
    def enter(self) -> GameState:
        super().enter()
        player_rescue_planet = self.context.get("clues", {})["rescue_planet"]
        scenario_rescue_planet = self.game_board.context.get("rescue_planet")
        success = player_rescue_planet == scenario_rescue_planet
        GameOver(self, success).enter()
        return self

    def leave(self) -> GameState:
        super().leave()
        return MenuState(self.game_board)


class ExitState(GameState):
    def enter(self) -> GameState:
        super().enter()
        window_request_close()
        return self
