# -*- coding: utf-8 -*-

import os
import os.path

from gi.repository import Pango

from gourmand.i18n import _
from gourmand.importers.importer import Tester
from gourmand.plugin import ImporterPlugin
from gourmand.recipeManager import get_recipe_manager

from . import gxml2_importer, gxml_importer

test_dir = os.path.split(__file__)[0]  # our directory src/lib/plugins/import_export/plugin/*/
test_dir = os.path.split(test_dir)[0]  # one back... src/lib/plugins/import_export/plugin/
test_dir = os.path.split(test_dir)[0]  # one back... src/lib/plugins/import_export/
test_dir = os.path.split(test_dir)[0]  # one back... src/lib/plugins/
test_dir = os.path.join(test_dir, "tests", "recipe_files")


class GxmlImportTester:

    def __init__(self):
        self.rm = get_recipe_manager()

    def run_test(self, recipe_objects, filename):
        if filename.endswith("test_set.grmt"):
            self.run_test_set_test(recipe_objects)

    def run_test_set_test(self, recs):
        assert "Amazing rice" in [r.title for r in recs], "Titles were: %s" % ([r.title for r in recs])
        rice = recs[0]
        if rice.title != "Amazing rice":
            rice = recs[1]
            sauce = recs[0]
        else:
            sauce = recs[1]
        assert sauce.source == "Tom's imagination", "value was %s" % sauce.source
        assert sauce.link == "http://slashdot.org", "value was %s" % sauce.link
        ings = self.rm.get_ings(rice)
        assert ings[1].refid == sauce.id, "Ingredient reference did not export properly"
        sings = self.rm.get_ings(sauce)
        assert sings[1].inggroup == "veggies", "value was %s" % sings[0].inggroup
        assert sings[1].item == "jalapeño peppers", 'value was "%s",%s' % (sings[1].item, type(sings[1].item))
        self.is_markup_valid(sauce)
        self.is_markup_valid(rice)
        assert "<i>well" in sauce.instructions, "value was %s" % sauce.instructions
        assert sauce.image
        assert sauce.thumb

    def is_markup_valid(self, rec):
        Pango.parse_markup(rec.instructions or "")
        Pango.parse_markup(rec.modifications or "")


class GourmetXML2Plugin(ImporterPlugin):

    name = _("Gourmet XML File")
    patterns = ["*.xml", "*.grmt", "*.gourmet"]
    mimetypes = ["text/xml", "application/xml", "text/plain"]

    def test_file(self, filename):
        return Tester(".*<gourmetDoc[> ]").test(filename)

    def get_importer(self, filename):
        return gxml2_importer.Converter(filename)


class GourmetXMLPlugin(ImporterPlugin):

    name = _("Gourmet XML File (Obsolete)")
    patterns = ["*.xml", "*.grmt", "*.gourmet"]
    mimetypes = ["text/xml", "application/xml", "text/plain"]

    def test_file(self, filename):
        return Tester(".*<recipeDoc[> ]").test(filename)

    def get_importer(self, filename):
        return gxml_importer.Converter(filename)

    def get_import_tests(self):
        """Return an alist with files to check and tester functions
        that will be run to test the imported recipes. The function
        will be called with the following signature

        tester(recipe_objects, filename, rd)
        """
        return [
            (os.path.join(test_dir, "test_set.grmt"), GxmlImportTester().run_test),
        ]
