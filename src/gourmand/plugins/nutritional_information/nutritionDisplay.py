import re

from gi.repository import Gtk

import gourmand.cb_extras as cb
import gourmand.dialog_extras as de
from gourmand.i18n import _

from . import parser_data


class NutritionModel(Gtk.TreeStore):
    TITLE_FIELD = "desc"

    def __init__(self, nvw):
        self.nvw = nvw
        Gtk.TreeStore.__init__(self, str, str)
        self.populate_model()

    def connect_treeview_signals(self, tv):
        tv.connect("row-expanded", self.row_expanded_cb)

    def populate_model(self, nvw=None):
        for n in self.nvw:
            self.add_row_to_model(n)

    def add_row_to_model(self, row):
        papa = self.append(None, [getattr(row, self.TITLE_FIELD), None])
        # debug('adding row to model: %s'%getattr(row,self.TITLE_FIELD),0)
        # add an empty child to make expander show up
        # (we don't actually expand until we have to)
        self.append(papa, [None, None])

    def row_expanded_cb(self, view, itr, path):
        child = self.iter_children(itr)
        if self.get_value(child, 0) is None:
            self.remove(child)
            self.add_children_to_row(itr)

    def add_children_to_row(self, papa):
        desc = self.get_value(papa, 0)
        row = self.nvw.select(**{self.TITLE_FIELD: desc})[0]
        for lname, sname, typ in parser_data.NUTRITION_FIELDS:
            if sname != self.TITLE_FIELD:
                self.append(papa, [lname, "%s" % getattr(row, sname)])


class SimpleNutritionalDisplay:
    def __init__(self, nutrition_data):
        self.w = Gtk.Window()
        self.nd = nutrition_data
        self.nm = NutritionModel(nutrition_data.db.nutrition_table)
        self.sw = Gtk.ScrolledWindow()
        self.tv = Gtk.TreeView()
        rend = Gtk.CellRendererText()
        # setup treeview columns
        for n, cname in enumerate(["Item", "Value"]):
            col = Gtk.TreeViewColumn(cname, rend, text=n)
            self.tv.append_column(col)
        self.tv.set_model(self.nm)
        self.nm.connect_treeview_signals(self.tv)
        self.w.add(self.sw)
        self.sw.add(self.tv)
        self.w.set_size_request(400, 400)
        self.w.show_all()


class SimpleIngredientCalculator(de.mDialog):
    """This will be a simple prototype -- type in an ingredient,
    select the USDA equivalent, type in an amount and we're off!"""

    def __init__(
        self,
        nd,
        umodel,
        fields=[
            "kcal",
            "protein",
            "carb",
            "fiber",
            "sugar",
            "famono",
            "fapoly",
            "fasat",
            "cholestrl",
        ],
    ):
        de.mDialog.__init__(self)
        self.fields = fields
        self.nd = nd
        self.db = self.nd.db
        self.umodel = umodel
        self.setup_boxes()

    def setup_boxes(self):
        self.hbb = Gtk.HBox()
        self.vbox.add(self.hbb)
        self.amtBox = Gtk.SpinButton()
        self.amtBox.set_range(0.075, 5000)
        self.amtBox.set_increments(0.5, 5)
        self.amtBox.set_sensitive(True)
        self.amtBox.set_value(1)
        self.amtBox.connect("changed", self.nutBoxCB)
        self.unitBox = Gtk.ComboBox()
        self.unitBox.set_model(self.umodel)
        cell = Gtk.CellRendererText()
        self.unitBox.pack_start(cell, True)
        self.unitBox.add_attribute(cell, "text", 1)
        cb.setup_typeahead(self.unitBox)
        self.itmBox = Gtk.Entry()
        self.nutBox = Gtk.ComboBox()
        self.nutBox.pack_start(cell, True)
        self.nutBox.add_attribute(cell, "text", 0)
        self.nutBox.connect("changed", self.nutBoxCB)
        self.unitBox.connect("changed", self.nutBoxCB)
        self.refreshButton = Gtk.Button("Update Nutritional Items")
        self.refreshButton.connect("clicked", self.updateCombo)
        self.hbb.add(self.amtBox)
        self.hbb.add(self.unitBox)
        self.hbb.add(self.itmBox)
        self.hbb.add(self.refreshButton)
        self.vbox.add(self.nutBox)
        self.nutLabel = Gtk.Label()
        self.vbox.add(self.nutLabel)
        self.vbox.show_all()

    def nutBoxCB(self, *args):
        txt = cb.cb_get_active_text(self.nutBox)
        row = self.db.nutrition_table[self.db.nutrition_table.find({"desc": txt})]
        conversion = self.nd.get_conversion_for_amt(float(self.amtBox.get_value()), cb.cb_get_active_text(self.unitBox), self.itmBox.get_text(), row)
        myfields = [x for x in parser_data.NUTRITION_FIELDS if x[1] in self.fields]
        lab = ""
        for ln, f, typ in myfields:
            amt = getattr(row, f)
            if f in parser_data.PER_100_GRAMS:
                if conversion:
                    amt = "%s" % (amt * conversion)
                else:
                    amt = "%s/%s" % (amt, _("100 grams"))
            lab += "\n%s: %s" % (ln, amt)
        self.nutLabel.set_text(lab)

    def updateCombo(self, *args):
        self.txt = self.itmBox.get_text()
        indexvw = self.db.nutrition_table.filter(self.search_func)
        nvw = self.db.nutrition_table.remapwith(indexvw)
        mod = Gtk.ListStore(str)
        list(map(lambda r: mod.append([r.desc]), nvw))
        self.nutBox.set_model(mod)

    def search_func(self, row):
        desc = row.desc.lower()
        txt = self.txt.lower()
        words = re.split(r"\W", txt)
        ret = True
        while ret and words:
            word = words.pop()
            if word:
                ret = desc.find(word) >= 0
        return ret


if __name__ == "__main__":
    from gourmand.recipeManager import RecipeManager, dbargs

    dbargs["file"] = "/tmp/fdsa/recipes.mk"
    db = RecipeManager(**dbargs)
    import gourmand.convert
    from gourmand.main import UnitModel

    # inginfo = gourmet.reccard.IngInfo(db)
    conv = gourmand.convert.converter()
    umod = UnitModel(conv)
    from . import nutritionGrabberGui

    try:
        nutritionGrabberGui.check_for_db(db)
    except nutritionGrabberGui.Terminated:
        print("Nutrition import was cut short a bit")

    def quit(*args):
        db.save()
        Gtk.mainquit()

    # snd=SimpleNutritionalDisplay(db.nutrition_table)
    # snd.w.connect('delete-event',quit)
    from . import nutrition

    nd = nutrition.NutritionData(db, conv)
    sic = SimpleIngredientCalculator(nd, umod)
    sic.run()
    Gtk.main()
