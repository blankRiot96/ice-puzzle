import abc
import itertools

import pygame

import src.shared as shared
from src.enums import MovementType
from src.utils import Time


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
            self.moving = True

    def snowball_collider(self) -> bool:
        for snowball in shared.snowballs:
            if snowball.rect.colliderect(self.rect):
                snowball.alive = False
                return True
        return False

    def update(self):
        self.move()
        self.transfer_cell()

    def draw(self):
        shared.screen.blit(self.image, self.rect)


class Enemy(Entity):
    def __init__(self, cell_start, cell_end) -> None:
        image = qload("enemy", True)
        super().__init__(cell_start, MovementType.FIXED, image)
        self.original_cell = itertools.cycle(
            (self.cell.copy(), pygame.Vector2(cell_end))
        )

        self.cell_movement = cell_end[0] - cell_start[0]
        self.direction = (self.cell_movement, 0)

    def update(self):
        super().update()

        if self.pos == self.desired_pos:
            self.cell_movement *= -1
            self.direction = (self.cell_movement, 0)
            self.desired_cell = next(self.original_cell)

        if self.rect.colliderect(shared.player.rect):
            shared.retry = True


class Snowball:
    SPEED = 500.0

    def __init__(self, start_pos, direction) -> None:
        self.image = qload("snowball", True)
        self.image = pygame.transform.scale_by(self.image, 0.5)
        self.rect = self.image.get_rect()
        self.start_pos = pygame.Vector2(start_pos)
        self.pos = self.start_pos.copy()
        self.direction = direction
        self.alive = True

    def update(self):
        self.pos.x += self.direction * Snowball.SPEED * shared.dt

        self.rect.center = self.pos

    def draw(self):
        shared.screen.blit(self.image, self.rect)


class Launcher(Entity):
    def __init__(self, cell, m_direction=-1) -> None:
        self.m_direction = m_direction
        image = qload("launcher", True)
        image = pygame.transform.flip(image, m_direction > 0, False)
        super().__init__(cell, MovementType.STATIC, image)
        shared.snowballs = []
        self.timer = Time(0.3)

    def update(self):
        super().update()

        if self.timer.tick():
            shared.snowballs.append(Snowball(self.rect.center, self.m_direction))

        for snowball in shared.snowballs[:]:
            snowball.update()

            if not snowball.alive:
                shared.snowballs.remove(snowball)

    def draw(self):
        super().draw()
        for snowball in shared.snowballs:
            snowball.draw()


class LauncherLeft(Launcher):
    def __init__(self, cell) -> None:
        super().__init__(cell, -1)


class LauncherRight(Launcher):
    def __init__(self, cell) -> None:
        super().__init__(cell, 1)


class Wall(Entity):
    def __init__(self, cell: tuple[int, int]) -> None:
        image = qload("wall", False)
        super().__init__(cell, MovementType.STATIC, image)

    def update(self):
        super().update()
        self.snowball_collider()


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
        self.image_still = qload("squirrel_still", True)
        self.image_still = pygame.transform.flip(self.image_still, True, False)
        self.image_right = image.copy()
        self.image_left = pygame.transform.flip(image, True, False)
        super().__init__(cell, MovementType.CONTROLLED, image)
        shared.player = self

    def handle_anim(self):
        if not self.direction[0]:
            return
        if self.direction[0] > 0:
            self.image = self.image_left
        else:
            self.image = self.image_right

    def scan_controls(self):
        if self.moving:
            self.handle_anim()
            return
        else:
            self.image = self.image_still

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

    def snowball_collider(self):
        if super().snowball_collider():
            shared.retry = True

    def update(self):
        self.scan_controls()
        super().update()
        self.scan_surroundings()
        self.snowball_collider()


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
        self.snowball_collider()


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

    def update(self):
        super().update()
        self.scan_surroundings()
