from app import login_manager
from app.libs.error_code import AuthFailed
from app.models.base import db
from app.models.entity import User


def create_user(username, nickname):
    with db.auto_commit():
        user = User()
        user.username = username
        user.nickname = nickname
        user.password = username
        user.permission = 0
        user.status = 1
        db.session.add(user)
    return user


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def check_password(user, password):
    return user.password == password


def modify_password(username, password):
    user = get_user_by_username(username)
    with db.auto_commit():
        user.password = password


def modify_user(user_id, nickname, permission, status):
    user = get_user_by_username(user_id)
    with db.auto_commit():
        user.nickname = nickname
        user.permission = permission
        user.status = status


def get_all_user():
    return [{
        'username': i.username,
        'nickname': i.nickname,
        'permission': i.permission,
        'status': i.status
    } for i in User.query.order_by(User.username).all()]


@login_manager.user_loader
def get_user_by_username(username):
    return User.query.get(username)


@login_manager.unauthorized_handler
def unauthorized_handler():
    return AuthFailed()


if __name__ == '__main__':
    from app import create_app

    with create_app().app_context():
        r = get_user_by_username('31702411')
        print(r)
        print(r.oj_username[0].oj_username)
