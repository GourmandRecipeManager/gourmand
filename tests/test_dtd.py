from pathlib import Path
from unittest import TestCase

from lxml import etree

EXAMPLE_FILE = Path(__file__).parent / "recipe_files" / "test_set.grmt"
DTD_FILE = Path(__file__).parent.parent / "src/gourmand/data/recipe.dtd"

class TestDtd(TestCase):

    def setUp(self):
        self.dtd = etree.DTD(DTD_FILE)

    def test_dtd_validates_example(self):
        example = etree.parse(EXAMPLE_FILE)
        assert self.dtd.validate(example)
