import unittest

from gourmand.plugins.import_export.mycookbook_plugin.mycookbook_exporter import rec_to_mcb


class RectoMCBTest(unittest.TestCase):
    def test_sanitized_name(self):
        input = "Brownies w/ caram/el"
        result = rec_to_mcb.sanitize_image_name(rec_to_mcb, input)
        self.assertNotIn('/', result)  # add assertion here


if __name__ == '__main__':
    unittest.main()
