import math
import time

import pygame

from src import shared


class SinWave:
    def __init__(self, speed):
        self.speed = speed
        self.radians = 0
        self.val = 0

    def update(self):
        self.radians += self.speed
        while self.radians >= (math.pi * 2):
            self.radians = self.radians - (math.pi * 2)
        self.val = math.sin(self.radians)


def render_at(
    base_surf: pygame.Surface,
    surf: pygame.Surface,
    pos: str,
    offset=(0, 0),
) -> None:
    """Renders a surface to a base surface by matching a point.

    Example: render_at(screen, widget, "center")
    """
    base_rect = base_surf.get_rect()
    surf_rect = surf.get_rect()
    setattr(surf_rect, pos, getattr(base_rect, pos))
    surf_rect.x += offset[0]
    surf_rect.y += offset[1]
    base_surf.blit(surf, surf_rect)


class Time:
    """
    Class to check if time has passed.
    """

    def __init__(self, time_to_pass: float):
        self.time_to_pass = time_to_pass
        self.start = time.perf_counter()

    def reset(self):
        self.start = time.perf_counter()

    def tick(self) -> bool:
        if time.perf_counter() - self.start > self.time_to_pass:
            self.start = time.perf_counter()
            return True
        return False


class DashBoardRenderer:
    def __init__(self, text, size, color, offset) -> None:
        font = pygame.font.Font(None, size)
        self.image = font.render(text, True, color)
        self.y = 0
        self.wave = SinWave(0.003)
        self.offset = offset

    def update(self):
        self.wave.update()
        self.y = self.wave.val * 30

    def draw(self):
        render_at(shared.screen, self.image, "center", (0, self.offset + self.y))
