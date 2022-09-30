"""Blogly application."""

from crypt import methods
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from helper import check_user_duplicate, create_user, update_user, update_post, create_post
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

# Routes for Users
@app.route("/users")
def all_users():
    users = User.get_all_users()
    return render_template("all_users.html", users=users)


@app.route("/users/<int:user_id>")
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.list_all_posts_by_user(user)
    return render_template("user.html", user=user, posts=posts)


@app.route("/users/new", methods=["GET", "POST"])
def new_user():
    if request.method == "GET":
        return render_template("new_user_form.html")
    else:
        new_user = create_user()
        try:
            check_user_duplicate(new_user)
            db.session.add(new_user)
            db.session.commit()
            flash("The user has been created!", "ui success message")
            return redirect(f"/users/{new_user.id}")
        except ValueError:
            flash("The user already exists!", "ui error message")
            return redirect("/users")


@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "GET":
        return render_template("edit_user_form.html", user=user)
    else:
        user = update_user(user)
        try:
            check_user_duplicate(user)
            db.session.add(user)
            db.session.commit()
            flash("The user has been edited!", "ui success message")
            return redirect(f"/users/{user.id}")
        except ValueError:
            flash("The user already exists!", "ui error message")
            return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["GET", "POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "GET":
        return render_template("delete_user.html", user=user)
    else:
        db.session.delete(user)
        db.session.commit()
        flash("The user has been deleted!", "ui success message")
        return redirect("/users")


@app.route("/users/<int:user_id>/posts/new", methods=["GET", "POST"])
def create_new_post(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "GET":
        return render_template("new_post_form.html", user=user)
    else:
        new_post = create_post(user_id)
        db.session.add(new_post)
        db.session.commit()
        flash("The post has been created!", "ui success message")
        return redirect(f"/posts/{new_post.id}")

# Routes for Posts
@app.route("/")
def ge_homepage():
    posts = Post.list_all_posts().limit(5).all()
    return render_template("homepage.html", posts=posts)


@app.route("/posts")
def get_all_posts():
    posts = Post.list_all_posts().all()
    return render_template("all_posts.html", posts=posts)


@app.route("/posts/<int:post_id>")
def get_user_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "GET":
        return render_template("edit_post_form.html", post=post)
    else:
        post = update_post(post)
        db.session.add(post)
        db.session.commit()
        flash("The post has been edited!", "ui success message")
        return redirect(f"/posts/{post.id}")


@app.route("/posts/<int:post_id>/delete", methods=["GET", "POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "GET":
        return render_template("delete_post.html", post=post)
    else:
        db.session.delete(post)
        db.session.commit()
        flash("The post has been deleted!", "ui success message")
        return redirect(f"/users/{post.user_id}")
