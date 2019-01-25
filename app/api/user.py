# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
import re
from flask import request, g, abort

from flask_security.utils import login_user, verify_password, hash_password
from flask_security import current_user
from flask_restful import reqparse
from .common import CommonResource, api_token_verify, \
api_arguments_sign_verify, parse_BizParam, api_abort, api_resp_code


class _UserResource(CommonResource):
    method_decorators = [api_token_verify]
    def __init__(self, **kwargs):
        super(_UserResource, self).__init__(**kwargs)
        self.model = self.models.Users

    def post(self, **kwargs):
        self.parser = reqparse.RequestParser()
        # self.parser.add_argument('email', type=str, location='json',required=True)
        # self.parser.add_argument('password', type=str, location='json', required=True)
        self.parser.add_argument("args", type=str, location='json', required=True)
        self.parser.add_argument("sign", type=str, location='json', required=True)
        args = self.parser.parse_args()
        api_arguments_sign_verify(args, kwargs["secret"])
        self.args = parse_BizParam(args.get("args"))
        emial = self.args.get("email")
        password = str(self.args.get("password"))
        if not emial or not password:
            api_abort(400, message="email and password are required")
        if len(password) < 6 or len(password) > 32:
            api_abort(400, message="password length is in range (6,32), {} given".format(len(password)))
        self.code = api_resp_code["faile"]
        self.http_code = 200
        self.message = None
        self.data = None

class ApiLogin(_UserResource):
    """
    game request to login
    """
    def post(self, **kwargs):
        """
        login post request\n
        :return: user ifo
        """
        super(ApiLogin, self).post(**kwargs)
        email = self.args.get("email")
        password = self.args.get("password")
        user = self.model.get_user_by_email(email)
        if not user:
            self.message = "username error or user is diabled"
        elif verify_password(password, user.password):
            self.data = {
               "userId": str(user.user_id)
            }
            self.code = api_resp_code["success"]
            login_user(user, remember=True)
        else:
            self.message = "password error"
        return self.utils.make_api_response(message=self.message, data=self.data, status=self.http_code, code=self.code)


class ApiRegister(_UserResource):

    def post(self, **kwargs):
        """
        register post request\n
        :return:
        """
        super(ApiRegister, self).post(**kwargs)
        email = self.args.get("email")
        password = self.args.get("password")
        exist_user = self.model.get_or_none(self.model.email == email)
        if exist_user:
            self.message = "email has been registed"
        else:
            try:
                user = self.model.create(
                    email=email,
                    password=hash_password(password)
                )
            except Exception:
                self.message = "register failed, retry after monment"
            else:
                self.data = {
                    "userId": str(user.user_id)
                }
                self.code = api_resp_code["success"]
                self.http_code = 201
        return self.utils.make_api_response(message=self.message, data=self.data, status=self.http_code, code=self.code)

class ApiReset(_UserResource):

    def post(self):
        """
        重置密码 暂时不做
        请求参数
        :return:
        """
        return self.utils.make_response()


