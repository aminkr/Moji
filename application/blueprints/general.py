from flask import Blueprint
from flask_bcrypt import Bcrypt
import cv2
import base64
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from application.model_utilities import predict
import sys
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


@gen_bp.route('/reset-password', methods=["POST"])
@login_required
def reset_password():
    current_pass = request.form['current_pass']
    new_pass = request.form['new_pass']
    confirm_pass = request.form['conf_pass']
    
    # do update password
    # ...
    # ...
    #

    return render_template('index.html', user=current_user)


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
