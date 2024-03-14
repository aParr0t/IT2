import pygame

from .. import Colors
from ..GlobalState import GlobalState
from ..utils.Button import Button
from ..utils.Path import path
from .Screen import Screen
from .Screens import SCREENS


class MenuScreen(Screen):
    def __init__(self, state: GlobalState):
        super().__init__(state)
        self.button = Button(
            self.state.screen,
            100,
            100,
            "Start",
            "red",
        )
        font = pygame.font.Font(path.rel_path("assets/pixel-font.ttf"), 72)
        self.title = font.render("Speed Circuit", True, Colors.BLACK)
        self.background = pygame.image.load(path.rel_path("assets/background.png"))
        self.background = pygame.transform.smoothscale(
            self.background, (self.state.SCREEN_W, self.state.SCREEN_H)
        )

    def render(self):
        half_screen_w = self.state.SCREEN_W // 2
        half_screen_h = self.state.SCREEN_H // 2
        self.state.screen.fill(Colors.WHITE)
        self.state.screen.blit(
            self.background,
            (
                half_screen_w - self.background.get_width() // 2,
                half_screen_h - self.background.get_height() // 2,
            ),
        )
        y = half_screen_h - 100
        self.state.screen.blit(
            self.title,
            (
                half_screen_w - self.title.get_width() // 2,
                y,
            ),
        )
        y += self.title.get_height() + 20
        self.button.draw(
            x=half_screen_w - self.button.width // 2,
            y=y,
        )

    def update(self, dt: float = 0.0):
        if self.button.is_clicked():
            self.state.change_screen(SCREENS.GAME)
