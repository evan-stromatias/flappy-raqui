import esper

import flappy_raqui.ecs.components as Component


class KillDeadProcessor(esper.Processor):
    def process(self, dt: float):
        for ent, liveliness in esper.get_component(Component.Liveliness):
            if not liveliness.is_alive:
                esper.delete_entity(ent)
