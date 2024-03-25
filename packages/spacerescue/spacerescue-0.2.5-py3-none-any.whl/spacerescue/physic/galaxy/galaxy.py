from typing import Iterator
import pyray as pr
import numpy as np

from spacerescue.constants import (
    GRID_SIZE,
    GRID_SPACING,
)
from spacerescue.physic.galaxy.planet import Planet
from spacerescue.resources.resource_manager import ResourceManager
from spacerescue.render import light as rl
from spacerescue.render.camera import Camera
from spacerescue.render.quadtree import QuadTreeBuilder
from spacerescue.physic.entity import Entity
from spacerescue.physic.universe import Universe
from spacerescue.physic.galaxy.galaxy_generator import GalaxyGenerator
from spacerescue.physic.galaxy.physic.physical_laws import PhysicalLaws
from spacerescue.physic.galaxy.physic.physical_mapper import PhysicalMapper
from spacerescue.physic.galaxy.hyperspace_portal import HyperspacePortal
from spacerescue.physic.galaxy.star import Star
from spacerescue.physic.galaxy.dust import Dust


ALL_STARS = lambda x: isinstance(x, Star)

ALL_PORTALS = lambda x: isinstance(x, HyperspacePortal)

ALL_SODB = (
    lambda x: isinstance(x, Star)
    or isinstance(x, Planet)
    or isinstance(x, HyperspacePortal)
)

ALL_STAR_SYSTEM_OBJECTS = lambda y: (
    lambda x: not isinstance(x, Dust) and isinstance(y, Star) and x.parent == y
)

ALL_STAR_SYSTEM_PORTALS = lambda y: (
    lambda x: isinstance(x, HyperspacePortal) and isinstance(y, Star) and x.parent == y
)

ALL_STAR_SYSTEM_PLANETS = lambda y: (
    lambda x: isinstance(x, Planet) and isinstance(y, Star) and x.parent == y
)

ALL_STAR_SYSTEM_HABITABLE_PLANETS = lambda y: (
    lambda x: isinstance(x, Planet)
    and isinstance(y, Star)
    and x.parent == y
    and x.is_habitable
)


class Galaxy(Universe):

    def __init__(self):
        super().__init__(PhysicalLaws(self), PhysicalMapper(self))

        self.star_selected: Star | None = None
        self.star_light: rl.Light | None = None

        # Generate stellar objects

        generator = GalaxyGenerator()
        self.stellar_objects = generator.generate_stellar_objects(self)
        self.hyperspace_indices, self.hyperspace_edges = generator.generate_hyperspace(
            self.stellar_objects
        )

        # Setup quad tree

        self.quadtree = QuadTreeBuilder(GRID_SIZE, GRID_SPACING).build()
        for stellar_object in self.stellar_objects:
            point = self.mapper.real_to_grid(stellar_object.position)
            self.quadtree.insert(point, stellar_object)

        # Lighting effect

        shader_lighting = ResourceManager.get_instance().load_shader("shader_lighting")
        shader_lighting.locs[pr.ShaderLocationIndex.SHADER_LOC_VECTOR_VIEW] = (
            pr.get_shader_location(shader_lighting, "viewPos")
        )
        amb = pr.get_shader_location(shader_lighting, "ambient")
        pr.set_shader_value(
            shader_lighting,
            amb,
            pr.Vector4(0.02, 0.02, 0.02, 1.0),
            pr.ShaderUniformDataType.SHADER_UNIFORM_VEC4,
        )

    def __del__(self):
        if self.star_light is not None:
            rl.delete_light(self.star_light)

    def update(self, dt: float, camera: Camera):
        self.quadtree.update(self.mapper.real_to_grid(camera.position), dt)
        super().update(dt)

    def draw(self, camera: Camera):
        self._update_events(camera)
        self._update_ligths(camera)
        self.quadtree.draw(camera)

    def filter_stellar_objects(self, filter_func=None) -> Iterator:
        if filter_func is not None:
            return filter(filter_func, self.stellar_objects)
        else:
            return iter(self.stellar_objects)

    def find_closest_stellar_object(
        self, position: np.ndarray, filter_func=None
    ) -> Entity | None:
        node = self.quadtree.find(self.mapper.real_to_grid(position))
        if node is not None:
            closest_entity = None
            min = 0
            for entity_ in filter(filter_func, node.entities):
                dist = np.linalg.norm(position - entity_.position)
                if closest_entity is None or dist < min:
                    closest_entity = entity_
                    min = dist
            return closest_entity

    def find_stellar_object_by_hyperspace_coord(self, idx) -> Entity:
        return self.stellar_objects[self.hyperspace_indices[idx]]

    def find_stellar_object_over_mouse(
        self, camera: Camera, filter_func=None
    ) -> Entity | None:
        ray = pr.get_mouse_ray(pr.get_mouse_position(), camera.camera)
        for stellar_object in self.filter_stellar_objects(filter_func):
            hit_info = pr.get_ray_collision_sphere(
                ray,
                stellar_object.to_grid_position(),
                max(stellar_object.to_grid_size(camera.position), 2),
            )
            if hit_info.hit:
                return stellar_object

    def _update_ligths(self, camera: Camera):
        shader_lighting = ResourceManager.get_instance().load_shader("shader_lighting")
        pr.set_shader_value(
            shader_lighting,
            shader_lighting.locs[pr.ShaderLocationIndex.SHADER_LOC_VECTOR_VIEW],
            camera.camera.position,
            pr.ShaderUniformDataType.SHADER_UNIFORM_VEC3,
        )

    def _update_events(self, camera: Camera):
        closest_star = self.find_closest_stellar_object(camera.position, ALL_STARS)
        assert closest_star is None or isinstance(closest_star, Star)
        if closest_star != self.star_selected:
            if self.star_selected is not None:
                self._leave_solar_system()
                self.star_selected = None
            if closest_star is not None:
                self._enter_solar_system(closest_star)
                self.star_selected = closest_star

    def _enter_solar_system(self, star: Star):
        assert self.star_light is None
        self.star_light = rl.create_light(
            rl.LIGHT_POINT,
            self.mapper.real_to_grid(star.position),
            pr.Vector3(0, 0, 0),
            star.color,
            ResourceManager.get_instance().load_shader("shader_lighting"),
        )

    def _leave_solar_system(self):
        assert self.star_light is not None
        self.star_light.enabled = False
        rl.light_update_values(self.star_light)
        rl.delete_light(self.star_light)
        self.star_light = None
