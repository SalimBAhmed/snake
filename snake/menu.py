from typing import ClassVar
import pygame
from snake.settings import BLACK

class Menu:
    selected_option: ClassVar[int] = 0
    options: ClassVar[list[str]] = []
    menu_name: ClassVar[str] = ""
    menu_type: ClassVar[str] = ""

    @classmethod
    def draw_title(cls, screen):
        screen_width, screen_height = screen.get_size()
        title_size = int(screen_height * 0.1)  # 10% of screen height
        # Create fonts with dynamic sizes
        title_font = pygame.font.Font(None, title_size)
        # Draw title
        title = title_font.render(cls.menu_name, True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen_width // 2, screen_height * 0.2))
        screen.blit(title, title_rect)
    
    @classmethod
    def draw(cls, screen):
        screen.fill(BLACK)
        screen_width, screen_height = screen.get_size()
        
        # Calculate font sizes based on screen dimensions
        option_size = int(screen_height * 0.05)  # 5% of screen height
        
        # Create fonts with dynamic sizes
        option_font = pygame.font.Font(None, option_size)
        cls.draw_title(screen)
        # Calculate spacing between options
        option_spacing = screen_height * 0.15  # 15% of screen height
        start_y = screen_height * 0.4  # Start at 40% of screen height
        
        # Draw options
        for i, option in enumerate(cls.options):
            color = (255, 255, 0) if i == cls.selected_option else (255, 255, 255)
            text = option_font.render(option, True, color)
            text_rect = text.get_rect(center=(screen_width // 2, start_y + i * option_spacing))
            screen.blit(text, text_rect)
    
    @classmethod
    def get_option(cls):
        return cls.options[cls.selected_option]
    @classmethod
    def next_option(cls):
        if cls.selected_option < len(cls.options) - 1:
            cls.selected_option += 1
    @classmethod
    def previous_option(cls):
        if cls.selected_option > 0:
            cls.selected_option -= 1

class GameMenu(Menu):
    selected_option: ClassVar[int] = 0
    options: ClassVar[list[str]] = ["single_player", "multiplayer", "exit"]
    menu_name: ClassVar[str] = "Game Menu"
    menu_type: ClassVar[str] = "game_menu"
    

class SinglePlayerMenu(Menu):
    selected_option: ClassVar[int] = 0
    options: ClassVar[list[str]] = ["classic", "infinite", "back"]
    menu_name: ClassVar[str] = "Single Player Menu"
    menu_type: ClassVar[str] = "single_player_menu"

class MultiplayerMenu(Menu):
    selected_option: ClassVar[int] = 0
    options: ClassVar[list[str]] = ["classic", "infinite", "co-op", "mode (local / lan)", "back"]
    menu_name: ClassVar[str] = "Multiplayer Menu"
    menu_type: ClassVar[str] = "multiplayer_menu"

class PauseMenu(Menu):
    selected_option: ClassVar[int] = 0
    options: ClassVar[list[str]] = ["Resume", "Menu", "Exit"]
    menu_name: ClassVar[str] = "Pause Menu"    
    menu_type: ClassVar[str] = "pause_menu"