import pygame

from .utils.SurfaceHelpers import blitRotate


class SpriteStack:
    def __init__(
        self, sprite_sheet: str, frame_size: tuple[int, int], frame_count: int
    ) -> None:
        self.sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()
        self.sprites = []
        self.frame_size: pygame.Vector2 = pygame.Vector2(frame_size)
        for i in range(frame_count):
            self.sprites.append(
                self.sprite_sheet.subsurface(
                    (i * self.frame_size.x, 0, self.frame_size.x, self.frame_size.y)
                ).convert_alpha()
            )
        self.frame_count = frame_count

    def surface(self, y_offset: int, angle: float = 0):
        # render the stack of sprites as a single surface,
        # with the sprites stacked on top of each other
        surface = pygame.surface.Surface(
            (
                self.frame_size.x,
                self.frame_size.y + (y_offset * (self.frame_count - 1)),
            ),
            pygame.SRCALPHA,
        ).convert_alpha()
        surface.fill((255, 0, 0, 0))
        # start by drawing the bottom sprite first, then increase the position
        # at which the next sprite is drawn by x_offset and y_offset
        half_w = self.frame_size.x // 2
        half_h = self.frame_size.y // 2
        x, y = half_w, surface.get_height() - half_w
        for sprite in self.sprites:
            blitRotate(surface, sprite, (x, y), (half_w, half_h), angle)
            y -= y_offset

        return surface
