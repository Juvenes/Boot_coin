from . import db
from sqlalchemy.sql import func

class Wallet(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    isPrivate=db.Column(db.Boolean, default=False)
    mdp=db.Column(db.String(150))
    name=db.Column(db.String(150))
    descript=db.Column(db.String(300))
    money=db.Column(db.Float)
    startmoney=db.Column(db.Float)
    coin=db.Column(db.Float)
    coinname=db.Column(db.String(150))
    transactions = db.relationship('Transaction', cascade="all, delete")


class Transaction(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    walletid = db.Column(db.Integer, db.ForeignKey('wallet.id'))
    type = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    explications = db.relationship('Explication', cascade="all, delete")
    close =db.Column(db.Float)
    wallet =db.Column(db.Float)
    reanalyse = db.Column(db.String(150))



class Explication(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    transacid = db.Column(db.Integer, db.ForeignKey('transaction.id'))
    havepic = db.Column(db.Boolean)
    pic =db.Column(db.String(150))
    descript=db.Column(db.String(500))
    statement=db.Column(db.String(120))

    