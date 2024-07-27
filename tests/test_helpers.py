import unittest
from bubbling_editor.helpers import get_size_to_fit


class WidthGreaterThanHeightTestHelpers(unittest.TestCase):
    def test_cw100_ch50_iw100_ih50(self):
        """ширина больше высоты, равные пропорции, изображение равно канвасу"""
        c_w, c_h = 100, 50
        i_w, i_h = 100, 50
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 100
        assert new_ih == 50
        assert i_scale == 1

    def test_cw100_ch50_iw10_ih5(self):
        """ширина больше высоты, равные пропорции, изображение меньше канваса"""
        c_w, c_h = 100, 50
        i_w, i_h = 10, 5
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 100
        assert new_ih == 50
        assert i_scale == 10

    def test_cw100_ch50_iw1000_ih500(self):
        """ширина больше высоты, равные пропорции, изображение больше канваса"""
        c_w, c_h = 100, 50
        i_w, i_h = 1000, 500
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 100
        assert new_ih == 50
        assert i_scale == 0.1


class HeightGreaterThanWidthTestHelpers(unittest.TestCase):
    def test_cw50_ch100_iw50_ih100(self):
        """высота больше ширины, равные пропорции, изображение равно канвасу"""
        c_w, c_h = 50, 100
        i_w, i_h = 50, 100
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 50
        assert new_ih == 100
        assert i_scale == 1

    def test_cw50_ch100_iw5_ih10(self):
        """высота больше ширины, равные пропорции, изображение меньше канваса"""
        c_w, c_h = 50, 100
        i_w, i_h = 5, 10
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 50
        assert new_ih == 100
        assert i_scale == 10

    def test_cw50_ch100_iw500_ih1000(self):
        """высота больше ширины, равные пропорции, изображение больше канваса"""
        c_w, c_h = 50, 100
        i_w, i_h = 500, 1000
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 50
        assert new_ih == 100
        assert i_scale == 0.1




if __name__ == '__main__':
    unittest.main()
