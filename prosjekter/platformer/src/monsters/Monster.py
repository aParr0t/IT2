import pygame

from ..Player import Player
from ..Sprite import Sprite
from ..utils.surface_scaler import scale_to_width


class INTERACT_OUTCOME:
    NOTHING = 0
    PLAYER_DIED = 1
    MONSTER_DIED = 2


class Monster(Sprite):
    INTERACT_OUTCOME = INTERACT_OUTCOME

    def __init__(self, x: int, y: int, width: int, image: pygame.Surface) -> None:
        self.sprite = scale_to_width(image, width)
        super().__init__(x, y, self.sprite.get_width(), self.sprite.get_height())
        self.speed = pygame.math.Vector2(0, 0)
        self.time_to_die = 0
        self.time_since_died = 0
        self.dead = False
        self.gravity = 1000

    def update(self, dt):
        self.x += self.speed.x * dt
        self.speed.y = self.speed.y + self.gravity * dt
        self.y += self.speed.y * dt

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

    def interact(self, player: Player):
        if self.rect.colliderect(player.rect):
            player.die()
            return self.INTERACT_OUTCOME.PLAYER_DIED

    def die(self, dt: float):
        self.time_since_died += dt
        if self.time_since_died > self.time_to_die:
            self.dead = True
