from html import entities
import numpy as np
import pyray as pr

from spacerescue.physic.simulation.physic.physical_laws import PhysicalLaws
from spacerescue.physic.simulation.physic.physical_mapper import PhysicalMapper
from spacerescue.physic.entity import Entity
from spacerescue.physic.universe import Universe


class Column:

    TILE_NUMBER = 5

    def __init__(self, world):
        self.x = world.bound.x + world.bound.width
        self.size = int(world.bound.height / Column.TILE_NUMBER)
        space = np.random.randint(0, Column.TILE_NUMBER)
        self.tiles = [
            pr.Rectangle(self.x, world.bound.y + y * self.size, self.size, self.size)
            for y in range(0, Column.TILE_NUMBER)
            if y != space
        ]

    def check_collision(self, center: pr.Vector2, radius: float) -> bool:
        for tile in self.tiles:
            if pr.check_collision_circle_rec(center, radius, tile):
                return True
        return False

    def update(self, dt: float):
        self.x -= 10 * dt
        for tile in self.tiles:
            tile.x = self.x

    def draw(self):
        for tile in self.tiles:
            pr.draw_rectangle_lines_ex(tile, 1, pr.WHITE)  # type: ignore


class World(Universe):

    WIDTH_BETWEEN_COLUMNS = 500
    ORIGIN = np.array([-200.0, 200.0, 0.0])
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.bound = pr.Rectangle(x, y, width, height)
        self.columns = []
        self.columns.append(Column(self))
        self.score = 0
        super().__init__(PhysicalLaws(self), PhysicalMapper(self))

    def find_closest_stellar_object(self, position: np.ndarray, filter_func=None):
        raise Exception("Not implemented")

    def get_sensor_data(self) -> list[int]:
        result = []
        
        if len(self.columns) > 0:
            first_column = self._get_front_column()
            assert first_column is not None
            result = [0, 0, 0, 0, 0, 0]
                
            pos = self.mapper.grid_to_real(pr.Vector3(first_column.x, 0, 0))
            dist = abs(pos[0] - World.ORIGIN[0])
            result[0] = int(dist)

            for tile in first_column.tiles:
                result[int(tile.y // tile.height)] = 1
              
        return result

    def check_collision(self, entity: Entity) -> bool:
        pos = entity.to_grid_position()
        pos = pr.Vector2(pos.x, pos.y)
        rad = entity.to_grid_size(np.zeros(3))
        
        if self._hit_boundaries(pos, rad):
            return True

        if len(self.columns) > 0:
            first_column = self._get_front_column()
            assert first_column is not None
            if first_column.check_collision(pos, rad):
                return True

        return False

    def update(self, dt: float):
        for column in self.columns:
            column.update(dt)

        if len(self.columns) > 0:
            first_column = self.columns[0]
            if first_column.x < self.bound.x - first_column.size:
                self.columns.pop(0)
                del first_column
                self.score += 1     

        if len(self.columns) > 0:
            last_column = self.columns[-1]
            if (
                abs(self.bound.x + self.bound.width - last_column.x)
                > World.WIDTH_BETWEEN_COLUMNS
            ):
                self.columns.append(Column(self))    

        super().update(dt)

    def draw(self):
        pr.draw_rectangle_lines_ex(self.bound, 1, pr.WHITE)  # type: ignore
        for column in self.columns:
            column.draw()
        pr.draw_text(str(self.score), int(self.bound.x + 5), int(self.bound.y + 5), 20, pr.WHITE)  # type: ignore

    def _hit_boundaries(self, center: pr.Vector2, radius: float):
        return (
            abs(self.bound.x - center.x) <= radius
            or abs(self.bound.x + self.bound.width - center.x - 1) <= radius
            or abs(self.bound.y - center.y) <= radius
            or abs(self.bound.y + self.bound.height - center.y - 1) <= radius
        )
        
    def _get_front_column(self):
        for column in self.columns:
            pos = self.mapper.grid_to_real(pr.Vector3(column.x, 0, 0))
            if World.ORIGIN[0] < pos[0] + column.size * 0.5:
                return column
        return None