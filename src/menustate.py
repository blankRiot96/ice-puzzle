import math

import pygame

from src import shared
from src.button import Button
from src.state_enums import State
from src.utils import SinWave, render_at


class DashBoardRenderer:
    def __init__(self) -> None:
        font = pygame.font.Font(None, 64)
        self.image = font.render("Ice Age Puzzle", True, "cyan")
        self.y = 0
        self.wave = SinWave(0.003)

    def update(self):
        self.wave.update()
        self.y = self.wave.val * 30

    def draw(self):
        render_at(shared.screen, self.image, "center", (0, -150 + self.y))


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
        self.dashboard = DashBoardRenderer()

    def update(self):
        self.start_btn.update(pygame.mouse.get_pos())
        self.dashboard.update()

        if self.start_btn.clicked:
            self.next_state = State.LEVEL_PICKER

    def draw(self):
        self.start_btn.draw(shared.screen)
        self.dashboard.draw()
