import esper

from flappy_raqui.pyrayngine.animation.gif import GifAnimator


class UpdateGifAnimations(esper.Processor):
    def process(self, dt: float):
        for ent, (gif_animation,) in esper.get_components(GifAnimator):
            if not gif_animation.loop and gif_animation.has_finished:
                esper.delete_entity(ent)
            gif_animation.update(dt=dt)
