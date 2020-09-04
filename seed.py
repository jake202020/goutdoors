from models import db, Park, Journal, User, Visit
from csv import DictReader
from app import app
from secrets import admin_user, admin_pass, admin_email
from datetime import datetime


# create tables
db.drop_all()
db.create_all()

with open('national_parks_codes.csv') as parks:
    db.session.bulk_insert_mappings(Park, DictReader(parks))

#Create admin user
username = admin_user
password = admin_pass
email=admin_email
first_name="admin"
last_name="user"
confirmed=True,
role="admin"

admin = User.register(username, password, email, first_name, last_name, confirmed, role)

db.session.add(admin)
db.session.commit()