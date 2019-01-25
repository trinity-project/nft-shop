# -*- coding: utf-8 -*-
__author__ = 'xu'

from datetime import timedelta, datetime
from .common import CommonResource, api_login_required, api_token_verify,\
api_arguments_sign_verify, parse_BizParam, api_game_transaction_verify, create_or_update_gtx,\
api_resp_code, api_abort
from flask_restful import reqparse
from decimal import Decimal
from app import db
import json

class _CoinResource(CommonResource):
    def __init__(self, **kwargs):
        super(_CoinResource, self).__init__(**kwargs)
        self.model = self.models.ShopCoin

class _CoinForGameResource(_CoinResource):
    method_decorators = [api_token_verify]
    def __init__(self, **kwargs):
        super(_CoinForGameResource, self).__init__(**kwargs)
        self.parser = reqparse.RequestParser()
        # self.parser.add_argument('userId', type=str, location='json',required=True)
        # self.parser.add_argument('amount', type=str, location='json', required=True)
        # self.parser.add_argument('cate', type=str, location='json', required=True)
        self.parser.add_argument("args", type=str, location='json', required=True)
        self.parser.add_argument('sign', type=str, location='json',required=True)

    def create_or_update_coin(self, amount, rate, coin=None, **kwargs):
        if isinstance(amount, str): amount = Decimal(amount)
        if coin is None:
            self.model.create(
                cate=kwargs["cate"],
                owner=self.target_user.id,
                amount=amount,
                lock=amount,
                updated_at = datetime.now()
            )
        else:
            amount = amount * rate
            coin.lock = coin.lock - amount
            if self.__class__.__name__ == "ApiCoinExpend":
                coin.amount = coin.amount - amount
            coin.updated_at = datetime.now()
            coin.save()

    def find_user_coin(self, userid, cate):
        found_coin = None
        cate_coins = self.model.select().where(self.model.owner == userid)
        for cate_coin in cate_coins:
            if cate_coin.cate.name == cate:
                found_coin = cate_coin
                break
        return found_coin

    def post(self, **kwargs):
        self.code = api_resp_code["faile"]
        self.http_code = 200
        self.message = None
        self.data = None
        self.args = self.parser.parse_args()
        api_arguments_sign_verify(self.args, kwargs["secret"])
        self.args = parse_BizParam(self.args.get("args"))
        try:
            self.amount = Decimal(self.args.get("amount"))
        except Exception:
            api_abort(400, message="the amount in args body format error")
        else:
            if self.amount <= 0:
                api_abort(400, message="the amount in args body must greater than zero")
        result = api_game_transaction_verify(self.args.get("tsId"), kwargs["gameid"])
        if result:
            print("直接返回处理结果")
            result[0]["data"] = json.loads(result[1].result)
            return self.utils.make_api_response(**result[0])


class ApiCoinTransfer(_CoinForGameResource):

    """
    game transfer erc20 asset to store\n
    url: /api/erc20/transfer
    """
    def post(self, **kwargs):
        """
        :return:
        """
        resp = super(ApiCoinTransfer, self).post(**kwargs)
        if resp: return resp
        self.user = self.models.Users.get_user_by_user_id(self.args.get("userId"))
        if self.user:
            found_coin = self.find_user_coin(self.user.id, kwargs["token"])
            if not found_coin:
                self.message = "The user have no {} asset".format(kwargs["token"])
            elif found_coin.lock < self.amount:
                self.message = "The user at most transfer {} {}".format(found_coin.lock, kwargs["token"])
            else:
                try:
                    with db.database.atomic():
                        create_or_update_gtx(
                            self.args["tsId"],
                            kwargs["gameid"],
                            desc="CoinTransfer",
                            result=json.dumps({
                                "amount": self.args.get("amount"),
                                "userId": self.args.get("userId")
                            })
                        )
                        self.create_or_update_coin(self.amount, 1, found_coin)
                except Exception as e:
                    self.message = e.args[0] if hasattr(e, "args") else e.__str__()
                else:
                    self.code = api_resp_code["success"]
                    self.http_code = 201
                    self.data = {
                        "amount": self.args.get("amount"),
                        "userId": self.args.get("userId")
                    }
        else: 
            self.message = "invalid user id"
        return self.utils.make_api_response(
            message=self.message, 
            data=self.data,
            status=self.http_code, 
            code=self.code
        )

class ApiCoinExpend(_CoinForGameResource):
    
    def post(self, **kwargs):
        """
        :return:
        """
        resp = super(ApiCoinExpend, self).post(**kwargs)
        if resp: return resp        
        target_user_id = self.args.get("targetUserId")
        self.target_user = self.models.Users.get_user_by_user_id(target_user_id if target_user_id.isdigit() else 0)
        self.user = self.models.Users.get_user_by_user_id(self.args.get("userId"))
        if self.user:
            found_coin = self.find_user_coin(self.user.id, kwargs["token"])
            if not found_coin:
                self.message = "The user have no {} asset".format(kwargs["token"])
            elif found_coin.lock < self.amount:
                self.message = "The user at most spend {} {} in game".format(found_coin.lock, kwargs["token"])
            else:
                try:
                    with db.database.atomic(): 
                        create_or_update_gtx(
                            self.args["tsId"], 
                            kwargs["gameid"], 
                            desc="CoinExpend",
                            result=json.dumps({
                                "amount": self.args.get("amount"),
                                "userId": self.args.get("userId"),
                                "targetUserId": self.args.get("targetUserId")
                            })
                        )
                        self.create_or_update_coin(self.amount, 1, found_coin)
                        if self.target_user:
                            found_target_coin = self.find_user_coin(self.target_user.id, kwargs["token"])
                            self.create_or_update_coin(self.amount, -1, found_target_coin, cate=found_coin.cate.id)
                except Exception as e:
                    self.message = e.args[0] if hasattr(e, "args") else e.__str__()
                else:
                    self.code = api_resp_code["success"]
                    self.http_code = 201
                    self.data = {
                        "amount": self.args.get("amount"),
                        "userId": self.args.get("userId"),
                        "targetUserId": self.args.get("targetUserId")
                    }
        else: 
            self.message = "invalid user id"
        return self.utils.make_api_response(
            message=self.message, 
            data=self.data,
            status=self.http_code, 
            code=self.code
        )