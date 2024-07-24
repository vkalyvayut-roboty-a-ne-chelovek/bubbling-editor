import tkinter

from bubbling_editor.bus import Bus


class Gui:
    def __init__(self, bus:Bus):
        self.bus = bus
        self.bus.register('gui', self)
        self.root: tkinter.Tk = None

    def make_gui(self):
        self.root = tkinter.Tk()
        try:
            self.root.attributes('-zoomed', True)
        except:
            self.root.geometry(f'{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0')

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=95)

        self.instruments_panel = tkinter.Frame(self.root, background='red')
        self.instruments_panel.grid(row=0, column=0, sticky='ew')

        self.canvas_panel = tkinter.Frame(self.root)
        self.canvas_panel.grid(row=1, column=0, sticky='nesw')

        self.new_image_btn = tkinter.Button(self.instruments_panel, text='NEW')
        self.new_image_btn.grid(row=0, column=0, sticky='n')

        self.open_image_btn = tkinter.Button(self.instruments_panel, text='OPEN')
        self.open_image_btn.grid(row=0, column=1, sticky='n')

        self.save_image_btn = tkinter.Button(self.instruments_panel, text='SAVE', state='disabled')
        self.save_image_btn.grid(row=0, column=2, sticky='n')


    def run(self):
        self.make_gui()
        self.root.mainloop()


if __name__ == '__main__':
    b = Bus()
    g = Gui(bus=b)
    g.run()