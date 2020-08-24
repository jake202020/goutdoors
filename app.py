"""Capstone 1: National Parks Site and Journal"""
from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
import requests

app = Flask(__name__)

# we are using a postgres database and this is our database to connect to.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone_1_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route("/")
def show_home():
    """Homepage to show information about site"""
    # parks = requests.get("https://developer.nps.gov/api/v1/parks?api_key=vG3tRs4GwEF0x8qK9FmVp5h8AhZjbkH13FydMyTc")
    # parks_json = parks.json()
    # parks_data = parks_json["data"]

    # return render_template("index.html", parks=parks_data)
    return render_template("index.html")