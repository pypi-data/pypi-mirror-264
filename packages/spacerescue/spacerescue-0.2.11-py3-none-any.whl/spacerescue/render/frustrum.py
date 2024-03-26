import pyray as pr

from spacerescue.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from spacerescue.core.math import DEG2RAD

CAMERA_NEAR_CULL_DISTANCE = 0.01
CAMERA_FAR_CULL_DISTANCE = 1000.0

def get_frustrum_planes(camera: pr.Camera3D, view_matrix: pr.Matrix) -> list[pr.Vector4]:
    aspect = float(SCREEN_WIDTH) / float(SCREEN_HEIGHT)
    PV = pr.matrix_multiply(
        view_matrix,
        pr.matrix_perspective(
            camera.fovy * DEG2RAD, aspect, CAMERA_NEAR_CULL_DISTANCE, CAMERA_FAR_CULL_DISTANCE
        ),
    )
    return [
        # Left clipping plane
        pr.Vector4(PV.m3 + PV.m0, PV.m7 + PV.m4, PV.m11 + PV.m8, PV.m15 + PV.m12),
        # # Right clipping plane
        pr.Vector4(PV.m3 - PV.m0, PV.m7 - PV.m4, PV.m11 - PV.m8, PV.m15 - PV.m12),
        # Bottom clipping plane
        pr.Vector4(PV.m3 + PV.m1, PV.m7 + PV.m5, PV.m11 + PV.m9, PV.m15 + PV.m13),
        # Top clipping plane
        pr.Vector4(PV.m3 - PV.m1, PV.m7 - PV.m5, PV.m11 - PV.m9, PV.m15 - PV.m13),
        # # Near clipping plane
        pr.Vector4(PV.m3 + PV.m2, PV.m7 + PV.m6, PV.m11 + PV.m10, PV.m15 + PV.m14),
        # # Far clipping plane
        pr.Vector4(PV.m3 - PV.m2, PV.m7 - PV.m6, PV.m11 - PV.m10, PV.m15 - PV.m14),
    ]

def is_point_in_frustrum(point: pr.Vector3, planes: list[pr.Vector4]):
    for plane in planes:
        dist = point.x * plane.x + point.y * plane.y + point.z * plane.z + plane.w
        if dist < 0:
            return False
    return True
