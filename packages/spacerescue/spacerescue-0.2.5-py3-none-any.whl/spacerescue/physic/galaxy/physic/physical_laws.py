import numpy as np

from spacerescue.constants import G
from spacerescue.physic.entity import Entity
from spacerescue.physic.laws import Laws
from spacerescue.core.math import limit, normalize


class PhysicalLaws(Laws):

    def __init__(self, galaxy):
        self.galaxy = galaxy

    def attraction(self, e1: Entity, e2: Entity) -> np.ndarray:
        norm = np.linalg.norm(e1.position - e2.position)
        if norm < 1e3:
            return np.zeros(3)
        attraction_value = (G * e1.mass * e2.mass) / norm**2
        attraction_vector = (e1.position - e2.position) / norm
        return attraction_value * attraction_vector
    
    def seek(self, e: Entity, t: Entity, v_max: float, f_max: float, dist: float = 0.0) -> np.ndarray:
        if dist > 0.0:
            target = t.position + t.heading * dist
        else:
            target = t.position
        desired_velocity = normalize(target - e.position) * v_max
        steering = limit(desired_velocity - e.velocity, f_max)
        return steering
    
    def arrive(self, e: Entity, t: Entity, v_max: float, f_max: float, radius: float, dist: float = 0.0) -> np.ndarray:
        if dist > 0.0:
            target = t.position + t.heading * dist
        else:
            target = t.position
        desired_velocity = target - e.position
        distance = np.linalg.norm(desired_velocity) 
        if distance < radius:
            desired_velocity = normalize(target - e.position) * v_max * (distance / radius)
        else:
            desired_velocity = normalize(target - e.position) * v_max
        steering = limit(desired_velocity - e.velocity, f_max)
        return steering
