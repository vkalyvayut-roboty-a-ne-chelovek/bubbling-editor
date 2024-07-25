import pathlib
import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk

from bubbling_editor.bus import Bus
from bubbling_editor import helpers

class TestabeGui:
    def __init__(self, bus: Bus):
        self.bus = bus
        self.bus.register('gui', self)

    def run(self):
        pass

    def load_image(self, path_to_image: pathlib.Path, bubbles: list) -> None:
        pass

class Gui:
    def __init__(self, bus: Bus):
        self.bus = bus
        self.bus.register('gui', self)
        self.root: tkinter.Tk = None

        self.path_to_image: pathlib.Path = None
        self.raw_image: Image = None
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

        self.open_image_btn = tkinter.Button(
            self.instruments_panel, text='OPEN',
            command=self._show_open_image_popup)
        self.open_image_btn.grid(row=0, column=1, sticky='n')

        self.save_image_btn = tkinter.Button(
            self.instruments_panel, text='SAVE',
            command=self._show_save_image_popup,
            state='normal')
        self.save_image_btn.grid(row=0, column=2, sticky='n')

    def run(self) -> None:
        self.make_gui()
        self.root.mainloop()

    def add_bubble(self, bubble) -> None:
        self.bubbles.append(bubble)

        self._redraw_image_with_bubbles()

    def load_image(self, path_to_image: pathlib.Path, bubbles: list) -> None:
        self.path_to_image = path_to_image
        self.bubbles = bubbles

        self._redraw_image_with_bubbles()

    def _redraw_image_with_bubbles(self):
        self._clear_image()

        self._resize_raw_image()
        self._apply_bubbles()
        self._draw_image_on_canvas()

    def _clear_image(self):
        self.tk_image = None
        for canvas_figure in self.canvas.find_withtag('#image'):
            self.canvas.delete(canvas_figure)

    def _resize_raw_image(self):
        self.raw_image = Image.open(self.path_to_image).convert(mode='RGBA')
        new_sizes = helpers.get_size_to_resize(
            i_w=self.raw_image.width, i_h=self.raw_image.height,
            c_w=self.canvas.winfo_width(), c_h=self.canvas.winfo_height()
        )
        self.raw_image = self.raw_image.resize(new_sizes, resample=Image.Resampling.NEAREST)

    def _apply_bubbles(self):
        pass

    def _draw_image_on_canvas(self):
        self.tk_image = ImageTk.PhotoImage(image=self.raw_image)
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


if __name__ == '__main__':
    b = Bus()
    g = Gui(bus=b)
    g.run()
