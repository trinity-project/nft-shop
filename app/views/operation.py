# -*- coding: utf-8 -*-
import time,re
from app.signals import takeout_created
from decimal import Decimal
from flask import request,render_template,redirect,url_for,flash,abort, g, session
from flask_security import current_user,login_required
from ..models import Assets, ShopCoin,Commodity,TakeOut, Recharge,Coin, ExchangePair, Exchange,GameType
from .. import app, db
from ..utils import request_data_to_dict, wrap_template_name
from .. import types
from datetime import datetime
import requests
from flask_security.utils import verify_password, hash_password
from .message import message_infos as mi
from app.asynctasks import distribute_props_task,distribute_erc721_asset_task,distribute_erc20_asset_task

@app.route('/user/take_coin',methods=['POST'])
@login_required
def take_coin():
    try:
        data = request_data_to_dict()
        addr = data.get("coin_location").strip()
        pay_pwd = data.get('pay_pwd')
        page = data.get('page')
        coin_type = data.get('coin_type').strip()
        coin_id = int(data.get('coin_id'))
        take_num = abs(Decimal(data.get('coin_num')).quantize(Decimal("0.00000000")))
        if len(addr) != 42 or not addr.startswith('0x'):
            flash('表单输入错误 请检查', 'take-error')
            return redirect(url_for('my_home',page=page))
    except Exception:
        flash('表单输入错误 请检查', 'take-error')
        return redirect(url_for('my_home',page=page))
    if len(pay_pwd) != 6 or not verify_password(pay_pwd, current_user.pay_password):
        flash('支付密码错误', 'take-error')
        return redirect(url_for('my_home',page=page))
    coin_cate = Coin.get_or_none(Coin.name == coin_type)
    if not coin_cate:
        flash('资产类型找不到 请检查输入', 'take-error')
        return redirect(url_for('my_home',page=page))
    exist_take = TakeOut.get_or_none(
        TakeOut.user == current_user.get_id(),
        TakeOut.status == types.take_out_status["pending"]
    )
    if exist_take:
        flash('您有未完成的提币订单 请稍后重试', 'take-warn')
        return redirect(url_for('my_home',page=page))
    try:
        token = None
        asset = None
        with db.database.atomic():
            if coin_cate.name == "WBA":
                take_num = 1
                asset = Assets.get(id=coin_id)
                if asset.lock:
                    flash('资产锁定不可提出', 'take-error')
                    return redirect(url_for('my_home',page=page))
                asset.lock = True
                asset.save()
            else:
                token = ShopCoin.get(id=coin_id)
                available_num = token.amount - token.lock - token.take_lock
                if available_num < take_num:
                    flash('最多可提{}{}'.format(available_num, coin_cate.name), 'take-error')
                    return redirect(url_for('my_home',page=page))
                else:
                    token.take_lock = token.take_lock + take_num
                    token.save()
            take = TakeOut.create(
                sender="0x",
                receiver=addr,
                value=take_num,
                cate=coin_cate.id,
                tx_id="0x",
                user = current_user.get_id(),
            )
    except Exception:
        flash('提币申请失败 请检查输入', 'take-error')
        return redirect(url_for('my_home',page=page))
    else:
        flash('提币申请成功', 'take-success')
        if asset:
            from_addr = asset.owner.eth_address if asset.took else g.game_admin.eth_address
            pk = asset.owner.eth_key if asset.took else g.game_admin.eth_key
        else:
            from_addr = g.sys_admin.eth_address
            pk = g.sys_admin.eth_key
        data = {
            "token_id": asset.asset_id if asset else None,
            "asset_type": coin_cate.name,
            "value": str(take_num),
            "to_addr": addr,
            "from_addr": from_addr,
            "pk": pk,
            "take_id": take.id
        }
        takeout_created.send("app", **data)
        return redirect(url_for('user_takeout',page=page))

@app.route('/user/recharge/<int:rid>')
@login_required
def recharge_detail(rid):
    query = Recharge.get_or_none(Recharge.id == rid, Recharge.user == current_user.get_id())
    if not query: abort(404)
    return render_template(wrap_template_name('user/recharge_infos.html'),data=query)
    
@app.route('/user/sell_coin',methods=['POST'])
@login_required
def sell_coin():
    try:
        # 挂售只针对NFT资产，别的资产不会被挂售，每次挂售数量都是单位1
        data = request_data_to_dict()
        coin_id = int(data.get("coin_id"))
        coin_name = data.get('coin_name')
        pay_pwd = data.get('pay_pwd')
        page = data.get('page')
        price = abs(Decimal(data.get('sell_price')).quantize(Decimal("0.00000000")))
    except Exception as e:abort(400)
    else:
        asset = Assets.get_or_none(Assets.id == coin_id)
        if asset.lock:
            flash('资产锁定不可挂售', 'take-error')
            return redirect(url_for('my_home',page=page))
        query = Commodity.select().where(Commodity.asset == coin_id).count() # 被摆上过货架
        print(query)
        # 验证密码
        if len(pay_pwd) == 6 and verify_password(pay_pwd, current_user.pay_password):
            if query:
                with db.database.atomic():
                    # 如果有了挂售的定价标准，还得更新本次挂售的价格及价格单位
                    Commodity.update(
                        price=price,status=1,created_at=datetime.now(),platform=2,seller=current_user.get_id()
                    ).where(Commodity.asset == coin_id).execute()
                    Assets.update(lock=True, visible=0).where(Assets.id == coin_id).execute()
            else:
                with db.database.atomic():
                    c = Commodity.create(
                        name=coin_name.strip(),
                        status=1,
                        platform=2,
                        commodity_type=1,
                        price=price,
                        price_unit='WBT', # 暂定
                        asset=coin_id,
                        desc=asset.desc,
                        seller=current_user.get_id()
                    )
                    c.save()
                    Assets.update(lock=True, visible=0).where(Assets.id == coin_id).execute()
            messages = mi['sell-success'] if session.get('lang','en') == 'en' else mi['sell-success-zh']
            flash(messages, 'order-success')
            return redirect(url_for('user_sales'))
        messages = mi['pay-pwd-err'] if session.get('lang','en') == 'en' else mi['pay-pwd-err-zh']
        flash(messages, 'order-error')
        return redirect(url_for('my_home',page=page))

@app.route('/stopsell',methods=["POST"])
@login_required
def stop_sell():
    try:
        data = request_data_to_dict()
        page = data.get("page")
        asset_id = int(data.get("asste_id"))
        pay_pwd = data.get('pay_pwd')
        query = Commodity.select().where(Commodity.id == asset_id)
        asset = int([q.asset.id for q in query][0])
    except Exception as e:
        raise
    else:
        # 验证密码
        if len(pay_pwd) == 6 and verify_password(pay_pwd, current_user.pay_password):
            with db.database.atomic():
                Commodity.update(status=0).where(Commodity.id == asset_id).execute()
                Assets.update(lock=False,visible=1).where(Assets.id == asset).execute()
            messages = mi['stop-sell-success'] if session.get('lang','en') == 'en' else mi['stop-sell-success-zh']
            flash(messages, 'order-success')
            return redirect(url_for('user_sales',page=page))
        messages = mi['pay-pwd-err'] if session.get('lang','en') == 'en' else mi['pay-pwd-err-zh']
        flash(messages, 'order-error')
        return redirect(url_for('user_sales',page=page))

@app.route("/exchange", methods=["POST"])
@login_required
def exchange_token():
    try:
        data = request_data_to_dict()
        print(data)
        exchange_pair_id = int(data.get("exchange_pair"))
        exchange_type = data.get("exchange_type")
        pay_pwd = data.get('pay_pwd')
        # exchange_price = Decimal(data.get("price")).quantize(Decimal("0.00000000"))
        exchange_quantity = Decimal(data.get("quantity")).quantize(Decimal("0.00000000"))
        if exchange_quantity <= 0:abort(400)
        # exchange_amount = Decimal data.get("amount")
    except Exception as e:
        raise e
        abort(400)
    else:
        exchange_pair = ExchangePair.get_or_none(ExchangePair.id == exchange_pair_id)
        # if not exchange_pair or exchange_type not in ["买入", "卖出","Buy","Sell"]: abort(400)
        if not exchange_pair or exchange_type not in ["买入","Buy"]: abort(400)
        try:
            price = requests.get(exchange_pair.query_api).json()["data"]["quotes"]["USD"]["price"]
        except Exception:
            return "exchange failed , please retry after a moment"
        else:
            current_exchange_price = (Decimal(0.1) / Decimal(price)).quantize(Decimal("0.00000000"))
            # diff_price = abs(current_exchange_price - exchange_price)
            # if diff_price > Decimal(0.00000010)
            total = (current_exchange_price * exchange_quantity).quantize(Decimal("0.00000000"))
            # 验证密码
            if len(pay_pwd) == 6 and verify_password(pay_pwd, current_user.pay_password):
                with db.database.atomic():
                    query = ShopCoin.select().where(ShopCoin.owner == current_user.get_id())
                    currency_coin = query.where(ShopCoin.cate == exchange_pair.currency.id).first()
                    token_coin = query.where(ShopCoin.cate == exchange_pair.token.id).first()
                    if exchange_type == "买入" or exchange_type == "Buy":
                        if not currency_coin or (currency_coin.amount - currency_coin.lock) < total:
                            return "exchange failed, you have not enough balance about {} asset".format(exchange_pair.currency.name)
                        currency_coin.amount = currency_coin.amount - total
                        currency_coin.save()
                        if token_coin:
                            token_coin.amount = token_coin.amount + exchange_quantity
                            token_coin.save()
                        else:
                            ShopCoin.create(
                                cate = exchange_pair.token.id,
                                owner = current_user.get_id(),
                                lock = 0,
                                amount = exchange_quantity
                            )
                    # else:
                    #     if not token_coin or (token_coin.amount - token_coin.lock) < exchange_quantity:
                    #         return "exchange failed, you have not enough balance about {} asset".format(exchange_pair.token.name)
                    #     token_coin.amount = token_coin.amount - exchange_quantity
                    #     token_coin.save()
                    #     if currency_coin:
                    #         currency_coin.amount = currency_coin.amount + total
                    #         currency_coin.save()
                    #     else:
                    #         ShopCoin.create(
                    #             cate = exchange_pair.currency.id,
                    #             owner = current_user.get_id(),
                    #             lock = 0,
                    #             amount = total
                    #         )
                    Exchange.create(
                        user = current_user.get_id(),
                        pair = exchange_pair.id,
                        quantity = exchange_quantity,
                        price = current_exchange_price,
                        amount = total,
                        exchange_type = types.exchange_type["buy"] if exchange_type == "买入" or exchange_type == "Buy" else types.exchange_type["sell"]
                    )
                messages = mi['exchange-success'] if session.get('lang','en') == 'en' else mi['exchange-success-zh']
                flash(messages, 'exchange-success')
                return redirect(url_for("user_exchange"))
            messages = mi['pay-pwd-err'] if session.get('lang','en') == 'en' else mi['pay-pwd-err-zh']
            flash(messages, 'order-error')
            return redirect(url_for('my_home'))

@app.route("/user/distribution", methods=["POST"])
@login_required
def distribution():
    try:
        data = request_data_to_dict()
        page = data.get("page")
        coin_id = int(data.get("coin_id"))
        coin_name = data.get("asset")
        game_id = int(data.get("game_id"))
        game_name = data.get("game")
        amount = Decimal(data.get("amount")).quantize(Decimal("0.00000000"))
        asset_no = data.get("asset_id")
        game = GameType.get_or_none(GameType.id == game_id)
        game_appid = game.appid
        if game_name != game.name:
            messages = mi['opera-err'] if session.get('lang','en') == 'en' else mi['opera-errr-zh']
            flash(messages, 'order-error')
            return redirect(url_for('my_home', page=page))
    except Exception as e:abort(400)
    else:
        if asset_no == '-' and coin_name != 'WBA': # 所要分配的是ShopCoin的资产
            shopcoin = ShopCoin.get_or_none(ShopCoin.id == coin_id)
            if 0 < amount <= shopcoin.amount - shopcoin.lock - shopcoin.take_lock:
                with db.database.atomic():
                    # lock_num = Decimal(shopcoin.lock).quantize(Decimal("0.00000000"))
                    ShopCoin.update(lock=ShopCoin.lock + amount).where(ShopCoin.id == coin_id).execute()
                    data = {
                        "user_id" : current_user.user_id,
                        "amount" : amount,
                        "lock": shopcoin.lock + amount,
                        "asset_type" : coin_name,
                        "appid" : game_appid
                    }
                    distribute_erc20_asset_task.delay(data)
                    messages = mi['distr-success'] if session.get('lang','en') == 'en' else mi['distr-success-zh']
                    flash(messages, 'order-success')
                    return redirect(url_for('my_home', page=page))
            messages = mi['distr-err'] if session.get('lang','en') == 'en' else mi['distr-err-zh']
            flash(messages, 'order-error')
            return redirect(url_for('my_home', page=page))
        else: # 所要分配的是Assets的资产
            if amount == 1:
                with db.database.atomic():
                    Assets.update(lock=True,visible=0).where(Assets.id == coin_id).execute()
                    asset = Assets.get_or_none(Assets.id == coin_id)
                    data = {
                        "user_id" : current_user.user_id,
                        "id" : asset.asset_id,
                        "appid" : game_appid
                    }
                    distribute_erc721_asset_task.delay(data)
                    messages = mi['distr-success'] if session.get('lang','en') == 'en' else mi['distr-success-zh']
                    flash(messages, 'order-success')
                    return redirect(url_for('my_home', page=page))
            messages = mi['distr-err'] if session.get('lang','en') == 'en' else mi['distr-err-zh']
            flash(messages, 'order-error')
            return redirect(url_for('my_home', page=page))
