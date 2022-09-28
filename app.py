"""Blogly application."""

from crypt import methods
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from helper import check_user_duplicate, create_user, update_user
from decouple import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = config("SECRET_KEY")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()


@app.route("/users")
def all_users():
    users = User.get_all_users()
    return render_template("all_users.html", users=users)


@app.route("/users/<int:user_id>")
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user.html", user=user)


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
            flash("The user has been editted!", "ui success message")
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
