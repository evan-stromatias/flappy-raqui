"""Entity factories: each builds a single entity on demand (the "how").

One class per module; re-exported here so callers can use
``flappy_raqui.ecs.spawners`` as a flat namespace or import a specific module
directly (``from flappy_raqui.ecs.spawners.bird import BirdEntitySpawner``).
"""

from flappy_raqui.ecs.spawners.base import EntitySpawnerABC
from flappy_raqui.ecs.spawners.bird import BirdEntitySpawner
from flappy_raqui.ecs.spawners.cloud import CloudEntitySpawner
from flappy_raqui.ecs.spawners.ground_lava import GroundLavaEntitySpawner
from flappy_raqui.ecs.spawners.lava import LavaEntitySpawner
from flappy_raqui.ecs.spawners.parallax_background import (
    ParallaxBackgroundEntitySpawner,
)
from flappy_raqui.ecs.spawners.parallax_ground import ParallaxGroundEntitySpawner
from flappy_raqui.ecs.spawners.player import PlayerEntitySpawner
from flappy_raqui.ecs.spawners.popcorn import PopCornEntitySpawner
from flappy_raqui.ecs.spawners.smoke import SmokeEntitySpawner
from flappy_raqui.ecs.spawners.star import StarEntitySpawner

__all__ = [
    "EntitySpawnerABC",
    "PlayerEntitySpawner",
    "GroundLavaEntitySpawner",
    "ParallaxGroundEntitySpawner",
    "ParallaxBackgroundEntitySpawner",
    "SmokeEntitySpawner",
    "PopCornEntitySpawner",
    "CloudEntitySpawner",
    "StarEntitySpawner",
    "LavaEntitySpawner",
    "BirdEntitySpawner",
]
