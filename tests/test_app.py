from flask import request

from server import app


def test_homepage():
    """Test the homepage works (HTTP status 200 OK)"""
    with app.test_client() as c:
        resp = c.get("/")
        assert resp.status_code == 200


def test_login():
    """Tests a login action"""
    with app.test_client() as c:
        resp = c.post(
            "/login", data={"email": "john@simplylift.co"}, follow_redirects=True
        )
        # The status code should be 200 OK
        assert resp.status_code == 200
        # The email of the user logged in is displayed on the page
        assert "john@simplylift.co" in resp.data.decode()
        # The page shows the logged-in club points
        assert "Points available: 13" in resp.data.decode()


def test_summary_only_shows_booking_link_for_future_competitions(monkeypatch):
    """Tests that past competitions are not shown as bookable"""
    monkeypatch.setattr(
        "server.get_competitions",
        lambda: [
            {
                "name": "Spring Festival",
                "date": "2030-03-27 10:00:00",
                "spotsAvailable": "25",
            },
            {
                "name": "Fall Classic",
                "date": "2020-10-22 13:30:00",
                "spotsAvailable": "13",
            },
        ],
    )

    with app.test_client() as c:
        resp = c.post(
            "/login", data={"email": "john@simplylift.co"}, follow_redirects=True
        )

        assert resp.status_code == 200
        page = resp.data.decode()
        assert "Spring Festival" in page
        assert "Fall Classic" in page
        assert page.count("Book spots") == 1


def test_login_with_invalid_email():
    """Tests that an invalid email is rejected"""
    with app.test_client() as c:
        resp = c.post(
            "/login", data={"email": "not-a-club@example.com"}, follow_redirects=True
        )

        assert request.path == "/login"
        assert resp.status_code == 401
        assert "Unknown email. Please try again." in resp.data.decode()


def test_clubs_page_is_public():
    """Tests that any user can see the clubs page"""
    with app.test_client() as c:
        resp = c.get("/clubs")

        assert resp.status_code == 200
        page = resp.data.decode()
        assert "Simply Lift" in page
        assert "Iron Temple" in page
        assert "Points available" in page


def test_booking_updates_points_and_available_spots(monkeypatch):
    """Tests that a successful booking updates club points and competition spots"""
    monkeypatch.setattr(
        "server.get_competitions",
        lambda: [
            {
                "name": "Spring Festival",
                "date": "2030-03-27 10:00:00",
                "spotsAvailable": "25",
            },
            {
                "name": "Fall Classic",
                "date": "2030-10-22 13:30:00",
                "spotsAvailable": "13",
            },
        ],
    )

    with app.test_client() as c:
        c.post("/login", data={"email": "john@simplylift.co"}, follow_redirects=True)

        resp = c.post(
            "/book",
            data={"competition": "Spring Festival", "spots": "1"},
            follow_redirects=True,
        )

        assert resp.status_code == 200
        page = resp.data.decode()
        assert "Great-booking complete!" in page
        assert "Points available: 12" in page
        assert "Number of spots available: 24" in page


def test_booking_more_than_twelve_spots_is_forbidden(monkeypatch):
    """Tests that a club cannot book more than 12 spots"""
    monkeypatch.setattr(
        "server.get_competitions",
        lambda: [
            {
                "name": "Spring Festival",
                "date": "2030-03-27 10:00:00",
                "spotsAvailable": "25",
            },
            {
                "name": "Fall Classic",
                "date": "2030-10-22 13:30:00",
                "spotsAvailable": "13",
            },
        ],
    )

    with app.test_client() as c:
        c.post("/login", data={"email": "john@simplylift.co"}, follow_redirects=True)

        resp = c.post(
            "/book",
            data={"competition": "Spring Festival", "spots": "13"},
            follow_redirects=True,
        )

        assert resp.status_code == 403
        assert "You cannot book more than 12 spots." in resp.data.decode()


def test_booking_more_than_available_points_is_forbidden(monkeypatch):
    """Tests that a club cannot book more spots than its points allow"""
    monkeypatch.setattr(
        "server.get_competitions",
        lambda: [
            {
                "name": "Spring Festival",
                "date": "2030-03-27 10:00:00",
                "spotsAvailable": "25",
            },
            {
                "name": "Fall Classic",
                "date": "2030-10-22 13:30:00",
                "spotsAvailable": "13",
            },
        ],
    )

    with app.test_client() as c:
        c.post("/login", data={"email": "admin@irontemple.com"}, follow_redirects=True)

        resp = c.post(
            "/book",
            data={"competition": "Spring Festival", "spots": "5"},
            follow_redirects=True,
        )

        assert resp.status_code == 403
        assert "You do not have enough points." in resp.data.decode()


def test_booking_more_than_available_competition_spots_is_forbidden(monkeypatch):
    """Tests that a club cannot book more spots than the competition has left"""
    def limited_competitions():
        return [
            {
                "name": "Spring Festival",
                "date": "2030-03-27 10:00:00",
                "spotsAvailable": "3",
            }
        ]

    monkeypatch.setattr("server.get_competitions", limited_competitions)

    with app.test_client() as c:
        c.post("/login", data={"email": "john@simplylift.co"}, follow_redirects=True)

        resp = c.post(
            "/book",
            data={"competition": "Spring Festival", "spots": "4"},
            follow_redirects=True,
        )

        assert resp.status_code == 403
        assert "There are not enough spots available." in resp.data.decode()


def test_booking_invalid_competition_returns_404():
    """Tests that an unknown competition returns a 404 page"""
    with app.test_client() as c:
        c.post("/login", data={"email": "john@simplylift.co"}, follow_redirects=True)

        resp = c.get("/book/Competition That Does Not Exist")

        assert resp.status_code == 404
        assert "This competition does not exist." in resp.data.decode()


def test_booking_past_competition_returns_403():
    """Tests that a past competition cannot be booked"""
    with app.test_client() as c:
        c.post("/login", data={"email": "john@simplylift.co"}, follow_redirects=True)

        resp = c.get("/book/Spring Festival")

        assert resp.status_code == 403
        assert "This competition has already taken place." in resp.data.decode()
