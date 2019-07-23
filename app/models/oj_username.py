from sqlalchemy import Column, Integer, String

from app.models.base import Base, db


class OJUsername(Base):
    __tablename__ = 'oj_username'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    oj_id = Column(Integer, nullable=False)
    username = Column(String(100), unique=True, nullable=False)


def modify_oj_username(user_id, oj_id, username):
    oj_username = OJUsername.query.filter_by(user_id=user_id, oj_id=oj_id).first()
    if not oj_username and username:
        add_oj_username(user_id, oj_id, username)
    else:
        with db.auto_commit():
            if username:
                oj_username.username = username
            else:
                db.session.delete(oj_username)


def add_oj_username(user_id, oj_id, username):
    with db.auto_commit():
        oj_username = OJUsername()
        oj_username.user_id = user_id
        oj_username.oj_id = oj_id
        oj_username.username = username
        db.session.add(oj_username)


def get_oj_username(user_id, oj_id):
    oj_username = OJUsername.query.filter_by(user_id=user_id, oj_id=oj_id).first()
    if oj_username:
        return oj_username.username


if __name__ == '__main__':
    from app import create_app

    with create_app().app_context():
        r = get_oj_username(3, 1)
    print(r)
