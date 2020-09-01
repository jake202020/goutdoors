from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField
from datetime import date
from wtforms.validators import InputRequired

class SearchForm(FlaskForm):
    """Form for searching national parks by state"""

    state = SelectField("State", choices=[('AL','AL'),('AK','AK'),('AZ','AZ'),('AR','AR'),('CA','CA'),('CO','CO'),('CT','CT'),('DE','DE'),('DC','DC'),('FL','FL'),('GA','GA'),('HI','HI'),('ID','ID'),('IL','IL'),('IN','IN'),('IA','IA'),('KS','KS'),('KY','KY'),('LA','LA'),('ME','ME'),('MD','MD'),('MA','MA'),('MI','MI'),('MN','MN'),('MS','MS'),('MO','MO'),('MT','MT'),('NE','NE'),('NV','NV'),('NH','NH'),('NJ','NJ'),('NM','NM'),('NY','NY'),('NC','NC'),('ND','ND'),('OH','OH'),('OK','OK'),('OR','OR'),('PA','PA'),('RI','RI'),('SC','SC'),('SD','SD'),('TN','TN'),('TX','TX'),('UT','UT'),('VT','VT'),('VA','VA'),('WA','WA'),('WV','WV'),('WI','WI'),('WY','WY')])

class RegistrationForm(FlaskForm):
    """New user registration form"""

    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("email", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """USer login form"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class NewJournalForm(FlaskForm):
    """New journal entry form"""
    
    date = DateField("Date of Visit (Y-M-D)", default=date.today)
    title = StringField("Title", validators=[InputRequired()])
    text = StringField("Content", validators=[InputRequired()])
    park_name = SelectField("Park Name", validators=[InputRequired()])
    title_img_url = StringField("Title Image URL")

class EditJournalForm(FlaskForm):
    """Edit journal entry form"""
    
    date = DateField("Date of Visit (Y-M-D)")
    title = StringField("Title", validators=[InputRequired()])
    text = StringField("Content", validators=[InputRequired()])
    title_img_url = StringField("Title Image URL")

