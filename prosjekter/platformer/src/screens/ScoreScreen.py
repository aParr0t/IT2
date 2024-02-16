import pygame

from ..GlobalState import GlobalState
from ..utils.Button import Button
from .Screens import SCREENS


class ScoreScreen:
    def __init__(self, state: GlobalState):
        self.state = state
        self.half_screen_w = self.state.SCREEN_W // 2
        self.half_screen_h = self.state.SCREEN_H // 2
        self.button = Button(
            self.state.screen,
            100,
            100,
            "Restart",
            "red",
        )
        self.font = pygame.font.SysFont("Arial", 50)
        self.scores_text = self.font.render("Scores", True, (0, 0, 0))
        self.rerender_scores()

    def rerender_scores(self):
        self.scores = self.state.scores.copy()
        self.scores.sort(reverse=True)
        scores = "\n".join([str(x) for x in self.scores])
        self.scores_surface = self.font.render(scores, True, (0, 0, 0))

    def tick(self, dt):
        if self.scores != self.state.scores:
            self.rerender_scores()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.running = False

        self.state.screen.fill("white")
        # render title
        y = self.half_screen_h - 100
        self.state.screen.blit(
            self.scores_text,
            (
                self.half_screen_w - self.scores_text.get_width() // 2,
                y,
            ),
        )
        y += self.scores_text.get_height() + 20
        # render score list
        self.state.screen.blit(
            self.scores_surface,
            (
                self.half_screen_w - self.scores_surface.get_width() // 2,
                y,
            ),
        )
        y += self.scores_surface.get_height() + 20

        # render button
        self.button.draw(
            x=self.half_screen_w - self.button.width // 2,
            y=y,
        )
        if self.button.isClicked():
            self.state.current_screen = SCREENS.GAME
