from __future__ import annotations
from functools import cache

import numpy as np

from spacerescue.resources.resource_manager import ResourceManager


class NameGenerator:

    PLANET_NAMES = ResourceManager.get_instance().load_res_lines("planet_names")

    @cache
    @staticmethod
    def get_instance(name: str = "singleton") -> NameGenerator:
        return NameGenerator()

    def __init__(self):
        self.uuid = 0

    def generate_object_name(self):
        self.uuid += 1
        return f"HCSS{self.uuid}"

    def generate_planet_name(self):
        return np.random.choice(NameGenerator.PLANET_NAMES)
