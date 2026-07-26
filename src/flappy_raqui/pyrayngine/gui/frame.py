from collections.abc import Iterable
from itertools import chain

import pyray as pr
import raylib as rl

from .layouts.base import LayoutBase
from .widgets.base import WidgetBase


def flatten(nested_iterable):
    for item in nested_iterable:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            yield from chain(flatten(item))  # Recursively flatten using chain
        else:
            yield item  # Yield non-iterable item directly


class WindowFrame:
    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        win_w,
        win_h,
        select_key: int = rl.KEY_SPACE,
        debug: bool = False,
    ):
        self.debug = debug
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
        self.win_w = win_w
        self.win_h = win_h
        self.select_key = select_key

        self._layouts = []
        self.widgets_flatten: list[WidgetBase] | None = None
        self.widgets_names: dict[str, WidgetBase] = {}
        self._widget_selected: int = 0

    def setup(self):
        self.widgets_flatten = list(flatten(self._layouts))
        for i, widget in enumerate(self.widgets_flatten):
            if name := widget.name:
                self.widgets_names[name] = widget

    def get_widget(self, name: str) -> WidgetBase:
        return self.widgets_names[name]

    def update_on_update(self, widget_name: str, func) -> None:
        self.widgets_names[widget_name].update_on_updated(func)

    def add_layout(self, widget: LayoutBase):
        self._layouts.append(widget)

    def render(self):
        if self.debug:
            pr.draw_text(f"{self._widget_selected}", 10, 10, 30, pr.BLACK)

        for _w in self._layouts:
            _w.render(self.x, self.y, self.w, self.h)

        if self.debug:
            pr.draw_rectangle_lines(self.x, self.y, self.w, self.h, pr.RED)

    def update(self, dt: float):
        if pr.is_key_pressed(rl.KEY_DOWN):
            self._widget_selected = (
                self._widget_selected + 1 if self.widgets_flatten else None
            )
            self._widget_selected = self._widget_selected % len(self.widgets_flatten)

            if not self.widgets_flatten[self._widget_selected].selectable:
                self._widget_selected += 1

        if pr.is_key_pressed(rl.KEY_UP):
            self._widget_selected = (
                self._widget_selected - 1 if self.widgets_flatten else None
            )
            self._widget_selected = self._widget_selected % len(self.widgets_flatten)
            if not self.widgets_flatten[self._widget_selected].selectable:
                self._widget_selected -= 1

        self._widget_selected = self._widget_selected % len(self.widgets_flatten)
        if not self.widgets_flatten[self._widget_selected].selectable:
            self._widget_selected += 1
        self._widget_selected = self._widget_selected % len(self.widgets_flatten)

        pr.draw_text(
            f"Widget = {self.widgets_flatten[self._widget_selected]}, name={self.widgets_flatten[self._widget_selected].name}, selectable={self.widgets_flatten[self._widget_selected].selectable}",
            10,
            10,
            30,
            pr.RED,
        )

        for i, _w in enumerate(self.widgets_flatten):
            select_key_pressed = True if pr.is_key_pressed(self.select_key) else False
            _w.update(
                dt,
                selected=i == self._widget_selected,
                select_key_pressed=select_key_pressed,
            )
