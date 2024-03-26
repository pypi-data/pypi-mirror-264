import logging
import numpy as np
import pyray as pr

from spacerescue.gameplay.game_board import GameBoard
from spacerescue.physic.galaxy.galaxy import ALL_PORTALS, ALL_STAR_SYSTEM_HABITABLE_PLANETS, Galaxy
from spacerescue.resources import GLOBAL_RESOURCES


class Sketch(GameBoard):
    
    def __init__(self):
        super().__init__()
        self.music = GLOBAL_RESOURCES.load_music("music")
        self._build_galaxy()
        self._build_scenario()
        
    def destroy(self):
        self.end()

    def update(self):
        if pr.is_music_stream_playing(self.music):
            pr.update_music_stream(self.music)
        super().update()
        
    def _build_galaxy(self):
        logging.info("INFO: CONTEXT: Generate galaxy ...")
        self.context["galaxy"] = Galaxy()

    def _build_scenario(self):
        logging.info("INFO: CONTEXT: Generate scenario ...")
        scenario_is_ok = False
        while not scenario_is_ok:
            self.context["start_portal"] = np.random.choice(
                list(self.context["galaxy"].filter_stellar_objects(ALL_PORTALS))
            )
            self.context["rescue_portal"] = np.random.choice(
                list(self.context["galaxy"].filter_stellar_objects(ALL_PORTALS))
            )
            self.context["rescue_planet"] = np.random.choice(
                list(
                    self.context["galaxy"].filter_stellar_objects(
                        ALL_STAR_SYSTEM_HABITABLE_PLANETS(self.context["rescue_portal"].parent)
                    )
                )
            )
            scenario_is_ok = self.context["start_portal"].name != self.context["rescue_portal"].name

        logging.info("INFO: CONTEXT: Generate challenges ...")
        