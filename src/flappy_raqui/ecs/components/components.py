"""Components that carry fields. Field-less tag components live in ``tags``."""

from __future__ import annotations

from dataclasses import dataclass as component
from typing import Union

import pyray as pr


@component
class Position:
    x: float = 0.0
    y: float = 0.0


@component
class Velocity:
    x: float = 0.0
    y: float = 0.0


@component
class RotationSpeed:
    rotation: float = 0.0
    speed: float = 0.0


@component
class Gravity:
    value: float


@component
class AntiGravity:
    value: float


@component
class Depth:
    z_order: int = 0


@component
class Sprite:
    texture: Union[pr.Texture2D, pr.Texture]
    width: int
    height: int
    scale: float = 1.0
    source_rect: pr.Rectangle | None = None

    @classmethod
    def from_texture(
        cls,
        texture: Union[pr.Texture2D, pr.Texture],
        scale: float = 1.0,
        source_rect: pr.Rectangle | None = None,
    ):
        return cls(
            texture=texture,
            width=texture.width,
            height=texture.height,
            scale=scale,
            source_rect=source_rect,
        )


@component
class SpriteAnimation:
    current_animation: str


@component
class Score:
    value: int = 0


@component
class Liveliness:
    is_alive: bool = True


@component
class Parallax:
    z_order: int


@component
class CollisionBox:
    x: float
    y: float
    w: float
    h: float
    collided: bool = False
    collision_group: int = 0


@component
class ObbCollisionBox:
    """Oriented Bounding Boxes (OBB) Collision Detection"""

    center: pr.Vector2
    w: float
    h: float
    rotation: float = 0.0
    collision_group: int = 0

    @classmethod
    def from_texture(
        cls,
        texture: Union[pr.Texture, pr.Texture2D],
        x: float,
        y: float,
        rotation: float = 0.0,
        scale: float = 1.0,
    ):
        return cls(
            center=pr.Vector2(
                x + (texture.width * scale) // 2, y + (texture.height * scale) // 2
            ),
            w=texture.width * scale,
            h=texture.height * scale,
            rotation=rotation,
        )

    @classmethod
    def from_rect(cls, rect: pr.Rectangle, rotation: float = 0.0):
        return cls(
            center=pr.Vector2(rect.x, rect.y),
            w=rect.width,
            h=rect.height,
            rotation=rotation,
        )


@component
class TimeToLive:
    remaining_seconds: float


@component
class CollidedWith:
    entity: int
