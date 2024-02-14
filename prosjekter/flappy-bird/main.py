import math
import random

import pygame
from src.Button import Button
from src.Pipe import Pipe
from src.Player import Player


class GlobalState:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)
        self.SCREEN_W, self.SCREEN_H = 720, 720
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        self.clock = pygame.time.Clock()
        self.current_screen = "menu"
        self.running = True


class GameScreen:
    def __init__(self, state: GlobalState):
        self.state = state
        self.reset()

    def reset(self):
        self.running = True
        self.pipes: list[Pipe] = []
        self.score = 0
        self.pipe_spawn_speed = 1  # seconds
        self.time_since_last_pipe = self.pipe_spawn_speed  # seconds
        self.player = Player(200, self.state.SCREEN_H / 2, 980)
        self.speed = 300
        self.has_started = False
        self.jump_buttons = [pygame.K_SPACE, pygame.K_UP, pygame.K_w]
        self.ground_height = 100

    def spawn_pipe(self):
        gap = 200
        w = 80
        min_h = 50
        x = self.state.SCREEN_W

        # top pipe
        h = random.randint(
            min_h, self.state.SCREEN_H - gap - min_h - self.ground_height
        )
        y = 0
        self.pipes.append(
            Pipe(x, y, width=w, height=h, speed=self.speed, position="top")
        )
        # bottom pipe
        y = h + gap
        h = self.state.SCREEN_H - y
        self.pipes.append(
            Pipe(x, y, width=w, height=h, speed=self.speed, position="bottom")
        )

    def tick(self, dt):
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.running = False
            if event.type == pygame.KEYDOWN:
                if event.key in self.jump_buttons:
                    self.player.jump()
                    if not self.has_started:
                        self.has_started = True

        if self.has_started:
            self.update(dt)
        else:
            self.player.y = (
                math.sin(pygame.time.get_ticks() / 500) * 50 + self.state.SCREEN_H / 2
            )

        self.render()

    def render(self):
        self.state.screen.fill("white")
        # draw ground
        pygame.draw.rect(
            self.state.screen,
            "#774d27",
            [
                0,
                self.state.SCREEN_H - self.ground_height,
                self.state.SCREEN_W,
                self.ground_height,
            ],
        )
        # draw sky
        pygame.draw.rect(
            self.state.screen,
            "#70c5cd",
            [0, 0, self.state.SCREEN_W, self.state.SCREEN_H - self.ground_height],
        )
        self.player.draw(self.state.screen)
        for pipe in self.pipes:
            pipe.draw(self.state.screen)

    def update(self, dt: float):
        # spawn pipes
        self.time_since_last_pipe += dt
        if self.time_since_last_pipe > self.pipe_spawn_speed:
            self.time_since_last_pipe = 0
            self.spawn_pipe()
            self.speed += 10

        # updates and collision checks
        self.player.update(dt)
        # check if player is out of bounds
        if not (
            0
            < self.player.y
            < self.state.SCREEN_H - self.player.height - self.ground_height
        ):
            self.state.running = False
        for pipe in self.pipes:
            if pipe.rect.colliderect(self.player.rect):
                self.state.running = False
            if pipe.x < -pipe.width:
                self.pipes.remove(pipe)
                self.score += 1
            pipe.update(dt)


class MenuScreen:
    def __init__(self, state: GlobalState):
        self.state = state
        self.button = Button(self.state.screen, 100, 100, 100, 100, "Start", "red")

    def tick(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.running = False

        self.state.screen.fill("white")
        self.button.draw()
        if self.button.isClicked():
            self.state.current_screen = "game"


class App:
    def __init__(self) -> None:
        self.global_state = GlobalState()
        self.screens = {
            "game": GameScreen(self.global_state),
            "menu": MenuScreen(self.global_state),
        }

    def run(self):
        while self.global_state.running:
            dt = self.global_state.clock.tick(60) / 1000
            self.screens[self.global_state.current_screen].tick(dt)
            pygame.display.flip()


if __name__ == "__main__":
    app = App()
    app.run()
