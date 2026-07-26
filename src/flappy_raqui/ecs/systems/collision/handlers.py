"""Collision handlers.

Each takes the two colliding entities already ordered by role (see the rule
table in ``resolution``) and applies that interaction's effects.
"""

import random

import esper

import flappy_raqui.ecs.components as Component
import flappy_raqui.ecs.spawners as entity_spawner
from flappy_raqui.pyrayngine.resource_managers.audio_manager import AudioManager


def popcorn_bird_collision(popcorn_entity: int, bird_entity: int):
    AudioManager().play("bist_du_mein_freund")
    velocity, animation = esper.try_components(
        bird_entity, Component.Velocity, Component.SpriteAnimation
    )

    if esper.has_component(bird_entity, Component.Enemy):
        esper.remove_component(bird_entity, Component.Enemy)
    if esper.has_component(bird_entity, Component.CollisionBox):
        esper.remove_component(bird_entity, Component.CollisionBox)

        for entity, score in esper.get_component(Component.Score):
            score.value += 1
        if bread_velocity := esper.try_component(popcorn_entity, Component.Velocity):
            bread_velocity.x = 0

        velocity.y = -120.0
        animation.current_animation = "fly"

    if esper.entity_exists(popcorn_entity):
        esper.delete_entity(entity=popcorn_entity)


def player_bird_collision(player_entity: int, other_entity: int):
    BIRD_SOUNDS = ("bird1", "bird2", "bird3")
    animation, velocity = esper.try_components(
        other_entity, Component.SpriteAnimation, Component.Velocity
    )
    if not animation or not velocity:
        return

    animation.current_animation = "fall"
    velocity.x = 0
    velocity.y = -(-120.0) * 2
    if esper.has_component(other_entity, Component.Enemy):
        esper.remove_component(other_entity, Component.Enemy)
        AudioManager().play(random.choice(BIRD_SOUNDS))
    if esper.has_component(other_entity, Component.CollisionBox):
        esper.remove_component(other_entity, Component.CollisionBox)

    if player_velocity := esper.try_component(player_entity, Component.Velocity):
        norm_bounce = max(0.1, player_velocity.y / 570)
        jump_val = random.randint(int(100 * norm_bounce), int((570 / 3) * norm_bounce))
        jump_val = max(50, jump_val)
        if player_position := esper.try_component(player_entity, Component.Position):
            player_position.y += jump_val
            player_velocity.y = -player_velocity.y // 4
    if score := esper.try_component(player_entity, Component.Score):
        score.value -= 1 if score.value > 0 else 0.0


def player_star_collision(player_entity: int, other_entity: int):
    AudioManager().play("score")
    esper.delete_entity(entity=other_entity)
    if score := esper.try_component(player_entity, Component.Score):
        score.value += 1


def player_lava_collision(player_entity: int, other_entity: int):
    AudioManager().play("raq")
    AudioManager().play("explosion")

    box = esper.try_component(
        player_entity, Component.CollisionBox
    ) or esper.try_component(player_entity, Component.ObbCollisionBox)
    pos = esper.try_component(player_entity, Component.Position)
    entity_spawner.SmokeEntitySpawner().spawn_entity(
        x=pos.x + box.x, y=pos.y + box.y, dx=-100
    )

    obb_box = esper.try_component(player_entity, Component.ObbCollisionBox)
    pos = esper.try_component(player_entity, Component.Position)
    vel = esper.try_component(player_entity, Component.Velocity)
    score = esper.try_component(player_entity, Component.Score)

    norm_bounce = max(0.1, vel.y / 570)
    jump_val = random.randint(int(100 * norm_bounce), int((570 / 3) * norm_bounce))
    jump_val = max(50, jump_val)
    pos.y -= jump_val
    vel.y = -vel.y // 4
    score.value -= 1 if score.value > 0 else 0.0
