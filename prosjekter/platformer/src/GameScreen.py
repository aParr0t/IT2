import pygame

from .GlobalState import GlobalState
from .monsters.Monster import Monster
from .monsters.MonsterSpawner import MonsterSpawner
from .Player import Player
from .utils.surface_scaler import scale_to_height


class GameScreen:
    def __init__(self, state: GlobalState):
        self.state = state
        self.reset()
        pipe_image = pygame.image.load("assets/pipe.png").convert_alpha()
        self.pipe_sprite = scale_to_height(pipe_image, 200)

    def reset(self):
        self.running = True
        self.score = 0
        self.player = Player(200, self.state.SCREEN_H / 2)
        self.jump_buttons = [pygame.K_SPACE, pygame.K_UP, pygame.K_w]
        self.ground_y = self.state.SCREEN_H - 100
        self.monster_spawn_speed = 1  # seconds
        self.time_since_last_monster = self.monster_spawn_speed
        self.monsters: list[Monster] = []
        self.monster_spawner = MonsterSpawner()
        self.score = 0
        self.score_font = pygame.font.Font(None, 36)
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

        if self.time_since_last_monster > self.monster_spawn_speed:
            self.time_since_last_monster = 0
            self.spawn_monster()

        self.update(dt)
        self.render()
        self.time_since_last_monster += dt

    def render(self):
        self.state.screen.fill("#9494ff")
        self.player.draw(self.state.screen)
        self.state.screen.fill("green", (0, self.ground_y, self.state.SCREEN_W, 100))
        for monster in self.monsters:
            monster.draw(self.state.screen)

        score_text = self.score_font.render(f"Score: {self.score}", True, "black")
        self.state.screen.blit(score_text, (10, 10))
        for monster in self.dead_monsters:
            monster.draw(self.state.screen)

        # draw pipe
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

        for monster in self.dead_monsters:
            monster.die(dt)
            if monster.dead:
                self.dead_monsters.remove(monster)

        for monster in self.monsters:
            monster.update(dt)
            interaction_outcome = monster.interact(self.player)
            if interaction_outcome == Monster.INTERACT_OUTCOME.PLAYER_DIED:
                self.reset()
                return
            elif interaction_outcome == Monster.INTERACT_OUTCOME.MONSTER_DIED:
                self.score += 3
                self.dead_monsters.append(monster)
                self.monsters.remove(monster)
            # collide monster with ground
            if monster.y + monster.height > self.ground_y:
                monster.y = self.ground_y - monster.height
                monster.speed.y = 0
            if monster.x < -monster.width:
                self.monsters.remove(monster)
                self.score += 1
