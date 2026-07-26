from typing import Any

import esper
import pyray as pr
import raylib as rl

import flappy_raqui.ecs.spawners as entity_spawner
import flappy_raqui.ecs.systems as systems
from flappy_raqui.__version__ import __version__
from flappy_raqui.ecs.systems.entity_spawners import StarSpawnerProcessor
from flappy_raqui.ecs.systems.renderers import (
    RenderParallaxProcessor,
    RenderSpritesProcessor,
)
from flappy_raqui.pyrayngine.gui.frame import WindowFrame
from flappy_raqui.pyrayngine.gui.layouts.box_layout import BoxLayout
from flappy_raqui.pyrayngine.gui.widgets.button import Button
from flappy_raqui.pyrayngine.resource_managers.audio_manager import AudioManager
from flappy_raqui.pyrayngine.resource_managers.font_manager import FontManager
from flappy_raqui.pyrayngine.resource_managers.texture_manager import TextureManager
from flappy_raqui.pyrayngine.scenes.scene_manager import SceneManager
from flappy_raqui.scenes.base import BaseGameScene


class TitleScene(BaseGameScene):
    ESPER_WORLD: str = "title"

    def __init__(self, width: int, height: int):
        super().__init__(width=width, height=height)
        self._ecs_switch_world()
        self.scene_manager = SceneManager()

        self.bg_texture = TextureManager().get_texture_data("background")
        self.player_big_texture = TextureManager().get_texture_data("player")
        self.font = FontManager().get_font("font")
        self.font_size = 60  # TODO hard-coded values
        self.y_player_location_margin = 30
        self.y_menu_choices_margin = 20

        # Version stamp in the bottom-right corner. The position never changes,
        # so measure it once here instead of on every frame.
        self.version_text = f"v{__version__}"
        self.version_font_size = 24
        self.version_font_spacing = 1
        self.version_margin = 12
        version_size = pr.measure_text_ex(
            self.font,
            self.version_text,
            self.version_font_size,
            self.version_font_spacing,
        )
        self.version_position = pr.Vector2(
            self.width - version_size.x - self.version_margin,
            self.height - version_size.y - self.version_margin,
        )

        self._pigeon_left = entity_spawner.BirdEntitySpawner().spawn_entity(0, 0, dx=0)
        self._pigeon_right = entity_spawner.BirdEntitySpawner().spawn_entity(
            self.width - 120, 0, dx=0
        )

        self.frame = WindowFrame(
            x=0,
            y=self.height // 2 + self.y_menu_choices_margin,
            w=self.width,
            h=self.height - self.height // 2,
            win_w=self.width,
            win_h=self.height,
        )
        layout = BoxLayout(orientation="vertical")
        button1 = Button(
            "Play",
            font_size=self.font_size,
            font=self.font,
            on_pressed=lambda: self.scene_manager.change_to("CountdownScene"),
        )
        button2 = Button(
            "Options",
            font_size=self.font_size,
            font=self.font,
            text_color_selected=pr.DARKGRAY,
            text_color_unselected=pr.GRAY,
            on_pressed=lambda: AudioManager().play("hurt"),
        )
        button3 = Button(
            "Exit",
            font_size=self.font_size,
            font=self.font,
            on_pressed=lambda: self.scene_manager.exit(),
        )
        layout.add_widget(button1)
        layout.add_widget(button2)
        layout.add_widget(button3)
        self.frame.add_layout(layout)
        self.frame.setup()

        self._render_processors = self._setup_render_processors()

        esper.add_processor(
            StarSpawnerProcessor(
                0.1,
                self.width,
                self.height,
                dx=(-200, -100),
                rotation_speed=(-200, 200),
            )
        )
        esper.add_processor(systems.KillOutOfScreenProcessor())
        esper.add_processor(systems.PositionProcessor())
        esper.add_processor(systems.UpdateRotationProcessor())
        esper.add_processor(systems.UpdateGifAnimations())
        esper.add_processor(systems.UpdateSpriteSheetAnimations())

    def _setup_render_processors(self) -> list[esper.Processor]:
        return [
            RenderParallaxProcessor(),
            RenderSpritesProcessor(),
        ]

    def _ecs_switch_world(self):
        esper.switch_world(self.ESPER_WORLD)

    def enter(self, params: Any | None = None):
        AudioManager().play("intro_voice")
        self._ecs_switch_world()

    def exit(self):
        audio_manager = AudioManager()
        audio_manager.stop_music_stream()

    def _update(self, dt: float):
        self.frame.update(dt)

        if pr.is_key_pressed(rl.KEY_SPACE):
            audio_manager = AudioManager()
            audio_manager.play("score")

        if pr.is_key_pressed(rl.KEY_S):
            AudioManager().play("intro_voice")

        esper.process(dt=dt)

    def _render(self):
        pr.draw_texture_ex(
            self.bg_texture.texture, pr.Vector2(0, 0), 0.0, 2.0, pr.WHITE
        )
        [rp.process() for rp in self._render_processors]
        pr.draw_texture(
            self.player_big_texture.texture,
            self.width // 2 - self.player_big_texture.width // 2,
            self.height // 4 + self.y_player_location_margin,
            pr.WHITE,
        )

        texture = TextureManager().get_texture_data("title")
        pr.draw_texture(texture.texture, 180, 0, pr.WHITE)
        self.frame.render()

        pr.draw_text_ex(
            self.font,
            self.version_text,
            self.version_position,
            self.version_font_size,
            self.version_font_spacing,
            pr.DARKGRAY,
        )

    def destroy(self) -> None:
        esper.switch_world("None")
        esper.delete_world(self.ESPER_WORLD)
