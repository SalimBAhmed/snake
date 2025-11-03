import os

# Window
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 320
GAME_WIDTH = 200
GAME_HEIGHT = 320
FPS = 120
BLOCK_SIZE = 20

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Debug
DEBUG_MODE = os.getenv("DEBUG_MODE")
DEV_MODE = os.getenv("DEV_MODE")
