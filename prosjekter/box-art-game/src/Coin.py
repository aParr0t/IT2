import time

import pygame

from .SpriteStack import SpriteStack


class Coin(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
    ):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.move_ip(-width // 2, -height // 2)
        self.speed = pygame.Vector2(0, 0)
        self.collect_time = None  # time when the coin was collected
        self.duration = 0.5  # duration of the collection animation
        self.is_collected = False

    def get_collected(self):
        if not self.is_collected:
            self.collect_time = time.time()
            self.is_collected = True

    def animation_done(self):
        return self.is_collected and time.time() - self.collect_time > self.duration

    def render(self, screen: pygame.Surface, xoff: int, yoff: int):
        # if the coin is collected, play the collection animation
        yfloat = 0
        if self.is_collected:
            yfloat = (
                -self.rect.height * (time.time() - self.collect_time) / self.duration
            )

        pygame.draw.circle(
            screen,
            "yellow",
            (
                self.rect.x - xoff + self.rect.width // 2,
                self.rect.y - yoff + yfloat + self.rect.height // 2,
            ),
            self.rect.width // 2,
        )
