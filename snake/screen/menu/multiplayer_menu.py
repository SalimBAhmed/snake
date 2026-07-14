from snake.screen import MenuScreen
from snake.screen.game import MultiplayerGame, NetworkMultiplayerGame

class MultiplayerMenu(MenuScreen):
    menu_name: str = "Multiplayer"
    options: list[str] = ["classic", "network join", "network host", "back"]
    selected_option: int = 0

    def _process_menu_selection(self):
        option = self.get_option()
        if option == "back":
            self._context.transition_to_previous_screen()
        elif option == "network join":
            self._context.transition_to(NetworkMultiplayerGame())
        elif option == "network host":
            self._context.transition_to(NetworkMultiplayerGame(is_host=True))

        else:
            self._context.transition_to(MultiplayerGame())
