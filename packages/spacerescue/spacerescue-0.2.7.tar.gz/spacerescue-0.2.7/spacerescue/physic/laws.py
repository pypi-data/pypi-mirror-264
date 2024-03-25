import numpy as np


class Laws:
    """interface"""

    def gravity(self, e) -> np.ndarray:
        raise Exception("Not implemented")
    
    def attraction(self, e1, e2) -> np.ndarray:
        raise Exception("Not implemented")
    
    def seek(self, e, t, v_max: float, f_max: float, dist: float = 0.0) -> np.ndarray:
        raise Exception("Not implemented")
    
    def arrive(self, e, t, v_max: float, f_max: float, radius: float, dist: float = 0.0) -> np.ndarray:
        raise Exception("Not implemented")
    