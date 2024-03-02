import json

import pygame

from . import Camera
from .Level import Level
from .screens.Screens import SCREENS


class GlobalState:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.SCREEN_W, self.SCREEN_H = 1280, 720
        self.screen = pygame.display.set_mode(
            (self.SCREEN_W, self.SCREEN_H), pygame.RESIZABLE, 32, 0
        )
        self.screen.convert_alpha()
        self.clock = pygame.time.Clock()
        self.current_screen = SCREENS.MENU
        self.running = True
        self.tile_width = 256
        self.level: Level = self._load_level()
        self.camera = Camera.Camera(self)

    def _load_level(self):
        with open("save/level.json") as f:
            data = json.load(f)
        return Level(
            level=data["level"],
            tile_width=self.tile_width,
            origin=data["origin"],
            start=data["start"],
        )

    def save_level(self):
        with open("save/level.json", "w") as f:
            json.dump(
                self.level.serialize(),
                f,
            )
