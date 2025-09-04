import unittest
from unittest.mock import Mock, patch

from gourmand.gglobals import _get_link_and_star_color


class TestLinkColor(unittest.TestCase):

    def setUp(self):
        pass

    @patch("gourmand.gglobals.Gtk")
    def test_dark_mode_link_color(self, Gtk):
        # Closer to 0 is darker.  So in dark mode the background
        # will be a smaller value than the foreground color.
        dark_bgcolor = Mock()
        fgcolor = Mock()
        Gtk.TextView().get_style_context().get_background_color.return_value = dark_bgcolor
        Gtk.TextView().get_style_context().get_color.return_value = fgcolor
        fgcolor.red, fgcolor.green, fgcolor.blue = (1, 1, 1)
        dark_bgcolor.red, dark_bgcolor.green, dark_bgcolor.blue = (0.18, 0.18, 0.19)
        link_color_actual, star_color_actual = _get_link_and_star_color()
        self.assertEqual("deeppink", link_color_actual)
        self.assertEqual("gold", star_color_actual)

    @patch("gourmand.gglobals.Gtk")
    def test_light_mode_link_color(self, Gtk):
        # Closer to 0 is darker.  So in light mode the background
        # will be a larger value than the foreground color.
        light_bgcolor = Mock()
        fgcolor = Mock()
        Gtk.TextView().get_style_context().get_background_color.return_value = light_bgcolor
        Gtk.TextView().get_style_context().get_color.return_value = fgcolor
        fgcolor.red, fgcolor.green, fgcolor.blue = (0.13, 0.13, 0.13)
        light_bgcolor.red, light_bgcolor.green, light_bgcolor.blue = (1, 1, 1)
        link_color_actual, star_color_actual = _get_link_and_star_color()
        self.assertEqual("blue", link_color_actual)
        self.assertEqual("blue", star_color_actual)
