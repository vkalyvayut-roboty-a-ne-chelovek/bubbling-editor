import os.path
import pathlib
import tempfile
import time
import unittest

from miros import stripped
from miros import Event
from miros import signals

from bubbling_editor.bus import Bus
from bubbling_editor.misc import AddBubblePayload, Kind
from bubbling_editor.statechart import Statechart
from bubbling_editor.gui import TestabeGui


class TestStatechart(unittest.TestCase):
    @staticmethod
    def _assert_trace_check(expected_trace, actual_trace):
        with (stripped(expected_trace) as _expected_trace, stripped(actual_trace) as _actual_trace):
            assert len(_expected_trace) == len(_actual_trace), \
                f'Not enough events: expected ({len(_expected_trace)}) != actual({len(_actual_trace)})'

            for expected, actual in zip(_expected_trace, _actual_trace):
                assert expected == actual, f'{expected} != {actual}'

    @staticmethod
    def _assert_spy_check(expected_spy, actual_spy):
        assert len(expected_spy) == len(
            actual_spy), f'Not enough events: expected ({len(expected_spy)}) != actual({len(actual_spy)})'
        for expected, actual in zip(actual_spy, expected_spy):
            assert expected == actual, f'{expected} != {actual}'

    def setUp(self):
        self.bus = Bus()
        self.s = Statechart('bubbling_editor', bus=self.bus)
        self.g = TestabeGui(self.bus)
        self.s.run()

    def test_run(self):
        expected_trace = '''
        [2024-07-23 11:46:20.964995] [bubbling_editor] e->start_at() top->init_state
        '''
        actual_trace = self.s.trace()

        self._assert_trace_check(expected_trace, actual_trace)

    def test_new_image(self):
        self.s.launch_new_image_event('./assets/smiley.png')
        time.sleep(0.1)

        expected_trace = '''
        [2024-07-23 11:56:21.926948] [bubbling_editor] e->start_at() top->init_state
        [2024-07-23 11:56:21.928058] [bubbling_editor] e->NEW_IMAGE() init_state->image_loaded
        '''
        actual_trace = self.s.trace()

        self._assert_trace_check(expected_trace, actual_trace)

    def test_load_project(self):
        self.s.launch_new_image_event('./assets/smiley.png')
        time.sleep(0.1)
        self.s.launch_add_bubble_event(AddBubblePayload(pos=[0, 0], radius=0))
        time.sleep(0.1)

        tmp_file = pathlib.Path(tempfile.mktemp(suffix='.bubbling')).absolute()
        self.s.launch_save_project_event(tmp_file)
        self.setUp()
        time.sleep(0.1)
        self.s.launch_load_project_event(path_to_project=tmp_file)
        time.sleep(0.1)

        expected_trace = '''
        [2024-07-28 21:09:13.019112] [bubbling_editor] e->start_at() top->init_state
        [2024-07-28 21:09:13.119735] [bubbling_editor] e->LOAD_PROJECT() init_state->image_loaded
        '''
        actual_trace = self.s.trace()

        expected_spy = ['START', 'SEARCH_FOR_SUPER_SIGNAL:init_state', 'ENTRY_SIGNAL:init_state', 'INIT_SIGNAL:init_state', '<- Queued:(0) Deferred:(0)', 'LOAD_PROJECT:init_state', 'SEARCH_FOR_SUPER_SIGNAL:image_loaded', 'ENTRY_SIGNAL:image_loaded', 'INIT_SIGNAL:image_loaded', '<- Queued:(0) Deferred:(0)']
        actual_spy = self.s.spy()

        self._assert_trace_check(expected_trace, actual_trace)
        self._assert_spy_check(expected_spy, actual_spy)

    def test_save_project(self):
        self.s.launch_new_image_event('./assets/smiley.png')
        time.sleep(0.1)
        self.s.launch_add_bubble_event(AddBubblePayload(pos=[0, 0], radius=0))
        time.sleep(0.1)

        tmp_file = pathlib.Path(tempfile.mktemp(suffix='.bubbling')).absolute()
        self.s.launch_save_project_event(tmp_file)
        time.sleep(0.1)

        assert os.path.exists(tmp_file), f'{tmp_file} does not exists'

        expected_spy = ['START', 'SEARCH_FOR_SUPER_SIGNAL:init_state', 'ENTRY_SIGNAL:init_state', 'INIT_SIGNAL:init_state', '<- Queued:(0) Deferred:(0)', 'NEW_IMAGE:init_state', 'SEARCH_FOR_SUPER_SIGNAL:image_loaded', 'ENTRY_SIGNAL:image_loaded', 'INIT_SIGNAL:image_loaded', '<- Queued:(0) Deferred:(0)', 'ADD_BUBBLE:image_loaded', 'ADD_BUBBLE:image_loaded:HOOK', '<- Queued:(0) Deferred:(0)', 'SAVE_PROJECT:image_loaded', 'SAVE_PROJECT:image_loaded:HOOK', '<- Queued:(0) Deferred:(0)']

        actual_spy = self.s.spy()

        self._assert_spy_check(expected_spy, actual_spy)

    def test_add_bubble(self):
        self.s.launch_new_image_event('./assets/smiley.png')
        self.s.launch_add_bubble_event(AddBubblePayload(pos=[0, 0], radius=0))
        self.s.launch_add_bubble_event(AddBubblePayload(pos=[0, 0], radius=0, kind=Kind.COUNTER))
        time.sleep(0.1)

        expected_spy = ['START', 'SEARCH_FOR_SUPER_SIGNAL:init_state', 'ENTRY_SIGNAL:init_state', 'INIT_SIGNAL:init_state', '<- Queued:(0) Deferred:(0)', 'NEW_IMAGE:init_state', 'SEARCH_FOR_SUPER_SIGNAL:image_loaded', 'ENTRY_SIGNAL:image_loaded', 'INIT_SIGNAL:image_loaded', '<- Queued:(2) Deferred:(0)', 'ADD_BUBBLE:image_loaded', 'ADD_BUBBLE:image_loaded:HOOK', '<- Queued:(1) Deferred:(0)', 'ADD_BUBBLE:image_loaded', 'ADD_BUBBLE:image_loaded:HOOK', '<- Queued:(0) Deferred:(0)']

        actual_spy = self.s.spy()

        self._assert_spy_check(expected_spy, actual_spy)

    def test_undo(self):
        self.s.launch_new_image_event('./assets/smiley.png')
        self.s.launch_add_bubble_event(AddBubblePayload(pos=[0, 0], radius=0))
        self.s.launch_add_bubble_event(AddBubblePayload(pos=[0, 0], radius=0))
        time.sleep(0.1)
        self.s.launch_undo_event()
        time.sleep(0.1)

        expected_spy = ['START', 'SEARCH_FOR_SUPER_SIGNAL:init_state', 'ENTRY_SIGNAL:init_state', 'INIT_SIGNAL:init_state', '<- Queued:(0) Deferred:(0)', 'NEW_IMAGE:init_state', 'SEARCH_FOR_SUPER_SIGNAL:image_loaded', 'ENTRY_SIGNAL:image_loaded', 'INIT_SIGNAL:image_loaded', '<- Queued:(2) Deferred:(0)', 'ADD_BUBBLE:image_loaded', 'ADD_BUBBLE:image_loaded:HOOK', '<- Queued:(1) Deferred:(0)', 'ADD_BUBBLE:image_loaded', 'ADD_BUBBLE:image_loaded:HOOK', '<- Queued:(0) Deferred:(0)', 'UNDO:image_loaded', 'UNDO:image_loaded:HOOK', '<- Queued:(0) Deferred:(0)']

        actual_spy = self.s.spy()

        self._assert_spy_check(expected_spy, actual_spy)

    def test_export(self):
        self.s.launch_new_image_event('./assets/smiley.png')
        self.s.launch_add_bubble_event(AddBubblePayload(pos=[0, 0], radius=0))
        self.s.launch_add_bubble_event(AddBubblePayload(pos=[0, 0], radius=0, kind=Kind.COUNTER))
        time.sleep(0.1)
        tmp_file = pathlib.Path(tempfile.mktemp(suffix='.png')).absolute()
        self.s.launch_export_image_event(tmp_file)
        time.sleep(0.1)

        assert os.path.exists(tmp_file)

        expected_spy = ['START', 'SEARCH_FOR_SUPER_SIGNAL:init_state', 'ENTRY_SIGNAL:init_state', 'INIT_SIGNAL:init_state', '<- Queued:(0) Deferred:(0)', 'NEW_IMAGE:init_state', 'SEARCH_FOR_SUPER_SIGNAL:image_loaded', 'ENTRY_SIGNAL:image_loaded', 'INIT_SIGNAL:image_loaded', '<- Queued:(2) Deferred:(0)', 'ADD_BUBBLE:image_loaded', 'ADD_BUBBLE:image_loaded:HOOK', '<- Queued:(1) Deferred:(0)', 'ADD_BUBBLE:image_loaded', 'ADD_BUBBLE:image_loaded:HOOK', '<- Queued:(0) Deferred:(0)', 'EXPORT_IMAGE:image_loaded', 'EXPORT_IMAGE:image_loaded:HOOK', '<- Queued:(0) Deferred:(0)']

        actual_spy = self.s.spy()

        self._assert_spy_check(expected_spy, actual_spy)

    def test_set_color(self):
        self.s.launch_new_image_event('./assets/smiley.png')
        self.s.launch_set_color_event('red')
        self.s.launch_add_bubble_event(AddBubblePayload(pos=[0, 0], radius=0))
        time.sleep(0.1)
        self.s.launch_undo_event()
        time.sleep(0.1)

        expected_spy = ['START', 'SEARCH_FOR_SUPER_SIGNAL:init_state', 'ENTRY_SIGNAL:init_state', 'INIT_SIGNAL:init_state', '<- Queued:(0) Deferred:(0)', 'NEW_IMAGE:init_state', 'SEARCH_FOR_SUPER_SIGNAL:image_loaded', 'ENTRY_SIGNAL:image_loaded', 'INIT_SIGNAL:image_loaded', '<- Queued:(2) Deferred:(0)', 'SET_COLOR:image_loaded', 'SET_COLOR:image_loaded:HOOK', '<- Queued:(1) Deferred:(0)', 'ADD_BUBBLE:image_loaded', 'ADD_BUBBLE:image_loaded:HOOK', '<- Queued:(0) Deferred:(0)', 'UNDO:image_loaded', 'UNDO:image_loaded:HOOK', '<- Queued:(0) Deferred:(0)']

        actual_spy = self.s.spy()

        self._assert_spy_check(expected_spy, actual_spy)


if __name__ == '__main__':
    unittest.main()
