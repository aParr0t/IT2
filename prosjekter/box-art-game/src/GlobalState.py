import json

import pygame
from src.screens.Screens import SCREENS

from . import Camera
from .Level import Level
from .utils.Path import path


class GlobalState:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.SCREEN_W, self.SCREEN_H = 1280, 720
        self.screen = pygame.display.set_mode(
            (self.SCREEN_W, self.SCREEN_H), pygame.RESIZABLE, 32, 0
        )
        self.clock = pygame.time.Clock()
        self.current_screen = SCREENS.MENU
        self.running = True
        self.level: Level = self._load_level()
        self.camera = Camera.Camera(self)

    def init_screens(self, screens):
        self.screens = screens

    def _load_level(self):
        with open(path.rel_path("save/level.json")) as f:
            data = json.load(f)
        return Level(
            level=data["level"],
            origin=data["origin"],
            start=data["start"],
        )

    def save_level(self):
        with open(path.rel_path("save/level.json"), "w") as f:
            json.dump(
                self.level.serialize(),
                f,
            )

    def change_screen(self, screen: SCREENS):
        self.current_screen = screen
