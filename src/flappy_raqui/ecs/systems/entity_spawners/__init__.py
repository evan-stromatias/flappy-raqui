"""Esper processors that call the entity factories on an interval"""

from flappy_raqui.ecs.systems.entity_spawners.base import BaseSpawnerProcessor
from flappy_raqui.ecs.systems.entity_spawners.bird import BirdSpawnerProcessor
from flappy_raqui.ecs.systems.entity_spawners.cloud import CloudSpawnerProcessor
from flappy_raqui.ecs.systems.entity_spawners.lava import LavaSpawnerProcessor
from flappy_raqui.ecs.systems.entity_spawners.star import StarSpawnerProcessor

__all__ = [
    "BaseSpawnerProcessor",
    "BirdSpawnerProcessor",
    "StarSpawnerProcessor",
    "LavaSpawnerProcessor",
    "CloudSpawnerProcessor",
]
