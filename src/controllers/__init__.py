from src.adapter.error_handler import *

from flask import Blueprint
users_bp = Blueprint('users', __name__, url_prefix='/api/users')
fund_bp = Blueprint('fund', __name__, url_prefix='/api/fund')
server_bp = Blueprint('server', __name__, url_prefix='/api/server')
email_bp = Blueprint('email', __name__, url_prefix='/api/email')
sell_bp = Blueprint('sell', __name__, url_prefix='/api/sell')
withdrawal_bp = Blueprint('withdrawal', __name__, url_prefix='/api/withdrawal')

from src.controllers import users_controller, fund_controller, server_controller, email_controller, sell_controler, withdrawal_controller