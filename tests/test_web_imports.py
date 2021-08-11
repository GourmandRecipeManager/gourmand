import gi
import pytest

gi.require_version("Gtk", "3.0")
from gourmand.plugins.web_imports import load  # noqa

@pytest.mark.parametrize(
    'urls, expected_pass, expected_fails',
    [
        ([], [], []),
        (['https://something.example.com/recipe.html'],
         [], 
         ['https://something.example.com/recipe.html']
        ),
        (['https://something.example.com/recipe.html',
          'https://www.allrecipes.com/recipe/17981/one-bowl-chocolate-cake-iii/'],
          ['https://www.allrecipes.com/recipe/17981/one-bowl-chocolate-cake-iii/'], 
         ['https://something.example.com/recipe.html']
        ),
     ],
)
def test_clipboard_exporter(urls, expected_pass, expected_fails):
    recipes, failures = load(urls)

    assert recipes == expected_pass
    assert failures == expected_fails
