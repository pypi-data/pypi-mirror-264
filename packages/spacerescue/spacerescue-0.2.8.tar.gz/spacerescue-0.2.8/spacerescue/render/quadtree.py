from __future__ import annotations

import numpy as np
import pyray as pr

from spacerescue.render.camera import Camera
from spacerescue.physic.entity import Entity
from spacerescue.render.aabb import AABB
from spacerescue.render.frustrum import get_frustrum_planes
from spacerescue.tools.util import first_not_none


class QuadTreeBuilder:
    """Cass to build a QuadTree data structure for spatial partitioning"""

    def __init__(self, size: float, spacing: float):
        """Constructor initializing the QuadTreeBuilder with a given size and spacing"""
        self.size = size
        self.spacing = spacing

    def build(self) -> QuadTree:
        """Function to create and return a new QuadTree"""

        bound = self.size * self.spacing / 2
        min = pr.Vector3(-bound, -bound, -bound)
        max = pr.Vector3(bound, bound, bound)
        depth = np.log2(self.size)
        return QuadTree(AABB(min, max), depth)


class QuadTree:
    """Class used for organizing objects in a virtual space to optimize various spatial queries"""

    # Static variables to keep track of usage statistics
    total_node_count = 0
    total_entity_count = 0
    count_find_call_per_frame = 0
    count_node_draw_per_frame = 0

    def __init__(self, aabb: AABB, depth: int, parent: QuadTree | None = None):
        """Constructor initializing the QuadTree node with an axis-aligned bounding box (AABB), depth, and optionally a parent"""
        QuadTree.total_node_count += 1
        self.parent = parent
        self.aabb = aabb
        self.entities: list[Entity] = []
        if depth > 1:
            self.children: list[QuadTree] = [
                QuadTree(x, depth - 1, self) for x in aabb.subdivide()
            ]
        else:
            self.children: list[QuadTree] = []

    def find(self, point: pr.Vector3) -> QuadTree | None:
        """Find the QuadTree node containing the given point"""
        QuadTree.count_find_call_per_frame += 1
        return self._find_rec(point)

    def insert(self, point: pr.Vector3, entity: Entity):
        """Insert an entity into the QuadTree at the given position"""
        node = self.find(point)
        if node is not None:
            QuadTree.total_entity_count += 1
            node.entities.append(entity)

    def update(self, point: pr.Vector3, dt: float):
        node = self.find(point)
        if node is not None:
            for stellar_object in node.entities:
                stellar_object.update(dt)

    def draw(self, camera: Camera):
        """Start drawing the visible QuadTree nodes and their entities"""
        QuadTree.count_node_draw_per_frame = 0
        view_matrix = pr.get_camera_matrix(camera.camera)
        frustrum_planes = get_frustrum_planes(camera.camera, view_matrix)
        self._draw_rec(camera, frustrum_planes, view_matrix)
        QuadTree.count_find_call_per_frame = 0

    #
    # Private Helpers
    #
    
    def _find_rec(self, point: pr.Vector3) -> QuadTree | None:
        """Recursive helper to find the QuadTree node containing the given position"""
        if self.aabb.contains(point):
            if len(self.children) == 0:
                return self
            else:
                return first_not_none([x._find_rec(point) for x in self.children])
    
    def _draw_rec(self, camera: Camera, frustrum_planes: list[pr.Vector4], view_matrix: pr.Matrix):
        """Recursive helper to draw nodes intersecting with the given view frustum"""
        if self.aabb.intersect_frustrum(frustrum_planes):
            if len(self.children) == 0:
                QuadTree.count_node_draw_per_frame += 1
                for entity in self.entities:
                    entity.draw(camera)
            else:
                for child in self._sorted_children_by_depth(view_matrix):
                    child._draw_rec(camera, frustrum_planes, view_matrix)

    def _sorted_children_by_depth(self, view_matrix: pr.Matrix):
        """Sorts children nodes based on distance squared from the camera for optimized drawing"""
        _by_depth_func = lambda x: abs(pr.vector3_transform(x.aabb.center, view_matrix).z)
        return sorted(self.children, key=_by_depth_func, reverse=True)
