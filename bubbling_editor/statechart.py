from collections import namedtuple
import pathlib

from miros import ActiveObject
from miros import return_status
from miros import signals
from miros import Event
from miros import spy_on

from bubbling_editor.bus import Bus

AddBubblePayload = namedtuple('AddBubblePayload', ['pos', 'radius'])


class Statechart(ActiveObject):
    def __init__(self, name: str, bus: Bus):
        super().__init__(name=name)
        self.bus = bus
        self.bus.register('statechart', self)

        self.path_to_image = None
        self.bubbles = []

    def run(self):
        self.start_at(init_state)

    def on_init_state_new_image(self, path_to_image: pathlib.Path):
        self.path_to_image = path_to_image
        self.bus.gui.load_image(path_to_image, bubbles=[])

    def on_init_state_load_image(self, path_to_image: pathlib.Path):
        pass

    def on_image_loaded_save_image(self, path_to_image: pathlib.Path):
        pass

    def on_image_loaded_add_bubble(self, bubble_data: AddBubblePayload):
        self.bubbles.append(bubble_data)



    def launch_new_image_event(self, path_to_image: pathlib.Path) -> None:
        self.post_fifo(Event(signal=signals.NEW_IMAGE, payload=path_to_image))

    def launch_load_image_event(self, path_to_image: pathlib.Path) -> None:
        self.post_fifo(Event(signal=signals.LOAD_IMAGE, payload=path_to_image))

    def launch_save_image_event(self, path_to_image: pathlib.Path) -> None:
        self.post_fifo(Event(signal=signals.SAVE_IMAGE, payload=path_to_image))


@spy_on
def init_state(s: Statechart, e: Event) -> return_status:
    status = return_status.UNHANDLED

    if e.signal == signals.ENTRY_SIGNAL:
        status = return_status.HANDLED
    elif e.signal == signals.NEW_IMAGE:
        s.on_init_state_new_image(e.payload)
        status = s.trans(image_loaded)
    elif e.signal == signals.LOAD_IMAGE:
        s.on_init_state_load_image(e.payload)
        status = s.trans(image_loaded)
    else:
        s.temp.fun = s.top
        status = return_status.SUPER

    return status


@spy_on
def image_loaded(s: Statechart, e: Event) -> return_status:
    status = return_status.UNHANDLED

    if e.signal == signals.ENTRY_SIGNAL:
        status = return_status.HANDLED
    elif e.signal == signals.ADD_BUBBLE:
        status = return_status.HANDLED
        s.on_image_loaded_add_bubble(e.payload)
    elif e.signal == signals.SAVE_IMAGE:
        s.on_image_loaded_save_image(e.payload)
        status = return_status.HANDLED
    else:
        s.temp.fun = init_state
        status = return_status.SUPER

    return status
