"""ECS components.

Fielded components live in ``components``; the field-less tag components live in
``tags``. Re-exported here so callers keep using the flat namespace
(``import flappy_raqui.ecs.components as Component`` then ``Component.Position``).
"""

from flappy_raqui.ecs.components.components import (
    AntiGravity,
    CollidedWith,
    CollisionBox,
    Depth,
    Gravity,
    Liveliness,
    ObbCollisionBox,
    Parallax,
    Position,
    RotationSpeed,
    Score,
    Sprite,
    SpriteAnimation,
    TimeToLive,
    Velocity,
)
from flappy_raqui.ecs.components.tags import (
    Bird,
    Bread,
    Enemy,
    HasTouchedLava,
    Lava,
    Player,
    Removable,
    Smoke,
    Star,
)

__all__ = [
    "Position",
    "Velocity",
    "RotationSpeed",
    "Gravity",
    "AntiGravity",
    "Depth",
    "Sprite",
    "SpriteAnimation",
    "Score",
    "Liveliness",
    "Parallax",
    "CollisionBox",
    "ObbCollisionBox",
    "TimeToLive",
    "CollidedWith",
    "Smoke",
    "Player",
    "Enemy",
    "Star",
    "Lava",
    "Removable",
    "Bird",
    "Bread",
    "HasTouchedLava",
]
