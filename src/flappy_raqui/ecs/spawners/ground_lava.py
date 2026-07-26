import esper

import flappy_raqui.ecs.components as Component
from flappy_raqui.ecs.spawners.base import EntitySpawnerABC
from flappy_raqui.pyrayngine.resource_managers.texture_manager import TextureManager


class GroundLavaEntitySpawner(EntitySpawnerABC):
    def spawn_entity(self, x: int, y: int, scale: float = 2.0) -> int:
        ground_texture = TextureManager().get_texture("ground")
        return esper.create_entity(
            Component.CollisionBox(x=0, y=0, w=1280, h=570),
            Component.Position(x=x, y=y - ground_texture.height),
            Component.Enemy(),
            Component.Lava(),
        )
