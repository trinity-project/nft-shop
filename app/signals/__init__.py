# -*- coding: utf-8 -*-
"""
signals for app
"""

from blinker import Namespace

signals = Namespace()

recharge_created = signals.signal("recharge_created")

takeout_created = signals.signal("takeout_created")

mintage_created = signals.signal("mintage_apply_success")

receive_notification_onchain = signals.signal("receive_notification_onchain")

user_disabled = signals.signal("user_disabled")