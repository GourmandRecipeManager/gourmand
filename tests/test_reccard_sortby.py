from unittest import mock

from gourmand.main import get_application
from gourmand.reccard import RecSelector


def test_sort_by(tmp_path):
    """Test the sort_by property of the RecSelector class."""
    with mock.patch("gourmand.gglobals.gourmanddir", tmp_path):
        rec_gui = get_application()

        # Mock UI-related calls within the RecSelector constructor to prevent
        # windows from being created during the test run.
        with mock.patch("gourmand.reccard.RecIndex.__init__", return_value=None), \
                mock.patch("gi.repository.Gtk.Dialog") as mock_dialog, \
                mock.patch("gi.repository.Gtk.Builder.get_object"):
            # The RecSelector constructor calls self.dialog.run(). We ensure the mock
            # for Gtk.Dialog doesn't block the test execution.
            mock_dialog.return_value.run.return_value = None

            # The RecSelector constructor expects an IngredientEditorModule instance.
            # We can mock this dependency.
            mock_ing_editor = mock.Mock()

            # Instantiate the class under test
            rec_selector = RecSelector(rec_gui, mock_ing_editor)

            # Test setting the sort_by property
            sort_order = [("name", 1), ("rating", -1)]
            rec_selector.sort_by = sort_order

            # Test the getter - use set to ignore order
            assert set(rec_selector.sort_by) == set(sort_order)

            # Test the underlying preference. RecSelector and rec_gui share
            # the same singleton Prefs instance.
            expected_prefs = {"name": True, "rating": False}
            assert rec_gui.prefs.get("sort_by") == expected_prefs

            # Test setting an empty value
            rec_selector.sort_by = []
            assert "sort_by" not in rec_gui.prefs

            # Test setting to None
            rec_selector.sort_by = sort_order  # set it again
            assert "sort_by" in rec_gui.prefs
            rec_selector.sort_by = None
            assert "sort_by" not in rec_gui.prefs
