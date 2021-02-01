import time
import os
from flask import abort
from flask import jsonify
from werkzeug.exceptions import BadRequest

from src.domain.value.exceptions import ServerError

async def get_server_time():
    server_time = time.time()
    return server_time

async def get_health(hostname):
    response = os.system("ping -c 2 -n " + hostname)

    if response == 0:
        return "health good"
    else:
        raise ServerError('Binance is Dead')