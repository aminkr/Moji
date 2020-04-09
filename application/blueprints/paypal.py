import paypalrestsdk
from flask import Blueprint
from application.config import PaypalConfig
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

paypalrestsdk.configure(PaypalConfig.SDK_CONFIG)

pay_bp = Blueprint('pay_bp', __name__,
                   template_folder='../templates',
                   static_folder='../static')


@pay_bp.route('/paypal')
def paypal():
    return render_template('paypal.html', user=current_user)


@pay_bp.route('/payment', methods=['POST'])
def payment():
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
        print("Payment created successfully")
    else:
        print(payment.error)

    return jsonify({'paymentID': payment.id})


@pay_bp.route('/execute', methods=['POST'])
def execute():
    success = False
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id': request.form['payerID']}):
        print('execute success')
        success = True
    else:
        print(payment.error)
    return jsonify({'success': success})


@pay_bp.route('/cancel-payment', methods=['POST', 'GET', 'PUT'])
def cancel_payment():
    print('cancel payment called')
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.error:
        print(f'request has error: {payment.error}')
    else:
        print(f'payment {payment}')
