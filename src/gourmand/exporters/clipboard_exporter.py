"""Export a recipe to the system's clipboard or via drag and drop.

This plugin demonstrates how to create an export plugin.
"""

from gi.repository import Gdk, Gtk


def _format(recipes):
    """Format recipes as a string.

    The expected list should contain tupes of (recipe, ingredients) that
    belong together.
    """
    # recipes = List[Tuple["RowProxy", "RowProxy"]]
    formatted_recipes = []

    # Each item in self.recipes is a set of (a recipe, its ingredients).
    for recipe, ingredients in recipes:

        # The ingredients have the name, quantity, and units attached
        formatted_ingredients = []
        for ingredient in ingredients:
            string = f"{ingredient.amount} " if ingredient.amount else ""
            string += f"{ingredient.unit} " if ingredient.unit else ""
            string += ingredient.item
            formatted_ingredients.append(string)

        formatted_ingredients = "\n".join(formatted_ingredients)

        # Now that the ingredients are formatted, the title, yield,
        # description etc. can be extracted.
        # The rating, for instance, is omitted: let the recipient make
        # their opinion!
        formatted_recipe = f"# {recipe.title}\n\n"
        formatted_recipe += f"{recipe.source}\n" if recipe.source else ""
        formatted_recipe += f"{recipe.link}\n" if recipe.link else ""
        formatted_recipe += "\n" if recipe.source or recipe.link else ""
        formatted_recipe += f"{recipe.yields} {recipe.yield_unit}\n\n" if recipe.yields else ""

        formatted_recipe += f"{recipe.description}\n\n" if recipe.description else ""
        formatted_recipe += f"{formatted_ingredients}\n\n"

        formatted_recipe += f"{recipe.instructions}\n"

        formatted_recipes.append(formatted_recipe)

    # Join all the recipes as one string.
    formatted_recipes = "\n\n".join(formatted_recipes)

    # Although not used here, the image can also be retrieved.
    # They are stored as jpegs in the database:
    # if recipe.image is not None:
    #     image_filename = self.export_path / f'{recipe.title}.jpg'
    #     with open(image_filename, 'wb') as fout:
    #         fout.write(recipe.image)

    return formatted_recipes


def copy_to_clipboard(recipes):
    # recipes = List[Tuple["RowProxy", "RowProxy"]]
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    formatted_recipes = _format(recipes)
    clipboard.set_text(formatted_recipes, -1)


def copy_to_drag(recipes, widget: Gtk.TreeView, drag_context: Gdk.DragContext, data: Gtk.SelectionData, info: int, time: int) -> bool:
    """Export recipes to text via drag and drop.

    This function is expected to be connected to a signal.
    If so, the signal will be done being handled here.
    """
    # recipes = List[Tuple["RowProxy", "RowProxy"]]
    if info == 0:  # Only support text export
        data.set_text(_format(recipes), -1)
    return True  # Done handling signal
