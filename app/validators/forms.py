from flask_login import current_user
from wtforms import BooleanField, IntegerField, StringField
from wtforms.validators import DataRequired, ValidationError

from app.validators.base import BaseForm as Form


class LoginForm(Form):
    username = StringField(validators=[DataRequired(message='用户名不能为空')])
    password = StringField(validators=[DataRequired(message='密码不能为空')])

