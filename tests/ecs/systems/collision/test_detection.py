"""Unit tests for
:class:`flappy_raqui.ecs.systems.collision.detection.CheckCollisionProcessor`.

The processor scans the active ``esper`` world for entities carrying a
``CollisionBox``/``Position`` (or ``ObbCollisionBox``/``Position``) and tags every
overlapping pair -- in the same collision group -- with a reciprocal
``CollidedWith`` component. Each test runs in its own throwaway esper world so the
global entity registry can't leak between tests.
"""

import esper
import pyray as pr
import pytest

import flappy_raqui.ecs.components as Component
from flappy_raqui.ecs.systems.collision.detection import CheckCollisionProcessor

WORLD = "test_check_collision"


@pytest.fixture(autouse=True)
def esper_world():
    """Give each test a fresh, isolated esper world."""
    esper.switch_world("default")
    if WORLD in esper.list_worlds():
        esper.delete_world(WORLD)
    esper.switch_world(WORLD)
    yield
    esper.switch_world("default")  # can't delete the active world
    if WORLD in esper.list_worlds():
        esper.delete_world(WORLD)


def make_box(px, py, *, x=0, y=0, w=10, h=10, group=0) -> int:
    """Spawn an axis-aligned box entity at world position ``(px, py)``."""
    return esper.create_entity(
        Component.CollisionBox(x, y, w, h, collision_group=group),
        Component.Position(px, py),
    )


def make_obb(px, py, *, cx=5, cy=5, w=10, h=10, rotation=0.0, group=0) -> int:
    """Spawn an oriented-bounding-box entity at world position ``(px, py)``."""
    return esper.create_entity(
        Component.ObbCollisionBox(
            center=pr.Vector2(cx, cy),
            w=w,
            h=h,
            rotation=rotation,
            collision_group=group,
        ),
        Component.Position(px, py),
    )


def collided_pairs() -> set[tuple[int, int]]:
    """All (entity, other) links currently recorded as CollidedWith."""
    return {(ent, cw.entity) for ent, cw in esper.get_component(Component.CollidedWith)}


def run():
    CheckCollisionProcessor().process(0.0)


# --------------------------------------------------------------------------- #
# Overlap detection (axis-aligned boxes)
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "pos_a, pos_b",
    [
        ((0, 0), (0, 0)),  # identical
        ((0, 0), (5, 5)),  # partial overlap
        ((0, 0), (9, 0)),  # 1px overlap on the x edge
        ((0, 0), (0, 9)),  # 1px overlap on the y edge
        ((5, 5), (0, 0)),  # order does not matter
    ],
)
def test_overlapping_boxes_tag_each_other(pos_a, pos_b):
    a = make_box(*pos_a)
    b = make_box(*pos_b)
    run()
    assert collided_pairs() == {(a, b), (b, a)}


@pytest.mark.parametrize(
    "pos_a, pos_b",
    [
        ((0, 0), (500, 500)),  # far apart
        ((0, 0), (10, 0)),  # touching edge on x -> not a collision
        ((0, 0), (0, 10)),  # touching edge on y -> not a collision
        ((0, 0), (11, 0)),  # small gap on x
        ((0, 0), (0, 25)),  # gap on y
    ],
)
def test_non_overlapping_boxes_are_not_tagged(pos_a, pos_b):
    make_box(*pos_a)
    make_box(*pos_b)
    run()
    assert collided_pairs() == set()


# --------------------------------------------------------------------------- #
# Position offsets the collision rectangle
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "px, should_collide",
    [(0, True), (9, True), (10, False), (50, False)],
)
def test_position_offsets_the_box(px, should_collide):
    # Both boxes share identical local coords; only Position separates them.
    a = make_box(0, 0)
    b = make_box(px, 0)
    run()
    assert (collided_pairs() == {(a, b), (b, a)}) is should_collide


# --------------------------------------------------------------------------- #
# Collision groups
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("group", [0, 1, 7, -3])
def test_same_group_overlap_collides(group):
    a = make_box(0, 0, group=group)
    b = make_box(0, 0, group=group)
    run()
    assert collided_pairs() == {(a, b), (b, a)}


@pytest.mark.parametrize("group_a, group_b", [(0, 1), (1, 2), (0, -1)])
def test_different_groups_never_collide(group_a, group_b):
    # Fully overlapping but in different groups -> skipped.
    make_box(0, 0, group=group_a)
    make_box(0, 0, group=group_b)
    run()
    assert collided_pairs() == set()


# --------------------------------------------------------------------------- #
# Oriented bounding boxes
# --------------------------------------------------------------------------- #


def test_obb_overlapping_box_collides():
    a = make_obb(0, 0)
    b = make_box(0, 0)
    run()
    assert collided_pairs() == {(a, b), (b, a)}


def test_obb_far_from_box_does_not_collide():
    make_obb(0, 0)
    make_box(500, 500)
    run()
    assert collided_pairs() == set()


def test_two_obbs_overlapping_collide():
    a = make_obb(0, 0)
    b = make_obb(3, 3)
    run()
    assert collided_pairs() == {(a, b), (b, a)}


# --------------------------------------------------------------------------- #
# Multiple entities / edge cases
# --------------------------------------------------------------------------- #


def test_multiple_disjoint_pairs_all_detected():
    # Two separate overlapping pairs, far apart; every entity is in at most one
    # collision, so all four links are recorded.
    a = make_box(0, 0)
    b = make_box(3, 0)  # overlaps A
    c = make_box(100, 0)
    d = make_box(103, 0)  # overlaps C, far from A/B
    run()
    assert collided_pairs() == {(a, b), (b, a), (c, d), (d, c)}


def test_entity_in_multiple_collisions_keeps_only_the_last_link():
    # CollidedWith is a single component per entity, so an entity overlapping two
    # others in the same frame only retains the last-processed link (each
    # add_component overwrites the previous one). Here B overlaps both A and C.
    a = make_box(0, 0)
    b = make_box(5, 0)
    c = make_box(10, 0)  # overlaps B, only edge-touches A (no collision)
    run()
    links = {ent: cw.entity for ent, cw in esper.get_component(Component.CollidedWith)}
    assert links[a] == b  # A only collided with B
    assert links[c] == b  # C only collided with B
    assert links[b] == c  # B overlapped A and C but kept only the last (C)


@pytest.mark.parametrize("n_entities", [0, 1])
def test_fewer_than_two_entities_is_a_noop(n_entities):
    for _ in range(n_entities):
        make_box(0, 0)
    run()
    assert collided_pairs() == set()
