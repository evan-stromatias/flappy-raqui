import esper
import pyray as pr
import raylib as rl

import flappy_raqui.ecs.components as Component
from flappy_raqui.ecs.systems.renderers.base import BaseRenderProcessor


class RenderSpritesProcessor(BaseRenderProcessor):
    def render(self) -> None:
        data = esper.get_components(
            Component.Depth, Component.Sprite, Component.Position
        )
        sorted_list = sorted(data, key=lambda item: item[1][0].z_order)

        for ent, (depth, sprite, position) in sorted_list:
            if esper.has_component(ent, Component.Parallax):
                continue

            rotation = 0.0
            if rotation_c := esper.try_component(ent, Component.RotationSpeed):
                rotation = rotation_c.rotation
            source_rect = (
                pr.Rectangle(0, 0, sprite.texture.width, sprite.texture.height)
                if sprite.source_rect is None
                else sprite.source_rect
            )
            dest_rect = pr.Rectangle(
                position.x + (sprite.width * sprite.scale) // 2,
                position.y + (sprite.height * sprite.scale) // 2,
                sprite.width * sprite.scale,
                sprite.height * sprite.scale,
            )
            origin = pr.Vector2(
                (sprite.width * sprite.scale) // 2, (sprite.height * sprite.scale) // 2
            )
            pr.draw_texture_pro(
                sprite.texture, source_rect, dest_rect, origin, rotation, rl.WHITE
            )
