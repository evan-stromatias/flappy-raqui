import esper

import flappy_raqui.ecs.components as Component


class KillBasedOnTimeoutProcessor(esper.Processor):
    def process(self, dt: float):
        for ent, time_to_live in esper.get_component(Component.TimeToLive):
            time_to_live.remaining_seconds -= 1 * dt
            if time_to_live.remaining_seconds <= 0:
                esper.delete_entity(ent)
