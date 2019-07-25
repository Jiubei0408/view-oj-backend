import datetime

from flask_login import current_user
from wtforms import DateField, IntegerField, StringField
from wtforms.validators import DataRequired, ValidationError

from app.libs.error_code import Forbidden
from app.models.oj import get_oj_by_oj_id
from app.validators.base import BaseForm as Form


class DateForm(Form):
    start_date = DateField()
    end_date = DateField()

    def validate_start_date(self, value):
        if self.start_date.data:
            self.start_date.data = datetime.datetime.strptime(self.start_date.data, '%Y-%m-%d')
        else:
            self.start_date.data = datetime.date.today() - datetime.timedelta(days=7)

    def validate_end_date(self, value):
        if self.end_date.data:
            self.end_date.data = datetime.datetime.strptime(self.end_date.data, '%Y-%m-%d')
        else:
            self.end_date.data = datetime.date.today()
        self.end_date.data += datetime.timedelta(days=1)


class UserIdForm(Form):
    user_id = IntegerField(validators=[DataRequired(message='User id cannot be empty')])

    def validate_user_id(self, value):
        if not current_user.permission and current_user.id != self.user_id.data:
            raise Forbidden()


class OJIdForm(Form):
    oj_id = IntegerField(validators=[DataRequired(message='OJ id cannot be empty')])

    def validate_oj_id(self, value):
        if not get_oj_by_oj_id(self.oj_id.data):
            raise ValidationError('OJ does not exist')


class LoginForm(Form):
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])
    password = StringField(validators=[DataRequired(message='Password cannot be empty')])


class OJNameForm(UserIdForm, OJIdForm):
    username = StringField()


class InquireForm(UserIdForm, DateForm):
    pass


class RefreshForm(UserIdForm, OJIdForm):
    pass


class ModifyPasswordForm(UserIdForm):
    password = StringField(validators=[DataRequired(message='Password cannot be empty')])


class CreateUserForm(Form):
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])
    nickname = StringField(validators=[DataRequired(message='Nickname cannot be empty')])
