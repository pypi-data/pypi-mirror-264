import numpy as np

from spacerescue.constants import G_SMALL
from spacerescue.physic.entity import Entity
from spacerescue.physic.laws import Laws


class PhysicalLaws(Laws):

    MAX_FORCE = 0.1
    
    def __init__(self, galaxy):
        self.galaxy = galaxy

    def gravity(self, e: Entity) -> np.ndarray:
        return e.mass * np.array([0, -G_SMALL, 0])
