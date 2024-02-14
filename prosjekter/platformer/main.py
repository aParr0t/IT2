import pygame
from src.GameScreen import GameScreen
from src.GlobalState import GlobalState
from src.MenuScreen import MenuScreen


class App:
    def __init__(self) -> None:
        self.global_state = GlobalState()
        self.screens = {
            "game": GameScreen(self.global_state),
            "menu": MenuScreen(self.global_state),
        }

    def run(self):
        while self.global_state.running:
            dt = self.global_state.clock.tick(60) / 1000
            self.screens[self.global_state.current_screen].tick(dt)
            pygame.display.flip()


if __name__ == "__main__":
    app = App()
    app.run()
