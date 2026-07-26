"""Processors that remove entities"""

from flappy_raqui.ecs.systems.lifetimes.kill_based_on_timeout import (
    KillBasedOnTimeoutProcessor,
)
from flappy_raqui.ecs.systems.lifetimes.kill_dead import KillDeadProcessor
from flappy_raqui.ecs.systems.lifetimes.kill_out_of_screen import (
    KillOutOfScreenProcessor,
)

__all__ = [
    "KillOutOfScreenProcessor",
    "KillDeadProcessor",
    "KillBasedOnTimeoutProcessor",
]
