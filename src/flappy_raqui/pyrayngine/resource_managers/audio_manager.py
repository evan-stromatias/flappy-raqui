from pathlib import Path

import pyray as pr

from flappy_raqui.pyrayngine.helpers.singleton import SingletonMeta

from .common import check_if_file_exists


class AudioManager(metaclass=SingletonMeta):
    """Singleton class that manages audio resources."""

    def __init__(self) -> None:
        pr.init_audio_device()

        self._sounds = {}
        self._music = {}
        self._current_music_playing = None

    def add_audio(self, name: str, file: Path) -> None:
        check_if_file_exists(file)
        self._sounds[name] = pr.load_sound(str(file))

    def add_music(self, name: str, file: Path) -> None:
        check_if_file_exists(file)
        self._music[name] = pr.load_music_stream(str(file))

    def play(self, name: str) -> None:
        pr.play_sound(self._sounds[name])

    def stop(self) -> None:
        for _, sound in self._sounds.items():
            pr.stop_sound(sound)

    def play_music(self, name: str) -> None:
        self._current_music_playing = self._music[name]
        pr.play_music_stream(self._current_music_playing)

    def update_music_stream(self) -> None:
        if self._current_music_playing is not None:
            pr.update_music_stream(self._current_music_playing)

    def stop_music_stream(self) -> None:
        if self._current_music_playing is not None:
            pr.stop_music_stream(self._current_music_playing)

    def pause_music_stream(self) -> None:
        if self._current_music_playing is not None:
            pr.pause_music_stream(self._current_music_playing)

    def resume_music_stream(self) -> None:
        if self._current_music_playing is not None:
            pr.resume_music_stream(self._current_music_playing)

    def is_music_stream_playing(self) -> bool:
        if self._current_music_playing is not None:
            return pr.is_music_stream_playing(self._current_music_playing)

    def destroy(self) -> None:
        self.stop_music_stream()

        for _, sound in self._sounds.items():
            pr.unload_sound(sound)

        for _, music_stream in self._music.items():
            pr.unload_music_stream(music_stream)

        pr.close_audio_device()
