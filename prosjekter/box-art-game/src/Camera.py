import pygame


class Camera:
    def __init__(self, state):
        self._pos = pygame.Vector2(0, 0)
        self.state = state

    def follow_center(self, target: tuple, dt: float):
        half_width = self.state.SCREEN_W / 2
        half_height = self.state.SCREEN_H / 2
        follow_x = target[0] - half_width
        follow_y = target[1] - half_height
        delta = pygame.Vector2(follow_x, follow_y) - self.pos
        self.pos += pygame.math.lerp(0, delta.x, 0.1), pygame.math.lerp(0, delta.y, 0.1)
        self.pos.x = int(self._pos.x)
        self.pos.y = int(self._pos.y)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
