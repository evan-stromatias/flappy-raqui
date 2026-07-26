import pyray as pr


class GifAnimator:
    def __init__(
        self,
        texture: pr.Texture,
        image: pr.Image,
        frames: int,
        frame_time: float,
        current_frame: int = 0,
        counter_frame: float = 0.0,
        loop: bool = True,
        has_finished: bool = False,
    ):
        self.texture = texture
        self.image = image
        self.frames = frames
        self.delay_frame = frame_time
        self.current_frame = current_frame
        self.counter_frame = counter_frame
        self.loop = loop
        self.has_finished = has_finished

    @property
    def width(self) -> int:
        return self.texture.width

    @property
    def height(self) -> int:
        return self.texture.height

    def update(self, dt: float):
        self.counter_frame += 1 * dt
        if self.counter_frame >= self.delay_frame:
            self.current_frame += 1
            if self.current_frame >= self.frames:
                self.current_frame = 0
                self.has_finished = True

            next_frame_offset = (
                self.texture.width * self.texture.height * 4 * self.current_frame
            )
            pr.update_texture(self.texture, self.image.data + next_frame_offset)
            self.counter_frame = 0

    def draw(self, x: int, y: int, tint=pr.WHITE):
        """
        Draws the current frame of the animation.

        Args:
            x (int): X-coordinate for drawing.
            y (int): Y-coordinate for drawing.
            tint (Color): Tint color for the texture.
        """
        pr.draw_texture(self.texture, int(x), int(y), tint)
