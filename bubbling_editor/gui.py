from bubbling_editor.bus import Bus


class Gui:
    def __init__(self, bus:Bus):
        self.bus = bus
        self.bus.register('gui', self)

    def run(self):
        pass
