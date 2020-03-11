from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models.Users import User
from models.Users import db
import re
from config import configs
from logger import logger
from utilities import validate_file
from model_utilities import predict
import numpy as np
import cv2
import base64
import paypalrestsdk

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AfnAfJVtzh_PF6dtM9MWJSuHaXvLbP2QzYuQzE28GXpdFG1F9i2tIUG8MkHhahUkh-mPfYOT8_VjMQ-M",
  "client_secret": "EGrwwObDHKf9xyOiGyF_G-FfBKvGATJjDW7pC0iRAXuTQUmfEkYdYIh-7mRAyadcZDadCZNhEE_P4D8Q"})


# setup the app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "SuperSecretKey"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
bcrypt = Bcrypt(app)

# setup the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# create the db structure
with app.app_context():
    db.create_all()


####  setup routes  ####
@app.route('/')
@login_required
def index():
    a = 0
    a = a + 1
    return render_template('index.html', user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    # clear the inital flash message
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
    if registered_user is None and bcrypt.check_password_hash(registered_user.password, password) == False:
        flash('Invalid Username/Password')
        return render_template('login.html')

    # login the user
    login_user(registered_user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/register', methods=["GET", "POST"])
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

    # generate error messages if it doesnt pass
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
        return redirect(url_for('login'))

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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/charts')
def charts():
    return render_template('charts.html', user=current_user)


@app.route('/tables')
def tables():
    return render_template('tables.html', user=current_user)


@app.route('/forms')
def forms():
    return render_template('forms.html', user=current_user)


@app.route('/bootstrap-elements')
def bootstrap_elements():
    return render_template('bootstrap-elements.html', user=current_user)


@app.route('/bootstrap-grid')
def bootstrap_grid():
    return render_template('bootstrap-grid.html', user=current_user)


@app.route('/blank-page')
def blank_page():
    return render_template('blank-page.html', user=current_user)


@app.route('/profile')
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/settings')
def settings():
    return render_template('settings.html', user=current_user)

@app.route('/paypal')
def paypal():
    return render_template('paypal.html', user=current_user)

@app.route('/payment', methods=['POST'])
def payment():
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://0.0.0.0:5000/charts",
            "cancel_url": "http://0.0.0.0:5000/cancel-payment"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "testitem",
                    "sku": "12345",
                    "price": "50.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "50.00",
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print("Payment created successfully")
    else:
        print(payment.error)

    return jsonify({'paymentID': payment.id})


@app.route('/execute', methods=['POST'])
def execute():
    success = False
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id': request.form['payerID']}):
        print('execute success')
        success = True
    else:
        print(payment.error)
    return jsonify({'success': success})

@app.route('/cancel-payment', methods=['POST', 'GET', 'PUT'])
def cancel_payment():
    print('cancel payment called')
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.error:
        print(f'request has error: {payment.error}')
    else:
        print(f'payment {payment}')

####  end routes  ####


# required function for loading the right user
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


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
    symbol_error = re.search(r"[ !@#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None

    ret = {
        'Password is less than 8 characters': length_error,
        'Password does not contain a number': digit_error,
        'Password does not contain a uppercase character': uppercase_error,
        'Password does not contain a lowercase character': lowercase_error,
        'Password does not contain a special character': symbol_error,
    }

    return ret


@app.route('/api/predict', methods=["POST"])
@app.route('/predict', methods=["POST"])
def predict_image():

    data = request.data

    pos_coma = data.decode("utf-8").find(',')
    nparr = np.fromstring(base64.b64decode(data[pos_coma:]), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    response = predict(img)

    if request.path == '/api/predict':
        return jsonify(response)
    else:
        pass  # TODO render template


if __name__ == "__main__":
    app.run(host=configs['host'], port=configs['port'])
