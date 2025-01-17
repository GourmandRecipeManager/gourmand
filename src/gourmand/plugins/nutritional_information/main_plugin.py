from gourmand.gglobals import add_icon as _add_icon
from gourmand.i18n import _
from gourmand.image_utils import load_pixbuf_from_resource
from gourmand.plugin import MainPlugin

from . import nutrition, nutritionGrabberGui


class NutritionMainPlugin(MainPlugin):

    def activate(self, pluggable):
        """Setup nutritional database stuff."""
        pixbuf = load_pixbuf_from_resource("Nutrition.png")
        _add_icon(pixbuf, "nutritional-info", _("Nutritional Information"))
        nutritionGrabberGui.check_for_db(pluggable.rd)
        pluggable.nd = nutrition.NutritionData(pluggable.rd, pluggable.conv)
        pluggable.rd.nd = pluggable.nd
