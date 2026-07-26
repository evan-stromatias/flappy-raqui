import random

import esper

import flappy_raqui.ecs.components as Component
from flappy_raqui.ecs.spawners.base import EntitySpawnerABC
from flappy_raqui.pyrayngine.animation.gif import GifAnimator
from flappy_raqui.pyrayngine.resource_managers.texture_manager import (
    AnimatedTextureManager,
)


class StarEntitySpawner(EntitySpawnerABC):
    def spawn_entity(
        self,
        x: int,
        y: int,
        dx: float,
        dy: float = 0.0,
        scale: float = 1.0,
        frame_time: float = 0.05,
        z_order: int = 2,
        rotation_speed: int | None = None,
    ) -> int:
        texture = AnimatedTextureManager().get_animated_texture_data("star")
        star = GifAnimator(
            texture=texture.texture,
            image=texture.image,
            frames=texture.frames,
            frame_time=frame_time,
            current_frame=random.randint(0, texture.frames),
        )
        y = random.randint(texture.height, int(y))
        components = [
            star,
            Component.Position(x, y),
            Component.Velocity(x=dx, y=dy),
            Component.Star(),
            Component.Sprite.from_texture(texture.texture, scale=scale),
            Component.Depth(z_order=z_order),
        ]

        if rotation_speed is not None:
            components.append(Component.RotationSpeed(speed=rotation_speed))
            components.append(
                Component.ObbCollisionBox.from_texture(
                    texture.texture,
                    0,
                    0,
                    scale=scale,
                )
            )
        else:
            components.append(
                Component.CollisionBox(0, 0, texture.width, texture.height)
            )
        return esper.create_entity(*components)
