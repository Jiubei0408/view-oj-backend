from flask import jsonify
from flask_login import current_user, login_required, login_user, logout_user

from app.libs.error_code import Success, AuthFailed
from app.libs.redprint import RedPrint

from app.models.user import get_user_by_username, check_password

from app.validators.forms import LoginForm

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
