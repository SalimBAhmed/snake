import os
import pygame
from snake.screen import MenuScreen
from snake.settings import set_resolution, get_resolution

class SettingsMenu(MenuScreen):
    menu_name: str = "Settings Menu"

    def __init__(self, sprites: pygame.sprite.Group = None) -> None:
        super().__init__(sprites)
        self.resolution_presets = ["800x600", "1024x768", "1280x720", "1920x1080"]
        
        # Get dynamic current resolution
        current_width, current_height = get_resolution()
        current_res = f"{current_width}x{current_height}"
        if current_res in self.resolution_presets:
            self.current_resolution_index = self.resolution_presets.index(current_res)
        else:
            self.current_resolution_index = 0
            
        self.window_types = ["Windowed", "Fullscreen", "Borderless"]
        
        # Try to infer current window type from active display if any
        self.current_window_type_index = 0
        surface = pygame.display.get_surface()
        if surface is not None:
            flags = surface.get_flags()
            if flags & pygame.FULLSCREEN:
                self.current_window_type_index = 1
            elif flags & pygame.NOFRAME:
                self.current_window_type_index = 2
        
        self.selected_option = 0
        self.update_options()

    def update_options(self) -> None:
        res_str = self.resolution_presets[self.current_resolution_index]
        win_str = self.window_types[self.current_window_type_index]
        self.options = [
            f"Resolution: < {res_str} >",
            f"Window Type: < {win_str} >",
            "Apply",
            "Back"
        ]

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self._handle_left()
            elif event.key == pygame.K_RIGHT:
                self._handle_right()
            else:
                super().handle_events(event)
        else:
            super().handle_events(event)

    def _handle_left(self) -> None:
        if self.selected_option == 0:  # Resolution
            self.current_resolution_index = (self.current_resolution_index - 1) % len(self.resolution_presets)
            self.update_options()
        elif self.selected_option == 1:  # Window Type
            self.current_window_type_index = (self.current_window_type_index - 1) % len(self.window_types)
            self.update_options()

    def _handle_right(self) -> None:
        if self.selected_option == 0:  # Resolution
            self.current_resolution_index = (self.current_resolution_index + 1) % len(self.resolution_presets)
            self.update_options()
        elif self.selected_option == 1:  # Window Type
            self.current_window_type_index = (self.current_window_type_index + 1) % len(self.window_types)
            self.update_options()

    def _process_menu_selection(self) -> None:
        if self.selected_option == 2:  # Apply
            res_str = self.resolution_presets[self.current_resolution_index]
            width, height = map(int, res_str.split('x'))
            set_resolution(width, height)
            
            win_str = self.window_types[self.current_window_type_index]
            flags = 0
            if win_str == "Fullscreen":
                flags = pygame.FULLSCREEN
            elif win_str == "Borderless":
                flags = pygame.NOFRAME
            
            # This centers the Pygame window whenever resolution/mode changes
            os.environ['SDL_VIDEO_CENTERED'] = '1'
            pygame.display.set_mode((width, height), flags)
            
        elif self.selected_option == 3:  # Back
            self._context.transition_to_previous_screen()