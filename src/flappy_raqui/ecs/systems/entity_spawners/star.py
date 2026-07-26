import random

import flappy_raqui.ecs.spawners as entity_spawner
from flappy_raqui.ecs.systems.entity_spawners.base import BaseSpawnerProcessor


class StarSpawnerProcessor(BaseSpawnerProcessor):
    def __init__(
        self,
        spawn_interval: float,
        x: int,
        y: int,
        dx: tuple[float, float],
        rotation_speed: tuple[int, int] | None = None,
    ):
        super().__init__(spawn_interval)
        self.x = x
        self.y = y
        self.dx = dx
        self.rotation_speed = rotation_speed

    def spawn_entity_logic(self) -> None:
        _ = entity_spawner.StarEntitySpawner().spawn_entity(
            x=self.x,
            y=self.y,
            dx=random.randint(*self.dx),
            rotation_speed=random.randint(*self.rotation_speed)
            if self.rotation_speed
            else None,
        )
