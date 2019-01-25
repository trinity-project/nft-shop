# -*- coding: utf-8 -*-

import time,datetime
from decimal import Decimal
from flask import request,session,jsonify,render_template,redirect,url_for,g,flash,abort
from flask_security import current_user,login_required,url_for_security,logout_user
from ..models import Assets, ShopCoin,Users,Order,Commodity,OrderDetail,Coin,Props,Recharge, UserRoles,GameType
from .. import app, db
from ..utils import request_data_to_dict, wrap_template_name, Pagination, create_verify_code,\
reset_user_password,reset_user_pay_password, md5_args_sign_verify
from .. import types
from app.signals import receive_notification_onchain
from app.asynctasks import send_email_task, distribute_props_task
from ..forms import ResetForm,ResetPayForm
from flask_security.utils import verify_password, hash_password
from .message import message_infos as mi
from ..picture import Picture


PER_PAGE = app.config["PER_PAGE"]
# app.logger.debug('A value for debugging')
@app.before_request
def init_g():
    g.lang = session.get("lang", "en")
    sys_u_r = UserRoles.get_or_none(UserRoles.id == 1)
    game_u_r = UserRoles.get_or_none(UserRoles.id == 2)
    g.sys_admin = sys_u_r.customer if sys_u_r else None
    g.game_admin = game_u_r.customer if game_u_r else None

@app.route('/index')
def index():
    res = verify_password("qwerty", "$pbkdf2-sha512$25000$cE4pBeDce681xpjzXkvJGQ$.eJPgTbu4O8y1ssy8jz6eVHKXqNZreRYLwnW7Vmpjq4wTy5LeJ/AWoRcC0LrTWQAfJUAEbW3gLxMtCgvWThERg")
    print("验证码密码结果:", res)
    # res = ShopCoin.update(
    #     # lock=ShopCoin.lock + 5, 
    #     take_lock=ShopCoin.take_lock + 5
    # ).where(
    #     ShopCoin.id == 1,
    #     ShopCoin.amount - ShopCoin.lock - ShopCoin.take_lock >= 5
    # ).execute()
    # print("**********", res)
    return render_template(wrap_template_name("index.html"))

@app.route('/mintage_patch')
@login_required
def mintage_patch():
    if current_user.email != '2548927655@qq.com':
        abort(400)
    from app.models import Mintage
    ids = [28346333398889299259397505729, 28346333398889299259397505731, 28346333251315346669721092799,\
        28346333251315346669721092797, 28346333103741394080044679865, 28346333103741394080044679867,\
        28346332900827209269239612087, 28346332900827209269239612085, 28346330152262342286516421275,
        28346327809525844925403366030, 28346327016315849755892646540, 28346316409438007372900467280,\
        28346316188077078488385847886, 28346315911375917382742573642, 28346315634674756277099299400,\
        28346315247293130729198715462, 28346305931687373505875149323, 28346305599645980179103220226,\
        28346305341391563147169497599, 28346304880222961304430707197, 28346298128714630326734815686,\
        28346291672354204528391750043, 28346283666467276538446348657, 28346283666467276538446348659,\
        28346281600431940282976567634, 28346281600431940282976567632, 28346281600431940282976567622,\
        28346281600431940282976567630, 28346281600431940282976567616, 28346281600431940282976567628,\
        28346281600431940282976567618, 28346281600431940282976567624, 28346281600431940282976567626,\
        28346281600431940282976567620, 28346264334279487290836254977, 28346264334279487290836254975
        ]
    count = 0
    for aid in set(ids):
        aid = hex(aid)[2:]
        print(aid)
        if not Assets.get_or_none(Assets.asset_id == aid):
            mintage = Mintage.get_or_none(Mintage.text_ids == aid)
            user = Users.get_or_none(Users.user_id == mintage.target_user)
            asset = Assets.create(
                asset_id = aid,
                owner=user.id,
                cate=2,
                desc=mintage.desc
            )
            count = count + 1
    return str(count)


@app.route("/switch/lang")
def switch_lang():
    next_url = request.args.get("next", "/")
    lang = request.args.get("lang", "en")
    session["lang"] = lang
    return redirect(next_url)

@app.route("/monitor/transactions", methods=["POST"])
def accept_monitor_transactions():
    data = request_data_to_dict()
    # if not md5_args_sign_verify(data, app.config["MONITOR_SIGN_SECRET"]):
    #     return jsonify({"state": False, "message": "args sign not match"})
    receive_notification_onchain.send("app", **data)
    return jsonify({"state": True})

@app.route("/reset", methods=["GET", "POST"])
def reset():
    if not current_user.is_anonymous:
        logout_user()
    form = ResetForm()
    if form.validate_on_submit():
        reset_user_password(form.email.data,form.password.data)
        messages = mi['reset-pwd'] if session.get('lang','en') == 'en' else mi['reset-pwd-zh']
        flash(messages,'reset-success')
        return redirect(url_for_security('login'))
    return render_template("authorization/change_password.html",reset_form=form)

@app.route("/reset_pay", methods=["GET", "POST"])
def reset_pay():
    form = ResetPayForm()
    # print(form.validate_on_submit())
    if form.validate_on_submit():
        # print(form.validate_on_submit)
        reset_user_pay_password(form.email.data,form.pay_password.data)
        messages = mi['reset-pay-pwd'] if session.get('lang','en') == 'en' else mi['reset-pay-pwd-zh']
        flash(messages,'reset-success')
        return redirect(url_for('my_home'))
    return render_template("authorization/reset_pay_password.html",reset_form=form)

@app.route("/get/verify/code")
def get_verify_code():
    #todo 图片验证码验证
    image_code = request.args.get("image_code")
    email = request.args.get("email")
    print("image_code:{} email:{} session_image_code:{}".format(image_code.lower(), email, session.get("image_code")))
    if not email or "@" not in email:
        return jsonify({"result": "failed"})
    if image_code.lower() != session.get("image_code"):
        return jsonify({"result": "failed"})
    verify_code = create_verify_code()
    session["email_code"] = (verify_code, int(time.time()))
    # rev = "2548927655@qq.com"
    send_email_task.delay(email, verify_code)
    return jsonify({"result": "success"})

@app.route("/refresh/verify/code")
def refresh_verify_code():
    # 刷新图片验证码
    session["image_code"],img = Picture.generate_verify_image()
    # print(session["image_code"],img)
    return img

@app.route("/recharge/status/<int:rid>")
def get_recharge_status(rid):
    print(rid)
    # query = Recharge.select().where(Recharge.id == rid)
    # status = int([q.status for q in query][0])
    query = Recharge.get_or_none(Recharge.id == rid)
    if query:
        if query.status == 1:
            return jsonify({"result": "success"})
        else:
            return jsonify({"result":"pending"})
    else:
        return jsonify({"result":"404"})


@app.route('/faq')
def faq():
    return render_template(wrap_template_name("faq.html"))

@app.route('/guide')
def guide():
    return render_template(wrap_template_name("guide.html"))

@app.route('/')
# @app.route('/market')
def market():
    args = request.args
    page = int(args.get('page', '1')) if (args.get('page', '1')).isdigit() else 1
    num = int(args.get('num')) if (args.get('num', 'None')).isdigit() else PER_PAGE
    com_type = int(args.get('cate')) if (args.get('cate', 'None')).isdigit() else 0
    sort = args.get('sort') if (args.get('sort','None')) else 'date'
    print(sort)
    if sort == 'date' or sort == None:
        if com_type == 0:
            query_commodity = Commodity.select().where(Commodity.status == 1,Commodity.platform == 1).order_by(Commodity.created_at.desc())
        else:
            query_commodity = Commodity.select().where(Commodity.status == 1, Commodity.platform == 1,Commodity.commodity_type == com_type).order_by(Commodity.created_at.desc())
    else:
        if com_type == 0:
            query_commodity = Commodity.select().where(Commodity.status == 1,Commodity.platform == 1).order_by(Commodity.level.desc())
        else:
            query_commodity = Commodity.select().where(Commodity.status == 1, Commodity.platform == 1,Commodity.commodity_type == com_type).order_by(Commodity.level.desc())
    total_count = query_commodity.count()
    # num = 12 if num <= 12 else 24
    pagination = Pagination(page, num, total_count)
    query_commodity = query_commodity.paginate(page=page, paginate_by=num)
    time_now = int(datetime.datetime.now().strftime("%Y%m%d"))
    return render_template(wrap_template_name("market.html"),data=query_commodity,pagination=pagination,page=page,time=time_now,sort=sort,cate=com_type)

@app.route('/c2c_market')
def c2c_market():
    args = request.args
    page = int(args.get('page', '1')) if (args.get('page', '1')).isdigit() else 1
    num = int(args.get('num')) if (args.get('num', 'None')).isdigit() else PER_PAGE
    com_type = int(args.get('cate')) if (args.get('cate', 'None')).isdigit() else 0
    sort = args.get('sort') if (args.get('sort', 'None')) else 'date'
    if sort == 'date':
        if com_type == 0 or com_type == None:
            query_commodity = Commodity.select().where(Commodity.status == 1, Commodity.platform == 2).order_by(Commodity.created_at.desc())
        else:
            query_commodity = Commodity.select().where(Commodity.status == 1, Commodity.platform == 2,Commodity.commodity_type == com_type).order_by(Commodity.created_at.desc())
    else:
        if com_type == 0:
            query_commodity = Commodity.select().where(Commodity.status == 1, Commodity.platform == 2).order_by(Commodity.level.desc())
        else:
            query_commodity = Commodity.select().where(Commodity.status == 1, Commodity.platform == 2,Commodity.commodity_type == com_type).order_by(Commodity.level.desc())
    total_count = query_commodity.count()
    # num = 12 if num <= 12 else 24
    pagination = Pagination(page, num, total_count)
    query_commodity = query_commodity.paginate(page=page, paginate_by=num)
    time_now = int(datetime.datetime.now().strftime("%Y%m%d"))
    return render_template(wrap_template_name("c2c_market.html"), data=query_commodity, pagination=pagination,page=page,time=time_now,sort=sort,cate=com_type)

@app.route('/order/confirm', methods=["POST"])
@login_required
def order_confirm():
    try:
        data = request_data_to_dict()
        commodity_id = int(data.get("id")) # 商品在Commodity表中的id
        page = int(data.get("page"))
        pay_pwd = data.get('pay_pwd')
        quantity = int(data.get('quantity'))
        commodity = Commodity.get_or_none(Commodity.id == commodity_id)
        if not commodity:
            messages = mi['opera-err'] if session.get('lang','en') == 'en' else mi['opera-errr-zh']
            flash(messages, 'market-error')
            return redirect(url_for('market',page=page))
        com_type = commodity.commodity_type
        price_a = Decimal(commodity.price).quantize(Decimal("0.00000000"))
        coin_type = commodity.price_unit
        price = quantity * price_a
    except Exception as e:abort(400)
    else:
        #todo order check
        # 判断用户状态，是否激活
        active = Users.select().where(Users.id == current_user.get_id(),Users.active == True).count()
        if active:
            # 验证密码
            if len(pay_pwd) == 6 and verify_password(pay_pwd, current_user.pay_password):
                coin_infos = Coin.select().where(Coin.name == coin_type)  # 当前登录用户余额类型信息
                if coin_infos:
                    coin_id = int([c.id for c in coin_infos][0])
                    seller = int(commodity.seller.id) # 卖家信息
                    sellcoin = ShopCoin.select().where(ShopCoin.owner == seller,ShopCoin.cate == coin_id)
                    sellamount = [s.amount for s in sellcoin] # 卖家在ShopCoin中的资产数量
                    # 如果卖家未拥有过此类型的资产，就给此条数据--资产数量定义为0
                    if sellamount == []:
                        sellamount = [0]
                    sellamount = Decimal(sellamount[0]).quantize(Decimal("0.00000000"))
                    if seller == current_user.get_id(): # 不允许购买自己挂售的商品
                        messages = mi['buy-self'] if session.get('lang','en') == 'en' else mi['buy-self-zh']
                        flash(messages, 'c2c_market-warn')
                        return redirect(url_for('c2c_market',page=page))
                    shopcoin = ShopCoin.select().where(ShopCoin.owner == current_user.get_id(), ShopCoin.cate == coin_id)
                    amount = [s.amount for s in shopcoin] # 当前用户拥有此种资产的数量
                    lock = [s.lock for s in shopcoin] # 当前用户此种资产的锁定数量
                    if amount != []: # 当前用户拥有此种资产
                        # 判断用户余额是否大于商品价格
                        if amount[0] - lock[0] >= price:
                            prop_infos = commodity.prop  # 商品关联的道具
                            asset_infos = commodity.asset  # 商品关联的Asste资产
                            # 购买的是一个NFT商品
                            if com_type == 1:
                                if asset_infos == None: # 管理员添加商品时，误将nft商品未关联nft资产
                                    messages = mi['com-err'] if session.get('lang','en') == 'en' else mi['com-err-zh']
                                    flash(messages, 'market-warn')
                                    return redirect(url_for('market',page=page))
                                if quantity > 1: # ntf商品只以单位1形式存在
                                    messages = mi['num-err'] if session.get('lang','en') == 'en' else mi['num-err-zh']
                                    flash(messages, 'market-warn')
                                    return redirect(url_for('market', page=page))
                                asset_id = asset_infos.id
                                with db.database.atomic():
                                    # 如果卖家从未拥有过此种资产，创建一条新纪录
                                    if not sellcoin.count():
                                        ShopCoin.create(
                                            cate=coin_id,
                                            owner=seller,
                                            amount=Decimal(0).quantize(Decimal("0.00000000")),
                                            lock=Decimal(0).quantize(Decimal("0.00000000"))
                                        )
                                    # 给当前用户添加购买的NFT资产
                                    Assets.update(owner=current_user.get_id(),lock=False,visible=1).where(Assets.id == asset_id).execute()
                                    # 更新当前用户的资产数量(减少数量)
                                    ShopCoin.update(amount=amount[0]-price).where(ShopCoin.owner == current_user.get_id(),ShopCoin.cate == coin_id).execute()
                                    # 更新卖家用户的资产数量(增加数量)
                                    ShopCoin.update(amount=sellamount+price).where(ShopCoin.owner == seller,ShopCoin.cate == coin_id).execute()
                                    # 更改被购买商品的状态  --> 下架
                                    Commodity.update(status=types.commodity_status['off_sale']).where(Commodity.id == commodity_id).execute()
                                    # 订单信息入库
                                    order = Order.create(buyer=current_user.get_id(),amount=price,price_unit=coin_type)
                                    # 订单快照信息入库(订单详情)
                                    OrderDetail.insert(order=order.id,commodity=commodity_id,price=price_a,quantity=quantity).execute()
                            # 购买的是一个道具商品
                            elif com_type == 2:
                                if prop_infos == None: # 管理员添加商品时，误将道具商品未关联道具资产
                                    messages = mi['com-err'] if session.get('lang','en') == 'en' else mi['com-err-zh']
                                    flash(messages, 'market-warn')
                                    return redirect(url_for('market',page=page))
                                prop_num = prop_infos.amount
                                if quantity > prop_num: # 购买数量超出prop商品库存
                                    messages = mi['num-warn'] if session.get('lang','en') == 'en' else mi['num-warn-zh']
                                    flash(messages, 'market-warn')
                                    return redirect(url_for('market', page=page))
                                prop_id = prop_infos.id
                                with db.database.atomic():
                                    sellcoin = ShopCoin.select().where(ShopCoin.owner == seller,ShopCoin.cate == coin_id).count()
                                    # 如果卖家从未拥有过此种资产，创建一条新纪录
                                    if not sellcoin:
                                        ShopCoin.create(
                                            cate=coin_id,
                                            owner=seller,
                                            amount=Decimal(0).quantize(Decimal("0.00000000")),
                                            lock=Decimal(0).quantize(Decimal("0.00000000"))
                                        )
                                    else:
                                        # 更新卖家用户的资产数量(增加数量)
                                        ShopCoin.update(amount=sellamount+price).where(ShopCoin.owner == seller,ShopCoin.cate == coin_id).execute()
                                    # 更新当前用户的资产数量(减少数量)
                                    ShopCoin.update(amount=amount[0]-price).where(ShopCoin.owner == current_user.get_id(),ShopCoin.cate == coin_id).execute()
                                    # 修改该道具商品的拥有者 暂无道具信息相关标准
                                    Props.update(owner=current_user.get_id(),amount=prop_num-quantity).where(Props.id == prop_id).execute()
                                    # 订单信息入库
                                    order = Order.create(buyer=current_user.get_id(),amount=price,price_unit=coin_type)
                                    # 订单快照信息入库(订单详情)
                                    OrderDetail.insert(order=order.id,commodity=commodity_id,price=price_a,quantity=quantity).execute()
                                    prop_query = Props.select().where(Props.id == prop_id)
                                    prop_amount = int([p.amount for p in prop_query][0])
                                    if prop_amount == 0:
                                        # 更改被购买商品的状态  --> 下架
                                        Commodity.update(status=types.commodity_status['off_sale']).where(Commodity.prop == prop_id).execute()
                                    prop = Props.get_or_none(Props.id == commodity.prop.id)
                                    item_id = prop.item_id
                                    gametype = GameType.get_or_none(GameType.id == commodity.game.id)
                                    appid = gametype.appid
                                    # print(item_id,item_count,appid)
                                    data = {
                                        "user_id": current_user.user_id,
                                        "item_count": quantity,
                                        "item_id": item_id,
                                        "appid": appid
                                    }
                                    distribute_props_task.delay(data)
                            messages = mi['buy-success'] if session.get('lang','en') == 'en' else mi['buy-success-zh']
                            flash(messages, 'user_order-success')
                            return redirect(url_for('user_order'))
                messages = mi['money'] if session.get('lang','en') == 'en' else mi['money-zh']
                flash(messages,'order-warn')
                return redirect(url_for('my_home'))
            messages = mi['pay-pwd-err'] if session.get('lang','en') == 'en' else mi['pay-pwd-err-zh']
            flash(messages, 'market-error')
            return redirect(url_for('market', page=page))
        messages = mi['user-err'] if session.get('lang','en') == 'en' else mi['user-errr-zh']
        flash(messages,'market-error')
        return redirect(url_for('market',page=page))
