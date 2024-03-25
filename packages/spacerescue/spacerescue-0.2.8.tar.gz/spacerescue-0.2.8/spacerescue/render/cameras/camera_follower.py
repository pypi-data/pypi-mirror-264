import numpy as np
import pyray as pr

from spacerescue.constants import CAMERA_FOV, DEFAULT_UP
from spacerescue.render.camera import Camera
from spacerescue.physic.entity import Entity
from spacerescue.core.math import EPSILON, ndarray_to_vector3


class CameraFollower(Camera):
    
    K = 1e3  # N

    def __init__(self, entity: Entity, length: float):
        self.entity = entity
        self.length = length
        self.velocity = pr.vector3_zero()
        
        camera_target = self.entity.universe.mapper.to_grid_position(self.entity)
        camera_position = pr.vector3_add(camera_target, ndarray_to_vector3(-self.entity.heading * self.length))
        self.camera = pr.Camera3D(
            camera_position,
            camera_target,
            pr.Vector3(*DEFAULT_UP),
            CAMERA_FOV / 2,
            pr.CameraProjection.CAMERA_PERSPECTIVE,
        )

        super().__init__(self.entity.position, self.camera)

    def update(self, dt: float):
        camera_target = self.entity.universe.mapper.to_grid_position(self.entity)
        # camera_position = pr.vector3_add(camera_target, ndarray_to_vector3(-self.entity.heading * self.length))
        
        force = self._get_tension_force(dt)
        force = pr.vector3_add(
            force, pr.vector3_scale(self.velocity, -1.0 / (dt + EPSILON))
        )
        self.velocity = pr.vector3_add(self.velocity, pr.vector3_scale(force, dt / 1.0))
        camera_position = pr.vector3_add(
            self.camera.position, pr.vector3_scale(self.velocity, dt)
        )
        
        self.camera.target = camera_target
        self.camera.position = camera_position
        self.position = self.entity.position.copy()
        super().update(dt)
        
    def _get_tension_force(self, dt: float):
        v = pr.vector3_subtract(self.camera.position, self.camera.target)
        l = pr.vector3_length(v) - self.length
        return pr.vector3_scale(pr.vector3_normalize(v), -CameraFollower.K * l)
