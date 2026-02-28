import os
from tarfile import BLOCKSIZE


def calculate_scale():
    global X_SCALE, Y_SCALE
    X_SCALE = WINDOW_WIDTH / BASE_WIDTH
    Y_SCALE = WINDOW_HEIGHT / BASE_HEIGHT


def calculate_scaled_values():
    global GAME_WIDTH, GAME_HEIGHT
    GAME_WIDTH = int(round(BASE_GAME_WIDTH * X_SCALE))
    BLOCK_SCALE = GAME_WIDTH // BLOCK_SIZE
    GAME_WIDTH = BLOCK_SCALE * BLOCK_SIZE
    GAME_HEIGHT = int(round(BASE_GAME_HEIGHT * Y_SCALE))
    BLOCK_SCALE = GAME_HEIGHT // BLOCK_SIZE
    GAME_HEIGHT = BLOCK_SCALE * BLOCK_SIZE
    return GAME_WIDTH, GAME_HEIGHT


def set_resolution(width, height):
    global WINDOW_WIDTH, WINDOW_HEIGHT
    WINDOW_WIDTH = int(width)
    WINDOW_HEIGHT = int(height)
    calculate_scale()
    calculate_scaled_values()


def get_resolution():
    global WINDOW_WIDTH, WINDOW_HEIGHT
    return WINDOW_WIDTH, WINDOW_HEIGHT


# Window
BASE_WIDTH = 600
BASE_HEIGHT = 320

WINDOW_WIDTH = BASE_WIDTH
WINDOW_HEIGHT = BASE_HEIGHT

calculate_scale()

BASE_GAME_WIDTH = 200
BASE_GAME_HEIGHT = 320


FPS = 120
BASE_BLOCK_SIZE = 20
BLOCK_SIZE = int(round(BASE_BLOCK_SIZE * X_SCALE))

calculate_scaled_values()

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Debug
DEBUG_MODE = os.getenv("DEBUG_MODE")
DEV_MODE = os.getenv("DEV_MODE")
