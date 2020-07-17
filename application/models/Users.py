from datetime import datetime, timedelta
from . import db
from application.models.Payments import Payment


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(60), unique=True, index=True)
    registered_on = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, unique=False, default=False)

    def __init__(self, username, password, email, is_admin=False):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.now()
        self.is_admin = is_admin

    def has_credit(self):
        # TODO changed number of days
        has_credit = False
        last_payment = Payment.query.filter_by(user_id=self.id).order_by(Payment.id.desc()).first()

        if last_payment is None:
            return has_credit
        if last_payment.payed_on + timedelta(days=30) >= datetime.now():
            has_credit = True

        return has_credit

    def get_last_paymets(self):
        # TODO changed limit
        last_payments = Payment.query.filter_by(user_id=self.id).order_by(Payment.id.desc()).limit(10).all()
        return last_payments

    def get_last_paymet(self):
        # TODO changed limit
        last_payments = Payment.query.filter_by(user_id=self.id).order_by(Payment.id.desc()).limit(1).first()
        return last_payments

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return f'User: {self.username}'

    # don't judge me...
    def unique(self):

        e_e = email_e = db.session.query(User.email).filter_by(email=self.email).scalar() is None
        u_e = username_e = db.session.query(User.username).filter_by(username=self.username).scalar() is None

        # none exist
        if e_e and u_e:
            return 0

        # email already exists
        elif e_e == False and u_e == True:
            return -1

        # username already exists
        elif e_e == True and u_e == False:
            return -2

        # both already exists
        else:
            return -3
