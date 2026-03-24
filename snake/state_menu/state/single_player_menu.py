from snake.state_menu import Menu

class SinglePlayerMenu(Menu):
    menu_name: str = "Single Player"
    options: list[str] = ["classic", "infinite", "back"]
    selected_option: int = 0

    def _process_menu_selection(self):
        option = self.get_option()
        if option == "back":
            self._context.transition_to_previous_menu()
        else:
            print(f"Selected option: {option}")