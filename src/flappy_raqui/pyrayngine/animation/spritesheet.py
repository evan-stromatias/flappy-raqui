from typing import TypedDict

import pyray as rl

from flappy_raqui.pyrayngine.collisions.collision_box import (
    generate_collision_rectangle_from_texture,
)

Row = int
Column = int
AnimationName = str


class AnimationFrames(TypedDict):
    frames: list[tuple[Row, Column]]
    frame_times: float | None


class SpritesheetAnimator:
    def __init__(
        self,
        texture: rl.Texture,
        rows: int,
        cols: int,
        default_frame_time: float = 0.1,
        animations: dict[AnimationName, AnimationFrames] | None = None,
        collision_boxes_map: dict[str, rl.Rectangle] | None = None,
    ):
        """
        Initializes the SpritesheetAnimator.

        Args:
            texture: A raylib Texture object.
            rows (int): Total number of rows in the spritesheet.
            cols (int): Total number of columns in the spritesheet.
            frame_time (float): Default time in seconds each frame is displayed.
            animations (dict, optional): A dictionary defining animations.
                                         Key: Animation name (str)
                                         Value: dict with 'frames' (list of (row_idx, col_idx) tuples)
                                         Example: {
                                             "walk": {"frames": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1)]}
                                         }
            collision_boxes_map: If provided it will be used to return the collision box for the current frame. If
                not provided then the collision box will be generated from the current frame width and height.
        """
        self.texture = texture
        self.rows = rows
        self.cols = cols
        self.default_frame_time = default_frame_time

        self.frame_width = self.texture.width / self.cols
        self.frame_height = self.texture.height / self.rows

        self.animations = animations if animations is not None else {}
        self.current_animation_name = None
        self.current_animation_data = None
        self.current_animation_looping = True
        self.current_animation_played_once = False

        self.current_frame_index_in_sequence = (
            0  # Index within the 'frames' list of the current animation
        )
        self.timer = 0.0
        self.current_frame_display_time = self.default_frame_time
        self.collision_boxes_map = collision_boxes_map

        # If animations are provided, set the first one as current by default
        if self.animations:
            first_animation_name = next(iter(self.animations))
            self.play_animation(first_animation_name)

    def get_collision_box(self) -> rl.Rectangle:
        if self.collision_boxes_map:
            return self.collision_boxes_map[self.current_animation_name][
                self.current_frame_index_in_sequence
            ]
        else:
            return rl.Rectangle(0, 0, self.width, self.height)

    @property
    def width(self) -> int:
        return int(self.frame_width)

    @property
    def height(self) -> int:
        return int(self.frame_height)

    def play_animation(self, anim_name):
        """
        Starts playing a specified animation.

        Args:
            anim_name (str): The name of the animation to play.
        """
        if anim_name not in self.animations:
            return

        if self.current_animation_name == anim_name:
            return  # Already playing this animation

        self.current_animation_name = anim_name
        self.current_animation_data = self.animations[anim_name]
        self.current_frame_index_in_sequence = 0
        self.timer = 0.0  # Reset timer for the new animation

        # You could also store frame_time per animation in the dict if needed
        self.current_frame_display_time = self.animations[anim_name].get(
            "frame_time", self.default_frame_time
        )
        self.current_animation_looping = self.current_animation_data.get("loop", True)
        self.current_animation_played_once = False

    def update(self, dt):
        """
        Updates the animation based on the elapsed time.

        Args:
            dt (float): Delta time (time elapsed since last frame).
        """
        if not self.current_animation_data or not self.current_animation_data["frames"]:
            # Handle case where no animation is set or frames list is empty
            return

        self.timer += dt
        if self.timer >= self.current_frame_display_time:
            self.timer -= self.current_frame_display_time
            self.current_frame_index_in_sequence += 1
            if self.current_frame_index_in_sequence >= len(
                self.current_animation_data["frames"]
            ):
                self.current_frame_index_in_sequence = 0
                self.current_animation_played_once = True

        if (
            self.current_animation_played_once is True
            and self.current_animation_looping is False
        ):
            self.current_frame_index_in_sequence = (
                len(self.current_animation_data["frames"]) - 1
            )

    def get_source_rect(self) -> rl.Rectangle:
        current_frame_coords = self.current_animation_data["frames"][
            self.current_frame_index_in_sequence
        ]
        frame_row, frame_col = current_frame_coords

        return rl.Rectangle(
            frame_col * self.frame_width,
            frame_row * self.frame_height,
            self.frame_width,
            self.frame_height,
        )

    def draw(self, x: int, y: int, tint=rl.WHITE, scale: float = 1.0):
        """
        Draws the current frame of the animation.

        Args:
            x (int): X-coordinate for drawing.
            y (int): Y-coordinate for drawing.
            tint (Color): Tint color for the texture.
        """
        if not self.current_animation_data or not self.current_animation_data["frames"]:
            return  # No animation playing or no frames to draw

        x = int(x)
        y = int(y)

        source_rec = self.get_source_rect()
        dest_rec = rl.Rectangle(
            x, y, self.frame_width * scale, self.frame_height * scale
        )
        origin = rl.Vector2(0, 0)  # Drawing from top-left corner
        rotation = 0.0
        rl.draw_texture_pro(self.texture, source_rec, dest_rec, origin, rotation, tint)


def generate_collision_boxes_from_spritesheet(
    texture: rl.Texture, rows: int, cols: int, animations: AnimationFrames
) -> dict[str, rl.Rectangle]:
    frame_width = texture.width / cols
    frame_height = texture.height / rows

    collision_boxes = {}
    for animation, anim_data in animations.items():
        for i, frame in enumerate(anim_data.get("frames", [])):
            row, col = frame
            rect = rl.Rectangle(
                col * frame_width, row * frame_height, frame_width, frame_height
            )
            bbox = generate_collision_rectangle_from_texture(texture, rect)
            try:
                collision_boxes[animation].append(bbox)
            except KeyError:
                collision_boxes[animation] = []
                collision_boxes[animation].append(bbox)
    return collision_boxes
