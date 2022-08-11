from fnmatch import fnmatch
from typing import Any, List, Optional, Tuple
from urllib.parse import urlparse

from gi.repository import Gtk

import gourmand.gtk_extras.dialog_extras as de
import gourmand.plugin_loader as plugin_loader
from gourmand.i18n import _
from gourmand.importers.web_importer import import_urls, supported_sites
from gourmand.importers.interactive_importer import import_interactivally
from gourmand.plugin import ImporterPlugin, ImportManagerPlugin
from gourmand.threadManager import (NotThreadSafe, get_thread_manager,
                                    get_thread_manager_gui)


class ImportFileList (Exception):
    """A special case error -- if an importer throws this error
    instead of returning an importer, our importer will import the
    list of files returned... This is basically a thread-safe way
    around the problem of how to let an importer initiate other
    imports (for zip files etc)"""
    def __init__ (self, filelist):
        self.filelist = filelist


class ImportManager(plugin_loader.Pluggable):

    '''A class to
    manage importers.
    '''

    __single = None

    @classmethod
    def instance(cls):
        if ImportManager.__single is None:
            ImportManager.__single = cls()

        return ImportManager.__single

    def __init__ (self):
        self.tempfiles = {}
        self.extensions_by_mimetype = {}
        self.plugins_by_name = {}
        self.plugins = []
        self.importer_plugins = []
        plugin_loader.Pluggable.__init__(self,
                                         [ImporterPlugin,
                                          ImportManagerPlugin]
                                         )
        self.get_app_and_prefs()

    def get_app_and_prefs(self):
        # FIXME: this function and self.app exist to work around circular imports
        from gourmand.main import get_application
        self.app = get_application()

    def offer_import(self, parent: Optional[Gtk.Window] = None,
                     default_value: Optional[str] = None):
        """Offer to import url or files."""

        uris = de.get_uri(label=_('Open recipe...'),
                          sublabel=_('Enter a recipe file path or website address.'),
                          entryLabel=_('Location:'),
                          entryTip=_('Enter the address of a website or recipe archive.'),
                          default_character_width=60,
                          filters=self.get_filters(),
                          supported_urls=supported_sites,
                          select_multiple=True,
                          default_value=default_value,
                          )
        if uris is None:
            return

        # There should be only a single url
        if urlparse(uris[-1]).netloc:
            supported, unsupported = import_urls(uris)
            if unsupported:
                import_interactivally(unsupported)
        else:
            self.import_filenames(uris)

        self.app.redo_search()  # Trigger a refresh of the recipe tree

    def import_filenames(self, filenames: List[str]) -> List[Any]:
        """Import list of filenames, filenames, based on our currently
        registered plugins.

        Return a list of importers (mostly useful for testing purposes)
        """
        importers = []
        while filenames:
            fn = filenames.pop()
            fallback = None
            found_plugin = False
            for plugin in self.importer_plugins:
                for pattern in plugin.patterns:
                    if fnmatch(fn.upper(),pattern.upper()):
                        result = plugin.test_file(fn)
                        if result==-1: # FALLBACK
                            fallback = plugin
                        elif result:
                            importers.append((fn,plugin))
                            found_plugin = True
                        else:
                            print('File ',fn,'appeared to match ',plugin,'but failed test.')
                        break
                if found_plugin: break
            if not found_plugin:
                if fallback:
                    importers.append((fn,fallback))
                else:
                    print('Warning, no plugin found for file ',fn)
        ret_importers = [] # a list of importer instances to return
        for fn,importer_plugin in importers:
            print('Doing import for ',fn,importer_plugin)
            ret_importers.append(
                self.do_import(importer_plugin,'get_importer',fn)
                )
        print('import_filenames returns',ret_importers)
        return ret_importers

    def do_import(self, importer_plugin: Any,
                  method: str, *method_args: Tuple[str]):
        try:
            importer = getattr(importer_plugin, method)(*method_args)
            self.setup_notification_message(importer)
        except ImportFileList as ifl:
            # recurse with new filelist...
            return self.import_filenames(ifl.filelist)
        else:
            if hasattr(importer, 'pre_run'):
                importer.pre_run()
            if isinstance(importer, NotThreadSafe):
                #print 'Running manually --- not threadsafe!'
                importer.run()
                self.follow_up(None,importer)
            else:
                label = _('Import') + ' ('+importer_plugin.name+')'
                self.setup_thread(importer, label)
            print('do_importer returns importer:',importer)
            return importer

    def setup_notification_message(self, importer):
        tmg = get_thread_manager_gui()
        importer.connect('completed',tmg.importer_thread_done)

    @plugin_loader.pluggable_method
    def follow_up (self, threadmanager, importer):
        if hasattr(importer,'post_run'):
            importer.post_run()

    def setup_thread (self, importer, label, connect_follow_up=True):
        tm = get_thread_manager()
        tm.add_thread(importer)
        tmg = get_thread_manager_gui()
        tmg.register_thread_with_dialog(label,
                                        importer)
        if connect_follow_up:
            importer.connect('completed',
                             self.follow_up,
                             importer
                             )

    def get_importer (self, name):
        return self.plugins_by_name[name]

    def guess_extension (self, content_type):
        if content_type in self.extensions_by_mimetype:
            answers = list(self.extensions_by_mimetype[content_type].items())
            return max(answers, key=lambda x: x[1])[0] # Return the most frequent by count...
        else:
            import mimetypes
            return mimetypes.guess_extension(content_type)

    def get_filters (self):
        all_importable_mimetypes = []
        all_importable_patterns = []
        filters = []; names = []
        for plugin in self.importer_plugins:
            if plugin.name in names:
                i = names.index(plugin.name)
                filters[i][1] += plugin.mimetypes
                filters[i][2] += plugin.patterns
            else:
                names.append(plugin.name)
                filters.append([plugin.name,plugin.mimetypes,plugin.patterns])
            all_importable_mimetypes += plugin.mimetypes
            all_importable_patterns += plugin.patterns
        filters = [[_('All importable files'),all_importable_mimetypes,all_importable_patterns]] + filters
        return filters

    def register_plugin (self, plugin):
        self.plugins.append(plugin)
        if isinstance(plugin,ImporterPlugin):
            name = plugin.name
            if name in self.plugins_by_name:
                print('WARNING','replacing',self.plugins_by_name[name],'with',plugin)
            self.plugins_by_name[name] = plugin
            self.learn_mimetype_extension_mappings(plugin)
            self.importer_plugins.append(plugin)


    def learn_mimetype_extension_mappings (self, plugin):
        for mt in plugin.mimetypes:
            if mt not in self.extensions_by_mimetype:
                self.extensions_by_mimetype[mt] = {}
            for ptrn in plugin.patterns:
                if ptrn.find('*.')==0:
                    ext = ptrn.split('.')[-1]
                    if ext.isalnum():
                        # Then increment our count for this...
                        self.extensions_by_mimetype[mt][ext] = self.extensions_by_mimetype[mt].get(ext,0) + 1

    def unregister_plugin (self, plugin):
        if isinstance(plugin,ImporterPlugin):
            name = plugin.name
            if name in self.plugins_by_name:
                del self.plugins_by_name[name]
                self.plugins.remove(plugin)
            else:
                print('WARNING: unregistering ',plugin,'but there seems to be no plugin for ',name)
        else:
            self.plugins.remove(plugin)


def get_import_manager():
    return ImportManager.instance()
