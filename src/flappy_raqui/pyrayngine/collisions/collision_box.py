from typing import Callable

import pyray as pr


def generate_collision_rectangle_from_image(image: pr.Image) -> pr.Rectangle:
    """
    Generates a collision rectangle based on the non-transparent pixels from a  raylib Image.
    """
    min_x = image.width
    max_x = 0
    min_y = image.height
    max_y = 0
    found_non_transparent = False
    for y in range(image.height):
        for x in range(image.width):
            pixel_color: pr.Color = pr.get_image_color(image, x, y)
            if pixel_color.a > 0:
                if not found_non_transparent:
                    min_x = x
                    max_x = x
                    min_y = y
                    max_y = y
                    found_non_transparent = True
                else:
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)

    if found_non_transparent:
        # Width and height are inclusive, so add 1
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        return pr.Rectangle(min_x, min_y, width, height)
    else:
        return pr.Rectangle(0, 0, 0, 0)


def generate_collision_rectangle_from_texture(
    texture: pr.Texture,
    region: pr.Rectangle,
    collision_rectangle_from_image_func: Callable[
        [pr.Image], pr.Rectangle
    ] = generate_collision_rectangle_from_image,
) -> pr.Rectangle:
    """
    Generates a collision rectangle based on the non-transparent pixels
    within a specific frame (rectangle) of a raylib Texture2D (spritesheet).

    Args:
        texture: The raylib Texture2D object (the entire spritesheet).
        region: A Rectangle specifying the region of interest (the current frame) within the texture.
            Its coordinates are relative to the texture's origin (0,0).

    Returns:
        A Rectangle representing the bounding box of non-transparent pixels
        within the specified frame, relative to the frame's top-left corner.
        Returns an empty rectangle if the frame is fully transparent or invalid.
    """
    if not pr.is_texture_valid(texture):
        return pr.Rectangle(0, 0, 0, 0)

    image = pr.load_image_from_texture(texture)
    image_from_rectangle = pr.image_from_image(image, region)
    pr.unload_image(image)
    collision_rect = collision_rectangle_from_image_func(image_from_rectangle)
    pr.unload_image(image_from_rectangle)
    return collision_rect
