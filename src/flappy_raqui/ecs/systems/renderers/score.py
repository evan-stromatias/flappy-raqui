import esper
import pyray as pr
import raylib as rl

import flappy_raqui.ecs.components as Component
from flappy_raqui.ecs.systems.renderers.base import BaseRenderProcessor
from flappy_raqui.pyrayngine.resource_managers.font_manager import FontManager


class RenderScoreProcessor(BaseRenderProcessor):
    def render(self) -> None:
        for ent, (score, _) in esper.get_components(Component.Score, Component.Player):
            font = FontManager().get_font("huge")
            pr.set_texture_filter(font.texture, rl.TEXTURE_FILTER_POINT)
            pr.draw_text_ex(font, f"{int(score.value)}", [10, 10], 40, 1, pr.BLACK)
