from snake.state_menu import Menu
from .single_player_menu import SinglePlayerMenu

class MainMenu(Menu):
    menu_name: str = "Main Menu"
    options: list[str] = ["single_player", "multiplayer", "settings", "exit"]
    selected_option: int = 0

    def _process_menu_selection(self):
        option = self.get_option()
        if option == "single_player":
            self._context.transition_to(SinglePlayerMenu())
        else:
            print(f"Selected option: {option}")