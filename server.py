from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, session, url_for

from provider import get_clubs, get_competitions

app = Flask(__name__)
# You should change the secret key in production!
app.secret_key = "something_special"


def is_past_competition(competition):
    """Checks whether a competition date is in the past"""
    competition_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
    return competition_date < datetime.now()


@app.route("/")
def index():
    """Homepage"""
    return render_template("index.html")


@app.route("/clubs")
def clubs():
    """Public page showing clubs and their available points"""
    return render_template("clubs.html", clubs=get_clubs())


@app.route("/login", methods=["POST"])
def login():
    """Use the session object to store the club information across requests"""
    clubs = get_clubs()
    email = request.form["email"]
    club = next((item for item in clubs if item["email"] == email), None)

    if club is None:
        flash("Unknown email. Please try again.")
        return render_template("index.html"), 401

    session["club"] = club

    return redirect(url_for("summary"))


@app.route("/summary")
def summary():
    """Custom "homepage" for logged in users"""

    club = session["club"]
    competitions = get_competitions()

    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>")
def book(competition):
    """Book spots in a competition page"""
    club = session["club"]

    competitions = get_competitions()
    matching_comps = [comp for comp in competitions if comp["name"] == competition]
    if not matching_comps:
        return render_template(
            "error.html", message="This competition does not exist."
        ), 404

    found_competition = matching_comps[0]

    if is_past_competition(found_competition):
        return render_template(
            "error.html", message="This competition has already taken place."
        ), 403

    return render_template("booking.html", club=club, competition=found_competition)


@app.route("/book", methods=["POST"])
def book_spots():
    """This page is only accessible through a POST request (form validation)"""
    club = session["club"]
    competitions = get_competitions()

    matching_comps = [
        comp for comp in competitions if comp["name"] == request.form["competition"]
    ]

    competition = matching_comps[0]

    if is_past_competition(competition):
        return render_template(
            "error.html", message="This competition has already taken place."
        ), 403

    spots_required = int(request.form["spots"])

    if spots_required > 12:
        return render_template(
            "error.html", message="You cannot book more than 12 spots."
        ), 403

    if spots_required > int(club["points"]):
        return render_template(
            "error.html", message="You do not have enough points."
        ), 403

    if spots_required > int(competition["spotsAvailable"]):
        return render_template(
            "error.html", message="There are not enough spots available."
        ), 403

    club["points"] = str(int(club["points"]) - spots_required)
    session["club"] = club
    competition["spotsAvailable"] = int(competition["spotsAvailable"]) - spots_required
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/logout")
def logout():
    """We delete session data in order to log the user out"""
    del session["club"]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
