"""Models for Blogly."""

# Set Up
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

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


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", backref=db.backref("posts", cascade="all, delete-orphan")
                           )

    @classmethod
    def list_all_posts(cls):
        return cls.query.order_by(cls.created_at.desc())

    @classmethod
    def list_all_posts_by_user(cls, user):
        return cls.query.filter(cls.user == user).all()

    def __repr__(self):
        return f"Post {self.id} Title - '{self.title}' Content - '{self.content}' Created_at - '{self.created_at}' by User - '{self.user}' "
