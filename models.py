"""Models for Blogly."""

# Set Up
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


# As a convenience, if we run this module interactively, the method below will leave you in a state of being able to work with the database directly.
# So that we can use Flask-SQLAlchemy, we'll make a Flask app
if __name__ == "__main__":
    from app import app
    connect_db(app)


DEFAULT_USER_IMAGE = "https://semantic-ui.com/images/avatar2/small/rachel.png"


class User(db.Model):
    """Define User Model"""

    # define a table
    __tablename__ = "users"

    # define schema
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False,
                          default=DEFAULT_USER_IMAGE)

    # define methods
    @classmethod
    def get_all_users(cls):
        return cls.query.order_by(cls.last_name, cls.first_name).all()

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def __repr__(self):
        return f"User{self.id} - {self.full_name}"

    def greet(self):
        return f"Hi, My name is {self.full_name}! Nice to meet you!"


class Post(db.Model):
    """Define Post Model"""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # define the relationship with users table
    user = db.relationship("User", backref=db.backref(
        "posts", cascade="all, delete-orphan"))
    # define relationship with the join table (posts_tags)
    details = db.relationship("PostTag", backref="post")
    # define a "through" relationship
    tags = db.relationship("Tag", secondary="posts_tags", backref="posts")

    @classmethod
    def list_all_posts(cls):
        return cls.query.order_by(cls.created_at.desc())

    @classmethod
    def list_all_posts_by_user(cls, user):
        return cls.query.filter(cls.user == user).order_by(cls.created_at.desc()).all()

    @property
    def formatted_datetime(self):
        return self.created_at.strftime("%b %d %Y %H:%M:%S")

    def __repr__(self):
        return f"Post {self.id} Title - '{self.title}' by User - '{self.user}' "


class Tag(db.Model):
    """Define Tag Model"""
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    # define relationship with join table (posts_tags)
    details = db.relationship("PostTag", backref="tag")

    def __repr__(self):
        return f"Tag {self.id} - {self.name}"


class PostTag(db.Model):
    """Define Join Table for TAGS and POSTS"""
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey(
        "posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)

    def __repr__(self):
        return f"Post - {self.post.title} & Tag - {self.tag.name}"
