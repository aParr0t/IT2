import random
from enum import Enum

from .Fish import Fish
from .Goomba import Goomba
from .Koopa import Koopa
from .Monster import Monster


class MonsterType(Enum):
    FISH = 0
    GOOMBA = 1
    KOOPA = 2


class MonsterSpawnDescription:
    def __init__(
        self, monster_type: MonsterType, probability: float, class_type: Monster
    ):
        self.monster_type = monster_type
        self.probability = probability
        self.class_type = class_type


class MonsterSpawner:
    def __init__(self) -> None:
        self.monsters = {
            MonsterType.FISH: MonsterSpawnDescription(MonsterType.FISH, 0.2, Fish),
            MonsterType.GOOMBA: MonsterSpawnDescription(
                MonsterType.GOOMBA, 0.5, Goomba
            ),
            MonsterType.KOOPA: MonsterSpawnDescription(MonsterType.KOOPA, 0.3, Koopa),
        }

    def spawn(self):
        monster_type = self.choose_monster()
        return self.monsters[monster_type].class_type

    def choose_monster(self):
        monster = random.choices(
            [monster_type for monster_type in self.monsters],
            [monster.probability for monster in self.monsters.values()],
            k=1,
        )[0]
        return monster
