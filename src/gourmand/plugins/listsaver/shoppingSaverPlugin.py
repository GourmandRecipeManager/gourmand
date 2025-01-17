import time

from gi.repository import Gtk

import gourmand.main
import gourmand.recipeManager
from gourmand.i18n import _
from gourmand.plugin import ShoppingListPlugin


class ShoppingListSaver(ShoppingListPlugin):

    ui_string = """<ui>
    <menubar name="ShoppingListMenuBar">
      <menu name="File" action="File">
        <placeholder name="ExtraFileStuff">
          <menuitem action="SaveAsRecipe"/>
        </placeholder>
      </menu>
    </menubar>
    <toolbar name="ShoppingListTopToolBar">
      <separator/>
      <toolitem action="SaveAsRecipe"/>
    </toolbar>
    </ui>
    """
    name = "shopping_list_saver"
    label = _("Shopping List Saver")

    def setup_action_groups(self):
        self.shoppingListSaverActionGroup = Gtk.ActionGroup(name="ShoppingListSaverActionGroup")
        self.shoppingListSaverActionGroup.add_actions(
            [
                (
                    "SaveAsRecipe",  # name
                    Gtk.STOCK_SAVE_AS,  # stock
                    _("Save List as Recipe"),  # text
                    _("<Ctrl><Shift>S"),  # key-command
                    _("Save current shopping list as a recipe for future use"),  # tooltip
                    self.save_as_recipe,  # callback
                ),
            ]
        )
        self.action_groups.append(self.shoppingListSaverActionGroup)

    def save_as_recipe(self, *args):
        sg = self.pluggable
        rr = sg.recs
        rd = gourmand.recipeManager.get_recipe_manager()
        rg = gourmand.main.get_application()
        # print rr
        rec = rd.add_rec(dict(title=_("Menu for %s (%s)") % (time.strftime("%x"), time.strftime("%X")), category=_("Menu")))
        for recipe, mult in list(rr.values()):
            # Add all recipes...
            rd.add_ing(
                {
                    "amount": mult,
                    "unit": "Recipe",
                    "refid": recipe.id,
                    "recipe_id": rec.id,
                    "item": recipe.title,
                }
            )
        for amt, unit, item in sg.extras:
            # Add all extras...
            rd.add_ing(
                {
                    "amount": amt,
                    "unit": unit,
                    "item": item,
                    "ingkey": item,
                }
            )
        rg.open_rec_card(rec)
