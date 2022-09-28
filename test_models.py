from unittest import TestCase

from models import User, db
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test Cases for User Model"""

    def setUp(self):
        """clean up any existing users"""
        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transactions"""
        db.session.rollback()

    def test_get_all_users(self):
        daniel = User(first_name="Daniel", last_name="Louise",
                      image_url="https://semantic-ui.com/images/avatar/small/daniel.jpg")

        stevie = User(first_name="Stevie", last_name="Feliciano",
                      image_url="https://semantic-ui.com/images/avatar/small/stevie.jpg")

        db.session.add(daniel)
        db.session.add(stevie)
        db.session.commit()

        self.assertEquals(User.get_all_users(), [daniel, stevie])

    def test_get_full_name(self):
        daniel = User(first_name="Daniel", last_name="Louise",
                      image_url="https://semantic-ui.com/images/avatar/small/daniel.jpg")
        self.assertEquals(daniel.get_full_name(), "Daniel Louise")

    def test_greet(self):
        daniel = User(first_name="Daniel", last_name="Louise",
                      image_url="https://semantic-ui.com/images/avatar/small/daniel.jpg")
        self.assertEquals(
            daniel.greet(), "Hi, My name is Daniel Louise! Nice to meet you!")
