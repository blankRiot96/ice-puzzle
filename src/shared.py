import pygame

# Constants
ROWS = 10
COLS = 20
TILE_SIZE = 64
WIN_WIDTH = COLS * TILE_SIZE
WIN_HEIGHT = ROWS * TILE_SIZE
WIN_SIZE = (WIN_WIDTH, WIN_HEIGHT)

# Shared Variables
screen: pygame.Surface
events: list[pygame.Event]
