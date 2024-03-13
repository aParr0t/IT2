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
        self.angular_speed = 0
        self.angle = 0
        self.frame_y_offset = frame_y_offset
        self.max_speed = 600
        self.max_angular_speed = 400

    def move(self, dt: float):
        self.angle += self.angular_speed * dt
        self.rect.x += self.speed.x * dt
        self.rect.y += self.speed.y * dt

        if self.speed.length() < 10:
            self.speed = pygame.Vector2(0, 0)

    def friction_speed(self, dt: float):
        # incorporate dt into the friction force
        friction_force = 2 * dt
        self.speed *= 1 - friction_force

    def friction_angular_speed(self):
        self.angular_speed *= 0.95

    def accelerate(self, speed: float):
        speed_vec = pygame.Vector2(speed, 0).rotate(-self.angle)
        self.speed += speed_vec
        self.speed.scale_to_length(min(self.max_speed, self.speed.length()))

    def brake(self, dt: float):
        # incorporate dt into the brake force
        brake_force = 0.2 * dt
        self.speed *= 1 - brake_force

    def steer(self, direction: int, dt: float):
        self.angular_speed += direction * dt
        self.angular_speed = max(
            -self.max_angular_speed, min(self.max_angular_speed, self.angular_speed)
        )

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
