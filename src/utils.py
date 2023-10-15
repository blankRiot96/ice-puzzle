import math

import pygame


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
