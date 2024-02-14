import pygame

from .Sprite import Sprite


class Player(Sprite):
    def __init__(self, x, y) -> None:
        sprite = pygame.image.load("assets/mario.png").convert_alpha()
        width1, height1 = sprite.get_size()
        desired_width = 60
        width2, height2 = desired_width, int(desired_width / width1 * height1)
        super().__init__(x, y, width2, height2)
        self.sprite = pygame.transform.scale(sprite, (self.width, self.height))
        self.speed = pygame.math.Vector2(0, 0)
        self.gravity = 1000
        self.right_buttons = [pygame.K_RIGHT, pygame.K_d]
        self.left_buttons = [pygame.K_LEFT, pygame.K_a]
        self.jump_buttons = [pygame.K_SPACE, pygame.K_UP, pygame.K_w]

    def update(self, dt):
        keys = pygame.key.get_pressed()  # Checking pressed keys
        if any(keys[i] for i in self.right_buttons):
            self.speed.x = 300
        if any(keys[i] for i in self.left_buttons):
            self.speed.x = -300
        if any(keys[i] for i in self.jump_buttons):
            if self.speed.y == 0:
                self.jump()

        self.speed.x = self.speed.x * 0.9
        self.x += self.speed.x * dt

        self.speed.y = self.speed.y + self.gravity * dt
        self.y += self.speed.y * dt

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

    def jump(self):
        self.speed.y = -500

    def die(self):
        pass
