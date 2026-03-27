from snake.screen import GameScreen
import pygame
from snake.settings import BLACK, calculate_scaled_values, BLOCK_SIZE, get_resolution, RIGHT
from snake.player import Player
from snake.food_generator import FoodGenerator
from snake.collision_handler import CollisionHandlerFactory
from snake.screen.menu.pause_menu import PauseMenu

class MultiplayerGame(GameScreen):
    def __init__(self):
        self.players = self.setup_players()
        self.food_generator = FoodGenerator()
        self.collision_chain = CollisionHandlerFactory.create_chain()
        self.started = False

    def setup_players(self):
        GAME_WIDTH, GAME_HEIGHT = calculate_scaled_values()
        WINDOW_WIDTH, WINDOW_HEIGHT = get_resolution()
        starting_position_x = (GAME_WIDTH // (2 * BLOCK_SIZE)) * BLOCK_SIZE
        starting_position_y = (GAME_HEIGHT // (2 * BLOCK_SIZE)) * BLOCK_SIZE
        
        # Single player in the middle of the screen
        players = []
        players.append(
                Player(
                    self._sprites,
                    start_pos=(starting_position_x, starting_position_y),
                    start_direction=RIGHT,
                    player_id=1,
                )
            )
        players.append(
                Player(
                    self._sprites,
                    start_pos=(
                        starting_position_x + WINDOW_WIDTH - GAME_WIDTH,
                        starting_position_y,
                    ),
                    start_direction=RIGHT,
                    player_id=2,
                )
            )
        return players

    def draw(self, screen):
        screen.fill(BLACK)
        GAME_WIDTH, GAME_HEIGHT = calculate_scaled_values()
        WINDOW_WIDTH, WINDOW_HEIGHT = get_resolution()
        game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        light_green_tile = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        light_green_tile.fill((207, 255, 112))

        dark_green_tile = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        dark_green_tile.fill((60, 163, 112))
        for x in range(0, game_surface.get_width(), BLOCK_SIZE):
            for y in range(0, game_surface.get_height(), BLOCK_SIZE):
                if ((x + y) / BLOCK_SIZE) % 2 == 0:
                    game_surface.blit(light_green_tile, (x, y))
                else:
                    game_surface.blit(dark_green_tile, (x, y))
        screen.blit(game_surface, (0, 0))
        screen.blit(game_surface, (WINDOW_WIDTH - GAME_WIDTH, 0))

        for player in self.players:
            player.draw(screen)
        self.food_generator.draw(screen)

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.context.transition_to(PauseMenu())
            else:
                self.started = True
                for player in self.players:
                    player.handle_input(event.key)

    def update(self, clock) -> None:
        """Update game state."""
        if not self.started:
            return
        # Update players
        for player in self.players:
            player.update(clock.get_time())

            # Check if player can move
            if player.can_move():
                self.food_generator.generate(player.player_id)
                
                # Check for collisions before moving (food & powerup checks + potential bounds check)
                if self.collision_chain.handle(self, player):
                    self.reset(player.player_id)
                    continue

                # Move the player
                player.move()
                
                # Check for collisions after moving (food, powerup, walls, self)
                if self.collision_chain.handle(self, player):
                    self.reset(player.player_id)
                    continue

    def reset(self, player_id: int) -> None:
        """Reset the game."""
        self.players = self.setup_players()
        for player in self.players:
            self.food_generator.destroy(player.player_id)
        self.started = False