import random

import pygame


class Sprite:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x, self.y = x, y
        self.w, self.h = w, h

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)


class Player(Sprite):
    def __init__(self, x, y, gravity) -> None:
        super().__init__(x, y, 20, 20)
        self.speed = 0
        self.gravity = gravity

    def update(self, dt):
        self.speed += self.gravity * dt
        self.y += self.speed * dt

    def draw(self, screen):
        pygame.draw.rect(screen, "black", self.rect, 10)

    def jump(self):
        self.speed = -400


class Pipe(Sprite):
    def __init__(self, x, y, w, h, speed):
        super().__init__(x, y, w, h)
        self.speed = speed

    def update(self, dt):
        self.x -= self.speed * dt

    def draw(self, screen):
        pygame.draw.rect(screen, "green", [self.x, self.y, self.w, self.h])


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)
        self.SCREEN_W, self.SCREEN_H = 720, 720
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        self.clock = pygame.time.Clock()

        # init data
        self.reset()

    def reset(self):
        self.running = True
        self.pipes = []
        self.score = 0
        self.pipe_spawn_speed = 1  # seconds
        self.time_since_last_pipe = self.pipe_spawn_speed  # seconds
        self.player = Player(20, 20, 980)
        self.speed = 300

    def spawn_pipe(self):
        gap = 200
        speed = self.speed
        w = 50
        min_h = 50

        h = random.randint(min_h, self.SCREEN_H - gap - min_h)
        x = self.SCREEN_W
        y = 0
        self.pipes.append(Pipe(x, y, w, h, speed))
        y = h + gap
        h = self.SCREEN_H - y
        self.pipes.append(Pipe(x, y, w, h, speed))

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w]:
                        self.player.jump()

            # spawn pipes
            self.time_since_last_pipe += dt
            if self.time_since_last_pipe > self.pipe_spawn_speed:
                self.time_since_last_pipe = 0
                self.spawn_pipe()
                self.speed += 10

            self.screen.fill("white")

            # check collisions
            for pipe in self.pipes:
                if pipe.rect.colliderect(self.player.rect):
                    self.running = False
                if pipe.x < -pipe.w:
                    self.pipes.remove(pipe)
                    self.score += 1
                    print("removed pipe")

            # update player
            self.player.update(dt)

            # draw player
            self.player.draw(self.screen)

            # draw pipes
            for pipe in self.pipes:
                pipe.update(dt)
                pipe.draw(self.screen)

            pygame.display.flip()


if __name__ == "__main__":
    app = App()
    app.run()
