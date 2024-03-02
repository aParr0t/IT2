import pygame

from .. import Colors
from ..GlobalState import GlobalState
from ..utils.Button import Button
from .Screens import SCREENS


class MenuScreen:
    def __init__(self, state: GlobalState):
        self.state = state
        self.half_screen_w = self.state.SCREEN_W // 2
        self.half_screen_h = self.state.SCREEN_H // 2
        self.button = Button(
            self.state.screen,
            100,
            100,
            "Start",
            "red",
        )
        font = pygame.font.Font("assets/pixel-font.ttf", 72)
        self.title = font.render("Speed Circuit", True, Colors.BLACK)
        self.background = pygame.image.load("assets/background.png")
        self.background = pygame.transform.smoothscale(
            self.background, (self.state.SCREEN_W, self.state.SCREEN_H)
        )

    def tick(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.running = False
        self.update()
        self.render()

    def render(self):
        self.state.screen.fill(Colors.WHITE)
        self.state.screen.blit(
            self.background,
            (
                self.half_screen_w - self.background.get_width() // 2,
                self.half_screen_h - self.background.get_height() // 2,
            ),
        )
        y = self.half_screen_h - 100
        self.state.screen.blit(
            self.title,
            (
                self.half_screen_w - self.title.get_width() // 2,
                y,
            ),
        )
        y += self.title.get_height() + 20
        self.button.draw(
            x=self.half_screen_w - self.button.width // 2,
            y=y,
        )

    def update(self):
        if self.button.isClicked():
            self.state.current_screen = SCREENS.GAME
