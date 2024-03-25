import numpy as np
import pyray as pr

from spacerescue.render import light as rl
from spacerescue.resources.resource_manager import ResourceManager


class Camera:
    
    def __init__(self, position: np.ndarray, camera: pr.Camera3D):
        self.position = position
        self.camera = camera
        
        self.camera_light = rl.create_light(
            rl.LIGHT_POINT,
            self.camera.position,
            pr.Vector3(0, 0, 0),
            pr.Color(8, 8, 8, 255),
            ResourceManager.get_instance().load_shader("shader_lighting"),
        )
        
    def __del__(self):
        rl.delete_light(self.camera_light)
        
    def update(self, dt: float):
        self.camera_light.position = self.camera.position
        rl.light_update_values(self.camera_light)
