import esper

import flappy_raqui.ecs.components as Component


class PositionProcessor(esper.Processor):
    def process(self, dt: float):
        for ent, (velocity, position) in esper.get_components(
            Component.Velocity, Component.Position
        ):
            velocity_x = velocity.x * dt
            velocity_y = velocity.y * dt
            position.x += velocity_x
            position.y += velocity_y
