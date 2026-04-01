# gudlift-registration

### Why

This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

### Getting Started

This project uses the following technologies:

* Python v3.x+
* [Flask](https://flask.palletsprojects.com/)
* [Virtual environment](https://docs.python.org/3/library/venv.html)


### Installation

- Clone the repository and create a new virtual (`python -m venv <VENV_FOLDER>`)

- Make sure the virtual environment you created is active

- Install the requirements based on the `requirements.txt` file: `pip install -r requirements.txt`

- Run the application with `python server.py`. The app will start and display in the terminal a link where you can access it (locally) using your browser.

### How To Use The App

- Open the homepage and log in with a club secretary email from `data/clubs.json`
- No password is required in this proof of concept
- After logging in, you can see:
  - the club email
  - the club points
  - the competition list
- The homepage also has a public link to the clubs page so any user can see clubs and their available points

### Current Features

- Club secretary login by email
- Invalid login returns an error
- Public clubs page
- Competition summary page
- Booking page for valid future competitions
- Booking validation for:
  - more than 12 spots
  - not enough club points
  - not enough competition spots
- Past competitions cannot be booked

### Current setup

The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). They live in the `data` folder.
    
* `competitions.json` - list of competitions
* `clubs.json` - list of clubs with relevant information. Inspect this file to find email addresses you can use to login.

### Testing

The project uses [pytest](https://docs.pytest.org/). You should also use [coverage](https://coverage.readthedocs.io/) to create a coverage report.

- Run tests with: `pytest -q`
- Tests are stored in the `tests` folder

### Notes

- Data is stored in JSON files and is loaded at runtime
- This project uses Flask templates and does not require JavaScript
