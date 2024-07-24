import tkinter

from bubbling_editor.bus import Bus


class Gui:
    def __init__(self, bus:Bus):
        self.bus = bus
        self.bus.register('gui', self)
        self.root: tkinter.Tk = None

    def make_gui(self):
        self.root = tkinter.Tk()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=5)
        self.root.rowconfigure(1, weight=95)

        self.instruments_panel = tkinter.Frame(self.root, background='red')
        self.instruments_panel.grid(row=0, column=0, sticky='nesw')

        self.canvas_panel = tkinter.Frame(self.root)
        self.canvas_panel.grid(row=1, column=0, sticky='nesw')

        self.new_image_btn = tkinter.Button(text='NEW')
        self.new_image_btn.instruments_panel.grid(row=0, column=0, sticky='ew')

        self.open_image_btn = tkinter.Button(text='OPEN')
        self.open_image_btn.instruments_panel.grid(row=0, column=1, sticky='ew')

        self.save_image_btn = tkinter.Button(text='SAVE')
        self.save_image_btn.instruments_panel.grid(row=0, column=2, sticky='ew')


    def run(self):
        self.root.mainloop()
