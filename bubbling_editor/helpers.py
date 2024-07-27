import math


def clamp(_min, _max, cur):
    return min(_max, max(_min, cur))


def clamp_coords_in_image_area(i_w, i_h, c_w, c_h, x, y) -> tuple[int, int]:
    center_x, center_y = c_w / 2.0, c_h / 2.0
    min_x = center_x - i_w / 2
    max_x = center_x + i_w / 2
    min_y = center_y - i_h / 2
    max_y = center_y + i_h / 2

    clamped_x = clamp(min_x, max_x, x)
    clamped_y = clamp(min_y, max_y, y)

    return clamped_x, clamped_y


def from_canvas_to_image_coords(i_w, i_h, c_w, c_h, x, y) -> tuple[int, int]:
    clamped_x, clamped_y = clamp_coords_in_image_area(i_w, i_h, c_w, c_h, x, y)

    center_x, center_y = c_w / 2.0, c_h / 2.0

    max_x = center_x + i_w / 2
    max_y = center_y + i_h / 2

    rel_x = 1.0 - (max_x - clamped_x) / i_w
    rel_y = 1.0 - (max_y - clamped_y) / i_h

    return rel_x, rel_y


def from_image_to_canvas_coords(i_w, i_h, c_w, c_h, x, y) -> tuple[int, int]:
    center_x, center_y = c_w / 2.0, c_h / 2.0

    min_x = center_x - i_w / 2
    min_y = center_y - i_h / 2

    abs_x = min_x + (x * i_w)
    abs_y = min_y + (y * i_h)

    return abs_x, abs_y


def get_size_to_fit(i_w: int, i_h: int, c_w: int, c_h: int) -> list[int, int, float]:
    result = [1, 1]
    scale = 1

    if i_w == i_h:
        min_side = min(c_w, c_h)
        scale = min_side / i_w
        result = [i_w * scale, i_h * scale]
    elif i_w / i_h > 1:
        scale = c_w / i_w
        result = [i_w * scale, i_h * scale]
    else:
        scale = c_h / i_h
        result = [i_w * scale, i_h * scale]

    return int(result[0]), int(result[1]), scale


def from_canvas_to_image_bubble_radius(c_w, c_h, radius) -> float:
    return (c_w / c_h) * radius


def from_image_to_canvas_bubble_radius(c_w, c_h, radius) -> float:
    return radius * 1.0 / (c_w / c_h)