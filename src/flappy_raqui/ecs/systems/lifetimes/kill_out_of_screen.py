import esper

import flappy_raqui.ecs.components as Component


class KillOutOfScreenProcessor(esper.Processor):
    def process(self, dt: float):
        for ent, (pos, _) in esper.get_components(
            Component.Position, Component.Removable
        ):
            if pos.x < 0:
                esper.delete_entity(ent)

        for ent, (pos, box) in esper.get_components(
            Component.Position, Component.CollisionBox
        ):
            self._check_and_remove_entity(
                ent, x=pos.x + box.x, y=pos.y + box.y, width=box.w, height=box.h
            )

        for ent, (pos, box) in esper.get_components(
            Component.Position, Component.ObbCollisionBox
        ):
            self._check_and_remove_entity(
                ent,
                x=pos.x + box.center.x,
                y=pos.y + box.center.y,
                width=box.w,
                height=box.h,
            )

    @staticmethod
    def _check_and_remove_entity(ent: int, x: int, y: int, width: int, height: int):
        if x + width < 0:
            esper.delete_entity(ent)
        if y > 570 + height:
            esper.delete_entity(ent)
