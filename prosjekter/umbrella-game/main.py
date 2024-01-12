import pygame


def main():
    pygame.init()
    pygame.font.init()
    SCREEN_W, SCREEN_H = 720, 720
    screen = pygame.display.set_mode((SCREEN_H, SCREEN_H))
    clock = pygame.time.Clock()
    dt = 0

    px, py = 0, 0
    pwidth, pheight = 50, 50

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")

        # draw player
        pygame.draw.rect(screen, "red", (px, py, pwidth, pheight))

        pygame.display.flip()
        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
