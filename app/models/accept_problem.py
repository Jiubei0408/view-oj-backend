from sqlalchemy import Column, Integer, String

from app.models.base import Base, db


class AcceptProblem(Base):
    __tablename__ = 'accept_problem'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    oj_id = Column(Integer, nullable=False)
    problem_id = Column(String(100), nullable=False)


def add_accept_problem(user_id, oj_id, problem_id):
    with db.auto_commit():
        problem = AcceptProblem()
        problem.user_id = user_id
        problem.oj_id = oj_id
        problem.problem_id = problem_id
        db.session.add(problem)


def get_accept_problem_list(user_id, oj_id):
    return [i.problem_id for i in AcceptProblem.query.filter_by(user_id=user_id, oj_id=oj_id).all()]


def get_accept_problem_list_by_date(user_id, start_date, end_date):
    r = AcceptProblem.query.filter(
        AcceptProblem.user_id == user_id,
        AcceptProblem.create_time >= start_date,
        AcceptProblem.create_time <= end_date
    ).all()
    rr = []
    for i in r:
        rr.append({
            'oj_id': i.oj_id,
            'problem_id': i.problem_id
        })
    return rr


if __name__ == '__main__':
    from app import create_app

    with create_app().app_context():
        r = get_accept_problem_list(3, 1)
    print(r)
