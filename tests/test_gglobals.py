import unittest
from unittest.mock import patch

from gourmand.gglobals import get_link_and_star_color


class TestLinkColor(unittest.TestCase):

    def setUp(self):
        pass

    @patch("gourmand.gglobals.fgcolor")
    @patch("gourmand.gglobals.bgcolor")
    def test_dark_mode_link_color(self, dark_bgcolor, fgcolor):
        # Closer to 0 is darker.  So in dark mode the background
        # will be a smaller value than the foreground color.
        fgcolor.red = 1
        fgcolor.green = 1
        fgcolor.blue = 1
        dark_bgcolor.red = 0.18
        dark_bgcolor.green = 0.18
        dark_bgcolor.blue = 0.19
        link_color_actual, star_color_actual = \
            get_link_and_star_color(dark_bgcolor, fgcolor)
        self.assertEqual("deeppink", link_color_actual)
        self.assertEqual("gold", star_color_actual)

    @patch("gourmand.gglobals.fgcolor")
    @patch("gourmand.gglobals.bgcolor")
    def test_light_mode_link_color(self, light_bgcolor, fgcolor):
        # Closer to 0 is darker.  So in light mode the background
        # will be a larger value than the foreground color.
        fgcolor.red = 0.13
        fgcolor.green = 0.13
        fgcolor.blue = 0.13
        light_bgcolor.red = 1
        light_bgcolor.green = 1
        light_bgcolor.blue = 1
        link_color_actual, star_color_actual = \
            get_link_and_star_color(light_bgcolor, fgcolor)
        self.assertEqual("blue", link_color_actual)
        self.assertEqual("blue", star_color_actual)
