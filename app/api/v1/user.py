from flask import jsonify
from flask_login import current_user, login_required, login_user, logout_user

from app.libs.error_code import AuthFailed, Success
from app.libs.red_print import RedPrint
from app.models.oj_username import modify_oj_username
from app.models.user import check_password, get_user_by_username
from app.validators.forms import LoginForm, OJNameForm

api = RedPrint('user')


@api.route("/login", methods=['POST'])
def login_api():
    form = LoginForm().validate_for_api()
    username = form.username.data
    password = form.password.data
    user = get_user_by_username(username)
    if not user:
        raise AuthFailed('用户名不存在')
    if not check_password(user, password):
        raise AuthFailed('用户名或密码错误')
    login_user(user, remember=True)
    return Success('登录成功')


@api.route("/logout", methods=['POST'])
def logout_api():
    logout_user()
    return Success('登出成功')


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


@api.route("/modify_oj_username", methods=['POST'])
@login_required
def modify_oj_username_api():
    form = OJNameForm().validate_for_api()
    modify_oj_username(current_user.id, form.oj_id.data, form.username.data)
    return Success('修改成功')
