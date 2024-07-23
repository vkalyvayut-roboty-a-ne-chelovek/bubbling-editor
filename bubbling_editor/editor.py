from bubbling_editor.bus import Bus
from bubbling_editor.statechart import Statechart
from bubbling_editor.gui import Gui


def run():
    bus = Bus()
    gui = Gui(bus)
    statechart = Statechart('bubbling_editor', bus=bus)

    statechart.run()
    gui.run()