# -*- coding: utf-8 -*-
__author__ = 'xu'

import os
from functools import wraps
from flask import Flask, Blueprint, jsonify, url_for, abort, Response
from flask_peewee.db import Database
from flask_peewee.auth import Auth
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
from flask_login import  LoginManager
from celery import Celery

app = Flask(__name__)
APP_ENV = 'dev'
if not os.environ.get('APP_ENV') or os.environ.get('APP_ENV').lower() == 'dev':
    print('Running on Dev Env:')
    app.config.from_object('config')
elif os.environ.get('APP_ENV').lower() in ('prod', 'test'):
    print('Running on %s Env:' %os.environ['APP_ENV'].upper())
    app.config.from_object('config')
    app.config.from_object('config_' + os.environ['APP_ENV'].lower())
    APP_ENV = os.environ['APP_ENV'].lower()
else:
    print('Wrong Env!')
    exit(1)


app.config["APP_ENV"] = APP_ENV
if app.config['DEBUG']:
    app.jinja_env.globals['static'] = (
        lambda filename: url_for('static', filename=filename)
    )
else:
    app.jinja_env.globals['static'] = (
        lambda filename: url_for('static', filename=filename)
    )

# celery
if APP_ENV == "prod":
    celery = Celery(app.name, broker='redis://localhost:6379/1')
else:
    celery = Celery(app.name, broker='redis://localhost:6379/0')
#db
db = Database(app)
auth = Auth(app, db)
toolbar = DebugToolbarExtension(app)

#mail
mail = Mail(app)



from . import models, utils, views, subscribers
utils.create_tables()
utils.init_admin_user()

# register flask_restful apis
from flask_restful import Api
from .api import ApiReset, ApiRegister, ApiLogin, ApiAllowGames, ApiNftGetNew, \
ApiNftUpdate, ApiNftConsignment, ApiNftTransfer, ApiCoinTransfer, ApiProduceProps, ApiCoinExpend
from .nft_api import ApiShowCommodity,ApiExchangeClass,ApiMyhone,ApiRechargeRecords,\
ApiTakeOutRecords,ApiSellRecords,ApiOrderRecords,ApiExchangeRecords,ApiBuy,ApiRecharge,\
ApiExchangeCoin,ApiCommodityInfos,ApiTakeOut,ApiDistGame,ApiChangeCommodity

api_bp = Blueprint('api', __name__, url_prefix="/api")
api = Api(api_bp, default_mediatype='application/json')
nft_api_bp = Blueprint('nft_api',__name__,url_prefix="/nft_api")
nft_api = Api(nft_api_bp,default_mediatype='application/json')

resource_class_kwargs = {"models": models, "utils": utils}

api.add_resource(
    ApiNftConsignment,
    '/v1/nft/consignment',
    resource_class_kwargs=resource_class_kwargs
)
api.add_resource(
    ApiNftUpdate,
    '/v1/nft/update',
    resource_class_kwargs=resource_class_kwargs
)
api.add_resource(
    ApiNftGetNew,
    '/v1/nft/get/new',
    resource_class_kwargs=resource_class_kwargs
)
api.add_resource(
    ApiNftTransfer,
    '/v1/nft/transfer',
    resource_class_kwargs=resource_class_kwargs
)
api.add_resource(
    ApiCoinExpend,
    '/v1/erc20/expend',
    resource_class_kwargs=resource_class_kwargs
)
api.add_resource(
    ApiCoinTransfer,
    '/v1/erc20/transfer',
    resource_class_kwargs=resource_class_kwargs
)
api.add_resource(
    ApiProduceProps,
    '/v1/props/get/new',
    resource_class_kwargs=resource_class_kwargs
)
api.add_resource(
    ApiAllowGames,
    '/v1/allow_games/<int:asset_id>',
    resource_class_kwargs=resource_class_kwargs
)

api.add_resource(
    ApiLogin,
    '/v1/game/login',
    resource_class_kwargs=resource_class_kwargs
)

api.add_resource(
    ApiRegister,
    '/v1/game/register',
    resource_class_kwargs=resource_class_kwargs
)
app.register_blueprint(api_bp)
app.jinja_env.globals['url_for_page'] = utils.url_for_page

nft_api.add_resource(
    ApiShowCommodity,
    '/v1/api/show/commodity',
    resource_class_kwargs=resource_class_kwargs
)
nft_api.add_resource(
    ApiExchangeClass,
    '/v1/api/exchange/class',
    resource_class_kwargs=resource_class_kwargs
)
nft_api.add_resource(
    ApiMyhone,
    '/v1/api/my/home',
    resource_class_kwargs=resource_class_kwargs
)
nft_api.add_resource(
    ApiRechargeRecords,
    '/v1/api/recharge/records',
    resource_class_kwargs=resource_class_kwargs
)
nft_api.add_resource(
    ApiTakeOutRecords,
    '/v1/api/takeout/records',
    resource_class_kwargs=resource_class_kwargs
)
nft_api.add_resource(
    ApiSellRecords,
    '/v1/api/sell/records',
    resource_class_kwargs=resource_class_kwargs
)
nft_api.add_resource(
    ApiOrderRecords,
    '/v1/api/order/records',
    resource_class_kwargs=resource_class_kwargs
)
nft_api.add_resource(
    ApiExchangeRecords,
    '/v1/api/exchange/records',
    resource_class_kwargs=resource_class_kwargs
)
nft_api.add_resource(
    ApiBuy,
    '/v1/api/buy',
    resource_class_kwargs=resource_class_kwargs
)
nft_api.add_resource(
    ApiRecharge,
    '/v1/api/recharge',
    resource_class_kwargs=resource_class_kwargs
)
nft_api.add_resource(
    ApiExchangeCoin,
    '/v1/api/exchange/coin',
    resource_class_kwargs=resource_class_kwargs
)
nft_api.add_resource(
    ApiCommodityInfos,
    '/v1/api/commodity/infos',
    resource_class_kwargs=resource_class_kwargs
)
nft_api.add_resource(
    ApiTakeOut,
    '/v1/api/take/out',
    resource_class_kwargs=resource_class_kwargs
)
nft_api.add_resource(
    ApiDistGame,
    '/v1/api/dist/game',
    resource_class_kwargs=resource_class_kwargs
)
nft_api.add_resource(
    ApiChangeCommodity,
    '/v1/api/change/commodity',
    resource_class_kwargs=resource_class_kwargs
)

app.register_blueprint(nft_api_bp)
app.jinja_env.globals['url_for_page'] = utils.url_for_page
