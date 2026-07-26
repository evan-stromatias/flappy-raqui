import esper

import flappy_raqui.ecs.components as Component


class UpdateRotationProcessor(esper.Processor):
    def process(self, dt: float):
        for ent, (rotation, obb_box) in esper.get_components(
            Component.RotationSpeed, Component.ObbCollisionBox
        ):
            _rotation_speed = rotation.speed * dt
            _rotation = rotation.rotation + _rotation_speed
            rotation.rotation = _rotation
            obb_box.rotation = _rotation
