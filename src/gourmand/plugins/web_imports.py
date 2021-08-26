"""Import recipes from the web using recipe-scrapers."""
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse

from recipe_scrapers import SCRAPERS, scrape_me
from gourmand.structure import Recipe
from gourmand.image_utils import ImageBrowser, make_thumbnail 


# The following imformation are used within the Plugin window
AUTHOR = 'Gourmand Team'
COPYRIGHT = 'MIT'
WEBSITE = ''


def load(urls: List[str]) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Import recipes.

    urls is a list of urls which will be imported one after the other.

    The supported sites are listed here:
    https://github.com/hhursev/recipe-scrapers#scrapers-available-for

    This function is called by Gourmand.

    The import function is always expected to return two lists: one of
    imported recipes and one of failed imported urls or files.

    Gourmand can then store the imported recipes and notify the users of
    any failures.
    """
    recipes = []
    failed: List[str] = []

    # Filter websites that are not supported by recipe-scrapers.
    for url in urls:
        url_ = urlparse(url).netloc.strip('www.')
        if url_ not in SCRAPERS.keys():
            failed.append(url)
            urls.remove(url)

    for url in urls:
        recipe = scrape_me(url)
        # Fetch the image if available, or else open an ImageBrowser
        # to let the user select one.
        if recipe.image():
            image = make_thumbnail(recipe.image())
        else:
            uris = []
            for schema in recipe.links():
                link = schema.get('href', '')
                if link.endswith('jpg'):
                    uris.append(link)
            image = ImageBrowser(uris=uris)

        # Gourmet has a 5-stars rating, stored as int between 0 and 10.
        # We assume that if the value is a float below 5, it's scaled to 5, and
        # we rescale it to 10.
        rating = recipe.ratings()
        if isinstance(rating, float) and rating <= 5.0:
            rating = rating * 2
        rating = int(rating)

        # recipe_scrapers keeps servings, yield, and yield units in one string
        yields, yield_unit = recipe.yields().split()
        yields = int(yields)

        # Convert the recipe into the expected namedtuple `recipe_tuple`
        # expected by the rest of the application.
        rec = Recipe(
                id=None,
                title=recipe.title(),
                instructions=recipe.instructions(),
                modifications=None,
                cuisine=None,
                rating=rating,
                description=None,
                source=recipe.author(),  # TODO: could this be done better?
                totaltime=recipe.total_time(),
                preptime=None,  # TODO: future recipe_scrapers will have them
                cooktime=None,  # TODO: future recipe_scrapers will have them
                servings=yields,
                yields=yields,
                yield_unit=yield_unit,
                ingredients=recipe.ingredients(),
                image=image,
                thumb=image,
                deleted=False,
                recipe_hash=None,
                ingredient_hash=None,
                link=recipe.canonical_url(),
                last_modified=None,
                nutrients=recipe.nutrients()
                )
        recipes.append(rec)

    return recipes, failed
