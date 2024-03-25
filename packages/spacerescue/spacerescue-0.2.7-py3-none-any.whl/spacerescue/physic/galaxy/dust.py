import pyray as pr
import numpy as np

from spacerescue.constants import PARSEC
from spacerescue.resources.resource_manager import ResourceManager
from spacerescue.render.camera import Camera
from spacerescue.physic.universe import Universe
from spacerescue.physic.entity import Entity
from spacerescue.physic.galaxy.star import Star


class Dust(Entity):

    MASS = 1e-5 # kg
    RADIUS = 15 * PARSEC
    COLOR = (96, 0, 64, 32)

    def __init__(
        self, universe: Universe, position: np.ndarray, star: Star
    ):
        super().__init__(
            universe=universe,
            mass=Dust.MASS,
            radius=Dust.RADIUS,
            position=position + np.random.rand(3),
            parent=star,
        )
        self.color = Dust.COLOR
        self.rotation = 180 * np.random.rand()
        self.texture = ResourceManager.get_instance().load_texture("particule")

    def draw(self, camera: Camera):
        if self.get_lod(camera.position) == 0:
            mat_view = pr.get_camera_matrix(camera.camera)
            source = pr.Rectangle(0.0, 0.0, self.texture.width, self.texture.height)
            position = self.to_grid_position()
            up = pr.Vector3(mat_view.m1, mat_view.m5, mat_view.m9)
            size = self.universe.mapper.real_to_grid_v(self.radius * 2)
            pr.draw_billboard_pro(
                camera.camera,
                self.texture,
                source,
                position,
                up,
                pr.Vector2(size, size),
                pr.vector2_zero(),
                self.rotation,
                self.color, # type: ignore
            )