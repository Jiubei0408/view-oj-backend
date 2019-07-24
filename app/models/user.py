from flask_login import UserMixin
from sqlalchemy import Column, Integer, String

from app import login_manager
from app.libs.error_code import AuthFailed
from app.models.base import Base, db


class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(100), nullable=False)
    username = Column(String(100), unique=True)
    password = Column(String(100), nullable=False)
    permission = Column(Integer, nullable=False)


def create_user(username, password):
    with db.auto_commit():
        user = User()
        user.username = username
        user.password = password
        user.permission = 0
        db.session.add(user)
    return user


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def check_password(user, password):
    return user.password == password


def get_all_user():
    return [i.id for i in User.query.filter(User.permission != -1).all()]


@login_manager.user_loader
def get_user_by_user_id(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return AuthFailed()


if __name__ == '__main__':
    from app import create_app

    with create_app().app_context():
        r = get_all_user()
    print(r)
