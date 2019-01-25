# -*- coding: utf-8 -*-
__author__ = 'xu'

from werkzeug.security import generate_password_hash,check_password_hash
from flask_peewee.admin import Admin, ModelAdmin
from flask_security import UserMixin, RoleMixin, PeeweeUserDatastore, Security
from flask_security.utils import hash_password as fl_hash_password
from peewee import TextField, BooleanField, DateTimeField, DateField,\
    ForeignKeyField, CharField, FloatField,IntegerField, DecimalField, BigIntegerField,\
    SmallIntegerField
from playhouse.signals import Signal
from hashlib import md5
import random, time, json
from datetime import datetime
from . import app,auth, db, types
from app.signals import user_disabled

before_save = Signal()
after_save = Signal()
per_page = 10

class SignalModel(db.Model):
    def save(self, *args, **kwargs):
        created = not bool(self.get_id())
        before_save.send(self, created=created)
        super(SignalModel, self).save(*args, **kwargs)
        after_save.send(self, created=created)


class Users(db.Model, UserMixin):
    # phone = CharField(unique=True, verbose_name="手机", null=True)
    email = CharField(unique=True, verbose_name="邮箱", index=True)
    password = CharField(verbose_name="密码")
    pay_password = CharField(verbose_name="支付密码", null=True)
    # name = CharField(null=True)
    # img = TextField(null=True)
    active = BooleanField(default=True)
    user_id = BigIntegerField(verbose_name="用户唯一编号", null=True, index=True)
    eth_address = CharField(verbose_name="用户充值以太坊钱包地址", null=True)
    eth_key = CharField(verbose_name="用户充值以太坊钱包私钥", null=True)
    private_address = CharField(verbose_name="用户私人太坊钱包地址", null=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(null=True)

    def __str__(self):
        return self.email

    def get_display_data(self):
        return {
            "email": self.email,
            "active": self.active,
            "wallet_address": self.wallet_address,
            "id": self.id,
            "user_id": self.user_id
        }

    def save(self, *args, **kwargs):
        super(Users, self).save(*args, **kwargs)
        if not self.active:
            user_disabled.send("app", uid=self.id)
        if not self.user_id:
            from .utils import create_eth_addr_key, get_app_logger
            self.user_id = (int(time.time()*10**3) << 22) + self.id
            eth_addr_key = create_eth_addr_key()
            self.pay_password = fl_hash_password(self.pay_password)
            if eth_addr_key:
                self.eth_address, self.eth_key = eth_addr_key
            self.save()

    @classmethod
    def get_user_by_email(cls, email):
        user = cls.get_or_none(cls.email == email)
        return user if user and user.active else None

    @classmethod
    def get_user_by_user_id(cls, user_id):
        user = cls.get_or_none(cls.user_id == user_id)
        if user and user.active: return user

    @classmethod
    def create_user(cls, **kwargs):
        user = cls.create(
            email = kwargs.get("email"),
            password = kwargs.get("password")
        )
        return user

    def check_password(self,password):
        return check_password_hash(self.password,password)

class UsersAdmin(ModelAdmin):

    def get_admin_name(self):
        return "用户记录"

    def get_display_name(self):
        return self.get_admin_name()


class Role(db.Model, RoleMixin):
    name = CharField(choices=(
        ('sys_admin', "系统管理员角色"),
        ('game_admin', "游戏管理员角色"))
        , verbose_name = "角色名")
    description = TextField(null=True)

    def __str__(self):
        return self.name

class RoleAdmin(ModelAdmin):

    def get_admin_name(self):
        return "用户角色"

    def get_display_name(self):
        return self.get_admin_name()

class UserRoles(db.Model):
    """
    记录用户与角色的映射关系
    """
    customer = ForeignKeyField(Users, related_name="roles")
    role = ForeignKeyField(Role, related_name="users")
    name = property(lambda self: self.role.name)

    def __str__(self):
        return "{}-{}".format(self.customer.email, self.role.name)

class UserRolesAdmin(ModelAdmin):

    def get_admin_name(self):
        return "用户-角色影射记录"

    def get_display_name(self):
        return self.get_admin_name()

class GameType(db.Model):
    """
    游戏种类 WOB WOT....
    """
    name = CharField(verbose_name="游戏名称", unique=True)
    token = CharField(verbose_name="代币名称", help_text="表示该游戏相关的商品售价单位")
    asset = CharField(verbose_name="资产名称", help_text="游戏角色资产对应erc721名称")
    appid = CharField(verbose_name="接口相关id", null=True)
    appsecret = CharField(verbose_name="接口相关密匙", null=True)
    npc_user_id = BigIntegerField(verbose_name="分配给游戏的npc用户", null=True)
    active = BooleanField(default=True, verbose_name="是否可用")
    created_at = DateTimeField(verbose_name="创建时间", default=datetime.now)

    def save(self, *args, **kwargs):
        super(GameType, self).save(*args, **kwargs)
        if not self.appsecret:
            print(datetime.now().strftime("%m%d%f"))
            self.appid = self.name + datetime.now().strftime("%m%d%f") + str(random.randint(10000, 99999))
            from .utils import hash_password
            print(type(self.appid))
            self.appsecret = hash_password(self.appid)
            user = Users.create_user(
                email="{0}@{1}.com".format(self.appid, self.name),
                password=fl_hash_password(self.appsecret[-10:])
            )
            self.npc_user_id = user.user_id
            self.save()

    def get_display_data(self):
        return {
            "name": self.name,
            "appid": self.appid,
            "token": self.token,
            "userid": self.npc_user_id,
            "appsecret": self.appsecret,
            "gameid": self.id
        }

    @classmethod
    def get_games_dict(cls):
        query = cls.select().where(GameType.active == True)
        games_dict = {}
        for q in query:
            game_dict = q.get_display_data()
            games_dict[game_dict["appid"]] = {
                "secret": game_dict["appsecret"],
                "name": game_dict["name"],
                "token": game_dict["token"],
                "userid": game_dict["userid"],
                "gameid": game_dict["gameid"],
                "appid": game_dict["appid"]
            }
        return games_dict

    def __str__(self):
        return self.name

class GameTypeAdmin(ModelAdmin):

    def get_admin_name(self):
        return "游戏类型记录"

    def get_display_name(self):
        return self.get_admin_name()

class Mintage(db.Model):
    """
    铸币记录
    """
    created_at = DateTimeField(verbose_name="铸币申请时间", default=datetime.now)
    complete_at = DateTimeField(null=True, verbose_name="铸币确认时间")
    text_ids = TextField(verbose_name="nft id 列表")
    user_id = BigIntegerField(verbose_name="铸币方用户编号")
    target_user = BigIntegerField(verbose_name="目标用户编号", null=True)
    tx_id = CharField(verbose_name="链上交易txID")
    gtx = CharField(verbose_name="游戏端铸币事务id")
    game = ForeignKeyField(GameType, verbose_name="铸币方")
    desc = TextField(verbose_name="ntf资产属性")
    status = SmallIntegerField(
        choices=((types.mintage_status["pending"], "进行中"), (types.mintage_status["complete"], "已完成")),
        default=types.mintage_status["pending"],
        index=True
    )
    def __str__(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")

class MintageAdmin(ModelAdmin):

    def get_admin_name(self):
        return "铸币记录"

    def get_display_name(self):
        return self.get_admin_name()

class Coin(db.Model):
    """
    记录商城支持的数字货币\n
    数字货币种类
    """
    name = CharField(verbose_name="数字货币名称")
    describe = TextField(verbose_name="数字货币描述")

    def __str__(self):
        return self.name

class CoinAdmin(ModelAdmin):

    def get_admin_name(self):
        return "资产类型记录"

    def get_display_name(self):
        return self.get_admin_name()

class Assets(db.Model):
    """
    虚拟资产,对应链上类似NFT资产\n
    具有不可分割、唯一性等特点
    """
    # asset_type = CharField(verbose_name="资产类型", default="NFT")
    cate = ForeignKeyField(Coin, verbose_name="货币种类")
    asset_id = CharField(verbose_name="nft资产链上唯一标识符")
    # role_name = CharField(verbose_name="角色名称", null=True)
    desc = TextField(verbose_name="游戏角色属性", null=True)
    lock = BooleanField(verbose_name="资产是否锁定", default=False)
    took = BooleanField(verbose_name="资产是否提出过", default=False)
    visible = SmallIntegerField(
        verbose_name="商城可见",
        choices=((types.visible_status["visible"], "商城可见"),(types.visible_status["invisible"], "商城不可见")),
        default=types.visible_status["visible"],
        help_text="""
        1 表示商城可见
        0 表示商城不可见,提出到钱包了
        """,
        index=True
    )
    status = SmallIntegerField(
        verbose_name="资产状态",
        choices=((types.nft_asset_status["alive"], "存活的"),(types.nft_asset_status["dead"], "销毁的")),
        default=types.nft_asset_status["alive"],
        help_text="""
        1 表示资产存活，可分配进游戏
        0 表示资产销毁，不可分配到游戏
        """,
        index=True
    )
    latest_game = CharField(verbose_name="当前所在游戏", null=True)
    owner = ForeignKeyField(Users, verbose_name="拥有者", related_name="assets")

    def parse_property(self):
        try:
            property_dict = json.loads(self.desc)
        except Exception:
            property_dict = {}
        if not isinstance(property_dict, dict):
            property_dict = {}
        return property_dict

    def __str__(self):
        return self.asset_id

    @classmethod
    def get_allow_games(cls, aid):
        query = GameAssets.select().where(GameAssets.asset == aid)
        return [q.game.id for q in query]

    @classmethod
    def dispatch_asset(cls, asset, user_id):
        """
        铸币完成后批量分发
        """
        #todo update asset owner
        pass

    @classmethod
    def destroy_asset(cls, asset_id):
        asset = cls.get_or_none(cls.asset_id == asset_id)
        if asset:
            asset.status = types.nft_asset_status["dead"]
            asset.save()
        return asset
    
    @classmethod
    def transfer_to_game(cls, asset_id, game_id):
        """
        用户选择商城资产分配到游戏
        """
        asset = cls.get_or_none(cls.id == asset_id)
        if not asset or not asset.status: return False
        if game_id not in cls.get_allow_games(asset_id): return False
        asset.visible = types.visible_status["invisible"]
        asset.save()
        return asset

class AssetsAdmin(ModelAdmin):
    columns = ['asset_id', 'visible', 'lock', 'status', 'owner']

    def get_admin_name(self):
        return "ERC721资产"

    def get_display_name(self):
        return self.get_admin_name()

class GameAssets(db.Model):
    """
    游戏与资产映射关系\n
    每个单位资产可以对应多个游戏\n
    实现资产跨游戏支持
    """
    asset = ForeignKeyField(Assets, verbose_name="nft资产")
    game = ForeignKeyField(GameType, verbose_name="游戏种类")
    role_id = CharField(verbose_name="nft资产对应游戏的ID")

class GameAssetsAdmin(ModelAdmin):
    columns = ['asset', 'game']

    def get_admin_name(self):
        return "游戏-ERC721资产映射记录"

    def get_display_name(self):
        return self.get_admin_name()
    
class ShopCoin(db.Model):
    """
    记录用户在商城拥有的数字货币
    """
    cate = ForeignKeyField(Coin, verbose_name="货币种类")
    owner = ForeignKeyField(Users, verbose_name="货币持有者")
    amount = DecimalField(verbose_name="货币数量", max_digits=30, decimal_places=8)
    lock = DecimalField(verbose_name="游戏锁定数量", max_digits=30, decimal_places=8, default=0)
    take_lock = DecimalField(verbose_name="提币锁定数量", max_digits=30, decimal_places=8, default=0)
    created_at = DateTimeField(verbose_name="创建于", default=datetime.now)
    updated_at = DateTimeField(null=True, verbose_name="更新于")

class ShopCoinAdmin(ModelAdmin):
    columns = ['cate', 'owner', 'amount', 'lock']

    def get_admin_name(self):
        return "ERC20资产"

    def get_display_name(self):
        return self.get_admin_name()

class Props(db.Model):
    """
    记录游戏中的道具
    """
    created_at = DateTimeField(verbose_name="创建于", default=datetime.now)
    name = CharField(verbose_name="名称")
    desc = TextField(verbose_name="描述")
    price = DecimalField(verbose_name="价格", max_digits=30, decimal_places=8)
    amount = IntegerField(verbose_name="数量")
    item_id = CharField(verbose_name="道具唯一编号", unique=True)
    owner = ForeignKeyField(Users, verbose_name="拥有者")

    # def save(self, *args, **kwargs):
    #     super(Props, self).save(*args, **kwargs)
    #     if not self.item_id:
    #         self.item_id = (int(time.time()*10**3) << 22) + self.id
    #         self.save()
    def __str__(self):
        return "{}-{}".format(self.name, self.item_id)

class PropsAdmin(ModelAdmin):
    columns = ['created_at', 'name', 'price', 'owner']

    def get_admin_name(self):
        return "道具记录"

    def get_display_name(self):
        return self.get_admin_name()

class Commodity(db.Model):
    """
    记录商品
    """
    name = CharField(verbose_name="商品名称", null=True)
    desc = TextField(verbose_name="商品描述", null=True)
    price = DecimalField(verbose_name="商品价格", max_digits=30, decimal_places=8)
    price_unit = CharField(verbose_name="商品价格单位")
    created_at = DateTimeField(verbose_name="创建时间", default=datetime.now)
    status = SmallIntegerField(
        verbose_name="商品状态",
        choices=((types.commodity_status["off_sale"], "下架"),(types.commodity_status["on_sale"], "上架")),
        default=types.commodity_status["on_sale"],
        index=True
    )
    platform = SmallIntegerField(
        verbose_name="挂售类型",
        choices=((types.platform["B2C"], "官方市场"),(types.platform["C2C"], "C2C市场")),
        default=types.platform["C2C"],
        index=True
    )
    commodity_type = SmallIntegerField(
        verbose_name="商品类型",
        choices=((types.commodity_type["nft"], "nft商品"),(types.commodity_type["prop"], "道具商品")),
        default=types.commodity_type["nft"]
    )
    level = IntegerField(verbose_name="商品热度指标", default=0)
    asset = ForeignKeyField(Assets, verbose_name="关联nft资产", null=True)
    prop = ForeignKeyField(Props, verbose_name="关联道具", null=True)
    game = ForeignKeyField(GameType, verbose_name="关联游戏", null=True)
    seller = ForeignKeyField(Users, verbose_name="商品卖家", null=True)

    def __str__(self):
        if self.commodity_type == types.commodity_type["nft"]:
            return "{}-{}".format(self.name, self.id)
        elif self.commodity_type == types.commodity_type["prop"]:
            return "{}-{}".format(self.name, self.id)

    def parse_property(self):
        try:
            property_dict = json.loads(self.desc)
        except Exception:
            property_dict = {}
        if not isinstance(property_dict, dict):
            property_dict = {}
        return property_dict

class CommodityAdmin(ModelAdmin):
    columns = ['created_at', 'name', 'seller', 'price', 'price_unit']

    def get_admin_name(self):
        return "商品记录"

    def get_display_name(self):
        return self.get_admin_name()

class Order(db.Model):
    """
    记录订单
    """
    order_no = BigIntegerField(verbose_name="订单编号", null=True)
    buyer = ForeignKeyField(Users, verbose_name="商品买家")
    amount = DecimalField(verbose_name="订单金额", max_digits=30, decimal_places=8)
    price_unit = CharField(verbose_name="商品价格单位")
    created_at = DateTimeField(verbose_name="创建时间", default=datetime.now)

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        if not self.order_no:
            self.order_no = (int(time.time()*10**3) << 22) + self.id
            self.save()

class OrderAdmin(ModelAdmin):
    columns = ['created_at', 'order_no', 'amount', 'price_unit']

    def get_admin_name(self):
        return "订单记录"

    def get_display_name(self):
        return self.get_admin_name()

class OrderDetail(db.Model):
    """
    订单快照
    """
    order = ForeignKeyField(Order, verbose_name="关联订单", related_name="details")
    created_at = DateTimeField(verbose_name="创建时间", default=datetime.now)
    commodity = ForeignKeyField(Commodity, verbose_name="关联商品")
    price = DecimalField(verbose_name="商品单价", max_digits=30, decimal_places=8)
    quantity = IntegerField(verbose_name="商品数量")

class OrderDetailAdmin(ModelAdmin):

    def get_admin_name(self):
        return "订单快照记录"

    def get_display_name(self):
        return self.get_admin_name()

class Recharge(db.Model):
    """
    充值记录
    """
    sender = CharField(verbose_name="付款地址", null=True)
    receiver = CharField(verbose_name="充值地址", null=True)
    value = DecimalField(verbose_name="充值数量", max_digits=30, decimal_places=8)
    cate = ForeignKeyField(Coin, verbose_name="货币种类")
    user = ForeignKeyField(Users, verbose_name="充值用户")
    created_at = DateTimeField(verbose_name="创建时间", default=datetime.now)
    complete_at = DateTimeField(null=True, verbose_name="确认时间")
    tx_id = CharField(verbose_name="链上交易txID", null=True)
    status = SmallIntegerField(
        verbose_name="充值状态",
        choices=((types.recharge_status["pending"], "确认中"),(types.recharge_status["complete"], "已完成")),
        default=types.recharge_status["pending"]
    )

class RechargeAdmin(ModelAdmin):
    columns = ['created_at', 'user', 'cate', 'value', 'tx_id']

    def get_admin_name(self):
        return "充值记录"

    def get_display_name(self):
        return self.get_admin_name()

class TakeOut(db.Model):
    """
    提币记录
    """
    sender = CharField(verbose_name="提币地址")
    receiver = CharField(verbose_name="接收地址")
    value = DecimalField(verbose_name="提币数量", max_digits=30, decimal_places=8)
    cate = ForeignKeyField(Coin, verbose_name="货币种类")
    user = ForeignKeyField(Users, verbose_name="提币用户")
    created_at = DateTimeField(verbose_name="申请时间", default=datetime.now)
    complete_at = DateTimeField(null=True, verbose_name="到账时间")
    tx_id = CharField(verbose_name="链上交易txID")
    status = SmallIntegerField(
        choices=((types.take_out_status["pending"], "进行中"), (types.take_out_status["complete"], "已完成")),
        default=types.take_out_status["pending"],
        index=True
    )

class TakeOutAdmin(ModelAdmin):
    columns = ['created_at', 'user', 'value', 'cate', 'complete_at', 'tx_id']

    def get_admin_name(self):
        return "提币记录"

    def get_display_name(self):
        return self.get_admin_name()

class ExchangePair(db.Model):
    """
    记录商城支持的交易对
    """
    token = ForeignKeyField(Coin, verbose_name="兑换代币")
    currency = ForeignKeyField(Coin, verbose_name="计价代币")
    query_api = CharField(verbose_name="价格查询接口")

    def __str__(self):
        return "{}/{}".format(self.token.name.upper(), self.currency.name.upper())

class ExchangePairAdmin(ModelAdmin):
    def get_admin_name(self):
        return "交易对"

    def get_display_name(self):
        return self.get_admin_name()

class Exchange(db.Model):
    """
    记录商城内代币兑换
    """
    user = ForeignKeyField(Users, verbose_name="用户")
    pair = ForeignKeyField(ExchangePair, verbose_name="交易对")
    quantity = DecimalField(verbose_name="兑换数量", max_digits=30, decimal_places=8)
    price = DecimalField(verbose_name="兑换单价", max_digits=30, decimal_places=8)
    amount = DecimalField(verbose_name="兑换总额", max_digits=30, decimal_places=8)
    exchange_type = SmallIntegerField(
        verbose_name="兑换类型",
        choices=((types.exchange_type["buy"], "买入"),(types.exchange_type["sell"], "卖出")),
    )
    created_at = DateTimeField(verbose_name="创建时间", default=datetime.now)

class ExchangeAdmin(ModelAdmin):
    columns = ['created_at', 'user', 'exchange_type', 'price', 'quantity', 'amount']
    def get_admin_name(self):
        return "兑换记录"

    def get_display_name(self):
        return self.get_admin_name()

class GameTransaction(db.Model):
    """
    游戏同步商城事务记录
    游戏发起的同步
    """
    game = ForeignKeyField(GameType, verbose_name="游戏类型")
    transaction_id = CharField(verbose_name="事务唯一编号")
    created_at = DateTimeField(verbose_name="创建时间", default=datetime.now)
    result = TextField(verbose_name="处理结果")
    desc = CharField(verbose_name="事务描述")
    status = SmallIntegerField(
        verbose_name="同步状态",
        choices=((types.sync_status["pending"], "确认中"),(types.sync_status["complete"], "完成")),
    )

class GameTransactionAdmin(ModelAdmin):
    columns = ['created_at', 'transaction_id', 'desc', 'result']

class MallTransaction(db.Model):
    """
    商城同步游戏事务记录
    商城发起的同步
    """
    transaction_id = CharField(verbose_name="事务唯一编号")
    created_at = DateTimeField(verbose_name="创建时间", default=datetime.now)
    sync_content = TextField(verbose_name="同步内容")
    sync_api = CharField(verbose_name="同步接口")
    status = SmallIntegerField(
        verbose_name="同步状态",
        choices=((types.sync_status["pending"], "确认中"),(types.sync_status["complete"], "完成")),
    )

class MallTransactionAdmin(ModelAdmin):
    columns = ['created_at', 'transaction_id', 'sync_content']

class Configuration(db.Model):
    """
    商城配置表
    """
    wbt_buy_price = IntegerField(verbose_name="wbt买入价格", help_text="USD")
    wbt_sell_price = IntegerField(verbose_name="wbt卖出价格", help_text="USD")



# Setup Flask-Security
class FixPeeweeUserDatastore(PeeweeUserDatastore):
    def get_user(self, identifier):
        try:
            return super(FixPeeweeUserDatastore, self).get_user(identifier)
        except self.user_model.DoesNotExist:
            print("user_model.DoesNotExist")
            pass

from .forms import LoginForm, RegisterForm
user_datastore = FixPeeweeUserDatastore(db, Users, Role, UserRoles)
# security = Security(app, user_datastore)
security = Security(
    app, 
    user_datastore,
    login_form=LoginForm,
    register_form=RegisterForm
)



# create admin object
admin = Admin(app, auth, prefix=app.config['ADMIN_URL'], branding=app.config['BRANDING'], )
admin.register(Users, UsersAdmin)
admin.register(Role, RoleAdmin)
admin.register(UserRoles, UserRolesAdmin)
admin.register(Recharge, RechargeAdmin)
admin.register(TakeOut, TakeOutAdmin)
admin.register(GameType, GameTypeAdmin)
admin.register(Assets, AssetsAdmin)
admin.register(Commodity, CommodityAdmin)
admin.register(Order, OrderAdmin)
admin.register(OrderDetail, OrderDetailAdmin)
admin.register(GameAssets, GameAssetsAdmin)
admin.register(Coin, CoinAdmin)
admin.register(ShopCoin, ShopCoinAdmin)
admin.register(Props, PropsAdmin)
admin.register(Mintage, MintageAdmin)
admin.register(ExchangePair, ExchangePairAdmin)
admin.register(Exchange, ExchangeAdmin)
admin.register(GameTransaction, GameTransactionAdmin)
admin.register(MallTransaction, MallTransactionAdmin)
auth.register_admin(admin)

admin.setup()
