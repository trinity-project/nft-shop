# -*- coding: utf-8 -*-
"""
the subscribers of signals for app
"""
from app.signals import recharge_created, takeout_created, mintage_created, \
receive_notification_onchain, user_disabled
from .utils import subscribe_monitoring_onchain, get_app_logger, detect_monitor_event, \
create_or_update_erc20
from .models import Recharge, TakeOut, Assets, Mintage, Users, ShopCoin, Coin, GameType
from . import types, db, app
from .game_api import GameApi
from decimal import Decimal
from datetime import datetime
from app.asynctasks import take_out_task, subscribe_monitoring_task, notify_mintage_complete_task
from flask import g

@recharge_created.connect_via("app")
def recharge_created_called(sender, **kwargs):
    print(kwargs)
    info = {
        "messageType": "pushEthAddress",
        "event": "recharge",
        "playload": kwargs.get("addr"),
        "walletAddress": "placeholder",
        "assetType": kwargs.get("asset_type")
    }
    try:
        subscribe_monitoring_task.delay(info)
    except:
        get_app_logger().exception("发布订阅监控任务异常")
    # subscribe_monitoring_onchain(info)

@takeout_created.connect_via("app")
def takeout_created_called(sender, **kwargs):
    try:
        take_out_task.delay(kwargs)
    except:
        get_app_logger().exception("发布提币任务异常")

@mintage_created.connect_via("app")
def mintage_created_called(sender, **kwargs):
    info = {
        "messageType": "pushEthTx",
        "event": "mintage",
        "walletAddress": "placeholder",
        "playload": kwargs.get("tx_id"),
        "assetType": kwargs.get("asset_type")
    }
    try:
        subscribe_monitoring_task.delay(info)
    except:
        get_app_logger().exception("发布订阅监控任务异常")

@receive_notification_onchain.connect_via("app")
def receive_notification_onchain_called(sender, **data):
    get_app_logger().info("收到监控通知消息\n：{}".format(data))
    message_type = data.get("messageType")
    from_addr = data.get("addressFrom")
    to_addr = data.get("addressTo")
    tx_id = data.get("txId")
    token_id = data.get("tokenId")
    value = data.get("value")
    asset_type = data.get("assetType").upper()
    timestamp = data.get("timestamp")
    event = detect_monitor_event(message_type, from_addr)
    if event == "recharge":
        recharge = Recharge.get_or_none(
            Recharge.status == types.recharge_status["pending"],
            Recharge.receiver == to_addr
        )
        try:
            with db.database.atomic():
                if recharge:
                    if asset_type != recharge.cate.name:
                        cate = Coin.get_or_none(Coin.name == asset_type)
                        if not cate:
                            get_app_logger().error("充值的资产是商城不支持的资产类型")
                            return False
                        else:
                            recharge.cate = cate.id
                    recharge.status = types.recharge_status["complete"]
                    recharge.tx_id = tx_id
                    recharge.sender = from_addr
                    recharge.value = Decimal(value) if value else 1
                    recharge.complete_at = datetime.fromtimestamp(float(timestamp))
                    recharge.save()
                    
                    # erc721 asset
                    if token_id:
                        if not isinstance(token_id, int):
                            token_id = int(token_id)
                        hex_token_id = hex(token_id)[2:]
                        asset = Assets.get_or_none(Assets.asset_id == hex_token_id)
                        if asset:
                            asset.owner = recharge.user.id
                            asset.visible = types.visible_status["visible"]
                            asset.lock = False
                            asset.save()
                        else:
                            get_app_logger().error("充值的nft资产在商城内找不到记录")
                    # erc20 (include eth) asset
                    elif value:
                        create_or_update_erc20(
                            amount=value,
                            userid=recharge.user.id,
                            cateid=recharge.cate.id,
                            timestamp=timestamp
                        )
                    else:
                        get_app_logger().error("收到异常的监控通知消息")
                else:
                    get_app_logger().error("充值监控通知消息未匹配充值记录")
        except Exception:
            get_app_logger().exception("铸币监控消息处理失败")

    elif event == "takeout":
        query = TakeOut.get_or_none(
            TakeOut.status == types.take_out_status["pending"],
            TakeOut.tx_id == tx_id
        )
        try:
            with db.database.atomic():
                if query:
                    query.status = types.take_out_status["complete"]
                    query.complete_at = datetime.fromtimestamp(float(timestamp))
                    query.save()
                    # erc721 asset
                    if token_id:
                        hex_token_id = hex(token_id)[2:]
                        asset = Assets.get_or_none(Assets.asset_id == hex_token_id)
                        if asset:
                            asset.owner = g.sys_admin.id
                            asset.took = True
                            # asset.visible = types.visible_status["invisible"]
                            asset.lock = False
                            asset.save()
                        else:
                            get_app_logger().error("监控的推送的nft提币资产在商城内找不到记录")
                    # erc20 (include eth) asset
                    elif value:
                        result = create_or_update_erc20(
                            "takeout",
                            amount=value,
                            userid=query.user.id,
                            cateid=query.cate.id,
                            timestamp=timestamp
                        )
                        if not result:
                            get_app_logger().error("用户资产记录异常 链上发送token数量超出锁币数量")
                    else:
                        get_app_logger().error("收到异常的监控通知消息")
                else:
                    get_app_logger().error("提币监控通知消息未匹配提币记录")
        except Exception:
            get_app_logger().exception("提币监控通知消息处理失败")

    elif event == "mintage":
        query = Mintage.get_or_none(
            Mintage.status == types.mintage_status["pending"],
            Mintage.tx_id == tx_id
        )
        if query:
            try:
                with db.database.atomic():
                    query.status = types.mintage_status["complete"]
                    query.complete_at = datetime.fromtimestamp(float(timestamp))
                    query.save()
                    asset_ids = query.text_ids.split(" ")
                    cate = Coin.get_or_none(Coin.name == query.game.asset)
                    if query.target_user:
                        user = Users.get_user_by_user_id(query.target_user)
                        data = [{"asset_id": aid, "desc": query.desc, "owner": user.id, "cate": cate.id, "lock": True} for aid in asset_ids]
                    else:
                        user = Users.get_user_by_user_id(query.user_id)
                        data = [{"asset_id": aid, "desc": query.desc, "owner": user.id, "cate": cate.id} for aid in asset_ids]

                    # insert maxsize(100) row at a time 
                    for index in range(0, len(data), 100):
                        Assets.insert_many(data[index:index+100]).execute()
            except Exception as e:
                get_app_logger().exception("铸币监控消息处理失败")
            else:
                try:
                    data = {
                        "appid": query.game.appid,
                        "user_id": str(query.user_id),
                        "ids": asset_ids,
                        "gtx": query.gtx
                    }
                    if query.target_user:
                        data["targetUserId"] = str(query.target_user)
                    notify_mintage_complete_task.delay(data)
                except:
                    get_app_logger().exception("发布[通知游戏铸币成功任务]异常")

@user_disabled.connect_via("app")
def user_disabled_called(sender, **kwargs):
    # 无法实现预期的功能 需要改进 
    from flask_security import current_user, logout_user
    if current_user.get_id() == kwargs.get("uid"):
        logout_user()