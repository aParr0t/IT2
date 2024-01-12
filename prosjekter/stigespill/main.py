# pygame template taken from: https://www.pygame.org/docs/

import random
import sys

import pygame

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("arial", 30)
SCREEN_W, SCREEN_H = 720, 720
screen = pygame.display.set_mode((SCREEN_H, SCREEN_H))
clock = pygame.time.Clock()
running = True
dt = 0

players = [0, 0]
colors = []
for p in players:
    r = lambda: random.randint(0, 255)
    color = "#%02X%02X%02X" % (r(), r(), r())
    colors.append(color)
player_turn = 0
w, h = 10, 10
tile_count = w * h

tunnels = {
    1: 38,
    4: 14,
    9: 31,
    21: 42,
    28: 84,
    36: 44,
    51: 67,
    71: 91,
    80: 100,
    16: 6,
    48: 26,
    49: 11,
    56: 53,
    62: 19,
    64: 60,
    87: 24,
    93: 73,
    95: 75,
    98: 78,
}

tile_w, tile_h = SCREEN_W / w, SCREEN_H / h
tile_pos = []

# precalculate tile positions
tx, ty = SCREEN_W - tile_w, SCREEN_H - tile_h
x_dir = -1
for i in range(tile_count):
    tile_pos.append((tx, ty))
    if i != 0 and (i + 1) % w == 0:
        x_dir *= -1
        ty -= tile_h
    else:
        tx += tile_w * x_dir

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                dice = random.randint(1, 6)
                players[player_turn] += dice
                p_pos = players[player_turn]
                if p_pos + 1 in tunnels:
                    players[player_turn] = tunnels[p_pos + 1] - 1
                if players[player_turn] >= w * h - 1:
                    print(f"player {player_turn+1} won!")
                    running = False
                    sys.exit()

                player_turn = (player_turn + 1) % len(players)

    # background
    screen.fill("white")

    # tiles
    for i, (tx, ty) in enumerate(tile_pos):
        pygame.draw.rect(screen, "black", (tx, ty, tile_w, tile_h), 1)
        text_surface = font.render(str(i + 1), False, (0, 0, 0))
        screen.blit(text_surface, (tx, ty))

    # snakes and ladders
    for f, t in tunnels.items():
        f -= 1
        t -= 1
        color = "green" if f < t else "red"
        x1, y1 = tile_pos[f]
        x2, y2 = tile_pos[t]
        x1, y1 = x1 + tile_w / 2, y1 + tile_h / 2
        x2, y2 = x2 + tile_w / 2, y2 + tile_h / 2
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), 6)

    # draw player positions
    for i, p in enumerate(players):
        x, y = tile_pos[p]
        x += tile_w / 2
        y += tile_h / 2
        pygame.draw.circle(screen, colors[i], (x, y), tile_w / 2)

    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
