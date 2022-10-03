from models import Tag, User, Post
from flask import request


def check_user_duplicate(new_user):
    all_users = User.get_all_users()
    for user in all_users:
        if new_user.full_name.upper() == user.full_name.upper() and user.id != new_user.id:
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
    tags_id = request.form.getlist("tag")
    tags = [Tag.query.get(id) for id in tags_id]
    return [title, content, tags]


def get_tag_input():
    name = request.form["tag-name"]
    posts_id = request.form.getlist("post")
    posts = [Post.query.get(id) for id in posts_id]
    return [name, posts]


def update_post(post):
    [title, content, tags] = get_post_inputs()
    post.title = title
    post.content = content
    post.tags = tags
    return post


def create_post(user_id):
    [title, content, tags] = get_post_inputs()
    new_post = Post(title=title, content=content, user_id=user_id, tags=tags)
    return new_post


def create_tag():
    [name, posts] = get_tag_input()
    new_tag = Tag(name=name, posts=posts)
    return new_tag


def update_tag(tag):
    [name, posts] = get_tag_input()
    tag.name = name
    tag.posts = posts
    return tag


def check_duplicate_tag(tag):
    if (Tag.query.filter(Tag.name == tag.name, Tag.id != tag.id).all()):
        raise ValueError("The tag already exists!")
