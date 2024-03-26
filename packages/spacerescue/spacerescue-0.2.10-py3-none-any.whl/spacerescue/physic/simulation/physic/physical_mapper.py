import pyray as pr
import numpy as np

from spacerescue.physic.entity import Entity
from spacerescue.physic.mapper import Mapper
from spacerescue.core.math import clamp, ndarray_to_vector3, vector3_to_ndarray


class PhysicalMapper(Mapper):

    def __init__(self, world):
        self.world = world
        self.center = np.array(
            [
                world.bound.x + world.bound.width * 0.5,
                world.bound.y + world.bound.height,
                0,
            ]
        )

    def real_to_grid_v(self, x: float) -> float:
        return x

    def grid_to_real_v(self, x: float) -> float:
        return x

    def real_to_grid(self, x: np.ndarray) -> pr.Vector3:
        return ndarray_to_vector3(self.center - x * np.array([-1.0, 1.0, 0.0]))

    def grid_to_real(self, x: pr.Vector3) -> np.ndarray:
        return (self.center - vector3_to_ndarray(x)) * np.array([-1.0, 1.0, 0.0])

    def get_lod(self, eye: np.ndarray, target: Entity) -> int:
        return 0

    def to_grid_size(self, eye: np.ndarray, target: Entity) -> float:
        return self.real_to_grid_v(target.radius)

    def to_grid_position(self, target: Entity) -> pr.Vector3:
        return self.real_to_grid(target.position)

    def enforce_boundary(self, target: Entity):
        pos = self.real_to_grid(target.position)
        rad = self.real_to_grid_v(target.radius)
        pos.x = clamp(
            pos.x,
            self.world.bound.x + rad,
            self.world.bound.x + self.world.bound.width - rad - 1,
        )
        pos.y = clamp(
            pos.y,
            self.world.bound.y + rad,
            self.world.bound.y + self.world.bound.height - rad - 1,
        )
        target.position = self.grid_to_real(pos)
