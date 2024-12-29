from collections import namedtuple

# This structure contains information stored in the database,
# as well as other fields that can be found in imports.
Recipe = namedtuple(
    "Recipe",
    [
        "id",
        "title",
        "instructions",
        "modifications",
        "cuisine",
        "rating",
        "description",
        "source",
        "totaltime",
        "preptime",
        "cooktime",
        "servings",
        "yields",
        "yield_unit",
        "ingredients",
        "image",
        "thumb",
        "deleted",
        "recipe_hash",
        "ingredient_hash",
        "link",
        "last_modified",
        "nutrients",
        "category",
    ],
)
