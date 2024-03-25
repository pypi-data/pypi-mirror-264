import pyray as pr

class Animator:
        
    def __init__(self, duration: float):
        self.duration = duration
        self.timer = 0

    def reset(self):
        self.timer = 0

    def is_playing(self, latency: float = 0.1) -> bool:
        return self.timer < self.duration + latency

    def update(self):
        self.timer = self.timer + min(pr.get_frame_time(), 1/60)

    def draw(self):
        pass
    