import pygame

from snake.screen import MenuScreen
from snake.screen.menu.multiplayer_menu import MultiplayerMenu
from snake.screen.menu.settings_menu import SettingsMenu
from snake.screen.menu.single_player_menu import SinglePlayerMenu


class MainMenu(MenuScreen):
    menu_name: str = "Main Menu"
    options: list[str] = ["Single Player", "Multiplayer", "Settings", "Exit"]
    selected_option: int = 0

    def _process_menu_selection(self):
        option = self.get_option()
        if option == "Single Player":
            self._context.transition_to(SinglePlayerMenu())
        elif option == "Multiplayer":
            self._context.transition_to(MultiplayerMenu())
        elif option == "Settings":
            self._context.transition_to(SettingsMenu())
        elif option == "Exit":
            pygame.quit()
            exit(0)
        else:
            print(f"Selected option: {option}")
