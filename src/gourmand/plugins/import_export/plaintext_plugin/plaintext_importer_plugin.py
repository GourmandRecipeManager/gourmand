import fnmatch
import os.path

from gi.repository import Gtk

from gourmand import check_encodings
from gourmand.i18n import _
from gourmand.importers.importer import Tester
from gourmand.importers.interactive_importer import InteractiveImporter
from gourmand.plugin import ImporterPlugin
from gourmand.threadManager import get_thread_manager

MAX_PLAINTEXT_LENGTH = 100000


class PlainTextImporter (InteractiveImporter):

    name = 'Plain Text Importer'

    def __init__(self, filename):
        self.filename = filename
        InteractiveImporter.__init__(self)

    def do_run(self):
        if os.path.getsize(self.filename) > MAX_PLAINTEXT_LENGTH*16:
            del data
            import gourmand.gtk_extras.dialog_extras as de
            de.show_message(title=_('Big File'),
                            label=_('File %s is too big to import' %
                                    self.filename),
                            sublabel=_('Your file exceeds the maximum length of %s characters. You probably didn\'t mean to import it anyway. If you really do want to import this file, use a text editor to split it into smaller files and try importing again.') % MAX_PLAINTEXT_LENGTH,
                            message_type=Gtk.MessageType.ERROR)
            return
        with open(self.filename, 'rb') as ifi:
            data = '\n'.join(check_encodings.get_file(ifi))
        self.set_text(data)
        return InteractiveImporter.do_run(self)


class PlainTextImporterPlugin (ImporterPlugin):

    name = _('Plain Text file')
    patterns = ['*.txt', '[^.]*', '*']
    mimetypes = ['text/plain']

    antipatterns = ['*.html', '*.htm', '*.xml', '*.doc', '*.rtf']

    def test_file(self, filename):
        '''Given a filename, test whether the file is of this type.'''
        if filename.endswith('.txt'):
            return 1
        elif True not in [fnmatch.fnmatch(filename, p) for p in self.antipatterns]:
            return -1  # we are a fallback option

    def get_importer(self, filename):
        return PlainTextImporter(filename=filename)
