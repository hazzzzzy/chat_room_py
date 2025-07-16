from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

from apps.forms.baseForm import baseForm


class addUserForm(baseForm):
    # 登录账号
    username = StringField(
        label='用户名',
        validators=[
            DataRequired(message='用户名不能为空'),
            Length(min=3, max=10, message='用户名长度在3~10个字符')
        ]
    )
    # 登录密码
    password = StringField(
        label='登录密码',
        validators=[
            DataRequired(message='登录密码不能为空'),
            Length(min=6, max=20, message='登录密码长度在6~20个字符')
        ]
    )
    account = StringField(
        label='登录账号',
        validators=[
            DataRequired(message='登录账号不能为空'),
            Length(min=3, max=8, message='登录账号长度在3~8个字符')
        ]
    )


class editUserForm(baseForm):
    userID = IntegerField(
        label='用户ID',
        validators=[
            DataRequired(message='用户ID不能为空'),
            NumberRange(min=1, message='用户ID必须大于0')
        ]
    )
    # 登录账号
    username = StringField(
        label='用户名',
        validators=[
            DataRequired(message='用户名不能为空'),
            Length(min=3, max=10, message='用户名长度在3~10个字符')
        ]
    )
    # 登录密码
    password = StringField(
        label='登录密码',
        validators=[
            Optional(),
            Length(min=6, max=20, message='登录密码长度在6~20个字符')
        ]
    )


class banUserForm(baseForm):
    userID = IntegerField(
        label='用户ID',
        validators=[
            DataRequired(message='用户ID不能为空'),
            NumberRange(min=1, message='用户ID必须大于0')
        ]
    )
    status = IntegerField(
        label='用户状态',
        validators=[
            DataRequired(message='用户状态不能为空'),
            NumberRange(min=1, max=2, message='用户状态必须为1或2')
        ]
    )
