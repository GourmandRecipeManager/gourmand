from unittest.mock import Mock
import pytest

from gourmand.plugins.nutritional_information.nutrition import NutritionData

@pytest.mark.parametrize(
    'description, mock_content, expected',
    [
        ('', ['', ''], []),
        ('with', ['', ''], []),
        ('what a str', ['str', 5], [('str', 5)])
    ],
)
def test_get_matches(description, mock_content, expected):
    content_mock = Mock()
    content_mock.desc = mock_content[0]
    content_mock.ndbno = mock_content[1]

    mock_db = Mock()
    mock_db.search_nutrition = Mock(return_value=(content_mock,))

    nd = NutritionData(db=mock_db, conv=None)

    ret = nd.get_matches(description)
    assert ret == expected
