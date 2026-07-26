"""Processors that draw the world each frame"""

from flappy_raqui.ecs.systems.renderers.base import BaseRenderProcessor
from flappy_raqui.ecs.systems.renderers.parallax import RenderParallaxProcessor
from flappy_raqui.ecs.systems.renderers.score import RenderScoreProcessor
from flappy_raqui.ecs.systems.renderers.sprites import RenderSpritesProcessor

__all__ = [
    "BaseRenderProcessor",
    "RenderParallaxProcessor",
    "RenderSpritesProcessor",
    "RenderScoreProcessor",
]
