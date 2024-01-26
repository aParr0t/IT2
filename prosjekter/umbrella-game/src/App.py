import pygame
import pygame_gui

from .DebugWindow import DebugUIWindow
from .State import State


class Player:
    def __init__(self) -> None:
        self.pos = (0, 0)
        self.width = 20
        self.height = 50


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)
        SCREEN_W, SCREEN_H = 720, 720
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.ui_manager = pygame_gui.UIManager((800, 600))

        # init data
        self.reset()

        # data is now initialized
        self.state_window = DebugUIWindow((0, 0), self.ui_manager, state=self.state)

    def reset(self):
        self.state = State()
        self.running = True
        self.player = Player()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    key = event.unicode
                    if key == "a":
                        print("a")

                self.ui_manager.process_events(event)

            self.screen.fill("white")

            # draw player
            pygame.draw.rect(
                self.screen,
                "red",
                (*self.player.pos, self.player.width, self.player.height),
            )

            self.ui_manager.update(dt)

            self.ui_manager.draw_ui(self.screen)
            pygame.display.flip()
