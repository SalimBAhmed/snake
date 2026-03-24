from abc import ABC, abstractmethod
from snake.settings import BLACK
import pygame

class Menu(ABC):
    """
    The Base State class declares operations common to all supported states.
    """
    _context: "MenuContext"
    menu_name: str
    options: list[str]
    selected_option: int

    @property
    def context(self) -> "MenuContext":
        return self._context

    @context.setter
    def context(self, context: "MenuContext") -> None:
        self._context = context

    def draw_title(self, screen):
        screen_width, screen_height = screen.get_size()
        title_size = int(screen_height * 0.1)  # 10% of screen height
        # Create fonts with dynamic sizes
        title_font = pygame.font.Font(None, title_size)
        # Draw title
        title = title_font.render(self.menu_name, True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen_width // 2, screen_height * 0.2))
        screen.blit(title, title_rect)

    def draw(self, screen):
        screen.fill(BLACK)
        screen_width, screen_height = screen.get_size()

        # Calculate font sizes based on screen dimensions
        option_size = int(screen_height * 0.05)  # 5% of screen height

        # Create fonts with dynamic sizes
        option_font = pygame.font.Font(None, option_size)
        self.draw_title(screen)
        # Calculate spacing between options
        option_spacing = screen_height * 0.15  # 15% of screen height
        start_y = screen_height * 0.4  # Start at 40% of screen height

        # Draw options
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = option_font.render(option, True, color)
            text_rect = text.get_rect(
                center=(screen_width // 2, start_y + i * option_spacing)
            )
            screen.blit(text, text_rect)

    def get_option(self):
        return self.options[self.selected_option]

    def next_option(self):
        if self.selected_option < len(self.options) - 1:
            self.selected_option += 1

    def previous_option(self):
        if self.selected_option > 0:
            self.selected_option -= 1

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.previous_option()
            elif event.key == pygame.K_DOWN:
                self.next_option()
            elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                self._process_menu_selection()

    @abstractmethod
    def _process_menu_selection(self) -> None:
        raise NotImplementedError


class MenuContext:
    """
    The Context defines the interface of interest to clients.
    """
    _menu: "Menu"
    _previous_menu = []
    def __init__(self, menu: "Menu") -> None:
        self.transition_to(menu)

    def transition_to(self, menu: "Menu") -> None:
        self._previous_menu.append(self._menu)
        self._menu = menu
        self._menu.context = self

    def transition_to_previous_menu(self) -> None:
        self.transition_to(self._previous_menu.pop())
