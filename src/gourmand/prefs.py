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


def copy_old_installation_or_initialize(target_dir: Path):
    """Initialize or migrate earlier installations.

    Previous installations of Gourmand or Gourmet, stored in "~/gourmand" or
    "~/gourmet" will be copied across if the specified directory does not
    exist.

    If both gourmand and gourmet directories exist, then the gourmet directory,
    presumably newer, is migrated.
    """
    if target_dir.is_dir():
        return

    legacy_gourmet = Path('~/.gourmet').expanduser()
    legacy_gourmand = Path('~/.gourmand').expanduser()

    source_dir = None
    if legacy_gourmet.is_dir():
        source_dir = legacy_gourmet
    if legacy_gourmand.is_dir():
        source_dir = legacy_gourmand

    if source_dir is not None:
        shutil.copytree(source_dir, target_dir)
    else:
        print("First time? We're setting you up with yummy recipes.")
        target_dir.mkdir()
        default_db = Path(__file__).parent.absolute() / 'backends' / 'default.db'
        shutil.copyfile(default_db, target_dir / 'recipes.db')