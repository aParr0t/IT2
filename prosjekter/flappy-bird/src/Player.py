import pygame

from .Sprite import Sprite


class Player(Sprite):
    def __init__(self, x, y, gravity) -> None:
        sprite = pygame.image.load("assets/bird.png").convert_alpha()
        width1, height1 = sprite.get_size()
        desired_width = 60
        width2, height2 = desired_width, int(desired_width / width1 * height1)
        super().__init__(x, y, width2, height2)
        self.sprite = pygame.transform.scale(sprite, (self.width, self.height))
        self.speed = 0
        self.gravity = gravity

    def update(self, dt):
        self.speed += self.gravity * dt
        self.y += self.speed * dt

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

    def jump(self):
        self.speed.y = -400
