import pygame

from src import shared
from src.grid import Grid
from src.state_enums import State


class GameState:
    def __init__(self) -> None:
        self.bg_image = pygame.image.load("assets/art/background.png").convert()

        self.next_state: State | None = None
        self.grid = Grid()
        self.grid.load_levels(shared.level_no)
        self.current_level = shared.level_no

    def update(self):
        self.grid.update()

        for event in shared.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.next_state = State.GAME

        if shared.level_no > self.current_level:
            self.next_state = State.GAME

        self.current_level = shared.level_no

    def draw(self):
        shared.screen.blit(self.bg_image, (0, 0))
        self.grid.draw()
