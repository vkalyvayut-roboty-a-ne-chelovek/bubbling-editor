import math
import pathlib
import json

from PIL import Image, ImageDraw, ImageOps
from bubbling_editor.misc import AddBubblePayload, Kind

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


def from_image_to_canvas_coords(i_w, i_h, c_w, c_h, x, y) -> tuple[int]:
    center_x, center_y = c_w / 2.0, c_h / 2.0

    min_x = center_x - i_w / 2
    min_y = center_y - i_h / 2

    abs_x = min_x + (x * i_w)
    abs_y = min_y + (y * i_h)

    return abs_x, abs_y


def get_size_to_fit(i_w: int, i_h: int, c_w: int, c_h: int) -> list[int | float]:
    result = [1, 1]
    scale = 1

    if i_w == i_h:
        min_side = min(c_w, c_h)
        scale = min_side / i_w
    elif i_w / i_h > 1:
        min_side = min(c_w, c_h)
        scale = min_side / i_w
    else:
        min_side = min(c_w, c_h)
        scale = min_side / i_h

    result = [i_w * scale, i_h * scale]

    return [int(math.floor(result[0])), int(math.floor(result[1])), scale]


def apply_bubbles(image: Image,
                  bubbles: list[AddBubblePayload],
                  image_scale: float = 1.0,
                  no_alpha: bool = False) -> Image:
    """
    накладываю одно изображение на другое с использованием маски
    перед этим делаю накладываемое изображение полупрозрачным,
    а маску, с нарисованными на ней кругами, инвертирую
    """

    image1: Image = image.copy()  # подложка
    image2: Image = None  # изображение, накладываемое поверх

    if no_alpha:
        image2: Image = Image.new(mode='RGBA', size=(image1.width, image1.height), color=(255, 0, 0))
        image2.putalpha(255)
    else:
        image2: Image = image.copy()
        image2.putalpha(127)

    mask = Image.new(mode='L', size=(image.width, image.height), color=0)
    mask_draw = ImageDraw.Draw(mask)

    for bubble in bubbles:
        x, y = bubble.pos[0] * image.width, bubble.pos[1] * image.height
        rel_radius = bubble.radius
        abs_radius = rel_radius * image_scale
        fill = 255
        if bubble.kind == Kind.COUNTER:
            fill = 0
        mask_draw.ellipse((x - abs_radius, y - abs_radius, x + abs_radius, y + abs_radius), fill=fill)

    mask = ImageOps.invert(mask)

    return Image.composite(image2, image1, mask)


def read_project(path_to_project: pathlib.Path) -> dict:
    result = {
        'path_to_image': None,
        'bubbles': None
    }

    with open(path_to_project, mode='r', encoding='utf-8') as project_handle:
        data = json.load(project_handle)
        path_to_image = data['path_to_image']
        bubbles = [AddBubblePayload(pos=bubble[0], radius=bubble[1], kind=bubble[2]) for bubble in data['bubbles']]

        result['path_to_image'] = path_to_image
        result['bubbles'] = bubbles

    return result


def save_project(path_to_image: pathlib.Path, bubbles: list[AddBubblePayload], path_to_project: pathlib.Path) -> None:
    data = {
        'version': 0,
        'path_to_image': str(pathlib.Path(path_to_image).absolute()),
        'bubbles': bubbles
    }
    with open(path_to_project, mode='w', encoding='utf-8') as project_handle:
        project_handle.write(json.dumps(data))


def export_image(path_to_image: Image, bubbles: list[AddBubblePayload], path_to_exported_image: pathlib.Path) -> None:
    image = Image.open(path_to_image)
    image = apply_bubbles(image, bubbles=bubbles, no_alpha=True)
    image.save(path_to_exported_image)
