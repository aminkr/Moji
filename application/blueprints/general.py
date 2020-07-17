from flask import Blueprint
from flask_bcrypt import Bcrypt
import cv2
import base64
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from application.model_utilities import predict
import sys
from application.models.Users import User
from datetime import timedelta
from application.config import PaypalConfig
sys.path.append("./")

gen_bp = Blueprint('gen_bp', __name__,
                   template_folder='../templates',
                   static_folder='../static')


@gen_bp.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)


@gen_bp.route('/edit-password')
@login_required
def edit_password():
    return render_template('edit-password.html', user=current_user)


@gen_bp.route('/balance', methods=["POST", "GET"])
@login_required
def show_user_balance():
    user = User.query.filter_by(username=current_user.username).first()
    payments = user.get_last_paymets()

    for i in range(len(payments)):
        payments[i].end_date = payments[i].payed_on.date() + timedelta(days=PaypalConfig.PAYMENT_EXPIRE_TIME)

    return render_template('balance.html', user=current_user, payments=payments)


@gen_bp.route('/tables')
def tables():
    return render_template('tables.html', user=current_user)


@gen_bp.route('/forms')
def forms():
    return render_template('forms.html', user=current_user)


@gen_bp.route('/bootstrap-elements')
def bootstrap_elements():
    return render_template('bootstrap-elements.html', user=current_user)


@gen_bp.route('/bootstrap-grid')
def bootstrap_grid():
    return render_template('bootstrap-grid.html', user=current_user)


@gen_bp.route('/blank-page')
def blank_page():
    return render_template('blank-page.html', user=current_user)


@gen_bp.route('/profile')
def profile():
    return render_template('profile.html', user=current_user)


@gen_bp.route('/settings')
def settings():
    return render_template('settings.html', user=current_user)


@gen_bp.route('/api/predict', methods=["POST"])
@gen_bp.route('/predict', methods=["POST"])
@login_required
def predict_image():
    # check input image size and type

    user = User.query.filter_by(username=current_user.username).first()
    if not user.has_credit():
        return jsonify({
            'error': 'You have not credit to prediction.'
        })

    data = request.data

    pos_coma = data.decode("utf-8").find(',')
    nparr = np.fromstring(base64.b64decode(data[pos_coma:]), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    response = predict(img)

    if request.path == '/api/predict':
        return jsonify(response)
    else:
        pass  # TODO render template
