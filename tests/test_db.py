import tempfile
import pytest

from gourmand.backends import db
from gourmand.plugin_loader import MasterLoader


@pytest.fixture
def database():
    # Remove all plugins for testing purposes
    ml = MasterLoader.instance()
    ml.save_active_plugins = lambda *args: True
    # Don't save anything we do to plugins
    ml.active_plugins = []
    ml.active_plugin_sets = []
    # Done knocking out plugins...
    tmpfile = tempfile.mktemp()
    return db.get_database(file=tmpfile)


def test_recipe_basics(database):
    initial_recipe_count = database.fetch_len(database.recipe_table)

    recipe1 = database.add_rec({'title': 'Fooboo'})
    assert recipe1.title == 'Fooboo'

    recipe2 = database.new_rec()
    recipe2 = database.modify_rec(recipe2, {'title': 'Foo', 'cuisine': 'Bar'})
    assert recipe2.title == 'Foo'
    assert recipe2.cuisine == 'Bar'

    database.delete_rec(recipe1)
    database.delete_rec(recipe2)
    assert database.fetch_len(database.recipe_table) == initial_recipe_count


def test_ingredient_basics(database):
    initial_ingredient_count = database.fetch_len(database.ingredients_table)
    recipe_id = database.new_rec().id
    ingredient1 = database.add_ing(
        {
            'amount': 1,
            'unit': 'c.',
            'item': 'Carrot juice',
            'ingkey': 'juice, carrot',
            'recipe_id': recipe_id,
        }
    )
    ingredient2 = database.add_ing(
        {
            'amount': 2,
            'unit': 'c.',
            'item': 'Tomato juice',
            'ingkey': 'juice, tomato',
            'recipe_id': recipe_id,
        }
    )

    assert len(database.get_ings(recipe_id)) == 2

    ingredient1 = database.modify_ing(ingredient1, {'amount': 2})
    assert ingredient1.amount == 2

    ingredient1 = database.modify_ing(ingredient1, {'unit': 'cup'})
    assert ingredient1.unit == 'cup'

    database.delete_ing(ingredient1)
    database.delete_ing(ingredient2)
    assert database.fetch_len(database.ingredients_table) == initial_ingredient_count


def test_add_multiple_ingredients(database):
    recipe_id = database.new_rec().id
    database.add_ings(
        [
            {
                'rangeamount': None,
                'item': 'water',
                'recipe_id': recipe_id,
                'position': 1,
                'ingkey': 'water',
            },
            {
                'rangeamount': None,
                'item': 'linguine',
                'amount': 0.5,
                'recipe_id': recipe_id,
                'position': 1,
                'ingkey': 'linguine',
                'unit': 'pound',
            },
        ]
    )
    ingredients = database.get_ings(recipe_id)
    assert ingredients[0].item == 'water'
    assert ingredients[1].item == 'linguine'
    assert ingredients[1].unit == 'pound'
    assert ingredients[1].amount == 0.5


def test_ingredients_unique(database):
    # Clear out ingredients
    database.delete_by_criteria(database.ingredients_table, {})

    for ingredient in ['juice, tomato', 'broccoli', 'spinach', 'spinach', 'spinach']:
        database.add_ing(
            {'amount': 1, 'unit': 'c.', 'item': ingredient, 'ingkey': ingredient}
        )

    ingredient_keys = database.get_unique_values('ingkey', database.ingredients_table)
    assert len(ingredient_keys) == 3

    spinach_keys = database.fetch_count(
        database.ingredients_table,
        'ingkey',
        ingkey='spinach',
        sort_by=[('count', -1)],
    )
    assert spinach_keys[0].count == 3
    assert spinach_keys[0].ingkey == 'spinach'


def test_recipe_search(database):
    # Clear out ingredients, recipes and categories
    database.delete_by_criteria(database.ingredients_table, {})
    database.delete_by_criteria(database.recipe_table, {})
    database.delete_by_criteria(database.categories_table, {})
    database.add_rec({'title': 'Foo', 'cuisine': 'Bar', 'source': 'Z'})
    database.add_rec({'title': 'Fooey', 'cuisine': 'Bar', 'source': 'Y'})
    database.add_rec({'title': 'Fooey', 'cuisine': 'Foo', 'source': 'X'})
    database.add_rec({'title': 'Foo', 'cuisine': 'Foo', 'source': 'A'})
    database.add_rec({'title': 'Boe', 'cuisine': 'Fa'})

    result = database.search_recipes(
        [
            {'column': 'deleted', 'search': False, 'operator': '='},
            {'column': 'cuisine', 'search': 'Foo', 'operator': '='},
        ]
    )
    assert len(result) == 2

    result = database.search_recipes(
        [
            {'column': 'deleted', 'search': False, 'operator': '='},
            {'column': 'cuisine', 'search': 'F.*', 'operator': 'REGEXP'},
        ]
    )
    assert len(result) == 3

    result = database.search_recipes(
        [
            {'column': 'deleted', 'search': False, 'operator': '='},
            {'column': 'cuisine', 'search': 'Foo'},
            {'column': 'title', 'search': 'Foo', 'operator': '='},
        ]
    )
    assert len(result) == 1

    result = database.search_recipes(
        [{'column': 'title', 'search': 'Fo.*', 'operator': 'REGEXP'}],
        [('source', 1)],
    )
    assert result[0].title == 'Foo' and result[0].source == 'A'

    # Advanced searching
    database.add_rec({'title': 'Spaghetti', 'category': 'Entree'})
    database.add_rec({'title': 'Quiche', 'category': 'Entree, Low-Fat, High-Carb'})
    assert (
        len(
            database.search_recipes(
                [
                    {'column': 'deleted', 'search': False, 'operator': '='},
                    {'column': 'category', 'search': 'Entree', 'operator': '='},
                ]
            )
        )
        == 2
    )

    # Test fancy multi-category searches...
    assert (
        len(
            database.search_recipes(
                [
                    {'column': 'category', 'search': 'Entree', 'operator': '='},
                    {'column': 'category', 'search': 'Low-Fat', 'operator': '='},
                ]
            )
        )
        == 1
    )

    # Test ingredient search
    recs = database.fetch_all(database.recipe_table)
    r = recs[0]
    database.add_ing({'recipe_id': r.id, 'ingkey': 'apple'})
    database.add_ing({'recipe_id': r.id, 'ingkey': 'cinnamon'})
    database.add_ing({'recipe_id': r.id, 'ingkey': 'sugar, brown'})
    r2 = recs[1]
    database.add_ing({'recipe_id': r2.id, 'ingkey': 'sugar, brown'})
    database.add_ing({'recipe_id': r2.id, 'ingkey': 'flour, all-purpose'})
    database.add_ing({'recipe_id': r2.id, 'ingkey': 'sugar, white'})
    database.add_ing({'recipe_id': r2.id, 'ingkey': 'vanilla extract'})
    r3 = recs[2]
    database.add_ing({'recipe_id': r3.id, 'ingkey': 'sugar, brown'})
    database.add_ing({'recipe_id': r3.id, 'ingkey': 'sugar, brown', 'unit': 'c.'})

    assert (
        len(
            database.search_recipes(
                [
                    {
                        'column': 'ingredient',
                        'search': 'sugar%',
                        'operator': 'LIKE',
                    }
                ]
            )
        )
        == 3
    )

    assert (
        len(
            database.search_recipes(
                [
                    {'column': 'ingredient', 'search': 'sugar, brown'},
                    {'column': 'ingredient', 'search': 'apple'},
                ]
            )
        )
        == 1
    )


def test_unicode_records(database):
    recipe = database.add_rec(
        {
            'title': '🥞',
            'source': '🍰',
            'category': 'C\xc6sar',
        }
    )
    assert recipe.title == '🥞'
    assert recipe.source == '🍰'

    recipe = database.modify_rec(recipe, {'title': '\xc1 Comida de \xc1guila'})
    assert recipe.title == '\xc1 Comida de \xc1guila'

    ingredient = database.add_ing_and_update_keydic(
        {
            'recipe_id': recipe.id,
            'amount': 1.0,
            'unit': '🥚🥓',
            'item': '🥚🥓',
            'ingkey': '🥚🥓',
        }
    )
    for attr in 'unit', 'item', 'ingkey':
        assert getattr(ingredient, attr) == '🥚🥓'


def test_ID_reservation(database):
    recipe_id1 = database.new_id()
    recipe_id2 = database.new_id()
    recipe1 = database.add_rec({'title': 'intermittent'})
    recipe2 = database.add_rec({'title': 'intermittent2'})
    recipe3 = database.add_rec({'title': 'intermittent3'})
    recipe4 = database.add_rec({'title': 'reserved', 'id': recipe_id1})
    recipe5 = database.add_rec({'title': 'reserved2', 'id': recipe_id2})

    assert recipe4.id == recipe_id1

    for r in [recipe1, recipe2, recipe3, recipe4, recipe5]:
        database.delete_rec(r)


img = (
    b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff'
    b'\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14'
    b'\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $'
    b'.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xdb\x00C\x01\t\t\t\x0c\x0b'
    b'\x0c\x18\r\r\x182!\x1c!2222222222222222222222222222222222222222222222222'
    b'2\xff\xc0\x00\x11\x08\x00(\x00#\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff'
    b'\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\x00\xb5\x10'
    b'\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04\x04\x00\x00\x01}\x01\x02'
    b'\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa\x07"q\x142\x81\x91\xa1\x08#B\xb1'
    b'\xc1\x15R\xd1\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&\'()*456789:CDEFGHIJS'
    b'TUVWXYZcdefghijstuvwxyz\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95'
    b'\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5'
    b'\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5'
    b'\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3'
    b'\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xc4\x00\x1f\x01\x00\x03\x01\x01\x01\x01'
    b'\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07'
    b'\x08\t\n\x0b\xff\xc4\x00\xb5\x11\x00\x02\x01\x02\x04\x04\x03\x04\x07\x05'
    b'\x04\x04\x00\x01\x02w\x00\x01\x02\x03\x11\x04\x05!1\x06\x12AQ\x07aq\x13"'
    b'2\x81\x08\x14B\x91\xa1\xb1\xc1\t#3R\xf0\x15br\xd1\n\x16$4\xe1%\xf1\x17'
    b'\x18\x19\x1a&\'()*56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x82\x83\x84\x85'
    b'\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5'
    b'\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5'
    b'\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe2\xe3\xe4\xe5'
    b'\xe6\xe7\xe8\xe9\xea\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xda\x00\x0c'
    b'\x03\x01\x00\x02\x11\x03\x11\x00?\x00\xf5\x01#r\xc0\x1c\x01\x92q\xd0S'
    b'\x9a\xea+x\x1a{\xa9\x92(\x82\x16R\xc7n\xefl\x9e+\x07\xc6z\xf0\xd3$\x16p'
    b'\xa4A\xf2\xb2d\xb1S\x8eq\xfc\'=\xff\x00:\xcf\x9a\xf7Q\xf1O\x85\x9eDB\xa9'
    b'\x14\xdbJ\xc7\xceO\xe4\x0f\x7f\xd6\xaeUU\xb4*4\x9bj\xfb\x1d5\x9e\xadk}m'
    b'\xba\x19\xe3\x92U8a\x1b\x02\x05`k\xfe\'m1\x84\x0bl\x1d\x87F.F>\xb8\xebSh'
    b'Ki\xa0\xe9-4\xf8I\xe7E\r\xba,\x98\xd8\x03\x81\x8c\xe4\xf5\xcf^A\x14\x96'
    b'\x97:>\xb5rl\xae\x00\xbd\x91\x8b"\xbbB\xcaz\xfd\xe1\xe9\xeb\xc1\x1c}1I'
    b'\xc9\xc9+n5\x15\x17\xaa\xba,\xe9\xda\xb5\xd6\xa3a\r\xdb\xa2\xabH2F\x07c'
    b'\x8f\xe9Etp\xd9\xc1o\x04p\xc5\x10\x11\xc6\xa1T{\n+U-52v\xbe\x86\x0f\x8c'
    b'\xbc2\xfa\xcc\x90\xdc@3 \xc4dd\x0f\xa7\xf3\xadm\x13H\x87C\xd2\xa2\xb2'
    b'\x1f31\xdc\xe4\x0e\x0b\x1cg\xf9\x01Z\x8e\xe7#\x18\x1e\xe6\xa2\xbb\xbb'
    b'\x8a\xd9Y\x9d\x86\xc03\x9a\xc9E\'r\xdc\xdb\x8f)\xc6\xfcF\xd3e\xb9\xb3'
    b'\x82\xea0\xc7h*v\xfey\xff\x00>\x95\x93\xf0\xfbIxo\x1e\xfex\xdbj\x02\xa8I'
    b'\xfe#\xd7\xf4\xcf\xe7]\xcc\x97\xd1\xdd\xda\xc8\x8a\x98S\xf2\xe5\xfe\\'
    b'\xfd;\xf1\x8c\xfe\x1d\xba\xd3\x86AX\xc4,\x15F7\xed\x00\x13\xdf\x8c\xf1'
    b'\xcei{?{\x98~\xd3\xdc\xe5,1%\x89\x07\x03\xd0QF(\xadL\xc9\xd9\xc6*\xa5'
    b'\xec"x\n\xed\xdcr\x1b\x1e\xb84QR\x80\xa0\xc8\xb3C\xf6i"|0\xc6\x0eG\x1f^'
    b'\xb9\xabS\\}\x968`p\xca\xa3\x01X\xe4\x8f\xc4\xff\x00\x8d\x14U\x89\n\xf7'
    b'r+m\x8ebT\x01\x8c-\x14QH\x0f\xff\xd9'
)


def test_recipe_image(database):
    r = database.add_rec({'image': img})
    assert r.image == img


def test_update_by_criteria(database):
    r = database.add_rec({'title': 'Foo', 'cuisine': 'Bar', 'source': 'Z'})

    database.update_by_criteria(
        database.recipe_table, {'title': 'Foo'}, {'title': 'Boo'}
    )

    assert database.get_rec(r.id).title == 'Boo'


def test_modify_recipe(database):
    orig_attrs = {
        'title': 'Foo',
        'cuisine': 'Bar',
        'yields': 7,
        'yield_unit': 'cups',
    }
    new_attrs = {
        'title': 'Foob',
        'cuisine': 'Baz',
        'yields': 4,
        'yield_unit': 'servings',
    }
    recipe = database.add_rec(orig_attrs.copy())

    for new_attr, new_val in new_attrs.items():
        recipe = database.modify_rec(recipe, {new_attr: new_val})
        # Make sure our value changed...
        assert getattr(recipe, new_attr) == new_val
        # Make sure no other values changed
        for old_attr, old_val in orig_attrs.items():
            if old_attr != new_attr:
                assert getattr(recipe, old_attr), old_val
        # Change back our recipe
        recipe = database.modify_rec(recipe, {new_attr: orig_attrs[new_attr]})


def test_modify_ingredient(database):
    r = database.add_rec({'title': 'itest'})
    orig_attrs = {
        'item': 'Foo',
        'ingkey': 'Bar',
        'amount': 7,
        'unit': 'cups',
        'optional': True,
        'rangeamount': None,
        'recipe_id': r.id,
    }
    new_attrs = {
        'item': 'Fooz',
        'ingkey': 'Baz',
        'amount': 3,
        'unit': 'ounces',
        'optional': False,
        'rangeamount': 2,
    }
    ingredient = database.add_ing(orig_attrs.copy())
    for new_attr, new_val in list(new_attrs.items()):
        ingredient = database.modify_ing(ingredient, {new_attr: new_val})
        # Make sure our value changed...
        assert getattr(ingredient, new_attr) == new_val
        # Make sure no other values changed
        for old_attr, old_val in list(orig_attrs.items()):
            if old_attr != new_attr:
                assert getattr(ingredient, old_attr) == old_val
        # Change back our ingredient...
        ingredient = database.modify_ing(ingredient, {new_attr: orig_attrs[new_attr]})


def test_format_amount_string_from_amount():
    ret = db.RecData.format_amount_string_from_amount((0.5, 1))
    assert ret == '½-1'

    ret = db.RecData.format_amount_string_from_amount((1.0, 1.5))
    assert ret == '1-1 ½'

    ret = db.RecData.format_amount_string_from_amount((1.5, 2))
    assert ret == '1 ½-2'

    ret = db.RecData.format_amount_string_from_amount((1.5, 2.5))
    assert ret == '1 ½-2 ½'

    ret = db.RecData.format_amount_string_from_amount((1.5, 2.5))
    assert ret == '1 ½-2 ½'
