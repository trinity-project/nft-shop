
import requests,re
from flask_security.utils import verify_password
from decimal import Decimal
from .common import CommonResource,api_abort,parse_BizParam
from flask_restful import reqparse
from flask_security.utils import verify_password
from flask_security import current_user
from app import db
from ..utils import api_login_required

# 点击商品进行购买(提交订单)
class ApiBuy(CommonResource):
    def __init__(self, **kwargs):
        super(ApiBuy, self).__init__(**kwargs)
        self.parser = reqparse.RequestParser()
        # 表单验证提交的信息
        self.parser.add_argument("id", type=int, location='json', required=True)
        self.parser.add_argument("quantity", type=int, location='json', required=True)
        self.parser.add_argument("pay_password", type=str, location='json', required=True)
        self.parser.add_argument("userId", type=str, location='json', required=True)
        # self.parser.add_argument("args", type=str, address='json', required=True)
        # self.parser.add_argument("sign", type=str, address='json', required=True)

    @api_login_required
    def post(self,**kwargs):
        args = self.parser.parse_args()
        quantity = int(args['quantity'])
        pay_password = str(args["pay_password"])
        user_id = args.get("userId")
        user = self.models.Users.get_or_none(self.models.Users.user_id == user_id)
        if not pay_password or not quantity:
            api_abort(400, message="quantity or password of pay is required")
        if len(pay_password) != 6:
            api_abort(400, message="password of pay length is 6, {} given".format(len(pay_password)))
        id = int(args.get("id"))
        commodity = self.models.Commodity.get_or_none(self.models.Commodity.id == id)
        if not commodity:
            return self.utils.make_api_response(message="Illegal operation，please submit order again")
        coin_infos = self.models.Coin.select().where(self.models.Coin.name == commodity.price_unit)
        coin_id = int([c.id for c in coin_infos][0])
        prop_infos = self.models.Props.select().where(self.models.Props.id == commodity.prop)
        prop_amount = int([p.amount for p in prop_infos][0])
        if not verify_password(pay_password,user.pay_password):
            return self.utils.make_api_response(message="password of pay is error")
        # 判断商品库存是否还充足
        if not 0 < quantity <= prop_amount:
            return self.utils.make_api_response(message="Fill in the integers between 0 and {}, please".format(prop_amount))
        # 判断买家此货币的余额
        currentCoin = self.models.ShopCoin.get_or_none(
            self.models.ShopCoin.owner == user.id,
            self.models.ShopCoin.cate == coin_id)
        order_price = commodity.price * quantity
        if not currentCoin or currentCoin.amount < order_price: # 余额不足
            return self.utils.make_api_response(message = 'Sorry, your credit is running low')
        sellerCoin = self.models.ShopCoin.get_or_none(
            self.models.ShopCoin.owner == commodity.seller,
            self.models.ShopCoin.cate == coin_id)
        with db.database.atomic():
            if not sellerCoin:
                self.models.ShopCoin.create(
                    cate=coin_id,
                    owner=commodity.seller,
                    amount=order_price,
                    lock=Decimal(0).quantize(Decimal("0.00000000")))
            else:
                self.models.ShopCoin.update(amount=sellerCoin.amount + order_price).where(
                    self.models.ShopCoin.cate == coin_id,
                    self.models.ShopCoin.owner == commodity.seller).execute()
            self.models.Props.update(amount=prop_amount-quantity).where(self.models.Props.id == commodity.prop).execute()
            if quantity == prop_amount:
                self.models.Commodity.update(status=0,seller=user.id).where(self.models.Commodity.id == id).execute()
            else:
                self.models.Commodity.update(seller=user.id).where(self.models.Commodity.id == id).execute()
            self.models.ShopCoin.update(amount=currentCoin.amount-order_price).where(
                self.models.ShopCoin.owner==user.id,
                self.models.ShopCoin.cate==coin_id).execute()
            order = self.models.Order.create(
                buyer = user.id,
                amount = order_price,
                print_uint = commodity.price_unit
            )
            self.models.OrderDetail.create(
                order = order.id,
                commodity = commodity.id,
                price = commodity.price,
                quantity = quantity
            )
            self.data = {
                'user_id' : user.id,
                'order_id' : order.id
            }
            self.data = {
                "result" : "success"
            }
        return self.utils.make_api_response(data = self.data)



# 资产充值
class ApiRecharge(CommonResource):
    def __init__(self, **kwargs):
        super(ApiRecharge, self).__init__(**kwargs)
        self.parser = reqparse.RequestParser()
        # 表单验证提交的要充值的资产类型
        self.parser.add_argument("id", type=int, location='json', required=True)
        self.parser.add_argument("userId", type=str, location='json', required=True)

    def get(self):
        coin = self.models.Coin.select()
        coin_name = [c.name for c in coin]
        user = self.models.Users.select()
        eth_address = [u.eth_address for u in user]
        self.data = {
            "result" : "success",
            "coin" : coin_name,
            "eth_address" : eth_address
        }
        return self.utils.make_api_response(data=self.data)

    @api_login_required
    def post(self):
        args = self.parser.parse_args()
        coin_type_id = str(args['id'])
        user_id = args.get("userId")
        user = self.models.Users.get_or_none(self.models.Users.user_id == user_id)
        coin = self.models.Coin.get_or_none(self.models.Coin.id == coin_type_id)
        if not coin:
            return self.utils.make_api_response(message="Illegal operation，please submit order again")
        recharge = self.models.Recharge.get_or_none(
            self.models.Recharge.user == user.id,
            self.models.Recharge.status == 0
        )
        if recharge:
            self.data = {
                'recharge_id' : recharge.id
            }
            return self.utils.make_api_response(data = self.data)
        else:
            recharge = self.models.Recharge.create(
                value=0,
                receiver = user.eth_address.lower(),
                user=user.id,
                cate=coin_type_id
            )
            self.data = {'result':'success','recharge_id' : recharge.id }
            return self.utils.make_api_response(data=self.data)

    def get_recharge_status(self,rid):
        query = self.models.Recharge.get_or_none(self.models.Recharge.id == rid)
        if query:
            if query.status == 1:
                self.data = {'result':'success'}
                return self.utils.make_api_response(data=self.data)
            else:
                self.data = {'result':'pending'}
                return self.utils.make_api_response(data=self.data)
        else:
            self.data = {'result':'404'}
            return self.utils.make_api_response(data=self.data)


# 资产兑换
class ApiExchangeCoin(CommonResource):
    def __init__(self, **kwargs):
        super(ApiExchangeCoin, self).__init__(**kwargs)
        self.parser = reqparse.RequestParser()
        # 表单验证提交的要兑换的交易对
        self.parser.add_argument("id", type=int, location='json', required=True)
        self.parser.add_argument("method",type=str,location='json',required=True)
        self.parser.add_argument("amount",type=int,location='json',required=True)
        self.parser.add_argument("pay_password",type=str,location='json',required=True)
        self.parser.add_argument("userId", type=str, location='json', required=True)


    @api_login_required
    def post(self):
        args = self.parser.parse_args()
        pair_id = int(args['id'])
        exchange_method = str(args['method'])
        amount = int(args['amount'])
        pay_password = str(args['pay_password'])
        user_id = args.get("userId")
        user = self.models.Users.get_or_none(self.models.Users.user_id == user_id)
        exchange_pair = self.models.ExchangePair.get_or_none(self.models.ExchangePair.id == pair_id)
        if not pay_password or not amount:
            api_abort(400, message="The num of exchange and password of pay is required")
        if not exchange_pair or exchange_method not in ["买入", "卖出", "Buy", "Sell"]:
            api_abort(400,message='The information submitted is incorrect')
        try:
            price = requests.get(exchange_pair.query_api).json()["data"]["quotes"]["USD"]["price"]
        except Exception:
            return "exchange failed , please retry after a moment"
        else:
            current_exchange_price = (Decimal(0.1) / Decimal(price)).quantize(Decimal("0.00000000"))
            total = (current_exchange_price * amount).quantize(Decimal("0.00000000"))
            # 验证密码
            # if True:
            if len(pay_password) == 6 and verify_password(pay_password, user.pay_password):
                with db.database.atomic():
                    query = self.models.ShopCoin.select().where(self.models.ShopCoin.owner == user.id)
                    currency_coin = query.where(self.models.ShopCoin.cate == exchange_pair.currency.id).first()
                    token_coin = query.where(self.models.ShopCoin.cate == exchange_pair.token.id).first()

                    if exchange_method == "买入" or exchange_method == "Buy":
                        if not currency_coin or (currency_coin.amount - currency_coin.lock) < total:
                            return self.utils.make_api_response(
                                message="exchange failed, you have not enough balance about {} asset".format(exchange_pair.currency.name))
                        currency_coin.amount = currency_coin.amount - total
                        currency_coin.save()
                        if token_coin:
                            token_coin.amount = token_coin.amount + amount
                            token_coin.save()
                        else:
                            self.models.ShopCoin.create(
                                cate=exchange_pair.token.id,
                                owner=user.id,
                                lock=Decimal(0).quantize(Decimal("0.00000000")),
                                amount=amount
                            )
                    else:
                        if not token_coin or (token_coin.amount - token_coin.lock) < amount:
                            return self.utils.make_api_response(
                                messages = "exchange failed, you have not enough balance about {} asset".format(exchange_pair.token.name))
                        token_coin.amount = token_coin.amount - amount
                        token_coin.save()
                        if currency_coin:
                            currency_coin.amount = currency_coin.amount + total
                            currency_coin.save()
                        else:
                            self.models.ShopCoin.create(
                                cate=exchange_pair.currency.id,
                                owner=user.id,
                                lock=Decimal(0).quantize(Decimal("0.00000000")),
                                amount=total
                            )
                    exchange = self.models.Exchange.create(
                        user=user.id,
                        pair=exchange_pair.id,
                        quantity=amount,
                        price=current_exchange_price,
                        amount=total,
                        exchange_type=1 if exchange_method == "买入" or exchange_method == "Buy" else 2 )
                    self.data = {
                        'result' : 'success',
                        'echange_id' : exchange.id
                    }
                return self.utils.make_api_response(data=self.data)
            return self.utils.make_api_response(message="password of pay is error")

# 提币
class ApiTakeOut(CommonResource):
    def __init__(self, **kwargs):
        super(ApiTakeOut, self).__init__(**kwargs)
        self.parser = reqparse.RequestParser()
        # 表单验证提交的要兑换的交易对
        self.parser.add_argument("id", type=int, location='json', required=True)
        self.parser.add_argument("address", type=str, location='json', required=True)
        self.parser.add_argument("amount", type=int, location='json', required=True)
        self.parser.add_argument("pay_password", type=str, location='json', required=True)
        self.parser.add_argument("userId", type=str, location='json', required=True)

    def post(self):
        args = self.parser.parse_args()
        coin_id = args.get('id')
        address = args.get('address')
        amount = args.get('amount')
        pay_password = args.get('pay_password')
        user_id = args.get("userId")
        if not address or not amount or not pay_password:
            api_abort(400, message="The num and address of take out and password of pay is required")
        coin = self.models.Coin.get_or_none(self.models.Coin.id == coin_id)
        user = self.models.Users.get_or_none(self.models.Users.user_id == user_id)
        if not coin:
            return self.utils.make_api_response(message="Illegal operation，please submit order again")
        if len(pay_password) != 6 or not verify_password(pay_password,user.pay_password):
            return self.utils.make_api_response(message="password of pay is error")
        # 地址是由40位或者42位以0x开头的16进制字串组成的
        pat = re.compile('[A-Fa-f0-9]')
        result = []
        if len(address) == 40:
            result = pat.findall(address)
        elif len(address) == 42 and address.startswith('0x'):
            result = pat.findall(address[2:])
            # 随意添加两位即可(将上一步切片的0x再添加上)
            result.insert(0, 'x')
            result.insert(0, '0')
        else:
            return self.utils.make_api_response(message="please fill in the correct address.")
        if not len(result) == len(address):
            return self.utils.make_api_response(message="please fill in the correct address.")
        coin_infos = self.models.ShopCoin.get_or_none(
            self.models.ShopCoin.owner == user.id,
            self.models.ShopCoin.id == coin_id)
        if 0 < amount <= coin_infos.amount - coin_infos.lock:
            return self.utils.make_api_response(message="The amount of money is out of range")
        take_order = self.models.TakeOut.get_or_none(
            self.models.TakeOut.user == user.id,
            self.models.TakeOut.status == 1)
        if take_order:
            return self.utils.make_api_response(message="there are ongoing withdrawal orders")
        with db.database.atomic():
            self.models.TakeOut.create(
                sender=user.eth_address,
                receiver=address,
                value=amount,
                cate=coin_id,
                tx_id="0x",
                user=user.id,
            )
            self.models.ShopCoin.update(amount=coin_infos.lock+amount).where(
                self.models.ShopCoin.owner == user.id,
                self.models.ShopCoin.cate == coin_id).execute()
            self.data = {
                "result" : "success"
            }
        return self.utils.make_api_response(data=self.data)

# 分配
class ApiDistGame(CommonResource):
    def __init__(self, **kwargs):
        super(ApiDistGame, self).__init__(**kwargs)
        self.parser = reqparse.RequestParser()
        # 表单验证提交的信息
        self.parser.add_argument("id", type=int, location='json', required=True)
        self.parser.add_argument("game_id", type=str, location='json', required=True)
        self.parser.add_argument("amount", type=int, location='json', required=True)
        self.parser.add_argument("userId", type=str, location='json', required=True)

    def get(self):
        game_infos = self.models.GameType.select()
        game = []
        for g in game_infos:
            data = {}
            data["id"] = g.id
            data["name"] = g.name
            game.append(data)
        self.data = {
            "result" : "success",
            "game" : game
        }
        return self.utils.make_api_response(data=self.data)

    def post(self,**kwargs):
        args = self.parser.parse_args()
        coin_id = args.get("id")
        game_type = args.get("game_id")
        dist_amount = args.get("amount")
        user_id = args.get("userId")
        user = self.models.Users.get_or_none(self.models.Users.user_id == user_id)
        # print(coin_id,game_type,dist_amount)
        game = self.models.GameType.get_or_none(self.models.GameType.id == game_type)
        coin = self.models.Coin.get_or_none(self.models.Coin.id == coin_id)
        if not game or not coin:
            return self.utils.make_api_response(message="Illegal operation，please submit order again")
        if not dist_amount:
            api_abort(400, message="The num of distribution is required")
        user_coin = self.models.ShopCoin.get_or_none(
            self.models.ShopCoin.owner == user,
            self.models.ShopCoin.cate == coin_id)
        if not 0 < dist_amount < user_coin.amount - user_coin.lock:
            return self.utils.make_api_response(message="The amount of money is out of range")
        with db.database.atomic():
            self.models.ShopCoin.update(lock=user_coin.lock+dist_amount).where(
                self.models.ShopCoin.owner == user.id,
                self.models.ShopCoin.cate == coin_id).execute()
            self.data = {
                "result": "success"
            }
        return self.utils.make_api_response(data=self.data)

# 挂售
class ApiSellCommodity(CommonResource):
    def __init__(self, **kwargs):
        super(ApiSellCommodity, self).__init__(**kwargs)
        self.parser = reqparse.RequestParser()
        # 表单验证提交的信息
        self.parser.add_argument("id", type=int, location='json', required=True) # NFT资产的id
        self.parser.add_argument("pay_password", type=str, location='json', required=True)
        self.parser.add_argument("userId", type=str, location='json', required=True)

    def post(self):
        args = self.parser.parse_args()
        asset_id = args.get("id")
        pay_password = args.get("pay_password")
        user_id = args.get("userId")
        user = self.models.Users.get_or_none(self.models.Users.user_id == user_id)
        asset = self.models.Assets.get_or_none(self.models.Assets.id == asset_id)
        if not asset or asset.lock == True:
            return self.utils.make_api_response(message="Illegal operation，please submit order again")
        if  not pay_password:
            api_abort(400, message="The password of pay is required")
        if len(pay_password) != 6 or not verify_password(pay_password,user.pay_password):
            return self.utils.make_api_response(message="password of pay is error")
        with db.database.atomic():
            self.models.Assets.update(lock=True,visible=0).where(
                self.models.Assets.id == asset_id,
                self.models.Assets.cate == user.id).execute()
            self.models.Commodity.create(
                price = 1, # 暂定
                price_unit = 'tnc', # 暂定
                status = 1,
                platform = 2, # 暂挂c2c
                commodity_type = 1,
                asset = asset_id,
                seller = user.id
            )
            self.data = {
                "result": "success"
            }
            return self.utils.make_api_response(data=self.data)