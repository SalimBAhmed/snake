import pygame

from snake.settings import BLACK, BLOCK_SIZE, GAME_HEIGHT, GAME_WIDTH


class UI:
    def __init__(self, screen):
        self.screen = screen
        self.draw()

    def draw(self):
        pass

class SinglePlayerUI(UI):
    def __init__(self, screen):
        super().__init__(screen)

    
    def draw(self):
        self.screen.fill(BLACK)
        game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        light_green_tile = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        light_green_tile.fill((207, 255, 112))

        dark_green_tile = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        dark_green_tile.fill((60, 163, 112))
        for x in range(0, game_surface.get_width(), BLOCK_SIZE):
            for y in range(0, game_surface.get_height(), BLOCK_SIZE):
                if ((x + y)/BLOCK_SIZE) % 2 == 0:
                    game_surface.blit(light_green_tile, (x, y))
                else:
                    game_surface.blit(dark_green_tile, (x, y))
        self.screen.blit(game_surface, (0, 0))

class MultiplayerUI(UI):
    def __init__(self, screen):
        super().__init__(screen)

    
    def draw(self):
        self.screen.fill(BLACK)
        game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        light_green_tile = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        light_green_tile.fill((207, 255, 112))

        dark_green_tile = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        dark_green_tile.fill((60, 163, 112))
        for x in range(0, game_surface.get_width(), BLOCK_SIZE):
            for y in range(0, game_surface.get_height(), BLOCK_SIZE):
                if ((x + y)/BLOCK_SIZE) % 2 == 0:
                    game_surface.blit(light_green_tile, (x, y))
                else:
                    game_surface.blit(dark_green_tile, (x, y))
        self.screen.blit(game_surface, (0, 0))
        self.screen.blit(game_surface, (400, 0))