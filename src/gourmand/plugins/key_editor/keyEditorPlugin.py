from gi.repository import Gtk

import gourmand.main
import gourmand.plugin
from gourmand.i18n import _

from . import keyEditor


class KeyEditorPlugin (gourmand.plugin.ToolPlugin):
    menu_items = '''
        <placeholder name="DataTool">
        <menuitem action="KeyEditor"/>
        </placeholder>
    '''

    def setup_action_groups (self):
        self.action_group = Gtk.ActionGroup(name='KeyEditorActionGroup')
        self.action_group.add_actions([
            ('KeyEditor',None,_('Ingredient _Key Editor'),
             None,_('Edit ingredient keys en masse'),self.show_key_editor)
            ])
        self.action_groups.append(self.action_group)

    def show_key_editor (self, *args):
        gourmand_app = gourmand.main.get_application()
        ke = keyEditor.KeyEditor(rd=gourmand_app.rd, rg=gourmand_app)
