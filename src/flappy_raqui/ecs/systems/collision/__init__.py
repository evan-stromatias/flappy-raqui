"""Collision detection, resolution, and the per-interaction handlers.

Re-exported here so callers can use ``flappy_raqui.ecs.systems.collision`` as a
flat namespace or import a specific module directly.
"""

from flappy_raqui.ecs.systems.collision.detection import CheckCollisionProcessor
from flappy_raqui.ecs.systems.collision.handlers import (
    player_bird_collision,
    player_lava_collision,
    player_star_collision,
    popcorn_bird_collision,
)
from flappy_raqui.ecs.systems.collision.resolution import CollisionResolutionProcessor

__all__ = [
    "CheckCollisionProcessor",
    "CollisionResolutionProcessor",
    "player_lava_collision",
    "player_star_collision",
    "player_bird_collision",
    "popcorn_bird_collision",
]
