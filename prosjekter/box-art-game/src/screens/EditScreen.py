import pygame

from ..GlobalState import GlobalState
from ..utils.SurfaceHelpers import scale_to_height
from .Screens import SCREENS


class EditScreen:
    def __init__(self, state: GlobalState):
        self.state = state
        self.reset()
        # pipe_image = pygame.image.load("assets/pipe.png").convert_alpha()
        # self.pipe_sprite = scale_to_height(pipe_image, 200)
        self.score_font = pygame.font.Font(None, 36)
        self.tile_width = 64

    def reset(self):
        self.score = 0

    def tick(self, dt):
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.running = False
                self.state.save_level()
            # if user pressed e switch to game screen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.state.current_screen = SCREENS.GAME

        self.update(dt)
        self.render()

    def render(self):
        # background
        self.state.screen.fill("white")

        # draw origin
        cx, cy = self.state.camera.pos
        pygame.draw.circle(self.state.screen, "red", (-cx, -cy), 10)

        # draw tiles
        tw = self.tile_width
        tile_region = self.get_visible_tile_region()
        hovered_tile = self.get_hovered_tile()
        ox, oy = self.state.level.origin
        self.state.screen.blit(
            self.state.level.as_surface(self.tile_width), (ox * tw - cx, oy * tw - cy)
        )
        for x in range(tile_region[0], tile_region[2] + 1):
            for y in range(tile_region[1], tile_region[3] + 1):
                # draw tile border
                color = "black"
                thickness = 1
                if x == hovered_tile[0] and y == hovered_tile[1]:
                    color = "red"
                    thickness = 3
                pygame.draw.rect(
                    self.state.screen,
                    color,
                    (x * tw - cx, y * tw - cy, tw, tw),
                    thickness,
                )

                # draw start
                if [x, y] == self.state.level.start:
                    half_tw = tw // 2
                    pygame.draw.circle(
                        self.state.screen,
                        "green",
                        (x * tw - cx + half_tw, y * tw - cy + half_tw),
                        tw // 4,
                    )

        # draw level border
        level = self.state.level
        lw = level.get_width() * tw
        lh = level.get_height() * tw
        ox, oy = level.origin
        pygame.draw.rect(
            self.state.screen, "blue", (ox * tw - cx, oy * tw - cy, lw, lh), 3
        )

    def update(self, dt: float):
        keys = pygame.key.get_pressed()
        move_speed = 200
        dx, dy = 0, 0
        if keys[pygame.K_RIGHT]:
            dx += move_speed * dt
        if keys[pygame.K_LEFT]:
            dx -= move_speed * dt
        if keys[pygame.K_UP]:
            dy -= move_speed * dt
        if keys[pygame.K_DOWN]:
            dy += move_speed * dt
        self.state.camera.pos += pygame.Vector2(dx, dy)

        if keys[pygame.K_s]:
            self.state.level.start = self.get_hovered_tile()

        # if mouse is down, place a tile
        if pygame.mouse.get_pressed()[0]:
            x, y = self.get_hovered_tile()
            self.state.level.set_tile(x, y, "x")

    def get_hovered_tile(self):
        mx, my = pygame.mouse.get_pos()
        cx, cy = self.state.camera.pos
        tw = self.tile_width
        return [int(x) for x in [(mx + cx) // tw, (my + cy) // tw]]

    def get_visible_tile_region(self):
        cx, cy = self.state.camera.pos
        tw = self.tile_width
        return [
            int(x)
            for x in [
                cx // tw,
                cy // tw,
                (cx + self.state.SCREEN_W) // tw,
                (cy + self.state.SCREEN_H) // tw,
            ]
        ]
