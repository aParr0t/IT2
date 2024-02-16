import pygame
from src.GlobalState import GlobalState
from src.screens.GameScreen import GameScreen
from src.screens.MenuScreen import MenuScreen
from src.screens.ScoreScreen import ScoreScreen
from src.screens.Screens import SCREENS


class App:
    def __init__(self) -> None:
        self.global_state = GlobalState()
        self.screens = {
            SCREENS.GAME: GameScreen(self.global_state),
            SCREENS.MENU: MenuScreen(self.global_state),
            SCREENS.SCORE: ScoreScreen(self.global_state),
        }

    def run(self):
        while self.global_state.running:
            dt = self.global_state.clock.tick(60) / 1000
            self.screens[self.global_state.current_screen].tick(dt)
            pygame.display.flip()


if __name__ == "__main__":
    app = App()
    app.run()
