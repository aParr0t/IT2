import pygame

from .Monster import Monster


class Koopa(Monster):
    def __init__(self, x: int, y: int):
        image = pygame.image.load("assets/koopa.png").convert_alpha()
        super().__init__(x, y, 50, image)
        self.speed.x = -200
        self.speed.y = 0
        self.sprite = pygame.transform.flip(self.sprite, True, False)

    def draw(self, screen):
        super().draw(screen)
