from abc import ABC, abstractmethod
from snake.settings import BLACK, BLOCK_SIZE
import pygame
from typing import ClassVar

class Screen(ABC):
    _context: "ScreenContext" = None
    _sprites: pygame.sprite.Group = None

    def __init__(self, sprites: pygame.sprite.Group = None) -> None:
        if Screen._sprites is None and sprites is not None:
            Screen._sprites = sprites

    @property
    def sprites(self) -> pygame.sprite.Group:
        return self._sprites

    @sprites.setter
    def sprites(self, sprites: pygame.sprite.Group) -> None:
        self._sprites = sprites

    @property
    def context(self) -> "ScreenContext":
        return self._context

    @context.setter
    def context(self, context: "ScreenContext") -> None:
        self._context = context
    
    @abstractmethod
    def draw(self, screen) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle_events(self, event: pygame.event.Event) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, clock) -> None:
        raise NotImplementedError

class MenuScreen(Screen):
    """
    The Base State class declares operations common to all supported states.
    """
    menu_name: str
    options: list[str]
    selected_option: int

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

    def update(self, clock) -> None:
        pass

    @abstractmethod
    def _process_menu_selection(self) -> None:
        raise NotImplementedError

class GameScreen(Screen):

    @abstractmethod
    def draw(self, screen):
        raise NotImplementedError

    @abstractmethod
    def handle_events(self, event: pygame.event.Event) -> None:
        raise NotImplementedError

class ScreenContext:
    """
    The Context defines the interface of interest to clients.
    """
    _screen: "Screen" = None
    _previous_screen = []

    def __init__(self, screen: "Screen") -> None:
        self.transition_to(screen)

    def transition_to(self, screen: "Screen") -> None:
        self._previous_screen.append(self._screen)
        self._screen = screen
        self._screen.context = self

    def transition_to_previous_screen(self) -> None:
        self._screen = self._previous_screen.pop()
        self._screen.context = self

    def handle_events(self, event: pygame.event.Event) -> None:
        self._screen.handle_events(event)

    def update(self, clock) -> None:
        self._screen.update(clock)

    def draw(self, screen) -> None:
        self._screen.draw(screen)