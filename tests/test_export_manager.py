import sys
import tempfile
import unittest
from pathlib import Path

import gourmand.backends.db
import gourmand.gglobals
import gourmand.main
from gourmand.exporters.exportManager import EXTRA_PREFS_DEFAULT, ExportManager


class SampleRecipeSetterUpper:

    __single = None

    @classmethod
    def instance(cls):
        if SampleRecipeSetterUpper.__single is None:
            SampleRecipeSetterUpper.__single = cls()

        return SampleRecipeSetterUpper.__single

    recipes = {
        "simple recipe": {
            "recipe": {
                "title": "Simple Test",
                "cuisine": "Indian",
                "instructions": "Cook as usual",
                "modifications": "Unless you want to get fancy",
                "preptime": 3600,
                "cooktime": 11239,
            },
            "categories": ["Healthy", "Bread"],
            "ingredients": [
                {"amount": 1, "unit": "cup", "item": "water", "ingkey": "water, municipal"},
                {"amount": 2, "unit": "cups", "item": "atta flour", "ingkey": "flour, atta (whole wheat)"},
                {"amount": 2, "unit": "Tbs", "item": "salt", "ingkey": "salt, table"},
                {"amount": 1, "unit": "tsp", "item": "black pepper", "ingkey": "pepper, black", "optional": True},
            ],
        },
        "unicode": {
            "recipe": {"title": "¡Jalapeño extravaganza!", "yields": 3, "yield_unit": "cups"},
            "categories": ["Spicy", "Healthy"],
            "ingredients": [
                {"amount": 1, "unit": "cup", "item": "water", "ingkey": "water, municipal"},
                {"amount": 1, "unit": "lb", "item": "jalapeño", "ingkey": "pepper, habañero"},
                {"amount": 2, "unit": "más", "item": "habañeros", "ingkey": "pepper, habañero"},
            ],
        },
        "formatting": {
            "recipe": {
                "title": "Recipe with formatting",
                "instructions": """These are my <i>instructions</i> I would like to <b>see</b> what you <u>think</u> of them.

<span color="red">Aren\'t these pretty nifty?</span>""",
                "modifications": """These are my <i>notes</i> I would like to <b>see</b> what you <u>think</u> of them.

<span color="blue">Aren\'t these pretty nifty?</span>""",
            },
            "ingredients": [
                {"amount": 1, "unit": "cup", "item": "water", "ingkey": "water, municipal"},
                {"amount": 1, "unit": "lb", "item": "jalapeño", "ingkey": "pepper, habañero"},
                {"amount": 2, "unit": "más", "item": "habañeros", "ingkey": "pepper, habañero"},
            ],
        },
    }

    def __init__(self):
        self.db = gourmand.backends.db.get_database()
        for rec in self.recipes:
            self.add_rec(self.recipes[rec])

    def add_rec(self, recdic):
        recdic["recipe"]["deleted"] = False
        r = self.db.add_rec(recdic["recipe"])
        recid = r.id
        print("added rec", r.id)
        recdic["recipe_id"] = r.id
        if "categories" in recdic:
            for c in recdic["categories"]:
                print("add categories", c)
                self.db.do_add_cat({"recipe_id": recid, "category": c})
        if "ingredients" in recdic:
            print("Add ingredients...")
            for i in recdic["ingredients"]:
                i["recipe_id"] = recid
                i["deleted"] = False
                print(i)
            self.db.add_ings(recdic["ingredients"])
        print("done add_rec\n-------")
        rec = self.db.get_rec(recdic["recipe_id"])
        print(rec)
        print(self.db.get_cats(rec))
        print(self.db.get_ings(rec))
        print("^^^^^^^^^^^^^^^^^^^^")


def setup_sample_recs():
    # FIXME: We're instantiating this class for side effects. Rethink that.
    return SampleRecipeSetterUpper.instance()


class TestExportManager(unittest.TestCase):
    def setUp(self):
        print("start setUp", file=sys.stderr)
        self.sample_recs = setup_sample_recs()
        self.recs = self.sample_recs.recipes
        print("in setUp 1", file=sys.stderr)
        self.em = ExportManager.instance()
        print("in setUp 2", file=sys.stderr)
        self.db = gourmand.backends.db.get_database()
        print("finish setUp", file=sys.stderr)

    def test_multiple_exporters(self):
        def fail_on_fail(thread, errorval, errortext, tb):
            self.assertTrue(False, errortext + "\n\n" + tb)

        for format_name, plugin in list(self.em.plugins_by_name.items()):
            print(format_name, file=sys.stderr)
            filters = plugin.saveas_filters
            ext = filters[-1][-1].strip("*.")
            recs = [
                self.db.get_rec(self.recs["simple recipe"]["recipe_id"]),
                self.db.get_rec(self.recs["unicode"]["recipe_id"]),
                self.db.get_rec(self.recs["formatting"]["recipe_id"]),
            ]
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory, "All." + ext)
                plugin, exporter = self.em.get_multiple_exporter(recs, str(path), format_name, extra_prefs=EXTRA_PREFS_DEFAULT)
                exporter.connect("error", fail_on_fail)
                exporter.do_run()

    def test_single_export(self):
        for format_name, plugin in list(self.em.plugins_by_name.items()):
            filters = plugin.saveas_single_filters
            ext = filters[-1][-1].strip("*.")
            for rec, f in [
                (self.db.get_rec(self.recs["simple recipe"]["recipe_id"]), "Simple." + ext),
                (self.db.get_rec(self.recs["unicode"]["recipe_id"]), "Uni." + ext),
                (self.db.get_rec(self.recs["formatting"]["recipe_id"]), "Formatted." + ext),
            ]:
                with tempfile.TemporaryDirectory() as directory:
                    Path(directory, f + ext)
                    self.em.do_single_export(rec, f, format_name, extra_prefs=EXTRA_PREFS_DEFAULT)
                    if hasattr(plugin, "check_export"):
                        print("Checking export for ", plugin, rec, f)
                        fi = open(f, "r")
                        try:
                            plugin.check_export(rec, fi)
                        except Exception:
                            import traceback

                            self.assertEqual(1, 2, "Exporter test for %s on file %s raised error %s" % (plugin, f, traceback.format_exc()))
                        finally:
                            fi.close()
