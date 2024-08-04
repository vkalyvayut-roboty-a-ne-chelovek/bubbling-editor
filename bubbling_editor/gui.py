import os.path
import pathlib
import tkinter
from tkinter import filedialog, colorchooser


from bubbling_editor.bus import Bus

from bubbling_editor.misc import AddBubblePayload, Kind
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

    def enable_export_btn(self):
        pass

    def disable_export_btn(self):
        pass

    def enable_click_listener(self):
        pass

    def disable_click_listener(self):
        pass

    def enable_bubble_radius_slider(self):
        pass

    def disable_bubble_radius_slider(self):
        pass

    def enable_undo_btn(self):
        pass

    def disable_undo_btn(self):
        pass

    def enable_forced_scale(self):
        pass

    def disable_forced_scale(self):
        pass

    def enable_color_picker_btn(self):
        pass

    def disable_color_picker_btn(self):
        pass

    def load_image(self, path_to_image: pathlib.Path, bubbles: list, color: str) -> None:
        pass

    def redraw_image(self) -> None:
        pass

    def add_bubble(self, bubble: AddBubblePayload) -> None:
        pass

    def update_bubbles(self, bubbles: list[AddBubblePayload]) -> None:
        pass


class Gui(TestabeGui):
    def __init__(self, bus: Bus):
        super().__init__(bus=bus)
        self.color = None
        self.path_to_image = None
        self.root: tkinter.Tk = None

        self.image: BubblingEditorImage = None

        self.forced_scale_var: tkinter.DoubleVar = None

        self._temp_bubble_coords: list[int, int] = [0, 0]

    def make_gui(self):
        self.root = tkinter.Tk()
        self.root.attributes('-zoomed', True)
        self.root.title('bubbling editor 🖼')

        self.menu = tkinter.Menu(self.root, tearoff=False, borderwidth=0)
        self.project_menu = tkinter.Menu(tearoff=False)
        self.bubble_menu = tkinter.Menu(tearoff=False)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=95)

        self.instruments_panel = tkinter.Frame(self.root)
        self.instruments_panel.grid(row=0, column=0, sticky='ew')

        self.canvas_panel = tkinter.Frame(self.root)
        self.canvas_panel.grid(row=1, column=0, sticky='nesw')
        self.canvas_panel.columnconfigure(0, weight=1)
        self.canvas_panel.rowconfigure(0, weight=1)

        self.canvas = tkinter.Canvas(self.canvas_panel)
        self.canvas.grid(row=0, column=0, sticky='nesw')

        # new image
        self.root.bind('<Control-n>', lambda _: self._show_new_image_popup())
        self.project_menu.add_command(label='New',
                                      command=self._show_new_image_popup,
                                      accelerator='<Control-n>')

        # load project
        self.root.bind('<Control-o>', lambda _: self._show_open_project_popup())
        self.project_menu.add_command(label='Open',
                                      command=self._show_open_project_popup,
                                      accelerator='<Control-o>')

        # save project
        self.project_menu.add_command(label='Save',
                                      command=self._show_save_project_popup,
                                      accelerator='<Control-s>',
                                      state='disabled')

        self.project_menu.add_separator()

        # export image
        self.project_menu.add_command(label='Export',
                                      command=self._show_export_image_popup,
                                      accelerator='<Control-e>',
                                      state='disabled')

        # undo last bubble
        self.root.bind('<Control-z>', lambda _: self.bus.statechart.launch_undo_event())
        self.bubble_menu.add_command(label='Undo',
                                     command=self.bus.statechart.launch_undo_event,
                                     state='disabled',
                                     accelerator='<Control-z>')
        self.bubble_menu.add_separator()

        # bubble radius
        self.bubble_radius_var = tkinter.IntVar(value=0)
        self.bubble_radius_frame = tkinter.Frame(self.instruments_panel)
        self.bubble_radius_prefix_label = tkinter.Label(self.bubble_radius_frame, text='Bubble size:')
        self.bubble_radius_label = tkinter.Label(self.bubble_radius_frame,
                                                 textvariable=self.bubble_radius_var,
                                                 width=5)
        self.bubble_radius_slider = tkinter.Scale(self.bubble_radius_frame,
                                                  from_=5,
                                                  to=250,
                                                  length=150,
                                                  resolution=5,
                                                  showvalue=False,
                                                  orient='horizontal',
                                                  variable=self.bubble_radius_var,
                                                  state='disabled')

        self.bubble_radius_frame.grid(row=0, column=4, sticky='nesw')
        self.bubble_radius_frame.rowconfigure(0, weight=1)
        self.bubble_radius_frame.columnconfigure(1, weight=1)
        self.bubble_radius_frame.columnconfigure(2, weight=1)

        self.bubble_radius_prefix_label.grid(column=0, row=0, sticky='nesw')
        self.bubble_radius_label.grid(column=1, row=0, sticky='nesw')
        self.bubble_radius_slider.grid(column=2, row=0, sticky='ew')
        self.bubble_menu.add_command(label='bubble size+',
                                     command=lambda: self._update_bubble_size(+5),
                                     accelerator='<KP_Add>',
                                     state='disabled')
        self.bubble_menu.add_command(label='bubble size-',
                                     command=lambda: self._update_bubble_size(-5),
                                     accelerator='<KP_Subtract>',
                                     state='disabled')
        self.bubble_menu.add_separator()

        # forced scale
        self.forced_scale_var = tkinter.DoubleVar(value=0)
        self.forced_scale_frame = tkinter.Frame(self.instruments_panel, padx=10)
        self.forced_scale_frame.grid(row=0, column=6, sticky='nesw')
        self.forced_scale_label = tkinter.Label(self.forced_scale_frame, text='Forced scale: ')
        self.forced_scale_label.grid(column=0, row=0, sticky='w')
        self.forced_scale_input = tkinter.Entry(self.forced_scale_frame,
                                                textvariable=self.forced_scale_var)
        self.forced_scale_input.grid(column=1, row=0, sticky='w')
        self.forced_scale_apply_btn = tkinter.Button(self.forced_scale_frame,
                                                     text='APPLY',
                                                     command=self._update_image_with_forced_scale,
                                                     state='disabled')
        self.forced_scale_apply_btn.grid(column=2, row=0, sticky='w')
        self.forced_scale_reset_btn = tkinter.Button(self.forced_scale_frame,
                                                     text='RESET',
                                                     command=self._reset_forced_scale,
                                                     state='disabled')
        self.forced_scale_reset_btn.grid(column=3, row=0, sticky='w')

        # color
        self.color_picker_frame = tkinter.Frame(self.instruments_panel)
        self.color_picker_frame.grid(row=0, column=7, sticky='nesw')
        self.color_picker_frame.columnconfigure(0, weight=1)
        self.color_picker_frame.columnconfigure(1, weight=1)
        self.color_picker_frame.rowconfigure(0, weight=1)

        self.color_picker_color_indicator = tkinter.Label(self.color_picker_frame,
                                                          width=5,
                                                          background='red')
        self.color_picker_color_indicator.grid(row=0, column=0, sticky='nesw')
        self.color_picker_btn = tkinter.Button(self.color_picker_frame,
                                               text='COLOR',
                                               command=self._show_color_picker_popup,
                                               state='disabled')
        self.color_picker_btn.grid(row=0, column=1, sticky='w')
        self.bubble_menu.add_command(label='Color',
                                     command=self._show_color_picker_popup,
                                     state='disabled',
                                     accelerator='<Control-k>')

        # help
        self.root.bind('<F1>', lambda _: self._show_help_popup())

        self.root.bind('<Configure>', lambda _: self.redraw_image())
        self.menu.add_cascade(label='Project', menu=self.project_menu)
        self.menu.add_cascade(label='Bubble', menu=self.bubble_menu)
        self.menu.add_command(label='Help', command=self._show_help_popup, accelerator='<F1>')

        self.root.config(menu=self.menu)

    def run(self) -> None:
        self.make_gui()
        self.disable_save_btn()
        self.root.mainloop()

    def enable_save_btn(self):
        try:
            self.root.bind('<Control-s>', lambda _: self._show_save_project_popup())
            self.project_menu.entryconfig('Save', state='normal')
        except:
            pass

    def disable_save_btn(self):
        try:
            self.root.unbind('<Control-s>')
            self.project_menu.entryconfig('Save', state='disabled')
        except:
            pass

    def enable_export_btn(self):
        try:
            self.root.bind('<Control-e>', lambda _: self._show_export_image_popup())
            self.project_menu.entryconfig('Export', state='normal')
        except:
            pass

    def disable_export_btn(self):
        try:
            self.root.unbind('<Control-e>')
            # self.export_image_btn['state'] = 'disabled'
            self.project_menu.entryconfig('Export', state='disabled')
        except:
            pass

    def enable_click_listener(self):
        self.canvas.bind('<Button-1>', lambda e: self._on_canvas_click(e.x, e.y))
        self.canvas.bind('<Button-3>', lambda e: self._on_canvas_click(e.x, e.y, counter=True))
        self.canvas.bind('<Motion>', lambda e: self._draw_temp_bubble(e.x, e.y))

    def disable_click_listener(self):
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Button-3>')
        self.canvas.unbind('<Motion>')

    def enable_bubble_radius_slider(self):
        self.bubble_radius_slider['state'] = 'normal'
        self.root.bind('<Button-4>', lambda _: self._update_bubble_size(delta_change=-5))
        self.root.bind('<Button-5>', lambda _: self._update_bubble_size(delta_change=+5))
        self.bubble_menu.entryconfig('bubble size+', state='normal')
        self.bubble_menu.entryconfig('bubble size-', state='normal')
        self.root.bind('<KP_Add>', lambda _: self._update_bubble_size(+5))
        self.root.bind('<KP_Subtract>', lambda _: self._update_bubble_size(-5))

    def disable_bubble_radius_slider(self):
        self.bubble_radius_slider['state'] = 'disabled'
        self.root.unbind('<Button-4>')
        self.root.unbind('<Button-5>')
        self.bubble_menu.entryconfig('bubble size+', state='disabled')
        self.bubble_menu.entryconfig('bubble size-', state='disabled')
        self.root.unbind('<KP_Add>')
        self.root.unbind('<KP_Subtract>')

    def enable_undo_btn(self):
        self.bubble_menu.entryconfig('Undo', state='normal')

    def disable_undo_btn(self):
        self.bubble_menu.entryconfig('Undo', state='disabled')

    def enable_forced_scale(self):
        self.forced_scale_apply_btn['state'] = 'normal'
        self.forced_scale_reset_btn['state'] = 'normal'

    def disable_forced_scale(self):
        self.forced_scale_apply_btn['state'] = 'disabled'
        self.forced_scale_reset_btn['state'] = 'disabled'

    def enable_color_picker_btn(self):
        self.color_picker_btn['state'] = 'normal'
        self.root.bind('<Control-k>', lambda _: self._show_color_picker_popup())
        self.bubble_menu.entryconfig('Color', state='normal')

    def disable_color_picker_btn(self):
        self.color_picker_btn['state'] = 'disabled'
        self.root.unbind('<Control-k>')
        self.bubble_menu.entryconfig('Color', state='normal')

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
        self.canvas.create_oval(x - radius,
                                y - radius,
                                x + radius,
                                y + radius,
                                fill=self.color, tags=('#temp_bubble',))

    def _on_canvas_click(self, x, y, counter=False) -> None:
        bubble_radius = int(self.bubble_radius_var.get())
        rel_x, rel_y, rel_radius = self.image.get_bubbles_coords_on_image(x, y, bubble_radius)
        kind = Kind.COUNTER if counter else Kind.REGULAR

        bubble = AddBubblePayload(pos=[rel_x, rel_y], radius=rel_radius, kind=kind)

        self.bus.statechart.launch_add_bubble_event(bubble)

    def load_image(self, path_to_image: pathlib.Path, bubbles: list, color: str) -> None:
        self.path_to_image = path_to_image
        self.color = color
        self.image = BubblingEditorImage(canvas=self.canvas,
                                         path_to_image=path_to_image,
                                         bubbles=bubbles,
                                         color=color)
        self.redraw_image()
        self.color_picker_color_indicator['background'] = color

    def redraw_image(self):
        if self.image:
            self.image.redraw_image()

    def _update_forced_scale(self, forced_scale_dir: float = 0):
        self.forced_scale_var.set(float(self.forced_scale_var.get()) + forced_scale_dir)
        self._update_image_with_forced_scale()

    def _update_image_with_forced_scale(self):
        if self.image:
            forced_scale = float(self.forced_scale_var.get())
            forced_scale = None if forced_scale <= 0 else forced_scale
            self.image.set_forced_scale(forced_scale)

    def _reset_forced_scale(self):
        self.forced_scale_var.set(0)
        self._update_image_with_forced_scale()

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
        path_to_image = filedialog.askopenfilename(filetypes=[('Images', '.jpg .jpeg .png .gif')])
        if path_to_image:
            self.bus.statechart.launch_new_image_event(path_to_image)

    def _show_open_project_popup(self):
        path_to_image = filedialog.askopenfilename(filetypes=[('Bubbling Editor Metadata', '.bubbling')])
        if path_to_image:
            self.bus.statechart.launch_load_project_event(path_to_image)

    def _show_save_project_popup(self):
        image_dir = os.path.dirname(self.path_to_image)
        image_name, _ = os.path.splitext(os.path.basename(self.path_to_image))
        path_to_image = filedialog.asksaveasfilename(
            filetypes=[('Bubbling Editor Metadata', '.bubbling')],
            initialdir=image_dir,
            initialfile=f'{image_name}.bubbling'
        )
        if path_to_image:
            self.bus.statechart.launch_save_project_event(path_to_image)

    def _show_export_image_popup(self):
        image_dir = os.path.dirname(self.path_to_image)
        image_name, _ = os.path.splitext(os.path.basename(self.path_to_image))

        path_to_image = filedialog.asksaveasfilename(
            filetypes=[('Image', '.png')],
            initialdir=image_dir,
            initialfile=f'{image_name}_bubbling.png'
        )
        if path_to_image:
            self.bus.statechart.launch_export_image_event(path_to_image)

    def _show_color_picker_popup(self):
        _, color_hex = colorchooser.askcolor(initialcolor=self.color)
        if color_hex:
            self.bus.statechart.launch_set_color_event(color_hex)

    def _show_help_popup(self):
        help_text = '''
<Control-o> - open project
<Control-s> - save project
<Control-n> - import image
<Left-click> - draw bubble
<Right-click> - draw counter bubble
<Mouse-wheel> or KP_Add/KP_Subtract - change bubble size
<Control-k> - change background (no bubble) color
<Control-z> - remove last-bubble
<Control-e> - export project

Typical workflow:
1. import image or open project
2. add bubbles
3. save project
4. export image

Export project from command-line: \nbubbling-editor -p <path-to-project> -i <path-to-image>
        '''
        toplevel = tkinter.Toplevel(self.root)
        toplevel.title('Help')
        toplevel.bind('<Escape>', lambda _: toplevel.destroy())

        toplevel.columnconfigure(0, weight=1)
        toplevel.rowconfigure(0, weight=1)

        help_label = tkinter.Label(toplevel, text=help_text, justify='left', pady=5, padx=15)
        help_label.grid(row=0, column=0, sticky='nesw')

        toplevel.grab_set()
        self.root.wait_window(toplevel)
