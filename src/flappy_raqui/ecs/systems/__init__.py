"""ECS processors, grouped by concern"""

from flappy_raqui.ecs.systems.animations import (
    UpdateGifAnimations,
    UpdateSpriteSheetAnimations,
)
from flappy_raqui.ecs.systems.collision import (
    CheckCollisionProcessor,
    CollisionResolutionProcessor,
    player_bird_collision,
    player_lava_collision,
    player_star_collision,
    popcorn_bird_collision,
)
from flappy_raqui.ecs.systems.entity_spawners import (
    BaseSpawnerProcessor,
    BirdSpawnerProcessor,
    CloudSpawnerProcessor,
    LavaSpawnerProcessor,
    StarSpawnerProcessor,
)
from flappy_raqui.ecs.systems.lifetimes import (
    KillBasedOnTimeoutProcessor,
    KillDeadProcessor,
    KillOutOfScreenProcessor,
)
from flappy_raqui.ecs.systems.movement import (
    GravityProcessor,
    PositionProcessor,
    UpdateParallaxProcessor,
    UpdateRotationProcessor,
)

__all__ = [
    "GravityProcessor",
    "PositionProcessor",
    "UpdateRotationProcessor",
    "UpdateParallaxProcessor",
    "KillOutOfScreenProcessor",
    "KillDeadProcessor",
    "KillBasedOnTimeoutProcessor",
    "CheckCollisionProcessor",
    "CollisionResolutionProcessor",
    "player_lava_collision",
    "player_star_collision",
    "player_bird_collision",
    "popcorn_bird_collision",
    "UpdateSpriteSheetAnimations",
    "UpdateGifAnimations",
    "BaseSpawnerProcessor",
    "BirdSpawnerProcessor",
    "StarSpawnerProcessor",
    "LavaSpawnerProcessor",
    "CloudSpawnerProcessor",
]
