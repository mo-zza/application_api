from flask import Flask
from flask import Blueprint
from flask_mail import Mail

from config import Config
from src.infrastructure.firebase import Firestore
from src.infrastructure.binance import Binance

binance_master_key = 'access key'
binance_master_secret = 'secret key'

firestore = Firestore()
binance = Binance(binance_master_key, binance_master_secret)

app = Flask(__name__)


def create_app(config_class=Config):
    app.config.from_object(Config)
    
    from src.controllers import users_bp, fund_bp, server_bp, email_bp, sell_bp, withdrawal_bp
    app.register_blueprint(users_bp)
    app.register_blueprint(fund_bp)
    app.register_blueprint(server_bp)
    app.register_blueprint(email_bp)
    app.register_blueprint(sell_bp)
    app.register_blueprint(withdrawal_bp)

    return app

def mail_server():

    app.config["MAIL_SERVER"] = 'smtp.gmail.com'
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = 'kamal.ha@alchemilab.com'
    app.config["MAIL_PASSWORD"] = 'h@je@w00&&*('
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True

    mail = Mail(app)

    return mail