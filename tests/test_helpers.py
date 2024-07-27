import unittest
from bubbling_editor.helpers import get_size_to_fit


class CanvasWidthGreaterThanCanvasHeightTestHelpers(unittest.TestCase):
    def test_cw100_ch50_iw100_ih50(self):
        """ширина больше высоты, прямоугольник, изображение равно канвасу"""
        c_w, c_h = 100, 50
        i_w, i_h = 100, 50
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 100
        assert new_ih == 50
        assert i_scale == 1

    def test_cw100_ch50_iw10_ih5(self):
        """ширина больше высоты, прямоугольник, изображение меньше канваса"""
        c_w, c_h = 100, 50
        i_w, i_h = 10, 5
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 50
        assert new_ih == 25
        assert i_scale == 5

    def test_cw100_ch50_iw1000_ih500(self):
        """ширина больше высоты, прямоугольник, изображение больше канваса"""
        c_w, c_h = 100, 50
        i_w, i_h = 1000, 500
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 50
        assert new_ih == 25
        assert i_scale == 0.05

    def test_cw100_ch50_iw50_ih50(self):
        """ширина больше высоты, квадрат, по высоте равен канвасу"""
        c_w, c_h = 100, 50
        i_w, i_h = 50, 50
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 50
        assert new_ih == 50
        assert i_scale == 1

    def test_cw100_ch50_iw5_ih5(self):
        """ширина больше высоты, квадрат, по высоте меньше канваса"""
        c_w, c_h = 100, 50
        i_w, i_h = 5, 5
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 50
        assert new_ih == 50
        assert i_scale == 10

    def test_cw100_ch50_iw100_ih100(self):
        """ширина больше высоты, квадрат, по высоте больше канваса"""
        c_w, c_h = 100, 50
        i_w, i_h = 100, 100
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 50
        assert new_ih == 50
        assert i_scale == 0.5

    def test_cw100_ch50_iw25_ih50(self):
        """ширина больше высоты, прямоугольник, по ширине меньше канваса, по высоте равно канвасу"""
        c_w, c_h = 100, 50
        i_w, i_h = 25, 50
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 25
        assert new_ih == 50
        assert i_scale == 1

    def test_cw100_ch50_iw5_ih25(self):
        """ширина больше высоты, прямоугольник, по ширине меньше канваса, по высоте меньше канваса"""
        c_w, c_h = 100, 50
        i_w, i_h = 5, 25
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 10
        assert new_ih == 50
        assert i_scale == 2

    def test_cw100_ch50_iw25_ih50(self):
        """ширина больше высоты, прямоугольник, по ширине меньше канваса, по высоте больше канваса"""
        c_w, c_h = 100, 50
        i_w, i_h = 50, 250
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 10
        assert new_ih == 50
        assert i_scale == 0.2

    def test_cw100_ch50_iw100_ih50(self):
        """ширина больше высоты, прямоугольник, по ширине равен канвасу, по высоте меньше"""
        c_w, c_h = 100, 50
        i_w, i_h = 100, 25
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 100
        assert new_ih == 25
        assert i_scale == 1

    def test_cw100_ch50_iw100_ih50(self):
        """ширина больше высоты, прямоугольник, по ширине меньше канваса, по высоте меньше канваса"""
        c_w, c_h = 100, 50
        i_w, i_h = 50, 25
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 100
        assert new_ih == 50
        assert i_scale == 2

    def test_cw100_ch50_iw100_ih50(self):
        """ширина больше высоты, прямоугольник, по ширине больше канваса, по высоте меньше канваса"""
        c_w, c_h = 100, 50
        i_w, i_h = 200, 50
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 50
        assert new_ih == 12
        assert i_scale == 0.25


class CanvasWidthLessThanCanvasHeightTestHelpers(unittest.TestCase):
    def test_cw50_ch100_iw50_ih100(self):
        """ширина меньше высоты, прямоугольник, изображение равно канвасу"""
        c_w, c_h = 50, 100
        i_w, i_h = 50, 100
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 50
        assert new_ih == 100
        assert i_scale == 1

    def test_cw50_ch100_iw25_ih50(self):
        """ширина меньше высоты, прямоугольник, изображение меньше канваса"""
        c_w, c_h = 50, 100
        i_w, i_h = 25, 50
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 50
        assert new_ih == 100
        assert i_scale == 2

    def test_cw50_ch100_iw50_ih100(self):
        """ширина меньше высоты, прямоугольник, изображение больше канваса"""
        c_w, c_h = 50, 100
        i_w, i_h = 500, 1000
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 50
        assert new_ih == 100
        assert i_scale == 0.1

    def test_cw50_ch100_iw50_ih50(self):
        """ширина меньше высоты, квадрат, по высоте равен канвасу"""
        c_w, c_h = 50, 100
        i_w, i_h = 50, 50
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 50
        assert new_ih == 50
        assert i_scale == 1

    def test_cw50_ch100_iw5_ih5(self):
        """ширина меньше высоты, квадрат, по высоте меньше канваса"""
        c_w, c_h = 50, 100
        i_w, i_h = 5, 5
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 50
        assert new_ih == 50
        assert i_scale == 10

    def test_cw50_ch100_iw100_ih100(self):
        """ширина меньше высоты, квадрат, по высоте больше канваса"""
        c_w, c_h = 100, 50
        i_w, i_h = 100, 100
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 50
        assert new_ih == 50
        assert i_scale == 0.5

    def test_cw50_ch100_iw25_ih100(self):
        """ширина меньше высоты, прямоугольник, по высоте равно канвасу, по ширине меньше канваса"""
        c_w, c_h = 50, 100
        i_w, i_h = 25, 100
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 12
        assert new_ih == 50
        assert i_scale == 0.5

    def test_cw50_ch100_iw25_ih50(self):
        """ширина меньше высоты, прямоугольник, по высоте меньше канваса, по ширине меньше канваса"""
        c_w, c_h = 50, 100
        i_w, i_h = 25, 50
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 50
        assert new_ih == 100
        assert i_scale == 2

    def test_cw50_ch100_iw25_ih200(self):
        """ширина меньше высоты, прямоугольник, по высоте больше канваса, по ширине меньше канваса"""
        c_w, c_h = 50, 100
        i_w, i_h = 10, 200
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 2
        assert new_ih == 50
        assert i_scale == 0.25

    def test_cw50_ch100_iw50_ih100(self):
        """ширина меньше высоты, прямоугольник, по высоте меньше канваса, по ширине равно канвасу"""
        c_w, c_h = 50, 100
        i_w, i_h = 25, 100
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 12
        assert new_ih == 50
        assert i_scale == 0.5

    def test_cw50_ch100_iw25_ih50(self):
        """ширина меньше высоты, прямоугольник, по высоте меньше канваса, по ширине меньше канваса"""
        c_w, c_h = 50, 100
        i_w, i_h = 25, 50
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 25
        assert new_ih == 50
        assert i_scale == 1

    def test_cw50_ch100_iw10_ih200(self):
        """ширина меньше высоты, прямоугольник, по высоте меньше канваса, по ширине больше канваса"""
        c_w, c_h = 50, 100
        i_w, i_h = 10, 200
        new_iw, new_ih, i_scale = get_size_to_fit(i_w=i_w, i_h=i_h, c_w=c_w, c_h=c_h)

        assert new_iw == 2  # должно быть 2.5, но из-за округления вниз будет 2
        assert new_ih == 50
        assert i_scale == 0.25



if __name__ == '__main__':
    unittest.main()
