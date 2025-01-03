import os
import os.path
import tempfile
import time
import unittest

import gourmand.backends.db
import gourmand.gglobals
import gourmand.GourmetRecipeManager
from gourmand.importers import importManager

tmpdir = tempfile.mktemp()
os.makedirs(tmpdir)
gourmand.gglobals.gourmetdir = tmpdir


gourmand.backends.db.RecData.__single = None
gourmand.GourmetRecipeManager.GourmetApplication.__single = None


class TestImports(unittest.TestCase):
    def setUp(self):
        self.im = importManager.get_import_manager()

    def test_plugins(self):
        for pi in self.im.importer_plugins:
            print("I wonder, is there a test for ", pi)
            if hasattr(pi, "get_import_tests"):
                for fn, test in pi.get_import_tests():
                    print("Testing ", test, fn)
                    self.__run_importer_test(fn, test)

    def done_callback(self, *args):
        print("done!")
        self.done = True

    def __run_importer_test(self, fn, test):
        self.done = False
        importer = self.im.import_filenames([fn])[0]
        assert importer, "import_filenames did not return an object"
        while not importer.done:
            time.sleep(0.2)
        print("Done!")
        assert importer.added_recs, "Importer did not have any added_recs (%s,%s)" % (fn, test)
        try:
            test(importer.added_recs, fn)
        except Exception:
            import traceback

            self.assertEqual(1, 2, "Importer test for %s raised error %s" % ((fn, test), traceback.format_exc()))
