from abc import ABC, abstractmethod


class EntitySpawnerABC(ABC):
    @abstractmethod
    def spawn_entity(self, *args, **kwargs) -> int:
        """"""
