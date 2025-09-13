"""Import recipes from the web using recipe-scrapers."""

from typing import List, Tuple
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from gi.repository import Gtk
from recipe_scrapers import SCRAPERS, scrape_html
from recipe_scrapers._exceptions import SchemaOrgException

from gourmand import __version__
from gourmand.gdebug import debug
from gourmand.image_utils import ImageBrowser, image_to_bytes, make_thumbnail
from gourmand.recipeManager import get_recipe_manager
from gourmand.structure import Recipe

supported_sites = list(SCRAPERS.keys())
HEADERS = {
    "User-Agent": f"Mozilla/5.0 (compatible; Windows NT 10.0; Win64; x64) gourmand/{__version__}"
}


def import_urls(urls: List[str]) -> Tuple[List[str], List[str]]:
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
    imported: List[str] = []
    unsupported: List[str] = []
    database = get_recipe_manager()

    # Filter websites that are not supported by recipe-scrapers.
    for url in urls:
        url_ = urlparse(url).netloc.strip("www.")
        if url_ not in supported_sites:
            unsupported.append(url)
            urls.remove(url)

    for url in urls:
        req = Request(url, headers=HEADERS)
        try:
            with urlopen(req) as response:
                html = response.read()
        except URLError as e:
            debug('The server could not fulfill the request.', 1)
            debug(f'Reason: {e.reason}', 1)
            continue
        recipe = scrape_html(html, org_url=url)

        # Fetch the image if available, or else open an ImageBrowser
        # to let the user select one.
        image = thumbnail = None
        image, thumbnail = capture_image_and_thumbnail(recipe)

        # Create local Recipe object
        rec = initialize_recipe(recipe, image, thumbnail)
        rec = rec._asdict()
        rec.pop("id")
        rec.pop("servings")
        recipe_id = database.add_rec(rec)["id"]

        ingredients = [database.parse_ingredient(ingredient) for ingredient in recipe.ingredients()]
        for position, ingredient in enumerate(ingredients):
            ingredient["recipe_id"] = recipe_id
            ingredient["position"] = position
            ingredient["deleted"] = False
        database.add_ings(ingredients)

        imported.append(url)

    return imported, unsupported


def capture_image_and_thumbnail(scraped_recipe):
    image = thumbnail = None

    if scraped_recipe.image():
        image = make_thumbnail(scraped_recipe.image())
        thumbnail = image.copy()
        thumbnail.thumbnail((40, 40))
        thumbnail = image_to_bytes(thumbnail)
        image = image_to_bytes(image)
    else:
        uris = []
        for schema in scraped_recipe.links():
            link = schema.get("href", "")
            if link.endswith("jpg"):
                uris.append(link)
        browser = ImageBrowser(parent=None, uris=uris)
        response = browser.run()
        browser.destroy()
        if response == Gtk.ResponseType.OK:
            thumbnail = browser.image.copy()
            thumbnail.thumbnail((40, 40))
            thumbnail = image_to_bytes(thumbnail)
            image = image_to_bytes(browser.image)

    return image, thumbnail


def initialize_recipe(recipe_scraped, image=None, thumbnail=None):
    # If a recipe doesn't have all the expected information a
    # SchemaOrgException is raised.  Catch it and assign a default
    # rating value.
    try:
        rating = recipe_scraped.ratings()
    except SchemaOrgException:
        rating = 0
    # Gourmet has a 5-stars rating, stored as int between 0 and 10.
    # We assume that if the value is a float below 5, it's scaled to 5, and
    # we rescale it to 10.
    if isinstance(rating, float) and rating <= 5.0:
        rating = rating * 2
    rating = int(rating)

    # recipe_scrapers keeps servings, yield, and yield units in one string
    yields, yield_unit = recipe_scraped.yields().split()
    yields = int(yields)

    # Convert the recipe into the expected namedtuple `recipe_tuple`
    # expected by the rest of the application.
    try:
        preptime = recipe_scraped.schema.prep_time()
        cooktime = recipe_scraped.schema.cook_time()
    except SchemaOrgException:
        preptime = ""
        cooktime = ""

    rec = Recipe(
        id=None,
        title=recipe_scraped.title(),
        instructions=recipe_scraped.instructions(),
        modifications=None,
        cuisine="",
        rating=rating,
        description="",
        source=recipe_scraped.author(),
        totaltime=recipe_scraped.total_time(),
        preptime=preptime,
        cooktime=cooktime,
        servings=yields,
        yields=yields,
        yield_unit=yield_unit,
        ingredients=recipe_scraped.ingredients(),
        image=image,
        thumb=thumbnail,
        deleted=False,
        recipe_hash=None,
        ingredient_hash=None,
        link=recipe_scraped.canonical_url(),
        last_modified=None,
        nutrients=recipe_scraped.nutrients(),
        category=recipe_scraped.category(),
    )

    return rec
