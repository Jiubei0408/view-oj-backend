from sqlalchemy import Column, Integer, String

from app.models.base import Base, db


class OJ(Base):
    __tablename__ = 'oj'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True)


def get_oj_by_oj_id(oj_id):
    return OJ.query.filter_by(id=oj_id).first()
