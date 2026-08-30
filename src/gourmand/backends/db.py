import re
import shutil
import time
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from gi.repository import Gtk
from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    LargeBinary,
    MetaData,
    Numeric,
    String,
    Table,
    Text,
    and_,
    asc,
    case,
    create_engine,
    delete,
    desc,
    event,
    func,
    insert,
    or_,
    select,
    text,
    update,
)
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import registry

import gourmand.__version__
import gourmand.gglobals as gglobals
import gourmand.recipeIdentifier as recipeIdentifier
from gourmand import Undo, convert, image_utils
from gourmand.defaults import lang as defaults
from gourmand.gdebug import TimeAction, debug
from gourmand.gtk_extras.dialog_extras import show_message
from gourmand.i18n import _
from gourmand.keymanager import KeyManager
from gourmand.optionparser import args
from gourmand.plugin import DatabasePlugin
from gourmand.plugin_loader import Pluggable, pluggable_method

# Follow commandline db specification if given
dbargs = {}

if "file" not in dbargs:
    dbargs["file"] = gglobals.gourmanddir / "recipes.db"
if args.db_url:
    print("We have a db_url and it is,", args.db_url)
    dbargs["custom_url"] = args.db_url

mapper_registry = registry()


def map_type_to_sqlalchemy(typ):
    """A convenience method -- take a string type and map it into a
    sqlalchemy type.
    """
    if typ == "int":
        return Integer()
    if typ.find("char(") == 0:
        return String(length=int(typ[typ.find("(") + 1 : typ.find(")")]))
    if typ == "text":
        return Text()
    if typ == "bool":
        return Boolean()
    if typ == "float":
        return Float()
    if typ == "binary":
        return LargeBinary()


def fix_colnames(dict, *tables):
    """Map column names to sqlalchemy columns."""
    # This is a convenience method -- throughout Gourmet, the column
    # names are handed around as strings. This converts them into the
    # object sqlalchemy prefers.
    newdict = {}
    for k, v in list(dict.items()):
        got_prop = False
        for t in tables:
            try:
                newdict[getattr(t.c, k)] = v
            except Exception:
                pass
            else:
                got_prop = True
        if not got_prop:
            raise ValueError("Could not find column %s in tables %s" % (k, tables))
    return newdict


def make_simple_select_arg(criteria, *tables):
    args = []
    for k, v in list(fix_colnames(criteria, *tables).items()):
        if isinstance(v, str):
            v = str(v)
        if isinstance(v, tuple):
            operator, value = v
            if isinstance(value, str):
                value = str(value)
            if operator == "in":
                args.append(k.in_(value))
            elif hasattr(k, operator):
                args.append(getattr(k, operator)(value))
            elif hasattr(k, operator + "_"):  # for keywords like 'in'
                args.append(getattr(k, operator + "_")(value))
            else:
                args.append(k.op(operator)(value))
        else:
            args.append(k == v)
    if len(args) > 1:
        return [and_(*args)]
    elif args:
        return [args[0]]
    else:
        return []


def make_order_by(sort_by, table, count_by=None, join_tables=None):
    if join_tables is None:
        join_tables = []

    ret = []
    for col, direction in sort_by:
        if col == "count" and not hasattr(table.c, "count"):
            col = func.count(getattr(table.c, count_by))
        else:
            if hasattr(table.c, col):
                col = getattr(table.c, col)
            elif join_tables:
                broken = True
                for t in join_tables:
                    if hasattr(t.c, col):
                        broken = False
                        col = getattr(t.c, col)
                        break
                if broken:
                    raise ValueError(f"No such column for tables {table} {join_tables}: {col}")
        if isinstance(col.type, Text):
            # Sort nulls last rather than first using case statement...
            col = case(
                (col.is_(None), '"%s"' % "z" * 20),
                (col == "", '"%s"' % "z" * 20),
                else_=func.lower(col),
            )
        if direction == 1:
            ret.append(asc(col))
        else:
            ret.append(desc(col))
    return ret


class DBObject:
    pass


# CHANGES SINCE PREVIOUS VERSIONS...
# categories_table: id -> recipe_id, category_entry_id -> id
# ingredients_table: ingredient_id -> id, id -> recipe_id


def db_url(filename: Optional[str] = None, custom_url: Optional[str] = None) -> str:
    if custom_url is not None:
        return custom_url
    else:
        if filename is None:
            filename = gglobals.gourmanddir / "recipes.db"
        return "sqlite:///" + str(filename)


class RecData(Pluggable):
    """RecData is our base class for handling database connections.

    Subclasses implement specific backends, such as sqlite, etc."""

    # constants for determining how to get amounts when there are ranges.
    AMT_MODE_LOW = 0
    AMT_MODE_AVERAGE = 1
    AMT_MODE_HIGH = 2

    _instance_by_db_url = {}

    @classmethod
    def instance_for(cls, file: Optional[str] = None, custom_url: Optional[str] = None) -> "RecData":
        url = db_url(file, custom_url)

        if url not in cls._instance_by_db_url:
            cls._instance_by_db_url[url] = cls(file, url)

        return cls._instance_by_db_url[url]

    def __init__(self, file: str, url: str):
        # hooks run after adding, modifying or deleting a recipe.
        # Each hook is handed the recipe, except for delete_hooks,
        # which is handed the ID (since the recipe has been deleted)
        # We keep track of IDs we've handed out with new_id() in order
        # to prevent collisions
        self.new_ids = []
        self._created = False
        self.filename = file
        self.url = url
        self.add_hooks = []
        self.modify_hooks = []
        self.delete_hooks = []
        self.add_ing_hooks = []

        timer = TimeAction("initialize_connection + setup_tables", 2)
        self.initialize_connection()
        super().__init__([DatabasePlugin])
        self.setup_tables()
        self.metadata.create_all(self.db)
        self.update_version_info(gourmand.__version__.version)
        self._created = True
        timer.end()

    # Basic setup functions

    def initialize_connection(self):
        """Initialize our database connection."""
        debug("Initializing DB connection", 1)
        self.new_db = False

        connect_args = {}
        if self.url.startswith("mysql"):
            connect_args["charset"] = "utf8mb4"

        self.db = create_engine(self.url, connect_args=connect_args)

        if self.url.startswith("sqlite"):
            def regexp(expr, item):
                if item:
                    return re.search(expr, item, re.IGNORECASE) is not None
                return False

            @event.listens_for(self.db, "connect")
            def on_connect(dbapi_con, con_record):
                dbapi_con.create_function("REGEXP", 2, regexp)

        self.metadata = MetaData()
        debug("Done initializing DB connection", 1)

    def save(self):
        """Save our database (if there is a separate 'save')"""
        row = self.fetch_one(self.info_table)
        if row:
            self.do_modify(
                self.info_table,
                row,
                {"last_access": time.time()},
                id_col=None,
            )
        else:
            self.do_add(self.info_table, {"last_access": time.time()})

    def _setup_object_for_table(self, table, klass):
        self.__table_to_object__[table] = klass

        if any(col.primary_key for col in table.columns):
            klass_path = f"{klass.__module__}.{klass.__name__}"
            mapped_paths = {
                f"{m.class_.__module__}.{m.class_.__name__}"
                for m in mapper_registry.mappers
            }

            if klass_path not in mapped_paths:
                mapper_registry.map_imperatively(klass, table)
        else:
            raise Exception(
                "All tables need a primary key -- specify "
                f"'rowid'/Integer/Primary Key in table spec for {table}"
            )

    @pluggable_method
    def setup_tables(self):
        """Subclasses do adjustments/tweaking before calling this."""
        self.__table_to_object__ = {}
        self.setup_base_tables()
        self.setup_shopper_tables()

    def setup_base_tables(self):
        self.setup_info_table()
        self.setup_recipe_table()
        self.setup_category_table()
        self.setup_ingredient_table()

    def setup_info_table(self):
        self.info_table = Table(
            "info",
            self.metadata,
            Column("version_super", Integer()),
            Column("version_major", Integer()),
            Column("version_minor", Integer()),
            Column("last_access", Integer()),
            Column("rowid", Integer(), primary_key=True),
            extend_existing=True,
        )

        class Info:
            pass

        self._setup_object_for_table(self.info_table, Info)

        self.plugin_info_table = Table(
            "plugin_info",
            self.metadata,
            Column("plugin", Text()),
            Column("id", Integer(), primary_key=True),
            Column("version_super", Integer()),
            Column("version_major", Integer()),
            Column("version_minor", Integer()),
            Column("plugin_version", String(length=32)),
            extend_existing=True,
        )

        class PluginInfo:
            pass

        self._setup_object_for_table(self.plugin_info_table, PluginInfo)


    def setup_recipe_table(self):
        self.recipe_table = Table(
            "recipe",
            self.metadata,
            Column("id", Integer(), primary_key=True),
            Column("title", Text()),
            Column("instructions", Text()),
            Column("modifications", Text()),
            Column("cuisine", Text()),
            Column("rating", Integer()),
            Column("description", Text()),
            Column("source", Text()),
            Column("preptime", Integer()),
            Column("cooktime", Integer()),
            # Note: servings is a legacy column replaced by yields.
            Column("servings", Float()),
            Column("yields", Float()),
            Column("yield_unit", String(length=32)),
            Column("image", LargeBinary()),
            Column("thumb", LargeBinary()),
            Column("deleted", Boolean()),
            Column("recipe_hash", String(length=32)),
            Column("ingredient_hash", String(length=32)),
            Column("link", Text()),
            Column("last_modified", Integer()),
            extend_existing=True,
        )

        class Recipe:
            pass

        self._setup_object_for_table(self.recipe_table, Recipe)

    def setup_category_table(self):
        self.categories_table = Table(
            "categories",
            self.metadata,
            Column("id", Integer(), primary_key=True),
            Column("recipe_id", Integer, ForeignKey("recipe.id")),
            Column("category", Text()),
            extend_existing=True,
        )

        class Category:
            pass

        self._setup_object_for_table(self.categories_table, Category)

    def setup_ingredient_table(self):
        self.ingredients_table = Table(
            "ingredients",
            self.metadata,
            Column("id", Integer(), primary_key=True),
            Column("recipe_id", Integer, ForeignKey("recipe.id")),
            Column("refid", Integer, ForeignKey("recipe.id")),
            Column("unit", Text()),
            Column("amount", Float()),
            Column("rangeamount", Float()),
            Column("item", Text()),
            Column("ingkey", Text()),
            Column("optional", Boolean()),
            Column("shopoptional", Integer()),
            Column("inggroup", Text()),
            Column("position", Integer()),
            Column("deleted", Boolean()),
            extend_existing=True,
        )

        class Ingredient:
            pass

        self._setup_object_for_table(self.ingredients_table, Ingredient)

    def setup_keylookup_table(self):
        self.keylookup_table = Table(
            "keylookup",
            self.metadata,
            Column("id", Integer(), primary_key=True),
            Column("word", Text()),
            Column("item", Text()),
            Column("ingkey", Text()),
            Column("count", Integer()),
            extend_existing=True,
        )

        class KeyLookup:
            pass

        self._setup_object_for_table(self.keylookup_table, KeyLookup)

    def setup_shopcats_table(self):
        self.shopcats_table = Table(
            "shopcats",
            self.metadata,
            Column("id", Integer(), primary_key=True),
            Column("ingkey", Text(32)),
            Column("shopcategory", Text()),
            Column("position", Integer()),
            extend_existing=True,
        )

        class ShopCat:
            pass

        self._setup_object_for_table(self.shopcats_table, ShopCat)

    def setup_shopcatsorder_table(self):
        self.shopcatsorder_table = Table(
            "shopcatsorder",
            self.metadata,
            Column("id", Integer(), primary_key=True),
            Column("shopcategory", Text(32)),
            Column("position", Integer()),
            extend_existing=True,
        )

        class ShopCatOrder:
            pass

        self._setup_object_for_table(
            self.shopcatsorder_table, ShopCatOrder
        )

    def setup_pantry_table(self):
        self.pantry_table = Table(
            "pantry",
            self.metadata,
            Column("id", Integer(), primary_key=True),
            Column("ingkey", Text(32)),
            Column("pantry", Boolean()),
            extend_existing=True,
        )

        class Pantry:
            pass

        self._setup_object_for_table(self.pantry_table, Pantry)

    def setup_density_table(self):
        self.density_table = Table(
            "density",
            self.metadata,
            Column("id", Integer(), primary_key=True),
            Column("dkey", String(length=150)),
            Column("value", String(length=150)),
            extend_existing=True,
        )

        class Density:
            pass

        self._setup_object_for_table(self.density_table, Density)


    def setup_crossunitdict_table(self):
        self.crossunitdict_table = Table(
            "crossunitdict",
            self.metadata,
            Column("id", Integer(), primary_key=True),
            Column("cukey", String(length=150)),
            Column("value", String(length=150)),
            extend_existing=True,
        )

        class CrossUnit:
            pass

        self._setup_object_for_table(
            self.crossunitdict_table, CrossUnit
        )

    def setup_unitdict_table(self):
        self.unitdict_table = Table(
            "unitdict",
            self.metadata,
            Column("id", Integer(), primary_key=True),
            Column("ukey", String(length=150)),
            Column("value", String(length=150)),
            extend_existing=True,
        )

        class Unitdict:
            pass

        self._setup_object_for_table(self.unitdict_table, Unitdict)

    def setup_convtable_table(self):
        self.convtable_table = Table(
            "convtable",
            self.metadata,
            Column("id", Integer(), primary_key=True),
            Column("ckey", String(length=150)),
            Column("value", String(length=150)),
            extend_existing=True,
        )

        class Convtable:
            pass

        self._setup_object_for_table(self.convtable_table, Convtable)

    def setup_shopper_tables(self):
        self.setup_keylookup_table()
        self.setup_shopcats_table()
        self.setup_shopcatsorder_table()
        self.setup_pantry_table()
        self.setup_density_table()
        self.setup_crossunitdict_table()
        self.setup_unitdict_table()
        self.setup_convtable_table()

    def update_version_info(self, version_string: str):
        """Report our version to the database.

        If necessary, we'll do some version-dependent updates to the GUI
        """
        version = version_string.split(".")
        current_super = int(version[0])
        current_major = int(version[1])
        current_minor = int(version[2])

        stored_info = self.fetch_one(self.info_table)

        has_valid_v = stored_info and (
            stored_info.version_super or stored_info.version_major
        )
        if not stored_info or not has_valid_v:
            default_info = {
                "version_super": 0,
                "version_major": 11,
                "version_minor": 0,
            }
            if not stored_info:
                if not self.new_db:
                    self.do_add(self.info_table, default_info)
                else:
                    self.do_add(
                        self.info_table,
                        {
                            "version_super": current_super,
                            "version_major": current_major,
                            "version_minor": current_minor,
                        },
                    )
            else:
                self.do_modify(
                    self.info_table, stored_info, default_info, id_col=None
                )
            stored_info = self.fetch_one(self.info_table)

        if not self.new_db:
            sv_text = (
                f"{stored_info.version_super}."
                f"{stored_info.version_major}."
                f"{stored_info.version_minor}"
            )

            # --- UPGRADE TO 0.16.0 ---
            is_v16_legacy = (
                stored_info.version_super == 0
                and stored_info.version_major < 16
            )
            if is_v16_legacy:
                print("Database older than 0.16.0 -- updating", sv_text)
                backup_database(self.filename)

                with self.db.connect() as conn:
                    stmt1 = (
                        update(self.pantry_table)
                        .where(self.pantry_table.c.pantry == "I01\n.")
                        .values(pantry=True)
                    )
                    conn.execute(stmt1)

                    stmt2 = (
                        update(self.pantry_table)
                        .where(self.pantry_table.c.pantry == "I00\n.")
                        .values(pantry=False)
                    )
                    conn.execute(stmt2)

                    sc_tbl = self.shopcats_table
                    stmt3 = (
                        update(sc_tbl)
                        .where(
                            and_(
                                sc_tbl.c.shopcategory.startswith("S'"),
                                sc_tbl.c.shopcategory.endswith(
                                    "'\np0\n."
                                ),
                            )
                        )
                        .values(
                            {
                                sc_tbl.c.shopcategory: func.substr(
                                    sc_tbl.c.shopcategory,
                                    3,
                                    func.char_length(
                                        sc_tbl.c.shopcategory
                                    )
                                    - 8,
                                )
                            }
                        )
                    )
                    conn.execute(stmt3)
                    conn.commit()

                self.alter_table(
                    "shopcats",
                    self.setup_shopcats_table,
                    {},
                    ["ingkey", "shopcategory", "position"],
                )
                self.alter_table(
                    "shopcatsorder",
                    self.setup_shopcatsorder_table,
                    {},
                    ["shopcategory", "position"],
                )
                self.alter_table(
                    "pantry",
                    self.setup_pantry_table,
                    {},
                    ["ingkey", "pantry"],
                )
                self.alter_table(
                    "density",
                    self.setup_density_table,
                    {},
                    ["dkey", "value"],
                )
                self.alter_table(
                    "crossunitdict",
                    self.setup_crossunitdict_table,
                    {},
                    ["cukey", "value"],
                )
                self.alter_table(
                    "unitdict",
                    self.setup_unitdict_table,
                    {},
                    ["ukey", "value"],
                )
                self.alter_table(
                    "convtable",
                    self.setup_convtable_table,
                    {},
                    ["ckey", "value"],
                )

            # --- UPGRADE TO 0.14.7 ---
            is_legacy_db = stored_info.version_super == 0 and (
                (
                    stored_info.version_major <= 14
                    and stored_info.version_minor <= 7
                )
                or (stored_info.version_major < 14)
            )
            if is_legacy_db:
                print("Database older than 0.14.7 -- updating", sv_text)
                self.add_column_to_table(
                    self.recipe_table, ("yields", Float(), {})
                )
                self.add_column_to_table(
                    self.recipe_table,
                    ("yield_unit", String(length=32), {}),
                )

                stmt_yields = (
                    update(self.recipe_table)
                    .where(self.recipe_table.c.servings.is_not(None))
                    .values(
                        {
                            self.recipe_table.c.yield_unit: "servings",
                            self.recipe_table.c.yields: (
                                self.recipe_table.c.servings
                            ),
                        }
                    )
                )
                with self.db.connect() as conn:
                    conn.execute(stmt_yields)
                    conn.commit()

             # --- UPGRADE TO 0.14.0 ---
            is_v14_legacy = (
                stored_info.version_super == 0
                and stored_info.version_major < 14
            )
            if is_v14_legacy:
                print("Database older than 0.14.0 -- updating", sv_text)
                backup_database(self.filename)
                print("Upgrade from < 0.14", sv_text)
                self.alter_table(
                    "categories",
                    self.setup_category_table,
                    {"id": "recipe_id"},
                    ["category"],
                )

                try:
                    with self.db.connect() as conn:
                        conn.execute(
                            text("select recipe_id from ingredients")
                        )
                except OperationalError:
                    self.alter_table(
                        "ingredients",
                        self.setup_ingredient_table,
                        {"id": "recipe_id"},
                        [
                            "refid",
                            "unit",
                            "amount",
                            "rangeamount",
                            "item",
                            "ingkey",
                            "optional",
                            "shopoptional",
                            "inggroup",
                            "position",
                            "deleted",
                        ],
                    )
                else:
                    print("Odd -- recipe_id seems to already exist")
                self.alter_table(
                    "keylookup",
                    self.setup_keylookup_table,
                    {},
                    ["word", "item", "ingkey", "count"],
                )

            # --- UPGRADE TO 0.13.0 ---
            is_v13_legacy = (
                stored_info.version_super == 0
                and stored_info.version_major <= 12
            )
            if is_v13_legacy:
                backup_database(self.filename)
                print("UPDATE FROM < 0.13.0...", sv_text)
                self.add_column_to_table(
                    self.recipe_table, ("last_modified", Integer(), {})
                )
                self.add_column_to_table(
                    self.recipe_table, ("recipe_hash", String(32), {})
                )
                self.add_column_to_table(
                    self.recipe_table, ("ingredient_hash", String(32), {})
                )
                self.add_column_to_table(
                    self.recipe_table, ("link", Text(), {})
                )
                print("Searching for links in old recipes...", sv_text)
                URL_SOURCES = ["instructions", "source", "modifications"]
                recs = self.search_recipes(
                    [
                        {
                            "column": col,
                            "operator": "LIKE",
                            "search": "%://%",
                            "logic": "OR",
                        }
                    for col in URL_SOURCES
                    ]
                )
                for r in recs:
                    rec_url = ""
                    for src in URL_SOURCES:
                        # Fixed: use dictionary mapping key lookups
                        blob = r[src]
                        if blob:
                            m = re.search(r"\w+://[^ ]*", blob)
                            if m:
                                rec_url = blob[m.start() : m.end()]
                                if rec_url[-1] in [
                                    ".",
                                    ")",
                                    ",",
                                    ";",
                                    ":",
                                ]:
                                    pass

    def update_plugin_version(self, plugin, current_version=None):
        if current_version:
            current_super, current_major, current_minor = current_version
        else:
            i = self.fetch_one(self.info_table)
            # Fixed: use dictionary mapping key lookups
            current_super = i["version_super"]
            current_major = i["version_major"]
            current_minor = i["version_minor"]

        existing = self.fetch_one(
            self.plugin_info_table, plugin=plugin.name
        )
        if existing:
            # Fixed: use dictionary mapping key lookups
            sup = int(existing["version_super"])
            maj = int(existing["version_major"])
            minor = int(existing["version_minor"])
            plugin_version = int(existing["plugin_version"])
        else:
            sup, maj, minor = 0, 13, 9
            plugin_version = 0

        try:
            plugin.update_version(
                gourmand_stored=(sup, maj, minor),
                plugin_stored=plugin_version,
                gourmand_current=(
                    current_super,
                    current_major,
                    current_minor,
                ),
                plugin_current=plugin.version,
            )
        except Exception:
            print("Problem updating plugin", plugin, plugin.name)
            raise

        info = {
            "plugin": plugin.name,
            "version_super": current_super,
            "version_major": current_major,
            "version_minor": current_minor,
            "plugin_version": plugin.version,
        }

        has_changed = (
            current_minor != minor
            or current_major != maj
            or current_super != sup
            or plugin.version != plugin_version
        )
        if existing and has_changed:
            self.do_modify(self.plugin_info_table, existing, info)
        else:
            self.do_add(self.plugin_info_table, info)

    def run_hooks(self, hooks, *args):
        """A basic hook-running function."""
        for h in hooks:
            msg = f"running hook {h} with args {args}"
            t = TimeAction(msg, 3)
            h(*args)
            t.end()

    def fetch_all(self, table, sort_by=None, criteria=None, **kwargs):
        if sort_by is None:
            sort_by = []

        search_criteria = criteria if criteria is not None else {}
        if kwargs:
            search_criteria.update(kwargs)

        stmt = select(table)

        where_args = make_simple_select_arg(search_criteria, table)
        if where_args:
            stmt = stmt.where(*where_args)

        order_args = make_order_by(sort_by, table)
        if order_args is not None:
            if isinstance(order_args, (list, tuple)):
                stmt = stmt.order_by(*order_args)
            else:
                stmt = stmt.order_by(order_args)

        with self.db.connect() as conn:
            return conn.execute(stmt).mappings().fetchall()

    def fetch_one(self, table, criteria=None, **kwargs):
        """Fetch one item from table and arguments"""
        search_criteria = criteria if criteria is not None else {}
        if kwargs:
            search_criteria.update(kwargs)

        stmt = select(table)
        where_args = make_simple_select_arg(search_criteria, table)
        if where_args:
            stmt = stmt.where(*where_args)
        with self.db.connect() as conn:
            return conn.execute(stmt).mappings().fetchone()

    def fetch_count(
        self, table, column, sort_by=None, criteria=None, **kwargs
    ):
        """Return a counted view of the table."""
        if sort_by is None:
            sort_by = []

        search_criteria = criteria if criteria is not None else {}
        if kwargs:
            search_criteria.update(kwargs)

        col_attr = getattr(table.c, column)
        stmt = select(func.count(col_attr).label("count"), col_attr)

        where_args = make_simple_select_arg(search_criteria, table)
        if where_args:
            stmt = stmt.where(*where_args)

        stmt = stmt.group_by(col_attr)

        order_args = make_order_by(sort_by, table, count_by=column)
        if order_args:
            if isinstance(order_args, (list, tuple)):
                stmt = stmt.order_by(*order_args)
            else:
                stmt = stmt.order_by(order_args)

        with self.db.connect() as conn:
            return conn.execute(stmt).fetchall()


    def fetch_len(self, table, criteria=None, **kwargs):
        """Return the number of rows in table that match criteria."""
        search_criteria = criteria if criteria is not None else {}
        if kwargs:
            search_criteria.update(kwargs)
        stmt = select(func.count()).select_from(table)
        where_args = make_simple_select_arg(search_criteria, table)
        if where_args:
            stmt = stmt.where(*where_args)

        with self.db.connect() as conn:
            return conn.scalar(stmt)

    def fetch_food_groups_for_search(self, words):
        """Return food groups that match a given set of words."""
        where_statement = or_(
            *[
                self.nutrition_table.c.desc.like(f"%{w.lower()}%")
                for w in words
            ]
        )

        stmt = (
            select(self.nutrition_table.c.foodgroup)
            .distinct()
            .where(where_statement)
        )

        with self.db.connect() as conn:
            query_results = conn.execute(stmt).fetchall()

        return [r[0] for r in query_results]

    def search_nutrition(self, words: List[str], group=None):
        """Search nutritional information for ingredient keys."""
        where_statement = and_(
            *[self.nutrition_table.c.desc.like(f"%{w}%") for w in words]
        )
        if group:
            where_statement = and_(
                self.nutrition_table.c.foodgroup == group, where_statement
            )
        stmt = select(self.nutrition_table).where(where_statement)
        with self.db.connect() as conn:
            return conn.execute(stmt).fetchall()

    def get_criteria(self, crit):
        if isinstance(crit, tuple):
            criteria, logic = crit
            if logic == "and":
                return and_(*[self.get_criteria(c) for c in criteria])
            elif logic == "or":
                return or_(*[self.get_criteria(c) for c in criteria])
        elif not isinstance(crit, dict):
            raise TypeError
        else:
            # join_crit = None # if we need to add an extra arg for a join
            if crit["column"] == "category":
                subtable = self.categories_table
                col = subtable.c.category
            elif crit["column"] in ["ingkey", "item"]:
                subtable = self.ingredients_table
                col = getattr(subtable.c, crit["column"])
            elif crit["column"] == "ingredient":
                d1 = crit.copy()
                d1.update({"column": "ingkey"})
                d2 = crit.copy()
                d2.update({"column": "item"})
                return self.get_criteria(([d1, d2], "or"))
            elif crit["column"] == "anywhere":
                searches = []
                columns = [
                    "ingkey",
                    "item",
                    "category",
                    "cuisine",
                    "title",
                    "instructions",
                    "modifications",
                    "source",
                    "link",
                ]
                for column in columns:
                    d = crit.copy()
                    d.update({"column": column})
                    searches.append(d)
                return self.get_criteria((searches, "or"))
            else:
                subtable = None
                col = getattr(self.recipe_table.c, crit["column"])

            op = crit.get("operator", "LIKE")
            if op == "LIKE":
                retval = col.like(crit["search"])
            elif op == "REGEXP":
                retval = col.op("REGEXP")(crit["search"])
            else:
                retval = col == crit["search"]

            if subtable is not None:
                sub_stmt = (
                    select(subtable.c.recipe_id)
                    .where(retval)
                    .scalar_subquery()
                )
                retval = self.recipe_table.c.id.in_(sub_stmt)

            return retval

    def search_recipes(
        self, searches, sort_by: Optional[List[Tuple]] = None
    ):
        """Search recipes for columns of values."""
        if sort_by is None:
            sort_by = []

        sort_keys = [param[0] for param in sort_by]

        if "rating" in sort_keys:
            sort_by_rating = sort_keys.index("rating")
            d = -1 if sort_by[sort_by_rating][1] == 1 else 1
            sort_by[sort_by_rating] = ("rating", d)

        criteria = self.get_criteria((searches, "and"))
        debug(
            f"backends.db.search_recipes - search criteria are {searches}",
            2,
        )

        if "category" in sort_keys:
            stmt = select(self.recipe_table).distinct()
            stmt = stmt.select_from(
                self.recipe_table.outerjoin(self.categories_table)
            )

            if criteria is not None:
                stmt = stmt.where(criteria)

            order_args = make_order_by(
                sort_by,
                self.recipe_table,
                join_tables=[self.categories_table],
            )
            if order_args:
                stmt = stmt.order_by(*order_args)
        else:
            stmt = select(self.recipe_table)

            if criteria is not None:
                stmt = stmt.where(criteria)

            order_args = make_order_by(sort_by, self.recipe_table)
            if order_args:
                stmt = stmt.order_by(*order_args)

        with self.db.connect() as conn:
            return conn.execute(stmt).mappings().fetchall()

    def get_unique_values(
        self, colname, table=None, criteria=None, **kwargs
    ):
        """Get list of unique values for column in table."""
        if table is None:
            table = self.recipe_table

        search_criteria = criteria if criteria is not None else {}
        if kwargs:
            search_criteria.update(kwargs)

        if search_criteria:
            where_args = make_simple_select_arg(search_criteria, table)
            criteria_expr = where_args[0] if where_args else None
        else:
            criteria_expr = None

        if colname == "category" and table == self.recipe_table:
            print("WARNING: you are using a hack to access category values.")
            table = self.categories_table
            table = table.alias("ingrtable")

        col_target = getattr(table.c, colname)
        stmt = select(col_target).distinct()

        if criteria_expr is not None:
            stmt = stmt.where(criteria_expr)

        with self.db.connect() as conn:
            retval = conn.execute(stmt).scalars().all()

        return [x for x in retval if x is not None]

    def get_ingkeys_with_count(
        self, search: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[int, str]]:
        """Get unique list of ingredient keys and usage counts."""
        if search is None:
            search = {}

        stmt = select(
            func.count(self.ingredients_table.c.ingkey).label("count"),
            self.ingredients_table.c.ingkey,
        )

        if search:
            col = getattr(self.ingredients_table.c, search["column"])
            operator = search.get("operator", "LIKE")
            if operator == "LIKE":
                criteria = col.like(search["search"])
            elif operator == "REGEXP":
                criteria = col.op("REGEXP")(search["search"])
            elif operator == "CONTAINS":
                criteria = col.contains(search["search"])
            else:
                criteria = col == search["search"]

            stmt = stmt.where(criteria)

        stmt = stmt.group_by(self.ingredients_table.c.ingkey)

        order_args = make_order_by(
            [], self.ingredients_table, count_by="ingkey"
        )
        if order_args:
            stmt = stmt.order_by(*order_args)

        with self.db.connect() as conn:
            return conn.execute(stmt).fetchall()

    def delete_by_criteria(self, table, criteria):
        """Delete rows from table that match given criteria."""
        criteria = fix_colnames(criteria, table)
        delete_args = [k == v for k, v in criteria.items()]

        if len(delete_args) > 1:
            delete_args = [and_(*delete_args)]

        # Modern 2.0 function design: delete(table)
        stmt = delete(table)
        if delete_args:
            stmt = stmt.where(*delete_args)

        with self.db.connect() as conn:
            conn.execute(stmt)
            conn.commit()

    def update_by_criteria(self, table, update_criteria, new_values_dic):
        """Update fields matched by update_criteria constraints."""
        try:
            to_del = [k for k in new_values_dic if not isinstance(k, str)]
            for k in to_del:
                v = new_values_dic[k]
                del new_values_dic[k]
                new_values_dic[str(k)] = v

            # Modern 2.0 function design: update(table)
            stmt = update(table)

            where_args = make_simple_select_arg(update_criteria, table)
            if where_args:
                stmt = stmt.where(*where_args)

            with self.db.connect() as conn:
                conn.execute(stmt, new_values_dic)
                conn.commit()

        except Exception:
            print("update_by_criteria error...")
            print("table:", table)
            print("UPDATE_CRITERIA:")
            for k, v in update_criteria.items():
                print(f" KEY: {k} VAL: {v}")
            print("NEW_VALUES_DIC:")
            for k, v in new_values_dic.items():
                print(f" KEY: {k} ({type(k)}) VAL: {v}")
            raise

    def add_column_to_table(self, table, column_spec):
        """Execute safe schema migrations adding individual columns."""
        name = table.name
        new_col = column_spec[0]
        coltyp = column_spec[1]
        coltyp_str = coltyp.compile(dialect=self.db.dialect)

        sql = f"ALTER TABLE {name} ADD {new_col} {coltyp_str};"
        try:
            with self.db.connect() as conn:
                conn.execute(text(sql))
                conn.commit()
        except Exception:
            print("FAILED TO EXECUTE", sql)
            print("Ignoring error in add_column_to_table")
            import traceback

            traceback.print_exc()

    def alter_table(
        self,
        table_name,
        setup_function,
        cols_to_change=None,
        cols_to_keep=None,
    ):
        """Reconstruct table constraints via safe temporary data steps."""
        if cols_to_change is None:
            cols_to_change = {}
        if cols_to_keep is None:
            cols_to_keep = []

        print(
            f"Altering {table_name}: keeping {cols_to_keep}, "
            f"changing {cols_to_change}"
        )

        with self.db.connect() as conn:
            try:
                conn.execute(
                    text(f"ALTER TABLE {table_name} RENAME TO {table_name}_temp")
                )
                conn.commit()
            except Exception:
                do_raise = True
                import traceback

                traceback.print_exc()
                try:
                    conn.execute(text(f"DROP TABLE {table_name}_temp"))
                    conn.commit()
                except Exception:
                    pass
                else:
                    do_raise = False
                    conn.execute(
                        text(
                            f"ALTER TABLE {table_name} "
                            f"RENAME TO {table_name}_temp"
                        )
                    )
                    conn.commit()
                if do_raise:
                    raise

            self.metadata._remove_table(table_name, self.metadata.schema)

            setup_function()

            new_table_obj = getattr(self, f"{table_name}_table")

            # Modern 2.0 direct schema construction syntax
            new_table_obj.create(conn)
            conn.commit()

            to_cols = cols_to_keep[:]
            from_cols = cols_to_keep[:]
            for fro, to_ in cols_to_change.items():
                from_cols.append(fro)
                to_cols.append(to_)

            from_str = ", ".join(from_cols)
            to_str = ", ".join(to_cols)

            stmt = f"""
                INSERT INTO {table_name} ({to_str})
                SELECT {from_str} FROM {table_name}_temp
            """

            conn.execute(text(stmt))
            conn.execute(text(f"DROP TABLE {table_name}_temp"))
            conn.commit()

    def increment_field(self, table, field):
        """Increment field in table, or return None if automatic."""
        return None

    def row_equal(self, r1, r2):
        """Test whether two row references are the same."""
        return r1 in [r2, str]

    def find_duplicates(
        self, by="recipe", recipes=None, include_deleted=True
    ):
        """Find all duplicate recipes by recipe or ingredient hash."""
        if by == "recipe":
            col = self.recipe_table.c.recipe_hash
        elif by == "ingredient":
            col = self.recipe_table.c.ingredient_hash
        else:
            raise ValueError(f"Invalid 'by' parameter: {by}")

        sub_stmt = select(col).group_by(col).having(func.count(col) > 1)

        if not include_deleted:
            sub_stmt = sub_stmt.where(
                self.recipe_table.c.deleted.is_(False)
            )

        duped_hashes = sub_stmt.subquery()
        main_stmt = select(self.recipe_table.c.id, col)

        # 2.0 standard: reference the subquery columns directly inside select
        hash_select = select(duped_hashes.c[col.name])
        if include_deleted:
            main_stmt = main_stmt.where(col.in_(hash_select))
        else:
            main_stmt = main_stmt.where(
                and_(
                    col.in_(hash_select),
                    self.recipe_table.c.deleted.is_(False),
                )
            )

        main_stmt = main_stmt.order_by(col)

        with self.db.connect() as conn:
            query_result = conn.execute(main_stmt).fetchall()

        recs_by_hash = {}
        for result in query_result:
            rec_id, hsh = result[0], result[1]
            if hsh not in recs_by_hash:
                recs_by_hash[hsh] = []
            recs_by_hash[hsh].append(rec_id)

        results = list(recs_by_hash.values())

        if recipes:
            # High-performance O(1) set filtering conversion
            rec_set = {r.id for r in recipes}
            results = [
                reclist for reclist in results
                if any(rid in rec_set for rid in reclist)
            ]

        return results

    def find_complete_duplicates(self, recipes=None, include_deleted=True):
        """Find duplicate recipes by recipe and ingredient hash matching."""
        subqueries = []
        targets = [
            self.recipe_table.c.ingredient_hash,
            self.recipe_table.c.recipe_hash,
        ]

        for col in targets:
            sub_stmt = select(col).group_by(col).having(func.count(col) > 1)
            if not include_deleted:
                sub_stmt = sub_stmt.where(
                    self.recipe_table.c.deleted.is_(False)
                )
            subqueries.append(sub_stmt.subquery())

        ing_sub, rec_sub = subqueries[0], subqueries[1]
        select_statements = []

        if not include_deleted:
            select_statements.append(self.recipe_table.c.deleted.is_(False))

        # Explicit clean 2.0 select extraction paths for subqueries
        select_statements.append(
            self.recipe_table.c.ingredient_hash.in_(
                select(ing_sub.c.ingredient_hash)
            )
        )
        select_statements.append(
            self.recipe_table.c.recipe_hash.in_(
                select(rec_sub.c.recipe_hash)
            )
        )

        main_stmt = (
            select(
                self.recipe_table.c.id,
                self.recipe_table.c.recipe_hash,
                self.recipe_table.c.ingredient_hash,
            )
            .where(and_(*select_statements))
            .order_by(
                self.recipe_table.c.recipe_hash,
                self.recipe_table.c.ingredient_hash,
            )
        )

        with self.db.connect() as conn:
            query_results = conn.execute(main_stmt).fetchall()

        recs_by_hash = {}
        for result in query_results:
            rec_id, rhsh, ihsh = result[0], result[1], result[2]
            key = (rhsh, ihsh)
            if key not in recs_by_hash:
                recs_by_hash[key] = []
            recs_by_hash[key].append(rec_id)

        results = list(recs_by_hash.values())

        if recipes:
            # High-performance O(1) set filtering conversion
            rec_set = {r.id for r in recipes}
            results = [
                reclist for reclist in results
                if any(rid in rec_set for rid in reclist)
            ]

        return results

        # Convenience DB access functions for working with ingredients,
    # recipes, etc.

    def delete_ing(self, ing):
        """Delete ingredient permanently."""
        self.delete_by_criteria(self.ingredients_table, {"id": ing.id})

    def modify_rec(self, rec, dic):
        """Modify recipe based on attributes/values in dictionary.

        Return modified recipe.
        """
        self.validate_recdic(dic)
        debug("validating dictionary", 3)

        if "category" in dic:
            newcats = [x for x in dic["category"].split(", ") if x]
            curcats = self.get_cats(rec)

            for c in curcats:
                if c not in newcats:
                    self.delete_by_criteria(
                        self.categories_table,
                        {"recipe_id": rec.id, "category": c},
                    )
            for c in newcats:
                if c not in curcats:
                    self.do_add_cat(
                        {"recipe_id": rec.id, "category": c}
                    )
            del dic["category"]

        debug("do modify rec", 3)
        retval = self.do_modify_rec(rec, dic)
        self.update_hashes(rec)
        return retval

    def validate_recdic(self, recdic):
        if "last_modified" not in recdic:
            recdic["last_modified"] = time.time()
        if "image" in recdic and "thumb" not in recdic:
            # if we have an image but no thumbnail, we want to create the thumbnail.
            try:
                img = image_utils.bytes_to_image(recdic["image"])
                thumb = img.copy()
                thumb.thumbnail((40, 40))
                recdic["thumb"] = image_utils.image_to_bytes(thumb)
            except Exception:
                del recdic["image"]
                print(
                    """Warning: Gourmand couldn't recognize the image.

                Proceding anyway, but here's the traceback should you
                wish to investigate.
                """
                )
                import traceback

                traceback.print_stack()
        for k, v in recdic.items():
            if isinstance(v, str):
                recdic[k] = v.strip()

    def modify_ings(self, ings, ingdict):
        # allow for the possibility of doing a smarter job changing
        # something for a whole bunch of ingredients...
        for i in ings:
            self.modify_ing(i, ingdict)

    def modify_ing_and_update_keydic(self, ing, ingdict):
        """Update our key dictionary and modify our dictionary.

        This is a separate method from modify_ing because we only do
        this for hand-entered data, not for mass imports.
        """
        # If our ingredient has changed, update our keydic...
        if ing.item != ingdict.get("item", ing.item) or ing.ingkey != ingdict.get("ingkey", ing.ingkey):
            if ing.item and ing.ingkey:
                self.remove_ing_from_keydic(ing.item, ing.ingkey)
                self.add_ing_to_keydic(ingdict.get("item", ing.item), ingdict.get("ingkey", ing.ingkey))
        return self.modify_ing(ing, ingdict)

    def update_hashes(self, rec):
        rhash, ihash = recipeIdentifier.hash_recipe(rec, self)
        self.do_modify_rec(rec, {"recipe_hash": rhash, "ingredient_hash": ihash})

    def find_duplicates_of_rec(self, rec, match_ingredient=True, match_recipe=True):
        """Return recipes that appear to be duplicates"""
        if match_ingredient and match_recipe:
            perfect_matches = self.fetch_all(ingredient_hash=rec.ingredient_hash, recipe_hash=rec.recipe_hash)
        elif match_ingredient:
            perfect_matches = self.fetch_all(ingredient_hash=rec.ingredient_hash)
        else:
            perfect_matches = self.fetch_all(recipe_hash=rec.recipe_hash)
        matches = []
        if len(perfect_matches) == 1:
            return []
        else:
            for r in perfect_matches:
                if r.id != rec.id:
                    matches.append(r)
            return matches

    def find_all_duplicates(self):
        """Return a list of sets of duplicate recipes."""
        raise NotImplementedError

    def merge_mergeable_duplicates(self):
        """Merge all duplicates for which a simple merge is possible.
        For those recipes which can't be merged, return:
        [recipe-id-list,to-merge-dic,diff-dic]
        """
        dups = self.find_all_duplicates()
        unmerged = []
        for recs in dups:
            rec_objs = [self.fetch_one(self.recipe_table, id=r) for r in recs]
            merge_dic, diffs = recipeIdentifier.merge_recipes(self, rec_objs)
            if not diffs:
                if merge_dic:
                    self.modify_rec(rec_objs[0], merge_dic)
                for r in rec_objs[1:]:
                    self.delete_rec(r)
            else:
                unmerged.append([recs, merge_dic, diffs])
        return unmerged

    def modify_ing(self, ing, ingdict):
        return self.do_modify_ing(ing, ingdict)

    def add_rec(self, dic: Dict[str, Any]):  # Returns "RowProxy"
        """Add a recipe to the database.

        The function expect a dictionary of column values for the recipe,
        and returns the entry in the database as a RowProxy.
        """
        cats = []
        if dic.get('category'):
            cats = [v.strip() for v in dic["category"].split(",") if v]
            del dic["category"]
        if "servings" in dic:
            if "yields" in dic:
                del dic["yields"]
            else:
                try:
                    dic["servings"] = float(dic["servings"])
                    dic["yields"] = dic["servings"]
                    dic["yield_unit"] = "servings"
                    del dic["servings"]
                except Exception:
                    del dic["servings"]
        if "deleted" not in dic:
            dic["deleted"] = False
        self.validate_recdic(dic)
        try:
            ret = self.do_add_rec(dic)
        except:
            print("Problem adding recipe with dictionary...")
            for k, v in list(dic.items()):
                print("KEY:", k, "of type", type(k), "VALUE:", v, "of type", type(v))
            raise
        else:
            if isinstance(ret, int):
                ID = ret
                ret = self.get_rec(ID)
            else:
                ID = ret.id
            for c in cats:
                if c:
                    self.do_add_cat({"recipe_id": ID, "category": c.strip()})
            self.update_hashes(ret)
            return ret

    def add_ing_and_update_keydic(self, dic):
        if "item" in dic and "ingkey" in dic and dic["item"] and dic["ingkey"]:
            self.add_ing_to_keydic(dic["item"], dic["ingkey"])
        return self.add_ing(dic)

    def add_ing(self, dic):
        if "deleted" not in dic:
            dic["deleted"] = False

        try:
            return self.do_add_ing(dic)
        except Exception:
            print("Problem adding", dic)
            raise

    def add_ings(self, dics: List[Dict[str, Any]]):
        """Add multiple ingredient dictionaries at a time."""
        required_keys = [
            "refid",
            "unit",
            "amount",
            "rangeamount",
            "item",
            "ingkey",
            "optional",
            "shopoptional",
            "inggroup",
            "position",
        ]
        for d in dics:
            if "deleted" not in d:
                d["deleted"] = False
            for key in required_keys:
                if key not in d:
                    d[key] = None

        stmt = insert(self.ingredients_table)
        try:
            with self.db.connect() as conn:
                conn.execute(stmt, dics)
                conn.commit()
        except ValueError:
            for d in dics:
                self.coerce_types(self.ingredients_table, d)
            with self.db.connect() as conn:
                conn.execute(stmt, dics)
                conn.commit()

    # Lower level DB access functions

    def coerce_types(self, table, dic):
        """Modify dic to make sure types are correct for table."""
        type_to_pytype = {
            Float: float,
            Integer: int,
            String: str,
            Boolean: bool,
            Numeric: float,
        }
        for k, v in list(dic.copy().items()):
            column_obj = getattr(table.c, k)
            if column_obj.type.__class__ in type_to_pytype:
                try:
                    v = type_to_pytype[column_obj.type.__class__](v)
                except Exception:
                    v = None
                if dic[k] != v:
                    dic[k] = v

    def commit_fast_adds(self):
        if hasattr(self, "extra_connection"):
            self.extra_connection.commit()

    def do_add_fast(self, table, dic):
        """Add fast -- return None."""
        try:
            stmt = insert(table)
            with self.db.connect() as conn:
                conn.execute(stmt, dic)
                conn.commit()
        except Exception:
            return self.do_add(table, dic)

    def do_add(self, table, dic):
        stmt = insert(table)
        try:
            with self.db.connect() as conn:
                result = conn.execute(stmt, dic)
                conn.commit()
                inserted_id = (
                    result.inserted_primary_key[0]
                    if result.inserted_primary_key
                    else None
                )
        except ValueError:
            print("Had to coerce types", table, dic)
            self.coerce_types(table, dic)
            with self.db.connect() as conn:
                result = conn.execute(stmt, dic)
                conn.commit()
                inserted_id = (
                    result.inserted_primary_key[0]
                    if result.inserted_primary_key
                    else None
                )

        return inserted_id

    def do_add_and_return_item(self, table, dic, id_prop="id"):
        inserted_id = self.do_add(table, dic)
        stmt = select(table).where(getattr(table.c, id_prop) == inserted_id)
        with self.db.connect() as conn:
            return conn.execute(stmt).mappings().fetchone()

    def do_add_ing(self, dic):
        return self.do_add_and_return_item(
            self.ingredients_table, dic, id_prop="id"
        )

    def do_add_cat(self, dic):
        return self.do_add_and_return_item(self.categories_table, dic)

    def do_add_rec(self, rdict):
        """Add a recipe based on a dictionary of properties and values."""
        self.changed = True
        if "deleted" not in rdict:
            rdict["deleted"] = 0

        if "id" in rdict:
            if rdict["id"] in self.new_ids:
                rid = rdict["id"]
                del rdict["id"]
                self.new_ids.remove(rid)
                self.update_by_criteria(
                    self.recipe_table, {"id": rid}, rdict
                )
                stmt = select(self.recipe_table).where(
                    self.recipe_table.c.id == rid
                )
                with self.db.connect() as conn:
                    return conn.execute(stmt).mappings().fetchone()
            else:
                raise ValueError(
                    f"New recipe created with preset id {rdict['id']}, "
                    "but ID is not in our list of new_ids"
                )

        stmt = insert(self.recipe_table)
        with self.db.connect() as conn:
            res = conn.execute(stmt, rdict)
            conn.commit()
            new_id = (
                res.inserted_primary_key[0]
                if res.inserted_primary_key
                else None
            )

        fetch_stmt = select(self.recipe_table).where(
            self.recipe_table.c.id == new_id
        )
        with self.db.connect() as conn:
            return conn.execute(fetch_stmt).mappings().fetchone()

    def do_modify_rec(self, rec, dic):
        """This is what other DBs should subclass."""
        return self.do_modify(self.recipe_table, rec, dic)

    def do_modify_ing(self, ing, ingdict):
        """Modify ing based on dictionary of properties and new values."""
        return self.do_modify(self.ingredients_table, ing, ingdict)

    def do_modify(self, table, row, d, id_col="id"):
        if id_col is not None:
            try:
                table_val = getattr(table.c, id_col)
                # Supports either mapped dict or object row
                row_val = (
                    row[id_col]
                    if isinstance(row, (dict, Mapping)) or hasattr(row, "__getitem__")
                    else getattr(row, id_col)
                )

                stmt = update(table).where(table_val == row_val)
                with self.db.connect() as conn:
                    conn.execute(stmt, d)
                    conn.commit()

            except Exception as e:
                print("do_modify failed with args")
                print("table=", table, "row=", row)
                print("d=", d, "id_col=", id_col)
                print(e)
                raise

            select_stmt = select(table).where(
                getattr(table.c, id_col) == row_val
            )
        else:
            stmt = update(table)
            with self.db.connect() as conn:
                conn.execute(stmt, d)
                conn.commit()

            select_stmt = select(table)

        with self.db.connect() as conn:
            return conn.execute(select_stmt).mappings().fetchone()


    def get_ings(self, rec):
        """Handed rec, return a list of ingredients.

        rec should be an ID or an object/mapping with an ID field.
        """
        if isinstance(rec, (dict, Mapping)) or hasattr(rec, "__getitem__"):
            rec_id = rec["id"]
        elif hasattr(rec, "id"):
            rec_id = rec.id
        else:
            rec_id = rec

        return self.fetch_all(
            self.ingredients_table, recipe_id=rec_id, deleted=False
        )

    def get_cats(self, rec):
        rec_id = rec["id"] if hasattr(rec, "__getitem__") else rec.id
        svw = self.fetch_all(self.categories_table, recipe_id=rec_id)

        # Access elements safely via mapping dictionary syntax
        cats = [c["category"] or "" for c in svw]
        while "" in cats:
            cats.remove("")
        return cats

    def get_referenced_rec(self, ing):
        """Get recipe referenced by ingredient object."""
        ref_id = ing["refid"] if hasattr(ing, "__getitem__") else ing.refid
        item_name = ing["item"] if hasattr(ing, "__getitem__") else ing.item

        if ref_id:
            rec = self.get_rec(ref_id)
            if rec:
                return rec

        if item_name:
            rec = self.fetch_one(self.recipe_table, title=item_name)
            if rec:
                self.modify_ing(ing, {"refid": rec["id"]})
                return rec
            else:
                print(f"Very odd: no match for {ing} refid: {ref_id}")

    def include_linked_recipes(self, recs):
        """Handed a list of recipes, append any recipes linked as ingredients.

        Modifies the list in place.
        """
        # Read elements dynamically whether they are objects or mappings
        ids = [
            r["id"] if hasattr(r, "__getitem__") else r.id
            for r in recs
        ]

        stmt = select(self.ingredients_table).where(
            and_(
                self.ingredients_table.c.refid.is_not(None),
                self.ingredients_table.c.refid > 0,
                self.ingredients_table.c.recipe_id.in_(ids),
            )
        )

        with self.db.connect() as conn:
            extra_ings = conn.execute(stmt).mappings().fetchall()

        for i in extra_ings:
            if i["refid"] not in ids:
                recs.append(self.get_referenced_rec(i))

    def get_rec(self, id_val, recipe_table=None):
        """Handed an ID, return a recipe object."""
        if recipe_table:
            print("handing get_rec a recipe_table is deprecated")
            print("Ignoring recipe_table handed to get_rec")
        return self.fetch_one(self.recipe_table, id=id_val)

    def delete_rec(self, rec):
        """Delete recipe object rec from our database."""
        if not isinstance(rec, int):
            rec_id = rec["id"] if hasattr(rec, "__getitem__") else rec.id
        else:
            rec_id = rec

        debug(f"deleting recipe ID {rec_id}", 0)
        self.delete_by_criteria(self.recipe_table, {"id": rec_id})
        self.delete_by_criteria(self.categories_table, {"recipe_id": rec_id})
        self.delete_by_criteria(self.ingredients_table, {"recipe_id": rec_id})
        debug(f"deleted recipe ID {rec_id}", 0)

    def new_rec(self):
        """Create and return a new, empty recipe"""
        return self.add_rec({"title": _("New Recipe")})

    def new_id(self) -> int:
        rec = self.do_add_rec({"deleted": 1})
        rec_id = rec["id"] if hasattr(rec, "__getitem__") else rec.id
        self.new_ids.append(rec_id)
        return rec_id

    def order_ings(self, ings):
        """Handed a view of ingredients, return an ordered alist."""
        defaultn = 0
        groups = {}
        group_order = {}
        n = 0

        for i in ings:
            # Safely navigate flexible input formats
            if hasattr(i, "__getitem__"):
                group = i.get("inggroup")
                position = i.get("position")
            else:
                group = getattr(i, "inggroup", None)
                position = getattr(i, "position", None)

            if group is None:
                group = n
                n += 1

            if position is None:
                print("Bad: ingredient without position", i)
                position = defaultn
                defaultn += 1

            if group in groups:
                groups[group].append(i)
                if position < group_order[group]:
                    group_order[group] = position
            else:
                groups[group] = [i]
                group_order[group] = position

        alist = sorted(groups.items(), key=lambda x: group_order[x[0]])

        for g, lst in alist:
            lst.sort(
                key=lambda x: x["position"] if hasattr(x, "__getitem__")
                else x.position
            )

        final_alist = []
        last_g = -1
        for g, ii in alist:
            if isinstance(g, int):
                if last_g is None:
                    final_alist[-1][1].extend(ii)
                else:
                    final_alist.append([None, ii])
                last_g = None
            else:
                final_alist.append([g, ii])
                last_g = g
        return final_alist

    def replace_ings(self, ingdicts):
        """Add new ingredients and remove old ingredient list."""
        if not ingdicts:
            return
        rec_id = ingdicts[0]["id"]
        debug(f"Deleting ingredients for recipe with ID {rec_id}", 1)
        self.delete_by_criteria(self.ingredients_table, {"id": rec_id})
        for ingd in ingdicts:
            self.add_ing(ingd)

    def ingview_to_lst(self, view):
        """Handed a view of ingredient data, output a useful list."""
        ret = []
        for i in view:
            unit_val = i["unit"] if hasattr(i, "__getitem__") else i.unit
            key_val = i["ingkey"] if hasattr(i, "__getitem__") else i.ingkey
            ret.append(
                [
                    self.get_amount(i),
                    unit_val,
                    key_val,
                ]
            )
        return ret


    def get_amount(self, ing, mult=1):
        """Given an ingredient object/dict, return the amount for it.

        Amount may be a tuple if the amount is a range, a float if
        there is a single amount, or None.
        """
        if isinstance(ing, (dict, Mapping)) or hasattr(ing, "__getitem__"):
            amt = ing.get("amount") if hasattr(ing, "get") else ing["amount"]
            ramt = (
                ing.get("rangeamount")
                if hasattr(ing, "get")
                else (ing["rangeamount"] if "rangeamount" in ing else None)
            )
        else:
            amt = getattr(ing, "amount", None)
            ramt = getattr(ing, "rangeamount", None)

        if mult != 1:
            if amt is not None:
                amt = amt * mult
            if ramt is not None:
                ramt = ramt * mult

        if ramt:
            return (amt, ramt)
        return amt

    @pluggable_method
    def get_amount_and_unit(
        self,
        ing,
        mult=1,
        conv=None,
        fractions=None,
        adjust_units=False,
        favor_current_unit=True,
        preferred_unit_groups=None,
    ):
        """Return a tuple of strings representing amount and unit.

        If handed a converter interface, units will be adjusted to make
        them readable.
        """
        if preferred_unit_groups is None:
            preferred_unit_groups = []

        amt = self.get_amount(ing, mult)
        unit = (
            ing["unit"]
            if hasattr(ing, "__getitem__")
            else getattr(ing, "unit", "")
        )
        ramount = None

        if isinstance(amt, tuple):
            amt, ramount = amt

        if adjust_units or preferred_unit_groups:
            if not conv:
                conv = convert.get_converter()
            amt, unit = conv.adjust_unit(
                amt,
                unit,
                favor_current_unit=favor_current_unit,
                preferred_unit_groups=preferred_unit_groups,
            )
            orig_unit = (
                ing["unit"]
                if hasattr(ing, "__getitem__")
                else getattr(ing, "unit", "")
            )
            if ramount and unit != orig_unit:
                ramount = ramount * conv.converter(orig_unit, unit)

        if ramount:
            amt = (amt, ramount)

        famount = self.format_amount_string_from_amount(
            amt, fractions=fractions, unit=unit
        )
        return famount, unit

    def get_amount_as_string(
        self,
        ing,
        mult=1,
        fractions=None,
    ):
        """Return a string representing amount with optional multiplier."""
        amt = self.get_amount(ing, mult)
        return self.format_amount_string_from_amount(
            amt, fractions=fractions
        )

    @staticmethod
    def format_amount_string_from_amount(amt, fractions=None, unit=None):
        """Format amount string given an amount tuple or float."""
        if fractions is None:
            fractions = convert.USE_FRACTIONS

        if unit:
            approx = defaults.unit_rounding_guide.get(unit, 0.01)
        else:
            approx = 0.01

        if isinstance(amt, tuple):
            low = convert.float_to_frac(
                amt[0], fractions=fractions, approx=approx
            ).strip()
            high = convert.float_to_frac(
                amt[1], fractions=fractions, approx=approx
            ).strip()
            return f"{low}-{high}"
        elif isinstance(amt, (float, int)):
            return convert.float_to_frac(
                amt, fractions=fractions, approx=approx
            )
        else:
            return ""

    def get_amount_as_float(self, ing, mode=1):
        """Return a float representing amount, resolving ranges."""
        amt = self.get_amount(ing)
        if isinstance(amt, (float, int, type(None))):
            return amt
        else:
            amt_list = sorted(list(amt))
            low, high = amt_list[0], amt_list[1]
            if mode == self.AMT_MODE_AVERAGE:
                return (low + high) / 2.0
            elif mode == self.AMT_MODE_LOW:
                return low
            elif mode == self.AMT_MODE_HIGH:
                return high
            else:
                raise ValueError(f"{mode} is an invalid value for mode")

    @pluggable_method
    def add_ing_to_keydic(self, item, key):
        """Add ingredient keyword tracking entries to keylookup."""
        if not item or not key:
            return

        if isinstance(item, bytes):
            item = item.decode("utf-8", "replace")
        else:
            item = str(item)

        if isinstance(key, bytes):
            key = key.decode("utf-8", "replace")
        else:
            key = str(key)

        row = self.fetch_one(
            self.keylookup_table, item=item, ingkey=key
        )
        if row:
            self.do_modify(
                self.keylookup_table,
                row,
                {"count": row["count"] + 1},
            )
        else:
            self.do_add(
                self.keylookup_table,
                {"item": item, "ingkey": key, "count": 1},
            )

        for w in item.split():
            w = w.casefold()
            row = self.fetch_one(
                self.keylookup_table, word=str(w), ingkey=str(key)
            )
            if row:
                self.do_modify(
                    self.keylookup_table,
                    row,
                    {"count": row["count"] + 1},
                )
            else:
                self.do_add(
                    self.keylookup_table,
                    {"word": str(w), "ingkey": str(key), "count": 1},
                )

    def remove_ing_from_keydic(self, item, key):
        """Remove or decrement ingredient keyword lookups."""
        row = self.fetch_one(
            self.keylookup_table, item=item, ingkey=key
        )
        if row:
            new_count = row["count"] - 1
            if new_count > 0:
                self.do_modify(
                    self.keylookup_table, row, {"count": new_count}
                )
            else:
                self.delete_by_criteria(
                    self.keylookup_table, {"item": item, "ingkey": key}
                )

        for word in item.split():
            w = word.casefold()
            row = self.fetch_one(
                self.keylookup_table, word=w, ingkey=key
            )
            if row:
                new_count = row["count"] - 1
                if new_count > 0:
                    self.do_modify(
                        self.keylookup_table, row, {"count": new_count}
                    )
                else:
                    self.delete_by_criteria(
                        self.keylookup_table,
                        {"word": w, "ingkey": key},
                    )

    def ing_shopper(self, view):
        from gourmand.databaseShopper import DatabaseShopper

        return DatabaseShopper(self.ingview_to_lst(view), self.db)

      # Functions to undoably modify tables

    def get_dict_for_obj(self, obj, keys):
        """Extract object parameters as a standard dictionary layer."""
        orig_dic = {}
        is_mapping = isinstance(obj, (dict, Mapping)) or hasattr(
            obj, "__getitem__"
        )
        for k in keys:
            if k == "category":
                v = ", ".join(self.get_cats(obj))
            elif is_mapping:
                v = obj.get(k) if hasattr(obj, "get") else obj[k]
            else:
                v = getattr(obj, k)
            orig_dic[k] = v
        return orig_dic

    def undoable_modify_rec(
        self,
        rec,
        dic,
        history=None,
        get_current_rec_method=None,
        select_change_method=None,
    ):
        """Modify a recipe and register explicit undo/redo actions."""
        if history is None:
            history = []

        orig_dic = self.get_dict_for_obj(rec, dic.keys())
        reundo_name = "Re_apply"
        reapply_name = "Re_apply "

        reundo_name += "".join(
            [f"{k} <i>{v}</i>" for k, v in orig_dic.items()]
        )
        reapply_name += "".join([f"{k} <i>{v}</i>" for k, v in dic.items()])
        redo, reundo = None, None

        if get_current_rec_method:

            def redo(*args):
                r = get_current_rec_method()
                odic = self.get_dict_for_obj(r, dic.keys())
                return ([r, dic], [r, odic])

            def reundo(*args):
                r = get_current_rec_method()
                odic = self.get_dict_for_obj(r, orig_dic.keys())
                return ([r, orig_dic], [r, odic])

        def action(*args, **kwargs):
            """Our actual action allows for selecting changes after modifying"""
            self.modify_rec(*args, **kwargs)
            if select_change_method:
                select_change_method(*args, **kwargs)

        obj = Undo.UndoableObject(
            action,
            action,
            history,
            action_args=[rec, dic],
            undo_action_args=[rec, orig_dic],
            get_reapply_action_args=redo,
            get_reundo_action_args=reundo,
            reapply_name=reapply_name,
            reundo_name=reundo_name,
        )
        obj.perform()

    def undoable_delete_recs(self, recs, history, make_visible=None):
        """Delete recipes by setting their 'deleted' flag to True."""

        def do_delete():
            for rec in recs:
                rec_id = (
                    rec["id"]
                    if hasattr(rec, "__getitem__")
                    else getattr(rec, "id")
                )
                debug(f"rec {rec_id} deleted=True", 1)
                self.modify_rec(rec, {"deleted": True})
            if make_visible:
                make_visible(recs)

        def undo_delete():
            for rec in recs:
                rec_id = (
                    rec["id"]
                    if hasattr(rec, "__getitem__")
                    else getattr(rec, "id")
                )
                debug(f"rec {rec_id} deleted=False", 1)
                self.modify_rec(rec, {"deleted": False})
            if make_visible:
                make_visible(recs)

        obj = Undo.UndoableObject(do_delete, undo_delete, history)
        obj.perform()

    def undoable_modify_ing(self, ing, dic, history, make_visible=None):
        """Modify ingredient object based on a dictionary of properties."""
        orig_dic = self.get_dict_for_obj(ing, dic.keys())
        key = dic.get("ingkey", None)
        ing_item = (
            ing["item"] if hasattr(ing, "__getitem__") else getattr(ing, "item")
        )
        item = key and dic.get("item", ing_item)

        def do_action():
            debug(f"undoable_modify_ing modifying {dic}", 2)
            self.modify_ing(ing, dic)
            if key:
                self.add_ing_to_keydic(item, key)
            if make_visible:
                make_visible(ing, dic)

        def undo_action():
            debug("undoable_modify_ing unmodifying %s" % orig_dic, 2)
            self.modify_ing(ing, orig_dic)
            if key:
                self.remove_ing_from_keydic(item, key)
            if make_visible:
                make_visible(ing, orig_dic)

        obj = Undo.UndoableObject(do_action, undo_action, history)
        obj.perform()

    def undoable_delete_ings(self, ings, history, make_visible=None):
        """Delete ingredients in list ings and add to our undo history."""

        def do_delete():
            modded_ings = [self.modify_ing(i, {"deleted": True}) for i in ings]
            if make_visible:
                make_visible(modded_ings)

        def undo_delete():
            modded_ings = [self.modify_ing(i, {"deleted": False}) for i in ings]
            if make_visible:
                make_visible(modded_ings)

        obj = Undo.UndoableObject(do_delete, undo_delete, history)
        obj.perform()

    def get_default_values(self, colname):
        try:
            return defaults.fields[colname]
        except Exception:
            return []


class RecipeManager:
    _instance_by_db_url = {}

    @classmethod
    def instance_for(cls, file: Optional[str] = None, custom_url: Optional[str] = None) -> "RecipeManager":
        url = db_url(file, custom_url)

        if url not in cls._instance_by_db_url:
            cls._instance_by_db_url[url] = cls(file, custom_url)

        return cls._instance_by_db_url[url]

    def __init__(self, *args, **kwargs):
        debug("recipeManager.__init__()", 3)
        self.rd = get_database(*args, **kwargs)
        self.km = KeyManager.instance(recipe_manager=self)

    def __getattr__(self, name):
        # RecipeManager was previously a subclass of RecData.
        # This was changed as they're both used as singletons, and there's
        # no good way to have a subclassed singleton (unless the parent class
        # is an abstract thing that's never used directly, which it wasn't).
        # However, lots of code uses RecData methods on RecipeManager objects.
        # This ensures that that code keeps working.
        if name.startswith("_"):
            raise AttributeError(name)
        return getattr(self.rd, name)

    def key_search(self, ing):
        """Handed a string, we search for keys that could match
        the ingredient."""
        result = self.km.look_for_key(ing)
        if isinstance(result, str):
            return [result]
        elif isinstance(result, list):
            # look_for contains an alist of sorts... we just want the first
            # item of every cell.
            if len(result) > 0 and result[0][1] > 0.8:
                return [a[0] for a in result]
            else:
                ## otherwise, we make a mad attempt to guess!
                k = self.km.generate_key(ing)
                ll = [k]
                ll.extend([a[0] for a in result])
                return ll
        else:
            return None

    def parse_ingredient(self, s, conv=None, get_key=True):
        """Handed a string, we hand back a dictionary representing a parsed ingredient (sans recipe ID)"""
        # if conv:
        #    print 'parse_ingredient: conv argument is now ignored'
        debug("ingredient_parser handed: %s" % s, 0)
        # Strip whitespace and bullets...
        d = {}
        if isinstance(s, bytes):
            s = s.decode("utf8")
        s = s.strip("\u2022\u2023\u2043\u204C\u204D\u2219\u25C9\u25D8\u25E6\u2619\u2765\u2767\u29BE\u29BF\n\t #*+-")
        option_m = re.match(r"\s*optional:?\s*", s, re.IGNORECASE)
        if option_m:
            s = s[option_m.end() :]
            d["optional"] = True
        debug('ingredient_parser handed: "%s"' % s, 1)
        m = convert.ING_MATCHER.match(s)
        if m:
            debug("ingredient parser successfully parsed %s" % s, 1)
            a, u, i = (m.group(convert.ING_MATCHER_AMT_GROUP), m.group(convert.ING_MATCHER_UNIT_GROUP), m.group(convert.ING_MATCHER_ITEM_GROUP))
            if a:
                asplit = convert.RANGE_MATCHER.split(a)
                if len(asplit) == 2:
                    d["amount"] = convert.frac_to_float(asplit[0].strip())
                    d["rangeamount"] = convert.frac_to_float(asplit[1].strip())
                else:
                    d["amount"] = convert.frac_to_float(a.strip())
            if u:
                conv = convert.get_converter()
                if conv and u.strip() in conv.unit_dict:
                    # Don't convert units to our units!
                    d["unit"] = u.strip()
                else:
                    # has this unit been used
                    prev_uses = self.rd.fetch_all(self.rd.ingredients_table, unit=u.strip())
                    if prev_uses:
                        d["unit"] = u
                    else:
                        # otherwise, unit is not a unit
                        i = u + " " + i
            if i:
                optmatch = re.search(r"\s+\(?[Oo]ptional\)?", i)
                if optmatch:
                    d["optional"] = True
                    i = i[0 : optmatch.start()] + i[optmatch.end() :]
                d["item"] = i.strip()
                if get_key:
                    d["ingkey"] = self.km.get_key(i.strip())
            debug("ingredient_parser returning: %s" % d, 0)
            return d
        else:
            debug("Unable to parse %s" % s, 0)
            d["item"] = s
            return d

    ingredient_parser = parse_ingredient

    def ing_search(self, ing, keyed=None, recipe_table=None, use_regexp=True, exact=False):
        """Search for an ingredient."""
        if not recipe_table:
            recipe_table = self.rd.recipe_table
        vw = self.joined_search(recipe_table, self.rd.ingredients_table, search_by="ingkey", search_str=ing, use_regexp=use_regexp, exact=exact)
        if not keyed:
            vw2 = self.joined_search(recipe_table, self.rd.ingredients_table, search_by="item", search_str=ing, use_regexp=use_regexp, exact=exact)
            if vw2 and vw:
                vw = vw.union(vw2)
            else:
                vw = vw2
        return vw

    def joined_search(self, table1, table2, search_by, search_str, use_regexp=True, exact=False, join_on="id"):
        raise NotImplementedError

    def ings_search(self, ings, keyed=None, recipe_table=None, use_regexp=True, exact=False):
        """Search for multiple ingredients."""
        raise NotImplementedError

    @classmethod
    def get_recipe_manager(cls, **kwargs):
        """Class method to get a specific instance of the manager"""
        return cls.instance_for(**kwargs)

    @classmethod
    def default_rec_manager(cls):
        """Class method to get the default manager using global/default args."""
        return cls.get_recipe_manager(**dbargs)

    def clear_remembered_optional_ings(self, recipe=None):
        """Clear our memories of optional ingredient defaults.

        If handed a recipe, we clear only for the recipe we've been
        given.

        Otherwise, we clear *all* recipes.
        """
        table = self.rd.ingredients_table
        filters = [table.c.shopoptional.in_([1, 2])]

        if recipe:
            recipe_id = recipe.id if hasattr(recipe, "id") else recipe
            filters.append(table.c.recipe_id == recipe_id)

        stmt = update(table).where(and_(*filters)).values(shopoptional=0)

        with self.rd.db.connect() as conn:
            conn.execute(stmt)
            conn.commit()


class DatabaseConverter(convert.Converter):

    def __init__(self, db):
        self.db = db
        # Use modern Python super() initialization
        super().__init__()

    # FIXME: still need to finish this class and then
    # replace calls to convert.converter with
    # calls to DatabaseConverter

    def create_conv_table(self):
        self.conv_table = dbDic(
            "ckey", "value", self.db.convtable_table, self.db
        )
        # Iterate over dictionary items dynamically without list()
        for k, v in defaults.CONVERTER_TABLE.items():
            if k not in self.conv_table:
                self.conv_table[k] = v

    def create_density_table(self):
        self.density_table = dbDic(
            "dkey", "value", self.db.density_table, self.db
        )
        for k, v in defaults.DENSITY_TABLE.items():
            if k not in self.density_table:
                self.density_table[k] = v

    def create_cross_unit_table(self):
        self.cross_unit_table = dbDic(
            "cukey", "value", self.db.crossunitdict_table, self.db
        )
        for k, v in defaults.CROSS_UNIT_TABLE:
            if k not in self.cross_unit_table:
                self.cross_unit_table[k] = v

    def create_unit_dict(self):
        self.units = defaults.UNITS
        self.unit_dict = dbDic(
            "ukey", "value", self.db.unitdict_table, self.db
        )
        for itm in self.units:
            key = itm[0]
            variations = itm[1]
            self.unit_dict[key] = key
            for v in variations:
                self.unit_dict[v] = key


class dbDic:
    def __init__(self, keyprop, valprop, view, db):
        """Create a dictionary interface to a database table."""
        self.vw = view
        self.kp = keyprop
        self.vp = valprop
        self.db = db
        self.just_got = {}

    def has_key(self, k):
        try:
            self.just_got = {k: self.__getitem__(k)}
            return True
        except Exception:
            try:
                self.__getitem__(k)
                return True
            except Exception:
                return False

    def __setitem__(self, k, v):
        store_v = v
        row = self.db.fetch_one(self.vw, **{self.kp: k})
        if row:
            self.db.do_modify(self.vw, row, {self.vp: store_v}, id_col=self.kp)
        else:
            self.db.do_add(self.vw, {self.kp: k, self.vp: store_v})
        self.db.changed = True
        return v

    def __getitem__(self, k):
        if k in self.just_got:
            return self.just_got[k]

        criteria = {self.kp: k}
        row = self.db.fetch_one(self.vw, criteria=criteria)
        if row is None:
            raise KeyError(k)

        return row[self.vp]

    def __repr__(self):
        return f"<dbDic table={self.vw.name} key={self.kp}>"

    def initialize(self, d):
        """Initialize values based on dictionary d.

        We assume the DB is known to be empty.
        """
        dics = [{self.kp: k, self.vp: d[k]} for k in d]
        if not dics:
            return

        stmt = insert(self.vw)
        with self.db.connect() as conn:
            conn.execute(stmt, dics)
            conn.commit()

    def keys(self):
        rows = self.db.fetch_all(self.vw)
        return [row[self.kp] for row in rows]

    def values(self):
        rows = self.db.fetch_all(self.vw)
        return [row[self.vp] for row in rows]

    def items(self):
        return list(zip(self.keys(), self.values()))


def get_database(*args, **kwargs):
    return RecData.instance_for(*args, **kwargs)


def backup_database(filename: Path) -> Path:
    if not filename:
        return

    backup_name = filename.with_name(filename.name + ".backup-" + time.strftime("%d-%m-%y"))

    while backup_name.is_file():
        backup_name = backup_name.with_name(backup_name.name + "I")

    show_message(
        title=_("Database Backup"),
        label=_("Database Backup"),
        sublabel=_("Depending on the size of your database, this may take some time."),
        expander=(
            _("Details"),
            _(
                "A backup will be made as %s in case something goes wrong."
                " If this upgrade fails, you can manually rename the "
                "backup file to recipes.db to recover it."
            )
            % backup_name,
        ),
        message_type=Gtk.MessageType.INFO,
    )

    shutil.copy(filename, backup_name)

    assert backup_name.is_file()
    return backup_name
