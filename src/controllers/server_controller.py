from flask import request

from src.controllers import server_bp as bp
from src.application.services.server_service import get_server_time, get_health
from src.adapter.response import success_response
from src.domain.value.data import eventLoop


@bp.route('time', methods=['GET'])
def server_time():
    result = eventLoop.run_until_complete(get_server_time())
    return success_response(result, 200)

@bp.route('health', methods=['GET'])
def health_check():
    binance_url = '8.8.8.8'
    result = eventLoop.run_until_complete(get_health(binance_url))
    return success_response(result, 200)