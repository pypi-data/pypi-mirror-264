import numpy as np

from spacerescue.physic.laws import Laws
from spacerescue.physic.mapper import Mapper
from spacerescue.render.camera import Camera


class Universe:
    """interface"""

    def __init__(self, laws: Laws, mapper: Mapper):
        self.laws = laws
        self.mapper = mapper
        self.time = 0
        
    def find_closest_stellar_object(self, position: np.ndarray, filter_func=None):
        raise Exception("Not implemented")

    def update(self, dt: float):
        self.time += dt

    def draw(self, camera: Camera):
        raise Exception("Not implemented")
