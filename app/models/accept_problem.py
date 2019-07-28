import datetime

from sqlalchemy import func
from app.models.base import db
from app.models.entity import AcceptProblem, Problem


def add_accept_problem(username, oj_id, problem_id):
    problem = AcceptProblem.query.filter_by(username=username, oj_id=oj_id, problem_id=problem_id).first()
    if not problem:
        with db.auto_commit():
            problem = AcceptProblem()
            problem.username = username
            problem.oj_id = oj_id
            problem.problem_id = problem_id
            problem.create_time = datetime.datetime.now()
            db.session.add(problem)


def get_accept_problem_list(username):
    return [i.problem_id for i in AcceptProblem.query.filter_by(username=username).all()]


def get_accept_problem_list_by_date(username, start_date, end_date):
    r = AcceptProblem.query.filter(
        AcceptProblem.username == username,
        AcceptProblem.create_time >= start_date,
        AcceptProblem.create_time <= end_date
    ).all()
    rr = []
    for i in r:
        rr.append({
            'oj_id': i.problem.oj_id,
            'oj_name': i.problem.oj.name,
            'problem_id': i.problem_id,
            'problem_pid': i.problem.problem_pid,
            'rating': i.problem.rating,
            'add_rating': i.add_rating,
            'create_time': i.create_time
        })
    return rr


def get_accept_problem_count_by_date(username, start_date, end_date):
    return AcceptProblem.query.filter(
        AcceptProblem.username == username,
        AcceptProblem.create_time >= start_date,
        AcceptProblem.create_time <= end_date
    ).count()


def get_accept_problem_distributed(username):
    return [{
        'oj_id': i[0],
        'accept_problem_count': i[1]
    } for i in
        db.session.query(Problem.oj_id, func.count(Problem.id)).join(AcceptProblem).filter(
            AcceptProblem.username == username
        ).group_by(Problem.oj_id).all()]


def delete_accept_problem_by_oj_id(username, oj_id):
    with db.auto_commit():
        AcceptProblem.query.filter_by(username=username).join(Problem).filter(
            Problem.oj_id == oj_id
        ).delete()


if __name__ == '__main__':
    from app import create_app

    with create_app().app_context():
        s = datetime.date.today()
    e = datetime.date.today() + datetime.timedelta(days=1)
    r = delete_accept_problem_list(1, 2)
    print(r)
