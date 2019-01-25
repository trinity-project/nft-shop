
from .. import app
from flask import Flask,request,jsonify
from werkzeug.exceptions import HTTPException
import flask_restful
from functools import wraps
from flask_security import current_user
from .common import CommonResource, api_abort,api_login_required,api_arguments_sign_verify, parse_BizParam
from datetime import timedelta, datetime
from flask_restful import reqparse, current_app
from decimal import Decimal
import json,random
from ..utils import api_login_required
from app.types import api_resp_code,visible_status, commodity_status


per_page = 3

# 首页-展示商品
class _CommodityResource(CommonResource):
    def __init__(self,**kwargs):
        super(_CommodityResource, self).__init__(**kwargs)
        self.models = self.models.Commodity
class ApiShowCommodity(_CommodityResource):
    def get(self):
        commodity_level = self.models.select().order_by(self.models.level.desc()).limit(4)
        com_level = []
        for q in commodity_level:
            data = {}
            data["id"] = q.id
            data["name"] = q.name
            data["desc"] = q.desc
            data["price"] = float(q.price)
            data["price_unit"] = q.price_unit
            com_level.append(data)
        commodity_date = self.models.select().order_by(self.models.created_at.desc()).limit(4)
        com_date = []
        for q in commodity_date:
            data = {}
            data["id"] = q.id
            data["name"] = q.name
            data["desc"] = q.desc
            data["price"] = float(q.price)
            data["price_unit"] = q.price_unit
            com_date.append(data)
        data = {
            'commodity_level': com_level,
            'commodity_data' : com_date
        }
        return self.utils.make_api_response(data=data)

# 首页-切换商品类型
class _CommodityClassResource(CommonResource):
    def __init__(self, **kwargs):
        super(_CommodityClassResource, self).__init__(**kwargs)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("id", type=int, location='json', required=True)
        self.parser.add_argument("page", type=int, location='json', required=True)
        self.models = self.models.Commodity

class ApiExchangeClass(_CommodityClassResource):
    # 将当前要切换到的商品种类id传入
    def post(self,**kwargs):
        """
        获取商品id为commodity_type_id的商品信息
        :param commodity_type_id:
        :return:
        """
        args = self.parser.parse_args()
        commodity_type_id = args.get('id')
        page = args.get('page',1)
        if commodity_type_id != None:
            query = self.models.select().where(
                self.models.commodity_type == commodity_type_id, self.models.status == 1
            ).order_by(self.models.created_at.desc()).limit(4).offset((page - 1) * 4)
        else:
            query = self.models.select().where(self.models.status == 1).order_by(self.models.created_at.desc()).limit(
                4).offset((page - 1) * 4)
        commodity = []
        for q in query:
            data = {}
            data["id"] = q.id
            data["name"] = q.name
            data["desc"] = q.desc
            data["price"] = float(q.price)
            data["price_unit"] = q.price_unit
            commodity.append(data)
        data = {
            'commodity' : commodity
        }
        return self.utils.make_api_response(data=data,page=page)

# 商品详情
class _CommodityInfosResource(CommonResource):
    def __init__(self,**kwargs):
        super(_CommodityInfosResource, self).__init__(**kwargs)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("id", type=int, location='json', required=True)
        self.models = self.models.Commodity

class ApiCommodityInfos(_CommodityInfosResource):
    def post(self,**kwargs):
        args = self.parser.parse_args()
        commodity_id = args.get("id")
        query = self.models.get_or_none(self.models.id == commodity_id)
        if not query:
            return self.utils.make_api_response(message="Illegal operation，please submit order again")
        commodity = {}
        commodity["id"] = query.id
        commodity["name"] = query.name
        commodity["desc"] = query.desc
        commodity["price"] = float(query.price)
        commodity["price_unit"] = query.price_unit
        self.data = {
            "result" : "success",
            "commodity" : commodity
        }
        return self.utils.make_api_response(data=self.data)

# 个人中心页-我的账户
class _MyhomeResource(CommonResource):
    def __init__(self,**kwargs):
        super(_MyhomeResource,self).__init__(**kwargs)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("page", type=int, location='json', required=True)
        self.parser.add_argument("userId", type=str, location='json', required=True)


class ApiMyhone(_MyhomeResource):
    @api_login_required
    def post(self):
        args = self.parser.parse_args()
        page = args.get("page",1)
        user_id = args.get("userId")
        user = self.models.Users.get_or_none(self.models.Users.user_id == user_id)
        asset = self.models.Assets.select().where(self.models.Assets.owner == user.id).limit(10).offset((page-1)*10)
        shopcoin_num = 10-asset.count() if asset.count() < 10 else 0
        if 0 < asset.count() < 10:
            shopcoin = self.models.ShopCoin.select().where(
                self.models.ShopCoin.owner == user.id
            ).order_by(self.models.ShopCoin.created_at.desc()).limit(shopcoin_num)
        elif asset.count() == 0:
            shopcoin = self.models.ShopCoin.select().where(
                self.models.ShopCoin.owner == user.id
            ).order_by(self.models.ShopCoin.created_at.desc()).limit(10).offset((page-1)*10-shopcoin_num+1)
        else:
            shopcoin = self.models.ShopCoin.select().where(
                self.models.ShopCoin.owner == 0)
        asset_infos = []
        for a in asset:
            data = {}
            data["id"] = a.id
            data["name"] = a.cate.name
            data["lock"] = a.lock
            data["asset_id"] = a.asset_id
            asset_infos.append(data)
        for c in shopcoin:
            data = {}
            data["id"] = c.id
            data["name"] = c.cate.name
            data["amount"] = float(c.amount)
            data["lock"] = float(c.lock)
            asset_infos.append(data)

        return self.utils.make_api_response(data=asset_infos,page=page)

# 个人中心页-充值记录
class _RechargeResource(CommonResource):
    def __init__(self, **kwargs):
        super(_RechargeResource, self).__init__(**kwargs)
        self.models = self.models.Recharge
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("page", type=int, location='json', required=True)
        self.parser.add_argument("userId", type=str, location='json', required=True)

class ApiRechargeRecords(_RechargeResource):
    @api_login_required
    def post(self,**kwargs):
        """
        将充值记录Recharge的内容反馈出来
        :return:
        """
        args = self.parser.parse_args()
        page = args.get("page", 1)
        user_id = args.get("userId")
        user = self.models.Users.get_or_none(self.models.Users.user_id == user_id)
        recharge = self.models.select().where(self.models.user == user.id).order_by(
            self.models.created_at.desc()).limit(per_page).offset(per_page*(page-1))
        recharge_infos = []
        for r in recharge:
            data = {}
            data["id"] = r.id
            data["coin"] = r.cate.name
            data["amount"] = float(r.value)
            data["created_at"] = r.created_at.strftime("%Y-%m-%d %H:%M:%S")
            data["status"] = r.status
            recharge_infos.append(data)

        return self.utils.make_api_response(data=recharge_infos,page=page)

# 个人中心页-提币记录
class _TakeOutResource(CommonResource):
    def __init__(self, **kwargs):
        super(_TakeOutResource, self).__init__(**kwargs)
        self.models = self.models.TakeOut
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("page", type=int, location='json', required=False)
        self.parser.add_argument("userId", type=str, location='json', required=True)

class ApiTakeOutRecords(_TakeOutResource):
    @api_login_required
    def post(self,**kwargs):
        """
        将提币记录TakeOut的内容反馈出来
        :return:
        """
        args = self.parser.parse_args()
        page = args.get("page", 1)
        user_id = args.get("userId")
        user = self.models.Users.get_or_none(self.models.Users.user_id == user_id)
        takeout = self.models.select().where(self.models.user == user.id).order_by(
            self.models.created_at.desc()).limit(per_page).offset(per_page*(page-1))
        takeout_infos = []
        for r in takeout:
            data = {}
            data["id"] = r.id
            data["coin"] = r.cate.name
            data["amount"] = float(r.value)
            data["created_at"] = r.created_at.strftime("%Y-%m-%d %H:%M:%S")
            data["status"] = r.status
            data["tx_id"] = r.tx_id
            takeout_infos.append(data)

        return self.utils.make_api_response(data=takeout_infos,page=page)

# 个人中心页-售卖记录
class _SellResource(CommonResource):
    def __init__(self, **kwargs):
        super(_SellResource, self).__init__(**kwargs)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("page", type=int, location='json', required=True)
        self.parser.add_argument("userId", type=str, location='json', required=True)
        self.models = self.models.Commodity

class ApiSellRecords(_SellResource):
    @api_login_required
    def post(self,**kwargs):
        """
        将售卖记录Commodity里卖家是当前用户的商品的内容反馈出来
        :return:
        """
        args = self.parser.parse_args()
        page = args.get("page", 1)
        user_id = args.get("userId")
        user = self.models.Users.get_or_none(self.models.Users.user_id == user_id)
        sell = self.models.select().where(self.models.seller == user.id).limit(per_page).offset((page-1)*per_page)
        sell_infos = []
        for s in sell:
            data = {}
            data["id"] = s.id
            data["asset"] = s.asset.id
            data["commodity_type"] = s.commodity_type
            data["created_at"] = s.created_at.strftime("%Y-%m-%d %H:%M:%S")
            data["status"] = s.status
            sell_infos.append(data)
        return self.utils.make_api_response(data=sell_infos,page=page)

# 个人中心页-订单记录
class _OrderResource(CommonResource):
    def __init__(self,**kwargs):
        super(_OrderResource,self).__init__(**kwargs)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("page", type=int, location='json', required=True)
        self.parser.add_argument("userId", type=str, location='json', required=True)

class ApiOrderRecords(_OrderResource):
    @api_login_required
    def post(self,**kwargs):
        args = self.parser.parse_args()
        page = args.get("page", 1)
        user_id = args.get("userId")
        user = self.models.Users.get_or_none(self.models.Users.user_id == user_id)
        order = self.models.Order.select().where(
            self.models.Order.buyer == user.id
        ).order_by(self.models.Order.created_at.desc()
        ).limit(per_page).offset(per_page*(page-1))
        order_infos = []
        for o in order:
            orderdetail = self.models.OrderDetail.get_or_none(self.models.OrderDetail.order == o.id)
            data = {}
            data["order_id"] = orderdetail.order.id
            data["order_no"] = orderdetail.order.order_no
            data["commodity"] = orderdetail.commodity.id
            data["price"] = float(orderdetail.price)
            data["price_unit"] = orderdetail.order.price_unit
            data["seller"] = orderdetail.commodity.seller.email
            data["quantity"] = orderdetail.quantity
            data["created_at"] = orderdetail.created_at.strftime("%Y-%m-%d %H:%M:%S")
            order_infos.append(data)
        return self.utils.make_api_response(data=order_infos,page=page)

# 个人中心页-兑换记录
class _ExchangeResource(CommonResource):
    def __init__(self, **kwargs):
        super(_ExchangeResource, self).__init__(**kwargs)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("page", type=int, location='json', required=True)
        self.parser.add_argument("userId", type=str, location='json', required=True)
        self.models = self.models.Exchange

class ApiExchangeRecords(_ExchangeResource):
    @api_login_required
    def post(self,**kwargs):
        """
        将兑换记录Exchange的内容反馈出来
        :return:
        """
        args = self.parser.parse_args()
        page = args.get("page", 1)
        user_id = args.get("userId")
        user = self.models.Users.get_or_none(self.models.Users.user_id == user_id)
        exchange = self.models.select().where(self.models.user == user.id).order_by(
            self.models.created_at.desc()).limit(per_page).offset((page-1)*per_page)
        exchange_infos = []
        for s in exchange:
            data = {}
            data["id"] = s.id
            data["pair"] = s.pair.id
            data["token"] = s.pair.token.name
            data["currency"] = s.pair.currency.name
            data["quantity"] = float(s.quantity)
            data["amount"] = float(s.amount)
            data["created_at"] = s.created_at.strftime("%Y-%m-%d %H:%M:%S")
            data["exchange_type"] = s.exchange_type
            exchange_infos.append(data)
        return self.utils.make_api_response(data=exchange_infos,page=page)

# 换一批
class _ChangeCommodityResource(CommonResource):
    def __init__(self, **kwargs):
        super(_ChangeCommodityResource, self).__init__(**kwargs)
        self.models = self.models.Commodity

class ApiChangeCommodity(_ChangeCommodityResource):
    def get(self):
        date_commodity = self.models.select().order_by(self.models.created_at.desc())
        dc = [c for c in date_commodity]
        random.shuffle(dc)
        commodity_date = []
        for dc in dc[:4]:
            data = {}
            data["id"] = dc.id
            data["name"] = dc.name
            data["id"] = dc.id
            data["name"] = dc.name
            data["desc"] = dc.desc
            data["price"] = float(dc.price)
            data["price_unit"] = dc.price_unit
            data["created_at"] = dc.created_at.strftime("%Y-%m-%d %H:%M:%S")
            commodity_date.append(data)
        for c in commodity_date:
            # datetime.strptime(c["created_at"],"%Y-%m-%d %H:%M:%S")
            commodity_date.sort(key=lambda c:c["created_at"],reverse=True)
        level_commodity = self.models.select().order_by(self.models.level.desc())
        lc = [c for c in level_commodity]
        random.shuffle(lc)
        commodity_level = []
        for dc in lc[:4]:
            data = {}
            data["id"] = dc.id
            data["name"] = dc.name
            data["id"] = dc.id
            data["name"] = dc.name
            data["desc"] = dc.desc
            data["price"] = float(dc.price)
            data["price_unit"] = dc.price_unit
            data["level"] = dc.level
            commodity_level.append(data)
        for c in commodity_level:
            commodity_level.sort(key=lambda c: c["level"], reverse=True)
        data = {
            "result":"success",
            "commodity_date" : commodity_date,
            "commodity_level" : commodity_level
        }
        return self.utils.make_api_response(data=data)
