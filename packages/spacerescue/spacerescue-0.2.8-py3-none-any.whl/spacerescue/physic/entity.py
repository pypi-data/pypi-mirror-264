from __future__ import annotations

import pyray as pr
import numpy as np


from spacerescue.constants import (
    DEFAULT_HEADING,
    DEFAULT_UP,
)
from spacerescue.core.math import normalize
from spacerescue.physic.universe import Universe
from spacerescue.render.camera import Camera


class Entity:

    def __init__(
        self,
        universe: Universe,
        mass: float,
        radius: float,
        position: np.ndarray,
        velocity: np.ndarray | None = None,
        spin_axis: np.ndarray | None = None,
        parent: Entity | None = None,
    ):
        self.universe = universe
        self.mass = mass
        self.radius = radius
        self.position = position
        self.velocity = velocity if velocity is not None else np.zeros(3)
        self.spin_axis = spin_axis if spin_axis is not None else np.array(DEFAULT_UP)
        self.heading = (
            normalize(velocity)
            if velocity is not None and np.linalg.norm(self.velocity) != 0.0
            else np.array(DEFAULT_HEADING)
        )
        self.parent = parent
        self.internal_clock = 0
        self._forces = np.zeros(3)

    def update(self, dt: float):
        self.apply_forces(dt)
        self.clear_force()
        self.internal_clock += dt

    def draw(self, camera: Camera):
        pr.draw_sphere(self.to_grid_position(), self.to_grid_size(camera.position), pr.WHITE)  # type: ignore

    def clear_force(self):
        self._forces = np.zeros(3)

    def add_force(self, force: np.ndarray):
        self._forces += force

    def apply_forces(self, dt: float):
        self.velocity += self._forces * dt / self.mass
        self.position += self.velocity * dt

    def get_lod(self, eye: np.ndarray):
        return self.universe.mapper.get_lod(eye, self)

    def to_grid_position(self) -> pr.Vector3:
        return self.universe.mapper.to_grid_position(self)

    def to_grid_size(self, eye: np.ndarray) -> float:
        return self.universe.mapper.to_grid_size(eye, self)

