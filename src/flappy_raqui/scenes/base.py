from abc import ABC, abstractmethod

import pyray as pr
import raylib as rl

from flappy_raqui.pyrayngine.resource_managers.audio_manager import AudioManager
from flappy_raqui.pyrayngine.resource_managers.font_manager import FontManager
from flappy_raqui.pyrayngine.scenes.base import SceneBase
from flappy_raqui.pyrayngine.scenes.scene_manager import SceneManager


class BaseGameScene(SceneBase):
    def __init__(self, width: int, height: int, debug: bool = False):
        super().__init__()
        self.width = width
        self.height = height
        self.debug = debug
        self.should_exit = False
        self.should_exit_changed = False
        self.pause = False
        self._timer = 0

    def _play_sound(self, sound: str):
        if not self.pause:
            AudioManager().play(sound)

    def render(self):
        pr.clear_background(pr.WHITE)
        self._render()

        if self.pause:
            pr.draw_rectangle(0, 0, self.width, self.height, (255, 255, 255, 200))

        if self.should_exit is True:
            font = FontManager().get_font("huge")
            font_size = 80
            font_spacing = 20
            text = "Are you sure?"
            text_len = pr.measure_text_ex(font, text, font_size, font_spacing)
            pr.draw_text_ex(
                font,
                "Are you sure?",
                pr.Vector2(
                    self.width // 2 - text_len.x // 2,
                    self.height // 2 - text_len.y // 2,
                ),
                font_size,
                font_spacing,
                pr.RED,
            )

    def update(self, dt: float):
        self._timer += 1 * dt

        if pr.is_key_pressed(rl.KEY_ESCAPE):
            self._timer = 0
            if self.should_exit:
                AudioManager().stop()
                SceneManager().exit()
                return

            AudioManager().stop()
            AudioManager().play("are_you_sure")
            self.should_exit = True
            self.pause = True
        if (
            pr.get_key_pressed()
            and self.should_exit is True
            and not pr.is_key_pressed(rl.KEY_ESCAPE)
        ):
            AudioManager().stop()
            AudioManager().play("i_didnt_think_so")
            self.should_exit_changed = True
            self.should_exit = False
            self._timer = 0

        if self._timer > 1.5 and self.should_exit_changed:
            self.should_exit = False
            self.pause = False
            self.should_exit_changed = False
            self._timer = 0

        if pr.is_key_pressed(rl.KEY_P):
            self.pause = not self.pause

        if self.pause:
            return

        self._update(dt)

    @property
    @abstractmethod
    def ESPER_WORLD(self) -> str:
        """"""

    @abstractmethod
    def _update(self, dt: float):
        """"""

    @abstractmethod
    def _render(self):
        """"""
