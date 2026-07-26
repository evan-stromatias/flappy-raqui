import esper
import pyray as pr

import flappy_raqui.ecs.components as Component
from flappy_raqui.pyrayngine.collisions.axis_aligned_bounding_boxes import (
    get_rotated_texture_aabb,
)


class CheckCollisionProcessor(esper.Processor):
    def process(self, dt: float):
        ents_components_map = {}
        for ent, components in esper.get_components(
            Component.ObbCollisionBox, Component.Position
        ):
            obb_collision_box = components[0]
            rect = get_rotated_texture_aabb(
                obb_collision_box.center,
                obb_collision_box.w,
                obb_collision_box.h,
                obb_collision_box.rotation,
            )
            collision_box = Component.CollisionBox(
                x=rect.x, y=rect.y, w=rect.width, h=rect.height
            )
            ents_components_map[ent] = [ent, [collision_box, components[1:]]]
        for ent, components in esper.get_components(
            Component.CollisionBox, Component.Position
        ):
            ents_components_map[ent] = [ent, components]
        components = list(ents_components_map.values())
        for i in range(len(components)):
            a_ent, (a_obb_box, a_pos) = components[i]
            for j in range(i + 1, len(components)):
                b_ent, (b_obb_box, b_pos) = components[j]

                a_box = a_obb_box
                b_box = b_obb_box

                if a_box.collision_group != b_box.collision_group:
                    continue

                a_rect = pr.Rectangle(a_box.x, a_box.y, a_box.w, a_box.h)
                b_rect = pr.Rectangle(b_box.x, b_box.y, b_box.w, b_box.h)

                # stars have list of 1
                a_pos = a_pos[0] if isinstance(a_pos, list) else a_pos
                b_pos = b_pos[0] if isinstance(b_pos, list) else b_pos

                a_rect.x = a_pos.x + a_rect.x
                a_rect.y = a_pos.y + a_rect.y
                b_rect.x = b_pos.x + b_rect.x
                b_rect.y = b_pos.y + b_rect.y

                collided = pr.check_collision_recs(a_rect, b_rect)

                if collided:
                    esper.add_component(a_ent, Component.CollidedWith(b_ent))
                    esper.add_component(b_ent, Component.CollidedWith(a_ent))
