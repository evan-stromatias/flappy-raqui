import pyray as pr
import raylib as rl

from .base import WidgetBase
from .types import ColorT


class Button(WidgetBase):
    def __init__(
        self,
        label: str,
        font=None,
        font_size: int = 20,
        text_color_selected: ColorT = pr.RED,
        text_color_unselected: ColorT = pr.BLACK,
        bg_color: ColorT | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.selectable = True
        self.label = label
        self.font_size = font_size
        self.bg_color = bg_color
        self.text_color_selected = text_color_selected
        self.text_color_unselected = text_color_unselected
        self.font = font
        self._selected = False
        self._pressed = False

    def render(self, x, y, w, h):
        super().render(x, y, w, h)

        if self.debug:
            pr.draw_rectangle_lines_ex(
                pr.Rectangle(int(x), int(y), int(w), int(h)), 1, pr.DARKGRAY
            )

        if self.bg_color:
            pr.draw_rectangle(int(x), int(y), int(w), int(h), self.bg_color)

        text_color = (
            self.text_color_selected if self._selected else self.text_color_unselected
        )
        t = pr.measure_text(self.label, self.font_size)

        text_x, text_y = int(x + w // 2 - t // 2), int(y + h / 2 - self.font_size // 2)
        if not self.font:
            pr.draw_text(self.label, text_x, text_y, self.font_size, text_color)
        else:
            pr.draw_text_ex(
                self.font,
                self.label,
                pr.Vector2(text_x, text_y),
                self.font_size,
                1.0,
                text_color,
            )

        if (self._selected and self.outline) or self.is_mouse_hover:
            pr.draw_rectangle_rounded_lines(
                pr.Rectangle(int(x), int(y), int(w), int(h)), 0.1, 5, pr.RED
            )

    def update(
        self, dt: float, selected: bool = False, select_key_pressed: bool = False
    ):
        super().update(dt=dt)
        self._selected = selected

        if self.enabled:
            if (selected and select_key_pressed) or self.is_mouse_clicked:
                self._pressed = True
                if self.on_pressed:
                    self.on_pressed()
                    self.reset_pressed()

    def reset_pressed(self):
        self._pressed = False
