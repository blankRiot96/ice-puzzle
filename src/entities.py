import abc

import pygame

import src.shared as shared
from src.enums import MovementType


def qload(name: str, alpha: bool) -> pygame.Surface:
    img = pygame.image.load(f"assets/art/{name}.png")

    if alpha:
        return img.convert_alpha()

    return img.convert()


class Entity(abc.ABC):
    def __init__(self, cell, movement_type, image) -> None:
        super().__init__()
        self.cell = cell
        self.movement_type = movement_type
        self.image = image

        self.cell = pygame.Vector2(cell)
        self.pos = self.cell * shared.TILE_SIDE
        self.rect = self.image.get_rect(topleft=self.pos)
        self.desired_cell = self.cell.copy()
        self.desired_pos = self.pos.copy()
        self._direction = (0, 0)
        self.moving = False

    @property
    def direction(self) -> tuple[int, int]:
        return self._direction

    @direction.setter
    def direction(self, new_direction):
        self._direction = new_direction
        self.desired_cell = self.cell + self.direction
        self.desired_pos = self.desired_cell * shared.TILE_SIDE
        self.moving = True

    def move(self):
        self.pos.move_towards_ip(self.desired_pos, shared.ENTITY_SPEED * shared.dt)
        self.rect.topleft = self.pos

    def transfer_cell(self):
        if self.pos == self.desired_pos:
            self.cell = self.desired_cell.copy()
            self.moving = False
        else:
            self.mvoing = True

    def update(self):
        self.move()
        self.transfer_cell()

    def draw(self):
        shared.screen.blit(self.image, self.rect)


class Enemy(Entity):
    def __init__(self, cell) -> None:
        image = qload("enemy", True)
        super().__init__(cell, MovementType.FIXED, image)

    def update(self):
        super().update()


class Launcher(Entity):
    ...


class LauncherLeft(Launcher):
    ...


class LauncherRight(Launcher):
    ...


class Wall(Entity):
    def __init__(self, cell: tuple[int, int]) -> None:
        image = qload("wall", False)
        super().__init__(cell, MovementType.STATIC, image)


class Squirrel(Entity):
    CONTROLS = {
        # Arrow keys
        pygame.K_RIGHT: (1, 0),
        pygame.K_LEFT: (-1, 0),
        pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),
        # WASD
        pygame.K_d: (1, 0),
        pygame.K_a: (-1, 0),
        pygame.K_w: (0, -1),
        pygame.K_s: (0, 1),
    }

    def __init__(self, cell: tuple[int, int]) -> None:
        image = qload("squirrel", True)
        super().__init__(cell, MovementType.CONTROLLED, image)

    def scan_controls(self):
        if self.moving:
            return
        for event in shared.events:
            if event.type == pygame.KEYDOWN and event.key in Squirrel.CONTROLS:
                self.direction = Squirrel.CONTROLS[event.key]

        for control in Squirrel.CONTROLS:
            if shared.keys[control]:
                self.direction = Squirrel.CONTROLS[control]

    def scan_surroundings(self):
        for entity in shared.entities:
            if entity.cell == self.cell:
                continue
            if (
                entity.cell == self.desired_cell
                and entity.movement_type == MovementType.PUSHED
                and isinstance(entity, Box)
            ):
                entity.direction = self.direction

            if (
                entity.cell == self.desired_cell
                and entity.movement_type == MovementType.STATIC
            ):
                self.direction = (0, 0)

    def update(self):
        self.scan_controls()
        super().update()
        self.scan_surroundings()


class Box(Entity):
    def __init__(self, cell) -> None:
        image = qload("box", False)
        super().__init__(cell, MovementType.PUSHED, image)

    def scan_surroundings(self):
        for entity in shared.entities:
            if entity.cell == self.cell:
                continue
            if (
                entity.cell == self.desired_cell
                and entity.movement_type == MovementType.PUSHED
            ):
                entity.direction = self.direction

            if (
                entity.cell == self.desired_cell
                and entity.movement_type == MovementType.STATIC
            ):
                self.direction = (0, 0)

    def update(self):
        super().update()
        self.scan_surroundings()


class Apricorn(Entity):
    def __init__(self, cell) -> None:
        image = qload("apricorn", True)
        super().__init__(cell, MovementType.PUSHED, image)


class Goal(Entity):
    def __init__(self, cell) -> None:
        image = pygame.Surface(shared.TILE_SIZE)
        image.fill((0, 0, 0))
        super().__init__(cell, MovementType.STATIC, image)

    def scan_surroundings(self):
        for entity in shared.entities:
            if entity.cell == self.cell:
                continue
            if entity.desired_cell == self.cell and isinstance(entity, Apricorn):
                shared.level_no += 1
                if shared.level_no == shared.MAX_LEVEL:
                    shared.victory = True

    def update(self):
        super().update()
        self.scan_surroundings()
