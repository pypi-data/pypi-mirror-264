import pyray as pr
 
from spacerescue.render.animator import Animator
from spacerescue.core.math import EPSILON, clamp


class FadeScr(Animator):

    def __init__(self, duration: float):
        super().__init__(duration)
        self.snapshot = self._take_screen_snapshot()
        
    def reset(self):
        super().reset()
        self.snapshot = self._take_screen_snapshot()

    def draw(self):
        t = self.timer / (self.duration + EPSILON)
        alpha = float(clamp(255 * (1.0 - t), 0, 255))
        if alpha > 0.0:
            pr.draw_texture(self.snapshot, 0, 0, pr.fade(pr.WHITE, alpha / 255.0))  # type: ignore
        elif self.snapshot is not None:
            pr.unload_texture(self.snapshot)
            self.snapshot = None

    def _take_screen_snapshot(self):
        image = pr.load_image_from_screen()
        texture = pr.load_texture_from_image(image)
        pr.unload_image(image)
        return texture