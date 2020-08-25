from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired

class SearchForm(FlaskForm):
    """Form for searching national parks by state"""

    state = SelectField("State", choices=["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"])

class RegistrationForm(FlaskForm):
    """New user registration form"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """USer login form"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class JournalForm(FlaskForm):
    """New journal entry form"""

    title = StringField("Title", validators=[InputRequired()])
    text = StringField("Content", validators=[InputRequired()])
    park_code = StringField("Park Code", validators=[InputRequired()])
    state_code = StringField("State Code", validators=[InputRequired()])
    title_img_url = StringField("Title Image")
    img_1_url = StringField("Title Image")
    img_2_url = StringField("Title Image")
