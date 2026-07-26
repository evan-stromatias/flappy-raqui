import esper

import flappy_raqui.ecs.components as Component


class UpdateParallaxProcessor(esper.Processor):
    def __init__(self):
        self.timer_ground = 0.0

    def process(self, dt: float):
        for ent, (_, sprite, position, velocity) in esper.get_components(
            Component.Parallax, Component.Sprite, Component.Position, Component.Velocity
        ):
            scrolling_x = position.x
            scrolling_y = position.y

            scrolling_x = 0 if scrolling_x <= -sprite.texture.width * 2 else scrolling_x
            scrolling_y = (
                0 if scrolling_y <= -sprite.texture.height * 2 else scrolling_y
            )

            position.x = scrolling_x
            position.y = scrolling_y

            if collision_box := esper.try_component(ent, Component.CollisionBox):
                collision_box.x = 0
            if collision_box := esper.try_component(ent, Component.ObbCollisionBox):
                collision_box.center.x = 0
