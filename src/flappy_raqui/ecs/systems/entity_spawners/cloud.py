import random

import flappy_raqui.ecs.spawners as entity_spawner
from flappy_raqui.ecs.systems.entity_spawners.base import BaseSpawnerProcessor


class CloudSpawnerProcessor(BaseSpawnerProcessor):
    def __init__(
        self, spawn_interval: float, x: int, y: int, dx: tuple[int, int] = (10, 50)
    ):
        super().__init__(spawn_interval)
        self.x = x
        self.y = y
        self._dx = dx

    def spawn_entity_logic(self) -> None:
        _ = entity_spawner.CloudEntitySpawner().spawn_entity(
            x=self.x, y=self.y, dx=-random.randint(*self._dx)
        )
