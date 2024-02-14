import pygame

from .Sprite import Sprite


class Pipe(Sprite):
    def __init__(self, x, y, height, width=80, speed=100, position: str = ""):
        super().__init__(x, y, width, height)
        self.speed = speed
        self.position = position

    def update(self, dt):
        self.x -= self.speed * dt

    def draw(self, screen):
        color = "#73bf2e"
        outline_color = "#543847"
        bar_overhang = 10
        outline_width = 2
        pygame.draw.rect(
            screen,
            color,
            [self.x + bar_overhang, self.y, self.width - bar_overhang * 2, self.height],
        )
        pygame.draw.rect(
            screen,
            outline_color,
            [self.x + bar_overhang, self.y, self.width - bar_overhang * 2, self.height],
            outline_width,
        )
        if self.position == "bottom":
            # draw top bar
            pygame.draw.rect(
                screen,
                color,
                [self.x, self.y, self.width, 30],
            )
            pygame.draw.rect(
                screen, outline_color, [self.x, self.y, self.width, 30], outline_width
            )
        elif self.position == "top":
            # draw bottom bar
            pygame.draw.rect(
                screen,
                color,
                [
                    self.x,
                    self.y + self.height - 30,
                    self.width,
                    30,
                ],
            )
            pygame.draw.rect(
                screen,
                outline_color,
                [
                    self.x,
                    self.y + self.height - 30,
                    self.width,
                    30,
                ],
                outline_width,
            )
