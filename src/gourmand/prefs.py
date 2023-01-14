import shutil
from pathlib import Path
from typing import Any, Optional

import toml

from gourmand.gglobals import gourmanddir


class Prefs(dict):
    """A singleton dictionary for handling preferences."""

    __single = None

    @classmethod
    def instance(cls):
        if Prefs.__single is None:
            Prefs.__single = cls()

        return Prefs.__single

    def __init__(self, filename='preferences.toml'):
        super().__init__()
        self.filename = Path(gourmanddir) / filename
        self.load()

    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        if key not in self and default is not None:
            self[key] = default
        return super().get(key)

    def save(self):
        self.filename.parent.mkdir(exist_ok=True)
        with open(self.filename, 'w') as fout:
            toml.dump(self, fout)

    def load(self) -> bool:
        if self.filename.is_file():
            with open(self.filename) as fin:
                for k, v in toml.load(fin).items():
                    self.__setitem__(k, v)
            return True
        return False


def update_preferences_file_format(target_dir: Path = gourmanddir):
    """Update saved preferences upon updates.

    This function is called upon launch to handle changes in the structure of the preference.
    Each change applied is documented inline.
    """
    filename = target_dir / 'preferences.toml'
    if not filename.is_file():
        return

    with open(filename) as fin:
        prefs = toml.load(fin)

    # Gourmand 1.2.0: several sorting parameters can be saved.
    # The old format had `column=name` and `ascending=bool`, which are now `name=bool`
    sort_by = prefs.get('sort_by')
    if sort_by is not None:
        if 'column' in sort_by.keys():  # old format
            prefs['sort_by'] = {sort_by['column']: sort_by['ascending']}

    with open(filename, 'w') as fout:
        toml.dump(prefs, fout)


def copy_old_installation_or_initialize(target_dir: Path):
    """Initialize or migrate earlier installations.

    Previous installations of Gourmand or Gourmet, stored in "~/gourmand" or
    "~/gourmet" will be copied across if the specified directory does not
    exist.

    If both gourmand and gourmet directories exist, then the gourmet directory,
    presumably newer, is migrated.
    """
    target_db = target_dir / 'recipes.db'
    if target_db.is_file():
        return

    legacy_gourmet = Path('~/.gourmet').expanduser()
    legacy_gourmand = Path('~/.gourmand').expanduser()

    source_dir = None
    if legacy_gourmet.is_dir():
        source_dir = legacy_gourmet
    if legacy_gourmand.is_dir():
        source_dir = legacy_gourmand

    if source_dir is not None:
        shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)

    if not target_db.is_file():
        print("First time? We're setting you up with yummy recipes.")
        target_dir.mkdir(exist_ok=True)
        default_db = Path(__file__).parent.absolute() / 'backends' / 'default.db'  # noqa
        shutil.copyfile(default_db, target_dir / 'recipes.db')
