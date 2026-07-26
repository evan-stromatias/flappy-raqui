import pytest

from flappy_raqui.pyrayngine.helpers.singleton import SingletonMeta
from flappy_raqui.pyrayngine.scenes.base import SceneBase
from flappy_raqui.pyrayngine.scenes.scene_manager import SceneManager


class DummyScene(SceneBase):
    """A scene that records its lifecycle calls instead of doing anything."""

    def __init__(self, label: str, log: list | None = None):
        self.label = label
        self.log = log if log is not None else []
        self.enter_params: list = []
        self.exit_count = 0
        self.update_dts: list[float] = []
        self.render_count = 0
        self.destroy_count = 0

    def enter(self, params=None):
        self.enter_params.append(params)
        self.log.append((self.label, "enter"))

    def exit(self):
        self.exit_count += 1
        self.log.append((self.label, "exit"))

    def update(self, dt: float):
        self.update_dts.append(dt)
        self.log.append((self.label, "update"))

    def render(self):
        self.render_count += 1
        self.log.append((self.label, "render"))

    def destroy(self):
        self.destroy_count += 1
        self.log.append((self.label, "destroy"))


@pytest.fixture(autouse=True)
def _reset_singleton():
    """Drop the cached singleton so each test gets a brand-new SceneManager."""
    SingletonMeta._instances.pop(SceneManager, None)
    yield
    SingletonMeta._instances.pop(SceneManager, None)


@pytest.fixture
def log() -> list:
    """Shared, ordered record of lifecycle calls across all scenes."""
    return []


@pytest.fixture
def scenes(log) -> dict[str, DummyScene]:
    return {name: DummyScene(name, log) for name in ("A", "B", "C")}


@pytest.fixture
def manager(scenes) -> SceneManager:
    """A manager with scenes A, B, C registered and A as the current scene."""
    m = SceneManager()
    for name, scene in scenes.items():
        m.add_scene(name, scene)
    m.set_current_scene("A")
    return m


def test_scene_manager_is_a_singleton():
    first = SceneManager()
    second = SceneManager()
    assert first is second


def test_singleton_shares_state():
    SceneManager().add_scene("X", DummyScene("X"))
    assert "X" in SceneManager()._scenes


@pytest.mark.parametrize("name", ["A", "B", "C"])
def test_add_scene_stores_the_same_instance(manager, scenes, name):
    assert manager._scenes[name] is scenes[name]


@pytest.mark.parametrize("name", ["A", "B", "C"])
def test_set_current_scene_switches_without_lifecycle_calls(manager, scenes, log, name):
    log.clear()
    manager.set_current_scene(name)
    assert manager._current_scene is scenes[name]
    assert log == []  # no enter/exit is triggered by set_current_scene


@pytest.mark.parametrize("unknown", ["", "Z", "a", "does-not-exist"])
def test_set_current_scene_unknown_raises_key_error(manager, unknown):
    with pytest.raises(KeyError):
        manager.set_current_scene(unknown)


@pytest.mark.parametrize("target", ["B", "C"])
def test_change_to_exits_current_then_enters_target_in_order(
    manager, scenes, log, target
):
    log.clear()
    manager.change_to(target)
    assert manager._current_scene is scenes[target]
    assert log == [("A", "exit"), (target, "enter")]


@pytest.mark.parametrize("params", [None, 42, "hello", {"k": "v"}, [1, 2, 3]])
def test_change_to_forwards_params_to_enter(manager, scenes, params):
    manager.change_to("B", params)
    assert scenes["B"].enter_params == [params]


@pytest.mark.parametrize("unknown", ["Z", "", "b"])
def test_change_to_unknown_raises_key_error(manager, unknown):
    with pytest.raises(KeyError):
        manager.change_to(unknown)


def test_change_to_unknown_keeps_current_but_still_exits_it(manager, scenes, log):
    # Documents current behaviour: exit() runs before the failing lookup, so the
    # old scene is exited yet remains current when the KeyError is raised.
    log.clear()
    with pytest.raises(KeyError):
        manager.change_to("Z")
    assert manager._current_scene is scenes["A"]
    assert log == [("A", "exit")]


@pytest.mark.parametrize("dt", [0.0, 0.016, 1.5, 100.0])
def test_update_delegates_only_to_current_scene(manager, scenes, dt):
    manager.update(dt)
    assert scenes["A"].update_dts == [dt]
    assert scenes["B"].update_dts == []
    assert scenes["C"].update_dts == []


def test_render_delegates_only_to_current_scene(manager, scenes):
    manager.render()
    assert scenes["A"].render_count == 1
    assert scenes["B"].render_count == 0
    assert scenes["C"].render_count == 0


@pytest.mark.parametrize("params", [None, 7, "x", {"a": 1}])
def test_load_current_scene_enters_current_with_params(manager, scenes, params):
    manager.load_current_scene(params)
    assert scenes["A"].enter_params == [params]


@pytest.mark.parametrize(
    "sequence, expected_enters, expected_exits",
    [
        (["B"], {"A": 0, "B": 1, "C": 0}, {"A": 1, "B": 0, "C": 0}),
        (["B", "A"], {"A": 1, "B": 1, "C": 0}, {"A": 1, "B": 1, "C": 0}),
        (["B", "C", "A"], {"A": 1, "B": 1, "C": 1}, {"A": 1, "B": 1, "C": 1}),
        (["B", "A", "B", "A"], {"A": 2, "B": 2, "C": 0}, {"A": 2, "B": 2, "C": 0}),
    ],
)
def test_transition_sequence_preserves_instances_and_counts(
    manager, scenes, sequence, expected_enters, expected_exits
):
    original = dict(scenes)  # capture identities before transitioning
    for target in sequence:
        manager.change_to(target)

    assert manager._current_scene is scenes[sequence[-1]]
    for name, scene in scenes.items():
        # the manager keeps the same objects around (nothing is recreated)
        assert manager._scenes[name] is original[name]
        assert len(scene.enter_params) == expected_enters[name]
        assert scene.exit_count == expected_exits[name]


def test_scene_state_persists_across_transitions(manager):
    manager._current_scene.custom = "hello"  # current scene is A
    manager.change_to("B")
    manager.change_to("A")
    assert manager._current_scene.custom == "hello"


def test_exit_sets_should_exit_flag(manager):
    assert manager.should_exit is False
    manager.exit()
    assert manager.should_exit is True


def test_destroy_calls_destroy_on_every_registered_scene(manager, scenes):
    manager.destroy()
    for scene in scenes.values():
        assert scene.destroy_count == 1
