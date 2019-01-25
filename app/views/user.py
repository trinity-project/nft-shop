from config import PER_PAGE
from decimal import Decimal
from flask import request,render_template,redirect,url_for,flash,abort,session
from flask_security import current_user,login_required,url_for_security
from ..models import Assets, ShopCoin,Order,Commodity,TakeOut, Recharge,Coin, ExchangePair, Exchange,GameType
from .. import app
from ..utils import request_data_to_dict, wrap_template_name, Pagination
from .. import types
from app.signals import recharge_created
from .message import message_infos as mi

@app.route('/user/home')
@login_required
def my_home():
    curr_login_user = current_user.get_id()
    coin = Coin.select()
    game = GameType.select()
    pairs = ExchangePair.select()
    args = request.args
    page = int(args.get('page', '1')) if (args.get('page', '1')).isdigit() else 1
    query_coin = ShopCoin.select().where(
        ShopCoin.owner == curr_login_user
    ).order_by(ShopCoin.created_at.desc())
    query_assets = Assets.select().where(
        Assets.owner == curr_login_user
    ).order_by(Assets.id.desc())
    query_coin_count = query_coin.count()
    query_assets_count = query_assets.count()
    total_count = query_coin_count + query_assets_count
    pagination = Pagination(page, PER_PAGE, total_count)
    # print(dir(query_coin))
    # query_coin = query_coin.paginate(page=page,paginate_by=PER_PAGE)
    # query_assets = query_assets.paginate(page=page,paginate_by=PER_PAGE)
    data = [q for q in query_coin] + [q for q in  query_assets]
    data = data[(page - 1)* PER_PAGE : page*PER_PAGE]
    return render_template(wrap_template_name("user/home.html"), items=data,infos=coin,pairs=pairs, pagination=pagination,page=page,game=game)

@app.route('/user/recharge', methods=["GET", "POST"])
@login_required
def user_recharge():
    if request.method == "GET":
        query = Coin.select().dicts()
        coin = [q for q in query]
        pairs = ExchangePair.select()
        args = request.args
        page = int(args.get('page', '1')) if (args.get('page', '1')).isdigit() else 1
        query_recharge = Recharge.select().where(Recharge.user == current_user.get_id()).order_by(Recharge.created_at.desc())
        total_count = query_recharge.count()
        pagination = Pagination(page, PER_PAGE, total_count)
        query_recharge = query_recharge.paginate(page=page, paginate_by=PER_PAGE)
        return render_template(wrap_template_name("user/home.html"), records=query_recharge,infos=coin,pairs=pairs,pagination=pagination)
    elif request.method == "POST":
        try:
            data = request_data_to_dict()
            coin_type_id = int(data.get("type")[0])
        except Exception: abort(400)
        else:
            cate = Coin.get_or_none(Coin.id == coin_type_id)
            if not cate: abort(400)
            exist_recharge = Recharge.get_or_none(
                Recharge.user == current_user.get_id(),
                # Recharge.cate == coin_type_id,
                Recharge.status == types.recharge_status["pending"]
            )
            if exist_recharge:
                messages = mi['recharge-err'] if session.get('lang','en') == 'en' else mi['recharge-err-zh']
                flash(messages, 'recharge-error')
                # Recharge.update(value=amount).where(Recharge.id == rid).execute()
                return redirect(url_for('recharge_detail', rid=exist_recharge.id))
            else:
                recharge = Recharge.create(
                    value=0,
                    receiver = current_user.eth_address.lower(),
                    user=current_user.get_id(),
                    cate=coin_type_id
                )
                recharge_created.send("app", addr=recharge.user.eth_address)
                return redirect(url_for("recharge_detail", rid=recharge.id))

@app.route('/user/takeout')
@login_required
def user_takeout():
    query = Coin.select().dicts()
    coin = [q for q in query]
    pairs = ExchangePair.select()
    args = request.args
    page = int(args.get('page', '1')) if (args.get('page', '1')).isdigit() else 1
    query_takeout = TakeOut.select().where(TakeOut.user == current_user.get_id()).order_by(TakeOut.created_at.desc())
    total_count = query_takeout.count()
    pagination = Pagination(page, PER_PAGE, total_count)
    query_takeout = query_takeout.paginate(page=page, paginate_by=PER_PAGE)
    return render_template(wrap_template_name("user/home.html"),records=query_takeout,infos=coin,pairs=pairs,pagination=pagination)

@app.route('/user/sales')
@login_required
def user_sales():
    query = Coin.select().dicts()
    coin = [q for q in query]
    pairs = ExchangePair.select()
    args = request.args
    page = int(args.get('page', '1')) if (args.get('page', '1')).isdigit() else 1
    query_sellout = Commodity.select().where(Commodity.seller == current_user.get_id(),Commodity.asset != None).order_by(Commodity.created_at.desc())
    total_count = query_sellout.count()
    pagination = Pagination(page, PER_PAGE, total_count)
    query_sellout = query_sellout.paginate(page=page, paginate_by=PER_PAGE)
    return render_template(wrap_template_name("user/home.html"),infos=coin,records=query_sellout,pairs=pairs,pagination=pagination,page=page)

@app.route('/user/order')
@login_required
def user_order():
    query = Coin.select().dicts()
    coin = [q for q in query]
    pairs = ExchangePair.select()
    args = request.args
    page = int(args.get('page', '1')) if (args.get('page', '1')).isdigit() else 1
    query_order = Order.select().where(Order.buyer == current_user.get_id()).order_by(Order.created_at.desc())
    total_count = query_order.count()
    pagination = Pagination(page, PER_PAGE, total_count)
    query_order = query_order.paginate(page=page, paginate_by=PER_PAGE)
    return render_template(wrap_template_name("user/home.html"),data=query_order,infos=coin,pairs=pairs,pagination=pagination)

@app.route('/user/exchange')
@login_required
def user_exchange():
    query = Coin.select().dicts()
    coin = [q for q in query]
    pairs = ExchangePair.select()
    args = request.args
    page = int(args.get('page', '1')) if (args.get('page', '1')).isdigit() else 1
    query_exchange = Exchange.select().where(Exchange.user == current_user.get_id()).order_by(Exchange.created_at.desc())
    total_count = query_exchange.count()
    pagination = Pagination(page, PER_PAGE, total_count)
    query_exchange = query_exchange.paginate(page=page, paginate_by=PER_PAGE)
    return render_template(wrap_template_name("user/home.html"),infos=coin,records=query_exchange,pairs=pairs,pagination=pagination)
