import random
from typing import Any

import esper
import pyray as pr
import raylib as rl

import flappy_raqui.ecs.components as Component
import flappy_raqui.ecs.spawners as entity_spawner
import flappy_raqui.ecs.systems as systems
import flappy_raqui.ecs.systems.entity_spawners as spawners
import flappy_raqui.ecs.systems.renderers as renderers
from flappy_raqui.pyrayngine.resource_managers.audio_manager import AudioManager
from flappy_raqui.pyrayngine.scenes.scene_manager import SceneManager
from flappy_raqui.scenes.base import BaseGameScene


def setup_spawn_processors(width: int, height: int) -> list[esper.Processor]:
    return [
        spawners.CloudSpawnerProcessor(5, width, height // 4),
        spawners.StarSpawnerProcessor(
            1.0, width, height // 2, dx=(-200, -100), rotation_speed=(-100, 100)
        ),
        spawners.BirdSpawnerProcessor(5.0, width, height // 5),
        spawners.LavaSpawnerProcessor(
            spawn_interval=5.0, x=width, dx=-100, anim_speed=0.01
        ),
    ]


def setup_update_processors() -> list[esper.Processor]:
    return [
        systems.CollisionResolutionProcessor(),
        systems.GravityProcessor(),
        systems.PositionProcessor(),
        systems.CheckCollisionProcessor(),
        systems.KillOutOfScreenProcessor(),
        systems.UpdateParallaxProcessor(),
        systems.UpdateGifAnimations(),
        systems.UpdateSpriteSheetAnimations(),
        systems.KillBasedOnTimeoutProcessor(),
        systems.UpdateRotationProcessor(),
    ]


def setup_render_processors() -> list[esper.Processor]:
    return [
        renderers.RenderParallaxProcessor(),
        renderers.RenderSpritesProcessor(),
        renderers.RenderScoreProcessor(),
    ]


class PlayScene(BaseGameScene):
    ESPER_WORLD: str = "play"

    def __init__(self, width: int, height: int):
        super().__init__(width=width, height=height)
        self._ecs_switch_world()

        self.player = entity_spawner.PlayerEntitySpawner().spawn_entity(
            x=self.width // 2 - (self.height // 2),
            y=self.height // 2 - self.height,
            gravity=200.0,  # TODO hard-coded value
            anti_gravity=(-120.0),  # TODO hard-coded value
        )
        entity_spawner.GroundLavaEntitySpawner().spawn_entity(x=0, y=self.height)
        entity_spawner.ParallaxGroundEntitySpawner().spawn_entity(
            x=0, y=self.height, z_order=10
        )
        entity_spawner.ParallaxBackgroundEntitySpawner().spawn_entity(
            x=0, y=0, z_order=0
        )

        self._update_processors = setup_update_processors()
        self._spawn_processors = setup_spawn_processors(
            width=self.width, height=self.height
        )
        _ = [
            esper.add_processor(p)
            for p in self._update_processors + self._spawn_processors
        ]

        self._render_processors = setup_render_processors()

    def _ecs_switch_world(self):
        esper.switch_world(self.ESPER_WORLD)

    def enter(self, params: Any | None = None):
        self._ecs_switch_world()

    def exit(self):
        audio_manager = AudioManager()
        audio_manager.stop_music_stream()

    def _update(self, dt: float):
        if pr.is_key_pressed(rl.KEY_BACKSPACE):
            scene_manager = SceneManager()
            scene_manager.change_to("ScoreScene")

        if pr.is_key_pressed(rl.KEY_SPACE):
            self._jump()
            esper.dispatch_event("Jump")

        if pr.is_key_pressed(rl.KEY_ENTER):
            feed_bird_sounds = ("feed_bird1", "feed_bird2")
            self._play_sound(random.choice(feed_bird_sounds))
            if not self.pause:
                box = esper.try_component(
                    self.player, Component.CollisionBox
                ) or esper.try_component(self.player, Component.ObbCollisionBox)
                pos = esper.try_component(self.player, Component.Position)
                if box and pos:
                    entity_spawner.PopCornEntitySpawner().spawn_entity(
                        x=pos.x + box.w, y=pos.y
                    )

        if pr.is_key_pressed(rl.KEY_D):
            self.debug = not self.debug
            for rp in self._render_processors:
                rp.debug = self.debug

        if not self.pause:
            esper.process(dt=dt)
            if not AudioManager().is_music_stream_playing():
                AudioManager().resume_music_stream()
        else:
            AudioManager().pause_music_stream()

    def _render(self):
        _ = [rp.process() for rp in self._render_processors]

    def _jump(self) -> None:
        velocity, anti_g, position = esper.try_components(
            self.player, Component.Velocity, Component.AntiGravity, Component.Position
        )
        if velocity and anti_g and position.y > 0:
            velocity.y = anti_g.value
            self._play_sound("jump")
