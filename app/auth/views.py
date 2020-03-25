from . import auth
from .forms import RegistrationForm
from flask import render_template, request


@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        return render_template('in_construction.html', message="Debugging signup form!")
    return render_template('auth/signup.html', form=form)



