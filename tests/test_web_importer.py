import unittest
from unittest.mock import Mock, patch

import gi
import pytest
from recipe_scrapers._exceptions import SchemaOrgException

from gourmand.importers.web_importer import (
    import_urls,
    initialize_recipe,  # noqa: E402
)

gi.require_version("Gtk", "3.0")


@pytest.mark.parametrize(
    "urls, expected_pass, expected_fails",
    [
        ([], 0, []),
        (["https://something.example.com/recipe.html"], 0, ["https://something.example.com/recipe.html"]),
        (
            ["https://something.example.com/recipe.html", "https://www.allrecipes.com/recipe/17981/one-bowl-chocolate-cake-iii/"],
            1,
            ["https://something.example.com/recipe.html"],
        ),
    ],
)
def test_import_urls(tmp_path, urls, expected_pass, expected_fails):
    with patch("gourmand.gglobals.gourmanddir", tmp_path):
        recipes, failures = import_urls(urls)

    assert len(recipes) == expected_pass
    assert failures == expected_fails


class TestWebImporter(unittest.TestCase):

    def test_no_rating_gets_set_to_zero(self):
        recipe_scrape_mock = Mock()
        recipe_scrape_mock.ratings.side_effect = SchemaOrgException("Error")
        recipe_scrape_mock.yields.return_value = ('5 muffins')

        recipe = initialize_recipe(recipe_scrape_mock)
        self.assertEqual(0, recipe.rating)
