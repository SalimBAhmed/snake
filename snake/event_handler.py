import pygame
from pygame.event import Event
from snake.game_state import GameState
from snake import menu
from snake.player import Player
from snake.settings import RIGHT, calculate_scaled_values

GAME_WIDTH, GAME_HEIGHT = calculate_scaled_values()


class EventHandler:
    def __init__(self):
        self.handler = {"menu": MenuHandler(), "game": GameHandler()}

    def handle(self, event: Event, game_state: GameState):
        self.handler[game_state.state].handle(event, game_state)


class MenuHandler:
    def __init__(self):
        self.menu = None

    def handle(self, event: Event, game_state: GameState):
        if event.key in (pygame.K_SPACE, pygame.K_RETURN):
            self.navigate_menu(game_state)

    def navigate_menu(self, game_state: GameState):
        menu_option = game_state.menu.get_option()
        if menu_option.upper() == "EXIT":
            game_state.running = False
        else:
            if isinstance(game_state.menu, menu.MainMenu):
                if menu_option == "single_player":
                    game_state.menu = menu.SinglePlayerMenu()
                elif menu_option == "multiplayer":
                    game_state.menu = menu.MultiplayerMenu()
            elif isinstance(game_state.menu, menu.SinglePlayerMenu):
                game_state.players = self.setup_players(1)
                game_state.in_menu = False
                game_state.started = True
            elif isinstance(game_state.menu, menu.MultiplayerMenu):
                game_state.players = self.setup_players(2)
                game_state.in_menu = False
                game_state.started = True
            elif isinstance(game_state.menu, menu.PauseMenu):
                game_state.in_menu = False
                game_state.started = True

    def setup_players(self, player_count: int) -> list[Player]:
        """Initialize players based on game mode."""
        players = []
        if player_count == 1:
            # Single player in the middle of the screen
            players.append(
                Player(
                    self.sprites,
                    start_pos=(GAME_WIDTH // 2, GAME_HEIGHT // 2),
                    start_direction=RIGHT,
                    player_id=1,
                )
            )
        else:
            # Two players on opposite sides
            players.append(
                Player(
                    self.sprites,
                    start_pos=(GAME_WIDTH // 2, GAME_HEIGHT // 2),
                    start_direction=RIGHT,
                    player_id=1,
                )
            )
            players.append(
                Player(
                    self.sprites,
                    start_pos=((GAME_WIDTH // 2) + 400, GAME_HEIGHT // 2),
                    start_direction=RIGHT,
                    player_id=2,
                )
            )
        return players


class GameHandler:
    def handle(self, event: Event, game_state: GameState):
        pass
