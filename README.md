# GOutdoors

*Actively deployed*: https://goutdoors.herokuapp.com
*Link to NPS API*: https://www.nps.gov/subjects/developer/index.htm

## Introduction
GOutdoors started out of a desire to quickly search all of the US national parks and monuments by state to easily see what parks/monuments were near by and what activities they offered. Additionally, GOutdoors offers the ability to keep track of journal notes from a visit to a national park, which then allows you to quickly see what parks/monuments you have visited, when you visited them, and how many times the park has been visited by all users.

## GOutdoors Features
- Search individual states for national parks and monuments (do not need account)
- Create a journal entry for any national park/monument with 1 photo (hosted externally ex. imgur, Facebook, etc)
- Edit your account with the state you reside in for a quick search in your dashboard for parks near you
- After creating journals, future searches will show which parks you have visited with links directly to your journal entries

## Running GOutdoors
Running GOutdoors includes creating an NPS API key  (free with minimal user information), setting up an admin account for seeing registered users, and email authentication for user sign-ups.

- Install all requirements from requirements.txt
- Obtain NPS API key (free)
- Create secrets.py in app root directory. Include:
    - api_key = "*nps_api_key*"
    - admin_user = "*admin_username*"
    - admin_pass = "*admin_password*"
    - admin_email = "*admin_email_address*"
    - SECRET_KEY = "*secret_key*"
    - SECURITY_PASSWORD_SALT = "$%^F45F"
    - **mail settings**
        - MAIL_SERVER = "*email_server*"
        - MAIL_PORT = *port_#*
        - MAIL_USE_TLS = *True or False*
        - MAIL_USE_SSL = *True or False*
    - **gmail authentication**
        - MAIL_USERNAME = "*default_site_email*"
        - MAIL_PASSWORD = "*gmail_created_password*"
    - **mail accounts**
        - MAIL_DEFAULT_SENDER = "*default_site_email*"
- Flask Run (start server locally)

### Tech Stack:
- Flask
  - Flask-WTForm
  - Flask-Login
  - Flask-mail
  - SQLAlchemy
- Bcrypt
- Postgresql
- HTML
- CSS
  - Bootstrap