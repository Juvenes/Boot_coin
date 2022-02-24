from flask import Flask
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] ="dafhizebnvgferhjkjlhhkgfjhdtgsfqsdthfyjgu"
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    from .market import market
    app.register_blueprint(market,url_prefix='/')
    return app
