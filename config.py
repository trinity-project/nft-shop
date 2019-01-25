# -*- coding: utf-8 -*-
__author__ = 'xu'

DATABASE = {
    'name': 'example.db',
    'engine': 'peewee.SqliteDatabase'
}

ADMIN_URL = "/asd/asd"
BRANDING = "asd"

DEBUG = True
DEBUG_TB_ENABLED = False

PER_PAGE=12
FORM_KEY_LEN = 100

# session config
# SESSION_PROTECTION = "strong"
SECRET_KEY = 'Your session secret key'
# when session is permanent 
SESSION_REFRESH_EACH_REQUEST = False
# SESSION_COOKIE_NAME = "fsid"
REMEMBER_COOKIE_DURATION = 3600*24*7
PERMANENT_SESSION_LIFETIME = 3600*24
'''
flask-security 配置选项
'''
# SECURITY_FLASH_MESSAGES 安全验证过程是否闪现flash消息 默认为 True
# SECURITY_TOKEN_AUTHENTICATION_KEY 指定使用令牌验证时需要读取的查询字符串参数 默认 auth_token
# SECURITY_TOKEN_AUTHENTICATION_HEADER 指定令牌验证需要读取的http头 默认 Authentication-Token 
# SECURITY_TOKEN_MAX_AGE 指定验证令牌过期时间(秒). 默认为 None,表示永不过期
# 指定哈希密码时所用的哈希算法 默认为 bcrypt
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
# 指定 HMAC 盐. 仅在密码hash类型设置为纯文本以外的类型时生效. 默认为 None.
SECURITY_PASSWORD_SALT = SECRET_KEY


# SECURITY_RECOVERABLE = True
# SECURITY_CHANGEABLE = True
# SECURITY_LOGIN_URL = "/$W4MuPXe4$844a685766c27a90e444"

# SECURITY_REGISTER_URL 指定注册URL 默认为  /register
# SECURITY_LOGOUT_URL 登出URL 默认为       /logout
# SECURITY_RESET_URL = "/reset"
# SECURITY_CHANGE_URL = "/change/password"
# SECURITY_CHANGE_URL 密码修改URL 默认为    /change
# SECURITY_CONFIRM_URL 邮箱验证URL 默认为   /confirm
# SECURITY_POST_LOGIN_VIEW 登录后默认跳转页面 默认为 / (url/endpoint)
# 注册
SECURITY_REGISTERABLE = True
# 忘记密码重置
SECURITY_RECOVERABLE = False
# 修改密码
SECURITY_CHANGEABLE = False

SECURITY_LOGIN_USER_TEMPLATE = "authorization/login.html"
SECURITY_REGISTER_USER_TEMPLATE = "authorization/register.html"
SECURITY_CHANGE_PASSWORD_TEMPLATE = "authorization/change_password.html"
SECURITY_FORGOT_PASSWORD_TEMPLATE = "authorization/reset_password.html"

# SECURITY_CONFIRMABLE = True
SECURITY_LOGIN_WITHOUT_CONFIRMATION = True
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_UNAUTHORIZED_VIEW = 'unauthorized'

## message
SECURITY_MSG_EMAIL_NOT_PROVIDED = ('邮箱别空着啊~', 'error')
SECURITY_MSG_PASSWORD_NOT_PROVIDED = ('怎么是空密码', 'error')
SECURITY_MSG_USER_DOES_NOT_EXIST = ('用户不存在', 'error')
SECURITY_MSG_DISABLED_ACCOUNT = ('这个用户被 BAN 了，请联系管理员', 'error')
SECURITY_MSG_EMAIL_ALREADY_ASSOCIATED =  ('已经关联过账号了.', 'error')
SECURITY_MSG_RETYPE_PASSWORD_MISMATCH = ('两次输入不一致', 'error')
SECURITY_MSG_INVALID_LOGIN_TOKEN = ('登录状态异常', 'error')
SECURITY_MSG_INVALID_EMAIL_ADDRESS = ('邮箱地址无效', 'error')
SECURITY_MSG_PASSWORD_INVALID_LENGTH = ('密码长度过短，最少6位哦', 'error')
SECURITY_MSG_PAY_PASSWORD_WITH_LENGTH_SIX = ('支付密码长度为6位', 'error')
SECURITY_MSG_INVALID_PASSWORD = ('密码不正确', 'error')
SECURITY_MSG_PASSWORDLESS_LOGIN_SUCCESSFUL = ('登陆成功.', 'success')
SECURITY_MSG_PASSWORD_RESET = ('密码重置成功，你已重新登陆', 'success')
SECURITY_MSG_LOGIN = ('请登录再查看本页面', 'info')
SECURITY_MSG_NICKNAME_HAVE_KEYWORDS = ('你的昵称含有敏感词汇','error')

#mail conf
# MAIL_SERVER = "smtp.ym.163.com"
MAIL_SERVER = "smtp.mxhichina.com"
# SECURITY_EMAIL_SENDER = "no-reply@aixunbang.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_DEBUG = False
MAIL_USERNAME = "no-reply@trinity.tech"
MAIL_PASSWORD = "Trinity123456"
MEMCACHE = ['127.0.0.1:11211']
SITEMAP_MAX_URL_COUNT = 2000

# db admin
ADMIN_USER = "lalala"
ADMIN_PASSWORD = "comeon"

# onchain conf
CHAIN_ENV = "test"
MONITOR_URL = "ws://47.104.81.20:9000/"
MONITOR_SIGN_SECRET = "Your sign secret"

# game api url
GAME_API_HOST = "Your game api"

WBA_CREATE_PK = "Your private key"
WBA_CREATE = "Your account address"