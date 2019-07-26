from flask import jsonify
from flask_login import current_user, login_required, login_user, logout_user

from app.libs.error_code import AuthFailed, Success, Forbidden
from app.libs.red_print import RedPrint
from app.models.oj_username import get_user_oj_username, modify_oj_username
from app.models.user import check_password, get_user_by_username, modify_password, create_user, get_all_user, \
    modify_user
from app.validators.forms import LoginForm, UserIdForm, OJNameForm, ModifyPasswordForm, CreateUserForm, UserInfoForm

api = RedPrint('user')


@api.route("/login", methods=['POST'])
def login_api():
    form = LoginForm().validate_for_api()
    username = form.username.data
    password = form.password.data
    user = get_user_by_username(username)
    if not user:
        raise AuthFailed('Username does not exist')
    if not check_password(user, password):
        raise AuthFailed('Wrong username or password')
    login_user(user, remember=True)
    return Success('Login successful')


@api.route("/logout", methods=['POST'])
def logout_api():
    logout_user()
    return Success('Logout successful')


@api.route("/get_user_info", methods=['POST'])
@login_required
def get_user_info_api():
    return jsonify({
        'code': 0,
        'data': {
            'id': current_user.id,
            'username': current_user.username,
            'nickname': current_user.nickname,
            'permission': current_user.permission
        }
    })


@api.route("/get_oj_username", methods=['POST'])
@login_required
def get_oj_username_api():
    form = UserIdForm().validate_for_api()
    res = get_user_oj_username(form.user_id.data)
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/modify_oj_username", methods=['POST'])
@login_required
def modify_oj_username_api():
    form = OJNameForm().validate_for_api()
    modify_oj_username(form.user_id.data, form.oj_id.data, form.username.data)
    return Success('Modify successful')


@api.route("/modify_password", methods=['POST'])
@login_required
def modify_password_api():
    form = ModifyPasswordForm().validate_for_api()
    modify_password(form.user_id.data, form.new_password.data)
    return Success('Modify successful')


@api.route("/create_user", methods=['POST'])
@login_required
def create_user_api():
    if not current_user.permission:
        raise Forbidden('Only administrators can operate')
    form = CreateUserForm().validate_for_api()
    create_user(form.username.data, form.nickname.data)
    return Success('Create successful')


@api.route("/get_user_list", methods=['POST'])
def get_user_list_api():
    res = get_all_user()
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/modify_user_info", methods=['POST'])
@login_required
def modify_user_info_api():
    form = UserInfoForm().validate_for_api()
    modify_user(form.user_id.data, form.nickname.data, form.permission.data, form.status.data)
    return Success('Modify successful')
