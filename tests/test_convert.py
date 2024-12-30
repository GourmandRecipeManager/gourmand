import unittest

import pytest

from gourmand import convert


class ConvertTest(unittest.TestCase):

    def setUp(self):
        self.c = convert.get_converter()

    def test_equal(self):
        self.assertEqual(self.c.convert_simple("c", "c"), 1)

    @pytest.mark.skip("Broken as of 20220813")
    def test_density(self):
        self.assertEqual(self.c.convert_w_density("ml", "g", item="water"), 1)
        self.assertEqual(self.c.convert_w_density("ml", "g", density=0.5), 0.5)

    def test_readability(self):
        self.assertTrue(self.c.readability_score(1, "cup") > self.c.readability_score(0.8, "cups"))
        self.assertTrue(self.c.readability_score(1 / 3.0, "tsp.") > self.c.readability_score(0.123, "tsp."))

    def test_adjustments(self):
        amt, unit = self.c.adjust_unit(12, "Tbs.", "water")
        self.assertEqual(amt, 0.75)

    def test_integer_rounding(self):
        self.assertTrue(convert.integerp(0.99))

    def test_fraction_generator(self):
        for d in [2, 3, 4, 5, 6, 8, 10, 16]:
            self.assertEqual(convert.float_to_frac(1.0 / d, fractions=convert.FRACTIONS_ASCII), ("1/%s" % d))

    def test_fraction_to_float(self):
        for s, n in [
            ("1", 1),
            ("123", 123),
            ("1 1/2", 1.5),
            # ("74 2/5", 74.4),  # TODO: Broken.
            ("1/10", 0.1),
            ("one", 1),
            ("a half", 0.5),
            ("three quarters", 0.75),
        ]:
            self.assertEqual(convert.frac_to_float(s), n)

    @pytest.mark.skip("Broken as of 20220813")
    def test_ingmatcher(self):
        for s, a, u, i in [
            ("1 cup sugar", "1", "cup", "sugar"),
            ("1 1/2 cup sugar", "1 1/2", "cup", "sugar"),
            ("two cloves garlic", "two", "cloves", "garlic"),
        ]:
            match = convert.ING_MATCHER.match(s)
            self.assertTrue(match)
            self.assertEqual(match.group(convert.ING_MATCHER_AMT_GROUP).strip(), a)
            self.assertEqual(match.group(convert.ING_MATCHER_UNIT_GROUP).strip(), u)
            self.assertEqual(match.group(convert.ING_MATCHER_ITEM_GROUP).strip(), i)
