import locale

from gi.repository import Gtk
from gtkspellcheck import SpellChecker

from gourmand.plugin import RecEditorPlugin, UIPlugin


def harvest_textviews(widget):
    if isinstance(widget, Gtk.TextView):
        return [widget]
    else:
        tvs = []
        if hasattr(widget, 'get_children'):
            for child in widget.get_children():
                tvs.extend(harvest_textviews(child))
        elif hasattr(widget, 'get_child'):
            tvs.extend(harvest_textviews(widget.get_child()))
        return tvs


class SpellPlugin(RecEditorPlugin, UIPlugin):

    main = None

    ui_string = ''

    def activate(self, editor):
        UIPlugin.activate(self, editor)
        language, _ = locale.getlocale()
        for module in self.pluggable.modules:
            tvs = harvest_textviews(module.main)
            for tv in tvs:
                SpellChecker(tv, language=language)
