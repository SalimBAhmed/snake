from snake.screen import MenuScreen

class SettingsMenu(MenuScreen):
    menu_name: str = "Settings Menu"
    options: list[str] = ["back"]
    selected_option: int = 0

    def _process_menu_selection(self):
        option = self.get_option()
        if option == "back":
            self._context.transition_to_previous_screen()
        else:
            print(f"Selected option: {option}") 