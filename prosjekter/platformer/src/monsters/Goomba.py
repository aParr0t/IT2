import pygame

from ..utils.surface_scaler import scale_to_width
from .Monster import Monster


class Goomba(Monster):
    def __init__(self, x: int, y: int):
        image = pygame.image.load("assets/goomba.png").convert_alpha()
        super().__init__(x, y, 50, image)
        self.speed.x = -200
        self.speed.y = 0
        self.sprite = pygame.transform.flip(self.sprite, True, False)
        squashed_image = pygame.image.load("assets/goomba_squashed.png").convert_alpha()
        self.squashed_sprite = scale_to_width(squashed_image, self.width)
        self.time_to_die = 1  # seconds

    def draw(self, screen):
        super().draw(screen)

    def interact(self, player):
        margin = self.height / 2
        player_is_above = self.y - margin < player.y + player.height < self.y + margin
        player_is_within_x = (
            player.x + player.width > self.x and player.x < self.x + self.width
        )

        if player_is_above and player_is_within_x and player.speed.y > 0:
            return self.INTERACT_OUTCOME.MONSTER_DIED
        if self.rect.colliderect(player.rect):
            player.die()
            return self.INTERACT_OUTCOME.PLAYER_DIED
        return self.INTERACT_OUTCOME.NOTHING

    def die(self, dt):
        if self.time_since_died == 0:
            self.sprite = self.squashed_sprite
            self.y = self.y + self.height - self.squashed_sprite.get_height()
        super().die(dt)
        self.speed.x = 0
        self.speed.y = 0
