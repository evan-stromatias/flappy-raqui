import pyray as pr
import raylib as rl

from ..widgets.base import WidgetBase
from .base import LayoutBase


def linspace(a, b, n=100):
    if n < 2:
        return b
    diff = (float(b) - a) / (n - 1)
    return [diff * i + a for i in range(n)]


class BoxLayout(LayoutBase):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    ORIENTATIONS = (VERTICAL, HORIZONTAL)

    def __init__(
        self,
        orientation: str,
        label: str | None = None,
        spacing: int | None = None,
        select_key: int = rl.KEY_SPACE,
        debug: bool = False,
    ):
        if orientation not in self.ORIENTATIONS:
            raise ValueError(f"Select a correct orientation: {self.ORIENTATIONS}")

        self.orientation = orientation
        self.label = label
        self.spacing = spacing
        self.debug = debug

        self.select_key = select_key

        self._widgets = []
        self._widget_selected = 0
        self._selected = False

    def add_widget(self, widget: WidgetBase):
        self._widgets.append(widget)

    def _update_positions(self, x, y, w, h):
        if self.orientation == self.HORIZONTAL:
            w_starts = linspace(x, x + w, len(self._widgets) + 1)
            for i, _w in enumerate(self._widgets):
                x1 = w_starts[i]
                x2 = w_starts[i + 1]
                _w.render(x1, y, x2 - x1, h)
        else:
            h_starts = linspace(y, y + h, len(self._widgets) + 1)
            for i, _w in enumerate(self._widgets):
                y1 = h_starts[i]
                y2 = h_starts[i + 1]
                _w.render(x, y1, w, y2 - y1)

    def render(self, x, y, w, h):
        if not self._widgets:
            return

        self._update_positions(x, y, w, h)

        if self._selected and self.debug:
            pr.draw_rectangle_rounded_lines(
                pr.Rectangle(int(x), int(y), int(w), int(h)), 0.5, 5, 2.0, pr.GREEN
            )

    def update(self, dt, selected: bool = False, select_key_pressed: bool = False):
        self._selected = selected
        if self._selected:
            if pr.is_key_pressed(rl.KEY_RIGHT):
                self._widget_selected = (
                    self._widget_selected + 1 if self._widgets else None
                )

            if pr.is_key_pressed(rl.KEY_LEFT):
                self._widget_selected = (
                    self._widget_selected - 1 if self._widgets else None
                )

            self._widget_selected = self._widget_selected % len(self._widgets)

            for i, _w in enumerate(self._widgets):
                select_key_pressed = True if pr.is_key_down(self.select_key) else False
                _w.update(
                    dt,
                    selected=i == self._widget_selected,
                    select_key_pressed=select_key_pressed,
                )

    def get_widgets(self):
        return self._widgets

    def __iter__(self):
        for each in self._widgets:
            yield each

    def __repr__(self):
        return f"<{self.__class__.__name__}>({list(self)})"
