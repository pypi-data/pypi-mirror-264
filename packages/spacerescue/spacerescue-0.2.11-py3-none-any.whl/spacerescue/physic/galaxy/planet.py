import pyray as pr
import numpy as np

from spacerescue.tools.name_generator import NameGenerator
from spacerescue.resources.resource_manager import ResourceManager
from spacerescue.render.camera import Camera
from spacerescue.physic.universe import Universe
from spacerescue.physic.entity import Entity
from spacerescue.physic.galaxy.star import Star


class Planet(Entity):
    
    ANGULAR_VELOCITY = 7.29e-7 # r⋅s−1   # earth like
    
    def __init__(
        self,
        universe: Universe,
        mass: float,
        radius: float,
        position: np.ndarray,
        velocity: np.ndarray,
        model: str,
        star: Star,
        is_habitable: bool
    ):
        super().__init__(
            universe=universe,
            mass=mass,
            radius=radius,
            position=position,
            velocity=velocity,
            spin_axis=star.spin_axis,
            parent=star,
        )
        self.parent = star
        self.name = NameGenerator.get_instance().generate_planet_name()
        self.is_habitable = is_habitable
        self.angle = np.random.random() * np.pi
        self.angular_velocity = Planet.ANGULAR_VELOCITY
        self.model = ResourceManager.get_instance().load_model(model)
        self.model.materials[0].shader = ResourceManager.get_instance().load_shader("shader_lighting")

    def update(self, dt: float):
        self.angle += self.angular_velocity * dt
        if self.parent is not None:
            force = self.universe.laws.attraction(self.parent, self)
            self.add_force(force)
            self.parent.add_force(-force)
        super().update(dt)

    def draw(self, camera: Camera):
        if self.get_lod(camera.position) > 0:
            self.model.transform = pr.matrix_rotate(pr.Vector3(*self.spin_axis), self.angle)
            pr.draw_model(self.model, self.to_grid_position(), self.to_grid_size(camera.position), pr.WHITE)  # type: ignore
