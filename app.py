"""Capstone 1: National Parks Site and Journal"""
from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
import requests
from models import db, connect_db
from forms import SearchForm

app = Flask(__name__)

# we are using a postgres database and this is our database to connect to.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone_1_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# from models.py
connect_db(app)

@app.route("/", methods=["GET", "POST"])
def show_home():
    """Homepage to show search form, park spotlight, and journaling overview (GET) or get search term and redirect to results page (POST)"""

    form = SearchForm()

    if form.validate_on_submit():
        state = form.state.data

        return redirect(f"results/{ state }")

    return render_template("index.html", form=form)

@app.route("/about")
def show_about():
    """Show about page for site"""

    return render_template("about.html")

@app.route("/results/<state>")
def get_search_results(state):
    """Use search term and call API to show results"""

    state_code = state

    parks = requests.get(f"https://developer.nps.gov/api/v1/parks?stateCode={ state_code }&api_key=vG3tRs4GwEF0x8qK9FmVp5h8AhZjbkH13FydMyTc")
    parks_json = parks.json()
    parks_data = parks_json["data"]

    return render_template("results.html", parks_data=parks_data)