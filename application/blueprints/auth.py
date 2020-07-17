from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from flask_bcrypt import Bcrypt
from flask import current_app as auth_app
from flask import jsonify
import re
import numpy as np

from application.models.Users import User
from application.models import db
from application.blueprints import login_manager

from application.logger import logger

auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='../templates',
                    static_folder='../static')
bcrypt = Bcrypt(auth_app)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('gen_bp.index'))

    session.clear()
    if request.method == 'GET':
        return render_template('login.html')

    # get the form data
    username = request.form['username']
    password = request.form['password']

    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True

    # query the user
    registered_user = User.query.filter_by(username=username).first()

    # check the passwords
    if registered_user is None or bcrypt.check_password_hash(registered_user.password, password) == False:
        flash('Invalid Username/Password')
        return render_template('login.html')

    # login the user
    login_status = login_user(registered_user, remember=remember_me)
    logger.info(
        f'login status is {login_status} and remember me {remember_me}')
    if login_status:
        session.permanent = True
        return redirect(request.args.get('next') or url_for('gen_bp.index'))


@auth_bp.route('/reset-password', methods=["POST"])
@login_required
def reset_password():
    response = ''
    current_pass = request.form['current_pass']
    new_pass = request.form['new_pass']
    confirm_pass = request.form['conf_pass']

    # check if it meets the right complexity
    check_password = password_check(new_pass)

    idx = np.where(np.array(list(check_password.values())) == True)

    msg_error = np.array(list(check_password.keys()))
    msg_error = msg_error[idx]

    if (len(msg_error) > 0):
        response = msg_error[0]

    # check previous pass is equal with previous pass
    registered_user = User.query.filter_by(
        username=current_user.username).first()
    if bcrypt.check_password_hash(registered_user.password, current_pass) == False:
        response = 'current password is not correct'
    print(response)
    if (response != ''):
        return render_template('edit-password.html', user=current_user, message=response, color='red')

    # do update password
    pw_hash = bcrypt.generate_password_hash(new_pass)

    registered_user.password = pw_hash
    db.session.commit()

    return render_template('edit-password.html', user=current_user, message='Password updated.', color='green')


@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        session.clear()
        return render_template('register.html')

    # get the data from our form
    password = request.form['password']
    conf_password = request.form['confirm-password']
    username = request.form['username']
    email = request.form['email']

    # make sure the password match
    if conf_password != password:
        flash("Passwords do not match")
        return render_template('register.html')

    # check if it meets the right complexity
    check_password = password_check(password)

    # generate error messages if it doesn't pass
    if True in check_password.values():
        for k, v in check_password.items():
            if str(v) is "True":
                flash(k)

        return render_template('register.html')

    # hash the password for storage
    pw_hash = bcrypt.generate_password_hash(password)

    # create a user, and check if its unique
    user = User(username, pw_hash, email)
    u_unique = user.unique()

    # add the user
    if u_unique == 0:
        db.session.add(user)
        db.session.commit()
        flash("Account Created")
        return redirect(url_for('auth_bp.login'))

    # else error check what the problem is
    elif u_unique == -1:
        flash("Email address already in use.")
        return render_template('register.html')

    elif u_unique == -2:
        flash("Username already in use.")
        return render_template('register.html')

    else:
        flash("Username and Email already in use.")
        return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('gen_bp.index'))


# required function for loading the right user
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))


# check password complexity
def password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
        credit to: ePi272314
        https://stackoverflow.com/questions/16709638/checking-the-strength-of-a-password-how-to-check-conditions
    """

    # calculating the length
    length_error = len(password) <= 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(
        r"[ !@#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None

    ret = {
        'Password is less than 8 characters': length_error,
        'Password does not contain a number': digit_error,
        'Password does not contain a uppercase character': uppercase_error,
        'Password does not contain a lowercase character': lowercase_error,
        'Password does not contain a special character': symbol_error,
    }

    return ret
