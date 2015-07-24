__author__ = 'vikram'

import decimal
import datetime
import json


class ApiResponse:
    def __init__(self, response=None):
        self.response = response if response is not None else {}
        self.api_version = 2.0
        self.code = 200
        self.message = {}

    def get_code(self):
        return self.code

    def set_code(self, code):
        self.code = code

    def set_error_response(self, msg=""):
        self.message = msg
        self.set_code(500)


def alchemyencoder(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


def make_response(results):
    data = {
        'message': results.message,
        'response': results.response
    }
    return json.dumps(data, default=alchemyencoder), results.get_code()


def api_response(data):
    return make_response((ApiResponse(data)))


def error_response(msg):
    resp = ApiResponse
    resp.set_error_response(msg)
    return make_response(resp)
