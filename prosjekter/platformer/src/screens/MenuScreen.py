import pygame

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
        font = pygame.font.SysFont("Arial", 50)
        self.title = font.render("Platformer", True, (0, 0, 0))

    def tick(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.running = False

        self.state.screen.fill("white")
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
        if self.button.isClicked():
            self.state.current_screen = SCREENS.GAME
