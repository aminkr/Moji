import paypalrestsdk
from flask import Blueprint
from application.config import PaypalConfig
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from application.models.Payments import Payment
from application.models.Users import User
from application.models import db
from datetime import datetime, timedelta

from application.logger import logger
# from

paypalrestsdk.configure(PaypalConfig.SDK_CONFIG)

pay_bp = Blueprint('pay_bp', __name__,
                   template_folder='../templates',
                   static_folder='../static')


@pay_bp.route('/paypal')
@login_required
def paypal():


    user = User.query.filter_by(username=current_user.username).first()
    pay = Payment(PaypalConfig.PAYMENT_PRICE, user)
    db.session.add(pay)
    db.session.commit()
    return render_template('paypal.html', user=current_user)


@pay_bp.route('/payment', methods=['POST'])
@login_required
def payment():

    user = User.query.filter_by(username=current_user.username).first()
    have_credit = False
    if user.has_credit():
        last_payment = user.get_last_paymet()
        credit_date = last_payment.payed_on.date() + timedelta(days=PaypalConfig.PAYMENT_EXPIRE_TIME)
        message = 'your account have credit until {} date.'.format(credit_date)
        have_credit = True

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": PaypalConfig.PAYMENT_RETURN_URI,
            "cancel_url": PaypalConfig.PAYMENT_CANCEL_URI},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "sale",
                    "sku": "12345",
                    "price": PaypalConfig.PAYMENT_PRICE,
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": PaypalConfig.PAYMENT_PRICE,
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        logger.debug("Payment has been done successfully")
    else:
        logger.debug(f"Payment has error: {payment.error}")

    return jsonify({'paymentID': payment.id, 'have_credit': have_credit})


@pay_bp.route('/execute', methods=['POST'])
@login_required
def execute():
    success = False
    message = ''
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])
    user = User.query.filter_by(username=current_user.username).first()

    data = {}
    if payment.execute({'payer_id': request.form['payerID']}):
        pay = Payment(PaypalConfig.PAYMENT_PRICE, user)
        db.session.add(pay)
        db.session.commit()
        success = True
        data['user_name'] = current_user.username
        data['date'] = pay.payed_on.strftime('%Y-%m-%d')
        data['time'] = pay.payed_on.strftime('%H:%M:%S')
        data['expire_date'] = (pay.payed_on + timedelta(days=PaypalConfig.PAYMENT_EXPIRE_TIME)).strftime('%Y-%m-%d')
        data['amount'] = str(pay.amount)
        message = 'Payment executed successfully'
    else:
        logger.debug(f"Payment has error: {payment.error}")
    return jsonify({'success': success, 'message': message, 'data': data})


@pay_bp.route('/cancel-payment', methods=['POST', 'GET', 'PUT'])
@login_required
def cancel_payment():
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.error:
        logger.debug(f'request has error: {payment.error}')
    else:
        logger.debug(f'payment is ok: {payment}')
