from abc import ABC, abstractmethod

import esper


class BaseSpawnerProcessor(ABC, esper.Processor):
    def __init__(self, spawn_interval: float):
        self._spawn_interval = spawn_interval
        self._timer = 0.0

    def process(self, dt: float) -> None:
        self._timer += 1 * dt
        if self._timer >= self._spawn_interval:
            self.spawn_entity_logic()
            self._timer = 0.0

    @abstractmethod
    def spawn_entity_logic(self) -> None:
        """ """
