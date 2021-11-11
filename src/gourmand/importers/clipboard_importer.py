"""Import recipes using the system's clipboard or via drag and drop."""
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import urlparse

from gi.repository import Gdk, Gtk

from gourmand.importers.importManager import ImportManager
from gourmand.plugins.import_export.plaintext_plugin.plaintext_importer_plugin import PlainTextImporter  # noqa


def handle_import(data: str):
    """Deduce the correct importer from the content."""
    if not data:
        return

    # Offer the regular import dialog if it's a uri
    is_supported = False

    uri = urlparse(data)
    if uri.netloc:
        is_supported = True
    elif uri.scheme == 'file' and Path(uri.path).is_file():
        is_supported = True  # The import manager will do file-type validation
        data = uri.path

    if is_supported:
        importer = ImportManager.instance()
        importer.offer_import(default_value=data)

    else:  # offer plaintext import
        with NamedTemporaryFile(delete=False) as tf:
            tf.write(data.encode())
        importer = PlainTextImporter(tf.name)
        importer.do_run()

        from gourmand.main import get_application  # work around circular import
        app = get_application()
        app.redo_search()


def import_from_clipboard(action: Gtk.Action):
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    content = clipboard.wait_for_text().strip()

    handle_import(content)


def import_from_drag_and_drop(treeview: Gtk.Widget,
                              drag_context: Gdk.DragContext,
                              x: int,
                              y: int,
                              data: Gtk.SelectionData,
                              info: int,
                              time: int) -> bool:
    """Handle imports from drag and drop action.

    This function is expected to be connected to a signal.
    If so, the signal will be done being handled here.
    """
    content = data.get_text().strip()
    handle_import(content)
    return True  # Done handling signal
