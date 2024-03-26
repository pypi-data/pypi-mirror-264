import numpy as np
import pyray as pr

from spacerescue.physic.simulation.world import World
from spacerescue.physic.entity import Entity


class Drone(Entity):

    THRUST = 4000
    MASS = 10
    RADIUS = 10

    def __init__(self, world: World, position: np.ndarray):
        super().__init__(
            universe=world,
            mass=Drone.MASS,
            radius=Drone.RADIUS,
            position=position,
            velocity=np.zeros(3),
        )
        self.world = world
        self.last_score = 0
        self.life = 0

    def get_life(self) -> int:
        return self.life
    
    def get_last_score(self) -> int:
        return self.last_score
    
    def get_sensor_data(self) -> list[int]:
        return self.world.get_sensor_data()
    
    def predict(self, training: bool):
        pass
    
    def thrust(self):
        self.add_force(np.array([0, Drone.THRUST, 0]))
        
    def update(self, dt: float, training: bool):
        self.predict(training)
        self.add_force(self.universe.laws.gravity(self))
        super().update(dt)
        self.universe.mapper.enforce_boundary(self)
        self.last_score = self.world.score
        self.life += 1

    def draw(self):
        eye = np.zeros(3)
        pos = self.to_grid_position()
        pr.draw_circle(int(pos.x), int(pos.y), self.to_grid_size(eye), pr.WHITE)  # type: ignore
