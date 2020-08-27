from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField
from datetime import date
from wtforms.validators import InputRequired

class SearchForm(FlaskForm):
    """Form for searching national parks by state"""

    state = SelectField("State", choices=["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"])

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
    
    date = DateField("Date of Visit (Y-M-D)", default=date.today)
    title = StringField("Title", validators=[InputRequired()])
    text = StringField("Content", validators=[InputRequired()])
    title_img_url = StringField("Title Image URL")

