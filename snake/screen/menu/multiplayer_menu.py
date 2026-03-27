from snake.screen import MenuScreen
from snake.screen.game import MultiplayerGame

class MultiplayerMenu(MenuScreen):
    menu_name: str = "Multiplayer"
    options: list[str] = ["classic", "back"]
    selected_option: int = 0

    def _process_menu_selection(self):
        option = self.get_option()
        if option == "back":
            self._context.transition_to_previous_screen()
        else:
            self._context.transition_to(MultiplayerGame())