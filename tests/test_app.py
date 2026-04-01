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


def test_login_with_invalid_email():
    """Tests that an invalid email is rejected"""
    with app.test_client() as c:
        resp = c.post(
            "/login", data={"email": "not-a-club@example.com"}, follow_redirects=True
        )

        assert request.path == "/login"
        assert resp.status_code == 401
        assert "Unknown email. Please try again." in resp.data.decode()
