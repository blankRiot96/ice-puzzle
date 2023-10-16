import math

import pygame

from src import shared
from src.button import Button
from src.state_enums import State
from src.utils import DashBoardRenderer


class MenuState:
    def __init__(self) -> None:
        self.next_state: State | None = None
        size = pygame.Vector2(100, 40)
        self.start_btn = Button(
            shared.SRECT.center - (size / 2),
            tuple(map(int, size)),
            colors={
                "static": (51, 57, 65),
                "hover": (74, 84, 98),
                "text": (179, 185, 209),
            },
            text="Start",
            corner_radius=3,
        )
        self.dashboard = DashBoardRenderer("Ice Age Puzzle", 64, "cyan", -150)

    def update(self):
        self.start_btn.update(pygame.mouse.get_pos())
        self.dashboard.update()

        if self.start_btn.clicked:
            self.next_state = State.LEVEL_PICKER

    def draw(self):
        self.start_btn.draw(shared.screen)
        self.dashboard.draw()
