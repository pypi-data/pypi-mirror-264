from spacerescue.core.types import Stateable
from spacerescue.resources import GLOBAL_RESOURCES


class GameBoard:
    
    def __init__(self):
        self.resources = GLOBAL_RESOURCES
        self.context = {}
        
    def begin(self, state: Stateable):
        self.state = state
        self.state.enter()
        
    def end(self):
        self.state.leave()
        self.resources.unload_all()
        
    def update(self):
        self.state = self.state.update().map(lambda x: x.leave().enter()).get()
        
    def draw(self):
        self.state.draw()
        