from flask_login import current_user
from wtforms import DateField, IntegerField, StringField
from wtforms.validators import DataRequired, ValidationError

from app.libs.error_code import Forbidden
from app.models.oj import get_oj_by_oj_id
from app.validators.base import BaseForm as Form


class LoginForm(Form):
    username = StringField(validators=[DataRequired(message='用户名不能为空')])
    password = StringField(validators=[DataRequired(message='密码不能为空')])


class OJNameForm(Form):
    user_id = IntegerField(validators=[DataRequired(message='用户id不能为空')])
    oj_id = IntegerField(validators=[DataRequired(message='oj id不能为空')])
    username = StringField()

    def validate_user_id(self, value):
        if not current_user.permission and current_user.id != self.user_id.data:
            raise Forbidden()

    def validate_oj_id(self, value):
        if not get_oj_by_oj_id(self.oj_id.data):
            raise ValidationError('oj不存在')


class InquireForm(Form):
    user_id = IntegerField(validators=[DataRequired(message='用户id不能为空')])
    start_date = DateField()
    end_date = DateField()

    def validate_user_id(self, value):
        if not current_user.permission and current_user.id != self.user_id.data:
            raise Forbidden()


class RefreshForm(Form):
    user_id = IntegerField()

    def validate_user_id(self, value):
        if not current_user.permission and current_user.id != self.user_id.data:
            raise Forbidden()
