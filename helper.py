from models import User
from flask import request


def check_user_duplicate(new_user):
    all_users = User.get_all_users()
    for user in all_users:
        if new_user.get_full_name().upper() == user.get_full_name().upper() and user.id != new_user.id:
            raise ValueError("The user already exists!")


def create_user():
    [first_name, last_name, image_url] = get_inputs()
    if image_url:
        new_user = User(first_name=first_name,
                        last_name=last_name, image_url=image_url)
    else:
        new_user = User(first_name=first_name,
                        last_name=last_name)
    return new_user


def update_user(user):
    [first_name, last_name, image_url] = get_inputs()
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url
    return user


def get_inputs():
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]
    return [first_name, last_name, image_url]
