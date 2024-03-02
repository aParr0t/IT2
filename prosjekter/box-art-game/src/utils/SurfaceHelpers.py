import pygame


def scale_to_width(image: pygame.Surface, width: int) -> pygame.Surface:
    width1, height1 = image.get_size()
    width2, height2 = width, int(width / width1 * height1)
    return pygame.transform.scale(image, (width2, height2))


def scale_to_height(image: pygame.Surface, height: int) -> pygame.Surface:
    width1, height1 = image.get_size()
    width2, height2 = height, int(height / width1 * height1)
    return pygame.transform.scale(image, (width2, height2))


def blitRotate(
    surf: pygame.Surface,
    image: pygame.Surface,
    pos: pygame.Vector2,
    originPos: pygame.Vector2,
    angle: float,
):
    """
    Rotate an image and blit it to the target surface.
    :param surf: target surface
    :param image: image to rotate
    :param pos: position of the pivot
    :param originPos: position of the image center
    :param angle: rotation angle
    :return: None
    Taken from: https://stackoverflow.com/a/54714144

    """

    # offset from pivot to center
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)

    # draw rectangle around the image
    # pygame.draw.rect(
    #     surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()), 2
    # )
