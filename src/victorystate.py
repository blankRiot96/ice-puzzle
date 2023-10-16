import pygame

from src import shared
from src.state_enums import State
from src.utils import DashBoardRenderer


class VictoryState:
    def __init__(self) -> None:
        self.next_state: State | None = None
        self.dash = DashBoardRenderer("You Win!", 128, "yellow", 0)

    def update(self):
        self.dash.update()

    def draw(self):
        self.dash.draw()
