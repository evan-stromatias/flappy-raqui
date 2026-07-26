import random

import flappy_raqui.ecs.spawners as entity_spawner
from flappy_raqui.ecs.systems.entity_spawners.base import BaseSpawnerProcessor


class BirdSpawnerProcessor(BaseSpawnerProcessor):
    def __init__(
        self,
        spawn_interval: float,
        x: int,
        y: int,
        default_frame_time: float = 0.1,
        scale: float = 1.0,
    ):
        super().__init__(spawn_interval)
        self.x = x
        self.y = y
        self.scale = scale
        self.default_frame_time = default_frame_time
        self.bird_spawner = entity_spawner.BirdEntitySpawner()

    def spawn_entity_logic(self) -> None:
        _ = self.bird_spawner.spawn_entity(
            x=self.x,
            y=self.y,
            dx=-random.randint(100, 200),
            dy=0,
            frame_time=self.default_frame_time,
        )
