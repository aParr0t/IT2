import pygame

from .Monster import Monster


class Fish(Monster):
    def __init__(self, x: int, y: int):
        image = pygame.image.load("assets/fish.png").convert_alpha()
        super().__init__(x, y, 50, image)
        self.speed.x = -200
        self.speed.y = 0
        self.sprite = pygame.transform.flip(self.sprite, True, False)
        self.jump_interval = 1.5  # seconds
        self.time_since_last_jump = 0
        self.jump_speed = 500

    def update(self, dt):
        self.time_since_last_jump += dt
        if self.time_since_last_jump > self.jump_interval:
            self.time_since_last_jump = 0
            self.speed.y = -self.jump_speed
        super().update(dt)

    def draw(self, screen):
        super().draw(screen)
