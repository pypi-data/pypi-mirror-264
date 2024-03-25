import numpy as np
import quaternion
import pyray as pr

EPSILON = 1e-6
DEG2RAD = np.pi / 180.0
RAD2DEG = 180.0 / np.pi


def vector3_to_ndarray(v: pr.Vector3) -> np.ndarray:
    return np.array([v.x, v.y, v.z])


def ndarray_to_vector3(v: np.ndarray) -> pr.Vector3:
    return pr.Vector3(*v)


def normalize(x: np.ndarray) -> np.ndarray:
    l = np.linalg.norm(x)
    return x / l if l != 0 else x


def scale(x: np.ndarray, l: float) -> np.ndarray:
    return normalize(x) * l


def limit(x: np.ndarray, max: float) -> np.ndarray:
    l = np.linalg.norm(x)
    return x * min(max / l, 1.0)


def lerp(a: np.ndarray, b: np.ndarray, t: float):
    return a * (1.0 - t) + b * t


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def perpendicular(v: np.ndarray) -> np.ndarray:
    min = abs(v[0])
    cardinal_axis = np.array([1.0, 0.0, 0.0])

    if abs(v[1]) < min:
        min = abs(v[1])
        cardinal_axis = np.array([0.0, 1.0, 0.0])

    if abs(v[2]) < min:
        cardinal_axis = np.array([0.0, 0.0, 1.0])

    return np.cross(v, cardinal_axis)


def rotate_by_axis_angle(v: np.ndarray, axis: np.ndarray, alpha: float) -> np.ndarray:
    axis = normalize(axis)
    R = quaternion.from_rotation_vector(axis * alpha)
    V = quaternion.from_vector_part(v)
    return quaternion.as_vector_part(R * V * R.conjugate())
