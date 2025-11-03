import pygame
from snake.settings import BLACK
class GameMenu:
    def __init__(self):
        self.selected_option = 0
        self.options = ["single_player", "multiplayer", "exit"]

    def draw(self, screen):
        screen.fill(BLACK)
        screen_width, screen_height = screen.get_size()
        
        # Calculate font sizes based on screen dimensions
        title_size = int(screen_height * 0.1)  # 10% of screen height
        option_size = int(screen_height * 0.05)  # 5% of screen height
        
        # Create fonts with dynamic sizes
        title_font = pygame.font.Font(None, title_size)
        option_font = pygame.font.Font(None, option_size)
        
        # Draw title
        title = title_font.render("Game Menu", True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen_width // 2, screen_height * 0.2))
        screen.blit(title, title_rect)
        
        # Calculate spacing between options
        option_spacing = screen_height * 0.15  # 15% of screen height
        start_y = screen_height * 0.4  # Start at 40% of screen height
        
        # Draw options
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = option_font.render(option, True, color)
            text_rect = text.get_rect(center=(screen_width // 2, start_y + i * option_spacing))
            screen.blit(text, text_rect)
    
    def get_option(self):
        return self.options[self.selected_option]
    def next_option(self):
        if self.selected_option < len(self.options) - 1:
            self.selected_option += 1
    def previous_option(self):
        if self.selected_option > 0:
            self.selected_option -= 1
class PauseMenu:
    def __init__(self):
        self.selected_option = 0
        self.options = ["Resume"]
        
    def draw(self, screen):
        screen.fill(BLACK)
        screen_width, screen_height = screen.get_size()
        
        # Calculate font sizes based on screen dimensions
        title_size = int(screen_height * 0.1)  # 10% of screen height
        option_size = int(screen_height * 0.05)  # 5% of screen height
        
        # Create fonts with dynamic sizes
        title_font = pygame.font.Font(None, title_size)
        option_font = pygame.font.Font(None, option_size)
        
        # Draw title
        title = title_font.render("Pause Menu", True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen_width // 2, screen_height * 0.2))
        screen.blit(title, title_rect)
        
        # Calculate spacing between options
        option_spacing = screen_height * 0.15  # 15% of screen height
        start_y = screen_height * 0.4  # Start at 40% of screen height
        
        # Draw options
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = option_font.render(option, True, color)
            text_rect = text.get_rect(center=(screen_width // 2, start_y + i * option_spacing))
            screen.blit(text, text_rect)
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return self.options[self.selected_option]
        return None 