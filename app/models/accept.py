from sqlalchemy import Column, Integer, String

from app.models.base import Base, db


class Accept(Base):
    __tablename__ = 'accept'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    oj_id = Column(Integer)
    problem_id = Column(String(100))


def add_accept(user_id, oj_id, problem_id):
    with db.auto_commit():
        accept = Accept()
        accept.user_id = user_id
        accept.oj_id = oj_id
        accept.problem_id = problem_id
        db.session.add(accept)


def get_accept_list(user_id, oj_id):
    return [i.problem_id for i in Accept.query.filter_by(user_id=user_id, oj_id=oj_id).all()]


def get_accept_list_by_date(user_id, start_date, end_date):
    r = Accept.query.filter(
        Accept.user_id == user_id,
        Accept.create_time >= start_date,
        Accept.create_time <= end_date
    ).all()
    rr = []
    for i in r:
        rr.append({
            'oj_id': i.oj_id,
            'problem_id': i.problem_id
        })
    return rr
