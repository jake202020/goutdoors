"""SQLAlchemy models for GOutdoors"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
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

    state = db.Column(db.String(2))

    # registration method
    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user with hashed password and return user"""

        hashed = bcrypt.generate_password_hash(pwd)
        # Turn bytestring into unicode utf8 string
        hashed_utf8 = hashed.decode("utf8")

        # Return instance of user with details and hased pwd
        return cls(username=username,
                    password=hashed_utf8,
                    email=email,
                    first_name=first_name,
                    last_name=last_name)

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

def connect_db(app):
    """Connect this database to provided Flask app.

    Called app.py
    """

    db.app = app
    db.init_app(app)