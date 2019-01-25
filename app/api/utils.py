# -*- coding: utf-8 -*-
from flask import request
from app.models import GameType, GameTransaction
from app import app
from app.types import sync_status, game_transaction_type, api_resp_code
from app.ethchain import create_nft, set_nft_by_token_id, get_nft_by_token_id
import requests
# 以后可能需要放入缓存
games_dict = GameType.get_games_dict

def custom_api_error_response(status=200, message=None):
    data = {
        "code": api_resp_code["ts_untreated"] if status == 403 else api_resp_code["faile"],
        "http_status_code": status,
        "message": message,
        "api": request.path
    }
    return data

def request_create_new_nft_onchain(args):
    """
    向链上请求创建一个新的nft资产
    """
    # import inspect
    # print(inspect.stack()[1].filename)
    try:
        int_nft_ids = [int(nft_id, 16) for nft_id in args.get("id")]
    except ValueError:
        return "asset id not a base 16 str"
    else:
        try:
            res = create_nft(int_nft_ids, args.get("address"), "9f56b1bc6c7ae9a715c7af2415f4c8c72ea3e2ebb8479b516918ae19dd3354ab")
            print(res)
            return res
        except Exception as e:
            raise e
            print(e)
            return "request nft create onchain failed"
            # return {
            #     "txId": "test tx id"
            # }

def set_nft_attr_onchain(args):
    """
    向链上请求更新nft资产属性
    """
    import json
    attr = {
        "attr1": "the value of attr1",
        "attr2": "the value of attr2  false modify" 
    }
    attr = json.dumps(attr)
    try:
        int_nft_id = int(args.get("id"), 16)
    except ValueError:
        return "asset id not a base 16 str"
    else:
        try:
            res = set_nft_by_token_id(args.get("address"), int_nft_id, attr, False, "095e53c9c20e23fd01eaad953c01da9e9d3ed9bebcfed8e5b2c2fce94037d963")
            print(res)
            return res
        except Exception as e:
            raise e
            return "request nft create onchain failed"

def get_nft_by_id(args):
    try:
        int_nft_id = int(args.get("id"), 16)
    except ValueError:
        return "asset id not a base 16 str"
    return get_nft_by_token_id(int_nft_id)

def find_game_transaction(tr_id, game_id):
    gtx = GameTransaction.get_or_none(
        GameTransaction.game == game_id,
        GameTransaction.transaction_id == tr_id
    )
    return gtx

def create_or_update_gtx(ts_id, game_id, gtx=None, **kwargs):
    if gtx:
        gtx.status = sync_status["complete"]
        gtx.save()
    else:
        GameTransaction.create(
            game=game_id,
            transaction_id=ts_id,
            result=kwargs["result"],
            desc=kwargs["desc"],
            status=sync_status["complete"]
        )