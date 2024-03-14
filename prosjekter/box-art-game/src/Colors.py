import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRASS = pygame.Color("#2bb15d")
ROAD = pygame.Color("#a9a9a9")
ROAD_BORDER = pygame.Color("#808080")


def color_int(color: pygame.Color) -> int:
    # convert a pygame.Color to an integer
    return color.r << 16 | color.g << 8 | color.b
