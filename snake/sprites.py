import pygame

def load_spritesheet(path, sprite_size, cols, rows):
    """Load a sprite sheet and return a dict of subsurfaces."""
    snake_head = pygame.image.load("snake/assets/head_no_mouth.png").convert_alpha()
    snake_body = pygame.image.load("snake/assets/snake_body.png").convert_alpha()
    snake_body_corner = pygame.image.load("snake/assets/snake_body_corner.png").convert_alpha()
    snake_tail = pygame.image.load("snake/assets/snake_tail.png").convert_alpha()
    tile = pygame.image.load("snake/assets/background.png").convert_alpha()
    sprites = {"head": snake_head, "body": snake_body, "body_corner": snake_body_corner, "tail": snake_tail, "tile": tile}

    for key, sprite in sprites.items():
        x = 0
        y = 0
        sprite = sprite.subsurface(pygame.Rect(x, y, sprite_size, sprite_size))
        sprites[key] = sprite
    return sprites