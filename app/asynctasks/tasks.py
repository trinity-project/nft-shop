# -*- coding: utf-8 -*-
from kombu import Exchange, Queue
from app import celery, app, mail
from app.utils import subscribe_monitoring_onchain
from app.models import TakeOut, Mintage
from app.ethchain import transfer_from, eth_client, create_nft
from app.game_api import GameApi
from app.signals import mintage_created
from flask_mail import Message
from decimal import Decimal
import time

celery.conf.update(
    broker_transport_options={
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.2,
    },
    task_queues = (
        Queue("default", Exchange("default"), routing_key="default"),
        Queue("task_take_out",Exchange("task_take_out"),routing_key="task_take_out"),
        Queue("subscribe_monitoring",Exchange("subscribe_monitoring"),routing_key="subscribe_monitoring"),
        Queue("send_mail",Exchange("send_mail"),routing_key="send_mail")
    ),
    task_routes = {
        "app.asynctasks.tasks.take_out_task": {"queue":"task_take_out","routing_key":"task_take_out"},
        "app.asynctasks.tasks.mintage_task": {"queue":"task_take_out","routing_key":"task_take_out"},
        "app.asynctasks.tasks.send_email_task": {"queue":"send_mail","routing_key":"send_mail"},
        "app.asynctasks.tasks.subscribe_monitoring_task": {"queue":"subscribe_monitoring","routing_key":"subscribe_monitoring"}
    },
    task_ignore_result = True,
    timezone='Asia/Shanghai'
)

@celery.task(bind=True, max_retries=3)
def send_email_task(self, rev, content):
    """
    发送邮件任务
    """
    try:
        with app.app_context():
            msg = Message("Market verification code", sender=("Wob Games", "no-reply@trinity.tech"), recipients=[rev])
            msg.body = content
            msg.html = '<b>{}</b>'.format(msg.body)
            mail.send(msg)
    except Exception as exc:
        self.retry(exc=exc, countdown=10)

@celery.task(bind=True, max_retries=10)
def subscribe_monitoring_task(self, data):
    """
    订阅链上监控任务  
    :param data: dict  
    keys:  
    messageType event playload walletAddress assetType
    """
    try:
        data['chainType'] = 'ETH'
        subscribe_monitoring_onchain(data)
        return True
    except Exception as exc:
        self.retry(exc=exc, countdown=10)

@celery.task(bind=True, max_retries=3)
def take_out_task(self, data):
    """
    提币任务  
    :param data: dict  
    keys:  
    asset_type token_id from_addr to_addr value pk take_id
    """
    try:
        token_name = data["asset_type"]
        token_id = data.get("token_id")
        from_addr = data["from_addr"]
        to_addr = data["to_addr"]
        value = Decimal(data["value"])
        pk = data["pk"]
        take_out_id = data["take_id"]
        take = TakeOut.get(id=take_out_id)
        if take.tx_id != '0x': return True
        if token_name.lower() == "wba":
            int_token_id = int(token_id,16)
            res = transfer_from(from_addr, to_addr, int_token_id, pk)
        elif token_name.lower() == "eth":
            res = eth_client.transfer_eth(from_addr, to_addr, value, pk)
        else:
            res = eth_client.transfer_erc20(token_name.lower(), from_addr, to_addr, value, pk)
        if res and isinstance(res, dict):
            TakeOut.update(tx_id=res["txId"]).where(TakeOut.id == take_out_id).execute()
            info = {
                "messageType": "pushEthTx",
                "event": "takeout",
                "playload": res["txId"],
                "walletAddress": "placeholder",
                "assetType": token_name
            }
            # 调用订阅链上监控任务
            subscribe_monitoring_task.delay(info)
            return True
    except Exception as exc:
        self.retry(exc=exc, countdown=60)

@celery.task(bind=True, max_retries=100)
def notify_mintage_complete_task(self, data):
    """
    通知游戏铸币成功任务
    """
    try:
        GameApi.notify_mintage_complete(data)
        return True
    except Exception as exc:
        self.retry(exc=exc, countdown=60)

@celery.task(bind=True, max_retries=100)
def distribute_props_task(self, data):
    """
    分发道具任务
    """
    try:
        GameApi.distribute_props(data)
        return True
    except Exception as exc:
        self.retry(exc=exc, countdown=60)

@celery.task(bind=True, max_retries=100)
def distribute_erc721_asset_task(self, data):
    """
    分发erc721资产任务
    """
    try:
        GameApi.distribute_erc721_asset(data)
        return True
    except Exception as exc:
        self.retry(exc=exc, countdown=60)

@celery.task(bind=True, max_retries=100)
def distribute_erc20_asset_task(self, data):
    """
    分发erc20资产任务
    """
    try:
        GameApi.distribute_erc20_asset(data)
        return True
    except Exception as exc:
        self.retry(exc=exc, countdown=60)

@celery.task(bind=True, max_retries=100)
def mintage_task(self, data):
    try:
        int_nft_ids = [int(nft_id, 16) for nft_id in data.get("id")]
    except ValueError:
        return "asset id not a base 16 str"
    else:
        try:
            res = create_nft(int_nft_ids, data.get("address"), app.config["WBA_CREATE_PK"])
        except Exception as exc:
            self.retry(exc=exc, countdown=60)
        else:
            if isinstance(res, dict):
                mintage = Mintage.create(
                    text_ids=" ".join(data.get("id")),
                    game=data["gameid"],
                    user_id=data["userid"],
                    tx_id=res["txId"],
                    gtx=data["tsId"],
                    desc=data["desc"]
                )
                if data.get("targetUserId"):
                    mintage.target_user = int(data["targetUserId"])
                    mintage.save()
                mintage_created.send("app", tx_id=res["txId"], asset_type="nft")


@celery.task(bind=True,max_retries=1)
def sum(self, num):
    try:
        num = num + '1'
        return num
    except Exception as exc:
        self.retry(exc=exc, countdown=5)