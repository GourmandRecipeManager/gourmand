import unittest

from gourmand.importers import importer


class TestImporter(unittest.TestCase):

    def setUp(self):
        self.i = importer.Importer()

    def _get_last_rec_(self):
        return self.i.added_recs[-1]

    def test_recipe_import(self):
        self.i.start_rec()
        attrs = [("title", "Foo"), ("cuisine", "Bar"), ("yields", 3), ("yield_unit", "cups")]
        for att, val in attrs:
            self.i.rec[att] = val
        self.i.commit_rec()
        rec = self._get_last_rec_()
        for att, val in attrs:
            self.assertEqual(getattr(rec, att), val)

    def test_ingredient_import(self):
        self.i.start_rec()
        self.i.rec["title"] = "Ingredient Import Test"
        self.i.start_ing()
        self.i.add_amt(2)
        self.i.add_unit("cups")
        self.i.add_item("water")
        self.i.commit_ing()
        self.i.commit_rec()
        ings = self.i.rd.get_ings(self._get_last_rec_())
        self.assertEqual(len(ings), 1)
        ing = ings[0]
        self.assertEqual(ing.amount, 2)
        self.assertEqual(ing.unit, "cups")
        self.assertEqual(ing.item, "water")


class ImporterTest(unittest.TestCase):

    def setUp(self):
        self.importer = importer.Importer()

    def test_parse_simple_yields(self):
        assert self.importer.parse_yields("3 cups") == (3, "cups")
        assert self.importer.parse_yields("7 servings") == (7, "servings")
        assert self.importer.parse_yields("12 muffins") == (12, "muffins")
        assert self.importer.parse_yields("10 loaves") == (10, "loaves")

    def test_parse_complex_yields(self):
        assert self.importer.parse_yields("Makes 12 muffins") == (12, "muffins")
        assert self.importer.parse_yields("Makes 4 servings") == (4, "servings")
        assert self.importer.parse_yields("Serves 7") == (7, "servings")

    def test_parse_fractional_yields(self):
        assert self.importer.parse_yields("Makes 4 3/4 muffins") == (4.75, "muffins")
        assert self.importer.parse_yields("Makes 4 3/4") == (4.75, "servings")
        assert self.importer.parse_yields("19/4") == (4.75, "servings")
        assert self.importer.parse_yields("Makes 19/4") == (4.75, "servings")

    @unittest.expectedFailure
    def test_failed_parsing_fractional_yields(self):
        assert self.importer.parse_yields("Makes 19/4") == (4.75, "muffins")


class RatingConverterTest(unittest.TestCase):

    def setUp(self):

        class FakeDB:

            recs = dict([(n, {}) for n in range(20)])

            def get_rec(self, n):
                return n

            def modify_rec(self, n, d):
                for attr, val in list(d.items()):
                    self.recs[n][attr] = val

        self.db = FakeDB()

    def test_automatic_converter(self):
        rc = importer.RatingConverter()
        tests = [("good", 6), ("Great", 8), ("Excellent", 10), ("poor", 2), ("okay", 4)]
        for n, (rating, number) in enumerate(tests):
            rc.add(n, rating)
            self.db.recs[n]["rating"] = rating
        rc.do_conversions(self.db)
        print("Conversions: ")
        for n, (rating, number) in enumerate(tests):
            print("Converted", rating, "->", self.db.recs[n]["rating"])
            self.assertEqual(number, self.db.recs[n]["rating"])

    def test_string_to_rating_converter(self):
        assert importer.string_to_rating("4/5 stars") == 8
        assert importer.string_to_rating("3 1/2 / 5 stars") == 7
        assert importer.string_to_rating("4/10 stars") == 4
