from snake.game_state import GameState


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.renderer = {"menu": MenuRenderer(), "game": GameRenderer()}

    def draw(self, game_state: GameState):
        self.renderer[self.game_state.state].draw(self.screen, game_state)


class GameRenderer:
    def draw(self, screen, game_state):
        pass


class MenuRenderer:
    def draw(self, screen, game_state):
        pass
