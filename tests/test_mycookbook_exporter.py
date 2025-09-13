import unittest

from gourmand.plugins.import_export.mycookbook_plugin.mycookbook_exporter import sanitize_image_name


class RectoMCBTest(unittest.TestCase):
    def test_sanitize_image_name(self):
        input_name = "Brownies w/ caram/el"
        result = sanitize_image_name(input_name)
        self.assertEqual("Brownies with caramel", result)


if __name__ == '__main__':
    unittest.main()
