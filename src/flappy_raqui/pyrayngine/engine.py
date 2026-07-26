import pyray as pr

from flappy_raqui.pyrayngine.configuration import EngineConfig
from flappy_raqui.pyrayngine.resource_managers.audio_manager import AudioManager
from flappy_raqui.pyrayngine.resource_managers.dummy_manager import DummyResourceManager
from flappy_raqui.pyrayngine.resource_managers.font_manager import FontManager
from flappy_raqui.pyrayngine.resource_managers.texture_manager import (
    AnimatedTextureManager,
    TextureManager,
)
from flappy_raqui.pyrayngine.scenes.scene_manager import SceneManager


class PyRayNgine:
    """"""

    def __init__(self, config: EngineConfig | None = None):
        self.config = config
        self.textures_manager = DummyResourceManager()
        self.animimated_textures_manager = DummyResourceManager()
        self.font_manager = DummyResourceManager()
        self.audio_manager = DummyResourceManager()

        self._setup()
        pr.set_exit_key(-1)

    def _setup(self) -> None:
        if not self.config:
            self.config = EngineConfig()
        pr.init_window(
            self.config.window_width,
            self.config.window_height,
            self.config.window_title,
        )

    def run(self, scene_manager: SceneManager) -> None:
        """"""
        monitor = pr.get_current_monitor()
        monitor_width = pr.get_monitor_width(monitor)
        monitor_height = pr.get_monitor_height(monitor)
        window_width = self.config.window_width
        window_height = self.config.window_height

        if fps := self.config.target_fps:
            pr.set_target_fps(fps)

        if self.config.full_screen:
            window_width = monitor_width
            window_height = monitor_height
            pr.set_window_size(window_width, window_height)
            pr.toggle_fullscreen()
        if self.config.hide_mouse:
            pr.hide_cursor()
            pr.disable_cursor()

        render_texture = pr.load_render_texture(
            self.config.window_width, self.config.window_height
        )
        while not pr.window_should_close() and not scene_manager.should_exit:
            dt = pr.get_frame_time()

            self.audio_manager.update_music_stream()

            scene_manager.update(dt=dt)

            pr.begin_texture_mode(render_texture)
            scene_manager.render()
            pr.end_texture_mode()

            pr.begin_drawing()
            pr.draw_texture_pro(
                render_texture.texture,
                pr.Rectangle(
                    0, 0, render_texture.texture.width, -render_texture.texture.height
                ),
                pr.Rectangle(0, 0, window_width, window_height),
                pr.Vector2(0, 0),
                0,
                pr.WHITE,
            )
            pr.end_drawing()

        # Release Resources
        pr.unload_render_texture(render_texture)
        scene_manager.destroy()
        self.textures_manager.destroy()
        self.animimated_textures_manager.destroy()
        self.font_manager.destroy()
        self.audio_manager.destroy()
        pr.close_window()
