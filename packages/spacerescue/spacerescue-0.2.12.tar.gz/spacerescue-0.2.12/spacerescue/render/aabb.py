from __future__ import annotations

import pyray as pr


class AABB:
    def __init__(self, min: pr.Vector3, max: pr.Vector3):
        self.min = min
        self.max = max
        self.center = pr.Vector3(
            (min.x + max.x) * 0.5, (min.y + max.y) * 0.5, (min.z + max.z) * 0.5
        )
        self.size = pr.Vector3(
            (max.x - min.x) * 0.5, (max.y - min.y) * 0.5, (max.z - min.z) * 0.5
        )

    def subdivide(self) -> list[AABB]:
        a, b, m = self.min, self.max, self.center
        return [
            AABB(pr.Vector3(a.x, a.y, a.z), pr.Vector3(m.x, m.y, m.z)),
            AABB(pr.Vector3(m.x, a.y, a.z), pr.Vector3(b.x, m.y, m.z)),
            AABB(pr.Vector3(a.x, a.y, m.z), pr.Vector3(m.x, m.y, b.z)),
            AABB(pr.Vector3(m.x, a.y, m.z), pr.Vector3(b.x, m.y, b.z)),
            AABB(pr.Vector3(a.x, m.y, a.z), pr.Vector3(m.x, b.y, m.z)),
            AABB(pr.Vector3(m.x, m.y, a.z), pr.Vector3(b.x, b.y, m.z)),
            AABB(pr.Vector3(a.x, m.y, m.z), pr.Vector3(m.x, b.y, b.z)),
            AABB(pr.Vector3(m.x, m.y, m.z), pr.Vector3(b.x, b.y, b.z)),
        ]

    def contains(self, point: pr.Vector3) -> bool:
        return (
            point.x > self.min.x
            and point.x < self.max.x
            and point.y > self.min.y
            and point.y < self.max.y
            and point.z > self.min.z
            and point.z < self.max.z
        )

    def intersect_frustrum(self, planes: list[pr.Vector4]):
        for plane in planes:
            point = pr.Vector3(self.min.x, self.min.y, self.min.z)
            if plane.x > 0:
                point.x = self.max.x
            if plane.y > 0:
                point.y = self.max.y
            if plane.z > 0:
                point.z = self.max.z
            dist = point.x * plane.x + point.y * plane.y + point.z * plane.z + plane.w
            if dist < 0:
                return False
        return True
    
    def draw_wrires(self):
        pr.draw_cube_wires(
            self.center,
            self.size.x,
            self.size.y,
            self.size.z,
            pr.Color(128, 128, 128, 128),
        )
