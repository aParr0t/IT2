import pygame

from .. import Colors
from ..GlobalState import GlobalState
from ..utils.Path import path
from .Screen import Screen
from .Screens import SCREENS


class EditScreen(Screen):
    def __init__(self, state: GlobalState):
        super().__init__(state)
        self.reset()
        self.score_font = pygame.font.Font(None, 36)
        self.tile_width = 64
        font = pygame.font.Font(path.rel_path("assets/pixel-font.ttf"), 72)
        self.arrow_images = {
            k: font.render(k, True, Colors.BLACK) for k in ["v", "^", ">", "<"]
        }
        self.start_edit = None
        self.dir_mapping = {
            (0, 1): "v",
            (0, -1): "^",
            (1, 0): ">",
            (-1, 0): "<",
        }

    def reset(self):
        self.score = 0
        self.state.camera.pos = pygame.Vector2(0, 0)

    def _handle_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.state.change_screen(SCREENS.GAME)

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

                # draw an arrow according to the tile type
                if (
                    0 <= x < self.state.level.get_width()
                    and 0 <= y < self.state.level.get_height()
                ):
                    tile = self.state.level.get_tile(x, y)
                    if tile in self.arrow_images:
                        self.state.screen.blit(
                            self.arrow_images[tile], (x * tw - cx, y * tw - cy)
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
        pygame.draw.rect(
            self.state.screen, "blue", (ox * tw - cx, oy * tw - cy, lw, lh), 3
        )

    def update(self, dt: float):
        keys = pygame.key.get_pressed()
        move_speed = 200
        dx, dy = 0, 0
        if keys[pygame.K_d]:
            dx += move_speed * dt
        if keys[pygame.K_a]:
            dx -= move_speed * dt
        if keys[pygame.K_w]:
            dy -= move_speed * dt
        if keys[pygame.K_s]:
            dy += move_speed * dt
        self.state.camera.pos += pygame.Vector2(dx, dy)

        if keys[pygame.K_s]:
            self.state.level.start = self.get_hovered_tile()
        if keys[pygame.K_x]:
            self.state.level.set_tile(*self.get_hovered_tile(), ".")

        # if mouse is down, place a tile
        if pygame.mouse.get_pressed()[0]:
            x, y = self.get_hovered_tile()
            if not (
                0 <= x < self.state.level.get_width()
                and 0 <= y < self.state.level.get_height()
            ):
                return

            if not self.start_edit:
                self.start_edit = [x, y]
            if self.start_edit != [x, y]:
                end_edit = [x, y]
                delta = [end_edit[i] - self.start_edit[i] for i in range(2)]
                if abs(delta[0]) + abs(delta[1]) > 1:
                    self.start_edit = None
                    return

                self.state.level.set_tile(
                    self.start_edit[0],
                    self.start_edit[1],
                    self.dir_mapping[tuple(delta)],
                )
                self.start_edit = None

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
