from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from OnlineAssessment import db
from werkzeug.security import generate_password_hash, check_password_hash
from OnlineAssessment.models import User
from OnlineAssessment.users.forms import RegistrationForm, LoginForm, UpdateUserForm


users = Blueprint('users', __name__)
# due to blueprint, all urlfor need to add prefix, such as "core"

# when user firstly registerer, register.html will be rendered, only when the form is submitted will be redirected


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    role=form.role.data)

        db.session.add(user)
        db.session.commit()
        flash('Registering successfully!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Get the user from User Models table
        user = User.query.filter_by(email=form.email.data).first()
        
        # The verify_password method comes from the User object
        if user is not None and user.check_password(form.password.data):
            # Log in the user
            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # if next === none or next Is Not equal to the home page, we'll go to the home page.
            if next == None or not next[0] == '/':
				#home page
                next = url_for('core.index')

            return redirect(next)
        # if the input email address or password is not correct
        flash('Invalid email address or password.')
    return render_template('login.html', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.index'))

# This page is for the user to change username and email
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('core.index'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('account.html', form=form)


