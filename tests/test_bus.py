import unittest

from bubbling_editor.bus import Bus


class TestBus(unittest.TestCase):
    def test_register(self):
        bus = Bus()

        bus.register('x', '1')
        assert len(bus.objects) == 1
        bus.register('y', '2')
        assert len(bus.objects) == 2
        bus.register('z', '3')
        assert len(bus.objects) == 3
        bus.register('x', '1')
        assert len(bus.objects) == 3

    def test_get_attr(self):
        bus = Bus()

        bus.register('x', '1')
        assert bus.x == '1'

        bus.register('some_val', '2')
        assert bus.some_val == '2'

    def test_get_item(self):
        bus = Bus()

        bus.register('x', '1')
        assert bus['x'] == '1'

        bus.register('some key', 'some val')
        assert bus['some key'] == 'some val'




if __name__ == '__main__':
    unittest.main()
