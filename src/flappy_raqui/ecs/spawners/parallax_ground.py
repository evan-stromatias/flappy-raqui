import esper

import flappy_raqui.ecs.components as Component
from flappy_raqui.ecs.spawners.base import EntitySpawnerABC
from flappy_raqui.pyrayngine.resource_managers.texture_manager import TextureManager


class ParallaxGroundEntitySpawner(EntitySpawnerABC):
    def spawn_entity(self, x: int, y: int, z_order: int, scale: float = 2.0) -> int:
        ground_texture = TextureManager().get_texture("ground")
        return esper.create_entity(
            Component.Parallax(z_order=z_order),
            Component.Position(x=x, y=y - ground_texture.height),
            Component.Velocity(x=-100, y=0.0),
            Component.Sprite(
                texture=ground_texture,
                scale=scale,
                width=ground_texture.width,
                height=ground_texture.height,
            ),
        )
