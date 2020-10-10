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