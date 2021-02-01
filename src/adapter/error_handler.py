from flask import jsonify
import json
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import BadRequestKeyError

from src import app
from src.domain.value.exceptions import *

@app.errorhandler(CustomNotFound)
@app.errorhandler(UnAuthenticationError)
@app.errorhandler(ServerError)
@app.errorhandler(VerifyTokenError)
@app.errorhandler(UnFinishOrder)
@app.errorhandler(ZeroBalance)
@app.errorhandler(LockedUser)
@app.errorhandler(VerifyPassword)
@app.errorhandler(ZeroFundAsset)
@app.errorhandler(ZeroFunding)
@app.errorhandler(ZeroRecord)
@app.errorhandler(ReqMethodsError)
@app.errorhandler(VerifyOTP)
@app.errorhandler(NotFound)
@app.errorhandler(InsuffiientError)
@app.errorhandler(ZeroAsset)
@app.errorhandler(BadRequestKeyError)
@app.errorhandler(NonAvailableAccount)
@app.errorhandler(BinanceError)
def handle_exception(e):
    response = {
        "message": HTTP_STATUS_CODES.get(e.code),
        "description": e.description,
    }
    return response, e.code

@app.errorhandler(ZeroDBCustom)
def zero_db(e):
    response = { 
        "data" : e.description,
        "message" : HTTP_STATUS_CODES.get(e.code)
        }
    return response, e.code