# -*- coding: utf-8 -*-
__author__ = 'xu'

import inspect,time
from datetime import date
from flask import request, current_app, session, flash, g
from flask_wtf import FlaskForm
from wtforms import validators, widgets, SelectMultipleField, SelectMultipleField,\
    TextAreaField, StringField, PasswordField
from wtforms.validators import ValidationError, StopValidation
from flask_security.forms import LoginForm as FS_LoginForm
from flask_security.forms import RegisterForm as FS_RegisterForm
from flask_security.forms import ValidatorMixin
from flask_security.utils import get_config, get_message
import flask_security
from werkzeug.local import LocalProxy
from .utils import create_verify_code
from .picture import Picture

_datastore = LocalProxy(lambda: current_app.extensions['security'].datastore)

def fix_config_value(key, app=None, default=None):
    app = app or current_app
    if key.startswith("MSG_"):
        # print("fix_config_value", key, g.lang)
        if g.lang == "cn":
            return get_config(app).get(key.upper(), default)
        else:
            # print("kkkkdkkkkkkkkkkkk")
            msg = " ".join(key.split("_")[1:])
            return (msg.lower(), get_config(app).get(key.upper(), default)[1])
    else:
        return get_config(app).get(key.upper(), default)

flask_security.utils.config_value = fix_config_value

"""扩展wtforms内建验证器"""
class EqualTo(ValidatorMixin, validators.EqualTo):
    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if field.data != other.data:
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
            }
            message = get_message(self.message)[0]
            raise ValidationError(message % d)

class Required(ValidatorMixin, validators.InputRequired):
    pass
class Length(ValidatorMixin, validators.Length):
    def __call__(self, form, field):
        l = field.data and len(field.data) or 0
        if l < self.min or self.max != -1 and l > self.max:
            message = get_message(self.message)[0]
            raise ValidationError(message % dict(min=self.min, max=self.max, length=l))

class Regexp(ValidatorMixin, validators.Regexp):
    pass

class Email(ValidatorMixin, validators.Email):
    def __call__(self, form, field):
        # super(Email, self).__call__(form, field)
        value = field.data
        message =  get_message(self.message)[0]

        if not value or '@' not in value:
            raise StopValidation(message)

        user_part, domain_part = value.rsplit('@', 1)
        if not self.user_regex.match(user_part):
            raise StopValidation(message)

        if not self.validate_hostname(domain_part):
            raise StopValidation(message)

"""验证器实例"""
email_validator = Email(message='INVALID_EMAIL_ADDRESS')
email_required = Required(message='EMAIL_NOT_PROVIDED')
common_required = Required(message=u"这是必填项")
username_required = Required(message=u'用户名不能为空')
username_length = Length(min=3, max=16, message=u"用户名长度须在3~16个字符内")
phone_required = Required(message=u'手机号码不能为空')
image_code_required = Required(message=u"图片验证码不能为空")
sms_code_required = Required(message=u"短信验证码不能为空")
phone_validator = Regexp(r'^1[3|5|7|8][0-9]\d{8}$', message=u"手机号码格式错误")
password_required = Required(message=u"密码不能为空")
password_confirm_required = Required(message=u"确认密码不能为空")
password_length = Length(min=6, max=128, message='PASSWORD_INVALID_LENGTH')
pay_password_length = Length(min=6, max=6, message='PAY_PASSWORD_WITH_LENGTH_SIX')
password_confirm_validator = EqualTo('password', message=u"两次输入密码不相同")
pay_password_confirm_validator = EqualTo('pay_password', message=u"两次输入密码不相同")

"""自定义验证(器)函数"""
def unique_user_phone(form, field):
    user = _datastore.find_user(phone=field.data)
    if user is not None:
        if user.is_active():
            raise ValidationError(u"该手机号码已经被注册")
        else:
            user.delete_instance()
def unique_user_name(form, field):
    user = _datastore.find_user(username=field.data)
    if user is not None:
        if user.is_active():
            raise ValidationError(u"该用户名已经被注册")
        else:
            user.delete_instance()
            
def custom_required(form, field):
    if not field.data:
        raise StopValidation(u"这是必填项")

def unique_user_email(form, field):
    print("进入邮箱唯一性验证")
    if _datastore.find_user(email=field.data) is not None:
        msg = get_message('EMAIL_ALREADY_ASSOCIATED', email=field.data)[0]
        raise ValidationError(msg)

def verify_image_code(form, field):
    print(field.data.lower(), session.get("image_code"))
    message = "图片验证码错误" if session.get("lang") == "cn" else "invalid image verification code"
    if field.data.lower() != session.get("image_code"):
        raise StopValidation(message)

def verify_email_code(form, field):
    print(field.data.lower(), session.get("email_code"))
    message = "邮件验证码错误" if session.get("lang") == "cn" else "invalid email verify code"
    session_email_code = session.get("email_code")
    if session_email_code is None:
        raise StopValidation(message)
    email_code, timestamp = session_email_code
    if field.data.lower() != email_code or (time.time() - timestamp) > 5 * 60:
        raise StopValidation(message)

class MultiCheckboxField(SelectMultipleField):
    """
    继承自SelectMultipleField\n
    修改SelectMultipleField默认widget(字段对应的html元素)
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

# 登录表单
class LoginForm(FS_LoginForm):
    email = StringField(
        'email', 
        validators=[email_required, email_validator]
    )
    image_code = StringField('image_code', validators=[image_code_required, verify_image_code])

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        # psot 请求时 必须要验证完毕 才能重新生成验证码
        if request.method == "GET":
            self.generate_image_code()

    def generate_image_code(self):
        session["image_code"], self.img = Picture.generate_verify_image()

    def validate(self):
        if not super(LoginForm, self).validate():
            self.generate_image_code()
            return False
        return True

# 注册表单
class RegisterForm(FS_RegisterForm):
    email = StringField(
        'email', 
        validators=[email_required, email_validator, unique_user_email]
    )
    password = PasswordField(
        'password',
        validators=[password_required, password_length])
    password_confirm = PasswordField(
        'retype_password',
        validators=[EqualTo('password', message='RETYPE_PASSWORD_MISMATCH'),
                    password_required])
    pay_password = PasswordField("pay_password", validators=[password_required, pay_password_length])
    image_code = StringField('image_code', validators=[image_code_required, verify_image_code])
    email_code = StringField('email_code', validators=[sms_code_required, verify_email_code])

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # psot 请求时 必须要验证完毕 才能重新生成验证码
        if request.method == "GET":
            self.generate_image_code()
        # 生成验证码

    def generate_image_code(self):
        session["image_code"], self.img = Picture.generate_verify_image()

    def validate(self):
        is_verified = True
        if not super(RegisterForm, self).validate(): is_verified = False
        if not is_verified: self.generate_image_code()
        return is_verified

# 重置表单
class ResetForm(FlaskForm):
    email = StringField(
        'email', 
        validators=[email_required, email_validator]
    )
    password = PasswordField("password", validators=[password_required, password_length])
    password_confirm = PasswordField(
        'retype_password',
        validators=[EqualTo('password', message='RETYPE_PASSWORD_MISMATCH'),password_required]
    )
    image_code = StringField('image_code', validators=[image_code_required, verify_image_code])
    email_code = StringField('email_code', validators=[sms_code_required, verify_email_code])

    def __init__(self, *args, **kwargs):
        super(ResetForm, self).__init__(*args, **kwargs)
        if request.method == "GET":
            self.generate_image_code()

    def generate_image_code(self):
        session["image_code"], self.img = Picture.generate_verify_image()

    def validate(self):
        is_verified = True
        if not super(ResetForm, self).validate(): is_verified = False
        user = _datastore.find_user(email=self.email.data)
        if user is None:
            self.email.errors.append(get_message("USER_DOES_NOT_EXIST")[0])
            is_verified = False
        if not is_verified: self.generate_image_code()
        return is_verified

# 重置支付表单
class ResetPayForm(FlaskForm):
    email = StringField(
        'email',
        validators=[email_required, email_validator]
    )
    pay_password = PasswordField("pay_password", validators=[password_required, pay_password_length])
    pay_password_confirm = PasswordField(
        'retype_pay_password',
        validators=[EqualTo('pay_password', message='RETYPE_PASSWORD_MISMATCH'),password_required]
    )
    image_code = StringField('image_code', validators=[image_code_required, verify_image_code])
    email_code = StringField('email_code', validators=[sms_code_required, verify_email_code])

    def __init__(self, *args, **kwargs):
        super(ResetPayForm, self).__init__(*args, **kwargs)
        if request.method == "GET":
            self.generate_image_code()

    def generate_image_code(self):
        session["image_code"], self.img = Picture.generate_verify_image()

    def validate(self):
        is_verified = True
        if not super(ResetPayForm, self).validate(): is_verified = False
        user = _datastore.find_user(email=self.email.data)
        if user is None:
            self.email.errors.append(get_message("USER_DOES_NOT_EXIST")[0])
            is_verified = False
        if not is_verified: self.generate_image_code()
        return is_verified

class SellForm(FlaskForm):
    username = StringField(u"姓名", validators=[username_required, username_length])
    phone = StringField(u"手机", validators=[phone_required, phone_validator])
    link = TextAreaField(u"店铺网址", validators=[common_required])
    def validate(self):
        return super(SellForm, self).validate()

class ResourceForm(FlaskForm):
    name = StringField(u"店铺名称", validators=[common_required])
    contact = StringField(u"联系方式", validators=[common_required])
    def validate(self):
        return super(ResourceForm, self).validate()

class SearchForm(FlaskForm):
    name = StringField(u"店铺名称", validators=[common_required])
    def validate(self):
        return super(SearchForm, self).validate()

