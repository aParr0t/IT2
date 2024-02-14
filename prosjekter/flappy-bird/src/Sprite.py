import pygame


class Sprite:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x, self.y = x, y
        self.width, self.height = w, h

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
