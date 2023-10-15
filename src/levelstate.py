import pygame

from src import shared
from src.button import Button
from src.state_enums import State
from src.utils import render_at


class LevelState:
    def __init__(self) -> None:
        self.next_state: State | None = None

        self.text = pygame.font.Font(None, 40).render("Pick your level!", True, "white")
        self.level_btns = [
            Button(
                pos=(120 * i, 300),
                size=(100, 100),
                colors={
                    "static": (51, 57, 65),
                    "hover": (74, 84, 98),
                    "text": (179, 185, 209),
                },
                text=str(i),
                corner_radius=3,
            )
            for i in range(1, 6)
        ]

    def update(self):
        for btn in self.level_btns:
            btn.update(pygame.mouse.get_pos())

            if btn.clicked:
                shared.level_no = int(btn.text)
                print(shared.level_no)
                self.next_state = State.GAME

    def draw(self):
        for btn in self.level_btns:
            btn.draw(shared.screen)

        render_at(shared.screen, self.text, "midtop", (0, 100))
