"""Tests for initial GOutdoors testing"""

# run by: python -m unittest tests.py

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User

# Before importing the app, set environmental variable
# to use a different database for tests

os.environ['DATABASE_URL'] = "postgresql:///capstone-test"

from app import app

# create the tables in the test database

db.create_all()

class UserModelTestCase(TestCase):
    """Test model for a user"""
    
    def setUp(self):
        """Create test client with sample data"""
        db.drop_all()
        db.create_all()

        u1 = User.register("test", "password", "email@email.com", "test", "case")

        db.session.add(u1)
        db.session.commit()

        u1 = User.query.get("test")

        self.u1 = u1
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_user_model(self):
        """Does the basic user model work?"""
        
        u = User(
            username="test1",
            password="password",
            email="test@email.com",
            first_name="test",
            last_name="user"
        )

        db.session.add(u)
        db.session.commit()

        # user state code should be blank
        self.assertIsNone(u.state_code)

    def test_valid_signup(self):
        """Does the register method work?"""
        u = User.register("test1","password","test@email.com","test","user")

        db.session.add(u)
        db.session.commit()

        u = User.query.get("test1")

        self.assertIsNotNone(u)
        self.assertEqual(u.username, "test1")
        self.assertEqual(u.email, "test@email.com")
        self.assertEqual(u.first_name, "test")
        self.assertEqual(u.last_name, "user")
        self.assertNotEqual(u.password, "password")
        # Bcrypt password should start with $2b$
        self.assertTrue(u.password.startswith("$2b$"))

    ######################
    # Journal Tests
    ######################
    def test_journal_model(self):
        """Does the basic journal model work?"""

    def test_journal_view(self):
        """Does the html show up for a journal"""

    ######################
    # Authentication Tests
    #####################

    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.username, self.u1.username)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))

# class UserViewTestCase(TestCase):
#     """Test views for users"""

# class JournalModelTestCase(TestCase):
#     """Test model for a journal"""

# class JournalViewTestCase(TestCase):
#     """Test view for a journal"""

# class ParkViewTestCase(TestCase):
#     """Test view for Park search results"""
