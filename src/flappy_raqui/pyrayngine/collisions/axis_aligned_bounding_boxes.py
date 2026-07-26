import math
import sys

import pyray as pr


def get_rotated_texture_aabb(
    center: pr.Vector2, width: float, height: float, rotation: float
) -> pr.Rectangle:
    """
    Calculates the Axis-Aligned Bounding Box (AABB) for a rotated rectangle
    using pyray.

    Args:
        center (pyray.Vector2): The center point of the rectangle.
        width (float): The unrotated width of the rectangle.
        height (float): The unrotated height of the rectangle.
        rotation (float): The rotation angle in degrees.

    Returns:
        pyray.Rectangle: The calculated AABB.
    """
    # pyray provides DEG2RAD as pyray.DEG2RAD
    rotation_radians = math.radians(rotation)
    half_extents = pr.Vector2(width / 2.0, height / 2.0)

    # Corners relative to the rectangle's center, before rotation
    # pyray.Vector2 can be created directly
    corners = [
        pr.Vector2(-half_extents.x, -half_extents.y),  # Top-left
        pr.Vector2(half_extents.x, -half_extents.y),  # Top-right
        pr.Vector2(half_extents.x, half_extents.y),  # Bottom-right
        pr.Vector2(-half_extents.x, half_extents.y),  # Bottom-left
    ]

    min_x = sys.float_info.max
    min_y = sys.float_info.max
    max_x = sys.float_info.min
    max_y = sys.float_info.min

    for corner in corners:
        # pyray.Vector2Rotate is available in pyray
        # It rotates around (0,0), which is exactly what we need since 'corner' is relative to center
        rotated_corner = pr.vector2_rotate(corner, rotation_radians)
        # Translate the rotated corner to world space
        rotated_corner = pr.vector2_add(rotated_corner, center)

        if rotated_corner.x < min_x:
            min_x = rotated_corner.x
        if rotated_corner.x > max_x:
            max_x = rotated_corner.x
        if rotated_corner.y < min_y:
            min_y = rotated_corner.y
        if rotated_corner.y > max_y:
            max_y = rotated_corner.y

    # pyray.Rectangle can be created directly
    return pr.Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)
