import pyray as pr
import numpy as np

from spacerescue.constants import (
    AU,
    GRID_SIZE,
    PARSEC
)
from spacerescue.core.math import (
    normalize,
    perpendicular,
    rotate_by_axis_angle,
)
from spacerescue.physic.entity import Entity
from spacerescue.physic.galaxy.dust import Dust
from spacerescue.physic.galaxy.star import Star
from spacerescue.physic.galaxy.planet import Planet
from spacerescue.physic.galaxy.hyperspace_portal import HyperspacePortal


class GalaxyGenerator:

    STARS_DIST = 15 * PARSEC  # milky way average distance
    STARS_DENSITY = 0.04  # milky way density
    STARS_COLORS = [
        (255, 255, 255, 255),
        (255, 255, 128, 255),
        (255, 128, 128, 255),
    ]

    DUSTS_DENSITY = STARS_DENSITY * 0.5

    PLANETS_DENSITY = STARS_DENSITY * 0.95
    PLANETS_DISTS = [
        0.7 * AU,  # venus like
        1.0 * AU,  # earth like
        1.5 * AU,  # mars like
    ]
    PLANETS_MASSES = [
        4.87e24,  # kg           # venus like
        5.97e24,  # kg           # earth like
        6.39e23,  # kg           # mars like
    ]
    PLANETS_VELOCITIES = [
        3.50e4,  # m⋅s-1         # venus like
        3.00e4,  # m⋅s-1         # earth like
        2.43e4,  # m⋅s-1         # mars like
    ]
    PLANETS_RADIUSES = [
        2.439e6,  # m            # venus like
        6.371e6,  # m            # earth like
        3.389e6,  # m            # mars like
    ]
    PLANETS_MODELS = [
        "venus",
        "earth",
        "mars",
    ]

    HYPERSPACE_PORTALS_DENSITY = STARS_DENSITY * 0.5
    HYPERSPACE_PORTALS_EDGES = 0.005
    HYPERSPACE_PORTALS_DIST = 5.0 * AU

    def generate_stellar_objects(self, galaxy) -> list[Entity]:
        D_matter = np.random.uniform(0, 1, (GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Generate stars

        stars: list[Entity] = []
        for vox, pos in self._for_each_voxel(GRID_SIZE):
            if D_matter[*vox] < GalaxyGenerator.STARS_DENSITY:
                spin_axis = normalize(np.random.rand(3))  # np.array([0., 1., 0.])
                color = np.random.randint(0, 3)
                stars.append(
                    Star(galaxy, spin_axis, pos, GalaxyGenerator.STARS_COLORS[color])
                )

        # Generate dusts

        dusts: list[Entity] = []
        for vox, pos in self._for_each_voxel(GRID_SIZE):
            if D_matter[*vox] < GalaxyGenerator.DUSTS_DENSITY:
                star = next(filter(lambda x: (x.position == pos).all(), stars), None)
                if star is not None:
                    dusts.append(Dust(galaxy, pos, star))

        # Generate planets

        planets: list[Entity] = []
        for vox, pos in self._for_each_voxel(GRID_SIZE):
            if D_matter[*vox] < GalaxyGenerator.PLANETS_DENSITY:
                star = next(filter(lambda x: (x.position == pos).all(), stars), None)
                if star is not None:
                    planets_count = np.random.randint(0, 3) + 1
                    for i in range(planets_count):
                        off = normalize(
                            rotate_by_axis_angle(
                                perpendicular(star.spin_axis),
                                star.spin_axis,
                                2 * np.pi * np.random.rand(),
                            )
                        )
                        vel = np.cross(star.spin_axis, off)
                        planets.append(
                            Planet(
                                galaxy,
                                GalaxyGenerator.PLANETS_MASSES[i],
                                GalaxyGenerator.PLANETS_RADIUSES[i],
                                pos + off * GalaxyGenerator.PLANETS_DISTS[i],
                                vel * GalaxyGenerator.PLANETS_VELOCITIES[i],
                                GalaxyGenerator.PLANETS_MODELS[i],
                                star,
                                i == 1, # is_habitable
                            )
                        )

        # Generate portals

        portals: list[Entity] = []
        for vox, pos in self._for_each_voxel(GRID_SIZE):
            if D_matter[*vox] < GalaxyGenerator.HYPERSPACE_PORTALS_DENSITY:
                star = next(filter(lambda x: (x.position == pos).all(), stars), None)
                if star is not None:
                    off = (
                        normalize(np.random.rand(3))
                        * GalaxyGenerator.HYPERSPACE_PORTALS_DIST
                    )
                    portals.append(HyperspacePortal(galaxy, pos + off, star))

        return dusts + stars + planets + portals

    def generate_hyperspace(self, stellar_objects) -> tuple[list[int], np.ndarray]:
        indices = [
            index
            for index, stellar_object in enumerate(stellar_objects)
            if isinstance(stellar_object, HyperspacePortal)
        ]
        A = np.random.rand(len(indices), len(indices))
        T = np.ma.masked_where(A < GalaxyGenerator.HYPERSPACE_PORTALS_EDGES, A).mask
        return indices, T

    def _for_each_voxel(self, size):
        for x in range(0, size):
            for y in range(0, size):
                for z in range(0, size):
                    voxel = x, y, z
                    off = (1.0 - GRID_SIZE) / 2.0
                    position = (np.array(voxel) + off) * GalaxyGenerator.STARS_DIST
                    yield voxel, position
