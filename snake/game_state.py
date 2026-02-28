from typing import List
from snake.menu import MainMenu
from snake.player import Player
from snake.food_generator import FoodGenerator


class GameState:
    def __init__(self):
        self.running = True
        self.state = "menu"
        # Menu State
        self.menu_option = None
        self.menu = MainMenu()
        # Game State
        self.started = False
        self.powerup_available = False
        self.players: List[Player] = []
        self.food_generator = FoodGenerator()
