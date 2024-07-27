
import pathlib
from PIL import Image, ImageTk, ImageDraw

class BubblingEditorImage:
    def __init__(self, canvas, path_to_image, bubbles):
        self.canvas = canvas
        self.path_to_image = path_to_image
        self.bubbles = bubbles

        self.path_to_image: pathlib.Path = None
        self.original_image: Image = None
        self.resized_image: Image = None
        self.tk_image: ImageTk = None
        self.image_on_canvas = None
        self.bubbles: list = []

    def get_bubbles_coords_on_image(self, c_x, c_y, radius) -> list[float, float, float]:
        return [0, 0, 0]

    def add_bubble(self, bubble) -> None:
        pass

    def _clear_image(self):
        self.tk_image = None
        for canvas_figure in self.canvas.find_withtag('#image'):
            self.canvas.delete(canvas_figure)

    def _load_raw_image(self):
        self.resized_image = Image.open(self.path_to_image).convert(mode='RGBA')

    def _resize_raw_image(self):
        c_w, c_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        i_w, i_h = self.resized_image.width, self.resized_image.height
        x, y = i_w, i_h
        if float(self.forced_scale_var.get()) == 0:
            x, y, scale = helpers.get_size_to_fit(
                i_w=i_w, i_h=i_h,
                c_w=c_w, c_h=c_h
            )
        else:
            x, y = int(i_w * float(self.forced_scale_var.get())), int(y * float(self.forced_scale_var.get()))

        self.resized_image = self.resized_image.resize((x, y), resample=Image.Resampling.NEAREST)

    def _apply_bubbles(self):
        mask = Image.new(mode='RGBA', size=(self.resized_image.width, self.resized_image.height), color=(0, 0, 0))
        draw = ImageDraw.Draw(mask, mode='RGBA')

        c_w, c_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        i_w, i_h = self.resized_image.width, self.resized_image.height

        new_sizes = helpers.get_size_to_fit(
            i_w=i_w, i_h=i_h,
            c_w=c_w, c_h=c_h
        )

        for bubble in self.bubbles:
            x, y = bubble.pos[0] * i_w, bubble.pos[1] * i_h
            rel_radius = bubble.radius
            abs_radius = helpers.from_image_to_canvas_bubble_radius(c_w=c_w, c_h=c_h, radius=rel_radius)
            draw.ellipse((x - abs_radius, y - abs_radius, x + abs_radius, y + abs_radius), fill=(255, 0, 0))

        # TODO костыли-костылики 🤦
        # переписать, чтобы использовался расчет на основе радиуса и координат, а не обход всего массива
        mask_data = mask.getdata()
        resized_data = list(self.resized_image.getdata())
        for idx, data in enumerate(mask_data):
            if data[0] == 0:
                resized_data[idx] = (
                    resized_data[idx][0],
                    resized_data[idx][1],
                    resized_data[idx][2],
                    125)
        self.resized_image.putdata(resized_data)

    def _draw_image_on_canvas(self):
        self.tk_image = ImageTk.PhotoImage(image=self.resized_image)
        self.canvas.create_image(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            image=self.tk_image,
            tags=('#image',)
        )

    def load_image(self, path_to_image: pathlib.Path, bubbles: list) -> None:
        self.original_image = Image.open(path_to_image)
        self.path_to_image = path_to_image
        self.bubbles = bubbles
        self.forced_scale_var.set(0)

        self.redraw_image()

    def redraw_image(self):
        self._clear_image()

        if self.path_to_image:
            self._load_raw_image()
            self._apply_bubbles()
            self._resize_raw_image()
            self._draw_image_on_canvas()

    def _on_canvas_click(self, x, y) -> None:
        # c_w, c_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        # i_w, i_h = self.resized_image.width, self.resized_image.height
        # rel_x, rel_y = helpers.from_canvas_to_image_coords(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h, x=x, y=y)
        #
        # abs_radius = int(self.bubble_radius_var.get())
        # rel_radius = helpers.from_canvas_to_image_bubble_radius(c_w=c_w, c_h=c_h, radius=abs_radius)

        rel_x, rel_y, rel_radius = self.image.get_bubbles_coords_on_image(x, y, self.bubble_radius_var.get())
        self.bus.statechart.launch_add_bubble_event(AddBubblePayload(pos=[rel_x, rel_y], radius=rel_radius))