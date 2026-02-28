from abc import abstractmethod
import pygame
from snake.settings import BLACK, WINDOW_HEIGHT, WINDOW_WIDTH, set_resolution


class Menu:
    def __init__(self):
        self.selected_option: int = 0
        self.options: list[str] = []
        self.menu_name: str = ""
        self.menu_type: str = ""

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


class MainMenu(Menu):
    def __init__(self):
        self.selected_option: int = 0
        self.options: list[str] = ["single_player", "multiplayer", "settings", "exit"]
        self.menu_name: str = "Main Menu"
        self.menu_type: str = "main_menu"

    def _process_menu_selection(self):
        option = self.get_option()


class SinglePlayerMenu(Menu):
    def __init__(self):
        self.selected_option: int = 0
        self.options: list[str] = ["classic", "infinite", "back"]
        self.menu_name: str = "Single Player Menu"
        self.menu_type: str = "single_player_menu"


class MultiplayerMenu(Menu):
    def __init__(self):
        self.selected_option: int = 0
        self.options: list[str] = [
            "classic",
            "infinite",
            "co-op",
            "mode (local / lan)",
            "back",
        ]
        self.menu_name: str = "Multiplayer Menu"
        self.menu_type: str = "multiplayer_menu"


class PauseMenu(Menu):
    def __init__(self):
        self.selected_option: int = 0
        self.options: list[str] = ["Resume", "Menu", "Exit"]
        self.menu_name: str = "Pause Menu"
        self.menu_type: str = "pause_menu"


class SettingsMenu(Menu):
    def __init__(self):
        self.selected_option: int = 0
        self.options: list[str] = ["Resolution", "Window Type", "Back"]
        self.menu_name: str = "Settings Menu"
        self.menu_type: str = "settings_menu"

        # Settings state
        self.in_submenu = False
        self.submenu_type = None

        # Resolution presets
        self.resolution_presets = ["800x600", "1024x768", "1280x720", "1920x1080"]
        self.current_resolution_index = 0

        # Window types
        self.window_types = ["Windowed", "Fullscreen", "Borderless"]
        self.current_window_type_index = 0

        # Submenu selection indices
        self.resolution_selection = 0
        self.window_type_selection = 0

        self.resolution_changed = False
        self.window_type_changed = False

    def draw(self, screen):
        if self.in_submenu:
            self._draw_submenu(screen)
        else:
            super().draw(screen)

    def _draw_submenu(self, screen):
        screen.fill(BLACK)
        screen_width, screen_height = screen.get_size()

        # Calculate font sizes
        title_size = int(screen_height * 0.08)
        option_size = int(screen_height * 0.05)

        title_font = pygame.font.Font(None, title_size)
        option_font = pygame.font.Font(None, option_size)

        # Draw submenu title
        title = title_font.render(self.submenu_type, True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen_width // 2, screen_height * 0.2))
        screen.blit(title, title_rect)

        # Draw options
        if self.submenu_type == "Resolution":
            options = self.resolution_presets
            selected_index = self.resolution_selection
        else:  # Window Type
            options = self.window_types
            selected_index = self.window_type_selection

        option_spacing = screen_height * 0.12
        start_y = screen_height * 0.35

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected_index else (255, 255, 255)
            text = option_font.render(option, True, color)
            text_rect = text.get_rect(
                center=(screen_width // 2, start_y + i * option_spacing)
            )
            screen.blit(text, text_rect)

        # Draw back instruction
        back_text = option_font.render("ESC to go back", True, (200, 200, 200))
        back_rect = back_text.get_rect(center=(screen_width // 2, screen_height * 0.85))
        screen.blit(back_text, back_rect)

    def handle_events(self, event: pygame.event.Event) -> dict | None:
        if self.in_submenu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.in_submenu = False
                    self.submenu_type = None
                elif event.key == pygame.K_UP:
                    if self.submenu_type == "Resolution":
                        if self.resolution_selection > 0:
                            self.resolution_selection -= 1
                    else:  # Window Type
                        if self.window_type_selection > 0:
                            self.window_type_selection -= 1
                elif event.key == pygame.K_DOWN:
                    if self.submenu_type == "Resolution":
                        if self.resolution_selection < len(self.resolution_presets) - 1:
                            self.resolution_selection += 1
                    else:  # Window Type
                        if self.window_type_selection < len(self.window_types) - 1:
                            self.window_type_selection += 1
                elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    # Apply selection (for now, just store it)
                    if self.submenu_type == "Resolution":
                        if self.resolution_selection != self.current_resolution_index:
                            self.resolution_changed = True
                        self.current_resolution_index = self.resolution_selection

                    else:  # Window Type
                        if self.window_type_selection != self.current_window_type_index:
                            self.window_type_changed = True
                        self.current_window_type_index = self.window_type_selection
                    self.in_submenu = False
                    self.submenu_type = None
                    res = {
                        "resolution": tuple(
                            self.resolution_presets[
                                self.current_resolution_index
                            ].split("x")
                        ),
                        "window_type": self.window_types[
                            self.current_window_type_index
                        ],
                    }
                    set_resolution(
                        *res.get("resolution", (WINDOW_HEIGHT, WINDOW_WIDTH))
                    )
                    changed = self.resolution_changed or self.window_type_changed
                    self.resolution_changed = False
                    self.window_type_changed = False
                    return changed

        else:
            super().handle_events(event)

    def _process_menu_selection(self):
        option = self.get_option()

        if option == "Resolution":
            self.in_submenu = True
            self.submenu_type = "Resolution"
        elif option == "Window Type":
            self.in_submenu = True
            self.submenu_type = "Window Type"
        elif option == "Back":
            # This will be handled by the game class
            pass
