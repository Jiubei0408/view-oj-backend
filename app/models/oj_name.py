from sqlalchemy import Column, Integer, String

from app.models.base import Base, db


class OJName(Base):
    __tablename__ = 'oj_name'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    oj_id = Column(Integer)
    name = Column(String(100), unique=True)


def modify_oj_name(user_id, oj_id, name):
    oj_name = OJName.query.filter_by(user_id=user_id, oj_id=oj_id).first()
    if not oj_name:
        add_oj_name(user_id, oj_id, name)
    else:
        with db.auto_commit():
            oj_name.name = name


def add_oj_name(user_id, oj_id, name):
    with db.auto_commit():
        oj_name = OJName()
        oj_name.user_id = user_id
        oj_name.oj_id = oj_id
        oj_name.name = name
        db.session.add(oj_name)
