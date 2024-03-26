import pyray as pr
import numpy as np

from spacerescue.resources.resource_manager import ResourceManager
from spacerescue.render.camera import Camera
from spacerescue.physic.universe import Universe
from spacerescue.physic.entity import Entity


class Asteroid(Entity):

    MASS = 1e14  # kg
    ANGULAR_VELOCITY = 1  # r⋅s−1
    RADIUS = 1e6  # m

    def __init__(self, universe: Universe, position: np.ndarray):
        super().__init__(
            universe=universe,
            mass=Asteroid.MASS,
            radius=Asteroid.RADIUS,
            position=position,
        )
        self.angle = np.random.random() * np.pi
        self.angular_velocity = Asteroid.ANGULAR_VELOCITY
        self.model = ResourceManager.get_instance().load_model("asteroid")
        self.model.materials[0].shader = ResourceManager.get_instance().load_shader(
            "shader_lighting"
        )

    def update(self, dt):
        self.angle += self.angular_velocity * dt
        super().update(dt)

    def draw(self, camera: Camera):
        if self.get_lod(camera.position) > 0:
            self.model.transform = pr.matrix_rotate_xyz(
                pr.Vector3(*(self.angle, self.angle, self.angle))
            )
            pr.draw_model(self.model, self.to_grid_position(), self.to_grid_size(camera.position), pr.WHITE)  # type: ignore
