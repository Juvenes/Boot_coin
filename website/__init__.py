from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] ="dafhizebnvgferhjkjlhhkgfjhdtgsfqsdthfyjgu"
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    from .models import Wallet
    db.init_app(app)
    create_database(app)
    from .market import market
    from .wallet import wallet
    from .backtestmenu import backtest_menu
    app.register_blueprint(market,url_prefix='/')
    app.register_blueprint(wallet,url_prefix='/')
    app.register_blueprint(backtest_menu,url_prefix='/')
    return app


def create_database(app):
    if not path.exists('website/'+DB_NAME):
        db.create_all(app=app)