import random

import esper

import flappy_raqui.ecs.components as Component
from flappy_raqui.ecs.spawners.base import EntitySpawnerABC
from flappy_raqui.pyrayngine.resource_managers.texture_manager import TextureManager


class CloudEntitySpawner(EntitySpawnerABC):
    def __init__(self):
        self.cloud_sprite_names = ["cloud1", "cloud2", "cloud3", "cloud4"]

    def spawn_entity(
        self, x: int, y: int, dx: float, dy: float = 0.0, scale: float = 2.0
    ) -> int:
        texture = TextureManager().get_texture(random.choice(self.cloud_sprite_names))
        return esper.create_entity(
            Component.Sprite.from_texture(texture, scale=scale),
            Component.Position(x, random.randint(texture.height, int(y))),
            Component.Velocity(dx, dy),
            Component.Depth(),
            Component.Removable(),
        )
