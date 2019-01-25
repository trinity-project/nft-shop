# -*- coding: utf-8 -*-
__author__ = 'xu'
import json
import random
import bcrypt
import binascii
import requests
from hashlib import md5
from websocket import create_connection
from datetime import datetime, date, timedelta
from functools import wraps
from math import ceil
from random import SystemRandom
from ethereum.utils import checksum_encode, privtoaddr
from flask import jsonify, g, abort,request, url_for,redirect, session
from flask_security import current_user, login_user
from flask_security.utils import hash_password as fs_hash_password
from .models import Users, Role, UserRoles, Recharge, TakeOut, GameType, Assets, \
Commodity, Order, OrderDetail, GameAssets, Coin, ShopCoin, Props, Mintage, ExchangePair, Exchange,\
GameTransaction, MallTransaction
from . import auth, db, app
from decimal import Decimal

def create_tables():
    auth.User.create_table(fail_silently=True)
    Users.create_table(fail_silently=True)
    Role.create_table(fail_silently=True)
    UserRoles.create_table(fail_silently=True)
    GameType.create_table(fail_silently=True)
    Coin.create_table(fail_silently=True)
    Props.create_table(fail_silently=True)
    Assets.create_table(fail_silently=True)
    Recharge.create_table(fail_silently=True)
    TakeOut.create_table(fail_silently=True)
    Commodity.create_table(fail_silently=True)
    Order.create_table(fail_silently=True)
    OrderDetail.create_table(fail_silently=True)
    GameAssets.create_table(fail_silently=True)
    ShopCoin.create_table(fail_silently=True)
    Mintage.create_table(fail_silently=True)
    ExchangePair.create_table(fail_silently=True)
    Exchange.create_table(fail_silently=True)
    GameTransaction.create_table(fail_silently=True)
    MallTransaction.create_table(fail_silently=True)
    
def init_admin_user():
    if auth.User.select().count() == 0:
        # print 'create admin user'
        admin = auth.User(username=app.config["ADMIN_USER"], email='lala@al.com',
                          admin=True, active=True)
        admin.set_password(app.config["ADMIN_PASSWORD"])
        admin.save()
    sys_admin_role = Role.get_or_none(Role.name == "sys_admin")
    print(sys_admin_role)
    if not sys_admin_role:
        print("创建系统用户")
        with app.app_context():
            user = Users.create(email="market@wob.games", password=fs_hash_password(app.config["ADMIN_PASSWORD"]))
            role = Role.create(name="sys_admin")
            UserRoles.create(customer=user, role=role)


def make_api_response(status=200, page=None, message=None, data=None, code=1):
    msg = {
        "code": code,
        "http_status_code": status,
        "api": request.path
    }
    if page != None:
        msg["current_page"] = page
    if data != None:
        msg["data"] = data
    if message != None:
        msg["message"] = message
    return msg, status
    # return jsonify(data)

class Pagination(object):
    def __init__(self, cur_page, per_page, total_count):
        self.cur_page = cur_page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.cur_page > 1

    @property
    def has_next(self):
        return self.cur_page < self.pages

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        has_gen_none = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
                    (self.cur_page - left_current - 1 < num < self.cur_page + right_current):
                yield num
            elif not has_gen_none:
                yield None
                has_gen_none = 1


def url_for_page(page, arg=None):
    args = request.args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

def url_for_search(key,value):
    args = request.args.copy()
    args[key] = value
    if not value:
        del args[key]
    
    return url_for(request.endpoint, **args)

def current_user_has_role(role_name):
    """
    验证当前用户是否拥有某个角色
    """
    return current_user.has_role(role_name)

def request_data_to_dict():
    """
    request数据转dict
    """
    data = {}
    if request.is_json:
        data = request.json
    else:
        for key in request.form.keys():
            if len(key) > app.config["FORM_KEY_LEN"]: abort(400)
            tmp = key if not key.endswith("[]") else key[:-2]
            if len(request.form.getlist(key)) > 1:
                data[tmp] = request.form.getlist(key)
            else:
                data[tmp] = request.form.getlist(key)[0]
    return data

def create_verify_code():
    """
    生成6位随机数字验证码
    """
    code = random.randint(100000,999999)
    return str(code)

def hash_password(password):
    """
    使用 CRYPT_BLOWFISH 算法创建散列\n
    随机 salt 保存在密码 hashed 中
    """
    password = password.encode("utf-8")
    try:
        salt = salt = bcrypt.gensalt(rounds=10)
        hashed = bcrypt.hashpw(password, salt)
    except Exception:
        hashed = None
    if isinstance(hashed, bytes):
        hashed = hashed.decode("utf-8")
    return hashed

def verify_password(password, hashed):
    """
    验证密码
    """
    password = password.encode("utf-8")
    hashed = hashed.encode("utf-8")
    print(password, hashed)
    try:
        result = bcrypt.checkpw(password, hashed)
    except Exception:
        result = False
    return result

def create_eth_addr_key():
    try:
        random=SystemRandom()
        key = hex(random.getrandbits(256))[2:-1].zfill(64)
        assert len(key) == 64
        addr=checksum_encode(binascii.hexlify(privtoaddr(key)).decode())
        return addr, key
    except Exception:
        return None

def subscribe_monitoring_onchain(info):

    """
    subscribe one or more event from onchain monitoring system  
    :param info: dict  
        event: recharge/takeout/mintage/update_nft
        addr: list
        txId: list
        assetType: erc20/erc271
    """
    # try:
    ws = create_connection(app.config["MONITOR_URL"], timeout=5)
    len = ws.send(json.dumps(info))
    print(len)
    ws.close()
    # except Exception as e:
    #     print(e.args)

def get_app_logger():
    return app.logger

def wrap_template_name(tpl_name):
    select_lang = session.get("lang") or "en"
    return "{}/{}".format(select_lang, tpl_name)

def detect_monitor_event(msg_type, from_addr):
    if msg_type == "pushEthAddress":
        event = "recharge"
    elif msg_type == "pushEthTx":
        if from_addr == "0x0000000000000000000000000000000000000000":
            event = "mintage"
        else:
            event = "takeout"
    else:
        event = "update"
    return event

def reset_user_password(user_email, new_password):
    """
    重置用户密码
    """
    return Users.update(password=fs_hash_password(new_password)).where(Users.email==user_email).execute()

def reset_user_pay_password(user_email, new_pay_password):
    """
    重置用户支付密码
    """
    return Users.update(pay_password=fs_hash_password(new_pay_password)).where(Users.email==user_email).execute()

def create_or_update_erc20(option="recharge", **kwargs):
    amount = Decimal(kwargs["amount"])
    userid = kwargs["userid"]
    cateid = kwargs["cateid"]
    complete_time = datetime.fromtimestamp(float(kwargs["timestamp"]))
    coin = ShopCoin.get_or_none(
        ShopCoin.owner == userid,
        ShopCoin.cate == cateid
    )
    if option == "recharge":
        if coin:
            coin.amount = coin.amount + amount
            coin.updated_at = complete_time
            coin.save()
        else:
            ShopCoin.create(
                cate=cateid,
                owner=userid,
                amount=amount,
                lock=0
            )
        return True
    elif option == "takeout":
        if not coin: return False
        else:
            if coin.take_lock < amount:
                return False
            coin.lock = coin.take_lock - amount
            coin.amount = coin.amount - amount
            coin.updated_at = complete_time
            coin.save()
        return True

def md5_args_sign_verify(args, secret):
    arg_sign = args.get("sign").lower()
    del args["sign"]
    pairs = sorted(args.items(), key=lambda e: e[0].lower())
    print(pairs)
    text = str()
    for key, value in pairs:
        text = text + "{}={}".format(key, value)
    print(text)
    text = "{0}{1}{0}".format(secret, text)
    text = text.encode("utf-8")
    sign = md5(text).hexdigest().lower()
    print(sign)
    if arg_sign == sign:
        return True
    else: 
        return False

def api_login_required(func):
    """
    自定义视图装饰器
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return make_api_response(
                status=401,
                message="authenticated error",
                code=-1
            )
        return func(*args, **kwargs)
    return decorated_function