"""
Create/update po/pot translation files.
"""

import shutil
import subprocess
from pathlib import Path

PACKAGE = "gourmand"
CURRENT_DIRECTORY = Path(__file__).parent
PACKAGEDIR = CURRENT_DIRECTORY.parent / "src" / PACKAGE
PODIR = CURRENT_DIRECTORY.parent / "po"
LANGS = sorted(f.stem for f in PODIR.glob("*.po"))


def main():
    print("Creating POT files")
    intltool_update = shutil.which("intltool-update")
    cmd = [intltool_update, "--pot", f"--gettext-package={PACKAGE}"]
    if not intltool_update:
        print(f"intltool-update not found, skipping {cmd!r} call ...")
    else:
        subprocess.run(cmd, cwd=PODIR)

    for lang in LANGS:
        print(f"Updating {lang}.po")
        cmd = [intltool_update, "--dist", f"--gettext-package={PACKAGE}", lang]
        if not intltool_update:
            print(f"intltool-update not found, skipping {cmd!r} call ...")
        else:
            subprocess.run(cmd, cwd=PODIR)


if __name__ == "__main__":
    main()
