from datetime import datetime
from . import db


class Account(db.Model):
    __tablename__ = "user_balance"

    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), db.ForeignKey('users.user_id'), index=True, nullable=False)
    balance = db.Column('balance', db.Integer, nullable=False)
    change = db.Column('change', db.Integer, nullable=False)
    date = db.Column('date', db.DateTime, nullable=False)

    def __init__(self, username, balance, change):
        self.username = username
        self.balance = balance
        self.change = change
        self.date = datetime.utcnow()

    def get_id(self):
        return self.username

    def __repr__(self):
        return '<User %r>' % (self.username)
