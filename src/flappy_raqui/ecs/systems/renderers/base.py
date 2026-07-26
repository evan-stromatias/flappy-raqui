from abc import ABC, abstractmethod

import esper
import pyray as pr

import flappy_raqui.ecs.components as Component
from flappy_raqui.pyrayngine.collisions.axis_aligned_bounding_boxes import (
    get_rotated_texture_aabb,
)


class BaseRenderProcessor(ABC, esper.Processor):
    def __init__(self, debug: bool = False):
        self.debug = debug
        self._bbox_line_thickness = 1
        self._bbox_line_color = pr.RED

    def _render_obb(self):
        for ent, (obb_box, pos) in esper.get_components(
            Component.ObbCollisionBox, Component.Position
        ):
            obb = get_rotated_texture_aabb(
                obb_box.center, obb_box.w, obb_box.h, obb_box.rotation
            )
            obb.x = pos.x + obb.x
            obb.y = pos.y + obb.y
            pr.draw_rectangle_lines_ex(obb, self._bbox_line_thickness, pr.RED)
            pr.draw_circle_v(obb_box.center, 2, pr.GREEN)

    def _render_debug(self):
        for ent, (box, pos) in esper.get_components(
            Component.CollisionBox, Component.Position
        ):
            bbox = pr.Rectangle(
                pos.x + int(box.x),
                pos.y + int(box.y),
                int(box.w),
                int(box.h),
            )
            pr.draw_rectangle_lines_ex(
                bbox, self._bbox_line_thickness, self._bbox_line_color
            )

    def process(self, *args, **kwargs) -> None:
        self.render()
        if self.debug:
            self._render_debug()
            self._render_obb()
            pr.draw_text(f"{len(esper._entities)}", 1280 - 100, 20, 20, pr.VIOLET)
            pr.draw_fps(1280 - 100, 0)

    @abstractmethod
    def render(self) -> None:
        """ """
