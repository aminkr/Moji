from datetime import datetime
from . import db


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    amount = db.Column(db.Float, nullable=False)
    payed_on = db.Column(db.DateTime)
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'),
                         nullable=False)
    user = db.relationship('User', foreign_keys=user_id)

    def __init__(self, amount, user):
        self.amount = amount
        self.user = user
        self.payed_on = datetime.now()

    def __repr__(self):
        return f'id: {self.id}, amount: {self.user_id}, amount: {self.amount}, payed_on: {self.payed_on}'
