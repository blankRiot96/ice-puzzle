import pygame

import src.shared as shared
from src.entities import (
    Apricorn,
    Box,
    Enemy,
    Goal,
    LauncherLeft,
    LauncherRight,
    Squirrel,
    Wall,
)


class Grid:
    LINE_COLOR = "black"

    ENTITIES = {
        1: Wall,
        2: Squirrel,
        3: Apricorn,
        4: Goal,
        5: Enemy,
        6: LauncherLeft,
        7: LauncherRight,
        8: Box,
    }

    def __init__(self) -> None:
        shared.entities: list = []

    def push_entity(self, entity):
        shared.entities.append(entity)

    def update(self):
        for entity in shared.entities:
            entity.update()

    def place_entity(self, row, col, entity_no):
        entity = Grid.ENTITIES.get(entity_no)
        if entity is None:
            return
        self.push_entity(entity((col, row)))

    def load_levels(self, level_no: int):
        with open(f"assets/data/level_{level_no}.txt") as f:
            data = f.readlines()

        for row, line in enumerate(data):
            line = line.strip()
            for col, ent in enumerate(line):
                ent = int(ent)
                if ent == 5:
                    if col != line.find("5"):
                        continue
                    col_2 = line.rfind("5")

                    entity = Enemy((col, row), (col_2, row))
                    self.push_entity(entity)
                    continue

                self.place_entity(row, col, ent)

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
