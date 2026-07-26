import esper

import flappy_raqui.ecs.components as Component
from flappy_raqui.ecs.systems.collision.handlers import (
    player_bird_collision,
    player_lava_collision,
    player_star_collision,
    popcorn_bird_collision,
)


class CollisionResolutionProcessor(esper.Processor):
    # (component_a, component_b, handler): for each collided pair, the first rule
    # whose two tag components are present (one on each entity) wins. The handler
    # is called with the entities already ordered - the one holding component_a
    # first, component_b second - so handlers never re-detect who is who.
    COLLISION_RULES = (
        (Component.Player, Component.Lava, player_lava_collision),
        (Component.Player, Component.Star, player_star_collision),
        (Component.Player, Component.Bird, player_bird_collision),
        (Component.Bread, Component.Bird, popcorn_bird_collision),
    )

    def process(self, dt: float) -> None:
        collided_pairs = set()
        for ent, (collided_with,) in esper.get_components(Component.CollidedWith):
            collided_pairs.add(tuple(sorted([ent, collided_with.entity])))

        for entity_a, entity_b in collided_pairs:
            if not esper.entity_exists(entity_a) or not esper.entity_exists(entity_b):
                continue

            for ent in (entity_a, entity_b):
                if esper.has_component(ent, Component.CollidedWith):
                    esper.remove_component(ent, Component.CollidedWith)

            for component_a, component_b, handler in self.COLLISION_RULES:
                ordered = self._match(entity_a, entity_b, component_a, component_b)
                if ordered is not None:
                    handler(*ordered)
                    break

    @staticmethod
    def _match(entity_a: int, entity_b: int, component_a, component_b):
        """Return (e_a, e_b) with e_a holding component_a and e_b component_b,
        regardless of the incoming order; or None if the pair doesn't match."""
        if esper.has_component(entity_a, component_a) and esper.has_component(
            entity_b, component_b
        ):
            return entity_a, entity_b
        if esper.has_component(entity_b, component_a) and esper.has_component(
            entity_a, component_b
        ):
            return entity_b, entity_a
        return None
