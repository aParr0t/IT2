import pygame

from .screens.Screens import SCREENS


class GlobalState:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.SCREEN_W, self.SCREEN_H = 720, 720
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        self.clock = pygame.time.Clock()
        self.current_screen = SCREENS.MENU
        self.running = True
        self.scores = []
