"""This test may leave marks in the user preferences file."""

from unittest import mock

from gourmand.plugins.import_export.pdf_plugin.pdf_exporter import PdfPrefGetter


def test_get_args_from_opts(tmp_path):
    with mock.patch("gourmand.gglobals.gourmanddir", tmp_path):
        pref_getter = PdfPrefGetter()

        options = (
            ["Paper _Size:", "Letter"],
            ["_Orientation:", "Portrait"],
            ["_Font Size:", 42],
            ["Page _Layout", "Plain"],
            ["Left Margin:", 70.86614173228347],
            ["Right Margin:", 70.86614173228347],
            ["Top Margin:", 70.86614173228347],
            ["Bottom Margin:", 70.86614173228347],
        )

        expected = {
            "pagesize": "letter",
            "pagemode": "portrait",
            "base_font_size": 42,
            "mode": ("column", 1),
            "left_margin": 70.86614173228347,
            "right_margin": 70.86614173228347,
            "top_margin": 70.86614173228347,
            "bottom_margin": 70.86614173228347,
        }

        ret = pref_getter.get_args_from_opts(options)

        assert ret == expected
