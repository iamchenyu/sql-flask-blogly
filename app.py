"""Blogly application."""

from crypt import methods
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
from helper import check_duplicate_tag, check_user_duplicate, create_user, update_user, update_post, create_post, create_tag, update_tag
# from decouple import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# app.config['SECRET_KEY'] = config("SECRET_KEY")
app.config['SECRET_KEY'] = "temp_key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)


# Customize 404 Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Homepage - get 5 latest posts
@app.route("/")
def ge_homepage():
    posts = Post.list_all_posts().limit(5).all()
    return render_template("homepage.html", posts=posts)

##################################################################################
######################          Routes for Users            ######################
##################################################################################


@app.route("/users")
def all_users():
    users = User.get_all_users()
    return render_template("users/all_users.html", users=users)


@app.route("/users/<int:user_id>")
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.list_all_posts_by_user(user)
    return render_template("users/user.html", user=user, posts=posts)


@app.route("/users/new", methods=["GET", "POST"])
def new_user():
    if request.method == "GET":
        return render_template("users/new_user_form.html")
    else:
        new_user = create_user()
        try:
            check_user_duplicate(new_user)
            db.session.add(new_user)
            db.session.commit()
            flash(
                f"New user {new_user.full_name} has been created!", "ui success message")
            return redirect(f"/users/{new_user.id}")
        except ValueError:
            flash(f"User {new_user.full_name} already exists!",
                  "ui error message")
            return redirect("/users")


@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "GET":
        return render_template("users/edit_user_form.html", user=user)
    else:
        user = update_user(user)
        try:
            check_user_duplicate(user)
            db.session.add(user)
            db.session.commit()
            flash(f"User {user.full_name} has been edited!",
                  "ui success message")
        except ValueError:
            flash(f"User {user.full_name} already exists!", "ui error message")
        return redirect(f"/users/{user.id}")


@app.route("/users/<int:user_id>/delete", methods=["GET", "POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "GET":
        return render_template("users/delete_user.html", user=user)
    else:
        posts = user.posts
        # because the cascade setting, deleting a user will automatically delete all his/her posts
        # so we need to delete the post-tag relationship in the join table first
        for post in posts:
            PostTag.query.filter(PostTag.post_id == post.id).delete()
        db.session.delete(user)  # related posts will be deleted as well
        db.session.commit()
        flash(f"User {user.full_name} has been deleted!", "ui success message")
        return redirect("/users")


##################################################################################
######################          Routes for Posts            ######################
##################################################################################

@app.route("/users/<int:user_id>/posts/new", methods=["GET", "POST"])
def create_new_post(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    if request.method == "GET":
        return render_template("posts/new_post_form.html", user=user, tags=tags)
    else:
        new_post = create_post(user_id)
        db.session.add(new_post)
        db.session.commit()
        flash(f"Post - '{new_post.title}' has been created!",
              "ui success message")
        return redirect(f"/posts/{new_post.id}")


@app.route("/posts")
def get_all_posts():
    posts = Post.list_all_posts().all()
    return render_template("posts/all_posts.html", posts=posts)


@app.route("/posts/<int:post_id>")
def get_user_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("posts/post.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    if request.method == "GET":
        return render_template("posts/edit_post_form.html", post=post, tags=tags)
    else:
        post = update_post(post)
        db.session.add(post)
        db.session.commit()
        flash(f"Post - '{post.title}' has been edited!", "ui success message")
        return redirect(f"/posts/{post.id}")


@app.route("/posts/<int:post_id>/delete", methods=["GET", "POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "GET":
        return render_template("posts/delete_post.html", post=post)
    else:
        PostTag.query.filter(PostTag.post_id == post_id).delete()
        db.session.delete(post)
        db.session.commit()
        flash(f"Post - '{post.title}' has been deleted!", "ui success message")
        return redirect(f"/users/{post.user_id}")

##################################################################################
######################          Routes for Tags            ######################
##################################################################################


@app.route("/tags")
def list_all_tags():
    tags = Tag.query.all()
    return render_template("tags/tags.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def get_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template("tags/tag_details.html", tag=tag, posts=posts)


@app.route("/tags/new", methods=["GET", "POST"])
def create_new_tag():
    posts = Post.list_all_posts().all()
    if request.method == "GET":
        return render_template("tags/new_tag_form.html", posts=posts)
    else:
        tag = create_tag()
        try:
            check_duplicate_tag(tag)
            db.session.add(tag)
            db.session.commit()
            flash(f"Tag #{tag.name} has been created!", "ui success message")
            return redirect(f"/tags/{tag.id}")
        except ValueError:
            flash(f"Tag #{tag.name} already exists!", "ui error message")
            return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit", methods=["GET", "POST"])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    if request.method == "GET":
        return render_template("tags/edit_tag_form.html", tag=tag, posts=posts)
    else:
        tag = update_tag(tag)
        try:
            check_duplicate_tag(tag)
            db.session.add(tag)
            db.session.commit()
            flash(f"Tag #{tag.name} has been edited!", "ui success message")
        except ValueError:
            flash(f"Tag #{tag.name} already exists!", "ui error message")
        return redirect(f"/tags/{tag.id}")


@app.route("/tags/<int:tag_id>/delete", methods=["GET", "POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    if request.method == "GET":
        return render_template("tags/delete_tag.html", tag=tag)
    else:
        # need to remove the relationship in the join table first ---> Foreign Key Constraints
        PostTag.query.filter(PostTag.tag_id == tag_id).delete()
        Tag.query.filter(Tag.id == tag_id).delete()
        db.session.commit()
        return redirect("/tags")
