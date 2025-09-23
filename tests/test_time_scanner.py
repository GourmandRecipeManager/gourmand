import unittest

from gourmand.timeScanner import make_time_links


class TimeScannerTest(unittest.TestCase):
    def test_single_time(self):
        text = "Bake for 15 minutes or until slightly brown."
        expected = 'Bake for <a href="15 minutes">15 minutes</a> or until slightly brown.'
        result = make_time_links(text)
        self.assertEqual(expected, result)

    def test_multiple_single_time(self):
        text = "Bake for 15 minutes or until slightly brown. Refrigerate 3 hours, until cooled."
        expected = 'Bake for <a href="15 minutes">15 minutes</a> or until slightly brown. Refrigerate <a href="3 hours">3 hours</a>, until cooled.'
        result = make_time_links(text)
        self.assertEqual(expected, result)

    def test_time_range_with_to(self):
        text = "Bake for 15 to 20 minutes."
        expected = 'Bake for <a href="15 minutes">15 to </a><a href="20 minutes">20 minutes</a>.'
        result = make_time_links(text)
        self.assertEqual(expected, result)

    def test_time_range_with_dash_no_spaces(self):
        text = "Bake for 15-20 minutes."
        expected = 'Bake for <a href="15 minutes">15-</a><a href="20 minutes">20 minutes</a>.'
        result = make_time_links(text)
        self.assertEqual(expected, result)

    def test_time_range_with_dash_with_spaces(self):
        text = "Bake for 15 - 20 minutes."
        expected = 'Bake for <a href="15 minutes">15 - </a><a href="20 minutes">20 minutes</a>.'
        result = make_time_links(text)
        self.assertEqual(expected, result)

    def test_time_range_multiple_types(self):
        text = ("Mix cream cheese, sugar and vanilla with electric mixer on "
                "medium speed until well blended.  Add eggs; mix until blended."
                "  Stir in white chocolate.  Pour into crust.\nMicrowave "
                "preserves in small bowl on HIGH 15 seconds or until melted.  "
                "Dot top of cheesecake with small spoonfuls of preserves.  Cut "
                "through batter with knife several times for marble effect.\n"
                "Bake at 350 degrees for 35 to 40 minutes or until center is "
                "almost set.  Cool.  Refrigerate 3 hours or overnight.\nThis "
                "recipe yields 8 servings.\nGreat Substitute:  To lower the "
                "fat, prepare as directed, substituting Philadelphia Neufchatel"
                " Cheese, 1/3 Less Fat than Cream Cheese, for cream cheese.")
        expected = ('Mix cream cheese, sugar and vanilla with electric mixer on'
                    ' medium speed until well blended.  Add eggs; mix until '
                    'blended.  Stir in white chocolate.  Pour into crust.\n'
                    'Microwave preserves in small bowl on HIGH <a href="15 '
                    'seconds">15 seconds</a> or until melted.  Dot top of '
                    'cheesecake with small spoonfuls of preserves.  Cut through'
                    ' batter with knife several times for marble effect.\nBake '
                    'at 350 degrees for <a href="35 minutes">35 to </a><a href='
                    '"40 minutes">40 minutes</a> or until center is almost set.'
                    '  Cool.  Refrigerate <a href="3 hours">3 hours</a> or '
                    'overnight.\nThis recipe yields 8 servings.\nGreat '
                    'Substitute:  To lower the fat, prepare as directed, '
                    'substituting Philadelphia Neufchatel Cheese, 1/3 Less Fat '
                    'than Cream Cheese, for cream cheese.')
        result = make_time_links(text)
        self.assertEqual(expected, result)
