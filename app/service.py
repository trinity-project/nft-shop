#!/usr/bin/env python
# encoding: utf-8
"""
@author: Maiganne
@contact: xuyunqiao826@gmail.com
@time: 2017/6/16 16:36
"""

from flask_login import login_user,logout_user
from models import Shop,Users,Category,Trademark,TrademarkCategory




class FrontService(object):
    def __init__(self):
        pass

    @staticmethod
    def register(phone,password):
        register_user=Users.select().where(Users.phone==phone).first()
        if register_user:
            return {
                'code':101,
                'data':None,
                'message':u' 用户已存在'
            }
        else:
            new_user=Users.create(phone=phone,password=Users.hash_password(password))
            new_user.save()
        return {
            'code': 0,
            'data': None,
            'message': u'注册成功'
        }

    @staticmethod
    def login(phone,password):
        user=Users.select().where(Users.phone==phone).first()
        if not user:
            return {
                'code':102,
                'data':None,
                'message':u' 用户不存在'
            }
        else:
            if user.check_password(password):
                login_user(user)
                return {
                    'code': 0,
                    'data': None,
                    'message': u'登入成功'
                }
            else:
                return {
                    'code': 103,
                    'data': None,
                    'message': u'密码错误'
                }

    @staticmethod
    def logout_user():
        logout_user()
        return {
            'code': 0,
            'data': None,
            'message': u'登出成功'
        }

    @staticmethod
    def get_category_list():
        query=Category.select().where(Category.parent == None)
        return {
            'code': 0,
            'data': [
                {
                    'id': str(q.id),
                    'name': q.name,
                } for q in query],
            'message': u'正常'
        }

    @staticmethod
    def get_trademark_category_list():
        query = TrademarkCategory.select()
        return {
            'code': 0,
            'data': [
                {
                    'id': str(q.id),
                    'name': q.name,
                } for q in query],
            'message': u'正常'
        }

    # @staticmethod
    # def get_shopType_list():
    #     query=ShopType.select()
    #     return {
    #         'code': 0,
    #         'data': [
    #             {
    #                 'id': q.id,
    #                 'name': q.name,
    #             } for q in query],
    #         'message': u'正常'
    #     }

    @staticmethod
    def get_shop_list(shop_type=None,cat=None,price_range=None,trade_mark_style=None,region=None,\
        trade_mark_transfer=None, is_all_red=None, is_no_punishment=None, sort=None, page=1,per_page=5):
        price_ranges=[(0,3),(3,5),(5,10),(10,20),(20,30),(30,50),(50,1000)]
        shop_type_filter=Shop.shop_type==shop_type if shop_type else None
        price_filter=Shop.price.between(price_ranges[price_range][0],price_ranges[price_range][1])\
            if price_range in [0,1,2,3,4,5,6] else  None
        category_filter=Shop.category==cat if cat else  None
        region_filter=Shop.region==region if region else  None
        trade_mark_filter=Trademark.mark_type==trade_mark_style if trade_mark_style else  None
        trade_mark_transfer_filter = Trademark.transfer==trade_mark_transfer if trade_mark_transfer else None
        is_all_red_filter = Shop.is_all_red==True if is_all_red else None
        is_no_punishment_filter = Shop.is_no_punishment==True if is_no_punishment else None
        multi_filter=[]
        for i in [shop_type_filter,category_filter,price_filter,region_filter,trade_mark_filter,\
            trade_mark_transfer_filter,is_all_red_filter,is_no_punishment_filter]:
            if i:
                multi_filter.append(i)
        if multi_filter:
            if trade_mark_filter or trade_mark_transfer_filter:
                query = Shop.select().join(Trademark).where(*multi_filter)
            else:
                query = Shop.select().where(*multi_filter)
        else:
            query =Shop.select()
        # 排序
        if sort == 'time':
            query = query.order_by(Shop.level.desc(), Shop.created_datetime.desc())
        elif sort == 'price':
            query = query.order_by(Shop.price.asc(), Shop.level.desc())
        # 分页
        shops =query.paginate(page=page,paginate_by=per_page)
        return {
            'code': 0,
            'total_count':query.count(),
            'data': [q.get_display_data() for q in shops],
            'message': u'正常'
        }

    @staticmethod
    def get_shop(shop_uid):
        try:
            shop = Shop.get(uid=shop_uid)
            data = shop.get_display_data()
        except:
            data = None
        return data



