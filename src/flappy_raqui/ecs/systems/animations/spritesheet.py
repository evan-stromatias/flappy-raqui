import esper

import flappy_raqui.ecs.components as Component
from flappy_raqui.pyrayngine.animation.spritesheet import SpritesheetAnimator


class UpdateSpriteSheetAnimations(esper.Processor):
    """"""

    def process(self, dt: float):
        """"""
        for ent, (spritesheet_animation, animation, sprite) in esper.get_components(
            SpritesheetAnimator, Component.SpriteAnimation, Component.Sprite
        ):
            spritesheet_animation.play_animation(animation.current_animation)
            spritesheet_animation.update(dt=dt)
            sprite.source_rect = spritesheet_animation.get_source_rect()
            sprite.width = sprite.source_rect.width
            sprite.height = sprite.source_rect.height
            if bbox := esper.try_component(ent, Component.CollisionBox):
                sprite_bbox = spritesheet_animation.get_collision_box()
                bbox.x = sprite_bbox.x
                bbox.y = sprite_bbox.y
                bbox.w = sprite_bbox.width
                bbox.h = sprite_bbox.height
