from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

class ResponseAdepter:
    data: any
    status_code: int

    def __init__(self, data, status_code: int):
        if isinstance(data , bool) == True:
            raise TypeError('No list or boolean')
        else:
            self.data = data
            self.status_code = status_code

    def success_response(self):
        payload = {'message': HTTP_STATUS_CODES.get(self.status_code),
            'data': self.data}
        response = jsonify(payload)
        response.status_code = self.status_code
        return response

def success_response(data, status_code: int):
    try:
        response = ResponseAdepter(data, status_code).success_response()
        return response

    except TypeError:
        response = 'response error', 500
        return  response