"""Seeding files for sample users"""

from models import db, User

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add Users
daniel = User(first_name="Daniel", last_name="Louise",
              image_url="https://semantic-ui.com/images/avatar/small/daniel.jpg")

stevie = User(first_name="Stevie", last_name="Feliciano",
              image_url="https://semantic-ui.com/images/avatar/small/stevie.jpg")

elliot = User(first_name="Elliot", last_name="Fu",
              image_url="https://semantic-ui.com/images/avatar/small/elliot.jpg")

helen = User(first_name="Helen", last_name="Chris",
             image_url="https://semantic-ui.com/images/avatar/small/helen.jpg")

# Add them to the db session
db.session.add(daniel)
db.session.add(stevie)
db.session.add(elliot)
db.session.add(helen)

# Commit them to the db
db.session.commit()
