import random

import esper

import flappy_raqui.ecs.components as Component
from flappy_raqui.ecs.spawners.base import EntitySpawnerABC
from flappy_raqui.pyrayngine.animation.spritesheet import (
    SpritesheetAnimator,
    generate_collision_boxes_from_spritesheet,
)
from flappy_raqui.pyrayngine.resource_managers.texture_manager import TextureManager


class BirdEntitySpawner(EntitySpawnerABC):
    ROWS = 2
    COLS = 4
    ANIMATIONS = {
        "idle": {
            "frames": [(0, 0), (0, 1)],  # Still on row 0
            "frame_time": 0.1,
        },
        "fly": {
            # Walk animation starting on row 0 and continuing on row 1
            "frames": [(0, 2), (0, 3), (1, 0)],  # Frames from row 1
            "frame_time": 0.1,
        },
        "fall": {
            "frames": [(1, 1), (1, 2)],  # All on row 1
            "frame_time": 0.1,
        },
        "die": {
            "frames": [(1, 3)],
            "frame_time": 0.1,
        },
    }

    def __init__(self):
        self.texture_data = TextureManager().get_texture_data("birdy")
        self.collision_boxes_map = generate_collision_boxes_from_spritesheet(
            texture=self.texture_data.texture,
            rows=self.ROWS,
            cols=self.COLS,
            animations=self.ANIMATIONS,
        )

    def spawn_entity(
        self,
        x: int,
        y: int,
        dx: float,
        dy: float = 0.0,
        scale: float = 1.0,
        frame_time: float = 1.0,
        z_order: int = 1,
        rotation_speed: int | None = None,
    ) -> int:
        birdy = SpritesheetAnimator(
            texture=self.texture_data.texture,
            rows=self.ROWS,
            cols=self.COLS,
            default_frame_time=frame_time,
            animations=self.ANIMATIONS,
            collision_boxes_map=self.collision_boxes_map,
        )
        y = random.randint(0, int(max(y - birdy.frame_height, birdy.frame_height)))
        return esper.create_entity(
            birdy,
            Component.Position(x, y),
            Component.Velocity(dx, dy),
            Component.Enemy(),
            Component.SpriteAnimation(current_animation="fly"),
            Component.Bird(),
            Component.Sprite(
                texture=birdy.texture,
                scale=scale,
                width=birdy.width,
                height=birdy.height,
            ),
            Component.Depth(z_order=z_order),
            Component.CollisionBox(0, 0, 0, 0),
        )
