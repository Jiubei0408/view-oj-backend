import datetime

from flask_login import current_user
from wtforms import DateField, IntegerField, StringField, FieldList
from wtforms.validators import DataRequired, ValidationError

from app.libs.error_code import Forbidden
from app.models.oj import get_oj_by_oj_id
from app.models.problem import get_problem_by_problem_id
from app.models.problem_set import get_problem_set_by_problem_id
from app.models.user import check_password, get_user_by_username
from app.validators.base import BaseForm as Form


class DateForm(Form):
    start_date = DateField()
    end_date = DateField()

    def validate_start_date(self, value):
        if self.start_date.data:
            self.start_date.data = datetime.datetime.strptime(self.start_date.data, '%Y-%m-%d').date()
        else:
            self.start_date.data = datetime.date.today() - datetime.timedelta(days=7)

    def validate_end_date(self, value):
        if self.end_date.data:
            self.end_date.data = datetime.datetime.strptime(self.end_date.data, '%Y-%m-%d').date()
        else:
            self.end_date.data = datetime.date.today()
        self.end_date.data += datetime.timedelta(days=1)


class UsernameForm(Form):
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])

    def validate_username(self, value):
        if not current_user.permission and current_user.username != self.username.data:
            raise Forbidden()
        if not get_user_by_username(self.username.data):
            raise ValidationError('Username does not exist')


class NoAuthUsernameForm(Form):
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])

    def validate_username(self, value):
        if not get_user_by_username(self.username.data):
            raise ValidationError('Username does not exist')


class OJIdForm(Form):
    oj_id = IntegerField(validators=[DataRequired(message='OJ id cannot be empty')])

    def validate_oj_id(self, value):
        if not get_oj_by_oj_id(self.oj_id.data):
            raise ValidationError('OJ does not exist')


class ProblemIdForm(Form):
    problem_id = IntegerField(validators=[DataRequired(message='Problem id cannot be empty')])

    def validate_problem_id(self, value):
        if not get_problem_by_problem_id(self.problem_id.data):
            raise ValidationError('Problem does not exist')


class ProblemSetIdForm(Form):
    problem_set_id = IntegerField(validators=[DataRequired(message='Problem set id cannot be empty')])

    def validate_problem_set_id(self, value):
        if not get_problem_set_by_problem_id(self.problem_set_id.data):
            raise ValidationError('Problem set does not exist')


class LoginForm(Form):
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])
    password = StringField(validators=[DataRequired(message='Password cannot be empty')])


class OJNameForm(UsernameForm, OJIdForm):
    oj_username = StringField()


class PageForm(Form):
    page = IntegerField(validators=[DataRequired(message='Page cannot be empty')])
    page_size = IntegerField(validators=[DataRequired(message='Page size cannot be empty')])

    def validate_page(self, value):
        if self.page.data <= 0:
            raise ValidationError('Page must >= 1')

    def validate_page_size(self, value):
        if self.page_size.data > 100:
            raise ValidationError('Page size must <= 100')


class ModifyPasswordForm(UsernameForm):
    old_password = StringField(validators=[DataRequired(message='Old password cannot be empty')])
    new_password = StringField(validators=[DataRequired(message='New password cannot be empty')])

    def validate_old_password(self, value):
        if not current_user.permission:
            if current_user.username != self.username.data:
                raise Forbidden()
            user = get_user_by_username(self.username.data)
            if not check_password(user, self.old_password.data):
                raise ValidationError('Old password wrong, please check again')


class CreateUserForm(Form):
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])
    nickname = StringField(validators=[DataRequired(message='Nickname cannot be empty')])

    def validate_username(self, value):
        if get_user_by_username(self.username.data):
            raise ValidationError('Username already exist')


class UserInfoForm(UsernameForm):
    nickname = StringField(validators=[DataRequired(message='Nickname cannot be empty')])
    permission = IntegerField()
    status = IntegerField()

    def validate_permission(self, value):
        if not current_user.permission:
            if self.permission.data != 0:
                raise Forbidden()


class ProblemSetNameForm(Form):
    problem_set_name = StringField(validators=[DataRequired(message='Problem set name cannot be empty')])


class ProblemSetInfoForm(ProblemSetNameForm):
    problem_id_list = FieldList(IntegerField(validators=[DataRequired(message='Problem id cannot be empty')]),
                                min_entries=1)


class ModifyProblemSetForm(ProblemSetIdForm, ProblemSetInfoForm):
    pass


class InquireForm(NoAuthUsernameForm, DateForm, PageForm):
    pass


class InquireCountForm(NoAuthUsernameForm, DateForm):
    pass


class RefreshAcceptProblemForm(NoAuthUsernameForm, OJIdForm):
    pass


class RefreshProblemRatingForm(ProblemIdForm):
    pass


class InquireProblemIdForm(OJIdForm):
    problem_pid = StringField(validators=[DataRequired(message='Problem pid cannot be empty')])
