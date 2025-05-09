import textwrap
from itertools import islice

from gourmand import convert, gglobals
from gourmand.exporters.exporter import exporter_mult
from gourmand.gdebug import debug
from gourmand.i18n import _
from gourmand.plugin_loader import pluggable_method


class mealmaster_exporter(exporter_mult):
    def __init__(self, rd, r, out, conv=None, change_units=True, mult=1):
        from . import mealmaster_importer

        self.add_to_instructions = []
        self.conv = conv
        mmf2mk = mealmaster_importer.mmf_constants()
        self.uc = mmf2mk.unit_convr
        recattrs_orig = mmf2mk.recattrs
        self.recattrs = {}
        for k, v in list(recattrs_orig.items()):
            self.recattrs[v] = k
        self.categories = ""
        exporter_mult.__init__(
            self,
            rd,
            r,
            out,
            conv=conv,
            order=["attr", "ings", "text"],
            attr_order=["title", "cuisine", "category", "yields", "cooktime", "preptime", "rating", "source", "link"],
            convert_attnames=False,
            change_units=change_units,
            mult=mult,
        )

    @pluggable_method
    def _write_attrs_(self):
        self.write_attr_head()
        title = self._grab_attr_(self.r, "title")
        if not title:
            title = ""

        categories = ", ".join([x for x in (self._grab_attr_(self.r, "cuisine"), self._grab_attr_(self.r, "category")) if x])

        yields = self._grab_attr_(self.r, "yields")
        if not yields:  # MealMaster format mandates numeric yield information
            yields = _("%s serving" % str(1))

        self.out.write("     Title: %s\r\n" % title)
        self.out.write("Categories: %s\r\n" % categories)
        self.out.write("     Yield: %s\r\n" % yields)

    def write_head(self):
        self.out.write("MMMMM----- Meal-Master (tm) export from Gourmet Recipe Manager\r\n\r\n")

    def write_attr_foot(self):
        pass

    def pad(self, text, chars):
        text = text.strip()
        fill = chars - len(text)
        return "%s%s" % (" " * fill, text)

    def write_text(self, label, text):
        ll = text.split("\n")
        for line in ll:
            if line == "":
                self.out.write("\r\n")
            else:
                for wrapped_line in textwrap.wrap(line):
                    self.out.write("  %s\r\n" % wrapped_line)

        self.out.write("\r\n")

        if label == "instructions":
            for label in ["preptime", "cooktime", "source", "rating"]:
                text = self._grab_attr_(self.r, label)
                if text:
                    self.out.write("  %s: %s\r\n" % (gglobals.REC_ATTR_DIC[label], text))

            self.out.write("\r\n")

    def write_inghead(self):
        self.master_ings = []  # our big list
        # self.ings is what we add to
        # this can change when we add groups
        self.ings = self.master_ings
        self.ulen = 1
        # the specs we found require 7 blanks to define an ingredient
        self.amtlen = 7
        self.out.write("\r\n")

    def write_grouphead(self, name):
        debug("write_grouphead called with %s" % name, 0)
        group = (name, [])
        self.ings.append(group)  # add to our master
        self.ings = group[1]  # change current list to group list

    def write_groupfoot(self):
        self.ings = self.master_ings  # back to master level

    def write_ing(self, amount="1", unit=None, item=None, key=None, optional=False):
        if isinstance(amount, (float, int)):
            amount = convert.float_to_frac(amount)
            if not amount:
                amount = ""
        if not unit:
            unit = ""
        unit_bad = False
        if len(unit) > 2 or "." in unit:
            unit_bad = True
            # Try to fix the unit
            if unit in self.conv.unit_dict:
                new_u = self.conv.unit_dict[unit]
                if len(new_u) <= 2 and "." not in new_u:
                    unit = new_u
                    unit_bad = False
                else:
                    if new_u in self.uc:
                        unit = self.uc[new_u]
                        unit_bad = False
        if unit_bad:  # If we couldn't fix the unit...  we add it to
            # the item
            if unit:
                item = "%s %s" % (unit, item)
            unit = ""
        if len(unit) > self.ulen:
            self.ulen = len(unit)
        if len(amount) > self.amtlen:
            self.amtlen = len(amount)
            # print "DEBUG: %s length %s"%(amount,self.amtlen)
        # we hold off writing ings until we know the lengths
        # of strings since we need to write out neat columns
        if optional:
            item = "%s (optional)" % item
        self.ings.append([amount, unit, item])

    def write_ingfoot(self):
        """Write all of the ingredients"""
        ## where we actually write the ingredients...
        for i in self.master_ings:
            # if we're a tuple, this is a group...
            if isinstance(i, tuple):
                # write the group title first...
                group = i[0]
                width = 70
                dashes = width - len(group)
                left_side = int(dashes / 2 - 5)
                right_side = int(dashes / 2)
                self.out.write("-----%s%s%s\r\n" % (left_side * "-", group.upper(), right_side * "-"))
                list(map(self._write_ingredient, i[1]))
                self.out.write("\r\n")  # extra newline at end of groups
            else:
                self._write_ingredient(i)
        # we finish with an extra newline
        self.out.write("\r\n")

    def _write_ingredient(self, ing):
        a, u, i = ing
        itemstart = 11
        inglen = 39
        itemlines = textwrap.wrap(i, inglen - itemstart)
        if not itemlines:
            return

        self.out.write("%s %s %s\r\n" % (self.pad(a, self.amtlen), self.pad(u, self.ulen), itemlines[0]))
        for line in islice(itemlines, 1, None):
            self.out.write("%s-%s\r\n" % (" " * itemstart, line))

    def write_foot(self):
        self.out.write("MMMMM")
        self.out.write("\r\n\r\n")
