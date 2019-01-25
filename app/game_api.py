# -*- coding: utf-8 -*-
from flask import request
from .models import GameType, MallTransaction
from app import app
from .types import sync_status
import time
import requests
import json
from hashlib import md5


def create_mtx(ts_id, json_str, mtx=None, **kwargs):
    mtx = MallTransaction.create(
        sync_content=json_str,
        transaction_id=ts_id,
        status=sync_status["pending"]
    )
    return mtx

def update_mtx(mtx):
    mtx.status = sync_status["complete"]
    mtx.save()

def request_game_api(path, appid ,data, mtx=None):
    """
    request game api\n
    :param asset_type: the type of request transactions: neo or eth
    """
    try:
        games_dict = GameType.get_games_dict()
        if path != "/api/v1/nft/createresult":
            data["rsId"] = str(int(time.time()*10**3))
        data_str = json.dumps(data)
        sign_text = "{0}args={1}{0}".format(games_dict[appid]["secret"], data_str)
        print(sign_text)
        msg = {
            "args": data_str,
            "sign": md5(sign_text.encode("utf-8")).hexdigest()
        }
        print(msg)
        res = requests.post(
            app.config["GAME_API_HOST"] + path,
            headers={"App-Id": appid},
            json=msg,
            timeout=(3.05, 15)
        )
        result = res.json()
        print(result)
        if mtx: update_mtx(mtx)
        return result
    except Exception:
        raise

class GameApi(object):

    @classmethod
    # def distribute_erc20_asset(cls, appid, user_id, **kwargs):
    def distribute_erc20_asset(cls, data):
        """
        分发erc20资产到游戏 wbt
        """
        api_path = "/api/v1/wbt/update"
        msg = {
            "userId": str(data["user_id"]),
            "wbtTotal": data["lock"],
            "wbtDelta": data["amount"],
            "assetType": data["asset_type"]
        }
        request_game_api(api_path, data["appid"], msg)

    @classmethod
    # def distribute_erc721_asset(cls, appid, user_id, **kwargs):
    def distribute_erc721_asset(cls, data):
        """
        分发erc721资产到游戏
        """
        api_path = "/api/v1/nft/pour"
        msg = {
            "userId": str(data["user_id"]),
            "id": data["id"] if isinstance(data["id"], list) else [data["id"]]
        }
        request_game_api(api_path, data["appid"], msg)

    @classmethod
    # def distribute_props(cls, appid, user_id, **kwargs):
    def distribute_props(cls, data):
        """
        分发道具到游戏
        """
        api_path = "/api/v1/item/pour"
        msg = {
            "userId": str(data["user_id"]),
            "itemCount": data["item_count"],
            "itemId": data["item_id"]
        }
        request_game_api(api_path, data["appid"], msg)

    @classmethod
    # def notify_mintage_complete(cls, appid, user_id, **kwargs):
    def notify_mintage_complete(cls, data):
        """
        通知游戏铸币成功
        """
        api_path = "/api/v1/nft/createresult"
        msg = {
            "userId": data["user_id"],
            "id": data["ids"],
            "rsId": data["gtx"],
            "code": 1
        }
        request_game_api(api_path, data["appid"], msg)

if __name__ == "__main__":
    GameApi.distribute_erc721_asset(
        "wob071913289742227",
        "6425605781151809538",
        id="asdfrt"
    )