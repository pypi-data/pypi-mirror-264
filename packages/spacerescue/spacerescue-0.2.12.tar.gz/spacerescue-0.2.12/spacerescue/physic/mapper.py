import pyray as pr
import numpy as np


class Mapper:
    """interface"""
    
    def real_to_grid_v(self, x: float) -> float:
        raise Exception("Not implemented")
    
    def grid_to_real_v(self, x: float) -> float:
        raise Exception("Not implemented")
    
    def real_to_grid(self, x: np.ndarray) -> pr.Vector3:
        raise Exception("Not implemented")
    
    def grid_to_real(self, x: pr.Vector3) -> np.ndarray:
        raise Exception("Not implemented")
    
    def get_lod(self, eye: np.ndarray, target):
        raise Exception("Not implemented")
    
    def to_grid_size(self, eye: np.ndarray, target) -> float:
        raise Exception("Not implemented")

    def to_grid_position(self, target) -> pr.Vector3:
        raise Exception("Not implemented")
    
    def enforce_boundary(self, target):
        raise Exception("Not implemented")