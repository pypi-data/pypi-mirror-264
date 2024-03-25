import pyray as pr
import numpy as np

from spacerescue.constants import GRID_SPACING, AU
from spacerescue.physic.galaxy import galaxy
from spacerescue.physic.entity import Entity
from spacerescue.physic.mapper import Mapper
from spacerescue.physic.galaxy.galaxy_generator import GalaxyGenerator
from spacerescue.physic.galaxy.star import Star
from spacerescue.core.math import EPSILON, clamp, ndarray_to_vector3, vector3_to_ndarray
from spacerescue.tools.util import np_cache_method


class PhysicalMapper(Mapper):
    
    STAR_SYSTEM_SIZE = 2e6 * AU

    REAL_TO_GRID = GRID_SPACING / GalaxyGenerator.STARS_DIST
    GRID_TO_REAL = GalaxyGenerator.STARS_DIST / GRID_SPACING

    def __init__(self, galaxy):
        self.galaxy = galaxy
        
    def real_to_grid_v(self, x: float) -> float:
        return x * PhysicalMapper.REAL_TO_GRID
    
    def grid_to_real_v(self, x: float) -> float:
        return x * PhysicalMapper.GRID_TO_REAL
        
    def real_to_grid(self, x: np.ndarray) -> pr.Vector3:
        return ndarray_to_vector3(x * PhysicalMapper.REAL_TO_GRID)
    
    def grid_to_real(self, x: pr.Vector3) -> np.ndarray:
        return vector3_to_ndarray(x) * PhysicalMapper.GRID_TO_REAL

    def get_lod(self, eye: np.ndarray, target: Entity) -> int:
        dist = np.linalg.norm(eye - target.position)
        return 1 if dist < PhysicalMapper.STAR_SYSTEM_SIZE else 0

    def to_grid_size(self, eye: np.ndarray, target: Entity) -> float:
        dist = float(np.linalg.norm(eye - target.position))
        if target.radius > 1e8:  # Stars and dust
            scale = self._scale_radius(dist, 1.0, 2e4)
        elif target.radius > 1e5:  # Planets
            scale = self._scale_radius(dist, 1.0, 5e6)
        else:  # Others
            scale = 2e11
        return target.radius * scale * PhysicalMapper.REAL_TO_GRID

    def to_grid_position(self, target: Entity) -> pr.Vector3:
        center = self._get_center(target)
        if center is None:
            return self.real_to_grid(target.position)
        else:
            off = target.position - center
            dist = float(np.linalg.norm(off))
            return self.real_to_grid(center + off * self._scale_offset(dist, 1.0, 8e5))

    @np_cache_method
    def _find_closest_star(self, position: np.ndarray) -> Star:
        return self.galaxy.find_closest_stellar_object(position, galaxy.ALL_STARS)

    def _get_center(self, target: Entity) -> np.ndarray | None:
        if target.parent is not None:
            return target.parent.position
        elif not isinstance(target, Star):
            star = self._find_closest_star(target.position)
            if star is not None:
                return star.position
       
    def _scale_offset(self, x: float, min: float, max: float) -> float:
        return clamp(PhysicalMapper.STAR_SYSTEM_SIZE / (x + EPSILON), min, max)
    
    def _scale_radius(self, x: float, min: float, max: float) -> float:
        if x < PhysicalMapper.STAR_SYSTEM_SIZE:
            return max
        else:
            return min
