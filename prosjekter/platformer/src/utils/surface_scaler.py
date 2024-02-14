import pygame


def scale_to_width(image: pygame.Surface, width: int) -> pygame.Surface:
    width1, height1 = image.get_size()
    width2, height2 = width, int(width / width1 * height1)
    return pygame.transform.scale(image, (width2, height2))


def scale_to_height(image: pygame.Surface, height: int) -> pygame.Surface:
    width1, height1 = image.get_size()
    width2, height2 = height, int(height / width1 * height1)
    return pygame.transform.scale(image, (width2, height2))
