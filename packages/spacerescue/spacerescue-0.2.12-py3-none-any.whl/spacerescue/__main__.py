import os
import logging
import fire
import fire.core
import numpy as np
import pyray as pr

from spacerescue.constants import (
    APP_NAME,
    FRAMES_PER_SECOND,
    GAME_SEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from spacerescue.core.pyray import window_should_close
from spacerescue.gameplay.databases.database import Database
from spacerescue.gameplay.game_states.game_states import LogoState
from spacerescue.sketch import Sketch


def main(game_seed: int = GAME_SEED, reset_database: bool = False):
    """ SpaceRescue
    """
    np.random.seed(game_seed)
    Database.set_options(
        reset_database = reset_database or not os.path.exists("resources/data/spacerescue.db")
    )
    Database.create_database()

    pr.set_config_flags(pr.ConfigFlags.FLAG_MSAA_4X_HINT)
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, APP_NAME)
    pr.set_target_fps(FRAMES_PER_SECOND)
    pr.init_audio_device()

    sketch = Sketch()
    sketch.begin(LogoState(sketch))
    while not window_should_close():
        sketch.update()
        sketch.draw()
    sketch.destroy()

    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.DEBUG)
    fire.core.Display = lambda lines, out: print(*lines, file=out)
    fire.Fire(main)
