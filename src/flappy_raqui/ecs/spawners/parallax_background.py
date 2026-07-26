import esper

import flappy_raqui.ecs.components as Component
from flappy_raqui.ecs.spawners.base import EntitySpawnerABC
from flappy_raqui.pyrayngine.resource_managers.texture_manager import TextureManager


class ParallaxBackgroundEntitySpawner(EntitySpawnerABC):
    def spawn_entity(self, x: int, y: int, z_order: int, scale: float = 2.0) -> int:
        background_texture = TextureManager().get_texture("background")
        return esper.create_entity(
            Component.Parallax(z_order=z_order),
            Component.Position(x=x, y=y),
            Component.Velocity(x=-15, y=0.0),
            Component.Sprite(
                texture=background_texture,
                scale=scale,
                width=background_texture.width,
                height=background_texture.height,
            ),
        )
