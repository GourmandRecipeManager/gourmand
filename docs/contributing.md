# Contributing

Thank you for taking an interest in contributing to Gourmand! We appreciate that
you're thinking about offering your time to improving the project, and it's our
goal to respect your contribution accordingly.

Although this document focuses on code contributions, you can contribute in
several ways:

- File a bug report.
- Add or improve documentation.
- Promote the project to others.

## Contributing Code

In general, the process for contributing code is:

1. Pick or open an [issue](https://github.com/GourmandRecipeManager/gourmand/issues) to work
   on
2. Post a comment expressing your intent to make sure nobody else is already
   working on it
3. Set up a development environment, as described below
4. Do your changes, and when ready
5. Push your changes to your forked repo and create a pull request.

## Setting Up a Development Environment

Fork and clone Gourmand.

Ensure your system has the necessary prerequisites installed:

- [Python](https://www.python.org/), which is what Gourmand is written in.
- [PyGObject](https://pygobject.readthedocs.io/en/latest/) for GTK+ 3 and
  other GNOME libraries. You may either install your system's `pygobject`
  package(s) or install the necessary system requirements to install
  `pygobject` from PyPI with `pip`. The latter method is recommended if you
  plan on doing development within a Python virtual environment.
- [intltool](https://freedesktop.org/wiki/Software/intltool/) for
  internationalization.
- (optional) [Enchant](https://abiword.github.io/enchant/) for spell-checking.
  At least one of the backends must be installed as well.
- (optional) [GStreamer](https://gstreamer.freedesktop.org/) for sound. The
  GStreamer library itself and gst-plugins-base are required. Python bindings
  are provided through PyGObject, so GObject introspection data is also needed.
- (optional) [poppler](https://poppler.freedesktop.org/) for exporting PDFs.
  Python bindings are provided through PyGObject, so install the GLIB bindings
  and associated GObject introspection data.

**Note:** Although some prerequisites are optional, the development install of
Gourmand enables all plugins and features, so you probably want to install all
prerequisites to avoid any issues.

You may want to set up a [Python virtual
environment](https://docs.python.org/3/library/venv.html). This is optional but
highly recommended:

```bash
$ python -m venv --prompt gourmand venv
$ source venv/bin/activate
(gourmand) $ pip install -U pip setuptools wheel
```

Then install Gourmand itself:

```bash
(gourmand) $ pip install -r development.in
```

This installs the remaining Python dependencies and Gourmand itself in editable
mode, which allows you to run Gourmand and see your changes without having to
reinstall it.

**Note:** If you encounter an error during the installation of
`pygtkspellcheck`, first install `pyenchant` and `pygobject` on their own:

```bash
(gourmand) $ pip install pyenchant pygobject
(gourmand) $ pip install -r development.in
```

You should now be able to launch and run Gourmand:

```bash
(gourmand) $ gourmand
```

## Style

Gourmand uses *ruff* for checking the code style, while trying to closely follow
[PEP 8](http://www.python.org/dev/peps/pep-0008/).

Check the style:

```bash
ruff check src/ tests/ setup.py
```

## Issues and Suggestions

We welcome feedback and issue reporting. You can do so by browsing existing
issues and commenting on them, or creating a new one.

When reporting an issue, please fill in the provided template.

For feedback or requests of features, please explain with details, and
screenshots if possible, what you would like.

## Translations

The following describes how to contribute translation.

Update the translation template:

```bash
cd po/
intltool-update -p -g gourmand
```

A file `gourmand.pot` should have been modified. Add it to git.

If modifying an already existing translation, update the translation file:

```bash
msgmerge --update --no-fuzzy-matching --backup=off fr.po gourmand.pot
```

If adding translation for a new language, copy the file for your target
language, such as `fr.po` or `de_AT.po`, if translating for a specific region,
and add it to git.

Once the translation is done, update the translations:

```bash
python private/update_i18n.py
```

Launch Gourmand and check the changes.  
Once satisfied, open a pull request with your work.

## Testing

Gourmand have a test suite in the `tests` directory. Patches that expands it are welcome.
It is run with [pytest](https://docs.pytest.org/):

```bash
LC_ALL=C pytest
```

Most modern python IDEs have support for running the tests using pytest.

**Warning:** Running the tests will most likely mess with your local configuration and
database file. Please make sure to backup the corresponding directory content manually
BEFORE running the tests.

**Note:** The current test suite unfortunately is rather small, thus we tend to be
careful with changes which might break stuff. The maintainers encourage every
contributor to add tests alongside their patches and/or utilize the principles of
test-driven development by writing tests before fixing a bug.

## Blaming

Consider using

```bash
git blame --ignore-revs-file .git-blame-ignore-revs
```

instead of plain blaming to ignore some mostly irrelevant commits.
