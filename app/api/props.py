# -*- coding: utf-8 -*-
__author__ = 'xu'

from datetime import timedelta, datetime
from .common import CommonResource, api_login_required, api_token_verify, \
api_arguments_sign_verify, parse_BizParam, api_abort, api_resp_code
from flask_restful import reqparse
from app import db, types
from decimal import Decimal
import json

class _PropsResource(CommonResource):
    def __init__(self, **kwargs):
        super(_PropsResource, self).__init__(**kwargs)
        self.model = self.models.Props

class _PropsForGameResource(_PropsResource):
    method_decorators = [api_token_verify]
    def __init__(self, **kwargs):
        super(_PropsForGameResource, self).__init__(**kwargs)
        self.parser = reqparse.RequestParser()
        # self.parser.add_argument('userId', type=str, location='json', required=True)
        self.parser.add_argument('sign', type=str, location='json', required=True)
        self.parser.add_argument('args', type=str, location='json', required=True)
        # self.parser.add_argument('items', type=dict, location='json', required=True, action='append')

class ApiProduceProps(_PropsForGameResource):
    
    """
    game ask store to produce new props\n
    url: /api/props/get/new
    """
    method_decorators = [api_token_verify]
    def post(self, **kwargs):
        """
        生成新的游戏道具
        :return:
        """
        self.code = api_resp_code["faile"]
        self.http_code = 200
        self.message = None
        self.data = None
        self.args = self.parser.parse_args()
        api_arguments_sign_verify(self.args, kwargs["secret"])
        self.args = parse_BizParam(self.args.get("args"))
        self.user = self.models.Users.get_user_by_user_id(self.args.get("userId"))
        if not self.user or self.user.user_id != kwargs["userid"]:
            self.message = "invalid user id"
        else:
            try:
                res_items = []
                with db.database.atomic():
                    for item in self.args.get("items"):
                        if float(item["price"]) <= 0 or float(item["amount"]) <=0:
                            api_abort(400, message="price or amount must greater than zero")
                        prop = self.model.create(
                            name = item["name"],
                            desc = json.dumps(item["desc"]) if isinstance(item["desc"], dict) else item["desc"],
                            price = item["price"],
                            amount = item["amount"],
                            item_id = item["itemId"],
                            owner = self.user.id
                        )
                        self.models.Commodity.create(
                            name = item["name"],
                            desc = prop.desc,
                            price = Decimal(item["price"]).quantize(Decimal("0.00000000")),
                            price_unit = kwargs["token"],
                            platform = types.platform["B2C"],
                            commodity_type = types.commodity_type["prop"],
                            prop = prop.id,
                            game = kwargs["gameid"],
                            seller = self.user.id
                        )
                        res_items.append(prop.item_id)
                        if len(res_items) == 10: break
                self.data = {
                    "items": res_items,
                    "userId": str(self.user.user_id)
                }
                self.code = 1
                self.http_code = 201
            except Exception as e:
                if hasattr(e, 'data') and isinstance(e.data, dict):
                    self.message = e.data.get("message")
                elif "UNIQUE constraint failed" in e.args[0]:
                    self.message = "item id has exist"
                else:
                    self.message = "create props failed"
        return self.utils.make_api_response(
            message=self.message,
            data=self.data,
            code=self.code,
            status=self.http_code
        )

class ApiGrantProps(_PropsForGameResource):
    pass