from src.entities import Apricorn, Box, Goal, Squirrel
from src.grid import Grid
from src.state_enums import State


class GameState:
    def __init__(self) -> None:
        self.next_state: State | None = None
        self.grid = Grid()
        self.grid.push_entity(Squirrel((5, 5)))
        self.grid.push_entity(Box((7, 5)))
        self.grid.push_entity(Apricorn((8, 6)))
        self.grid.push_entity(Goal((10, 3)))

    def update(self):
        self.grid.update()

    def draw(self):
        self.grid.draw()
