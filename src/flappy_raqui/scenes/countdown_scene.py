from typing import Any

import esper
import pyray as pr

import flappy_raqui.ecs.components as Component
from flappy_raqui.ecs.systems import KillOutOfScreenProcessor, PositionProcessor
from flappy_raqui.ecs.systems.renderers import (
    RenderParallaxProcessor,
    RenderSpritesProcessor,
)
from flappy_raqui.pyrayngine.animation.gif import GifAnimator
from flappy_raqui.pyrayngine.resource_managers.audio_manager import AudioManager
from flappy_raqui.pyrayngine.resource_managers.font_manager import FontManager
from flappy_raqui.pyrayngine.resource_managers.texture_manager import (
    AnimatedTextureManager,
    TextureManager,
)
from flappy_raqui.pyrayngine.scenes.scene_manager import SceneManager
from flappy_raqui.scenes.base import BaseGameScene


class CountdownScene(BaseGameScene):
    ESPER_WORLD: str = "countdown"

    def __init__(self, width: int, height: int):
        super().__init__(width=width, height=height)
        self.scene_manager = SceneManager()
        self.bg_texture = TextureManager().get_texture_data("background")
        self.player_big_texture = TextureManager().get_texture_data("player")
        self.animated_big_star = AnimatedTextureManager().get_animated_texture_data(
            "star-big"
        )
        self.font = FontManager().get_font("font")
        self.font_size = 120  # TODO hard-coded values
        self._timer = 0.0
        self._count_to = 3  # TODO hard-coded values
        self._counter = self._count_to

        self._ecs_switch_world()
        self._create_entity_star(10, 10)  # TODO hard-coded values
        self._create_entity_star(
            self.width - 10 - self.animated_big_star.width, 10
        )  # TODO hard-coded values
        self._render_processors = self._setup_render_processors()
        esper.add_processor(KillOutOfScreenProcessor())
        esper.add_processor(PositionProcessor())

    def _setup_render_processors(self) -> list[esper.Processor]:
        return [
            RenderParallaxProcessor(),
            RenderSpritesProcessor(),
        ]

    def _ecs_switch_world(self):
        esper.switch_world(self.ESPER_WORLD)

    def _create_entity_star(self, x: int, y: int) -> None:
        star = GifAnimator(
            texture=self.animated_big_star.texture,
            image=self.animated_big_star.image,
            frames=self.animated_big_star.frames,
            frame_time=0.05,  # TODO hard-coded values
            current_frame=0,
        )

        esper.create_entity(star, Component.Position(x, y), Component.Star())

    def enter(self, params: Any | None = None):
        AudioManager().stop()
        self._counter = self._count_to
        self._ecs_switch_world()

    def exit(self):
        self._counter = self._count_to

    def _update(self, dt: float):

        if self._timer >= 1:
            self._counter -= 1
            self._timer = 0.0

            if self._counter >= 1:
                self._play_sound("score")
            if self._counter == 1:
                self._play_sound("bist_du_mein_freund")

        if self._counter <= 0:
            self.scene_manager.change_to("PlayScene")

        esper.process(dt=dt)

    def _render(self):
        pr.clear_background(pr.WHITE)
        pr.draw_texture_ex(
            self.bg_texture.texture, pr.Vector2(0, 0), 0.0, 2.0, pr.WHITE
        )

        pr.draw_texture(
            self.player_big_texture.texture,
            self.width // 2 - self.player_big_texture.width // 2,
            self.height // 2,
            pr.WHITE,
        )
        [rp.process() for rp in self._render_processors]

        text = f"{self._counter}"
        text_len = pr.measure_text(text, self.font_size)
        pr.draw_text_ex(
            self.font,
            text,
            pr.Vector2(self.width // 2 - text_len // 2, 570 // 4),
            self.font_size,
            1.0,
            pr.RED,
        )

    def destroy(self) -> None:
        esper.switch_world("None")
        esper.delete_world(self.ESPER_WORLD)
