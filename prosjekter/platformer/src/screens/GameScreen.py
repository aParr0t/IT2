import pygame

from ..GlobalState import GlobalState
from ..monsters.Monster import Monster
from ..monsters.MonsterSpawner import MonsterSpawner
from ..Player import Player
from ..utils.surface_scaler import scale_to_height
from .Screens import SCREENS


class GameScreen:
    def __init__(self, state: GlobalState):
        self.state = state
        self.reset()
        pipe_image = pygame.image.load("assets/pipe.png").convert_alpha()
        self.pipe_sprite = scale_to_height(pipe_image, 200)
        self.score_font = pygame.font.Font(None, 36)
        self.jump_buttons = [pygame.K_SPACE, pygame.K_UP, pygame.K_w]

    def reset(self):
        self.score = 0
        self.player = Player(200, self.state.SCREEN_H / 2)
        self.ground_y = self.state.SCREEN_H - 100
        self.monster_spawn_speed = 1  # seconds
        self.time_since_last_monster = 0
        self.monsters: list[Monster] = []
        self.monster_spawner = MonsterSpawner()
        self.dead_monsters: list[Monster] = []

    def spawn_monster(self):
        monster = self.monster_spawner.spawn()
        monster: Monster = monster(self.state.SCREEN_W, 0)
        monster.y = self.ground_y - monster.height
        self.monsters.append(monster)

    def tick(self, dt):
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.running = False

        # spawn monsters
        if self.time_since_last_monster > self.monster_spawn_speed:
            self.time_since_last_monster = 0
            self.spawn_monster()

        self.update(dt)
        self.render()
        self.time_since_last_monster += dt

    def render(self):
        # background
        self.state.screen.fill("#9494ff")
        # ground
        self.state.screen.fill("green", (0, self.ground_y, self.state.SCREEN_W, 100))
        # render entities
        self.player.draw(self.state.screen)
        for monster in self.monsters:
            monster.draw(self.state.screen)
        # render score
        score_text = self.score_font.render(f"Score: {self.score}", True, "black")
        self.state.screen.blit(score_text, (10, 10))
        for monster in self.dead_monsters:
            monster.draw(self.state.screen)
        # render pipe
        self.state.screen.blit(
            self.pipe_sprite,
            (self.state.SCREEN_W - 50, self.ground_y - self.pipe_sprite.get_height()),
        )

    def update(self, dt: float):
        # updates and collision checks
        self.player.update(dt)
        if self.player.y + self.player.height > self.ground_y:
            self.player.y = self.ground_y - self.player.height
            self.player.speed.y = 0

        # draw (and animate) dead monsters (for a short time after they die)
        for monster in self.dead_monsters:
            monster.die(dt)
            if monster.dead:
                self.dead_monsters.remove(monster)

        # update monsters
        for monster in self.monsters:
            monster.update(dt)
            interaction_outcome = monster.interact(self.player)
            if interaction_outcome == Monster.INTERACT_OUTCOME.PLAYER_DIED:
                self.game_end()
                return
            elif interaction_outcome == Monster.INTERACT_OUTCOME.MONSTER_DIED:
                self.score += 3
                self.dead_monsters.append(monster)
                self.monsters.remove(monster)
            if monster.y + monster.height > self.ground_y:
                # collide monster with ground
                monster.y = self.ground_y - monster.height
                monster.speed.y = 0
            if monster.x < -monster.width:
                # delete monster if it goes off screen
                self.monsters.remove(monster)
                self.score += 1

    def game_end(self):
        self.state.current_screen = SCREENS.SCORE
        self.state.scores.append(self.score)
        self.reset()
        if len(self.state.scores) > 3:
            self.state.scores.sort()
            self.state.scores = self.state.scores[:3]
