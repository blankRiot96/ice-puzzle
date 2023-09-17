from enum import Enum, auto

import pygame

import src.shared as shared


class MovementType(Enum):
    FIXED = auto()
    STATIC = auto()
    PUSHED = auto()
    CONTROLLED = auto()


class Grid:
    LINE_COLOR = "black"

    def __init__(self) -> None:
        shared.entities: list = []

    def push_entity(self, entity):
        shared.entities.append(entity)

    def update(self):
        for entity in shared.entities:
            entity.update()

    def draw_grid(self):
        for row in range(shared.ROWS + 1):
            start = 0, row * shared.TILE_SIDE
            end = shared.WIN_WIDTH, row * shared.TILE_SIDE
            pygame.draw.line(shared.screen, Grid.LINE_COLOR, start, end)

        for col in range(shared.COLS + 1):
            start = col * shared.TILE_SIDE, 0
            end = col * shared.TILE_SIDE, shared.WIN_HEIGHT
            pygame.draw.line(shared.screen, Grid.LINE_COLOR, start, end)

    def draw(self):
        self.draw_grid()
        for entity in shared.entities:
            entity.draw()
