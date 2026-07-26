"""Processors that advance sprite animations each frame"""

from flappy_raqui.ecs.systems.animations.gif import UpdateGifAnimations
from flappy_raqui.ecs.systems.animations.spritesheet import UpdateSpriteSheetAnimations

__all__ = [
    "UpdateSpriteSheetAnimations",
    "UpdateGifAnimations",
]
