import gi

gi.require_version("Gtk", "3.0")
from gourmand.plugins.web_imports import load  # noqa

print(load(['https://www.allrecipes.com/recipe/17981/one-bowl-chocolate-cake-iii/']))
