import random
import time

import pygame

from .. import Colors
from ..Car import Car
from ..GlobalState import GlobalState
from .Screens import SCREENS


class GameScreen:
    def __init__(self, state: GlobalState):
        self.state = state
        self.reset()
        # pipe_image = pygame.image.load("assets/pipe.png").convert_alpha()
        # self.pipe_sprite = scale_to_height(pipe_image, 200)
        self.score_font = pygame.font.Font(None, 36)
        self.player_car = Car(
            "assets/PurpleCar.png",
            frame_width=16,
            frame_count=8,
            frame_y_offset=1,
            x=self.state.level.start[0] * self.state.tile_width,
            y=self.state.level.start[1] * self.state.tile_width,
            width=48,
            height=48,
        )
        self.cars = [self.player_car]
        self.trails = [[], []]
        self.trail_duration = 1

    def reset(self):
        self.score = 0

    def tick(self, dt):
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.state.current_screen = SCREENS.EDITOR

        self.update(dt)
        self.render()

    def render(self):
        keys = pygame.key.get_pressed()

        # background
        self.state.screen.fill(Colors.GRASS)

        cx, cy = self.state.camera.pos
        self.state.screen.blit(
            self.state.level.as_surface(self.state.tile_width), (-cx, -cy)
        )

        # draw the trail
        for trail in self.trails:
            # pygame.draw.circle(self.state.screen, Colors.BLACK, pos[0] - (cx, cy), 2)
            # draw a line between the points
            for i in range(len(trail) - 1):
                distance = trail[i][0] - trail[i + 1][0]
                if distance.length() < 20:
                    pygame.draw.line(
                        self.state.screen,
                        (0, 0, 0),
                        trail[i][0] - (cx, cy),
                        trail[i + 1][0] - (cx, cy),
                        5,
                    )

        # draw cars, scaled up to half the size of the tiles
        for car in self.cars:
            surface = car.surface()
            self.state.screen.blit(surface, (car.rect.x - cx, car.rect.y - cy))

    def update(self, dt: float):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player_car.accelerate()
        if keys[pygame.K_s]:
            self.player_car.decelerate()
        if keys[pygame.K_a]:
            self.player_car.steer(1)
        if keys[pygame.K_d]:
            self.player_car.steer(-1)

        for car in self.cars:
            car.move(dt)

        self.state.camera.follow_center(self.player_car.rect.topleft, dt)

        if not self.is_car_on_road(self.player_car):
            wheels = self.player_car.get_wheel_positions()
            for i, wheel in enumerate(wheels):
                self.trails[i].append((wheel, time.time()))
        for trail in self.trails:
            for i, pos in enumerate(trail):
                if time.time() - pos[1] > 1:
                    trail.pop(i)

    def is_car_on_road(self, car: Car):
        return self.car_on_road_percentage(car) > 0.5

    def car_on_road_percentage(self, car: Car):
        # if the car rect is outside the level, return 0
        if (
            not self.state.level.as_surface(self.state.tile_width)
            .get_rect()
            .contains(car.rect)
        ):
            return 0

        road = self.state.level.collision_surface(self.state.tile_width)
        # make a surface for the car filled with white
        car_surface = pygame.surface.Surface(car.rect.size)
        car_surface.fill("red")
        # get the collision rectangle
        road.blit(car_surface, car.rect.topleft, special_flags=pygame.BLEND_RGBA_MIN)
        area_to_check = road.subsurface(car.rect)
        self.state.screen.blit(road, -self.state.camera.pos)

        # count the percentage of red pixels
        cnt = 0
        red_decimal = Colors.color_int(pygame.Color("red"))
        total_pixels = car.rect.width * car.rect.height
        for row in pygame.PixelArray(area_to_check):
            for px in row:
                if px == red_decimal:
                    cnt += 1
        return cnt / total_pixels
