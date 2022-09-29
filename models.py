"""Models for Blogly."""

# Set Up
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    # define a table
    __tablename__ = "users"

    # define schema
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False,
                          default="https://semantic-ui.com/images/avatar2/small/rachel.png")

    # define methods
    @classmethod
    def get_all_users(cls):
        return cls.query.order_by(cls.last_name, cls.first_name).all()

    @property
    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def __repr__(self):
        return f"User{self.id} - {self.first_name} {self.last_name} with the profile image {self.image_url}"

    def greet(self):
        return f"Hi, My name is {self.get_full_name}! Nice to meet you!"
