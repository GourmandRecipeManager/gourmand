from gourmand.i18n import _
from gourmand.importers.importer import Tester
from gourmand.plugin import ImporterPlugin

from . import krecipe_importer


class KrecipeImporterPlugin(ImporterPlugin):

    name = _("KRecipe XML File")
    patterns = ["*.xml", "*.kreml"]
    mimetypes = ["text/xml", "application/xml", "text/plain"]

    def test_file(self, filename):
        return Tester(".*<krecipes.*[> ]").test(filename)

    def get_importer(self, filename):
        return krecipe_importer.Converter(filename)
