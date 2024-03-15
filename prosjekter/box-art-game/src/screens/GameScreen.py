import time

import pygame

from .. import Colors
from ..Car import Car
from ..Coin import Coin
from ..GlobalState import GlobalState
from ..utils.Path import path
from .Screen import Screen
from .Screens import SCREENS


class GameScreen(Screen):
    def __init__(self, state: GlobalState):
        super().__init__(state)
        self.tile_width = 256
        self.font = pygame.font.Font(path.rel_path("assets/pixel-font.ttf"), 72)
        self.trail_duration = 1
        self.reset()

    def reset(self):
        self.trails = [[], []]
        self.level_surface = self.state.level.as_surface(self.tile_width)
        self.player_car = Car(
            path.rel_path("assets/PurpleCar.png"),
            frame_width=16,
            frame_count=8,
            frame_y_offset=1,
            x=self.state.level.start[0] * self.tile_width + self.tile_width / 2,
            y=self.state.level.start[1] * self.tile_width + self.tile_width / 2,
            width=64,
            height=64,
        )
        self.cars = [self.player_car]
        self._init_coins()

    def _init_coins(self):
        # create the coins on each level tile that is road
        self.coins: list[Coin] = []
        for y, row in enumerate(self.state.level.level):
            for x, tile in enumerate(row):
                if tile != ".":
                    cx = x * self.tile_width + self.tile_width / 2
                    cy = y * self.tile_width + self.tile_width / 2
                    self.coins.append(Coin(cx, cy, 64, 64))

    def _handle_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.state.change_screen(SCREENS.EDITOR)

    def render(self):
        # background
        self.state.screen.fill(Colors.GRASS)

        cx, cy = self.state.camera.pos

        # draw the trail
        for trail in self.trails:
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

        # draw the level
        self.state.screen.blit(self.level_surface, (-cx, -cy))

        # draw coins
        for coin in self.coins:
            coin.render(self.state.screen, cx, cy)
            # draw coin rect
            # pygame.draw.rect(
            #     self.state.screen,
            #     Colors.BLACK,
            #     coin.rect.move(-cx, -cy),
            #     1,
            # )

        # draw cars, scaled up to half the size of the tiles
        for car in self.cars:
            surface = car.surface()
            self.state.screen.blit(surface, (car.rect.x - cx, car.rect.y - cy))
            # draw car outline
            # pygame.draw.rect(
            #     self.state.screen,
            #     Colors.BLACK,
            #     car.rect.move(-cx, -cy),
            #     1,
            # )

        # draw ui and text
        stats = self.font.render(
            f"Fps: {self.state.clock.get_fps():.0f}\ne: edit", True, Colors.BLACK
        )
        self.state.screen.blit(stats, (10, 10))

    def update(self, dt: float):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player_car.accelerate(10)
        elif keys[pygame.K_s]:
            self.player_car.brake(dt)
        else:
            self.player_car.friction_speed(dt)
        if keys[pygame.K_a]:
            self.player_car.steer(600, dt)
        elif keys[pygame.K_d]:
            self.player_car.steer(-600, dt)
        else:
            self.player_car.friction_angular_speed()

        for car in self.cars:
            car.move(dt)

        self.state.camera.follow_center(self.player_car.rect.topleft, dt)

        wheels = self.player_car.get_wheel_positions()
        for i, wheel in enumerate(wheels):
            self.trails[i].append((wheel, time.time()))

        for trail in self.trails:
            if len(trail) > 0:
                if time.time() - trail[0][1] > 1:
                    trail.pop(0)

        # collect coins
        for coin in self.coins:
            if self.player_car.rect.colliderect(coin.rect):
                coin.get_collected()
            if coin.animation_done():
                self.coins.remove(coin)

    def _is_car_on_road(self, car: Car):
        return self._car_on_road_percentage(car) > 0.5

    def _car_on_road_percentage(self, car: Car):
        # if the car rect is outside the level, return 0
        if (
            not self.state.level.as_surface(self.tile_width)
            .get_rect()
            .contains(car.rect)
        ):
            return 0

        road = self.state.level.collision_surface(self.tile_width)
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
