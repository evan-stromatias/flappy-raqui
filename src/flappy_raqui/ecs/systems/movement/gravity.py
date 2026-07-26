import esper

import flappy_raqui.ecs.components as Component


class GravityProcessor(esper.Processor):
    def process(self, dt: float):
        for ent, (velocity, gravity) in esper.get_components(
            Component.Velocity, Component.Gravity
        ):
            velocity.y += gravity.value * dt
