from models import User, Post
from flask import request


def check_user_duplicate(new_user):
    all_users = User.get_all_users()
    for user in all_users:
        if new_user.get_full_name.upper() == user.get_full_name.upper() and user.id != new_user.id:
            raise ValueError("The user already exists!")


def create_user():
    [first_name, last_name, image_url] = get_user_inputs()
    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url or None)
    return new_user


def update_user(user):
    [first_name, last_name, image_url] = get_user_inputs()
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url
    return user


def get_user_inputs():
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]
    return [first_name, last_name, image_url]


def get_post_inputs():
    title = request.form["title"]
    content = request.form["content"]
    return [title, content]


def update_post(post):
    [title, content] = get_post_inputs()
    post.title = title
    post.content = content
    return post


def create_post(user_id):
    [title, content] = get_post_inputs()
    new_post = Post(title=title, content=content, user_id=user_id)
    return new_post
