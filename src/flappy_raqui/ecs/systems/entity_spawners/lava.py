import random

import flappy_raqui.ecs.spawners as entity_spawner
from flappy_raqui.ecs.systems.entity_spawners.base import BaseSpawnerProcessor
from flappy_raqui.pyrayngine.resource_managers.texture_manager import (
    AnimatedTextureManager,
)


class LavaSpawnerProcessor(BaseSpawnerProcessor):
    def __init__(
        self, spawn_interval: float, x: int, dx: float, anim_speed: float = 1.0
    ):
        super().__init__(spawn_interval)
        self.anim_speed = anim_speed
        self.x = x
        self.dx = dx
        self._texture = AnimatedTextureManager().get_animated_texture_data("lava")

    def spawn_entity_logic(self) -> None:
        lava_height = random.randint(2, 4)
        for i in range(0, lava_height):
            y = 570 - self._texture.height * i
            _ = entity_spawner.LavaEntitySpawner().spawn_entity(
                x=self.x, y=y, dx=self.dx, dy=0.0, frame_time=self.anim_speed, z_order=1
            )
