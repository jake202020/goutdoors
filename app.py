"""Capstone 1: National Parks Site and Journal"""
from flask import Flask, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
import requests
from models import db, connect_db, User, Park, Journal
from forms import SearchForm, RegistrationForm, LoginForm, JournalForm
from key import api_key

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

BASE_URL = "https://developer.nps.gov/api/v1"

# create tables in database
# db.drop_all()
# db.create_all()

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

# @app.route("/all")
# def get_parks():
#     """Use to get all parks and park codes
# 
#       Have to adjust start in URL by 50 after each call in order to step to the next set of 50"""

#     parks = requests.get(f"{ BASE_URL }/parks?limit=50&start=450&api_key={ api_key }")
#     parks_json = parks.json()
#     parks_data = parks_json["data"]

#     return render_template("all.html", parks=parks_data)

@app.route("/results/<state>")
def get_search_results(state):
    """Use search term and call API to show results"""

    state_code = state

    parks = requests.get(f"{ BASE_URL }/parks?stateCode={ state_code }&api_key={ api_key }")
    parks_json = parks.json()
    parks_data = parks_json["data"]

    return render_template("results.html", parks_data=parks_data, state_code=state_code)

@app.route("/register", methods=["GET", "POST"])
def register_form():
    """Display registration form (GET) or create a user and show user dashboard (POST)"""
    form = RegistrationForm()

    # if there is already a user logged in, let them know to logout
    if "user_id" in session:
        flash("Must logout first to register new user")
        return redirect("/")
        
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
        session["username"] = user.username

        flash("User successfully created")
        # on successful login, redirect to users page
        return redirect(f"/users/{ user.id }")

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login_form():
    """Display login form (GET) or login user and show user dashboard (POST)"""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(username, password)

        if user:
            flash("Login Successful")

            # Add user_id to session for authorization
            session["username"] = user.username

            # on successful login, redirect to dashboard
            return redirect(f"/users/{ user.username }")
        else:
            form.username.errors = ["Bad username and/or password"]

    return render_template("login.html", form=form)

@app.route("/users/<username>")
def user_page(username):
    """Show logged in user page"""

    if "username" in session:
        user = User.query.get_or_404(username)

        journals = Journal.query.filter(Journal.username == username).all()

        return render_template("user_dashboard.html", user=user, journals=journals)

    flash("Need to be logged in first")
    return redirect("/")

@app.route("/users/<username>/journals/new", methods=["GET", "POST"])
def new_journal(username):
    """Show form for adding a new journal (GET) or add journal to db and go to user page (POST)"""
    form = JournalForm()

    return render_template("new_journal.html", form=form)

@app.route("/logout")
def logout_user():
    """Logout currently logged in user"""

    session.pop("user_id")
    return redirect("/")