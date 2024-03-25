import pyray as pr


class Widget:
    
    def __init__(self, id: str, bound: pr.Rectangle):
        self.id = id
        self.bound = bound
        
    def update(self):
        pass
    
    def draw(self):
        pass
    