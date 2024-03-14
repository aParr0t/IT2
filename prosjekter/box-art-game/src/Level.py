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


class Level:
    # i think the order of the tiles matters
    # because the more complicated tiles would not get considered if the simpler
    # tiles were considered before the more complicated ones
    PATTERNS = {
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

    def __init__(
        self,
        level: list[str],
        origin: tuple[int, int] = (0, 0),
        start: tuple[int, int] = (0, 0),
    ):
        # add padding to the level so that the level is surrounded by "."
        # this is to prevent index out of bounds errors
        level = self._add_padding(level)
        self.level = [list(row) for row in level]
        self.origin = origin
        self.start = start

        self.tile_mapping: dict[int, dict[TileCategory, pygame.Surface]] = {}
        self._calculate_grid()

    def _add_tileset(self, tile_width: int):
        # check if the tileset already exists
        if tile_width in self.tile_mapping:
            return

        # create a new tileset
        self.tile_mapping[tile_width] = {}
        tiles = self.tile_mapping[tile_width]

        # create a surface for each tile category
        for category in TileCategory:
            surface = pygame.surface.Surface((tile_width, tile_width), pygame.SRCALPHA)
            tiles[category] = surface

        # create corner tiles
        road_padding = tile_width // 6
        road_border = road_padding // 2
        circle_radius = tile_width - road_padding
        ## draw outer border
        pygame.draw.circle(
            tiles[TileCategory.Q1],
            Colors.ROAD_BORDER,
            (tile_width, 0),
            circle_radius + road_border,
        )
        ## draw road
        pygame.draw.circle(
            tiles[TileCategory.Q1],
            Colors.ROAD,
            (tile_width, 0),
            circle_radius,
        )
        ## draw inner border
        pygame.draw.circle(
            tiles[TileCategory.Q1],
            Colors.ROAD_BORDER,
            (tile_width, 0),
            road_padding,
        )
        ## draw inner grass
        pygame.draw.circle(
            tiles[TileCategory.Q1],
            Colors.GRASS,
            (tile_width, 0),
            road_border,
        )
        # copy the first corner quarter to the other quarters
        tiles[TileCategory.Q2] = pygame.transform.rotate(tiles[TileCategory.Q1], 90)
        tiles[TileCategory.Q3] = pygame.transform.rotate(tiles[TileCategory.Q1], 180)
        tiles[TileCategory.Q4] = pygame.transform.rotate(tiles[TileCategory.Q1], 270)

        # create horizontal and vertical roads
        pygame.draw.rect(
            tiles[TileCategory.VERTICAL],
            Colors.ROAD_BORDER,
            (road_border, 0, tile_width - road_border * 2, tile_width),
        )
        pygame.draw.rect(
            tiles[TileCategory.VERTICAL],
            Colors.ROAD,
            (road_padding, 0, tile_width - road_padding * 2, tile_width),
        )
        # copy the vertical road to the horizontal road
        tiles[TileCategory.HORIZONTAL] = pygame.transform.rotate(
            tiles[TileCategory.VERTICAL], 90
        )

    def _add_padding(self, level: list[str]):
        # add padding to the level so that the level is surrounded by "."
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
            self._calculate_grid()
        else:
            print(f"Tile ({x}, {y}) out of bounds")

    def _do_patterns_match(self, p1: list[str], p2: list[str]):
        # order of p1 and p2 is important! p1 is the pattern and p2 is the tile
        # p1 as precedence over p2
        for i in range(3):
            for j in range(3):
                if p1[i][j] == p2[i][j]:
                    continue
                if p1[i][j] == ".":
                    continue
                if p1[i][j] != p2[i][j]:
                    return False
        return True

    def _get_fitting_tile_category(self, x: int, y: int):
        # get the 3x3 pattern around the tile
        # add 1 to x and y because of the level border
        x += 1
        y += 1
        p = [self.bordered[yy][x - 1 : x + 2] for yy in range(y - 1, y + 2)]

        # return the pattern that matches any of the patterns, if not return empty
        for pattern, category in self.PATTERNS.items():
            # order is important!
            if self._do_patterns_match(pattern, p):
                return category
        return TileCategory.EMPTY

    def _calculate_grid(self):
        # create a grid of tile categories, this is used to draw the level
        # the grid is based on the level, and uses the PATTERNS to determine
        # the categories for each tile

        # initialize the grid
        gw, gh = self.get_width(), self.get_height()
        self.tile_grid = [[None for _ in range(gw)] for _ in range(gh)]

        # add a border around the level with "." tiles
        self.bordered = [["." for _ in range(gw + 2)] for _ in range(gh + 2)]
        for y in range(gh):
            for x in range(gw):
                self.bordered[y + 1][x + 1] = self.get_tile(x, y)

        # calculate the grid
        for y in range(gh):
            for x in range(gw):
                tile = self.get_tile(x, y)
                if tile is None:
                    continue
                self.tile_grid[y][x] = self._get_fitting_tile_category(x, y)

    def as_surface(self, tile_width: int):
        # create a surface of the level
        self._add_tileset(tile_width)
        tw = tile_width
        surface = pygame.surface.Surface(
            (tw * self.get_width(), tw * self.get_height()), pygame.SRCALPHA
        )

        # draw the level
        for x in range(self.get_width()):
            for y in range(self.get_height()):
                surface.blit(
                    self.tile_mapping[tile_width][self.tile_grid[y][x]],
                    (x * tw, y * tw),
                )
        return surface

    def serialize(self):
        # serialize the level for saving
        return {
            "level": ["".join(row) for row in self.level],
            "origin": self.origin,
            "start": self.start,
        }

    def collision_surface(self, tile_width: int):
        # create a surface for collision detection

        # the road is white and the grass is black
        px_array = pygame.PixelArray(self.as_surface(tile_width))
        px_array.replace(Colors.ROAD, Colors.WHITE)
        px_array.replace(Colors.GRASS, Colors.BLACK)
        return px_array.surface
