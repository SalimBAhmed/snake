import pygame
import sys
from typing import ClassVar, List, Optional, Dict
from snake.settings import (
    GAME_HEIGHT,
    GAME_WIDTH,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    BLOCK_SIZE,
    RIGHT,
)
from snake.player import Player
from snake.sprites import load_spritesheet
from snake.menu import PauseMenu, GameMenu, SinglePlayerMenu, MultiplayerMenu, Menu
from snake.ui import UI, SinglePlayerUI, MultiplayerUI
from snake.food_generator import FoodGenerator
from snake.mode import SinglePlayerMode, MultiplayerMode


class Game:
    menu: ClassVar[Dict[str, Menu]] = {
        "game_menu": GameMenu,
        "single_player_menu": SinglePlayerMenu,
        "multiplayer_menu": MultiplayerMenu,
        "pause_menu": PauseMenu,
    }

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game 🐍")
        self.clock = pygame.time.Clock()
        self.sprites = load_spritesheet("", BLOCK_SIZE, 4, 4)

        # Game state
        self.running = True
        self.started = False
        self.menu_option = None
        self.in_menu = True
        self.menu_type = "game_menu"
        self.ui: Optional[UI] = None
        self.powerup_available = False
        self.players: List[Player] = []
        self.food_generator = FoodGenerator()
        self.mode = None

    def setup_players(self, player_count: int) -> None:
        """Initialize players based on game mode."""
        self.players.clear()

        if player_count == 1:
            # Single player in the middle of the screen
            self.players.append(
                Player(
                    self.sprites,
                    start_pos=(GAME_WIDTH // 2, GAME_HEIGHT // 2),
                    start_direction=RIGHT,
                    player_id=1,
                )
            )
        else:
            # Two players on opposite sides
            self.players.append(
                Player(
                    self.sprites,
                    start_pos=(GAME_WIDTH // 2, GAME_HEIGHT // 2),
                    start_direction=RIGHT,
                    player_id=1,
                )
            )
            self.players.append(
                Player(
                    self.sprites,
                    start_pos=((GAME_WIDTH // 2) + 400, GAME_HEIGHT // 2),
                    start_direction=RIGHT,
                    player_id=2,
                )
            )

    def run(self) -> None:
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def reset(self, player_id=None) -> None:
        """Reset the game state."""
        player_count = len(self.players)
        self.setup_players(player_count)
        self.food_generator.destroy(player_id)
        self.started = False

    def handle_events(self) -> None:
        """Handle all input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.in_menu:
                self._handle_menu_events(event)
            elif event.type == pygame.KEYDOWN:
                self._handle_game_events(event)

    def _handle_menu_events(self, event: pygame.event.Event) -> None:
        """Handle events when in the game menu."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                Game.menu[self.menu_type].previous_option()
            elif event.key == pygame.K_DOWN:
                Game.menu[self.menu_type].next_option()
            elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                self._process_menu_selection()

    def _process_menu_selection(self) -> None:
        """Process the selected menu option."""
        self.menu_option = Game.menu[self.menu_type].get_option()
        print(self.menu_option)
        if self.menu_option.upper() == "EXIT":
            self.running = False
        else:
            if self.menu_type == "game_menu":
                self.menu_type = (
                    "single_player_menu"
                    if self.menu_option == "single_player"
                    else "multiplayer_menu"
                )
            elif self.menu_type == "single_player_menu":
                self.mode = SinglePlayerMode()
                self.setup_players(1)
                self.in_menu = False
                self.started = True
            elif self.menu_type == "multiplayer_menu":
                self.mode = MultiplayerMode()
                self.setup_players(2)
                self.in_menu = False
                self.started = True
            elif self.menu_type == "pause_menu":
                self.in_menu = False
                self.started = True

    def _handle_game_events(self, event: pygame.event.Event) -> None:
        """Handle events during gameplay."""
        if event.key == pygame.K_ESCAPE:
            self.in_menu = not self.in_menu
            self.menu_type = "pause_menu"
        elif not self.in_menu:
            # Pass input to all players
            for player in self.players:
                player.handle_input(event.key)
        self.started = not self.in_menu

    def update(self) -> None:
        """Update game state."""
        if not self.started or self.in_menu:
            return
        # Update players
        for player in self.players:
            player.update(self.clock.get_time())

            # Check if player can move
            if player.can_move():
                self.food_generator.generate(player.player_id)
                # Check for collisions with food
                self._check_food_collisions(player)

                # Move the player
                player.move()
                self._check_food_collisions(player)
                # Check for collisions with walls or self
                if self._check_collisions(player):
                    self.reset(player.player_id)

    def _check_food_collisions(self, player: Player) -> None:
        """Check if player collides with food."""
        # Check regular food
        food = self.food_generator.get(player.player_id, "food")
        if food and player.check_collision(food.position[0], food.position[1]):
            player.grow()
            self.food_generator.destroy(player.player_id, "food")

        # Check power-ups
        for powerup_type in ["slow_down"]:  # Add more power-up types as needed
            powerup = self.food_generator.get(player.player_id, powerup_type)
            if powerup and player.check_collision(
                powerup.position[0], powerup.position[1]
            ):
                powerup.apply(player)
                self.food_generator.destroy(player.player_id, powerup_type)

    def _check_collisions(self, player: Player) -> bool:
        """Check for collisions with walls or self."""
        head = player.body[0]

        # Wall collision
        min_x = 0
        max_x = GAME_WIDTH
        if player.player_id == 2:
            min_x = 400
            max_x = GAME_WIDTH + 400
        if head.x < min_x or head.x >= max_x or head.y < 0 or head.y >= GAME_HEIGHT:
            return True

        # Self collision
        if player.check_self_collision():
            return True

        # # Player-player collision (for multiplayer)
        # for other in self.players:
        #     if other != player and other.check_collision(head.x, head.y, include_head=False):
        #         return True

        return False

    def draw(self) -> None:
        """Draw the current game state."""

        if self.in_menu:
            Game.menu[self.menu_type].draw(self.screen)
        else:
            if isinstance(self.mode, SinglePlayerMode):
                self.ui = SinglePlayerUI(self.screen)
            elif isinstance(self.mode, MultiplayerMode):
                self.ui = MultiplayerUI(self.screen)
            self.ui.draw()
            for player in self.players:
                player.draw(self.screen)
            self.food_generator.draw(self.screen)

        pygame.display.flip()
