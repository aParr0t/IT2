import pygame

from .SpriteStack import SpriteStack


class Car(pygame.sprite.Sprite):
    def __init__(
        self,
        sprite_sheet: str,
        frame_width: int,
        frame_count: int,
        frame_y_offset: int,
        x: int,
        y: int,
        width: int,
        height: int,
    ):
        super().__init__()
        self.sprite_stack = SpriteStack(sprite_sheet, frame_width, frame_count)
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = pygame.Vector2(0, 0)
        self.speed_multiplier = 20
        self.angular_speed = 0
        self.angle = 0
        self.steer_speed = 10
        self.frame_y_offset = frame_y_offset

    def move(self, dt: float):
        self.angle += self.angular_speed * dt
        self.rect.x += self.speed.x * dt
        self.rect.y += self.speed.y * dt

        self.angular_speed *= 0.95
        self.speed *= 0.95
        if self.speed.length() < 1:
            self.speed = pygame.Vector2(0, 0)

    def accelerate(self):
        speed_vec = pygame.Vector2(1, 0).rotate(-self.angle)
        speed_vec *= self.speed_multiplier
        self.speed += speed_vec

    def decelerate(self):
        self.speed *= 0.90

    def steer(self, direction: int):
        self.angular_speed += direction * self.steer_speed

    def surface(self):
        surface = self.sprite_stack.surface(self.frame_y_offset, self.angle)
        # scale the surface to the size of the car
        surface = pygame.transform.scale(surface, (self.rect.width, self.rect.height))
        return surface

    def get_wheel_positions(self):
        base_vector = pygame.Vector2(self.rect.center)
        angle = self.angle
        half_width = self.rect.width / 2
        half_height = self.rect.height / 2 - self.rect.height / 4
        wheels = [
            base_vector + pygame.Vector2(-half_width, half_height).rotate(-angle),
            base_vector + pygame.Vector2(-half_width, -half_height).rotate(-angle),
        ]
        return wheels
