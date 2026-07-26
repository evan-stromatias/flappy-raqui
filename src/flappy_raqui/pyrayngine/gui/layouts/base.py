from abc import ABC, abstractmethod


class LayoutBase(ABC):
    @abstractmethod
    def render(self, x: int, y: int, w: int, h: int):
        """"""

    @abstractmethod
    def update(self, dt, selected: bool = False, select_key_pressed: bool = False):
        """"""
