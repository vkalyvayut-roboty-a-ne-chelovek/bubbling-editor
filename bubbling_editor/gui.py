import pathlib
import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

from bubbling_editor.bus import Bus
from bubbling_editor import helpers

from bubbling_editor.misc import AddBubblePayload


class TestabeGui:
    def __init__(self, bus: Bus):
        self.bus = bus
        self.bus.register('gui', self)

    def run(self):
        pass

    def enable_save_btn(self):
        pass

    def disable_save_btn(self):
        pass

    def enable_click_listener(self):
        pass

    def disable_click_listener(self):
        pass

    def load_image(self, path_to_image: pathlib.Path, bubbles: list) -> None:
        pass

    def add_bubble(self, bubble: AddBubblePayload) -> None:
        pass

class Gui(TestabeGui):
    def __init__(self, bus: Bus):
        self.bus = bus
        self.bus.register('gui', self)
        self.root: tkinter.Tk = None

        self.path_to_image: pathlib.Path = None
        self.original_image: Image = None
        self.resized_image: Image = None
        self.tk_image: ImageTk = None
        self.image_on_canvas = None
        self.bubbles: list = []

    def make_gui(self):
        self.root = tkinter.Tk()
        self.root.attributes('-zoomed', True)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=95)

        self.instruments_panel = tkinter.Frame(self.root, background='red')
        self.instruments_panel.grid(row=0, column=0, sticky='ew')

        self.canvas_panel = tkinter.Frame(self.root, background='green')
        self.canvas_panel.grid(row=1, column=0, sticky='nesw')
        self.canvas_panel.columnconfigure(0, weight=1)
        self.canvas_panel.rowconfigure(0, weight=1)

        self.canvas = tkinter.Canvas(self.canvas_panel, background='blue')
        self.canvas.grid(row=0, column=0, sticky='nesw')

        self.new_image_btn = tkinter.Button(
            self.instruments_panel, text='NEW',
            command=self._show_new_image_popup)
        self.new_image_btn.grid(row=0, column=0, sticky='n')
        self.root.bind('<Control-n>', lambda _: self._show_new_image_popup())

        self.open_image_btn = tkinter.Button(
            self.instruments_panel, text='OPEN',
            command=self._show_open_image_popup)
        self.open_image_btn.grid(row=0, column=1, sticky='n')
        self.root.bind('<Control-o>', lambda _: self._show_open_image_popup())

        self.save_image_btn = tkinter.Button(
            self.instruments_panel, text='SAVE',
            command=self._show_save_image_popup)
        self.save_image_btn.grid(row=0, column=2, sticky='n')
        self.root.bind('<Control-s>', lambda _: self._show_save_image_popup())

        self.root.bind('<Configure>', lambda _: self._redraw_image_with_bubbles())

    def run(self) -> None:
        self.make_gui()
        self.disable_save_btn()
        self.root.mainloop()

    def enable_save_btn(self):
        if hasattr(self, 'save_image_btn'):
            self.save_image_btn['state'] = 'normal'

    def disable_save_btn(self):
        if hasattr(self, 'save_image_btn'):
            self.save_image_btn['state'] = 'disabled'

    def enable_click_listener(self):
        self.canvas.bind('<Button-1>', lambda e: self._on_canvas_click(e.x, e.y))
        self.canvas.bind('<Motion>', lambda e: self._draw_temp_bubble(e.x, e.y))

    def disable_click_listener(self):
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Motion>')

    def _draw_temp_bubble(self, x, y) -> None:
        for bubble in self.canvas.gettags('#temp_bubble'):
            self.canvas.delete(bubble)

        c_w, c_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        i_w, i_h = self.resized_image.width, self.resized_image.height
        x, y = helpers.clamp_coords_in_image_area(i_w, i_h, c_w, c_h, x, y)
        self.canvas.create_oval(x - 50, y - 50, x + 50, y + 50, fill='red', tags=('#temp_bubble',))

    def _on_canvas_click(self, x, y) -> None:
        c_w, c_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        i_w, i_h = self.resized_image.width, self.resized_image.height
        rel_x, rel_y = helpers.from_canvas_to_image_coords(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h, x=x, y=y)

        self.bus.statechart.launch_add_bubble_event(AddBubblePayload(pos=[rel_x, rel_y], radius=50))

    def add_bubble(self, bubble: AddBubblePayload) -> None:
        self.bubbles.append(bubble)
        self._redraw_image_with_bubbles()

    def load_image(self, path_to_image: pathlib.Path, bubbles: list) -> None:
        self.original_image = Image.open(path_to_image)
        self.path_to_image = path_to_image
        self.bubbles = bubbles

        self._redraw_image_with_bubbles()

    def _redraw_image_with_bubbles(self):
        self._clear_image()

        if self.path_to_image:
            self._resize_raw_image()
            self._apply_bubbles()
            self._draw_image_on_canvas()

    def _clear_image(self):
        self.tk_image = None
        for canvas_figure in self.canvas.find_withtag('#image'):
            self.canvas.delete(canvas_figure)

    def _resize_raw_image(self):
        self.resized_image = Image.open(self.path_to_image).convert(mode='RGBA')
        new_sizes = helpers.get_size_to_resize(
            i_w=self.resized_image.width, i_h=self.resized_image.height,
            c_w=self.canvas.winfo_width(), c_h=self.canvas.winfo_height()
        )
        self.resized_image = self.resized_image.resize(new_sizes, resample=Image.Resampling.NEAREST)

    def _apply_bubbles(self):
        draw = ImageDraw.Draw(self.resized_image, mode='RGBA')

        i_w, i_h = self.resized_image.width, self.resized_image.height

        for bubble in self.bubbles:
            x, y = bubble.pos[0] * i_w, bubble.pos[1] * i_h
            radius = bubble.radius
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(255, 0, 0))

    def _draw_image_on_canvas(self):
        self.tk_image = ImageTk.PhotoImage(image=self.resized_image)
        self.canvas.create_image(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            image=self.tk_image,
            tags=('#image',)
        )

    def _show_new_image_popup(self):
        path_to_image = filedialog.askopenfilename()
        if path_to_image:
            self.bus.statechart.launch_new_image_event(path_to_image)

    def _show_open_image_popup(self):
        path_to_image = filedialog.askopenfilename()
        if path_to_image:
            self.bus.statechart.launch_load_image_event(path_to_image)

    def _show_save_image_popup(self):
        path_to_image = filedialog.asksaveasfilename()
        if path_to_image:
            self.bus.statechart.launch_save_image_event(path_to_image)
