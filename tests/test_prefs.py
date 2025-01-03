from pathlib import Path
from sys import version_info

import pytest

if version_info >= (3, 11):
    from tomllib import loads as toml_loads
else:
    from tomli import loads as toml_loads

from tomli_w import dumps as toml_dumps

from gourmand.prefs import Prefs, update_preferences_file_format


def test_singleton():
    prefs = Prefs.instance()
    pprefs = Prefs.instance()
    assert prefs == pprefs


def test_get_sets_default():
    """Test that using get with a default value adds it to the dictionnary"""
    prefs = Prefs.instance()

    val = prefs.get("key", "value")
    assert val == val

    assert prefs["key"] == val  # The value was inserted

    val = prefs.get("anotherkey")
    assert val is None

    with pytest.raises(KeyError):
        prefs["anotherkey"]


def test_update_preferences_file_format(tmpdir):
    """Test the update of preferences file format."""

    filename = tmpdir.join("preferences.toml")

    with open(filename, "w") as fout:
        fout.write(toml_dumps({"sort_by": {"column": "title", "ascending": True}}))

    update_preferences_file_format(Path(tmpdir))

    with open(filename) as fin:
        d = toml_loads(fin.read())

    assert "category" not in d["sort_by"].keys()
    assert d["sort_by"]["title"]

    with open(filename, "w") as fout:
        fout.write(toml_dumps({}))

    update_preferences_file_format(Path(tmpdir))

    with open(filename) as fin:
        d = toml_loads(fin.read())

    assert d == {}
