from . import auth
from .forms import RegistrationForm
from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from app.models import User
from app import db


@auth.route("/login", methods=['GET', 'POST'])
def login():
    username = request.form.get("username")
    user = User.query.filter_by(username=username).first()
    if user is None:
        return render_template("error.html", message="Username Non-existent. Please register!")
    if user.verify_password(request.form.get("password")):
        login_user(user, request.form.get("rememberme"))
        return render_template("main/user.html", username=username)
    return render_template("auth/login.html")


@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations you can login now!")
        return redirect(url_for('main.index'))
    return render_template('auth/signup.html', form=form)



