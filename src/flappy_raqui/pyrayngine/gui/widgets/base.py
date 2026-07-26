from abc import ABC, abstractmethod

import pyray as pr
import raylib as rl


class WidgetBase(ABC):
    def __init__(
        self,
        name: str | None = None,
        selectable: bool = True,
        on_pressed=None,
        on_updated=None,
        size_hint: tuple[float, float] | None = None,
        use_outline: bool = False,
        enabled: bool = True,
        debug: bool = False,
    ):
        self.name = name
        self.selectable = selectable
        self.on_pressed = on_pressed
        self.on_updated = on_updated
        self.size_hint = size_hint
        self.outline = use_outline
        self.enabled = enabled
        self.debug = debug

        self.is_mouse_clicked = False
        self.is_mouse_hover = False

    def update(self, dt: float) -> None:
        """"""
        if self.is_mouse_hover and pr.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            self.is_mouse_clicked = True
        else:
            self.is_mouse_clicked = False

    def render(self, x: int, y: int, w: int, h: int) -> None:
        """"""
        mouse_pos = pr.get_mouse_position()
        button_rec = pr.Rectangle(x, y, w, h)
        mouse_rec = pr.Rectangle(mouse_pos.x, mouse_pos.y, 1, 1)
        pr.draw_rectangle_rec(mouse_rec, pr.PURPLE)

        if pr.check_collision_recs(mouse_rec, button_rec):
            self.is_mouse_hover = True
            if self.enabled:
                pr.draw_rectangle_rec(button_rec, pr.YELLOW)
        else:
            self.is_mouse_hover = False

    def update_on_pressed(self, func) -> None:
        self.on_pressed = func

    def update_on_updated(self, func) -> None:
        self.on_updated = func

    def get_widgets(self):
        return self

    def __getitem__(self, index):
        if index < 0 or index >= 1:
            raise IndexError
        return self

    def __repr__(self):
        return f"<{self.__class__.__name__}>({self.name})"
