import esper

import flappy_raqui.ecs.components as Component
from flappy_raqui.ecs.spawners.base import EntitySpawnerABC
from flappy_raqui.pyrayngine.animation.gif import GifAnimator
from flappy_raqui.pyrayngine.resource_managers.texture_manager import (
    AnimatedTextureManager,
)


class LavaEntitySpawner(EntitySpawnerABC):
    def spawn_entity(
        self,
        x: int,
        y: int,
        dx: float,
        dy: float = 0.0,
        scale: float = 1.0,
        frame_time: float = 1.0,
        z_order: int = 1,
    ) -> int:
        texture = AnimatedTextureManager().get_animated_texture_data("lava")
        lava = GifAnimator(
            texture=texture.texture,
            image=texture.image,
            frames=texture.frames,
            frame_time=frame_time,
            current_frame=0,
        )
        return esper.create_entity(
            lava,
            Component.Position(x, y),
            Component.CollisionBox(0, 0, texture.width, texture.height),
            Component.Velocity(dx, dy),
            Component.Enemy(),
            Component.Lava(),
            Component.Sprite.from_texture(texture.texture, scale=scale),
            Component.Depth(z_order=z_order),
        )
