"""Capstone 1: National Parks Site and Journal"""
from flask import Flask, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
import requests
from models import db, connect_db, User
from forms import SearchForm, RegistrationForm

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

# create tables in database
db.drop_all()
db.create_all()

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

    return render_template("results.html", parks_data=parks_data, state_code=state_code)

@app.route("/register", methods=["GET", "POST"])
def register_form():
    """Display registration form (GET) or create a user and show user dashboard (POST)"""
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        # add username to session for authorization
        session["user_id"] = user.id

        flash("User successfully created")
        # on successful login, redirect to users page
        return redirect(f"/users/{ user.id }")

    return render_template("register.html", form=form)

@app.route("/users/<int:user_id>")
def user_page(user_id):
    """Show logged in user page"""

    if "user_id" in session:
        user = User.query.get_or_404(user_id)

        return render_template("user_dashboard.html", user=user)

    flash("Need to be logged in first")
    return redirect("/")

@app.route("/logout")
def logout_user():
    """Logout currently logged in user"""

    session.pop("user_id")
    return redirect("/")