import re
import unittest
from pathlib import Path

from gourmand.backends.db import RecipeManager
from gourmand.importers.importManager import ImportFileList, ImportManager
from gourmand.plugins.import_export.mastercook_import_plugin.mastercook_plaintext_importer import Tester as MCTester

TEST_FILE_DIRECTORY = Path(__file__).parent / "recipe_files"


class ThreadlessImportManager(ImportManager):
    def get_app_and_prefs(self):
        self.prefs = {}

    def do_import(self, importer_plugin, method, *method_args):
        # No threading, for profiling purposes!
        try:
            importer = getattr(importer_plugin, method)(*method_args)
        except ImportFileList as ifl:
            # recurse with new filelist...
            self.import_filenames(ifl.filelist)
        else:
            if hasattr(importer, "pre_run"):
                importer.pre_run()
            importer.run()
            self.follow_up(None, importer)


class ImportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.im = ThreadlessImportManager.instance()
        cls.db = RecipeManager.instance_for()

    def run_test(self, d):
        self.db.delete_by_criteria(self.db.recipe_table, {"title": d["test"]["title"]})
        filename = str(TEST_FILE_DIRECTORY / d["filename"])
        self.im.import_filenames([filename])
        self.do_test(d["test"])

    def do_test(self, test):
        recs = self.db.search_recipes([{"column": "deleted", "search": False, "operator": "="}, {"column": "title", "search": test["title"], "operator": "="}])
        assert recs, 'No recipe found with title "%s".' % test["title"]
        rec = recs[0]
        ings = self.db.get_ings(rec)
        if test.get("all_ings_have_amounts", False):
            for i in ings:
                assert i.amount, (i, i.amount, i.unit, i.item, "has no amount!")
        if test.get("all_ings_have_units", False):
            for i in ings:
                assert i.unit, (i, i.amount, i.unit, i.item, "has no unit")
        for blobby_attribute in ["instructions", "modifications"]:
            if test.get(blobby_attribute, False):
                match_text = test[blobby_attribute]

                assert re.match(match_text, getattr(rec, blobby_attribute)), "%s == %s != %s" % (blobby_attribute, getattr(rec, blobby_attribute), match_text)
        for non_blobby_attribute in ["source", "cuisine", "preptime", "cooktime"]:
            if test.get(non_blobby_attribute, None) is not None:
                assert getattr(rec, non_blobby_attribute) == test[non_blobby_attribute], "%s == %s != %s" % (
                    non_blobby_attribute,
                    getattr(rec, non_blobby_attribute),
                    test[non_blobby_attribute],
                )
        if test.get("categories", None):
            cats = self.db.get_cats(rec)
            for c in test.get("categories"):
                assert c in cats, "Found no category %s, only %s" % (c, cats)
                cats.remove(c)
            assert not cats, "Categories include %s not specified in %s" % (cats, test["categories"])
        print("Passed test:", test)

    def run_test_2(self, d):
        self.db.delete_by_criteria(self.db.recipe_table, {"title": d["test"]["title"]})
        filename = str(TEST_FILE_DIRECTORY / d["filename"])
        self.im.import_filenames([filename])
        self.do_test_2(d["test"])

    def do_test_2(self, test):
        recs = self.db.search_recipes([{"column": "deleted", "search": False, "operator": "="}, {"column": "title", "search": test["title"], "operator": "="}])
        assert recs, 'No recipe found with title "%s".' % test["title"]
        rec = recs[0]
        for blobby_attribute in ["instructions", "modifications"]:
            if test.get(blobby_attribute, False):
                match_text = test[blobby_attribute]
                assert match_text == getattr(rec, blobby_attribute)


    def progress(self, bar, msg):
        pass


    def test_mastercook(self):
        self.run_test(
            {
                "filename": "athenos1.mx2",
                "test": {
                    "title": "5 Layer Mediterranean Dip",
                    "all_ings_have_amounts": True,
                    "all_ings_have_units": True,
                },
            }
        )


    def test_mealmaster(self):
        self.run_test(
            {
                "filename": "mealmaster.mmf",
                "test": {
                    "title": "Almond Mushroom Pate",
                    "categories": ["Appetizers"],
                    "servings": 6,
                },
            }
        )


    def test_krecipes(self):
        self.run_test(
            {
                "filename": "sample.kreml",
                "test": {
                    "title": "Recipe title",
                    "source": "Unai Garro, Jason Kivlighn",
                    "categories": ["Ethnic", "Cakes"],
                    "servings": 5,
                    "preptime": 90 * 60,
                    "instructions": "Write the recipe instructions here",
                },
            }
        )


    def test_mycookbook(self):
        self.run_test(
            {
                "filename": "mycookbook.mcb",
                "test": {
                    "title": "Best Brownies",
                    "link": "https://www.allrecipes.com/recipe/10549/best-brownies/",
                },
            }
        )


    def test_grmt_formatting_and_special_chars(self):
        self.run_test_2(
            {
                "filename": "special_chars.grmt",
                "test": {
                    "title": "Yes special characters - Origx2",
                    "instructions": '<b>less than bold &lt;</b>\n<i>greater than italic &gt;</i>\n<u>ampersand underlined &amp;</u>\nAll 10 symbols above <u>nu\
mbers </u><u><b>!@#</b></u><u><i>$%</i></u><u><b>^&amp;*()</b></u>',
                },
            }
        )


def test_mastercook_file_tester():
    filename = TEST_FILE_DIRECTORY / "mastercook_text_export.mxp"
    tester = MCTester()
    assert tester.test(filename)
