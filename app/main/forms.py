# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, EqualTo, Regexp
from ..models import User
from wtforms import ValidationError

class LoginForm(Form):
    email = StringField(u'邮箱', validators = [Required(), Length(1, 64), Email()])
    password = PasswordField(u'密码', validators = [Required()])
    remember_me = BooleanField(u'保持登录')
    submit = SubmitField(u'登录')

class RegistrationForm(Form):
    email = StringField(u'邮箱', validators = [Required(), Length(1, 64),
                Email()])
    username = StringField(u'用户名', validators = [Required(), Length(1, 64)])
    password = PasswordField(u'密码', validators = [Required(), Length(1, 64),
                EqualTo('password2', message = u"密码必须保持一致")])
    password2 = PasswordField(u'重复密码', validators = [Required()])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError(u'邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError(u'用户名已被使用')
