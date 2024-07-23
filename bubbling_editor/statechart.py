from miros import ActiveObject
from miros import return_status
from miros import signals
from miros import Event

from bubbling_editor.bus import Bus


class Statechart(ActiveObject):
    def __init__(self, name: str, bus: Bus):
        super().__init__(name=name)
        self.bus = bus
        self.bus.register('statechart', self)

    def run(self):
        pass