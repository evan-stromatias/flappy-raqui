from typing import Any

from flappy_raqui.pyrayngine.helpers.singleton import SingletonMeta
from flappy_raqui.pyrayngine.scenes.base import SceneABC, SceneBase


class SceneManager(metaclass=SingletonMeta):
    def __init__(self):
        self._scenes: dict[str, SceneABC] = {}
        self._current_scene: SceneABC = SceneBase()
        self.should_exit = False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<{list(self._scenes)}>"

    def add_scene(self, name: str, scene: SceneABC) -> None:
        self._scenes[name] = scene

    def set_current_scene(self, scene_name: str) -> None:
        try:
            self._current_scene = self._scenes[scene_name]
        except KeyError:
            raise KeyError(f"The scene=`{scene_name}` does not exist!")

    def update(self, dt: float) -> None:
        self._current_scene.update(dt=dt)

    def render(self) -> None:
        self._current_scene.render()

    def change_to(self, scene_name: str, params: Any | None = None) -> None:
        try:
            self._current_scene.exit()
            self._current_scene = self._scenes[scene_name]
            self._current_scene.enter(params=params)
        except KeyError:
            raise KeyError(f"The scene=`{scene_name}` does not exist!")

    def load_current_scene(self, params: Any | None = None) -> None:
        if not self._current_scene:
            raise RuntimeError("Current Scene not set!")
        self._current_scene.enter(params)

    def exit(self) -> bool:
        self.should_exit = True

    def destroy(self) -> None:
        for _, scene in self._scenes.items():
            scene.destroy()
