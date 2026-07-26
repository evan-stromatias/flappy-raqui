import random

import esper

import flappy_raqui.ecs.components as Component
from flappy_raqui.ecs.spawners.base import EntitySpawnerABC
from flappy_raqui.pyrayngine.resource_managers.texture_manager import TextureManager


class PopCornEntitySpawner(EntitySpawnerABC):
    def __init__(self):
        self.popcorn_sprite_names = ("popcorn1", "popcorn1")

    def spawn_entity(
        self,
        x: int,
        y: int,
        dx: float = 100.0,
        dy: float = 10.0,
        time_to_live_seconds: float = 2,
        scale: float = 1.0,
        z_order: int = 2,
        rotation_speed: float = 100,
    ) -> int:
        texture = TextureManager().get_texture(random.choice(self.popcorn_sprite_names))
        return esper.create_entity(
            Component.Sprite.from_texture(texture, scale=scale),
            Component.Position(x, y),
            Component.Velocity(dx, dy),
            Component.Bread(),
            Component.TimeToLive(remaining_seconds=time_to_live_seconds),
            Component.Depth(z_order),
            Component.RotationSpeed(speed=rotation_speed),
            Component.ObbCollisionBox.from_texture(texture, 0, 0, scale=scale),
        )
