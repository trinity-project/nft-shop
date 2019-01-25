# -*- coding: utf-8 -*-
__author__ = 'wog'
import sys
from app import app, APP_ENV
import logging

port = 8080
host = '127.0.0.1'

if APP_ENV == "prod":
    app.debug = False
    app.logger.setLevel(logging.INFO)
elif APP_ENV == "test":
    app.logger.setLevel(logging.DEBUG)
else:
    app.logger.setLevel(logging.DEBUG)
    host = "0.0.0.0"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port, debug=True)
    # from app.game_api import GameApi
    # GameApi.distribute_erc721_asset(
    #     "wob071913289742227",
    #     "6425605781151809538",
    #     id="asdfrt"
    # )
    # GameApi.distribute_props(
    #     "wob071913289742227",
    #     "6425605781151809538",
    #     item_count=3,
    #     item_id="kkdkfff"
    # )
    # GameApi.notify_mintage_complete(
    #     "wob071913289742227",
    #     "6425605781151809538",
    #     id="adfdvvv"
    # )