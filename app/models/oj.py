from sqlalchemy import Column, Integer, String

from app.models.base import Base, db


class OJ(Base):
    __tablename__ = 'oj'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True)


def get_oj_by_oj_id(oj_id):
    return OJ.query.get(oj_id).name


def get_all_oj():
    return [i.name for i in OJ.query.all()]


if __name__ == '__main__':
    from app import create_app

    with create_app().app_context():
        r = get_oj_by_oj_id(1)
    print(r)
