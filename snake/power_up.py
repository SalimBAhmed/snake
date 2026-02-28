import random
from snake.settings import (
    BLOCK_SIZE,
    BLUE,
    calculate_scaled_values,
    get_resolution,
)
import pygame

GAME_WIDTH, GAME_HEIGHT = calculate_scaled_values()


class PowerUp:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()

    def spawn(self, player_id: int = 1):
        GAME_WIDTH, GAME_HEIGHT = calculate_scaled_values()
        WINDOW_WIDTH, WINDOW_HEIGHT = get_resolution()

        base_x = 0
        if player_id == 2:
            base_x += WINDOW_WIDTH - GAME_WIDTH
        self.position = (
            base_x + random.randint(0, (GAME_WIDTH - 1) // BLOCK_SIZE) * BLOCK_SIZE,
            random.randint(0, (GAME_HEIGHT - 1) // BLOCK_SIZE) * BLOCK_SIZE,
        )

    def draw(self, screen):
        pygame.draw.rect(
            screen, BLUE, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE)
        )

    def apply(self, snake):
        pass


class SlowDown(PowerUp):
    def __init__(self):
        super().__init__()

    def apply(self, snake):
        super().apply(snake)
        snake.speed_score -= 1
        snake.speed_score = max(1, snake.speed_score)
