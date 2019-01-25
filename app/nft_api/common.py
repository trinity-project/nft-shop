# -*- coding: utf-8 -*-

from hashlib import md5
import flask_restful
from functools import wraps
from werkzeug.exceptions import HTTPException
from flask import request
from app.types import api_resp_code
from flask_security import current_user
import json

def custom_api_error_response(status=200, message=None):
    data = {
        "code": api_resp_code["ts_untreated"] if status == 403 else api_resp_code["faile"],
        "http_status_code": status,
        "message": message,
        "api": request.path
    }
    return data

class CommonResource(flask_restful.Resource):
    def __init__(self, **kwargs):
        # smart_engine is a black box dependency
        self.models = kwargs['models']
        self.utils = kwargs['utils']


def api_abort(http_status_code, **kwargs):
    # print kwargs
    try:
        flask_restful.original_flask_abort(http_status_code)
    except HTTPException as e:
        if len(kwargs):
            e.data = kwargs
        if http_status_code in [400, 401, 403]:
            data = custom_api_error_response(
                status=http_status_code,
                message=kwargs.get("message")
            )
            e.data = data
        raise


####### api view func decorators begin #######
def api_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flask_restful.abort(401)
        return func(*args, **kwargs)

    return wrapper

def api_arguments_sign_verify(args, appsecret):
    """
    接口参数签名验证
    """
    arg_sign = args.get("sign").lower()
    del args["sign"]
    for key, value in args.items():
        if isinstance(args[key], list) and len(value) and isinstance(value[0], dict):
            sorted_list = []
            for el in value:
                inner_pairs = sorted(el.items(), key=lambda e: e[0].lower())
                sorted_dict = dict(pair for pair in inner_pairs)
                sorted_list.append(sorted_dict)
            args[key] = sorted_list
    pairs = sorted(args.items(), key=lambda e: e[0].lower())
    print(pairs)
    text = str()
    for key, value in pairs:
        text = text + "{}={}".format(key, value)
    print(text)
    text = "{0}{1}{0}".format(appsecret, text)
    text = text.encode("utf-8")
    sign = md5(text).hexdigest().lower()
    print(sign)
    if arg_sign != sign:
        api_abort(401, message="api arguments sign verify failed")


def parse_BizParam(param):
    """
    解析业务参数 可能是非标准json 字符串
    """
    if not isinstance(param, str):
        api_abort(400, message="param format error")
    param = param.replace("'", '"')
    try:
        return json.loads(param)
    except Exception:
        api_abort(400, message="param format error")


# overwriting flask_restful abort func
flask_restful.abort = api_abort
