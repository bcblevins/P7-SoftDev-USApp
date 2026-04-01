from provider import get_clubs, get_competitions


def test_get_clubs_loads_expected_data():
    """Tests that clubs can be loaded from the JSON file"""
    clubs = get_clubs()

    assert len(clubs) > 0
    assert clubs[0]["name"] == "Simply Lift"
    assert clubs[0]["email"] == "john@simplylift.co"


def test_get_competitions_loads_expected_data():
    """Tests that competitions can be loaded from the JSON file"""
    competitions = get_competitions()

    assert len(competitions) > 0
    assert competitions[0]["name"] == "Spring Festival"
    assert "spotsAvailable" in competitions[0]
