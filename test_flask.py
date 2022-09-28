from unittest import TestCase

from models import db, User
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class FlaskAppTestCase(TestCase):
    """Test Cases for Flask Application"""

    def setUp(self):
        User.query.delete()
        daniel = User(first_name="Daniel", last_name="Louise",
                      image_url="https://semantic-ui.com/images/avatar/small/daniel.jpg")
        db.session.add(daniel)
        db.session.commit()
        self.id = daniel.id

    def tearDown(self):
        db.session.rollback()

    def test_all_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Daniel Louise", html)

    def test_get_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Daniel Louise", html)
