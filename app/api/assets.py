# -*- coding: utf-8 -*-
__author__ = 'xu'

from datetime import timedelta, datetime
from flask_restful import reqparse, current_app
from .common import CommonResource, api_login_required, api_token_verify, \
api_arguments_sign_verify, parse_BizParam, api_resp_code, api_game_transaction_verify,\
create_or_update_gtx
from .utils import request_create_new_nft_onchain, set_nft_attr_onchain, \
get_nft_by_id
# from app.asynctasks import background_task
from app.types import visible_status, commodity_status
from app.signals import mintage_created
from app.asynctasks import notify_mintage_complete_task, mintage_task
from app import db
from decimal import Decimal
import json

class _AssetsResource(CommonResource):
    def __init__(self, **kwargs):
        super(_AssetsResource, self).__init__(**kwargs)
        self.model = self.models.Assets
        

class ApiAllowGames(_AssetsResource):
    method_decorators = [api_login_required]
    def get(self, asset_id):
        """
        获取对应asset_id可分配的游戏列表
        :return:
        """
        games = self.model.get_allow_games(asset_id)
        message = {
            "result": "success",
            "games": games
        }
        return self.utils.make_api_response(message=message)

class _NftForGameResource(_AssetsResource):
    method_decorators = [api_token_verify]
    def __init__(self, **kwargs):
        super(_NftForGameResource, self).__init__(**kwargs)
        self.parser = reqparse.RequestParser()
        # self.parser.add_argument('userId', type=str, location='json',required=True)
        # self.parser.add_argument('id', type=str, location='json', required=True, action='append')
        # self.parser.add_argument("desc", type=str, location='json', required=True)
        self.parser.add_argument("args", type=str, location='json', required=True)
        self.parser.add_argument("sign", type=str, location='json', required=True)

    def post(self, **kwargs):
        self.args = self.parser.parse_args()
        api_arguments_sign_verify(self.args, kwargs["secret"])
        self.args = parse_BizParam(self.args.get("args"))
        user = self.models.Users.get_user_by_user_id(self.args.get("userId"))
        self.code = api_resp_code["faile"]
        self.http_code = 200
        self.message = None
        self.data = None
        result = api_game_transaction_verify(self.args.get("tsId"), kwargs["gameid"])
        # todo 其他业务参数校验
        if result:
            print("直接返回处理结果")
            result[0]["data"] = json.loads(result[1].result)
            return self.utils.make_api_response(**result[0])

    def find_user_asset(self):
        found_asset = None
        for asset in self.user.assets:
            if asset.asset_id == self.args.get("id")[0]:
                found_asset = asset
                break            
        return found_asset
        
    
class ApiNftGetNew(_NftForGameResource):
    """
    game request to produce a new nft asset
    """
    # def get(self, **kwargs):
    # def get(self, **kwargs):
    #     args = {"id": "e7fbda05223c57d3a3eddb64"}
    #     result = get_nft_by_id(args)
    #     # result = background_task.delay(10, 20)
    #     # print(result)
    #     return result

    # def put(self, **kwargs):
    #     args = self.parser.parse_args()
    #     api_arguments_sign_verify(args, kwargs["secret"])
    #     user = self.models.Users.get_user_by_user_id(args.get("userId"))
    #     if not user or not user.eth_address:
    #         message = "invalid user id or no wallet address"
    #         code = 0
    #         http_code = 200
    #     else:
    #         args["address"] = user.eth_address
    #         args["key"] = user.eth_key
    #         result = set_nft_attr_onchain(args)
    #         if isinstance(result, dict):
    #             message = {
    #                 "id": args.get("id"),
    #                 "userId": args.get("userId")
    #             }
    #             code = 1
    #             http_code = 201
    #         else:
    #             message = result
    #             http_code = 200
    #             code = -1
    #     return self.utils.make_api_response(message=message, status=http_code, code=code)

    def post(self, **kwargs):
        resp = super(ApiNftGetNew, self).post(**kwargs)
        if resp: return resp
        exist_asset = self.model.get_or_none(self.model.asset_id == self.args.get("id")[0])
        if exist_asset:
            self.data = {
                "id": self.args.get("id"),
                "userId": self.args.get("userId")
            }
            self.code = api_resp_code["success"]
            self.http_code = 201
            data = {
                "appid": kwargs["appid"],
                "user_id": self.args.get("userId"),
                "ids": self.args.get("id"),
                "gtx": self.args.get("tsId")
            }
            if self.args.get("targetUserId"):
                data["targetUserId"] = self.args.get("targetUserId")
            notify_mintage_complete_task.delay(data)
            return self.utils.make_api_response(
                message=self.message, 
                data=self.data,
                status=self.http_code, 
                code=self.code
            )
        self.user = self.models.Users.get_user_by_user_id(self.args.get("userId"))
        if self.user and self.user.user_id == kwargs["userid"]:
            self.args["address"] = self.user.eth_address
            self.args["key"] = self.user.eth_key
            try:
                task_data = {
                    "id": self.args["id"],
                    "gameid": kwargs["gameid"],
                    "userid": self.user.user_id,
                    "address": self.args["address"],
                    "tsId": self.args["tsId"],
                    "desc": self.args["desc"]
                }
                if self.args.get("targetUserId"):
                    task_data["targetUserId"] = self.args.get("targetUserId")
                create_or_update_gtx(
                    self.args["tsId"],
                    kwargs["gameid"],
                    desc="NftGetNew",
                    result=json.dumps({
                        "id": self.args.get("id"),
                        "userId": self.args.get("userId")
                    }) if not self.args.get("targetUserId") else \
                    json.dumps({
                        "id": self.args.get("id"),
                        "targetUserId": self.args.get("targetUserId"),
                        "userId": self.args.get("userId")
                    })
                )
                mintage_task.delay(task_data)
            except Exception as e:
                self.message = e.args[0] if hasattr(e, "args") else e.__str__()
            else:
                self.data = {
                    "id": self.args.get("id"),
                    "userId": self.args.get("userId")
                }
                if self.args.get("targetUserId"):
                    self.data["targetUserId"] = self.args.get("targetUserId")
                self.code = api_resp_code["success"]
                self.http_code = 201
        else:
            self.message = "invalid user id"
        return self.utils.make_api_response(
            message=self.message, 
            data=self.data,
            status=self.http_code, 
            code=self.code
        )

class ApiNftUpdate(_NftForGameResource):
    """
    game's nft request sync desc to store
    """
    def post(self,  **kwargs):
        args = self.parser.parse_args()
        api_arguments_sign_verify(args, kwargs["secret"])
        message = {
            "id": args.get("userId"),
            "userId": args.get("id")
        }
        return self.utils.make_api_response(message=message, status=201)

class ApiNftConsignment(_NftForGameResource):
    
    """
    game's nft request to store sell
    """
    def post(self, **kwargs):
        # self.parser.add_argument("price", type=str, location='json', required=True)
        resp = super(ApiNftConsignment, self).post(**kwargs)
        if resp: return resp
        self.user = self.models.Users.get_user_by_user_id(self.args.get("userId"))
        if self.user:
            asset = self.find_user_asset()
            if asset:
                commodity = self.models.Commodity.get_or_none(
                    self.models.Commodity.asset == asset.id,
                    self.models.Commodity.status == commodity_status["on_sale"]
                )
                if not commodity:
                    try:
                        with db.database.atomic():
                            asset.desc = self.args.get("desc")
                            asset.save()
                            commodity = self.models.Commodity.create(
                                asset=asset,
                                seller=self.user,
                                price=Decimal(self.args.get("price")).quantize(Decimal("0.00000000")),
                                price_unit=kwargs.get("token")
                            )
                            create_or_update_gtx(
                                self.args["tsId"], 
                                kwargs["gameid"],
                                desc="NftConsignment",
                                result=json.dumps({
                                    "id": self.args.get("id"),
                                    "userId": self.args.get("userId")
                                })
                            )
                    except Exception as e:
                        #todo log error info
                        self.message = e.args[0] if hasattr(e, "args") else e.__str__()
                    else:
                        self.data = {
                            "id": self.args.get("id"),
                            "userId": self.args.get("userId")
                        }
                        self.code = api_resp_code["success"]
                        self.http_code = 201
                else:
                    self.message = "The asset has on sale"
            else:
                self.message = "the user have no this nft asset"
        else:
            self.message = "invalid user id"
        return self.utils.make_api_response(
            message=self.message,
            data=self.data,
            status=self.http_code,
            code=self.code
        )

class ApiNftTransfer(_NftForGameResource):

    """
    transfer nft from game to store
    """
    def post(self, **kwargs):
        resp = super(ApiNftTransfer, self).post(**kwargs)
        if resp: return resp
        # todo nft 属性参数校验 -- json 字符串
        self.user = self.models.Users.get_user_by_user_id(self.args.get("userId"))
        if self.user:
            asset = self.find_user_asset()
            if asset:
                try:
                    with db.database.atomic():
                    # todo 多游戏支持 避免属性覆盖
                        asset.desc = self.args.get("desc")
                        asset.visible = visible_status["visible"]
                        asset.lock = False
                        asset.save()
                        create_or_update_gtx(
                            self.args["tsId"], 
                            kwargs["gameid"], 
                            desc="NftTransfer",
                            result=json.dumps({
                                "id": self.args.get("id"),
                                "userId": self.args.get("userId")
                            })
                        )
                except Exception as e:
                    self.message = e.args[0] if hasattr(e, "args") else e.__str__()
                else:
                    self.data = {
                        "id": self.args.get("id"),
                        "userId": self.args.get("userId")
                    }
                    self.code = api_resp_code["success"]
                    self.http_code = 201
            else:
                self.message = "the user have no this nft asset"
        else:
            self.message = "invalid user id"
        return self.utils.make_api_response(
            message=self.message,
            data=self.data,
            status=self.http_code,
            code=self.code
        )