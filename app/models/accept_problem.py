import datetime

from sqlalchemy import func

from app.config.setting import DEFAULT_USER_RATING
from app.models.base import db
from app.models.entity import AcceptProblem, Problem


def create_accept_problem(username, problem_id, add_rating):
    if not AcceptProblem.query.filter_by(username=username, problem_id=problem_id).first():
        with db.auto_commit():
            r = AcceptProblem()
            r.username = username
            r.problem_id = problem_id
            r.add_rating = add_rating
            r.create_time = datetime.datetime.now()
            db.session.add(r)


def get_accept_problem_list_by_oj_id(username, oj_id):
    return [i.problem_pid for i in Problem.query.filter(
        Problem.oj_id == oj_id,
        Problem.id.in_(db.session.query(AcceptProblem.problem_id).filter_by(username=username).subquery())
    ).all()]


def get_accept_problem_list_by_date(username, start_date, end_date):
    return [{
        'oj_id': i.problem.oj_id,
        'oj_name': i.problem.oj.name,
        'problem_id': i.problem_id,
        'problem_pid': i.problem.problem_pid,
        'rating': i.problem.rating,
        'add_rating': i.add_rating,
        'create_time': i.create_time
    } for i in AcceptProblem.query.filter(
        AcceptProblem.username == username,
        AcceptProblem.create_time >= start_date,
        AcceptProblem.create_time <= end_date
    ).all()]


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
        AcceptProblem.query.filter_by(username=username).filter(
            AcceptProblem.problem_id.in_(db.session.query(Problem.id).filter_by(oj_id=oj_id).subquery())
        ).delete()


def get_rating_by_username(username):
    add_rating = db.session.query(func.sum(AcceptProblem.add_rating)).filter(
        AcceptProblem.username == username
    ).first()[0]
    if add_rating is None:
        add_rating = 0
    return DEFAULT_USER_RATING + add_rating


if __name__ == '__main__':
    from app import create_app

    with create_app().app_context():
        s = datetime.date.today()
        e = datetime.date.today() + datetime.timedelta(days=1)
        r = get_rating_by_username(31702411)
    print(r)
