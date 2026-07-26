from pathlib import Path

import pyray as pr
import raylib as rl

from flappy_raqui.pyrayngine.helpers.singleton import SingletonMeta

from .common import check_if_file_exists


class FontManager(metaclass=SingletonMeta):
    def __init__(self):
        self._fonts = {}

    def add_font(self, name: str, file: Path) -> None:
        check_if_file_exists(file)

        font = pr.load_font(str(file))
        pr.set_texture_filter(font.texture, rl.TEXTURE_FILTER_POINT)
        self._fonts[name] = font

    def get_font(self, name: str):
        return self._fonts[name]

    def destroy(self) -> None:
        for _, font in self._fonts.items():
            pr.unload_font(font)
