from dataclasses import dataclass
from pathlib import Path
from typing import Union

import pyray as pr

from flappy_raqui.pyrayngine.helpers.singleton import SingletonMeta

from .common import check_if_file_exists


@dataclass
class TextureData:
    texture: pr.Texture
    width: int
    height: int


class TextureManager(metaclass=SingletonMeta):
    def __init__(self):
        self._textures = {}

    def add_texture(self, name: str, file: Path, filter: int | None = None) -> None:
        check_if_file_exists(file)

        texture = pr.load_texture(str(file))
        if filter is not None:
            pr.set_texture_filter(texture.texture, filter)
        self._textures[name] = texture

    def get_texture(self, name: str) -> Union[pr.Texture, pr.Texture2D]:
        return self._textures[name]

    def get_texture_data(self, name: str) -> TextureData:
        return TextureData(
            texture=self._textures[name],
            width=self._textures[name].width,
            height=self._textures[name].height,
        )

    def destroy(self) -> None:
        for _, texture in self._textures.items():
            pr.unload_texture(texture)


@dataclass
class AnimatedTextureData:
    texture: pr.Texture
    image: pr.Image
    width: int
    height: int
    frames: int


class AnimatedTextureManager(metaclass=SingletonMeta):
    def __init__(self):
        self._textures = {}
        self._images = {}
        self._frames = {}

    def add_texture(self, name: str, file: Path, filter: int | None = None) -> None:
        check_if_file_exists(file)
        frames = pr.ffi.new("int *", 1)
        image_anim = pr.load_image_anim(str(file), frames)
        texture = pr.load_texture_from_image(image_anim)
        if filter is not None:
            pr.set_texture_filter(texture.texture, filter)
        self._textures[name] = texture
        self._images[name] = image_anim
        self._frames[name] = frames

    def get_animated_texture_data(self, name: str) -> AnimatedTextureData:
        texture = self._textures[name]
        return AnimatedTextureData(
            texture=texture,
            width=texture.width,
            height=texture.height,
            image=self._images[name],
            frames=self._frames[name][0],
        )

    def destroy(self) -> None:
        for _, texture in self._textures.items():
            pr.unload_texture(texture)
        for _, image in self._images.items():
            pr.unload_image(image)
