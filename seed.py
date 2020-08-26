from models import db, Park, Journal, User, Visit
from csv import DictReader
from app import app

# create tables
db.drop_all()
db.create_all()

with open('national_parks_codes.csv') as parks:
    db.session.bulk_insert_mappings(Park, DictReader(parks))

db.session.commit()