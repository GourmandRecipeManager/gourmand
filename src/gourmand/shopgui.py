#!/usr/bin/env python
import os
import os.path
import time

from gi.repository import Gdk, GObject, Gtk

from gourmand.i18n import _
from gourmand.recipeManager import get_recipe_manager

# from nutrition.nutritionLabel import NutritionLabel
# from nutrition.nutrition import NutritionInfoList
from . import convert, plugin, plugin_loader, prefs, recipeManager
from .exporters.printer import PrintManager
from .gdebug import debug
from .gtk_extras import WidgetSaver, fix_action_group_importance
from .gtk_extras import dialog_extras as de
from .gtk_extras import treeview_extras as te
from .shopping import ShoppingList

ui_string = """
<ui>
  <menubar name="ShoppingListMenuBar">
    <menu name="File" action="File">
      <menuitem action="Save"/>
      <menuitem action="Print"/>
      <separator/>
      <placeholder name="ExtraFileStuff"/>
      <separator/>
      <menuitem action="Close"/>
    </menu>
    <menu name="Edit" action="Edit">
      <menuitem action="AddNewItems"/>
      <menuitem action="RemoveRecipes"/>
      <separator/>
      <menuitem action="ItemToPantry"/>
      <menuitem action="ItemToShoppingList"/>
      <menuitem action="ChangeCategory"/>
    </menu>
    <menu name="HelpMenu" action="HelpMenu">
      <menuitem action="Help"/>
    </menu>
  </menubar>
  <popup name="ShopPop">
    <menuitem action="ItemToPantry"/>
    <menu action="ChangeCategoryPop">
      <placeholder name="categories"/>
      <menuitem action="newCategory"/>
    </menu>
  </popup>
  <popup name="PanPop">
    <menuitem name="ItemToShoppingList" action="ItemToShoppingList"/>
    <menu name="ChangeCategoryPop" action="ChangeCategoryPop">
      <placeholder name="categories"/>
      <menuitem name="newCategory" action="newCategory"/>
    </menu>
  </popup>
  <popup action="ChangeCategoryPopup">
     <placeholder name="categories"/>
     <menuitem name="newCategory" action="newCategory"/>
  </popup>
  <toolbar name="ShoppingListTopToolBar">
    <toolitem action="Save"/>
    <toolitem action="Print"/>
    <separator/>
    <toolitem action="RemoveRecipes"/>
  </toolbar>
  <toolbar name="ShoppingListActionToolBar">
    <toolitem action="AddNewItems"/>
    <separator/>
    <toolitem action="ChangeCategory"/>
    <separator/>
    <toolitem action="ItemToShoppingList"/>
    <toolitem action="ItemToPantry"/>
  </toolbar>
</ui>
"""


# Convenience functions
def setup_frame_w_accel_label(txt, target_widget=None):
    """Return a frame with a mnemonic label"""
    label = Gtk.Label(label=txt)
    label.set_use_underline(True)
    f = Gtk.Frame()
    f.set_label_widget(label)
    label.show()
    if target_widget:
        label.set_mnemonic_widget(target_widget)
    return f


def setup_sw(child):
    sw = Gtk.ScrolledWindow()
    sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    sw.add(child)
    child.show()
    sw.show()
    return sw


# end convenience functions


class IngredientAndPantryList:
    """A subclass to handle all TreeView code for moving items between
    shopping and pantry list
    """

    def __init__(self):
        self.rd = recipeManager.get_recipe_manager()
        self.setup_ui_manager()
        self.setup_actions()

    def setup_ui_manager(self):
        self.ui_manager = Gtk.UIManager()
        self.ui_manager.add_ui_from_string(ui_string)

    def setup_actions(self):
        self.pantryActions = Gtk.ActionGroup(name="PantryActions")
        self.shoppingActions = Gtk.ActionGroup(name="ShoppingActions")
        self.pantryOrShoppingActions = Gtk.ActionGroup(name="PantryOrShoppingActions")
        self.pantryOrShoppingActions.add_actions(
            [
                ("ChangeCategoryPop", None, _("Change _Category")),
                (
                    "newCategory",
                    None,
                    _("Create new category"),
                    None,
                    None,
                    lambda *args: self.pantryOrShoppingActions.get_action("ChangeCategory").set_active(True),
                ),
            ]
        )
        self.pantryOrShoppingActions.add_toggle_actions(
            [
                ("ChangeCategory", None, _("Change _Category"), None, _("Change the category of the currently selected item"), self.change_category),
            ]
        )

        self.pantryActions.add_actions(
            [
                ("PantryPopup", None, _("Pantry")),
                (
                    "ItemToShoppingList",  # name
                    "add-to-shopping-list",  # stock
                    _("Move to _Shopping List"),  # text
                    _("<Ctrl>B"),  # key-command
                    None,  # tooltip
                    lambda *args: self.rem_selection_from_pantry(),  # callback
                ),
            ]
        )
        self.shoppingActions.add_actions(
            [
                ("ShopPopup", None, _("Shopping List")),
                (
                    "ItemToPantry",  # name
                    Gtk.STOCK_UNDO,  # stock
                    _("Move to _pantry"),  # text
                    _("<Ctrl>D"),  # key-command
                    _("Remove from shopping list"),  # tooltip
                    lambda *args: self.add_selection_to_pantry(),  # callback
                ),
            ]
        )
        fix_action_group_importance(self.pantryActions)
        self.ui_manager.insert_action_group(self.pantryActions, 0)
        fix_action_group_importance(self.shoppingActions)
        self.ui_manager.insert_action_group(self.shoppingActions, 0)
        fix_action_group_importance(self.pantryOrShoppingActions)
        self.ui_manager.insert_action_group(self.pantryOrShoppingActions, 0)

    def setup_category_ui(self):
        self.cats_setup = True
        catUI = """<placeholder name="categories">"""

        def my_cb(widget, cat):
            self.change_to_category(cat)

        for n, category in enumerate(self.sh.get_orgcats()):
            actionName = "category" + str(n)
            catUI += '<menuitem action="%s"/>' % actionName
            self.pantryOrShoppingActions.add_actions([(actionName, None, category, None, _("Move selected items into %s") % category, None)])

            self.pantryOrShoppingActions.get_action(actionName).connect("activate", my_cb, category)
            self.get_catmodel().append([category])
        catUI += "</placeholder>"
        catUI = """<ui>
        <menubar action="ShoppingListMenu">
          <menu action="Edit">
            <menu action="ChangeCategoryPop">
              %(ph)s
            </menu>
          </menu>
        </menubar>
        <popup action="ShopPop">
            <menu action="ChangeCategoryPop">
              %(ph)s
            </menu>
        </popup>
        <popup name="PanPop">
          <menu name="ChangeCategoryPop" action="ChangeCategoryPop">
            %(ph)s
          </menu>
        </popup>
        <popup name="ChangeCategoryPopup">
            %(ph)s
        </popup>
        </ui>""" % {
            "ph": catUI
        }
        self.last_category_merge = self.ui_manager.add_ui_from_string(catUI)
        self.ui_manager.ensure_update()

    # Base GUI Setup
    def setup_paned_view(self):
        self.create_pTree()
        self.create_slTree()
        hp = Gtk.HPaned()
        hp.set_position(400)
        f1 = setup_frame_w_accel_label(_("_Shopping List"), self.slTree)
        f2 = setup_frame_w_accel_label(_("Already Have (_Pantry Items)"), self.pTree)
        f1.add(setup_sw(self.slTree))
        f1.show_all()
        f2.add(setup_sw(self.pTree))
        f2.show_all()
        hp.add1(f1)
        hp.add2(f2)
        return hp

    # TreeView and TreeModel setup
    def create_pTree(self):
        debug("create_pTree (self, data):", 5)
        self.pMod = self.createIngModel(self.pantry)
        self.pTree = self.create_ingTree(Gtk.TreeView(), self.pMod)
        self.pTree.set_name("pantry_tree")
        self.pTree.get_selection().connect("changed", self.pTree_sel_changed_cb)
        # reset the first time...
        self.pTree_sel_changed_cb(self.pTree.get_selection())

        def pTree_popup_cb(tv, event):
            debug("pTree_popup_cb (tv, event):", 5)
            if event.button == 3 or event.type == Gdk.EventType._2BUTTON_PRESS:
                self.popup_menu(tv, event)
                return True

        self.pTree.connect("button-press-event", pTree_popup_cb)

    def create_slTree(self):
        debug("create_slTree (self, data):", 5)
        self.slMod = self.createIngModel(self.data)
        self.slTree = self.create_ingTree(Gtk.TreeView(), self.slMod)
        self.slTree.set_name("shopping_list_tree")
        self.slTree.show()
        self.slTree.connect("popup-menu", self.popup_menu)

        def slTree_popup_cb(tv, event):
            debug("slTree_popup_cb (tv, event):", 5)
            if event.button == 3 or event.type == Gdk.EventType._2BUTTON_PRESS:
                self.popup_menu(tv, event)
                return True

        self.slTree.connect("button-press-event", slTree_popup_cb)
        self.slTree.get_selection().connect("changed", self.slTree_sel_changed_cb)
        # reset the first time
        self.slTree_sel_changed_cb(self.slTree.get_selection())

    def create_ingTree(self, widget, model):
        debug("create_ingTree (self, widget, model):", 5)
        # self.slTree = Gtk.TreeView(self.slMod)
        tree = widget
        tree.set_model(model)
        ## add multiple selections
        tree.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        ## adding drag and drop functionality
        targets = [
            ("GOURMET_SHOPPER_SW", Gtk.TargetFlags.SAME_WIDGET, 0),
            ("GOURMET_SHOPPER", Gtk.TargetFlags.SAME_APP, 1),
            ("text/plain", 0, 2),
            ("STRING", 0, 3),
            ("STRING", 0, 4),
            ("COMPOUND_TEXT", 0, 5),
            ("text/unicode", 0, 6),
        ]
        tree.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, list(Gtk.TargetEntry.new(*t) for t in targets), Gdk.DragAction.COPY | Gdk.DragAction.MOVE)
        tree.enable_model_drag_dest(targets, Gdk.DragAction.COPY | Gdk.DragAction.MOVE)
        tree.connect("drag_begin", self.on_drag_begin)
        tree.connect("drag_data_get", self.on_drag_data_get)
        tree.connect("drag_data_received", self.on_drag_data_received)
        tree.connect("drag_motion", self.on_drag_motion)
        tree.connect("drag_drop", self.on_drag_drop)
        renderer = Gtk.CellRendererText()
        for n, t in [[0, "Item"], [1, "Amount"]]:
            col = Gtk.TreeViewColumn(t, renderer, text=n)
            col.set_resizable(True)
            tree.append_column(col)
        tree.expand_all()
        tree.show()
        return tree

    def createIngModel(self, data):
        debug("createIngModel (self, data):", 5)
        """Data is a list of lists, where each item is [ing amt]"""
        mod = Gtk.TreeStore(GObject.TYPE_STRING, GObject.TYPE_STRING)
        for c, lst in data:
            catiter = mod.append(None)
            mod.set_value(catiter, 0, c)
            for i in lst:
                ing = i[0]
                amt = i[1]
                iter = mod.append(catiter)
                mod.set_value(iter, 0, ing)
                mod.set_value(iter, 1, amt)
        return mod

    # ---- TreeView callbacks...
    def slTree_sel_changed_cb(self, selection):
        """Callback handler for selection change on shopping treeview."""
        if selection.count_selected_rows() > 0:
            self.shoppingActions.set_sensitive(True)
            # if we have items selected, the pantry tree should not
            # this makes these feel more like one control/list divided
            # into two sections.
            self.tv = self.slTree
            self.pTree.get_selection().unselect_all()
        else:
            self.shoppingActions.set_sensitive(False)

    def pTree_sel_changed_cb(self, selection):
        """Callback handler for selection change on pantry treeview"""
        if selection.count_selected_rows() > 0:
            self.pantryActions.set_sensitive(True)
            # if we have items selected, the shopping tree should not.
            # this makes these feel more like one control/list divided
            # into two sections.
            self.tv = self.pTree
            self.slTree.get_selection().unselect_all()
        else:
            self.pantryActions.set_sensitive(False)

    # Popup menu setup
    def create_popups(self):
        self.shoppop = self.ui_manager.get_widget("/ShopPop")
        self.panpop = self.ui_manager.get_widget("/PanPop")

    # Drag-and-drop
    def on_drag_begin(self, tv, context):
        debug("on_drag_begin(self, tv, context):", 5)
        self.tv = tv
        self.ssave = te.selectionSaver(self.slTree, 1)
        self.pssave = te.selectionSaver(self.pTree, 1)

    def on_drag_motion(self, tv, context, x, y, time):
        pass

    def on_drag_data_get(self, tv, context, selection, info, time):
        self.drag_selection = selection

    def on_drag_data_received(self, tv, context, x, y, selection, info, time):
        debug("on_drag_data_received(self, tv,context,x,y,selection,info,time):", 5)
        if str(selection.target) == "GOURMET_SHOPPER_SW":
            ## in this case, we're recategorizing
            # try:
            dest = tv.get_dest_row_at_pos(x, y)
            if dest:
                path, drop_where = dest
                iter = tv.get_model().get_iter((path[0]))  # grab the category (outside of tree)
                cat = tv.get_model().get_value(iter, 0)
                for sel, iter in self.get_selected_ingredients(return_iters=True):
                    path = tv.get_model().get_path(iter)
                    if len(path) == 1:
                        # if we're moving an entire category, then we
                        # need to reorder categories.
                        debug("Saving new category orders", 0)
                        self.commit_category_orders(tv)
                        # and now we need to move our new category into place...
                        if drop_where == Gtk.TreeViewDropPosition.AFTER or drop_where == Gtk.TreeViewDropPosition.INTO_OR_AFTER:
                            new_pos = self.sh.catorder_dic[cat] + 0.5
                        else:
                            new_pos = self.sh.catorder_dic[cat] - 0.5
                        self.sh.catorder_dic[sel] = new_pos
                        debug("%s moved to position %s" % (sel, self.sh.catorder_dic[sel]), 0)
                        debug("The current order is: %s" % self.sh.catorder_dic)
                    else:
                        self.sh.orgdic[sel] = cat
                self.resetSL()
                self.ssave.restore_selections(tv=self.slTree)
                self.pssave.restore_selections(tv=self.pTree)
            # except TypeError:
            else:
                debug("Out of range!", 0)
        elif str(selection.target) == "GOURMET_SHOPPER":
            ## in this case, we're moving
            if tv == self.pTree:
                self.add_selection_to_pantry()
            else:
                self.rem_selection_from_pantry()

    def on_drag_drop(self, tv, context, x, y, time):
        debug("on_drag_drop (self, tv, context, x, y, time):", 5)
        # model = tv.get_model()
        otv, oselection = self.dragged
        if otv == self.pTree and tv == self.slTree:
            self.rem_selection_from_pantry()
        elif otv == self.slTree and tv == self.pTree:
            self.add_selection_to_pantry()
        else:
            try:
                path, drop_where = tv.get_dest_row_at_pos(x, y)
                iter = tv.get_model().get_iter((path[0]))  # grab the category (outside of tree)
                cat = tv.get_model().get_value(iter, 0)
                for sel in oselection:
                    self.sh.orgdic[sel] = cat
                self.resetSL()
            except TypeError as e:
                self.message("Out of range! %s" % e)
        return False

    # end drag-n-drop methods

    # ---- end TreeView callbacks

    # -- End TreeView and TreeModel setup

    # Callbacks for moving data back and forth
    def resetSL(self):
        debug("resetSL (self):", 5)
        if not hasattr(self, "cats_setup") or not self.cats_setup:
            self.setup_category_ui()
        self.data, self.pantry = self.organize_list(self.lst)
        self.slMod = self.createIngModel(self.data)
        self.pMod = self.createIngModel(self.pantry)
        self.slTree.set_model(self.slMod)
        self.pTree.set_model(self.pMod)
        # self.rectree.set_model(self.create_rmodel())
        self.slTree.expand_all()
        self.pTree.expand_all()
        # self.pTree_sel_changed_cb(self.pTree.get_selection())
        # self.slTree_sel_changed_cb(self.slTree.get_selection())

    def add_selection_to_pantry(self, *args):
        """Add selected items to pantry."""
        debug("add_selection_to_pantry (self, *args):", 5)
        self.tv = self.slTree
        self.ssave = te.selectionSaver(self.slTree, 1)
        self.pssave = te.selectionSaver(self.pTree, 1)
        kk = self.get_selected_ingredients()
        for k in kk:
            self.sh.add_to_pantry(k)
        self.resetSL()
        self.ssave.restore_selections(tv=self.pTree)

    def rem_selection_from_pantry(self, *args):
        """Add selected items to shopping list."""
        debug("rem_selection_from_pantry (self, *args):", 5)
        self.tv = self.pTree
        self.ssave = te.selectionSaver(self.slTree, 1)
        self.pssave = te.selectionSaver(self.pTree, 1)
        for k in self.get_selected_ingredients():
            self.sh.remove_from_pantry(k)
        self.resetSL()
        self.pssave.restore_selections(tv=self.slTree)

    def change_to_category(self, category):
        """Change selected recipes to category category"""
        do_reset = category not in self.sh.get_orgcats()
        kk = self.get_selected_ingredients()
        for k in kk:
            self.sh.orgdic[k] = category
        ssave = te.selectionSaver(self.slTree, 1)
        pssave = te.selectionSaver(self.pTree, 1)
        self.resetSL()
        ssave.restore_selections(tv=self.slTree)
        pssave.restore_selections(tv=self.slTree)
        if do_reset:
            self.reset_categories()

    def reset_categories(self):
        self.ui_manager.remove_ui(self.last_category_merge)
        self.get_catmodel().clear()
        self.setup_category_ui()
        self.create_popups()

    def add_sel_to_newcat(self, menuitem, *args):
        debug("add_sel_to_newcat (self, menuitem, *args):", 5)
        kk = self.get_selected_ingredients()
        sublab = ", ".join(kk)
        cat = de.getEntry(label=_("Enter Category"), sublabel=_("Category to add %s to") % sublab, entryLabel=_("Category:"), parent=self.widget)
        if cat:
            for k in kk:
                self.sh.orgdic[k] = cat
            self.shoppop.get_children()[-1].hide()
            self.panpop.get_children()[-1].hide()
            self.setup_popup()
            ssave = te.selectionSaver(self.slTree, 1)
            pssave = te.selectionSaver(self.pTree, 1)
            self.resetSL()
            ssave.restore_selections(tv=self.slTree)
            pssave.restore_selections(tv=self.slTree)

    # Popup methods...
    def popup_menu(self, tv, event=None, *args):
        if event is None:
            event = Gtk.get_current_event()

        t = getattr(event, "time", 0)
        btn = getattr(event, "button", 0)

        if tv.get_name() == "shopping_list_tree":
            self.shoppop.popup(None, None, None, None, btn, t)
        else:  # tv.get_name == 'pantry_tree':
            self.panpop.popup(None, None, None, None, btn, t)
        return True

    # Data convenience methods
    def get_selected_ingredients(self, return_iters=False):
        """A way to find out what's selected. By default, we simply return
        the list of ingredient keys. If return_iters is True, we return the selected
        iters themselves as well (returning a list of [key,iter]s)"""
        debug("get_selected_ingredients (self):", 5)

        def foreach(model, path, iter, selected):
            debug("foreach(model,path,iter,selected):", 5)
            selected.append(iter)

        selected = []
        self.tv.get_selection().selected_foreach(foreach, selected)
        debug("multiple selections = %s" % selected, 3)
        # ts,itera=self.tv.get_selection().get_selected()
        selected_keys = []
        for itera in selected:
            key = self.tv.get_model().get_value(itera, 0)
            if return_iters:
                selected_keys.append((key, itera))
            else:
                selected_keys.append(key)
        debug("get_selected_ingredients returns: %s" % selected_keys, 3)
        return selected_keys


class ShopGui(ShoppingList, plugin_loader.Pluggable, IngredientAndPantryList):

    def __init__(self):
        IngredientAndPantryList.__init__(self)
        ShoppingList.__init__(self)
        self.prefs = prefs.Prefs.instance()
        self.conf = []
        self.w = Gtk.Window()
        self.main = Gtk.VBox()
        self.w.set_title(_("Shopping List"))
        self.w.set_default_size(800, 600)
        self.w.connect("delete-event", self.hide)
        # from .main import get_application

        self.setup_ui_manager()
        self.setup_actions()
        self.setup_main()
        self.conf.append(WidgetSaver.WindowSaver(self.w, self.prefs.get("shopGuiWin", {}), show=False))
        self.conf.append(WidgetSaver.WidgetSaver(self.vp, self.prefs.get("shopvpaned1", {"position": self.vp.get_position()})))
        self.conf.append(WidgetSaver.WidgetSaver(self.hp, self.prefs.get("shophpaned1", {"position": self.hp.get_position()})))
        plugin_loader.Pluggable.__init__(self, [plugin.ShoppingListPlugin])
        self.sh = self.get_shopper([])
        self.setup_category_ui()
        self.create_popups()

    def get_shopper(self, lst):
        return recipeManager.DatabaseShopper(lst, self.rd)

    # Create interface...

    def setup_ui_manager(self):
        self.ui_manager = Gtk.UIManager()
        self.ui_manager.add_ui_from_string(ui_string)

    def setup_main(self):
        mb = self.ui_manager.get_widget("/ShoppingListMenuBar")
        # help(self.main)
        # pack_start(self, child:Gtk.Widget, expand:bool, fill:bool, padding:int)
        self.main.pack_start(mb, False, False, 0)
        ttb = self.ui_manager.get_widget("/ShoppingListTopToolBar")
        self.main.pack_start(ttb, False, False, 0)
        self.vp = Gtk.VPaned()
        self.vp.show()
        self.vp.set_position(150)
        self.create_rtree()
        self.top_frame = setup_frame_w_accel_label(_("_Recipes"), self.rectree)
        self.top_frame.add(setup_sw(self.rectree))
        self.top_frame.show()
        self.vp.add1(self.top_frame)
        vb = Gtk.VBox()
        vb.show()
        self.vp.add2(vb)
        slatb = self.ui_manager.get_widget("/ShoppingListActionToolBar")
        slatb.show()
        vb.pack_start(slatb, False, False, 0)
        self.setup_add_box()
        vb.pack_start(self.add_box, False, False, 0)
        self.setup_cat_box()
        vb.pack_start(self.cat_box, False, False, 0)
        self.hp = self.setup_paned_view()
        self.hp.show()
        vb.pack_start(self.hp, True, True, 0)
        self.main.pack_start(self.vp, True, True, 0)
        self.vp.show()
        vb.show()
        self.w.add(self.main)
        self.main.show()
        self.w.add_accel_group(self.ui_manager.get_accel_group())

    def setup_add_box(self):
        # Setup add-ingredient widget
        self.add_box = Gtk.HBox()
        self.add_entry = Gtk.Entry()
        add_label = Gtk.Label(label=_("_Add items:"))
        add_label.set_use_underline(True)
        add_label.set_mnemonic_widget(self.add_entry)
        self.add_box.pack_start(add_label, False, False, 0)
        add_label.show()
        self.add_box.pack_start(self.add_entry, True, True, 0)
        self.add_entry.show()
        self.add_button = Gtk.Button.new_with_label("gtk-add")
        self.add_box.pack_start(self.add_button, False, False, 0)
        self.add_button.show()
        self.add_entry.connect("activate", self.item_added)
        self.add_button.connect("clicked", self.item_added)

    def get_catmodel(self):
        if hasattr(self, "catmodel"):
            return self.catmodel
        else:
            self.catmodel = Gtk.ListStore(str)
            return self.catmodel

    def setup_cat_box(self):
        # Setup change-category widget
        self.cat_box = Gtk.HBox()  # ; self.cat_box.set_spacing(6)
        self.cat_cbe = Gtk.ComboBox.new_with_entry()
        self.cat_cbe.set_model(self.get_catmodel())
        self.cat_cbe.set_entry_text_column(0)
        self.cat_entry = self.cat_cbe.get_child()
        self.cat_button = Gtk.Button.new_with_label("gtk-apply")
        self.cat_label = Gtk.Label(label="_Category: ")
        self.cat_label.set_use_underline(True)
        self.cat_label.set_mnemonic_widget(self.cat_entry)
        comp = Gtk.EntryCompletion()
        comp.set_model(self.get_catmodel())
        comp.set_text_column(0)
        self.cat_entry.set_completion(comp)
        self.cat_box.pack_start(self.cat_label, False, False, 0)
        self.cat_label.show()
        self.cat_box.pack_start(self.cat_cbe, True, True, 0)
        self.cat_cbe.show()
        self.cat_box.pack_start(self.cat_button, False, False, 0)
        self.cat_button.show()
        self.cat_entry.connect("activate", self.category_changed)
        self.cat_button.connect("clicked", self.category_changed)

    def setup_actions(self):
        self.mainActionGroup = Gtk.ActionGroup(name="MainActions")
        self.recipeListActions = Gtk.ActionGroup(name="RecipeListActions")
        self.recipeListActions.add_actions(
            [
                (
                    "RemoveRecipes",
                    Gtk.STOCK_REMOVE,
                    _("Remove Recipes"),
                    "<Control>Delete",
                    _("Remove recipes from shopping list"),
                    self.clear_recipes,
                )
            ]
        )
        self.mainActionGroup.add_actions(
            [
                ("Edit", None, _("_Edit")),
                ("Save", Gtk.STOCK_SAVE, None, None, None, self.save),  # name  # stock  # text  # key-command  # tooltip  # callback
                ("Print", Gtk.STOCK_PRINT, None, "<Ctrl>P", None, self.printList),  # name  # stock  # text  # key-command  # tooltip  # callback
                ("Close", Gtk.STOCK_CLOSE, None, None, None, self.hide),  # name  # stock  # text  # key-command  # tooltip  # callback
                ("File", None, _("_File")),
                ("Help", Gtk.STOCK_HELP, _("_Help"), None, None, lambda *args: de.show_faq(parent=self.w, jump_to="Shopping")),
                ("HelpMenu", None, _("_Help")),
            ]
        )
        self.mainActionGroup.add_toggle_actions(
            [
                ("AddNewItems", Gtk.STOCK_ADD, _("Add items"), "<Ctrl>plus", _("Add arbitrary items to shopping list"), self.add_item),
                # ( , # name
                #   , # stock
                #   , # text
                #   , # key-command
                #   , # tooltip
                #     # callback
                #   ),
            ]
        )

        fix_action_group_importance(self.mainActionGroup)
        self.ui_manager.insert_action_group(self.mainActionGroup, 0)
        fix_action_group_importance(self.recipeListActions)
        self.ui_manager.insert_action_group(self.recipeListActions, 0)
        IngredientAndPantryList.setup_actions(self)

    def getOptionalIngDic(self, ivw, mult, prefs):
        """Return a dictionary of optional ingredients with a TRUE|FALSE value

        Alternatively, we return a boolean value, in which case that is
        the value for all ingredients.

        The dictionary will tell us which ingredients to add to our shopping list.
        We look at prefs to see if 'shop_always_add_optional' is set, in which case
        we don't ask our user."""
        debug("getOptionalIngDic (ivw):", 5)
        # vw = ivw.select(optional=True)
        vw = [r for r in ivw if r.optional]
        # optional_mode: 0==ask, 1==add, -1==dont add
        optional_mode = prefs.get("shop_handle_optional", 0)
        if optional_mode:
            if optional_mode == 1:
                return True
            elif optional_mode == -1:
                return False
        elif len(vw) > 0:
            if None not in [i.shopoptional for i in vw]:
                # in this case, we have a simple job -- load our saved
                # defaults
                dic = {}
                for i in vw:
                    if i.shopoptional == 2:
                        dic[i.ingkey] = True
                    else:
                        dic[i.ingkey] = False
                return dic
            # otherwise, we ask our user
            oid = OptionalIngDialog(vw, prefs, mult)
            retval = oid.run()
            if retval:
                return retval
            else:
                raise de.UserCancelledError("Option Dialog cancelled!")

    # -- TreeView and TreeModel setup
    def create_rtree(self):
        debug("create_rtree (self):", 5)
        self.rmodel = self.create_rmodel()
        self.rectree = Gtk.TreeView(model=self.rmodel)
        # self.glade.signal_connect('ingmen_pantry',self.add_selection_to_pantry)
        # self.glade.signal_connect('panmen_remove',self.rem_selection_from_pantry)
        self.rectree.set_model(self.rmodel)
        renderer = Gtk.CellRendererText()
        # renderer.set_property('editable',True)
        # renderer.connect('edited',tst)
        titl = Gtk.TreeViewColumn(_("Title"), renderer, text=1)
        mult = Gtk.TreeViewColumn(_("x"), renderer, text=2)
        self.rectree.append_column(titl)
        self.rectree.append_column(mult)
        titl.set_resizable(True)
        titl.set_clickable(True)
        titl.set_reorderable(True)
        mult.set_resizable(True)
        mult.set_clickable(True)
        mult.set_reorderable(True)
        self.rectree.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        self.rectree.connect("row-activated", self.rectree_activated_cb)
        self.rectree.show()

    def create_rmodel(self):
        debug("create_rmodel (self):", 5)
        mod = Gtk.TreeStore(GObject.TYPE_PYOBJECT, GObject.TYPE_STRING, GObject.TYPE_STRING)
        for r, mult in list(self.recs.values()):
            iter = mod.append(None)
            mod.set_value(iter, 0, r)
            mod.set_value(iter, 1, r.title)
            mod.set_value(iter, 2, convert.float_to_frac(mult))
        return mod

    def rectree_activated_cb(self, tv, path, vc):
        rec = tv.get_model()[path][0]
        from .GourmetRecipeManager import get_application

        get_application().open_rec_card(rec)

    # End UI Set-up

    # Convenience methods for handling our data
    def getSelectedRecs(self):
        """Return each recipe in list"""

        def foreach(model, path, iterable, recs):
            debug("foreach(model,path,iter,recs):", 5)
            try:
                rec = model.get_value(iterable, 0)
                recs.append(rec)
            except Exception:
                debug("DEBUG: There was a problem with iterable: %s path: %s" % (iterable, path), 1)

        recs = []
        self.rectree.get_selection().selected_foreach(foreach, recs)
        debug("%s selected recs: %s" % (len(recs), recs), 3)
        return recs

    def commit_category_orders(self, tv, space_before=None, space_after=None):
        """Commit the order of categories to memory.
        We allow for making room before or after a given
        iter, in which case"""
        mod = tv.get_model()
        iter = mod.get_iter_first()
        last_val = -100
        while iter:
            cat = mod.get_value(iter, 0)
            if cat in self.sh.catorder_dic:
                val = self.sh.catorder_dic[cat]
            else:
                val = 0
            if val <= last_val:
                val = last_val + 10
                self.sh.catorder_dic[cat] = val
            last_val = val
            iter = mod.iter_next(iter)

    def reset(self):
        self.grabIngsFromRecs(list(self.recs.values()), self.extras)
        self.resetSL()
        self.rectree.set_model(self.create_rmodel())

    # Callbacks
    def hide(self, *args):
        self.w.hide()
        return True

    def show(self, *args):
        self.w.present()

    def clear_recipes(self, *args):
        debug("clear_recipes (self, *args):", 5)
        selectedRecs = self.getSelectedRecs()
        if selectedRecs:
            for t in selectedRecs:
                self.recs.__delitem__(t.id)
                debug("clear removed %s" % t, 3)
            self.reset()
        elif de.getBoolean(label=_("No recipes selected. Do you want to clear the entire list?"), cancel=False):
            self.recs = {}
            self.extras = []
            self.reset()
        else:
            debug("clear cancelled", 2)

    def save(self, *args):
        debug("save (self, *args):", 5)
        filename = de.select_file(
            _("Save Shopping List As..."),
            filename=os.path.join(
                os.path.expanduser("~"),
                "%s %s.txt"
                % (
                    _("Shopping List"),
                    time.strftime("%x").replace("/", "-"),
                ),
            ),
            action=Gtk.FileChooserAction.SAVE,
        )
        if not filename:
            return
        self.doSave(*filename)

    def printList(self, *args):
        debug("printList (self, *args):", 0)
        self._printList(PrintManager.instance().get_simple_writer(), dialog_parent=self.w)

    def add_item(self, toggleWidget):
        if toggleWidget.get_active():
            self.add_box.show()
            self.add_entry.grab_focus()
            if self.pantryOrShoppingActions.get_action("ChangeCategory").get_active():
                self.pantryOrShoppingActions.get_action("ChangeCategory").set_active(False)
        else:
            self.add_box.hide()

    def change_category(self, toggleWidget):
        if toggleWidget.get_active():
            self.cat_box.show()
            self.cat_entry.grab_focus()
            if self.mainActionGroup.get_action("AddNewItems").get_active():
                self.mainActionGroup.get_action("AddNewItems").set_active(False)
        else:
            self.cat_box.hide()

    def item_added(self, *args):
        txt = self.add_entry.get_text()
        dct = get_recipe_manager().parse_ingredient(txt)
        if not dct:
            dct = {"amount": None, "unit": None, "item": txt}
        self.extras.append([dct.get("amount"), dct.get("unit"), dct.get("item")])
        # Make sure it doesn't end up in the pantry...
        self.sh.remove_from_pantry(dct.get("item"))
        self.grabIngsFromRecs(list(self.recs.values()), self.extras)
        self.resetSL()
        self.add_entry.set_text("")

    def category_changed(self, *args):
        cat = self.cat_entry.get_text()
        self.change_to_category(cat)
        self.cat_entry.set_text("")


class OptionalIngDialog(de.ModalDialog):
    """A dialog to query the user about whether to use optional ingredients."""

    def __init__(self, vw, prefs, mult=1, default=False):
        debug("__init__ (self,vw,default=False):", 5)
        self.rd = recipeManager.get_recipe_manager()
        de.ModalDialog.__init__(
            self,
            default,
            label=_("Select optional ingredients"),
            sublabel=_("Please specify which of the following optional ingredients you'd like to include on your shopping list."),
        )
        self.mult = mult
        self.vw = vw
        self.ret = {}
        self.create_tree()
        self.cb = Gtk.CheckButton("Always use these settings")
        self.cb.set_active(prefs.get("remember_optionals_by_default", False))
        alignment = Gtk.Alignment.new(1.0, 0, 0, 0)
        alignment.add(self.cb)
        self.vbox.add(alignment)
        alignment.show()
        self.cb.show()

    def create_model(self):
        """Create the TreeModel to show optional ingredients."""
        debug("create_model (self):", 5)
        self.mod = Gtk.TreeStore(
            GObject.TYPE_PYOBJECT,  # the ingredient obj
            GObject.TYPE_STRING,  # amount
            GObject.TYPE_STRING,  # unit
            GObject.TYPE_STRING,  # item
            GObject.TYPE_BOOLEAN,
        )  # include
        for i in self.vw:
            iter = self.mod.append(None)
            self.mod.set_value(iter, 0, i)
            if self.mult == 1:
                self.mod.set_value(iter, 1, self.rd.get_amount_as_string(i))
            else:
                self.mod.set_value(iter, 1, self.rd.get_amount_as_string(i, float(self.mult)))
            self.mod.set_value(iter, 2, i.unit)
            self.mod.set_value(iter, 3, i.item)
            self.mod.set_value(iter, 4, self.default)
            self.ret[i.ingkey] = self.default

    def create_tree(self):
        """Create our TreeView and populate it with columns."""
        debug("create_tree (self):", 5)
        self.create_model()
        self.tree = Gtk.TreeView(self.mod)
        txtr = Gtk.CellRendererText()
        togr = Gtk.CellRendererToggle()
        togr.set_property("activatable", True)
        togr.connect("toggled", self.toggle_ing_cb)
        # togr.start_editing()
        for n, t in [[1, "Amount"], [2, "Unit"], [3, "Item"]]:
            col = Gtk.TreeViewColumn(t, txtr, text=n)
            col.set_resizable(True)
            self.tree.append_column(col)
        bcol = Gtk.TreeViewColumn("Add to Shopping List", togr, active=4)
        self.tree.append_column(bcol)
        self.vbox.add(self.tree)
        self.tree.show()

    def toggle_ing_cb(self, cellrenderertoggle, path, *args):
        debug("toggle_ing_cb (self, cellrenderertoggle, path, *args):", 5)
        iter = self.mod.get_iter(path)
        val = self.mod.get_value(iter, 4)
        newval = not val
        self.ret[self.mod.get_value(iter, 0).ingkey] = newval
        self.mod.set_value(iter, 4, newval)

    def run(self):
        self.show()
        Gtk.main()
        if self.cb.get_active() and self.ret:
            # if we are saving our settings permanently...
            # we add ourselves to the shopoptional attribute
            for row in self.mod:
                ing = row[0]
                ing_include = row[4]
                if ing_include:
                    self.rd.modify_ing(ing, {"shopoptional": 2})
                else:
                    self.rd.modify_ing(ing, {"shopoptional": 1})
        return self.ret


if __name__ == "__main__":

    class TestIngredientAndPantryList(IngredientAndPantryList):

        def __init__(self):
            IngredientAndPantryList.__init__(self)
            # self.data = [('Dairy',[('milk','1 gal'),('cheese, cheddar','1 lb'),
            #                        ('cottage cheese','8 oz'),
            #                        ('yogurt','8 oz')]),
            #              ('Pastas',[('rotini','1 lb')]),]
            # self.pantry = [('Dairy',[('eggs','1/2 doz')]),
            #                ('Frozen',[('ice cream','1 gal')]),]
            #
            rm = recipeManager.get_recipe_manager()
            recs = [(r, 1) for r in rm.fetch_all(rm.recipe_table)[:2]]
            self.data, self.pantry = self.grabIngsFromRecs(recs)
            self.w = Gtk.Window()
            self.w.set_title(_("Shopping List"))
            self.w.add(self.setup_paned_view())
            self.w.show_all()
            self.w.connect("delete-event", Gtk.main_quit)

    # tst = TestIngredientAndPantryList()
    sg = ShopGui()
    rm = recipeManager.get_recipe_manager()
    recs = [(r, 1) for r in rm.fetch_all(rm.recipe_table)[:2]]
    for r, mult in recs:
        sg.addRec(r, mult)
    Gtk.main()

    # sg = ShopGui()
    # sg.show()
    sg.w.connect("delete-event", Gtk.main_quit)
    Gtk.main()
