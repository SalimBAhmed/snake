from snake.screen import MenuScreen

class PauseMenu(MenuScreen):
    menu_name: str = "Pause Menu"
    options: list[str] = ["Resume", "Main Menu", "Exit"]
    selected_option: int = 0

    def _process_menu_selection(self):
        option = self.get_option()
        if option == "Resume":
            self._context.transition_to_previous_screen()
        if option == "Main Menu":
            self._context.transition_to(self.context._previous_screen[0])
            self._context._previous_screen.clear()
        elif option == "Exit":
            exit(0)