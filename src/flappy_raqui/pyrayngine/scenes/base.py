""" """

from abc import ABC, abstractmethod
from typing import Any

from flappy_raqui.pyrayngine.helpers.class_property import classproperty


class SceneABC(ABC):
    @classproperty
    def name(cls) -> str:
        return cls.__name__

    @abstractmethod
    def setup(self):
        """"""

    @abstractmethod
    def enter(self, params: Any | None = None):
        """"""

    @abstractmethod
    def exit(self):
        """"""

    @abstractmethod
    def update(self, dt: float):
        """"""

    @abstractmethod
    def render(self):
        """"""

    @abstractmethod
    def destroy(self):
        """"""


class SceneBase(SceneABC):
    """"""

    def setup(self):
        """"""

    def enter(self, params: Any | None = None):
        """"""

    def exit(self):
        """"""

    def update(self, dt: float):
        """"""

    def render(self):
        """"""

    def destroy(self):
        """"""
