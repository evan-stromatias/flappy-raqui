import esper

import flappy_raqui.ecs.components as Component
from flappy_raqui.ecs.spawners.base import EntitySpawnerABC
from flappy_raqui.pyrayngine.animation.gif import GifAnimator
from flappy_raqui.pyrayngine.resource_managers.texture_manager import (
    AnimatedTextureManager,
)


class SmokeEntitySpawner(EntitySpawnerABC):
    def __init__(
        self, frame_animation_time: float = 0.03, loop_animation: bool = False
    ):
        self.frame_animation_time = frame_animation_time
        self.loop_animation = loop_animation

    def spawn_entity(
        self,
        x: int,
        y: int,
        dx: float = 0.0,
        dy: float = 0.0,
        scale: float = 1.0,
        z_order: int = 2,
    ) -> int:
        smoke_animated_texture_data = (
            AnimatedTextureManager().get_animated_texture_data("smoke")
        )
        smoke_half_width = smoke_animated_texture_data.width / 2
        smoke_half_height = smoke_animated_texture_data.height / 2
        smoke = GifAnimator(
            texture=smoke_animated_texture_data.texture,
            image=smoke_animated_texture_data.image,
            frames=smoke_animated_texture_data.frames,
            frame_time=self.frame_animation_time,
            current_frame=0,
            loop=self.loop_animation,
        )
        return esper.create_entity(
            smoke,
            Component.Position(x=x - smoke_half_width, y=y - smoke_half_height),
            Component.Liveliness(is_alive=True),
            Component.Velocity(dx, dy),
            Component.Smoke,
            Component.Depth(z_order),
            Component.Sprite.from_texture(
                texture=smoke_animated_texture_data.texture, scale=scale
            ),
        )
