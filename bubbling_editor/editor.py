from bubbling_editor.helpers import export_project, get_args
from bubbling_editor.bus import Bus
from bubbling_editor.statechart import Statechart
from bubbling_editor.gui import Gui


def run():
    args = get_args()
    if args.path_to_project:
        export_project(path_to_project=args.path_to_project,
                       path_to_exported_image=args.path_to_image)
    else:
        bus = Bus()
        gui = Gui(bus)
        statechart = Statechart('bubbling_editor', bus=bus)

        statechart.run()
        gui.run()


if __name__ == '__main__':
    run()
