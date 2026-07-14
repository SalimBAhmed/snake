import pygame

from snake.screen import ScreenContext
from snake.screen.menu import MainMenu
from snake.settings import (
    BLOCK_SIZE,
    FPS,
    calculate_scaled_values,
    get_resolution,
)
from snake.sprites import load_spritesheet

WINDOW_WIDTH, WINDOW_HEIGHT = get_resolution()
GAME_WIDTH, GAME_HEIGHT = calculate_scaled_values()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game 🐍")
        self.clock = pygame.time.Clock()
        self.sprites = load_spritesheet("", BLOCK_SIZE, 4, 4)

        # Game state
        self.running = True
        self.screen_context = ScreenContext(MainMenu(sprites=self.sprites))

    def run(self) -> None:
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        exit(0)

    def handle_events(self) -> None:
        """Handle all input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.screen_context.handle_events(event)

    def update(self) -> None:
        """Update game state."""
        self.screen_context.update(self.clock)

    def draw(self) -> None:
        """Draw the current game state."""
        self.screen_context.draw(self.screen)

        pygame.display.flip()
