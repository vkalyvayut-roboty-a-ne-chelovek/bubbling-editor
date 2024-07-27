import pathlib
import time
import tkinter
from tkinter import filedialog


from bubbling_editor.bus import Bus
from bubbling_editor import helpers

from bubbling_editor.misc import AddBubblePayload
from bubbling_editor.bubbling_editor_image import BubblingEditorImage


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

    def enable_bubble_radius_slider(self):
        pass

    def disable_bubble_radius_slider(self):
        pass

    def load_image(self, path_to_image: pathlib.Path, bubbles: list) -> None:
        pass

    def redraw_image(self) -> None:
        pass

    def add_bubble(self, bubble: AddBubblePayload) -> None:
        pass


class Gui(TestabeGui):
    def __init__(self, bus: Bus):
        super().__init__(bus=bus)
        self.root: tkinter.Tk = None

        self.image: BubblingEditorImage = None

        self.forced_scale_var: tkinter.DoubleVar = None

        self._temp_bubble_coords: list[int, int] = [0, 0]

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
        self.new_image_btn.grid(row=0, column=0, sticky='w')
        self.root.bind('<Control-n>', lambda _: self._show_new_image_popup())
        self.root.bind('<Control-n>', lambda _: self.bus.statechart.launch_new_image_event('/home/user28/projects/python/bubbling-editor/tests/assets/smiley.png'))


        self.open_image_btn = tkinter.Button(
            self.instruments_panel, text='OPEN',
            command=self._show_open_image_popup)
        self.open_image_btn.grid(row=0, column=1, sticky='w')
        self.root.bind('<Control-o>', lambda _: self._show_open_image_popup())

        self.save_image_btn = tkinter.Button(
            self.instruments_panel, text='SAVE',
            command=self._show_save_image_popup)
        self.save_image_btn.grid(row=0, column=2, sticky='w')
        self.root.bind('<Control-s>', lambda _: self._show_save_image_popup())

        self.bubble_radius_frame = tkinter.Frame(self.instruments_panel)
        self.bubble_radius_var = tkinter.IntVar(value=0)
        self.bubble_radius_label = tkinter.Label(self.bubble_radius_frame, textvariable=self.bubble_radius_var, width=5)
        self.bubble_radius_slider = tkinter.Scale(self.bubble_radius_frame,
                                                  from_=5, to=250, length=150, resolution=5, showvalue=False,
                                                  orient='horizontal', variable=self.bubble_radius_var,
                                                  state='disabled')

        self.bubble_radius_frame.grid(row=0, column=3, sticky='nesw')
        self.bubble_radius_frame.columnconfigure(0, weight=1)
        self.bubble_radius_frame.rowconfigure(0, weight=1)
        self.bubble_radius_frame.columnconfigure(1, weight=1)

        self.bubble_radius_label.grid(column=0, row=0, sticky='nesw')
        self.bubble_radius_slider.grid(column=1, row=0, sticky='ew')

        self.undo_btn = tkinter.Button(
            self.instruments_panel, text='UNDO',
            command=self.bus.statechart.launch_undo_event)
        self.undo_btn.grid(row=0, column=4, sticky='w')
        self.root.bind('<Control-z>', lambda _: self.bus.statechart.launch_undo_event())

        self.forced_scale_var = tkinter.DoubleVar(value=0)
        self.forced_scale_frame = tkinter.Frame(self.instruments_panel)
        self.forced_scale_frame.grid(row=0, column=5, sticky='nesw')
        self.forced_scale_input = tkinter.Entry(self.forced_scale_frame, textvariable=self.forced_scale_var)
        self.forced_scale_input.grid(column=0, row=0, sticky='w')
        self.forced_scale_apply_btn = tkinter.Button(self.forced_scale_frame, text='SCALE', command=self.update_image_with_forced_scale)
        self.forced_scale_apply_btn.grid(column=1, row=0, sticky='w')
        self.forced_scale_apply_btn = tkinter.Button(self.forced_scale_frame, text='RESET', command=self.reset_forced_scale)
        self.forced_scale_apply_btn.grid(column=2, row=0, sticky='w')

        self.root.bind('<Configure>', lambda _: self.redraw_image())

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

    def enable_bubble_radius_slider(self):
        self.bubble_radius_slider['state'] = 'normal'
        self.root.bind('<Button-4>', lambda _: self._update_bubble_size(delta_change=-5))
        self.root.bind('<Button-5>', lambda _: self._update_bubble_size(delta_change=+5))

    def disable_bubble_radius_slider(self):
        self.bubble_radius_slider['state'] = 'disabled'
        self.root.unbind('<Button-4>')
        self.root.unbind('<Button-5>')

    def _draw_temp_bubble(self, x: int = None, y: int = None) -> None:
        if not self.image:
            return

        if x is None or y is None:
            x, y = self._temp_bubble_coords

        x, y = self.image.get_clamped_coords_on_image(x, y)
        self._temp_bubble_coords = [x, y]

        for bubble in self.canvas.gettags('#temp_bubble'):
            self.canvas.delete(bubble)

        radius = int(self.bubble_radius_var.get())
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill='red', tags=('#temp_bubble',))

    def _on_canvas_click(self, x, y) -> None:
        rel_x, rel_y, rel_radius = self.image.get_bubbles_coords_on_image(x, y, self.bubble_radius_var.get())
        self.bus.statechart.launch_add_bubble_event(AddBubblePayload(pos=[rel_x, rel_y], radius=rel_radius))

    def load_image(self, path_to_image: pathlib.Path, bubbles: list) -> None:
        self.image = BubblingEditorImage(canvas=self.canvas, path_to_image=path_to_image, bubbles=bubbles)
        self.redraw_image()

    def redraw_image(self):
        if self.image:
            self.image.redraw_image()

    def update_image_with_forced_scale(self):
        if self.image:
            forced_scale = None if float(self.forced_scale_var.get()) <= 0 else float(self.forced_scale_var.get())
            self.image.set_forced_scale(forced_scale)

    def reset_forced_scale(self):
        self.forced_scale_var.set(0)
        self.update_image_with_forced_scale()

    def add_bubble(self, bubble: AddBubblePayload) -> None:
        self.image.add_bubble(bubble)

    def update_bubbles(self, bubbles: list[AddBubblePayload]) -> None:
        self.image.update_bubbles(bubbles)

    def _update_bubble_size(self, delta_change):
        current_size = int(self.bubble_radius_var.get())
        new_size = current_size + delta_change
        self.bubble_radius_var.set(new_size)
        self._draw_temp_bubble()

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

