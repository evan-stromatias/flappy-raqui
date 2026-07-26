import esper

import flappy_raqui.ecs.components as Component
from flappy_raqui.ecs.spawners.base import EntitySpawnerABC
from flappy_raqui.pyrayngine.resource_managers.texture_manager import TextureManager


class PlayerEntitySpawner(EntitySpawnerABC):
    def spawn_entity(
        self,
        x: int,
        y: int,
        gravity: float,
        anti_gravity: float,
        scale: float = 1.0,
        z_order: int = 10,
    ) -> int:
        player_texture_data = TextureManager().get_texture_data("player")
        return esper.create_entity(
            Component.Position(x=x, y=y),
            Component.Velocity(x=0.0, y=0.0),
            Component.Gravity(gravity),
            Component.AntiGravity(anti_gravity),
            Component.Sprite.from_texture(player_texture_data.texture, scale=scale),
            Component.Player(),
            Component.CollisionBox(
                0,
                0,
                player_texture_data.width * scale,
                player_texture_data.height * scale,
            ),
            Component.Score(0),
            Component.Depth(z_order),
        )
