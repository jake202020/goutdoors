from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.widgets import TextArea
from datetime import date
from wtforms.validators import InputRequired, Email
import email_validator

STATES = [('AL','AL'),('AK','AK'),('AZ','AZ'),('AR','AR'),('CA','CA'),('CO','CO'),('CT','CT'),('DE','DE'),('DC','DC'),('FL','FL'),('GA','GA'),('GU', 'GU'),('HI','HI'),('ID','ID'),('IL','IL'),('IN','IN'),('IA','IA'),('KS','KS'),('KY','KY'),('LA','LA'),('ME','ME'),('MD','MD'),('MA','MA'),('MI','MI'),('MN','MN'),('MS','MS'),('MO','MO'),('MT','MT'),('NE','NE'),('NV','NV'),('NH','NH'),('NJ','NJ'),('NM','NM'),('NY','NY'),('NC','NC'),('ND','ND'),('OH','OH'),('OK','OK'),('OR','OR'),('PA','PA'),('RI','RI'),('SC','SC'),('SD','SD'),('TN','TN'),('TX','TX'),('UT','UT'),('VT','VT'),('VA','VA'),('WA','WA'),('WV','WV'),('WI','WI'),('WY','WY')]

class SearchForm(FlaskForm):
    """Form for searching national parks by state"""

    state = SelectField("State", choices=STATES)

class RegistrationForm(FlaskForm):
    """New user registration form"""

    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Email("Must enter valid email")])

class EditUserForm(FlaskForm):
    """Edit user registration form"""

    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    state_code = SelectField("State", choices=STATES)


class LoginForm(FlaskForm):
    """USer login form"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class NewJournalForm(FlaskForm):
    """New journal entry form"""
    
    date_of_visit = DateField("Date of Visit", default=date.today)
    title = StringField("Journal Title", validators=[InputRequired()])
    text = StringField("Journal Content", validators=[InputRequired()], widget=TextArea())
    park_name = SelectField("Park Name", validators=[InputRequired()])
    title_img_url = StringField("Title Image URL")

class EditJournalForm(FlaskForm):
    """Edit journal entry form"""
    
    date = DateField("Date of Visit")
    title = StringField("Title", validators=[InputRequired()])
    text = StringField("Content", validators=[InputRequired()], widget=TextArea())
    title_img_url = StringField("Title Image URL")

