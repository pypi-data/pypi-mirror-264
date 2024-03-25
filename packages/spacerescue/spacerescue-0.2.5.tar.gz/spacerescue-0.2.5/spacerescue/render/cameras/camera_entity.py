import pyray as pr

from spacerescue.constants import CAMERA_FOV
from spacerescue.render.camera import Camera
from spacerescue.physic.entity import Entity
from spacerescue.core.math import ndarray_to_vector3, vector3_to_ndarray


class CameraEntity(Camera):

    def __init__(self, entity: Entity):
        self.entity = entity

        camera_position = self.entity.universe.mapper.to_grid_position(self.entity)
        camera_target = pr.vector3_add(
            camera_position, ndarray_to_vector3(entity.heading)
        )
        self.camera = pr.Camera3D(
            camera_position,
            camera_target,
            ndarray_to_vector3(entity.spin_axis),
            CAMERA_FOV / 2,
            pr.CameraProjection.CAMERA_PERSPECTIVE,
        )

        super().__init__(self.entity.position, self.camera)

    def update(self, dt: float):
        camera_position = self.entity.universe.mapper.to_grid_position(self.entity)
        camera_target = pr.vector3_add(
            camera_position, ndarray_to_vector3(self.entity.heading)
        )
        self.camera.position = camera_position
        self.camera.target = camera_target
        self.camera.up = ndarray_to_vector3(self.entity.spin_axis)
        
        self.position = self.entity.position.copy()
        super().update(dt)
