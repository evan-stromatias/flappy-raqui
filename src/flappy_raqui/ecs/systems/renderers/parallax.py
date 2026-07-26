import esper
import pyray as pr
import raylib as rl

import flappy_raqui.ecs.components as Component
from flappy_raqui.ecs.systems.renderers.base import BaseRenderProcessor


class RenderParallaxProcessor(BaseRenderProcessor):
    def render(self) -> None:
        data = esper.get_components(
            Component.Sprite, Component.Position, Component.Parallax
        )
        # sort data based on the z_order value
        sorted_list = sorted(data, key=lambda item: item[1][2].z_order)
        for ent, (sprite, position, par) in sorted_list:
            pr.draw_texture_ex(
                sprite.texture,
                pr.Vector2(position.x, position.y),
                0.0,
                sprite.scale,
                rl.WHITE,
            )
            pr.draw_texture_ex(
                sprite.texture,
                pr.Vector2(sprite.texture.width * 2 + position.x, position.y),
                0.0,
                sprite.scale,
                rl.WHITE,
            )
