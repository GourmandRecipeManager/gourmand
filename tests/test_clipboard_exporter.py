from collections import namedtuple  # noqa: E402

import gi
import pytest

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk, Gtk  # noqa: E402

from gourmand.exporters.clipboard_exporter import copy_to_clipboard  # noqa: E402

Recipe = namedtuple("Recipe", ["title", "source", "yields", "yield_unit", "description", "instructions", "link"])

recipe1 = Recipe("Title1", "Source1", 700.0, "g.", None, "Make the Dough.", "")
recipe2 = Recipe("Title2", "Source2", 2, "litres", "test", "Directions.", "https://example.com")

Ingredient = namedtuple("Ingredient", ["amount", "unit", "item"])

ingredients1 = (Ingredient(600, "g.", "flour"),)
ingredients2 = (Ingredient(600, "g.", "flour"), Ingredient(2, "l.", "water"))

recipe_input = [(recipe1, ingredients1)]
recipe_expected_output = """# Title1

Source1

700.0 g.

600 g. flour

Make the Dough.
"""

two_recipes_input = [(recipe1, ingredients1), (recipe2, ingredients2)]

two_recipes_expected_output = """# Title1

Source1

700.0 g.

600 g. flour

Make the Dough.


# Title2

Source2
https://example.com

2 litres

test

600 g. flour
2 l. water

Directions.
"""


@pytest.mark.parametrize(
    "recipes, expected",
    [
        ([], ""),
        (recipe_input, recipe_expected_output),
        (two_recipes_input, two_recipes_expected_output),
    ],
)
def test_clipboard_exporter(recipes, expected):
    copy_to_clipboard(recipes)

    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    assert clipboard.wait_for_text() == expected
