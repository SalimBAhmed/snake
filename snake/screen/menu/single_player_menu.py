from snake.screen import MenuScreen
from snake.screen.game.single_player_game import SinglePlayerGame

class SinglePlayerMenu(MenuScreen):
    menu_name: str = "Single Player"
    options: list[str] = ["classic", "infinite", "back"]
    selected_option: int = 0

    def _process_menu_selection(self):
        option = self.get_option()
        if option == "back":
            self._context.transition_to_previous_screen()
        else:
            self._context.transition_to(SinglePlayerGame())