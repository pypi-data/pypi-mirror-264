import pyray as pr
import numpy as np

from spacerescue.constants import SCREEN_HEIGHT, SCREEN_WIDTH


class Star:

    def __init__(self):
        self.x = np.random.randint(-SCREEN_WIDTH, SCREEN_WIDTH)
        self.y = np.random.randint(-SCREEN_HEIGHT, SCREEN_HEIGHT)
        self.z = np.random.randint(0, 400)
        self.sx, self.sy = self.transform()
        self.ox, self.oy = self.sx, self.sy

    def update(self, dt: float):
        self.z -= 30 * dt
        if self.z <= 0:
            self.x = np.random.randint(-SCREEN_WIDTH, SCREEN_WIDTH)
            self.y = np.random.randint(-SCREEN_HEIGHT, SCREEN_HEIGHT)
            self.z = 400
            self.sx, self.sy = self.transform()
            self.ox, self.oy = self.sx, self.sy
        else:
            self.ox, self.oy = self.sx, self.sy
            self.sx, self.sy = self.transform()

    def draw(self):
        pr.draw_line(self.ox, self.oy, self.sx, self.sy, pr.WHITE)  # type: ignore

    def transform(self):
        w = 1.0 / (self.z + 1e-5)
        sx = int(self.x * w) + SCREEN_WIDTH // 2
        sy = int(self.y * w) + SCREEN_HEIGHT // 2
        return sx, sy


class StarField:

    def __init__(self):
        self.stars = []
        for i in range(5000):
            self.stars.append(Star())

    def update(self, dt: float):
        for star in self.stars:
            star.update(dt)

    def draw(self):
        for star in self.stars:
            star.draw()
