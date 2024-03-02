from enum import Enum

import pygame

from . import Colors


# make an enum class for tile categories
class TileCategory(Enum):
    EMPTY = "empty"
    Q1 = "q1"
    Q2 = "q2"
    Q3 = "q3"
    Q4 = "q4"
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


# i think the order of the tiles matters
# because the more complicated tiles would not get considered if the simpler
# tiles were considered before the more complicated ones
patterns = {
    ("...", ".^<", "..."): TileCategory.Q1,
    (".v.", ".>.", "..."): TileCategory.Q1,
    ("...", ">^.", "..."): TileCategory.Q2,
    (".v.", ".<.", "..."): TileCategory.Q2,
    ("...", ">v.", "..."): TileCategory.Q3,
    ("...", ".<.", ".^."): TileCategory.Q3,
    ("...", ".v<", "..."): TileCategory.Q4,
    ("...", ".>.", ".^."): TileCategory.Q4,
    ("...", ".^.", "..."): TileCategory.VERTICAL,
    ("...", ".v.", "..."): TileCategory.VERTICAL,
    ("...", ".<.", "..."): TileCategory.HORIZONTAL,
    ("...", ".>.", "..."): TileCategory.HORIZONTAL,
    ("...", "...", "..."): TileCategory.EMPTY,
}


class Level:
    def __init__(
        self,
        level: list[str],
        tile_width: int,
        origin: tuple[int, int] = (0, 0),
        start: tuple[int, int] = (0, 0),
    ):
        level = self._add_padding(level)
        self.level = [list(row) for row in level]
        self.origin = origin
        self.start = start

        # init tiles
        self.tile_mapping: dict[TileCategory, pygame.Surface] = {}
        for category in TileCategory:
            surface = pygame.surface.Surface((tile_width, tile_width))
            surface.fill(Colors.GRASS)
            # add the surface to the dict
            self.tile_mapping[category] = surface
        ## corner tiles
        road_padding = tile_width // 6
        road_border = road_padding // 2
        circle_radius = tile_width - road_padding
        # draw outer border
        pygame.draw.circle(
            self.tile_mapping[TileCategory.Q1],
            Colors.ROAD_BORDER,
            (tile_width, 0),
            circle_radius + road_border,
        )
        # draw road
        pygame.draw.circle(
            self.tile_mapping[TileCategory.Q1],
            Colors.ROAD,
            (tile_width, 0),
            circle_radius,
        )
        # draw inner border
        pygame.draw.circle(
            self.tile_mapping[TileCategory.Q1],
            Colors.ROAD_BORDER,
            (tile_width, 0),
            road_padding,
        )
        # draw inner grass
        pygame.draw.circle(
            self.tile_mapping[TileCategory.Q1],
            Colors.GRASS,
            (tile_width, 0),
            road_border,
        )
        # copy the first quarter to the other quarters
        self.tile_mapping[TileCategory.Q2] = pygame.transform.rotate(
            self.tile_mapping[TileCategory.Q1], 90
        )
        self.tile_mapping[TileCategory.Q3] = pygame.transform.rotate(
            self.tile_mapping[TileCategory.Q1], 180
        )
        self.tile_mapping[TileCategory.Q4] = pygame.transform.rotate(
            self.tile_mapping[TileCategory.Q1], 270
        )
        # horizontal and vertical roads
        pygame.draw.rect(
            self.tile_mapping[TileCategory.VERTICAL],
            Colors.ROAD_BORDER,
            (road_border, 0, tile_width - road_border * 2, tile_width),
        )
        pygame.draw.rect(
            self.tile_mapping[TileCategory.VERTICAL],
            Colors.ROAD,
            (road_padding, 0, tile_width - road_padding * 2, tile_width),
        )
        self.tile_mapping[TileCategory.HORIZONTAL] = pygame.transform.rotate(
            self.tile_mapping[TileCategory.VERTICAL], 90
        )

        self.calculate_grid()

    def _add_padding(self, level: list[str]):
        level = level.copy()
        if level[0].count(".") != len(level[0]):
            level = ["." * len(level[0])] + level
        if level[-1].count(".") != len(level[-1]):
            level = level + ["." * len(level[0])]
        if not all(row[0] == "." for row in level):
            level = [f".{row}" for row in level]
        if not all(row[-1] == "." for row in level):
            level = [f"{row}." for row in level]
        return level

    def get_width(self):
        return len(self.level[0])

    def get_height(self):
        return len(self.level)

    def get_tile(self, x: int, y: int):
        return self.level[y][x]

    def set_tile(self, x: int, y: int, tile: str):
        if 0 <= x < self.get_width() and 0 <= y < self.get_height():
            self.level[y][x] = tile
        else:
            print(f"Tile ({x}, {y}) out of bounds")

    def do_patterns_match(self, p1: list[str], p2: list[str]):
        # order of p1 and p2 is important!
        for i in range(3):
            for j in range(3):
                if p1[i][j] == p2[i][j]:
                    continue
                if p1[i][j] == ".":
                    continue
                if p1[i][j] != p2[i][j]:
                    return False
        return True

    def get_fitting_tile_category(self, x: int, y: int):
        x += 1
        y += 1
        p = [self.bordered[yy][x - 1 : x + 2] for yy in range(y - 1, y + 2)]
        for pattern, category in patterns.items():
            # order is important!
            if self.do_patterns_match(pattern, p):
                return category
        return TileCategory.EMPTY

    def get_fitting_tile(self, x: int, y: int):
        return self.tile_grid[y][x]

    def calculate_grid(self):
        gw, gh = self.get_width(), self.get_height()
        self.tile_grid = [[None for _ in range(gw)] for _ in range(gh)]

        # add a border around the level with "." tiles
        self.bordered = [["." for _ in range(gw + 2)] for _ in range(gh + 2)]
        for y in range(gh):
            for x in range(gw):
                self.bordered[y + 1][x + 1] = self.get_tile(x, y)

        for y in range(gh):
            for x in range(gw):
                tile = self.get_tile(x, y)
                if tile is None:
                    continue
                self.tile_grid[y][x] = self.get_fitting_tile_category(x, y)

    def as_surface(self, tile_width: int):
        tw = tile_width
        surface = pygame.surface.Surface(
            (tw * self.get_width(), tw * self.get_height())
        )
        for x in range(self.get_width()):
            for y in range(self.get_height()):
                surface.blit(
                    self.tile_mapping[self.get_fitting_tile(x, y)], (x * tw, y * tw)
                )
        return surface

    def serialize(self):
        return {
            "level": ["".join(row) for row in self.level],
            "origin": self.origin,
            "start": self.start,
        }

    def collision_surface(self, tile_width: int):
        # the road is white and the grass is black
        px_array = pygame.PixelArray(self.as_surface(tile_width))
        px_array.replace(Colors.ROAD, Colors.WHITE)
        px_array.replace(Colors.GRASS, Colors.BLACK)
        return px_array.surface
