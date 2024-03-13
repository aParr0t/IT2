import os

import pygame
from src.GlobalState import GlobalState
from src.screens.EditScreen import EditScreen
from src.screens.GameScreen import GameScreen
from src.screens.MenuScreen import MenuScreen
from src.screens.Screens import SCREENS
from src.utils.Path import path


class App:
    def __init__(self) -> None:
        path.set_base_path(os.path.dirname(__file__))
        self.state = GlobalState()
        self.state.set_screens(
            {
                SCREENS.GAME: GameScreen(self.state),
                SCREENS.MENU: MenuScreen(self.state),
                SCREENS.EDITOR: EditScreen(self.state),
            }
        )
        self.prev_screen = self.state.current_screen

    def run(self):
        while self.state.running:
            if self.prev_screen != self.state.current_screen:
                self.state.screens[self.state.current_screen].reset()
                self.prev_screen = self.state.current_screen
            dt = self.state.clock.tick(120) / 1000
            self.state.screens[self.state.current_screen].tick(dt)
            pygame.display.flip()


if __name__ == "__main__":
    app = App()
    app.run()
