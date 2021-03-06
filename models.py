"""SQLAlchemy models for GOutdoors"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User Model"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    username = db.Column(db.String(30),
                        nullable=False,
                        unique=True)
    
    password = db.Column(db.Text,
                        nullable=False)

    email = db.Column(db.String(60),
                    nullable=False)
    
    first_name = db.Column(db.String(30),
                            nullable=False)
    
    last_name = db.Column(db.String(30),
                            nullable=False)

    confirmed = db.Column(db.Boolean, nullable=False, default=False)

    confirmed_on = db.Column(db.DateTime, nullable=True)

    role = db.Column(db.Text,
                        nullable=False)

    state_code = db.Column(db.String(2))

    created_at = db.Column(db.DateTime)

    journal = db.relationship("Journal", backref="user", cascade="all,delete")

    visit = db.relationship("Visit", backref="user", cascade="all,delete")

    # registration method
    @classmethod
    def register(cls, username, pwd, email, first_name, last_name, confirmed, role, created_at):
        """Register user with hashed password and return user"""

        hashed = bcrypt.generate_password_hash(pwd)
        # Turn bytestring into unicode utf8 string
        hashed_utf8 = hashed.decode("utf8")

        # Return instance of user with details and hashed pwd
        return cls(username=username,
                    password=hashed_utf8,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    confirmed=confirmed,
                    role=role,
                    created_at=created_at)

    # authentication method
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate user exists and password is correct.

        Return user if valid, else return False"""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False

class Park(db.Model):
    """Park Model"""

    __tablename__ = "parks"

    park_code = db.Column(db.String(4),
                            primary_key=True,
                            nullable=False)

    park_name = db.Column(db.String,
                    nullable=False)

    state_code = db.Column(db.String(2),
                            nullable=False)

    visit_count = db.Column(db.Integer)

    journal = db.relationship("Journal", backref="park", cascade="all,delete")

    visit = db.relationship("Visit", backref="park", cascade="all,delete")


class Journal(db.Model):
    """Journal model"""

    __tablename__ = "journals"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    date_added = db.Column(db.DateTime,
                            nullable=False)

    date_of_visit = db.Column(db.DateTime,
                        nullable=False,
                        unique=False)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    
    title = db.Column(db.Text,
                        nullable=False)

    text = db.Column(db.Text,
                    nullable=False)
    
    park_code = db.Column(db.String(4),
                            db.ForeignKey('parks.park_code'),
                            nullable=False)
    
    title_img_url = db.Column(db.String)

    visit = db.relationship("Visit", backref="journal", cascade="all,delete")

class Visit(db.Model):
    """Park Visit Model"""

    __tablename__ = "visits"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    date_of_visit = db.Column(db.DateTime,
                        nullable=False)

    user_id = db.Column(db.ForeignKey('users.id'),
                        nullable=False)

    park_code = db.Column(db.String(4),
                            db.ForeignKey('parks.park_code'),
                            nullable=False)

    journal_id = db.Column(db.Integer,
                            db.ForeignKey('journals.id'),
                            nullable=True)

def connect_db(app):
    """Connect this database to provided Flask app.

    Called app.py
    """

    db.app = app
    db.init_app(app)