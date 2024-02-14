import pygame


class GlobalState:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)
        self.SCREEN_W, self.SCREEN_H = 720, 720
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        self.clock = pygame.time.Clock()
        self.current_screen = "menu"
        self.running = True
