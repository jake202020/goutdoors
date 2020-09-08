"""Capstone 1: National Parks Site and Journal"""
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_login import LoginManager, login_required, logout_user, current_user, login_user

import requests
import os
from sqlalchemy.exc import IntegrityError

from datetime import datetime

from models import db, connect_db, User, Park, Journal, Visit
from forms import SearchForm, RegistrationForm, LoginForm, NewJournalForm, EditJournalForm, EditUserForm

app = Flask(__name__)
Bootstrap(app)

# login manager initialization
login_manager = LoginManager()
login_manager.init_app(app)

from tokens import generate_confirmation_token, confirm_token
from secrets import MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USE_SSL, MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER, SECRET_KEY

from secrets import api_key, admin_user

# we are using a postgres database and this is our database to connect to.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'postgresql:///capstone_1_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", SECRET_KEY)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# mail settings
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL

# gmail authentication
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

# mail accounts
app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER

# from models.py
connect_db(app)

# email setup and import
mail = Mail(app)
from send import send_email

# Base URL for NPS API
BASE_URL = "https://developer.nps.gov/api/v1"

##############################################
############## General Routes ################
##############################################

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

    parks = requests.get(f"{ BASE_URL }/parks?stateCode={ state_code }&api_key={ api_key }")
    parks_json = parks.json()
    parks_data = parks_json["data"]

    for park in parks_data:
        visit_count = Visit.query.filter(Visit.park_code == park["parkCode"]).count()
        park["visit_count"] = visit_count

        db.session.commit()

    if current_user.is_authenticated:
        user_id = current_user.id
        user = User.query.get_or_404(user_id)
        visits = Visit.query.filter(Visit.id == user_id).all()

        if visits:
            for visit in visits:
                adjusted_date = visit.date_of_visit.strftime("%b %d, %Y")
                visit.date_of_visit = adjusted_date

            return render_template("results.html", parks_data=parks_data, state_code=state_code, visits=visits, user=user)


        return render_template("results.html", parks_data=parks_data, state_code=state_code, user=user)

    else:
        return render_template("results.html", parks_data=parks_data, state_code=state_code)

    
##############################################
############## Signup, Login, Logout #########
##############################################

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on page load"""
    if user_id is not None:
        user = User.query.get_or_404(user_id)
        return user
    return None

@login_manager.unauthorized_handler
def Unauthorized():
    """Redirect unauthorized users to Login page."""
    flash("You must be logged in to view that page")
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register_form():
    """Display registration form (GET) or create a user and show user dashboard (POST)"""
    form = RegistrationForm()
        
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user is None:
            username = form.username.data
            password = form.password.data
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            confirmed=False
            role = "user"
            created_at = datetime.now()
            # Create user in db and commit
            user = User.register(username, password, email, first_name, last_name, confirmed, role, created_at)
            db.session.add(user)
            db.session.commit()
            # send confirmation email
            send_confirmation(user)
            # on successful login, redirect to users page
            login_user(user)
            return redirect(f"/users/{ user.username }")

        flash("Username taken")

    return render_template("register.html", form=form)

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or expired.')
    
    user = User.query.get_or_404(current_user.id)

    if user.confirmed:
        flash('Account already confirmed. Please login.')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        db.session.commit()

        flash('You have confirmed your account. Thanks!')
        return redirect(f"/users/{ user.username }")

    return redirect('/')

@app.route('/resend')
def resend_confirmation():
    # get a new confirmation email
    new_confirmation_email()

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login_form():
    """Display login form (GET) or login user and show user dashboard (POST)"""
    if current_user.is_authenticated:
        user = User.query.get_or_404(current_user.id) 
        return redirect(f"/users/{ user.username }")

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        username = form.username.data
        password = form.password.data
        
        if user and user.authenticate(username, password):
            login_user(user)
            next_page = request.args.get('next')

            if user.role == "admin":    
                flash(f"Logged in as ADMIN")
                return redirect(next_page or "/users/admin")

            else:
                flash("Login Successful")
                # on successful login, redirect to dashboard
                return redirect(next_page or f"/users/{ user.username }")
        else:
            form.username.errors = ["Bad username and/or password"]

    return render_template("login.html", form=form)


##############################################
############## User Routes ###################
##############################################

@app.route("/users/<username>")
@login_required
def user_page(username):
    """Show logged in user page"""
    # Check if logged in user is this user
    if is_correct_user(username):
        user = User.query.filter_by(username=username).first()

        journals = Journal.query.filter(Journal.user_id == user.id).order_by(Journal.date_of_visit.desc()).all()

        for journal in journals:
            adjusted_date = journal.date_of_visit.strftime("%b %d, %Y")
            journal.date_of_visit = adjusted_date

        return render_template("user_dashboard.html", user=user, journals=journals)

    flash("Unauthorized")
    return redirect("/")

@app.route("/users/<username>/edit", methods=["GET", "POST"])
@login_required
def edit_user(username):
    """Show form for editing user details (GET) or add user edits to db and go to user page (POST)
    
    User cannot change username or password for now"""
    
    # Check if logged in user is this user
    if is_correct_user(username):
        form = EditUserForm(first_name = current_user.first_name,
                            last_name = current_user.last_name,
                            state_code= current_user.state_code)

        if form.validate_on_submit():
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.state_code = form.state_code.data
                            
            db.session.commit()

            flash("User updated")
            # on successful edit, redirect to users page
            return redirect(f"/users/{ current_user.username }")

        return render_template("edit_user.html", form=form)

    flash("Not your profile")
    return redirect("/")

@app.route("/users/<username>/delete", methods=["POST"])
@login_required
def delete_user(username):
    """Delete logged in user"""

    # Check if logged in user is this user
    if is_correct_user(username):
        db.session.delete(user)
        db.session.commit()

        logout_user()
        flash('User Successfully Deleted')
        return redirect("/")

    flash("Unauthorized")
    return redirect("/")

@app.route("/logout")
@login_required
def logout():
    """Logout currently logged in user"""
    
    logout_user()

    flash(f"Successfully Logged Out")
    return redirect("/login")

##############################################
############## Journal Routes ################
##############################################

@app.route("/users/<username>/journals/new", methods=["GET", "POST"])
@login_required
def new_journal(username):
    """Show form for adding a new journal (GET) or add journal to db and go to user page (POST)"""
    # Check if logged in user is this user
    if is_correct_user(username):
        form = NewJournalForm()

        # Get park_code and name from db table for select field in form
        form.park_name.choices = [(p.park_code, p.park_name) for p in Park.query.order_by('park_name')]


        if form.validate_on_submit():
            date_added = datetime.now()
            date_of_visit = form.date_of_visit.data
            user_id = current_user.id
            title = form.title.data
            text = form.text.data
            park_code = form.park_name.data
            title_img_url = form.title_img_url.data

            journal = Journal(date_added=date_added,
                            date_of_visit=date_of_visit,
                            user_id=user_id,
                            title=title, 
                            text=text, 
                            park_code=park_code, 
                            title_img_url=title_img_url)
                            
            db.session.add(journal)
            db.session.commit()

            visit = Visit(date_of_visit=date_of_visit, user_id=user_id, park_code=park_code, journal_id=journal.id)
            db.session.add(visit)
            db.session.commit()

            flash("Journal successfully created")
            # on successful creation, redirect to users page
            return redirect(f"/users/{ username }")

        return render_template("new_journal.html", form=form)

    flash("Not your dashboard")
    return redirect("/")

@app.route("/users/<username>/journals/<park_code>/new", methods=["GET", "POST"])
@login_required
def new_journal_from_search(username, park_code):
    """Show form for adding a new journal with park already chosen (GET) or add journal to db and go to user page (POST)"""
    # Check if logged in user is this user
    if is_correct_user(username):
        form = NewJournalForm()

        # Get park_code and name from db table for select field in form
        park = Park.query.get_or_404(park_code)
        form.park_name.choices = [(park_code, park.park_name)]


        if form.validate_on_submit():
            date_added = datetime.now()
            date_of_visit = form.date_of_visit.data
            user_id = user_id
            title = form.title.data
            text = form.text.data
            park_code = form.park_name.data
            title_img_url = form.title_img_url.data

            journal = Journal(date_added=date_added,
                            date_of_visit=date_of_visit,
                            user_id=user_id,
                            title=title, 
                            text=text, 
                            park_code=park_code, 
                            title_img_url=title_img_url)
                            
            db.session.add(journal)
            db.session.commit()

            visit = Visit(date_of_visit=date_of_visit, user_id=user_id, park_code=park_code, journal_id=journal.id)
            db.session.add(visit)
            db.session.commit()

            flash("Journal successfully created")
            # on successful creation, redirect to users page
            return redirect(f"/users/{ user.username }")

        return render_template("new_journal.html", form=form)

    flash("Not your dashboard")
    return redirect("/")

@app.route("/users/<username>/journals/<int:journal_id>")
@login_required
def view_journal(username, journal_id):
    """Show user a single journal"""
    # Check if logged in user is this user
    if is_correct_user(username):
        journal = Journal.query.get_or_404(journal_id)

        adjusted_visit_date = journal.date_of_visit.strftime("%b %d, %Y")
        journal.date_of_visit = adjusted_visit_date

        adjusted_added_date = journal.date_added.strftime("%b %d, %Y")
        journal.date_added = adjusted_added_date

        return render_template("journal.html", journal=journal)

    flash("Not your journal")
    return redirect("/")

@app.route("/users/<username>/journals/<int:journal_id>/edit", methods=["GET", "POST"])
@login_required
def edit_journal(username, journal_id):
    """Show form for editing a journal (GET) or add journal edits to db and go to user page (POST)
    
    User cannot edit the park they visited"""
    
    # Check if logged in user is this user
    if is_correct_user(username):
        journal = Journal.query.get_or_404(journal_id)
        visit = Visit.query.get_or_404(journal_id)

        form = EditJournalForm(date_of_visit=journal.date_of_visit,
                            user_id=journal.user_id,
                            title=journal.title, 
                            text=journal.text, 
                            title_img_url=journal.title_img_url)

        if form.validate_on_submit():                
            journal.date_of_visit = form.date_of_visit.data
            visit.date_of_visit = form.date_of_visit.data
            journal.user_id = current_user.id
            journal.title = form.title.data
            journal.text = form.text.data
            journal.title_img_url = form.title_img_url.data
                            
            db.session.commit()

            flash("Journal updated")
            # on successful edit, redirect to users page
            return redirect(f"/users/{ username }")

        return render_template("edit_journal.html", journal=journal, form=form)

    flash("Not your journal")
    return redirect("/")

@app.route("/users/<username>/journals/<int:journal_id>/delete", methods=["POST"])
@login_required
def delete_journal(username, journal_id):
    """Delete a specific journal entry for a logged in user"""
    # Check if logged in user is this user
    if is_correct_user(username):
        user = User.query.get_or_404(current_user.id)
        journal = Journal.query.get_or_404(journal_id)

        db.session.delete(journal)
        db.session.commit()

        return redirect(f"/users/{ username }")

    flash("Not your journal to delete")
    return redirect("/")

################################################
########### Route for admin user ###############
################################################
@app.route("/users/admin")
@login_required
def admin_route():
    """Display interface for admin account to see all users and make changes"""
    if current_user.id == 1:
        users = User.query.all()
        
        return render_template('admin.html', users=users)

    flash("You do not have access to this route")
    return redirect("/")


################################################
########### Helper Functions ###################
################################################
def is_correct_user(username):
    """Logic for checking if logged in user is the same as the user page requested"""
    user = User.query.get_or_404(current_user.id)

    if user.username == username:
        return True
    else:
        return False

def send_confirmation(user):
    """Logic for sending a email to confirm a user"""

    token = generate_confirmation_token(user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email for GOutdoors"
    send_email(user.email, subject, html)

    flash('A confirmation email has been sent via email')

def new_confirmation_email():
    """Logic for a new confirmation email 

    Selected by a user"""

    user = User.query.get_or_404(current_user.id)

    token = generate_confirmation_token(user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email for GOutdoors"
    send_email(user.email, subject, html)

    flash('A new confirmation email has been sent.')



################################################
########### Route for app development ##########
################################################
# @app.route("/all")
# def get_parks():
#     """Use to get all parks and park codes
# 
#       Have to adjust start in URL by 50 after each call in order to step to the next set of 50"""

#     parks = requests.get(f"{ BASE_URL }/parks?limit=50&start=450&api_key={ api_key }")
#     parks_json = parks.json()
#     parks_data = parks_json["data"]

#     return render_template("all.html", parks=parks_data)