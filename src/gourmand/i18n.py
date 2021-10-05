"""Internationalization for Gourmand.

This file defines a gettext-like interface with the gourmet domain, and is
later imported in the rest of the application.
"""
import gettext
import locale
from pathlib import Path

mo_path = Path(__file__).parent / 'data' / 'locale'

locale.bindtextdomain('gourmand', mo_path)
langs = gettext.translation('gourmand', mo_path, fallback=True)
_ = langs.gettext
