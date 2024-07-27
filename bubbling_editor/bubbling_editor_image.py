import pathlib
from PIL import Image, ImageTk, ImageDraw

import bubbling_editor.helpers as helpers
from bubbling_editor.misc import AddBubblePayload


class BubblingEditorImage:
    def __init__(self, canvas, path_to_image: pathlib.Path, bubbles: list[AddBubblePayload]):
        self.canvas = canvas

        self.path_to_image: pathlib.Path = path_to_image
        self.bubbles = bubbles

        self.original_image: Image = None
        self.resized_image: Image = None
        self.tk_image: ImageTk = None
        self.image_on_canvas = None
        self.image_scale: float = 0
        self.image_forced_scale: float = None

    def redraw_image(self) -> None:
        if self.path_to_image:
            self._clear_image()
            self._load_raw_image()
            self._apply_bubbles()
            self._resize_raw_image()
            self._draw_image_on_canvas()

    def set_forced_scale(self, forced_scale: float = None) -> None:
        self.image_forced_scale = forced_scale
        self.redraw_image()

    def _clear_image(self):
        self.tk_image = None
        for canvas_figure in self.canvas.find_withtag('#image'):
            self.canvas.delete(canvas_figure)

    def _load_raw_image(self):
        self.original_image = Image.open(self.path_to_image).convert(mode='RGBA')

    def _apply_bubbles(self):
        mask = Image.new(mode='RGBA', size=(self.original_image.width, self.original_image.height), color=(0, 0, 0))
        draw = ImageDraw.Draw(mask, mode='RGBA')

        c_w, c_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        i_w, i_h = self.original_image.width, self.original_image.height

        new_sizes = helpers.get_size_to_fit(
            i_w=i_w, i_h=i_h,
            c_w=c_w, c_h=c_h
        )

        for bubble in self.bubbles:
            x, y = bubble.pos[0] * i_w, bubble.pos[1] * i_h
            rel_radius = bubble.radius
            abs_radius = rel_radius
            draw.ellipse((x - abs_radius, y - abs_radius, x + abs_radius, y + abs_radius), fill=(255, 0, 0))

        # TODO костыли-костылики 🤦
        # переписать, чтобы использовался расчет на основе радиуса и координат, а не обход всего массива
        mask_data = mask.getdata()
        resized_data = list(self.original_image.getdata())
        for idx, data in enumerate(mask_data):
            if data[0] == 0:
                resized_data[idx] = (
                    resized_data[idx][0],
                    resized_data[idx][1],
                    resized_data[idx][2],
                    125)
        self.original_image.putdata(resized_data)

    def _resize_raw_image(self):
        c_w, c_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        i_w, i_h = self.original_image.width, self.original_image.height

        x, y, scale = i_w, i_h, 1
        if self.image_forced_scale is None:
            x, y, scale = helpers.get_size_to_fit(
                i_w=i_w, i_h=i_h,
                c_w=c_w, c_h=c_h
            )
        else:
            x, y = int(i_w * self.image_forced_scale), int(y * self.image_forced_scale)
            scale = self.image_forced_scale

        self.image_scale = scale
        self.resized_image = self.original_image.resize((x, y), resample=Image.Resampling.NEAREST)

    def _draw_image_on_canvas(self):
        self.tk_image = ImageTk.PhotoImage(image=self.resized_image)
        self.canvas.create_image(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            image=self.tk_image,
            tags=('#image',)
        )

    def get_bubbles_coords_on_image(self, c_x, c_y, radius) -> list[float, float, float]:

        i_w, i_h = self.resized_image.width, self.resized_image.height
        c_w, c_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        x, y = helpers.from_canvas_to_image_coords(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h, x=c_x, y=c_y)
        new_data = [x, y, radius * 1 / self.image_scale]

        return new_data

    def get_clamped_coords_on_image(self, x: int, y: int) -> list[int, int]:
        i_w, i_h = self.resized_image.width, self.resized_image.height
        c_w, c_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        x, y = helpers.clamp_coords_in_image_area(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h, x=x, y=y)

        return [x, y]

    def add_bubble(self, bubble: AddBubblePayload) -> None:
        self.bubbles.append(bubble)
        self.redraw_image()

    def update_bubbles(self, bubbles: list[AddBubblePayload]) -> None:
        self.bubbles = bubbles
        self.redraw_image()
