from flask_login import UserMixin
from sqlalchemy import Column, Integer, String

from app import login_manager
from app.libs.error_code import AuthFailed
from app.models.base import Base, db


class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True)
    password = Column(String(100))


def create_user(username, password):
    with db.auto_commit():
        user = User()
        user.username = username
        user.password = password
        db.session.add(user)
    return user


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def check_password(user, password):
    return user.password == password


@login_manager.user_loader
def get_user_by_user_id(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return AuthFailed()
